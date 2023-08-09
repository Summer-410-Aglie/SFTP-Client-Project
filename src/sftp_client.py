import pysftp
import os 
from simple_term_menu import TerminalMenu


LIST_DIR: str =         '[1] List directories'
CHANGE_DIR: str =       '[2] Change directories'
EXIT: str =             '[3] Exit'

OPTIONS: str = [
    LIST_DIR,
    CHANGE_DIR,
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
    
    def getRemoteFile(self, src: str, dest: str = None) -> None:
        try:
            src = self.connection.normalize(src)
            if dest == ".":	dest = None
            self.connection.get(src, dest)
        except Exception as e:
            print(str(e))
        pass
    
    def getManyRemoteFiles(self, src: list[str], dest: str = None) -> None:
        try:
            for file, index in enumerate(src):
                self.getRemoteFile(file, dest)
        except Exception as e:
            print(str(e), f"Get failed on file index number {index}")
        pass

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

    def listCurrentDir(self) -> list:
        return self.connection.listdir()
        pass

    def changeDir(self):
        current_dir = self.listCurrentDir()
        current_dir.append("Quit")
        current_path: str = self.connection.pwd
        choosen_index = self.ChooseMenu(options=current_dir, title_name="Current path: " + current_path)
        if choosen_index == len(current_dir) -1:
            return
        self.connection.chdir(current_dir[choosen_index])
        print(self.listCurrentDir())
        pass



    def ChooseMenu(self, options: list, title_name: str = "MENU") -> int:
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

            if OPTIONS.index(LIST_DIR) == index:
                print(self.listCurrentDir())  
                for i in self.listCurrentDir():
                    print(i)
                pass
            elif OPTIONS.index(CHANGE_DIR) == index:
                self.changeDir()
                pass
            elif OPTIONS.index(EXIT) == index:
                return
                pass

            pass       

        pass


    


    pass
