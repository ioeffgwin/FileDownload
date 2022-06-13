import sys


def resource_path( relative_path):
    absolute_path = os.path.abspath(__file__)
    root_path = os.path.dirname(absolute_path)
    base_path = getattr(sys, 'MEIPASS', root_path)
    return os.path.join(base_path, relative_path)

from bdb import Breakpoint
#from importlib.abc import Traversable
from msilib.schema import CheckBox
from optparse import Values
from tkinter import filedialog as fd
from datetime import datetime
import subprocess
import time
import os
from tkinter import *
import tkinter
from tkinter.ttk import *
from tkinter.messagebox import showinfo
from turtle import bgcolor, color, width
from ttkwidgets import CheckboxTreeview
from tkinter import ttk
import tkinter.font as tkFont
import customtkinter as ctk
from FileDownloadConstants import FileDownloadConstants as constants
from FileDownloadDBConn import FileDownloadDBConn as dbconn
from FileDownloadFileMeta import FileDownloadFileMeta as FileMeta


####################################################################
# Main class to launch and set up interface for this app
# Check source and destination locations are valid
#   - either at start with default or with chosen location
# Populate tree with relevant files from source
# View file if double clicked (and VNC installed)
# Download selected files or Download all files
# Update database
# Reload tree to show remaining undownloaded files
####################################################################

# create the window
window = ctk.CTk()




# check if database available
dbchk = dbconn(db_name=constants().DB_NAME, db_path=constants().DB_PATH)
if dbchk.dbOK == False:
    # Database not available and won't create, so close
    # (This is pretty unlikely unless being run in read-only area)
    window.destroy()



# set up the window
window.title("Download video files from card to HDD")
window.geometry('800x800+120+120')
window.minsize(800,800)
iconpic = PhotoImage(file=resource_path('logo_1a.png'))
window.iconphoto(True, iconpic)

# constants kept elsewhere to make it easier to change them
PATH_CARD = constants().PATH_CARD
PATH_DEST = constants().PATH_DEST
FILE_TYPES = constants().FILE_TYPES

# add gui theme
ctk.set_appearance_mode("Dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(size=12)

#decided not to have label in row 0 but keep this in case change mind
#lbl = ctk.CTkLabel(window, text="Download video files") #, font=("Consolas", 18))
#lbl.config(anchor='e')
#lbl.grid(column=0, row=0, columnspan=5, sticky='w', padx=10)

#create text for labels
lbl1_text = tkinter.StringVar()
lbl1_text.set('Select the source and destination of your files if you want different from the default locations: ')
lbl2_text = tkinter.StringVar()
lbl2_text.set(dbchk.dbmsg)
txt1_text = tkinter.StringVar()
txt1_text.set(PATH_DEST)
txt2_text = tkinter.StringVar()
txt2_text.set(PATH_CARD)

#we need to give some colour to the treeview
treeStyle = ttk.Style()
treeStyle.theme_use("clam")
treeStyle.configure('Treeview.Heading', background='#5B97D3', foreground='#D5D9DE')
#treeStyle.configure('Treeview.Column', background='blue', foreground='silver')

#now we need to give user the option to choose which files
treeFrame = ctk.CTkFrame(window)
treeFrame.grid(column=0, row=7, columnspan=5, padx=15, pady=15, sticky='nsew')
treeColumns = ('file_name', 'file_size', 'file_folder', 'date_created')

#add scrollbars
myTree = CheckboxTreeview(treeFrame, columns=treeColumns, show=('headings','tree'))
scrollbarv = Scrollbar(treeFrame, orient=VERTICAL, command=myTree.yview)
scrollbarv.pack(side='right', fill = Y)
scrollbarh = Scrollbar(treeFrame, orient=HORIZONTAL, command=myTree.xview)
scrollbarh.pack(side='bottom', fill = X)
myTree.pack(side=LEFT, fill=BOTH, expand=TRUE)
myTree.configure(yscroll=scrollbarv.set)
myTree.configure(xscroll=scrollbarh.set)

# define headings
myTree.heading('file_name', text='File Name')
myTree.heading('file_size', text='File Size')
myTree.heading('file_folder', text='File Folder')
myTree.heading('date_created', text='Date Created')
myTree.column('file_name', width=220, minwidth=150)
myTree.column('file_size', width=100, minwidth=100, anchor='e')
myTree.column('file_folder', width=275, minwidth=250)
myTree.column('date_created', width=100, minwidth=75) # make this narrower than default

#make checkbox column narrower
myTree.column('#0',width=50, minwidth=50)

#create the labels - these give updates on progress
lbl1 = ctk.CTkLabel(window, textvariable=lbl1_text)
lbl1.config(anchor='w')
lbl1.grid(column=0, row=1, columnspan=5, sticky='w', padx=10, pady=10, ipadx=10, ipady=10)
lbl2 = ctk.CTkLabel(window, textvariable=lbl2_text)
lbl2.config(anchor='w')
lbl2.grid(column=0, row=2, columnspan=5, sticky='w', padx=10, pady=10, ipadx=10, ipady=10)

#create labels next to choose source and destination buttons shwoing current choice (or lack of)
txt2 = ctk.CTkLabel(window, textvariable=txt2_text)
txt2.config(anchor='w')
txt2.grid(column=1, row=3, columnspan=4, sticky='w', padx=10, pady=10, ipadx=10, ipady=10)
txt1 = ctk.CTkLabel(window, textvariable=txt1_text)
txt1.config(anchor='w')
txt1.grid(column=1, row=4, columnspan=4, sticky='w', padx=10, pady=10, ipadx=10, ipady=10)

#Create the buttons (they are fully configured later)
btn1 = ctk.CTkButton()
btn2 = ctk.CTkButton()
btn3 = ctk.CTkButton()
btn4 = ctk.CTkButton()
btn5 = ctk.CTkButton()

#add methods relating to buttons and treeview
def populateTree(path_to_files):
    #######################################################
    # populate treeview with data from FILE_CARD
    # 
    #######################################################
    for i in myTree.get_children():
        myTree.delete(i)

    treeData = []
    for root, dirs, files in os.walk(path_to_files):
        #for dir in dirs:
        for file in files:
            pathname = os.path.join(root,file)
            filedets = FileMeta(pathname)
            lbl2_text.set(f'Checking {pathname}...')
            lbl2.update()
            if filedets.FileExt in FILE_TYPES and filedets.alreadyinDB==False: #only look at the filetypes we want to download
                #download file to PATH_DEST
                treeData.append((filedets.FileName ,filedets.sizedesc,filedets.FileDirName,filedets.FileDate,filedets.filePath))
    for treeDat in treeData:
        myTree.insert('',END, values=treeDat)
    lbl2_text.set('  ')
    lbl2.update()


def downloadCheckedFiles():
    #######################################################
    # download selected files checked in treeview
    #
    #######################################################
    timestart = time.process_time()# check how long it takes to run
    global lbl1
    global lbl2
    chkFiles = myTree.get_checked()
    for chkFile in chkFiles:
        myFile = myTree.item(chkFile)
        pathname = myFile['values'][4]
        #get the file properties
        filedets = FileMeta(pathname)
        lbl1_text.set(f'Checking {pathname}...')
        lbl1.update()
        #download file to PATH_DEST
        lbl1_text.set(f'File {pathname} copying to {filedets.new_fileName}')
        lbl1.update()
        if filedets.copyFileToNew():    #successfule copying = True
            lbl2_text.set(filedets.updateDBmsg)
            lbl2.update()
            # update terminal
            lbl1_text.set(f'File {pathname} copied to {filedets.new_fileName}')
            lbl1.update()
            #Update DB with details of files copied
            filedets.updateDB()
            # update terminal
            lbl2_text.set(filedets.updateDBmsg)
            lbl2.update()
        else:
            lbl2_text.set(f'File {pathname} copy failed!')
            lbl2.update()

    for i in myTree.get_children():
        myTree.delete(i)
    populateTree(PATH_CARD)
    lbl1_text.set('  ')
    lbl1.update()

    # check how long it takes to run - delete when testing finished
    lbl2_text.set(f'Download finished in {time.process_time()-timestart} seconds.')
    lbl2.update()




def downloadAllFiles(path_to_files):
    #######################################################
    # iterate through source files and check against DB
    # If of correct type and not previously downloaded, 
    #   copy to new location and rename to yyyy\mm\yyyy_mm_dd_hhmmssfff
    #######################################################
    timestart = time.process_time()# check how long it takes to run
    global lbl1
    global lbl2
    for root, dirs, files in os.walk(path_to_files):
        #for dir in dirs:
        for file in files:
            pathname = os.path.join(root,file)
            filedets = FileMeta(pathname)
            lbl1_text.set(f'Checking {pathname}...')
            lbl1.update()
            #window.after(300) #slow down so that user can see some progress ;-)
            if filedets.FileExt in FILE_TYPES and filedets.alreadyinDB==False: #only look at the filetypes we want to download
                #download file to PATH_DEST
                # create new folders if needed
                os.makedirs(os.path.dirname(filedets.dest_fpath), exist_ok=True)
                #update terminal
                lbl1_text.set(f'File {pathname} copying to {filedets.new_fileName}')
                lbl1.update()
                if filedets.copyFileToNew():    #successfule copying = True
                    lbl2_text.set(filedets.updateDBmsg)
                    lbl2.update()
                    # update terminal
                    lbl1_text.set(f'File {pathname} copied to {filedets.new_fileName}')
                    lbl1.update()
                    #Update DB with details of files copied
                    filedets.updateDB()
                    lbl2_text.set(filedets.updateDBmsg)
                    lbl2.update()
                else:
                    lbl2_text.set(f'File {pathname} copy failed!')
                    lbl2.update()

    # update the tree
    populateTree(path_to_files)
    lbl1_text.set('  ')
    lbl1.update()

    # check how long it takes to run - delete when testing finished
    lbl2_text.set(f'Download finished in {time.process_time()-timestart} seconds.')
    lbl2.update()

def treeDoubleClick(self):
    #######################################################
    # opens video file in VLC when double clicked in the treeview
    # JV 19/5/22
    #######################################################
    #need to get the slashes in the right direction to pass the string to open file in VLC
    fileitem = myTree.item(myTree.selection()[0])
    filetoopen = fileitem['values'][4]
    filetoopen = filetoopen.replace('//','/')
    filetoopen = filetoopen.replace('/', '\\')
    #print(r'C:\Program Files\VideoLAN\VLC\vlc.exe ' + filetoopen)
    subprocess.run(r'"C:\Program Files\VideoLAN\VLC\vlc.exe" "' + filetoopen +'"', check=True)


def checkCardLoc():
    #######################################################
    # Check that the file start and finish locations are valid
    # if not ask for the path
    # exit code execution if no valid path given
    # call download method if valid paths given
    #######################################################
    chk1=False
    chk2=False
    
    global PATH_CARD
    global PATH_DEST
    global txt1
    global txt2

    # check to see if default PATH_DEST is there
    if isinstance(PATH_DEST,str):
        if os.path.exists(PATH_DEST) == False:
            txt1_text.set('No Path available to copy files to.')
            txt1.update()
            chk1=False
        
        else:
            txt1_text.set('Destination path is: ' + PATH_DEST)
            txt1.update()
            chk1=True
    else:
        for dest in PATH_DEST:
            if os.path.exists(dest):
                newPath_Dest = dest
                txt1_text.set('Destination path is: ' + newPath_Dest)
                txt1.update()
                PATH_DEST = newPath_Dest
                chk1=True
                break
        else:
            txt1_text.set('No Path available to copy files to.')
            txt1.update()
            chk1=False


    # check to see if default PATH_CARD is there
    if isinstance(PATH_CARD,str):
            if os.path.exists(PATH_CARD):
                txt2_text.set('Source path is: ' + PATH_CARD)
                txt2.update()
                chk2=True
            else:
                txt2_text.set('No Path available to copy files from.')
                txt2.update()
                chk2=False
    else:
        for card in PATH_CARD:
            if os.path.exists(card):
                newPath_Card = card
                txt2_text.set('Source path is: ' + newPath_Card)
                txt2.update()
                PATH_CARD = newPath_Card
                chk2=True
                break
        else:
            txt2_text.set('No Path available to copy files from.')
            txt2.update()
            chk2=False

    if chk1 and chk2:
        btn3.config(state='normal')
        btn4.config(state='normal')
        populateTree(PATH_CARD)
        lbl2_text.set(dbchk.dbmsg)
        lbl2.update()
    else:
        btn3.config(state='disabled')
        btn4.config(state='disabled')


def getCardLoc():
    #######################################################
    # Get the path of the files to be downloaded
    # added 28/2/22 JV
    #######################################################
    global PATH_CARD
    newPath_Card = fd.askdirectory(title="Path of files to be copied")
    if len(newPath_Card)==0:
        txt2_text.set('No Path available to copy files to.')
        txt2.update()
    else:
        txt2_text.set('Source path is: ' + newPath_Card)
        txt2.update()
        PATH_CARD = newPath_Card
    checkCardLoc() # check the card location is valid

def getDestLoc():
    #######################################################
    # Get the location files to be copied to
    # added 28/2/22 JV
    #######################################################
    global PATH_DEST
    newPath_Dest = fd.askdirectory(title="Path of final destination")
    if len(newPath_Dest)==0:
        txt1_text.set('Destination path is: ' + PATH_DEST)
        txt1.update()
    else:
        PATH_DEST = newPath_Dest
        txt1_text.set('Destination path is: ' + PATH_DEST)
        txt1.update()
    checkCardLoc() # check the destination location is valid


# This is called when close button hit
def theEnd():
    #######################################################
    # What happens when the close button gets hit
    #######################################################
    window.destroy()

# finished creating methods now finish getting the window open

#double click on tree item to open in default programme
myTree.bind('<Double-1>', treeDoubleClick)

#configure the buttons
btn1 = ctk.CTkButton(window, text="Locate source files", command=getCardLoc)
btn1.config(state='normal')
btn1.grid(column=0, row=3, sticky='ew', padx=10, pady=10, ipadx=10, ipady=10)
btn2 = ctk.CTkButton(window, text="Locate Destination files", command=getDestLoc)
btn2.config(state='normal')
btn2.grid(column=0, row=4, sticky='ew', padx=10, pady=10, ipadx=10, ipady=10)
btn3 = ctk.CTkButton(window, text="Download All files", command=lambda: downloadAllFiles(PATH_CARD))
btn3.config(state='disabled')
btn3.grid(column=0, row=9, sticky='ew', padx=10, pady=10, ipadx=10, ipady=10)
btn4 = ctk.CTkButton(window, text="Download Selected files", command=downloadCheckedFiles)
btn4.config(state='disabled')
btn4.grid(column=0, row=8, sticky='ew', padx=10, pady=10, ipadx=10, ipady=10)
btn5 = ctk.CTkButton(window, text="Close", command=theEnd)
btn5.grid(column=4, row=10, sticky='ew', padx=10, pady=10, ipadx=10, ipady=10)

# add weighting to the rows and columns so they resize nicely
window.grid_columnconfigure(0,weight=0)
window.grid_columnconfigure(1,weight=1)
window.grid_columnconfigure(2,weight=1)
window.grid_columnconfigure(3,weight=1)
window.grid_columnconfigure(4,weight=0)
window.grid_rowconfigure(0,weight=0)
window.grid_rowconfigure(1,weight=0)
window.grid_rowconfigure(2,weight=0)
window.grid_rowconfigure(3,weight=0)
window.grid_rowconfigure(4,weight=0)
window.grid_rowconfigure(5,weight=0)
window.grid_rowconfigure(6,weight=0)
window.grid_rowconfigure(7,weight=5)
window.grid_rowconfigure(8,weight=0)
window.grid_rowconfigure(9,weight=0)
window.grid_rowconfigure(10,weight=0)
treeFrame.grid_columnconfigure(0,weight=1)
treeFrame.grid_rowconfigure(0, weight=1)
#opened db earlier, now close it
dbchk.closeDB()
# check if card and destination locations are valid
checkCardLoc()

#leave at bottom so that code loops round and goes again to check for changes
window.mainloop()

