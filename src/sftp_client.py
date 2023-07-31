import pysftp

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
            print(str(e))
            return False
        
        return True
        pass

    def close(self) -> bool:
        """"Closes the established SFTP connection

        :return: disconnection was successful or not
        :rtype: bool
        """
        try:        
            self.connection.close()
        except Exception as e:
            print(str(e))
            return False
        
        return True
        pass

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