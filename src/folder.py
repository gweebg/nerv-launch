import json
import sys
import subprocess
import os

from colorama import init
from termcolor import colored
import getpass

"""
Config file example:
{
    "profile_name": "Guilherme",
    "default_editor": "vscode",
    "github_name": "gweebg",
    "setup": "False",
    "default_folders": false,
    "add_readme": true,
    "folders" :
    [
        {
            "folder_name": "docs",
            "files": "README.md"
        },
        {
            "folder_name": "src",
            "files": "script.py"
        }
    ],
    "subfolders":
    [
        {
            "sub_name": "html",
            "inside": "docs",
            "content": "index.html"
        }
    ]
}
project
    | docs
        | html
            | index.html
    | src
        | script.py
        
First parse the "folder" key and create the folders,
then add its content and finally parse the "subfolder" key
and add the folders and files.
"""

current_dir = os.getcwd()

def checkConfig(path):

    """
    Checking if the config file is setup right.
    Check for replicated files on the same folder.
    Check subfolders inside of subfolders, try to correct it.
    """

    # Correct path
    os.chdir(path)

    # Opening the config.json file
    os.chdir(current_dir)
    with open("config.json","r") as f:
        config = json.load(f)

    # Checking for equal file names on the same folder.
    data = config["folders"]

    rep = []
    folders = []
    for folder in data:
        file_name = folder["files"]
        folder_names = folder["folder_name"]

        rep.append(file_name)
        folders.append(folder_names)

    for file_set in rep:
        names = file_set.split(",")

        if len(names) != len(set(names)):
            print(colored("Error while parsing config.json\nDuplicate file name on the same folder.","red"))
            sys.exit()
        else:
            # print("passed")
            pass

    # Checking if the folder where the subfolder is exists.
    sub_data = config["subfolders"]
    sub_rep = []
    sub_name = []
    f_name = []

    for sub_folder in sub_data:
        inside = sub_folder["inside"]
        file_name = sub_folder["content"]
        name = sub_folder["sub_name"]

        f_name.append(name)
        sub_rep.append(inside)
        sub_name.append(file_name)

    for name in sub_rep:
        if name in folders:
            pass
        elif name in f_name:
            pass
        else:
            print(colored("Error while parsing config.json\nFolder non existent.","red"))
            sys.exit()

    # Checking for duplicate file names in subfolders.
    file_name = file_name.split(",")
    for name in file_name:
        if len(file_name) != len(set(file_name)):
            print(colored("Error while parsing config.json\nDuplicate file name on the same subfolder.","red"))
            sys.exit()
        else:
            pass

    # Checking for subfolders inside of subfolders
    for elem in f_name:
        if elem in sub_rep:
            return False
        else:
            pass

    return True

def readConfig(path,proj):
    # Path where to work
    config_path = path
    os.chdir(config_path)
    
    global current_dir
    user = getpass.getuser() 
    
    with open("config.json","r") as file:
        config = json.load(file)

    if config["add_readme"] :

        if config["default_folders"] :
            defaultFolder(proj, f"/home/{user}/{proj}")
        else :
            createFolder("config.json",f"/home/{user}/{proj}")
            os.chdir(current_dir)
            createSub("config.json",f"/home/{user}/{proj}")


def defaultFolder(name,path):
    
    # Adding folders and README.md
    print(" Adding files...")
    os.mkdir(f"{path}/src") # Creates the folder src into the project folder.
    os.system(f'touch {path}/src/README.md') # Adds the README file to it.
    os.system(f"echo '# Source code' >> {path}/src/README.md") # Writes the folder name to the README file.

    # Creates documentation folder and adds a README to it.
    os.mkdir(f"{path}/docs") # docs
    os.system(f'touch {path}/docs/README.md') 
    os.system(f"echo '# Documentation' >> {path}/docs/README.md") 

    # Creates lib folder and adds a README to it.
    os.mkdir(f"{path}/lib") # lib
    os.system(f'touch {path}/lib/README.md') 
    os.system(f"echo '# Libs' >> {path}/lib/README.md") 

    # Creates README to the frontpage of the repository.
    os.system(f'touch {path}/README.md') 
    os.system(f"echo '# {name}' >> {path}/README.md") 
    print("  ʟ Successful\n")

                 # Acabar, dar parse para adiciconar folder dentro de folder.
def createFolder(file,path): # path where the project is
    # Open config to read
    with open(file,"r") as f:
        config = json.load(f)

    data = config["folders"] # List
    # print(type(data))
    # print(data)
    # print("="*50)

    print("  ʟ Adding primary folders..")
    
    # Folder creation
    for folder in data:
        name = folder["folder_name"]
        files = folder["files"] # str needs to be parsed first

        if len(files.strip()) != 0:
            files = files.split(",") # list with files

            os.chdir(path)
            os.mkdir(name)
            os.chdir(f"{path}/{name}")

            for file in files:
                os.system(f"touch {file}")
                # print(f"{file} created in {path}")
        else:
            os.chdir(path)
            os.mkdir(name)
    
    print("    ʟ Successful\n ")

def createSub(file,path):

    global current_dir
    with open(file,"r") as file:
        config = json.load(file)

    print("  ʟ Adding secondary folders..")

    # Subfolder creation
    sub_data = config["subfolders"]
    if checkConfig(current_dir) == True:
        for sub in sub_data:

            sub_name = sub["sub_name"]
            inside = sub["inside"]
            files = sub["content"]

            if os.path.exists(f"{path}/{inside}"):

                if len(files.strip()) != 0:

                    files = files.split(",")
                    # print(files)

                    os.chdir(f"{path}/{inside}")
                    os.mkdir(sub_name)
                    os.chdir(f"{path}/{inside}/{sub_name}")
                    
                    for file in files:
                        os.system(f"touch {file}")

                else:
                    print(colored("Error on config.json\nEmpty name.","red"))
                    sys.exit()
            else:
                print(colored(f"Error on config.json\nThe folder {inside} does not exist within {path}.","red"))
                sys.exit()
    
    print("    ʟ Successful\n ")
    
    print("  ʟ Adding files..")
    print("    ʟ Successful\n ")
    
def config(path):
    
    if checkConfig(current_dir): 
        readConfig(os.getcwd(),path)
    else: 
        print(colored("Error while parsing the configuration file.\nThe maximum depth level is one, thus you can't create a subfolder inside of a subfolder.","red"))


# FIX aos . em vez de path