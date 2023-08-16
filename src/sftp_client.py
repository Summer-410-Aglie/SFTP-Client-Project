import pysftp
import os 
from simple_term_menu import TerminalMenu

FORWARD_SLASH: str =                '/'

LIST_DIR_REMOTE: str =              'List remote directories'
LIST_FILE_REMOTE: str =             'List remote files'
LIST_DIR_LOCAL: str =               'List local directories'
CHANGE_DIR_REMOTE: str =            'Change remote directories'
CHANGE_DIR_LOCAL: str =             'Change local directories'
REMOVE_LOCAL: str =                 'Remove local files or directories'
REMOVE_DIR_REMOTE: str =            'Remove remote directories'
REMOVE_FILE_REMOTE: str =           'Remove remote files'
RENAME_REMOTE: str =                'Rename remote file or directory'
RENAME_REMOTE: str =                'Rename file or directory'
GET_FILE_REMOTE: str =				'Get remote file(s)'
CREATE_DIR_REMOTE: str =            'Create remote directory'
CREATE_DIR_LOCAL: str =             'Create local directory'
CURRENT_PATH: str =                 'Output current path'
EXIT: str =                         'Exit'
QUIT: str =                         'Quit'
RETURN: str =                       'Return'

OPTIONS: str = [
    LIST_DIR_REMOTE,
    LIST_FILE_REMOTE,
    CHANGE_DIR_REMOTE,
    LIST_DIR_LOCAL,
    CHANGE_DIR_LOCAL,
    REMOVE_LOCAL,
    REMOVE_DIR_REMOTE,
    REMOVE_FILE_REMOTE,
    RENAME_REMOTE,
    GET_FILE_REMOTE,
    CREATE_DIR_REMOTE,
    CREATE_DIR_LOCAL,
    CURRENT_PATH,
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
    
    def getRemoteWrapper(self) -> bool:
        self.listCurrentRemoteDir(includeFile=True)
        numFiles = int(input("How many files would you like to get?: "))
        srcs = []
        for i in range(numFiles):
            srcs.append(input(f'Which file would you like to get? ({i+1} of {numFiles}): '))
            
        srcPaths = [(self.getCurrentRemotePath() + FORWARD_SLASH + s) for s in srcs]
        
        return self.getManyRemoteFiles(srcPaths)
    
    # def getRemoteWrapper(self) -> bool:
    #     remote_options = self.getCurrentRemoteDir()
 
    #     menu = TerminalMenu(
    #         menu_entries=remote_options,
    #         title="Get remote files (To pick files click space, once finished click Enter)",
    #         multi_select=True
    #     )
    #     index_list = menu.show()
    #     choosen_dirs = list()
        
    #     for i in index_list:
    #         choosen_dirs.append(self.getCurrentRemotePath() + FORWARD_SLASH + remote_options[i])
            
    #     choosen_path = self.getLocalDir()
    #     print(data)
        
    #     return self.getManyRemoteFiles(choosen_dirs, choosen_path)
    #     pass    
    
    def getLocalDir(self, include_files: bool = True) -> str:        
        current_path = self.getCurrentLocalPath()
        while True:
            options = list()
            options.append('.')
            options = self.getCurrentLocalDir(include_files=include_files)
            options.append('..')
            options.append(QUIT)
            
            localPath = self.getCurrentLocalPath()
            menu = TerminalMenu(
                menu_entries=options,
                title="Current path: " + localPath + " (press space to navigate, to choose a folder press Enter)",
                accept_keys=("enter", " ")
            )
            
            index = menu.show()
            choosen_option = options[index]
            choosen_key = menu.chosen_accept_key
            
            if choosen_option == QUIT:
                return None
            
            if choosen_key == "enter":
                os.chdir(current_path)
                return self.getCurrentLocalDir() + FORWARD_SLASH + choosen_option
            pass
            
            new_path = os.path.join(localPath, choosen_option)
            if os.path.isdir(new_path):
                self.local_path = new_path 
                os.chdir(new_path) 
            
        pass
    

    def getRemoteFile(self, src: str, dest: str = None) -> bool:
        try:
            src = self.connection.normalize(src)
            if dest == ".":	dest = None
            self.connection.get(src, dest)
            return True
        except Exception as e:
            print(str(e))
            return False
    
    def getManyRemoteFiles(self, src: list[str], dest: str = None) -> bool:
        try:
            for index, file in enumerate(src):
                self.getRemoteFile(file, dest)
            return True
        except Exception as e:
            print(str(e), f"Failed to get file index number {index}")
            return False

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

    def removeLocalFileOrDir(self) -> bool:
        current_dir = self.getCurrentLocalDir()
        current_dir.append(QUIT)
        choosen_index = self.ChooseMenu(options=current_dir, title_name="Current path: " + self.getCurrentLocalPath())
        choosen_dir: str = current_dir[choosen_index]

        if choosen_dir == QUIT:
            return False
        
        fullPath = self.getCurrentLocalPath() + FORWARD_SLASH + choosen_dir

        if os.path.isfile(fullPath):
            return self.removeLocalFile(fullPath)
        else:
            return self.removeLocalDirectory(fullPath)
                 
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
        options = self.getCurrentRemoteDir()
        options.append(QUIT)
        index = self.ChooseMenu(options, "Removing remote file/directory")
        choosen = options[index]
        if choosen == QUIT: return False
        srcPath = self.getCurrentRemotePath() + FORWARD_SLASH + choosen
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
        options = self.getCurrentRemoteDir()
        options.append(QUIT)
        index = self.ChooseMenu(options, "Removing remote directory")
        choosen = options[index]
        if choosen == QUIT:
            return False
        srcPath = self.getCurrentRemotePath() + FORWARD_SLASH + choosen
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
        options = self.getCurrentRemoteDir()
        options.append(QUIT)
        index = self.ChooseMenu(options, "Renaming remote files and directory")
        choosen = options[index]
        if choosen == QUIT: return False
        dest = input('What would you like to rename to?: ')
        
        srcPath = self.getCurrentRemotePath() + '/' + choosen
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
    
    def getCurrentRemoteDir(self, include_files: bool = True) -> list:    
        """Gets a list of current remote directory

        :param include_files: if True includes files else if False not include files, defaults to True
        :type include_files: bool, optional
        :return: list of current remote directory
        :rtype: list
        """                 
    
        items = self.connection.listdir()
        if include_files == True:
            return items
        else:
            dir_items = list()
            for item in items:
                if self.connection.isdir(item):
                    dir_items.append(item)
            return dir_items
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
        
        while True:
            main_options = self.getCurrentRemoteDir()
            main_options.append("..")
            main_options.append(QUIT)
            options = self.getCurrentRemoteDir()
            options.append("..")
            options.append(QUIT)
            for i in range(len(options)):
                if self.connection.isdir(options[i]):
                    options[i] = options[i] + " - dir"
            current_path: str = self.connection.pwd
            
            menu = TerminalMenu(
                menu_entries=options,
                title="Current path: " + self.getCurrentRemotePath() + " (Changing directory)"
            )
            
            index = menu.show()
            choosen_option = main_options[index]       
            if choosen_option == QUIT:
                return None
            if self.connection.isdir(choosen_option):
                self.connection.chdir(choosen_option)
            
            pass

        pass

    def getCurrentLocalDir(self, include_files: bool = True) -> list:
        """Gets a list of contents in current local directory/files

        :param include_files: if True, files includes if False files not included, defaults to True
        :type include_files: bool, optional
        :return: A list current local directory
        :rtype: list
        """        

        items = os.listdir(self.local_path)  
        if include_files == True:
            return items
        else:
            dir_items = list()
            for item in items:
                full_path = os.path.join(self.local_path, item)
                if os.path.isdir(full_path):
                    dir_items.append(item)
            return dir_items   
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
        
        while True:
            main_options = self.getCurrentLocalDir(include_files=True)
            main_options.append("..")
            main_options.append(QUIT)
            
            temp_options = self.getCurrentLocalDir(include_files=True)
            temp_options.append("..")
            temp_options.append(QUIT)
            for i in range(len(temp_options)):
                full_path = self.getCurrentLocalPath() + FORWARD_SLASH + temp_options[i]
                if os.path.isdir(full_path):
                    temp_options[i] = temp_options[i] + " -dir"
            
            menu = TerminalMenu(
                menu_entries=temp_options,
                title="Current path: "+self.getCurrentLocalPath() + " (Changing local directory)"
            )
                   
            index = menu.show()
            choosen = main_options[index]
            
            if choosen == QUIT:
                return
            
            new_path = self.getCurrentLocalPath() + FORWARD_SLASH + choosen
            
            if os.path.isdir(new_path):
                os.chdir(new_path)
            pass

        pass

    def createRemoteDirectory(self) -> None:
        """creates a remote directory
        """        
        print("Current remote directory: ", self.getCurrentRemotePath())
        dir_name: str = input("Enter directory name you want to create: ")

        try:
            if dir_name in self.getCurrentRemoteDir():
                print("The directory ", dir_name, " already exists on the remote server!")
            else:
                self.connection.mkdir(dir_name)
                print("Directory '", dir_name, "' created successfully!")
        except Exception as e:
            print("Failed to create a directory!")

        pass

    def createLocalDirectory(self) -> None:
        """Creates local directory
        """        
        print("Current local directory: ", self.getCurrentLocalPath())
        dir_name: str = input("Enter directory name you want to create: ")

        try:
            if dir_name in self.getCurrentLocalDir(include_files=False):
                print("The directory ", dir_name, " already exists on the local server!")
            else:
                os.mkdir(dir_name)
                print("Directory '", dir_name, "' created successfully!")

        except Exception as e:
            print("Failed to create a directory!")
        pass

    def getCurrentRemotePath(self) -> str: 
        """Get current remote path
        """
        return self.connection.pwd
        
    def getCurrentLocalPath(self) -> str: 
        """Get current local path
        """
        return os.getcwd()
    
    def putRemote(self, fileName: str) -> bool:
        """Put file to remote Server
        """ 
        
        current_dir = self.getCurrentRemoteDir()
        try:
                self.connection.put(str,current_dir)
        except Exception as e:
            print(str(e))
            return ValueError('Unable to upload file. ')

        return True

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
        print("\n\n")
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
            elif entry == REMOVE_LOCAL: 
                self.removeLocalFileOrDir()
            elif entry == REMOVE_DIR_REMOTE:
                self.removeRemoteDirectoryWrapper()
            elif entry == REMOVE_FILE_REMOTE:
                self.removeRemoteFileWrapper()
            elif entry == RENAME_REMOTE: 
                self.renameRemoteWrapper()
            elif entry == GET_FILE_REMOTE:
                self.getRemoteWrapper()
            elif entry == CREATE_DIR_REMOTE:
                self.createRemoteDirectory()
            elif entry == CREATE_DIR_LOCAL:
                self.createLocalDirectory()
            elif entry == CURRENT_PATH:
                print('\nYour current remote path is: ' + self.getCurrentRemotePath() + '\n')
                print('\nYour current local path is: ' + self.getCurrentLocalPath() + '\n')
            elif entry == EXIT:
                return

            pass       

        pass

    pass
