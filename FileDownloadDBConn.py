import sqlite3
from datetime import datetime
import os

####################################################################
#
#
#
#
#
#
####################################################################


class FileDownloadDBConn:
    
    dbmsg = ''
    dbmsgUpdate = ''


    def __init__(self, db_name, db_path):

        #if not used before the db path will need to be checked and, if necessary created 
        if not os.path.exists(db_path + '\\'):
            os.makedirs(os.path.dirname(db_path + '\\'), exist_ok=True)
        dbName = os.path.join(db_path, db_name)

        #dbName = db_name

        self.dbConn = sqlite3.connect(dbName)  #   Open the database file connection
        self.cur = self.dbConn.cursor()  #   Open the database cursor
        self.dbOK = self.checkDB()

    def checkDB(self):
        #######################################################
        # on first use create DB, otherwise check DB, tables and indexes are all in place
        # added 26/2/22 JV
        # test if db exists
        #   if not create db and tables
        # return True if OK
        #   and .dbmsg with error or confirmation
        #######################################################
        allOK = False
        try:
            sSQL = ('CREATE TABLE IF NOT EXISTS tblFiles (fileID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,'
            'fileName TEXT NOT NULL, fileExt TEXT NOT NULL, fileSize INTEGER NOT NULL, fileDateCreated REAL NOT NULL, '
            'dateAdded REAL NOT NULL, newFileName TEXT NOT NULL)')
            self.cur.execute(sSQL)
            self.cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_files on tblFiles(fileName,filesize)')

            sSQL = "SELECT Count() as TotRecs FROM tblFiles"
            totRecs = self.cur.execute(sSQL).fetchone()[0]
            self.dbmsg = f'Database is OK. You have already downloaded {totRecs} files.'
            allOK = True
        except sqlite3.Error as er:
            self.dbmsg = ('SQLite error: %s' % (' '.join(er.args)))
            allOK = False
        
        return allOK
    
    def chkNotAlreadyinDB(self,fileName,filesize):
        #######################################################
        # added JV 18/5/22
        # check if file already in DB
        # Return True if not in db
        #######################################################
        sSQL = ('SELECT fileName, fileDateCreated FROM tblFiles WHERE fileName  = ? AND filesize = ?')
        self.cur.execute(sSQL,(fileName,filesize))
        fileData = self.cur.fetchall()
        if len(fileData) == 0 : # it hasn't been downloaded before
            return True
        else:
            return False
    
    def updateDB(self, fileName, fileExt, filesize, dateEarliest, newFileName):
        #######################################################
        # added JV 18/5/22
        # add file details to the db
        # return True if success
        #   and .dbmsg with error or confirmation
        #######################################################
        try:
            if self.chkNotAlreadyinDB(fileName,filesize):
                #Update DB with details of files copied
                sSQL = ('INSERT INTO tblFiles (fileName, fileExt, fileSize, fileDateCreated, dateAdded, newFileName) VALUES (?,?,?,?,?,?)')
                with self.dbConn:
                    self.cur.execute(sSQL,(fileName,fileExt,filesize, dateEarliest, datetime.today(), newFileName))
                    self.dbConn.commit()
                self.dbmsgUpdate = f'{fileName} has been recorded'
                return True
            else:
                #it has been downloaded before so no need to download again
                return False
        except sqlite3.Error as er:
            self.dbmsgUpdate = ('SQLite error: %s' % (' '.join(er.args)))

    def closeDB(self):
        self.dbConn.close()