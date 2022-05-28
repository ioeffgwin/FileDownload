import os
import os.path

####################################################################
#
#
#
#
#
#
####################################################################



class FileDownloadConstants :
    userhome = os.path.expanduser('~') # find the user home dir

    PATH_CARD = [r'F:\DCIM',r'E:\DCIM'] # default paths to search for source files

    PATH_DEST = r'D:\Public\Videos' # root of destination on local machine

    PATH_DEST_ALT = os.path.join(userhome,r'Videos') # This should probably be the default for users videos

    FILE_TYPES = ['.mp4', '.mov', '.aac', '.svg', '.avi', '.3gp', '.MP4', '.MOV', '.AAC', '.SVG','.AVI'] # video and sound. could also add jpg and raw formats?

    DB_NAME = '.FileDownloads.d' #  Not an obvious name for a database
    DB_PATH = os.path.join(userhome, r'AppData\Local\FileDownloads') # default to Appdata (no slashes at either end)
    #DB_FULL = os.path.join(DB_PATH, DB_NAME) #not using this in the code

    # not likely to need these, but....
    def addPathCard(self, newValue):
        # append new path to the list
        self.PATH_CARD.append(newValue)
        #print(FileDownloadConstants().PATH_CARD)

    def setPathDest(self, newValue):
        #set new destination path
        self.PATH_DEST = newValue

    def addFileTypes(self,newValue):
        # append new filetype to the list
        self.FILE_TYPES.append(newValue)

    def setDBName(self,newValue):
        # create a new default db name
        # (this won't rename any existing)
        self.DB_NAME = newValue
        #print(self.DB_NAME)

    def setDBPath(self,newValue):
        # create a new default db path
        # (this won't rename any existing)
        self.DB_PATH = newValue
        #print(self.DB_FULL)

    
#    def __init__(self):
#        #   Constants
#        self.PATH_CARD = PATH_CARD

    


    
