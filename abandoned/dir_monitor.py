import os
import win32file
import datetime
import win32con


ACTIONS = {
  1 : "Created",
  2 : "Deleted",
  3 : "Updated",
  4 : "Renamed from something",
  5 : "Renamed to something"
}

FILE_LIST_DIRECTORY = win32con.GENERIC_READ | win32con.GENERIC_WRITE
path_to_watch = r"C:\FineReport_10.0"
hDir = win32file.CreateFile (
  path_to_watch,
  FILE_LIST_DIRECTORY,
  win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
  None,
  win32con.OPEN_EXISTING,
  win32con.FILE_FLAG_BACKUP_SEMANTICS,
  None
)

if __name__ == '__main__':
    print("begin")
    while 1:
        print(datetime.datetime.now())
        results = win32file.ReadDirectoryChangesW (
                                               hDir,  #handle: Handle to the directory to be monitored. This directory must be opened with the FILE_LIST_DIRECTORY access right.
                                               1024,  #size: Size of the buffer to allocate for the results.
                                               True,  #bWatchSubtree: Specifies whether the ReadDirectoryChangesW function will monitor the directory or the directory tree. 
                                               win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                                                win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                                                win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                                                win32con.FILE_NOTIFY_CHANGE_SIZE |
                                                win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                                                win32con.FILE_NOTIFY_CHANGE_SECURITY,
                                               None,
                                               None)
        for action, file in results:
            full_filename = os.path.join (path_to_watch, file)
            print (full_filename, ACTIONS.get (action, "Unknown"))