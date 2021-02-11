import argparse
import os
import sys
import subprocess
import requests

from git import Repo
import keyboard
from colorama import init
from cryptography.fernet import Fernet
from termcolor import colored

"""
Suported languages: 
    .python
    .c
    .haskell
    .java 

Arguments : 
    -n * --name
    -l * --language
    -e * --editor
    -p * --path (optional)
    -g --git
    -h --help 
    
nerv -l python3 -e vscode -g gpl3
"""    

init()
key = True

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", type = str, required = True, help = "Project Name")
parser.add_argument("-l", "--language", type = str, required = True, help = "Coding Language" )
parser.add_argument("-e", "--editor", type = str, required = True, help = "Text Editor")
parser.add_argument("-p", "--path", type = str, required = False, help = "Project Path")

group = parser.add_mutually_exclusive_group()
group.add_argument("-g", "--git", action = "store_true", help = "Create Repository")

args = parser.parse_args()

# print(args.name, args.language, args.editor, args.path)

class bcolors:
    
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
    
    global key
    # Info message
    print("\nLooks like this is your first time using Nerv-Launch.")
    print("In order to continue, please, complete the setup. Keep in mind that this is only required one time.\n")
    
    while True:
        
        # Get user name for greetings
        user = input(f"{bcolors.OKGREEN}[1]{bcolors.ENDC} User: ")
        if not user.strip(): # Check if it is not an empty string
            print(colored("Please enter a username.\n","yellow")) 
        
        # Get default editor
        editor = input(f"{bcolors.OKGREEN}[2]{bcolors.ENDC} Default code editor: ")
        if not editor.strip(): # Check for empty string
            print(colored("Please enter a default code editor.\n","yellow"))
        else:
            break
    
    while True:
        
        # Use github for project
        o = input(f"{bcolors.OKGREEN}[3]{bcolors.ENDC} Do you wish to have access to Github when creating a new project ? (y/n) ")
        if o == 'y' or o =='n':
            break
        else:
            print(colored("Please select an option.\n","yellow"))
            
    
    if o == "y": 
        
        try:
            
            username = input(f"  {bcolors.WARNING}(*){bcolors.ENDC} Please enter your Github username : ")
            token = input(f"  {bcolors.WARNING}(*){bcolors.ENDC} Please provide your authentication token for your Github account : ")
            
            # Sets the api token as an env variable.
            if 'GIT_TOKEN' in os.environ:
                x = input(print("\n{bcolors.WARNING}(!){bcolors.ENDC} Environmental variable already existent please rename it.\n(!) Do you wish to use it ? (y/n)","yellow"))

                while True: 
                    if x == 'y' or x == 'n':
                        if x == 'y':
                            print(colored("\nUsing existing token.\n","yellow"))
                            print(colored("To change the token run the command [nerv --token].\n","yellow"))
                            break
                        else:
                            print(colored("Sugestion : rename the variable on ~/.bashrc ","red"))
                            input("Press Enter To Exit...")
                            sys.exit()
                    else:
                        pass

            else: 
                os.system(f"echo 'export GIT_TOKEN='{token}'' >> ~/.bashrc")
                print(colored("\nThe token has been saved as an environmental variable.","yellow"))
                print(colored("To change the token run the command [nerv --token].\n","yellow"))
                print(colored("Restart your terminal.\n","red"))
               
            file = open("log.txt","w")
            file.write(f"{user}\n{editor}\n{username}") # Username , default editor, Github name
            file.close()
            
            print(colored("Setup finished.\n","green"))
            sys.exit()
            
        except Exception as e:
            
            print(colored(f"An error has occured:\n[{e}]","yellow"))
            print(colored("Something went wrong.","red"))
            sys.exit()
                
    else: 
        with open("log.txt","w") as f:
            f.write(f"{user}\n{editor}")
            f.close()
        
        key = False
        
        print(colored("\nSetup finished.\n","green"))
          
def check_lan(lan):
    if lan == 'python3':
        if os.system("python --version > /dev/null") != 0:
            print(colored("Language/Compiler not installed.","yellow"))
            return False
        else: 
            return True
                
    elif lan == 'haskell':
        if os.system("ghci --version > /dev/null") != 0: 
            print(colored("Language/Compiler not installed.","yellow"))
            return False
        else: 
            return True
            
    elif lan == 'c':
        if os.system("gcc --version > /dev/null") != 0:
            print(colored("Language/Compiler not installed.","yellow"))
            return False
        else: 
            return True
        
    elif lan == 'java':
        if os.system("java -version > /dev/null") != 0:
            print(colored("Language/Compiler not installed.","yellow"))
            return False
        else: 
            return True
        
    else: 
        print(colored("Language not suported.\n Use [nerv -h] to check all the supported languages.","yellow"))
        return False

# Creating the new project folder
def new_folder(path,name):
    # Changing into the given path.
    os.chdir(os.getcwd() if path == "." else path)
    
    # Tries to create a folder with the args.name if FileExistsError is raised than ends the program.
    try:
        print(colored("Creating project folder:","green"))
        os.mkdir(name)
    except FileExistsError:
        print(colored(f"The directory '{name}' already exists, please remove it or change the project name.","red"))
    
    print(" {bcolors.WARNING}.{bcolors.ENDC}src")
    os.mkdir(f"{name}/src") # Create 'src' folder 
    print(" {bcolors.WARNING}.{bcolors.ENDC}docs")
    os.mkdir(f"{name}/docs") # Create 'docs' folder
    print(" {bcolors.WARNING}.{bcolors.ENDC}lib")
    os.mkdir(f"{name}/lib") # Create 'lib' folder

def git():
    
    # Opens the log.txt file to read the github username.
    with open("log.txt","r") as file:
        info = file.read().split('\n')
        file.close()
    
    git_user = info[-1] # Github username.
    
    print("\n Creating new repository...")
    
    # Gets the token saved as env variable.
    GIT = os.environ.get("GIT_TOKEN")
    API_URL = "https://api.github.com" # API base url, useless when in this format.
    payload = '{"name": "' + args.name + '", "private": false }' # Data about the new repository such as name and privacy.

    # Authentication on the API using the OAuth token provided by the user on the setup.
    headers = {
        "Authorization": "token " + GIT,
        "Accept": "application/vnd.github.v3+json"
    } 

    # POST request on the API. 
    r = requests.post(API_URL + "/user/repos", data = payload, headers = headers)

    if r.status_code != 201: # 201 is the OK code, meaning the repository has been created.
        print(colored(f"Something went wrong - Error {r.status_code}","red"))
    else:
        print(f"{bcolors.OKGREEN}  ʟ Repository created :{bcolors.ENDC} https://github.com/{git_user}/{args.name} ")
    
    print(colored("\n Starting up your project :\n"))

    # Project build up
    os.chdir(os.path.expanduser("~")) # Changing to root directory.
    os.chdir(os.getcwd() if args.path == "." else args.path) # Changes the directory to clone the repository.
    
    try: 
        # Cloning the repository
        print("  ʟ Cloning the repository..")
        os.system(f"git clone -q https://{GIT}@github.com/gweebg/{args.name}.git 2>&1 | grep -v 'warning: You appear to have cloned an empty repository.'")
        print("    ʟ Successful\n")

    except Exception as e:
        # Catching exceptions.
        print(colored(f"An exception has occured :\n{e}"))
        input("Press Enter To Exit...")
        sys.exit()

    # Adding folders and README.md
    print("  ʟ Adding files..")
    os.mkdir(f"{args.name}/src") # src
    os.system(f'touch {args.name}/src/README.md') # README
    os.system(f"echo '# Source code' >> {args.name}/src/README.md") # README update


    os.mkdir(f"{args.name}/docs") # docs
    os.system(f'touch {args.name}/docs/README.md') 
    os.system(f"echo '# Documentation' >> {args.name}/docs/README.md") 

    os.mkdir(f"{args.name}/lib") # lib
    os.system(f'touch {args.name}/lib/README.md') 
    os.system(f"echo '# Libs' >> {args.name}/lib/README.md") 

    os.system(f'touch {args.name}/README.md') 
    os.system(f"echo '# {args.name}' >> {args.name}/README.md")

    print("    ʟ Successful\n ")

    # Pushing to the repository
    print("  ʟ Pushing to remote..")
    os.chdir(os.path.expanduser("~")) # Goes to root
    os.chdir(f"{args.path}/{args.name}") # Goes to new repo folder.
    subprocess.run(["git","add","."],stdout=subprocess.DEVNULL)
    subprocess.run(["git","commit","-m","Init"],stdout=subprocess.DEVNULL)

    try:
        subprocess.run(["git","push","-q", f"https://{GIT}@github.com/gweebg/{args.name}.git"],stdout=subprocess.DEVNULL)
        print("    ʟ Successful\n ")
        print(colored(" Project created.","green"))

    except Exception as ex: 
        print(colored(f"An exception has occured while pushing to remote :\n{ex}"))
        input("Press Enter To Exit...")
        sys.exit()



def create_venv(lan):
    if lan == "python3": 
        os.chdir(f"{args.path}/agrs.name") # Creates a virtual environment for python 
        
        # os.system() return an exit code, 0 is successful any other code are failures, thus the verification of os.system() != 0.
        if os.system("python3 -m venv env") != 0: 
            # If virtualenv is not installed, asks to install it.
            print("The Python module required to initalize the virtual environment is not installed.\n Do you wish to install it? (y/n)\n")
            
            # Waits for 'y' to get pressed, if so downloads and installs virtualenv, otherwise aborts the process.
            while True: 
                try:
                    if keyboard.is_pressed('y'):
                        print("Installing virtualenv...")
                        if os.system("pip3 install virtualenv") != 0:
                            print("An error occured while installing virtualenv.\nAborting...")
                        else:
                            print("virtualenv installed successfully.")
                        break
                except:
                    print("Aborting...")
                    break
        else: 
            os.system("python3 -m venv env")
    
if __name__ == "__main__":
    if os.path.isfile("log.txt"):
        # Meter tudo aqui sem o setup
        git()
        pass
    else: 
        setup()
        # Meter tudo o resto 

