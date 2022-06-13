# FileDownload
This is for downloading video files fromn cards to PC
It renames files to yyyy_mm_dd  format and stores that file has been downloaded



_Don't mess with the content of the files at C:\Users\<username>\AppData\Local\FileDownloads unless you are sure you know what you are doing._

__.FileDownloads.d__ is a SQLite database recording the files that have already been downloaded. If you delete it files may get downloaded twice if you haven't deleted them from the card. Their unique test is by file date, time and size.

Details of default values for folder locations and allowed file types are listed below:
These are created at first start (or again on next start if deleted) with default values set by the developer in them. One item to each line. _If you delete all the contents, the file will recreate with the default values._

__AllowedFiles.txt__ is the file extension for files types to be included. This includes regular video and sound formats. Code is case sensitive hence the upper and lower case. Any other files in the source folder will not appear in the Treeview or Download all option. Make sure to add '.' before extension

__LocationDestination.txt__ - the default path root to send your files to. On windows the would be C:\users\<username>\Videos, but change or add if another path is the usual choice

__LocationSource.txt__ - defaults as either F:\DCIM or G:\DCIM  but add another if there is another regularly used path
