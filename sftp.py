import sys
from os import path, getcwd
from getpass import getpass
from src.sftp_client import SFTPClient


def login() -> SFTPClient:
    """Collects user input for host, username, and password and creates an SFTPClient

    :return: SFTPClient object with the entered data
    :rtype: SFTPClient
    """    
    user: str = input("Username: ")
    host: str = input("host: ")
    pwd = getpass("password: ")
    return SFTPClient(host_name=host, user_name=user, password=pwd)

def get_directories_from_user() -> tuple[str]:
    print("\nEnter the desired FULL paths AND file names:")
    print("(Press ENTER/RETURN immediately if the current " + 
    	"working directory is desired.)\n")
    src: str = path.normpath(input("Source path and file name: "))
    dst: str = path.normpath(input("Destination path and file name: "))
    
    return src, dst



if __name__=='__main__':
    client: SFTPClient = login()
    if client.connect():
        src, dst = get_directories_from_user()
        client.get_remote_file(src, dst)
        
        client.close()