import pysftp
import os 
from simple_term_menu import TerminalMenu

FORWARD_SLASH: str =                '/'

LIST_DIR_REMOTE: str =              'List remote directories'
LIST_FILE_REMOTE: str =             'List remote files'
LIST_DIR_LOCAL: str =               'List local directories'
CHANGE_DIR_REMOTE: str =            'Change remote directories'
CHANGE_DIR_LOCAL: str =             'Change local directories'
REMOVE_DIR_REMOTE: str =            'Remove remote directories'
RENAME_REMOTE: str =                'Rename file or directory'
CURRENT_REMOTE_PATH: str =          'Output current remote path'
EXIT: str =                         'Exit'
QUIT: str =                         'Quit'
RETURN: str =                       'Return'

OPTIONS: str = [
    LIST_DIR_REMOTE,
    LIST_FILE_REMOTE,
    CHANGE_DIR_REMOTE,
    LIST_DIR_LOCAL,
    CHANGE_DIR_LOCAL,
    REMOVE_DIR_REMOTE,
    RENAME_REMOTE,
    CURRENT_REMOTE_PATH,
    EXIT
    ]

class SFTPClient:
    """ A wrapper class for SFTP Client
    """    
    def __init__(
            self,
            host_name: str,
            user_name: str,
            password: str,
    ) -> None:
        """Constructs the necessary data for the SFTP client object.

        :param host_name: host name or IP address
        :type host_name: str
        :param user_name: user name for the host id
        :type user_name: str
        :param password: password for the user name
        :type password: str
        """          

        self.host_name: str = host_name
        self.user_name: str = user_name
        self.password: str = password

        self.local_path: str = '.'
        pass

    def connect(self) -> bool:
        """Establishes the SFTP connection

        :return: connection was successful or not
        :rtype: bool
        """
        try:      
            self.connection = pysftp.Connection(host=self.host_name, username=self.user_name, password=self.password)
        except Exception as e:
            return False
            pass
        
        return True

    def close(self) -> bool:
        """"Closes the established SFTP connection

        :return: disconnection was successful or not
        :rtype: bool
        """
        try:        
            self.connection.close()
        except Exception as e:
            return False
        
        return True
    
    def get_remote_file(self, src: str, dest: str = None) -> None:
        try:
            src = self.connection.normalize(src)
            if dest == ".":	dest = None
            self.connection.get(src, dest)
        except Exception as e:
            print(str(e))
        pass
    
    def get_many_remote_files(self, src: list[str], dest: str = None) -> None:
        pass

    def removeLocalFile(self, fileNamePath: str) -> bool:
        """Remove the local file

        :return: remove file from local server
        :rtype: bool
        """
        try: 
            os.remove(fileNamePath)
        except OSError as e:
            print(str(e))
            return ValueError('Unable to remove: ' + fileNamePath)
        
        return True
    
    def removeLocalDirectory(self, directoryNamePath: str) -> bool:
        """Remove the local directory. Directory must be empty

        :return: remove directory from local server
        :rtype: bool
        """
        try: 
            os.rmdir(directoryNamePath)
        except OSError as e:
            print(str(e))
            return ValueError('Unable to remove directory ' + directoryNamePath)
        
        return True
    
    def removeRemoteFileWrapper(self) -> bool:
        self.listCurrentRemoteDir(includeFile=True)
        src = input('what file would you like to remove? ')
        srcPath = self.getCurrentRemotePath() + FORWARD_SLASH + src
        return self.removeRemoteFile(srcPath)
    
    def removeRemoteFile(self, fileName: str) -> bool: 
        """Remove the remote file

        :return: remove file from remote server
        :rtype: bool
        """
        try:
            self.connection.remove(fileName)
        except Exception as e:
            print(str(e))
            return ValueError('Unable to remove file: ' + fileName)

        return True

    def removeRemoteDirectoryWrapper(self) -> bool:
        self.listCurrentRemoteDir(includeFile=False)
        src = input('what directory would you like to remove? ')
        srcPath = self.getCurrentRemotePath() + FORWARD_SLASH + src
        return self.removeRemoteDirectory(srcPath)
    
    def removeRemoteDirectory(self, dirName: str) -> bool: 
        """Remove the remote directory

        :return: remove directory from remote server
        :rtype: bool
        """
        try:
            self.connection.rmdir(dirName)
        except Exception as e:
            print(str(e))
            return ValueError('Unable to remove directory: ' + dirName)

        return True

    def renameRemoteWrapper(self) -> bool: 
        """Rename the file or directory on a remote host (WRAPPER)
        """
        self.listCurrentRemoteDir(includeFile=True)
        self.listCurrentRemoteDir(includeFile=False)
        src = input('what file or directory would you like to rename?')
        dest = input('What would you like to rename to?')
        srcPath = self.getCurrentRemotePath() + '/' + src
        destPath = self.getCurrentRemotePath() + '/' + dest
        self.renameRemote(srcPath, destPath)
        print('changing from: ' + srcPath + ' to ' + destPath)
        return True
    
    def renameRemote(self, src, dest):
        """Rename the file or directory on a remote host
        
        :return: rename file or directory from remote server
        :rtype: bool
        """
        try:
            self.connection.rename(src, dest)
        except Exception as e:
            print(str(e))
            return ValueError('Unable to rename file or directory: ' + src + ' to: ' + dest)
        
        return True
      
    def renameLocal(self, src, dest) -> bool:
        """Rename the file or directory on the local server

        :return: rename the file/directory or not
        :rtype: bool
        """
        try: 
            os.rename(src, dest)
        except FileNotFoundError as e:
            return FileNotFoundError(f"{src} does not exist")

        return True
    
    def getCurrentRemoteDir(self) -> list:    
        """Gets a list of contents in current remote directory

        :return: list of files/folder names
        :rtype: list
        """          
        # return self.connection.listdir()
        return self.connection.listdir()
        pass

    def listCurrentRemoteDir(self, includeFile) -> None:
        """List all the current content of current remote directory
        """
        if includeFile == True: 
            for i in self.getCurrentRemoteDir():
                path = self.getCurrentRemotePath() + FORWARD_SLASH + i
                if self.connection.isfile(path) == True:
                    print(i)
        elif includeFile == False:      
            for i in self.getCurrentRemoteDir():
                path = self.getCurrentRemotePath() + FORWARD_SLASH + i
                if self.connection.isfile(path) == False:
                    print(i)
        pass

    def changeCurrentRemoteDir(self) -> None:
        """Changes remote directory
        """   
        current_dir = self.getCurrentRemoteDir()
        current_dir.append("..")
        current_dir.append(RETURN)
        current_path: str = self.connection.pwd
        choosen_index = self.ChooseMenu(options=current_dir, title_name="Current path: " + current_path)
        choosen_dir: str = current_dir[choosen_index]
        
        if choosen_dir == RETURN:
            return None
        if self.connection.isdir(choosen_dir) or choosen_dir == "..":
            self.connection.chdir(choosen_dir)
        pass

    def getCurrentLocalDir(self) -> list:
        """Gets a list of contents in current local directory

        :return: list of files/folder names
        :rtype: list
        """        
        return os.listdir(self.local_path)
        pass

    def listCurrentLocalDir(self) -> None:
        """List all the current content of current local directory
        """ 
        list_dir = self.getCurrentLocalDir()
        for i in list_dir:
            print(i)

        pass

    def changeCurrentLocalDir(self) -> None:
        """Changes local directory
        """
        options = self.getCurrentLocalDir()
        options.append("..")
        options.append(RETURN)
        choosen_index = self.ChooseMenu(options=options, title_name="Current Path: " + self.local_path)
        
        if options[choosen_index] == RETURN:
            return None
        
        new_path = os.path.join(self.local_path, options[choosen_index])
        
        if os.path.isdir(new_path):
            self.local_path = new_path

        return
        pass

    def getCurrentRemotePath(self) -> str: 
        """Get current remote path
        """
        return self.connection.pwd


    def ChooseMenu(self, options: list, title_name: str = "MENU") -> int:
        """Allows you to choose from list of options

        :param options: the data to display
        :type options: list
        :param title_name: the title you want to have for the menu, defaults to "MENU"
        :type title_name: str, optional
        :return: the choosen menu
        :rtype: int
        """        
        terminal_menu: TerminalMenu = TerminalMenu(
        menu_entries=options,
        title=title_name,
        )
        return terminal_menu.show()
        pass

    def mainMenu(self) -> None:
        """Menu for this class
        """        
        exit_flag: bool = False 

        while not exit_flag:
            index: int = self.ChooseMenu(OPTIONS, "User Name: "+ self.user_name+" Host: "+ str(self.host_name))
            entry = OPTIONS[index]
            if entry == LIST_DIR_REMOTE:
                self.listCurrentRemoteDir(includeFile=False)
                pass
            elif entry == LIST_FILE_REMOTE:
                self.listCurrentRemoteDir(includeFile=True)
            elif entry == CHANGE_DIR_REMOTE:
                self.changeCurrentRemoteDir()
                pass
            elif entry == LIST_DIR_LOCAL:
                self.listCurrentLocalDir()
            elif entry == CHANGE_DIR_LOCAL:
                self.changeCurrentLocalDir()
            elif entry == REMOVE_DIR_REMOTE:
                self.removeRemoteDirectoryWrapper()
            elif entry == RENAME_REMOTE: 
                self.renameRemoteWrapper()
            elif entry == CURRENT_REMOTE_PATH:
                print('Your current remote path is:' + self.getCurrentRemotePath())
            elif entry == EXIT:
                return
                pass

            pass       

        pass

    pass
