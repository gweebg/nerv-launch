import sys
import os 
import subprocess
import json

import requests
from colorama import init
from termcolor import colored

"""
This module is responsible for the 
initial setup that is required in order 
to use Github on your projects.
"""

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

def setup(): # Setup function 
    
    # Info message
    print("\nLooks like this is your first time using Nerv-Launch.")
    print("In order to continue, please, complete the setup. Keep in mind that this is only required one time.\n")
    
    while True:
        
        # Get user name used on profile managing.
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

        # Use github for project ? 
        o = input(f"{colors.OKGREEN}[3]{colors.ENDC} Do you wish to have access to Github when creating a new project ? (y/n) ")
        if o == 'y' or o =='n':
            break
        else:
            print(colored("Please select an option.\n","yellow"))
            
    
    if o == "y": 
        
        try:
            
            # Taking the Github username as well as the OAuth token.
            username = input(f"  {colors.WARNING}(*){colors.ENDC} Please enter your Github username : ")
            token = input(f"  {colors.WARNING}(*){colors.ENDC} Please provide your authentication token for your Github account : ")
            
            """
            The setup() function will only execute if the value 'setup' on  
            'config.json' is set to 'True'. 
            But that doesn't mean that the script hasn't been run at least once,
            meaning that there could be a GIT_TOKEN env variable already set.
            So, first, we need to check it, if it has the variable, we ask if 
            the user wants to use it or not.
            """
            
            if 'GIT_TOKEN' in os.environ: # Checks for already existing variable.
                
                # Do you want to use the exsiting variable ? 
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
                
                # Saving the token at .bashrc if there isn't a GIT_TOKEN variable.
                # os.system(f"echo 'export GIT_TOKEN='{token}'' >> ~/.bashrc")
                store_var = f'''echo 'export GIT_TOKEN='{token}'' >> ~/.bashrc'''
                subprocess.run(store_var, shell = True , stdout = subprocess.DEVNULL)
                print(colored("\nThe token has been saved as an environmental variable.","yellow"))
                print(colored("To change the token run the command [nerv --token].\n","yellow"))
                print(colored("Restart your terminal.\n","red"))
            
            # Logs the user information into "config.json" .
            with open("config.json","r") as f:
                config = json.load(f)
                
            config["profile_name"] = user
            config["default_editor"] = editor
            config["github_name"] = username
            config["setup"] = "True"
                
            with open("config.json","w") as f:
                json.dump(config,f)
            
            print(colored("Setup finished.\n","green"))
            input("Press Enter To Exit...")
            sys.exit()
            
        except Exception as e:
            
            print(colored(f"An error has occured:\n[{e}]","yellow"))
            print(colored("Something went wrong.","red"))
            input("Press Enter To Exit...")
            sys.exit()
                
    else: 
        # Only runs if the user doesn't want to use Github.
        with open("config.json","w") as f:
            config = json.load(f)
            
        config["profile_name"] = user
        config["default_editor"] = editor
        
        with open("config.json","w") as f:
            json.dump(config,f)
        
        print(colored("\nSetup finished.\n","green"))

