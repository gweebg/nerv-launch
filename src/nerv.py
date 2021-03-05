import argparse
import os
import string
import subprocess
import sys
import json
from argparse import RawTextHelpFormatter

import requests
from colorama import init
from termcolor import colored

import git
import setup

"""
Project launcher for unix systems written in Python3 and some shell script.
Easy to use and costumizable.
To use it, call the script and add the arguments down bellow.

Arguments : 
    -n * --name (Project name) 
    -l --license (Project license)
    -e * --editor (Code editor) [optional]
    -p * --path (Project path)
    -g --git (Disable repository creation) [optional]
    -h --help  (Help)
    -q --quiet (Runs the code quietly) [optional]
    
Example : 
    python3 nerv.py -n project_name -l mit -p project_path
    nerv -n project_name -p . -g
"""    

# Inits colorama colors.
init()
directory = os.getcwd() # Initial directory, where the script is

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

# Terminal colors for better application of them.
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

# Class containing an argparse action. The function token replaces the new OAuth token by the old one.
class chToken(argparse.Action):

    def token(self):
        print(colored("\nChanging Github OAuth token : ","green"))

        # Asking for the new token, gets stored on new_token variable.
        new_token = input(f"{colors.OKGREEN}(+){colors.ENDC} Please submit your new Github OAuth token : ")

        # Changing into the home directory.
        os.chdir(os.path.expanduser("~")) # dir = ~ 
        
        # Deletes the old token from .bashrc .
        try:
            with open(".bashrc","r+") as f: # Open .bashrc as read and write.
                new_f = f.readlines()
                f.seek(0) # Set pointer position to 0.
                for line in new_f:
                    if "export GIT_TOKEN" not in line: # If it's not the key phrase then rewrites the same phrase on itself.
                        f.write(line)
                f.truncate() # If it's the key phrase then truncates it.
                    
            # Adds the new token as a new environmental variable (on .bashrc).
            os.system(f"echo 'export GIT_TOKEN='{new_token}'' >> ~/.bashrc") 
            print(colored("\nRestart your terminal to commit the changes.\nOAuth token updated successfully.\n","green"))
            input("Press Enter To Exit...")
            sys.exit()

        except Exception as e: 
            # "Raises" an error if an exception is risen (just in case).
            print(colored(f"\nSomething went wrong while replacing the old token.\n Error : {e}\n","red"))
            input("Press Enter To Exit...")
            sys.exit()
    
    # This function is called by the parser.
    def __call__(self, parser, namespace, values, option_string=None):
        self.token()
        parser.exit()

# Our argument parser with some script information.
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
""", formatter_class = RawTextHelpFormatter) # Needs the formatter_class in order to create new lines and format text.

# Project name set as -n 
parser.add_argument("-n", "--name", type = str, required = True, help = "Project Name")
# Project license set as -l
parser.add_argument("-l", "--license", type = str, required = False, help = "Project License")
# Project code editor set as -e
parser.add_argument("-e", "--editor", type = str, required = False, help = "Code Editor")
# Project path set as -p
parser.add_argument("-p", "--path", type = str, required = True, help = "Project Path")
# Git disable option set as -g
parser.add_argument("-g", "--git", action = "store_true", help = "Disable Repository Creation")
# Run quiet option set as -q
parser.add_argument("-q", "--quiet", action = "store_true", help = "Run Quietly")

# This group parser only allows its arguments to be ran alone.
group = parser.add_mutually_exclusive_group()
# Change OAuth token option set as -t
group.add_argument("-t", "--token", action = chToken, nargs = 0, help = "Change OAuth Token")
# group.add_argument("-o", "--options", nargs = 0, help = "Customize the folders.")
# Generates a list with all the arguments parsed out. These arguments can be called by using args.name_of_argument .
args = parser.parse_args()

# Function that opens the new project with the correct code editor.
def open_repo():
    """
    We need to change the current directory
    to the initial one, since it's where 'config.json' is
    located. open_repo() is always executed after
    git() and so the directory wouldn't be the inital.
    """
    os.chdir(directory)

    """
    Since the editor argument is optional, we check it has
    been called. If it didn't we use the default one that 
    has been set during setup. If it did we just take it from args.
    """
    if args.editor == None:
        with open("config.json","r") as f: # Open "config.json"
            config = json.load(f)
            editor = config["default_editor"]
    else: 
        editor = (args.editor).lower() # Set editor as the argument.
    
    """
    After having the editor we need to open the project
    by calling it on the project directory.
    """
    print(colored(" Opening folder...\n","cyan"))
    os.chdir(os.path.expanduser("~")) # cd ~
    # cd project_path
    os.chdir(f"{args.path}/{args.name}" if not args.path == "." else f"{directory}/{args.name}") # Checks if path = '.', if so, uses the inital directory.
    
    # Editors keywords
    vs = ["vscode","vs","code"] 
    subl = ["sublime","subl"]
    atom = ["atom"]

    # Opening the project over terminal.
    try: 
        if editor in vs:                  # We don't want any kind of output so we set stdou to /dev/null.
            subprocess.run(["code", "."], stdout = subprocess.DEVNULL) # code .
        elif editor in subl: 
            subprocess.run(["subl", "."], stdout = subprocess.DEVNULL) # subl .
        elif editor in atom:
            subprocess.run(["atom", "."], stdout = subprocess.DEVNULL) # atom .
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

    """
    This function in only responsible for creating the folders
    and essential files to the project generation, such as 
    README.md and /src/, /docs/, /lib/ folders.
    """
    os.chdir(os.path.expanduser("~")) # Changing to root directory.
    # Changes the directory to the project's. 
    os.chdir(os.getcwd() if args.path == "." else args.path)   
    os.mkdir(args.name) 

    # Adding folders and README.md
    print("\n Adding files...")
    os.mkdir(f"{args.name}/src") # Creates the folder src into the project folder.
    os.system(f'touch {args.name}/src/README.md') # Adds the README file to it.
    os.system(f"echo '# Source code' >> {args.name}/src/README.md") # Writes the folder name to the README file.

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
    os.system(f"echo '# {args.name}' >> {args.name}/README.md") 
    print("  ʟ Successful\n")

# Runs every function according to the arguments given.
if __name__ == "__main__":

    """
    In this part we manage what functions are executed and when they are.
    Things like not creating a repository or running the code on quiet mode
    are handled here. 
    """
    
    os.chdir(directory) # Added for the same reason as the open_repo()
    
    with open("config.json","r") as f:
        config = json.load(f)
        key = config["setup"]

     # Checking if the setup() has already been made by looking for the "setup" value on config.json .
    if key == "True": 
        if args.quiet: # Checks if it needs to be ran in quiet mode.
            with NoStdStreams():
                if not args.git: # Checks if it needs to create a new repository.
                    git.git(args.name,args.license,args.path) # Creating repository
                    open_repo() # Opening the repository
                    sys.exit()
                else: 
                    files_only() # No repository, just folders.
                    open_repo() # Opening the folder, once again.
        else:
            if not args.git:
                git.git(args.name,args.license,args.path)
                open_repo()
                sys.exit()
            else: 
                files_only()
                open_repo()
    else: 
        # If it's false we need to create one by doing the setup. 
        setup.setup()
      