import sys
import os 
import subprocess

import requests
from colorama import init
from termcolor import colored

class colors:
    
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[33m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def setup():

    # Info message
    print("\nLooks like this is your first time using Nerv-Launch.")
    print("In order to continue, please, complete the setup. Keep in mind that this is only required one time.\n")
    
    while True:
        
        # Get user name for greetings
        user = input(f"{colors.OKGREEN}[1]{colors.ENDC} User: ")
        if not user.strip(): # Check if it is not an empty string
            print(colored("Please enter a username.\n","yellow")) 
        
        # Get default editor
        editor = input(f"{colors.OKGREEN}[2]{colors.ENDC} Default code editor: ")
        if not editor.strip(): # Check for empty string
            print(colored("Please enter a default code editor.\n","yellow"))
        else:
            break
    
    while True:

        # Use github for project
        o = input(f"{colors.OKGREEN}[3]{colors.ENDC} Do you wish to have access to Github when creating a new project ? (y/n) ")
        if o == 'y' or o =='n':
            break
        else:
            print(colored("Please select an option.\n","yellow"))
            
    
    if o == "y": 
        
        try:
            
            username = input(f"  {colors.WARNING}(*){colors.ENDC} Please enter your Github username : ")
            token = input(f"  {colors.WARNING}(*){colors.ENDC} Please provide your authentication token for your Github account : ")
            
            # Sets the api token as an env variable.
            if 'GIT_TOKEN' in os.environ:
                x = input(f"\n{colors.WARNING}(!){colors.ENDC} Environmental variable already existent please rename it.\n{colors.WARNING}(!){colors.ENDC} Do you wish to use it ? (y/n)")

                while True: 

                    x = input(f"\n{colors.WARNING}(!){colors.ENDC} Environmental variable already existent please rename it.\n{colors.WARNING}(!){colors.ENDC} Do you wish to use it ? (y/n) ")
                    
                    if x == 'y' or x == 'n':
                        break
                    else:
                        print(colored("\nPlease select an option.","yellow"))

                if x == 'y':
                    print(colored(f"\nUsing existing token.","yellow"))
                    print(colored("To change the token run the command [nerv --token].\n","yellow"))
                else:
                    print(colored("\nRename or delete the variable on ~/.bashrc\nOnce that's done, restart the terminal. ","red"))
                    input("\nPress Enter To Exit...")
                    sys.exit()

            else: 
                os.system(f"echo 'export GIT_TOKEN='{token}'' >> ~/.bashrc")
                print(colored("\nThe token has been saved as an environmental variable.","yellow"))
                print(colored("To change the token run the command [nerv --token].\n","yellow"))
                print(colored("Restart your terminal.\n","red"))
               
            file = open("log.txt","w")
            file.write(f"{user}'s Profile :\n{editor}\n{username}") # Username , default editor, Github name
            file.close()
            
            print(colored("Setup finished.\n","green"))
            input("Press Enter To Exit...")
            sys.exit()
            
        except Exception as e:
            
            print(colored(f"An error has occured:\n[{e}]","yellow"))
            print(colored("Something went wrong.","red"))
            input("Press Enter To Exit...")
            sys.exit()
                
    else: 
        with open("log.txt","w") as f:
            f.write(f"{user}\n{editor}")
            f.close()
        
        print(colored("\nSetup finished.\n","green"))