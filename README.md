# sync_delete

Delete files in sync between two (or more) folders 

This guy here is a small project that I've coded in a day-ish to cover a need I've just made up in order to not start the big projects I have in mind. 

If you use a synchorization tool such as SyncBack or rsync or such, deleting files are a bit annoying. 

Either you need to delete the file from other folder manually every time, or you should set the action manual for cases where a file exists one side and does not exist on the other. Did you just created the file in the existing folder or deleted it from the other one? Sync software cannot know this (because they generally do not track the history of the files). If you automate the process, the file just gets copied from where it exists, to the other side.

To prevent this I've developed this simple script. 

Instead of deleting the file or the folder, you just rename it and add a predefined suffix to it (default is *__del*, you can change it in the script).

Script will scan all base folders you define for the files or folders with the designated suffix. It memorizes them and scans other base folders for the same file. Then move all files on a folder called *_deleted*, which can be found on their own base folder. It also suffixes the files with the date and time of deletion (well, of the move actually) so that it can be seen when the file has been deleted (moved). 

You can also change the folder that the files will be moved to(*_deleted* as default)

Maybe it is a little bit contradiction with the script's name, but this script does not delete any file. It just moves the files to another folder on your base folders. So any expression which includes word "delete" can be readed as "move"

Parameter details can be seen & changed within the code by you if you follow the code comments. 

I've tested the code on a Windows System. I did not test it for *nix and Os X systems, but since I've used python libraries for all file operations, I'd like to believe that it should work fine. 

If you have a question, or encounter a problem you can reach me through my Twitter account (@SercioSoydanov) or email (sercan.sydn@gmail.com)

# Usage

I personally use SyncBack for file synchronization between my two machines, which happens to have a very neat feature called *Programs - Before*. It conveniently runs a file or another software before (or after) the synchronization runs. I put the script on a folder which is defined in my path variable and SyncBack just fires it up before each time it runs the sync profile. And ta-daaa! The files that are supposed to be deleted has just been moved to the *_deleted* folder. Neat. 

# Renaming / Moving Files

Be careful renaming the files though, because this simple script does not track file renames. It would have been a nice feature, but it requires a whole new level of design and architecture. 

Plus to my knowledge, there is no Python library (though I may be wrong) to recognize a file by it's unique ID after a rename. 

It can be done by using an operation system's api calls, if you are interested here is a reference manual for Windows for *GetFileInformationByHandle* : 

https://docs.microsoft.com/tr-tr/windows/win32/api/fileapi/nf-fileapi-getfileinformationbyhandle?redirectedfrom=MSDN