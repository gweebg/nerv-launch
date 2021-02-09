import argparse
import os
import sys

import github
import keyboard
import stdiomask
from colorama import init
from cryptography.fernet import Fernet
from github import Github
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
    # ask for github token 
    # ask for default editor
    # save in file encripted 
    # example : token
    # check if .txt file exists then skip setup else run setup
    print("\nLooks like this is your first time using Nerv-Launch.")
    print("In order to continue complete the setup. Keep in mind that this is only required one time.\n")
    

    while True:
        
        user = input(f"{bcolors.OKGREEN}[1]{bcolors.ENDC} User: ")
        if not user.strip():
            print(colored("Please enter a username.\n","yellow"))
        
        editor = input(f"{bcolors.OKGREEN}[2]{bcolors.ENDC} Default code editor: ")
        if not editor.strip():
            print(colored("Please enter a default code editor.\n","yellow"))
        else:
            break
    
    while True:
        
        o = input(f"{bcolors.OKGREEN}[3]{bcolors.ENDC} Do you wish to have access to Github when creating a new project ? (y/n) ")
        if o == 'y' or o =='n':
            break
        else:
            print(colored("Please select an option.\n","yellow"))
    
    if o == "y": 
        
        try:
            
            token = input(f"  {bcolors.WARNING}(*){bcolors.ENDC} Please provide your authentication token for your Github account : ")
            key = Fernet.generate_key() # secret key for encription 
            
            f = Fernet(key)
            encrypted = f.encrypt(b"{token}")
            
            # decrypted_message = f.decrypt(encrypted_message)

            # print(decrypted_message.decode())
            
            file = open("log.txt","w")
            file.write(f"{str(encrypted)}\n{user}\n{editor}")
            file.close()
            
            print(colored("\nSetup finished.","green"))
            
        except Exception as e:
            
            print(colored(f"An error has occured:\n[{e}]","yellow"))
            print(colored("Something went wrong.","red"))
            sys.exit()
                
    else: 
        print(colored("Aborting ...", "red"))
        sys.exit()
        
            
def check_lan(lan):
    if lan == 'python3':
        if os.system("python --version > /dev/null") != 0:
            print("Language/Compiler not installed.")
            return False
        else: 
            return True
                
    elif lan == 'haskell':
        if os.system("ghci --version > /dev/null") != 0: 
            print("Language/Compiler not installed.")
            return False
        else: 
            return True
            
    elif lan == 'c':
        if os.system("gcc --version > /dev/null") != 0:
            print("Language/Compiler not installed.")
            return False
        else: 
            return True
        
    elif lan == 'java':
        if os.system("java -version > /dev/null") != 0:
            print("Language/Compiler not installed.")
            return False
        else: 
            return True
        
    else: 
        print("Language not suported.\n Use [nerv -h] to check all the supported languages.")
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
        raise Exception("Duplicate name, choose another name.")
    
    print(" .src")
    os.mkdir(f"{name}/src") # Create 'src' folder 
    print(" .docs")
    os.mkdir(f"{name}/docs") # Create 'docs' folder
    print(" .lib")
    os.mkdir(f"{name}/lib") # Create 'lib' folder

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
    
def git():
        
    # Asking for credentials 
    print("GitHub login:")
    username = input("Username: ")
    pwd = stdiomask.getpass()
    
    try:
        # Github instance using username and password
        hub = Github(username,pwd, retry = 3) # After 3 tries 
        user = hub.get_user()

        try:
            user.login()
            repo = user.create_repo(args.name)
            print("Repo created")
        
        except github.GithubException as e:
            print(e.status)
            print(colored("Something went wrong.","red"))
            
    except github.GithubException.RateLimitExceededException as e:
        print(e.status)
        print(colored("Rate limit exceeded.","red"))
        
    except github.GithubException.TwoFactorException as ex: 
        print(ex.status)
        print(colored("Please disable two factor authentication.","red"))
        
    # not working yet, user auth token instead 
    # read and decrpyt the auth token from log.txt 
    # solution might be not using Github api but shell commands using the token 
    # commit the folder where the repo is created

# if __name__ == "__main__": 
#     if check_lan(args.language):
#         print("Language available.")
#         # Creates the project folder.
#         new_folder(args.path,args.name)
#         #if args.git then git() else pass
        
setup()
    

