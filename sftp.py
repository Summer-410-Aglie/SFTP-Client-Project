import sys
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




if __name__=='__main__':
    client: SFTPClient = login()
    if client.connect():
        client.get_remote_file("test.txt")
        client.get_remote_file("test2.txt", "./test2.txt")
        client.close()