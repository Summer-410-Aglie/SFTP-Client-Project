import pysftp
import os 
from simple_term_menu import TerminalMenu


LIST_DIR_REMOTE: str =              'List remote directories'
LIST_DIR_LOCAL: str =               'List local directories'
CHANGE_DIR_REMOTE: str =            'Change remote directories'
CHANGE_DIR_LOCAL: str =             'Change local directories'
EXIT: str =                         'Exit'
QUIT: str =                         'Quit'
RETURN: str =                       'Return'

OPTIONS: str = [
    LIST_DIR_REMOTE,
    CHANGE_DIR_REMOTE,
    LIST_DIR_LOCAL,
    CHANGE_DIR_LOCAL,
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

    def listCurrentRemoteDir(self) -> None:
        """List all the current content of current remote directory
        """      
        for i in self.getCurrentRemoteDir():
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
                self.listCurrentRemoteDir()
                pass
            elif entry == CHANGE_DIR_REMOTE:
                self.changeCurrentRemoteDir()
                pass
            elif entry == LIST_DIR_LOCAL:
                self.listCurrentLocalDir()
            elif entry == CHANGE_DIR_LOCAL:
                self.changeCurrentLocalDir()

            elif entry == EXIT:
                return
                pass

            pass       

        pass

    pass
