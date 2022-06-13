#from dataclasses import Field
import os
from datetime import datetime
import shutil
from FileDownloadDBConn import FileDownloadDBConn as DBConn
from FileDownloadConstants import FileDownloadConstants

class FileDownloadFileMeta :
        #######################################################
    #   Extract meta data from file
    #   Added actions for copy, new files names etc.
    #######################################################


    def __init__(self, path_to_file):
        #######################################################
        #Get metadata from source files to be used to rename 
        #   and store information in database
        #   Get date to be used in new name and build string to be used
        #######################################################

        path_dest = FileDownloadConstants().PATH_DEST

        path = path_to_file # not sure why I created this! (So i didn't have to keeping typing path_to_file)
        self.filePath = path
        self.filesize = os.path.getsize(path) #returns the size of the file
        self.DateCreated = os.path.getctime(path) #returns the file creation date (equals to last modified date in Unix systems like macOS)
        self.DateLastModified = os.path.getmtime(path) #returns the file last modified date
        if self.DateCreated < self.DateLastModified: #Returns the earliest date of modified or created
            self.DateEarliest = self.DateCreated
        else:
            self.DateEarliest = self.DateLastModified
        FilePathName, self.FileExt = os.path.splitext(path) # splits file suffixe from filepath
        self.FileName = os.path.basename(path) #get filename inc suffix
        self.FileDirName = os.path.dirname(path)

        mydb = DBConn(db_name=FileDownloadConstants().DB_NAME, db_path=FileDownloadConstants().DB_PATH)
        self.alreadyinDB = not mydb.chkNotAlreadyinDB(self.FileName,self.filesize)
        mydb.closeDB

        # get constituent parts of date for filepath\filename string
        t_date = datetime.fromtimestamp(self.DateEarliest)
        t_day = t_date.strftime('%d')
        t_month = t_date.strftime('%m')
        t_year = t_date.strftime('%Y')
        t_hour = t_date.strftime('%H')
        t_mins = t_date.strftime('%M')
        t_secs = t_date.strftime('%S')
        t_msecs = t_date.strftime('%f')

        self.dest_fpath = f"{path_dest}\\{t_year}\\{t_year}_{t_month}_{t_day}\\"
        self.new_fileName = f"{path_dest}\\{t_year}\\{t_year}_{t_month}_{t_day}\\{t_year}_{t_month}_{t_day}_{t_hour}{t_mins}{t_secs}{t_msecs}{self.FileExt}"

        self.FileDate = f'{t_day}/{t_month}/{t_year}'

        self.filemsg = ""
        self.updateDBmsg = ""

        self.sizedesc = self.displayFileSize(self.filesize)


    def updateDB(self):
        #######################################################
        #  Update the database with details of files being downloaded
        #
        #######################################################
        mydb = DBConn(db_name=FileDownloadConstants().DB_NAME, db_path=FileDownloadConstants().DB_PATH)
        mydb.updateDB(self.FileName,self.FileExt,self.filesize,self.DateEarliest,self.new_fileName)
        self.updateDBmsg = mydb.dbmsgUpdate
        mydb.closeDB

    def displayFileSize(self,filesize):
        #######################################################
        # return the file size as string with MB, GB as appropriate
        #  use in treeview
        #######################################################
        ans = ""
        if filesize < 1024 :
            ans = f'{round(filesize,2):,} B'
        elif filesize > 1024-1 and filesize <(1024*1024) < 1:
            ans = f'{round(filesize/1024,2):,} KB'
        elif filesize > (1024*1024)-1 and filesize <(1024*1024*1024):
            ans = f'{round(filesize/(1024*1024),2):,} MB'
        else:
            ans = f'{round(filesize/(1024*1024*1024),2):,} GB'
        return ans




    def copyFileToNew(self):
        #######################################################
        #  Copy file from source to new location with new name
        #
        #######################################################
        try:
            #copy to the new destination
            # create new folders if needed
            os.makedirs(os.path.dirname(self.dest_fpath), exist_ok=True)
            # copy file
            shutil.copy2(self.filePath,self.new_fileName)
            self.fileCopymsg = f'{self.new_fileName} successfully copied'
            return True
        except os.error as er:
            self.fileCopymsg = ('OS error: %s' % (' '.join(er.args)))
            return False
