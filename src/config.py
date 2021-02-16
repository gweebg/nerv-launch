import json
import sys 
import subprocess
import os 

from colorama import init
from termcolor import colored

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

def readConfig(path): 
    # Path where to work
    config_path = path
    os.chdir(config_path)
    
    with open("config.json","r") as file:
        config = json.load(file)
    
    if config["add_readme"] : 
        
        if config["default_folders"] : 
            return True
        else : 
            getValues("config.json","/home/gwee/proj/testes")
            
     
    
def getValues(file,path): # path where the project is 
    # Open config to read
    with open(file,"r") as f:
        config = json.load(f)
        
    data = config["folders"] # List
    print(type(data))
    # print(data)
    print("="*50)
    
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
                print(f"{file} created in {path}")
        else: 
            os.chdir(path)
            os.mkdir(name)
            
    # Subfolder creation 
    sub_data = config["subfolders"]
    for sub in sub_data: 
        
        sub_name = sub["sub_name"]
        inside = sub["inside"]
        files = sub["content"]
        
        if os.path.exists(f"{path}/{inside}"):
            
            if len(files.strip()) != 0: 
                
                files = files.split(",")
                print(files)
                
                os.chdir(f"{path}/{inside}")
                os.mkdir(sub_name)
                os.chdir(f"{path}/{inside}/{sub_name}")
                
                for file in files: 
                    os.system(f"touch {file}")
        else: 
            print(colored("Error on config.json\nThe folder {inside} does not exist within {path}.","red"))

# Ver casos onde o folder já existe ou files com nomes iguais, dois folder com o mesmo nome nas configs (fazer função para isso)
# Ver se é criado subfolder dentro de um subfolder e testar (dar fix)
# Tutorial de como editar as configs 
    
readConfig(os.getcwd())
        
    