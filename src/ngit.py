import sys
import os 
import subprocess

import requests
from colorama import init
from termcolor import colored

def git(name,lic,path):
    
    init()

    # Opens the log.txt file to read the github username.
    with open("log.txt","r") as file:
        info = file.read().split('\n')
        file.close()
    
    git_user = info[-1] # Github username.
    
    print("\n Creating new repository...")
    
    # Gets the token saved as env variable.
    GIT = os.environ.get("GIT_TOKEN")
    API_URL = "https://api.github.com" # API base url, useless when in this format.

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
    
    print(colored("\n Starting up your project :\n"))

    # Project build up
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

    # Adding folders and README.md
    print("  ʟ Adding files..")
    os.mkdir(f"{name}/src") # src
    os.system(f'touch {name}/src/README.md') # README
    os.system(f"echo '# Source code' >> {name}/src/README.md") # README update

    # Creates documentation folder and adds a README to it.
    os.mkdir(f"{name}/docs") # docs
    os.system(f'touch {name}/docs/README.md') 
    os.system(f"echo '# Documentation' >> {name}/docs/README.md") 

    # Creates lib folder and adds a README to it.
    os.mkdir(f"{name}/lib") # lib
    os.system(f'touch {name}/lib/README.md') 
    os.system(f"echo '# Libs' >> {name}/lib/README.md") 

    # Creates README to the frontpage of the repository.
    os.system(f'touch {name}/README.md') 
    os.system(f"echo '# {name}' >> {name}/README.md") # Writes the project name to the README.md file.
    print("    ʟ Successful\n ")

    # Pushing to the repository
    print("  ʟ Pushing to remote..")
    os.chdir(os.path.expanduser("~")) # Goes to root
    os.chdir(f"{path}/{name}") # Goes to new repo folder.
    subprocess.run(["git","add","."],stdout=subprocess.DEVNULL) # > git add .
    subprocess.run(["git","commit","-m","Init"],stdout=subprocess.DEVNULL) # > git commit -m "Init"

    try:
        subprocess.run(["git","push","-q", f"https://{GIT}@github.com/gweebg/{name}.git"],stdout=subprocess.DEVNULL) # > git push -q ...
        print("    ʟ Successful\n ")
        print(colored(" Project build-up finished.","green"))

    except Exception as ex: 
        print(colored(f"An exception has occured while pushing to remote :\n{ex}"))
        input("Press Enter To Exit...")
        sys.exit()