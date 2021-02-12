import argparse
import os
import string
import subprocess
import sys
from argparse import RawTextHelpFormatter

import requests
from colorama import init
from termcolor import colored

"""
Arguments : 
    -n * --name (Project name)
    -l --license (Project license)
    -e * --editor (Code editor)
    -p * --path (Project path)
    -g --git (Disable repository creation)
    -h --help  (Help)
    -q --quiet (Runs the code quietly)
"""    

# Inits colorama colors.
init()
directory = os.getcwd()

# Redirect stdout to /dev/null
# https://codereview.stackexchange.com/questions/25417/is-there-a-better-way-to-make-a-function-silent-on-need
class NoStdStreams(object):
    def __init__(self,stdout = None, stderr = None):
        self.devnull = open(os.devnull,'w')
        self._stdout = stdout or self.devnull or sys.stdout
        self._stderr = stderr or self.devnull or sys.stderr

    def __enter__(self):
        self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
        self.old_stdout.flush(); self.old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr

    def __exit__(self, exc_type, exc_value, traceback):
        self._stdout.flush(); self._stderr.flush()
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        self.devnull.close()

# Terminal colors.
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

# Class for changing the Github token.
class chToken(argparse.Action):

    def token(self):
        print(colored("\nChanging Github OAuth token : ","green"))

        # Asking for the new token, gets stored on new_token variable.
        new_token = input(f"{bcolors.OKGREEN}(+){bcolors.ENDC} Please submit your new Github OAuth token : ")

        # Changing into the home directory and deleting the old token.
        os.chdir(os.path.expanduser("~")) # dir = ~ 
        
        # Deletes the old token from .bashrc
        try:
            with open(".bashrc","r+") as f: # Open .bashrc as read and write
                new_f = f.readlines()
                f.seek(0) # Set pointer position to 0 
                for line in new_f:
                    if "export GIT_TOKEN" not in line: # If it's not the key phrase then rewrites the same phrase 
                        f.write(line)
                f.truncate() # If it's the key phrase then truncates it
                    
            # Adds the new token as a new environmental variable 
            os.system(f"echo 'export GIT_TOKEN='{new_token}'' >> ~/.bashrc") 
            print(colored("\nRestart your terminal to commit the changes.\nOAuth token updated successfully.\n","green"))
            input("Press Enter To Exit...")
            sys.exit()

        except Exception as e: 
            # "Raises" an error if an exception is risen.
            print(colored(f"\nSomething went wrong while replacing the old token.\n Error : {e}\n","red"))
            input("Press Enter To Exit...")
            sys.exit()
       
    def __call__(self, parser, namespace, values, option_string=None):
        self.token()
        parser.exit()

parser = argparse.ArgumentParser(description = 
"""
[FAQ] : 
 (+) The name given alongside the name flag will be your repository name.
 (+) If you're using GitHub make sure you have an OAuth token and give it repos permissions.
 (+) The inical path of the program is /home/ (~), so to specify the path you can just state it's parents folders.
 (+) Your GitHub token gets stored as an environmental variable on ~/.bashrc as the last line.
 (+) Check https://docs.github.com/pt/github/creating-cloning-and-archiving-repositories/licensing-a-repository to get license keywords.
 (+) If an error occurs during the project build-up (after creating the repo) the repo won't be deleted.\n
[Editor keywords] :
  ʟ VScode : vscode
  ʟ Sublime : subl
  ʟ Atom : atom (requires 'Install Shell Commands')\n
""", formatter_class = RawTextHelpFormatter)

parser.add_argument("-n", "--name", type = str, required = True, help = "Project Name")
parser.add_argument("-l", "--license", type = str, required = False, help = "Project License")
parser.add_argument("-e", "--editor", type = str, required = False, help = "Code Editor")
parser.add_argument("-p", "--path", type = str, required = True, help = "Project Path")
parser.add_argument("-g", "--git", action = "store_true", help = "Disable Repository Creation")
parser.add_argument("-q", "--quiet", action = "store_true", help = "Run Quietly")

group = parser.add_mutually_exclusive_group()
group.add_argument("-t", "--token", action = chToken, nargs = 0, help = "Change OAuth Token")

args = parser.parse_args()

# print(args.name, args.language, args.editor, args.path)

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
            
            # Sets the api token as an env variable.
            if 'GIT_TOKEN' in os.environ:
                x = input(f"\n{bcolors.WARNING}(!){bcolors.ENDC} Environmental variable already existent please rename it.\n{bcolors.WARNING}(!){bcolors.ENDC} Do you wish to use it ? (y/n)")

                while True: 

                    x = input(f"\n{bcolors.WARNING}(!){bcolors.ENDC} Environmental variable already existent please rename it.\n{bcolors.WARNING}(!){bcolors.ENDC} Do you wish to use it ? (y/n) ")
                    
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

    if args.license != None:
        payload = '{"name": "' + args.name + '", "private": false, "license_template": "' + args.license + '"}' # Data about the new repository such as name and privacy.
    else:
        payload = '{"name": "' + args.name + '", "private": false}'

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
        print(f"  ʟ Repository created : https://github.com/{git_user}/{args.name} ")
    
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

    # Creates documentation folder and adds a README to it.
    os.mkdir(f"{args.name}/docs") # docs
    os.system(f'touch {args.name}/docs/README.md') 
    os.system(f"echo '# Documentation' >> {args.name}/docs/README.md") 

    # Creates lib folder and adds a README to it.
    os.mkdir(f"{args.name}/lib") # lib
    os.system(f'touch {args.name}/lib/README.md') 
    os.system(f"echo '# Libs' >> {args.name}/lib/README.md") 

    # Creates README to the frontpage of the repository.
    os.system(f'touch {args.name}/README.md') 
    os.system(f"echo '# {args.name}' >> {args.name}/README.md") # Writes the project name to the README.md file.
    print("    ʟ Successful\n ")

    # Pushing to the repository
    print("  ʟ Pushing to remote..")
    os.chdir(os.path.expanduser("~")) # Goes to root
    os.chdir(f"{args.path}/{args.name}") # Goes to new repo folder.
    subprocess.run(["git","add","."],stdout=subprocess.DEVNULL) # > git add .
    subprocess.run(["git","commit","-m","Init"],stdout=subprocess.DEVNULL) # > git commit -m "Init"

    try:
        subprocess.run(["git","push","-q", f"https://{GIT}@github.com/gweebg/{args.name}.git"],stdout=subprocess.DEVNULL) # > git push -q ...
        print("    ʟ Successful\n ")
        print(colored(" Project build-up finished.","green"))

    except Exception as ex: 
        print(colored(f"An exception has occured while pushing to remote :\n{ex}"))
        input("Press Enter To Exit...")
        sys.exit()

def open_repo():

    os.chdir(directory)

    if args.editor == None:
        with open("log.txt","r") as f:
            lines = f.readlines()
            editor = (lines[1].lower())
            editor = editor.strip('\n')
    else: 
        editor = (args.editor).lower()
    
    print(colored(" Opening folder...\n","cyan"))
    os.chdir(os.path.expanduser("~"))
    os.chdir(f"{args.path}/{args.name}" if not args.path == "." else f"{os.getcwd()}/{args.name}")
    
    vs = ["vscode","vs","code"]
    subl = ["sublime","subl"]
    atom = ["atom"]

    try: 
        if editor in vs:
            subprocess.run(["code", "."], stdout = subprocess.DEVNULL)
        elif editor in subl: 
            subprocess.run(["subl", "."], stdout = subprocess.DEVNULL)
        elif editor in atom:
            subprocess.run(["atom", "."], stdout = subprocess.DEVNULL)
        else: 
            print(colored(" Editor not supported.","red"))
            input(" Press Enter To Exit...")
            sys.exit()
        
    except Exception as error: 
        print(colored(f" Something went wrong while opening the project.\nError : {error}"))
        input("Press Enter To Exit...")
        sys.exit()

# Only creates the project folder without creating a new repository.
def files_only():

    os.chdir(os.path.expanduser("~")) # Changing to root directory.
    os.chdir(os.getcwd() if args.path == "." else args.path) # Changes the directory to clone the repository.    

    os.mkdir(args.name)

    # Adding folders and README.md
    print("\n Adding files...")
    os.mkdir(f"{args.name}/src") # src
    os.system(f'touch {args.name}/src/README.md') # README
    os.system(f"echo '# Source code' >> {args.name}/src/README.md") # README update

    # Creates documentation folder and adds a README to it.
    os.mkdir(f"{args.name}/docs") # docs
    os.system(f'touch {args.name}/docs/README.md') 
    os.system(f"echo '# Documentation' >> {args.name}/docs/README.md") 

    # Creates lib folder and adds a README to it.
    os.mkdir(f"{args.name}/lib") # lib
    os.system(f'touch {args.name}/lib/README.md') 
    os.system(f"echo '# Libs' >> {args.name}/lib/README.md") 

    # Creates README to the frontpage of the repository.
    os.system(f'touch {args.name}/README.md') 
    os.system(f"echo '# {args.name}' >> {args.name}/README.md") # Writes the project name to the README.md file.
    print("  ʟ Successful\n")

# Runs every function according to the arguments given.
if __name__ == "__main__":

    if os.path.isfile("log.txt"):
        if args.quiet:
            with NoStdStreams():
                if not args.git:
                    git()
                    open_repo()
                    sys.exit()
                else: 
                    files_only()
                    open_repo()
        else:
            if not args.git:
                git()
                open_repo()
                sys.exit()
            else: 
                files_only()
                open_repo()
    else: 
        setup()
      

