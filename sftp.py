import sys
from getpass import getpass
from src.sftp_client import SFTPClient
from simple_term_menu import TerminalMenu


LOGIN: str =        'Login'
PICK_SAVED: str =   'Pick from saved account'
EXIT: str =         'Exit'


def login() -> SFTPClient:
    """Collects user input for host, username, and password and creates an SFTPClient

    :return: SFTPClient object with the entered data
    :rtype: SFTPClient
    """    
    user: str = input("Username: ")
    host: str = input("host: ")
    pwd = getpass("password: ")

    response = input("Would you like to save the login information? [y/n]: ")
    if response[0] == 'Y' or response == 'y':
        print("your login information have been saved!")        
        pass

    return SFTPClient(host_name=host, user_name=user, password=pwd)
    pass

def exampleListAccounts():
    login_1 = {
        "username":"user1",
        "host":"www.example.com",
        "password":"pAssWOrD!"
    }
    
    login_2 = {
        "username":"user2",
        "host":"192.000.000.00",
        "password":"PassCode"
    }

    login_3 = {
        "username":"user3",
        "host":"linux.cs.pdx.edu",
        "password":"passWORD"
    }

    options = [str(login_1), str(login_2), str(login_3), "Quit"]
    terminal_menu: TerminalMenu = TerminalMenu(
        menu_entries=options,
        title="Saved login info"
        )
    menu_entry_index = terminal_menu.show()



    pass



def menu():
    options = [LOGIN, PICK_SAVED, EXIT]
    terminal_menu: TerminalMenu = TerminalMenu(
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
            exampleListAccounts()
            pass
        elif menu_entry == EXIT:
            exit_flag = True
            pass

        pass
    pass




if __name__=='__main__':
    
    # try:
    #     int("not a number")
    # except Exception as e:
    #     # print(str(e))
    #     pass
    
    menu()