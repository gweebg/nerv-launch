import sys
import os 
import subprocess
import json

import requests
from colorama import init
from termcolor import colored

import folder

"""
This module is responsible for the
creation of the repository, cloning, 
creation of all the folders, subfolders and README/License,
adding, commiting and pushing.
"""

def get_token():
    
    init()
    os.chdir(os.path.expanduser("~"))

    try:
        
        # Getting the variable out of the system
        with open(".bashrc","r+") as f: # Open .bashrc as read and write.
            new_f = f.readlines()
            f.seek(0) # Set pointer position to 0.
            for line in new_f:
                if "export GIT_TOKEN" not in line: # If it's not the key phrase then rewrites the same phrase on itself.
                    f.write(line)
                else:
                    token_line = line  
                    
        # Formatting the line 
        token_line = token_line.split("=")
        x = []
        for part in token_line: 
            x.append(part.strip())
        
        token = x[1]
        
    except Exception as error:
        print(colored(f"Something went wrong.\n{error}","red"))
    
    return token

def git(name,lic,path):
    
    # Startup of the coloroma package.
    init()

    # Opens the config.json file to read the github username.
    with open("config.json","r") as file:
        config = json.load(file)
        git_user = config["github_name"]
    
    print(colored("\n [ Project {name} ]","cyan"))
    
    print("\n Creating new repository...")
    
    # Gets the token from .bashrc using the get_token() function above.
    GIT = get_token() 
    API_URL = "https://api.github.com" # API base url, useless when in this format.

    """
    Checks if the license flag was used,
    if so, adds the license when creating the repository
    else only creates the repo. 
    """
    
    if lic != None:
        payload = '{"name": "' + name + '", "private": false, "license_template": "' + lic + '"}' # Data about the new repository such as name and privacy.
    else:
        payload = '{"name": "' + name + '", "private": false}'

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
        print(f"  ʟ Repository created : https://github.com/{git_user}/{name} ")
    
    print("\n Starting up your project :\n")

    """
    Cloning the repository created above,
    creating its folders and subfolders,
    commiting the changes and pushing to remote. 
    """
    os.chdir(os.path.expanduser("~")) # Changing to root directory.
    os.chdir(os.getcwd() if path == "." else path) # Changes the directory to clone the repository.
    
    try: 
        # Cloning the repository
        print("  ʟ Cloning the repository..")
        os.system(f"git clone -q https://{GIT}@github.com/gweebg/{name}.git 2>&1 | grep -v 'warning: You appear to have cloned an empty repository.'")
        print("    ʟ Successful\n")

    except Exception as e:
        # Catching exceptions.
        print(colored(f"An exception has occured :\n{e}"))
        input("Press Enter To Exit...")
        sys.exit()

    # Using folder.py to create folders from config.json 
    folder.config(f"{path}/{name}")

    # Pushing to the repository
    print("  ʟ Pushing to remote..")
    os.chdir(os.path.expanduser("~")) # Goes to root
    os.chdir(f"{path}/{name}") # Goes to new repo folder.
    subprocess.run(["git","add","."],stdout=subprocess.DEVNULL) # > git add .
    subprocess.run(["git","commit","-m","Init"],stdout=subprocess.DEVNULL) # > git commit -m "Init"

    # Pushing the updated repository to Github.
    try:
        subprocess.run(["git","push","-q", f"https://{GIT}@github.com/gweebg/{name}.git"],stdout=subprocess.DEVNULL) # > git push -q ...
        print("    ʟ Successful\n ")
        print(colored(" Project build-up finished.","green"))

    except Exception as ex: 
        print(colored(f"An exception has occured while pushing to remote :\n{ex}"))
        input("Press Enter To Exit...")
        sys.exit()
        
# Falta adicionar config.py para a criação dos folders: 
# Primeiro criar, depois adicionar, e dar push 