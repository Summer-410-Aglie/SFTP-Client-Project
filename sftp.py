#! /usr/bin/python3
import sys
from getpass import getpass
from src.sftp_client import SFTPClient
from src.LoginInfoManager import LoginInfoManager
from simple_term_menu import TerminalMenu


LOGIN: str =        'Login'
PICK_SAVED: str =   'Pick from saved account'
DEL_SAVED: str =    'Delete a saved account'
EXIT: str =         'Exit'
QUIT: str =         'Quit'
RETURN: str =       'Return'

def login() -> SFTPClient:
    """Collects user input for host, username, and password and creates an SFTPClient

    :return: SFTPClient object with the entered data
    :rtype: SFTPClient
    """    
    user: str = input("Username: ")
    host: str = input("host: ")
    pwd = getpass("password: ")

    response = input("Would you like to save the login information? [y/n]: ")
    if len(response) < 1:
        response = 'n'
    if response[0] == 'Y' or response == 'y':
        manager = LoginInfoManager()
        result = manager.addLoginInfo(user_name=user, host=host, password=pwd)
        if result == True:
            print("your login information have been saved!")
        else:
            print("This login already exist.")        
        pass

    return SFTPClient(host_name=host, user_name=user, password=pwd)

def pickFromSaved() -> dict:
    """Allows you to pick from saved connections/account

    :return: picked connection/account
    :rtype: dict
    """    
    manager = LoginInfoManager()
    all_login = manager.getAllLoginInfo()
    options = list()
    for i in all_login:
        options.append(str(i))
    options.append(RETURN) # allows you to exit

    terminal_menu = TerminalMenu(
        menu_entries=options,
        title="Saved login Info"
    )
    menu_entry_index = terminal_menu.show()

    if options[menu_entry_index] == RETURN:
        return None
    else:
        choosen_login: dict = all_login[menu_entry_index]
        client: SFTPClient = SFTPClient( 
            host_name=choosen_login.get('host'),
            user_name=choosen_login.get('username'),
            password=choosen_login.get('password')
        )
        return client

def deleteFromSaved() -> None:
    """Allows you to delete from saved connections/account
    """    
    manager = LoginInfoManager()
    all_login = manager.getAllLoginInfo()
    options = list()
    for i in all_login:
        options.append(str(i))
    options.append(RETURN) # allows you to return

    terminal_menu = TerminalMenu(
        menu_entries=options,
        title="Saved login Info"
    )
    menu_entry_index = terminal_menu.show()

    if options[menu_entry_index] == RETURN:
        return None
    else:
        choosen_login: dict = all_login[menu_entry_index]
        result = manager.deleteLoginInfo(choosen_login)
        if result == True:
            print("Selected account has been deleted!")
        else:
            print("Selected account has not been deleted!")
    return None


def menu() -> None:
    """menu interface login
    """    
    options = [LOGIN, 
               PICK_SAVED,
               DEL_SAVED, 
               EXIT]
    terminal_menu: TerminalMenu = TerminalMenu(  #Menu Window
        menu_entries=options,
        title="MAIN MENU"
        )
    exit_flag: bool = False

    while not exit_flag:
        menu_entry: str = options[terminal_menu.show()]
        if menu_entry == LOGIN:
            client: SFTPClient = login()
            result = client.connect()
            if result == False:
                print("LOGIN FAILED!, please try again.")
            else:
                client.mainMenu()
                client.close()
        elif menu_entry == PICK_SAVED:
            client: SFTPClient = pickFromSaved()
            if client != None:
                result = client.connect()
                if result == False:
                    print("LOGIN FAILED!, please try again.")
                else:
                    client.mainMenu()
                    client.close()
            pass
        elif menu_entry == DEL_SAVED:
            deleteFromSaved()
        elif menu_entry == EXIT:
            exit_flag = True
            pass

        pass
    pass




if __name__=='__main__':
    menu()