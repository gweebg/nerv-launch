import argparse
import os
import sys
import subprocess
import requests

from git import Repo
import keyboard
import stdiomask
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
            key = Fernet.generate_key() # secret key for encription 
            
            f = Fernet(key)
            encrypted = f.encrypt(b"{token}")
            
            # decrypted_message = f.decrypt(encrypted_message)

            # print(decrypted_message.decode())
            
            file = open("log.txt","w")
            e = encrypted.decode("utf-8")
            file.write(f"{e}\n{user}\n{editor}\n{username}")
            file.close()
            
            file = open("key.key","w") 
            file.write(key.decode('utf-8'))
            
            print(colored("\nSetup finished.\n","green"))
            
        except Exception as e:
            
            print(colored(f"An error has occured:\n[{e}]","yellow"))
            print(colored("Something went wrong.","red"))
            sys.exit()
                
    else: 
        with open("log.txt","w") as f:
            f.write(f"{user}\n{editor}")
            f.close()
        
        ghub = False
        
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
    
    print("\n")

    with open("log.txt","r") as file:
        info = file.read().split('\n')
        file.close()
     
    with open("key.key","r") as keyf:
        key = keyf.read()
        keyf.close()
    
    f = Fernet(key)
    t = (info[0]).encode("utf-8")

    token = (f.decrypt(t)).decode('utf-8')
    token = token.replace('{','')
    token = token.replace('}','')
    
    git_user = info[-1]
    
    #print(f"{token}\n{user}\n{editor}\n{git_user}") 
    print("Creating new repository...")
    #token = "ab819535bdbecf678475e90390441772e9049e7e" 
    #TODO TOKEN MAL FORMATADO

    API_URL = "https://api.github.com"
    payload = '{"name": "' + args.name + '", "private": true }'
    headers = {
        "Authorization": "token " + token,
        "Accept": "application/vnd.github.v3+json"
    } 

    r = requests.post(API_URL + "/user/repos", data = payload, headers = headers)

    if r.status_code != 201: 
        print(colored(f"Something went wrong - Error {r.status_code}","red"))
    else:
        print(colored(f"Repository created : https://github.com/{git_user}/{args.name} ","green"))

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
    
# if __name__ == "__main__": 
#     if check_lan(args.language):
#         print("Language available.")
#         # Creates the project folder.
#         new_folder(args.path,args.name)
#         #if args.git then git() else pass
       
if __name__ == "__main__":
    if os.path.isfile("log.txt"):
        # Meter tudo aqui sem o setup
        git()
        pass
    else: 
        setup()
        git()
        # Meter tudo o resto 

    

# g = Github(token)
#     print("instacia criada",g)
#     u = g.get_user()
#     print(u)
    
#     try:
#         repo = u.create_repo(
#             args.name,
#             allow_rebase_merge = True,
#             auto_init = False,
#             description = f"{args.name} repository.",
#             has_projects = False,
#             license_template = "gpl-3.0",
#             private = True
#         )
#     except Exception as e:
#         print(e)