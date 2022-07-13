from genericpath import getsize
import os
import os.path

####################################################################
#   Class used to set defaults at start of app
#   gets Card Path, Location Path
#   database Name and location
#   allowed file types - puts defaults in memory rather than having 
#     to read databases or files each time
#   Used in other classes
#   Also makes it easier for future development to change these defaults!
####################################################################

def getSourceList(file_loc, source_loc):
    #Read LocationSource.txt file to get list
    #check if file exists
    path_to_file = os.path.join(file_loc,r'LocationSource.txt')
    if os.path.exists(path_to_file) and os.path.getsize(path_to_file) != 0:
        #if it does read contents
        my_file = open(path_to_file, "r")
        return my_file.read().splitlines()
    else :
        from pathlib import Path
        Path(file_loc).mkdir(parents=True, exist_ok=True) #create filedownloads path if doesn't exist
        my_file = open(path_to_file, "a")
        for element in source_loc:
            my_file.write (element + '\n')
        return source_loc
        #return my_file.read().splitlines()
            


def getDestinationList(file_loc, dest_loc):
    #Read LocationDestination.txt file to get list
    #check if file exists
    path_to_file = os.path.join(file_loc,r'LocationDestination.txt')
    if os.path.exists(path_to_file) and os.path.getsize(path_to_file) != 0:
        #if it does read contents
        my_file = open(path_to_file, "r")
        return my_file.read().splitlines()
    else :
        my_file = open(path_to_file, "a")
        for element in dest_loc:
            my_file.write (element + '\n')
        return dest_loc
        #return my_file.read().splitlines()


def getRequiredFileTypes(file_loc, file_types):
    #Read AllowedFiles.txt file to get list
    #check if file exists
    path_to_file = os.path.join(file_loc,r'AllowedFiles.txt')
    if os.path.exists(path_to_file) and os.path.getsize(path_to_file) != 0:
        #if it does read contents
        my_file = open(path_to_file, "r")
        return my_file.read().splitlines()
    else :
        my_file = open(path_to_file, "a")
        for element in file_types:
            my_file.write (element + '\n')
        #my_file.close() 
        return file_types   
        #return my_file.read().splitlines()

def cleanList(a_list):
    # Filter out empty strings from a list
    filter_object = filter(lambda x: x != "", a_list)

    without_empty_strings = list(filter_object)

    return without_empty_strings



class FileDownloadConstants :
    userhome = os.path.expanduser('~') # find the user home dir (e.g. C:\users\username)

    #Default locations and file tuypes are stored at C:\Users\username\AppData\Local\FileDownloads 

    #This is the default card locations used to create txt file. The user can override in the LocationSource.txt file if they wish
    pathCard = [r'F:\DCIM',r'E:\DCIM'] # default paths to search for source files

    # This is the developers default video location (variable not used in production)
    pathDest = [r'D:\Public\Videos'] # root of destination on local machine

    #This is the default video location (C:\users\username\videos) used to create txt file. The user can override in the LocationDestination.txt file if they wish
    PATH_DEST_ALT = [os.path.join(userhome,r'Videos')] # This should probably be the default for users videos

    #These are the default file types used to create txt file. The user can override in the allowedfiles.txt file if they wish
    # video and sound. could also add jpg and raw formats?
    # currently lower and upper case as code is case sensitive
    fileTypes = ['.mp4', '.mov', '.aac', '.svg', '.avi', '.3gp', '.wav', '.MP4', '.MOV', '.AAC', '.SVG','.AVI', '.WAV']
    
    
    DB_NAME = '.FileDownloads.d' #  Not an obvious name for a database. Can't be changed without rebuilding build
    DB_PATH = os.path.join(userhome, r'AppData\Local\FileDownloads') # default to Appdata (no slashes at either end)
    #DB_FULL = os.path.join(DB_PATH, DB_NAME) #not using this in the code

    PATH_CARD = cleanList(getSourceList(DB_PATH, pathCard))
    PATH_DEST = cleanList(getDestinationList(DB_PATH, PATH_DEST_ALT))
    FILE_TYPES = cleanList(getRequiredFileTypes(DB_PATH, fileTypes))
    #print(pathCard)
    #print(pathDest)
    #print(fileTypes)

    # These aren't being used in the build at the moment 
    def setDBName(self,newValue):
        # create a new default db name
        # (this won't rename any existing)
        self.DB_NAME = newValue
        #print(self.DB_NAME)

    def setDBPath(self,newValue):
        # create a new default db path (and location of default constant values)
        # (this won't rename any existing)
        self.DB_PATH = newValue
        #print(self.DB_FULL)



    
