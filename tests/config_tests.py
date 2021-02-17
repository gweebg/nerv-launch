import json
import os
import subprocess
import sys
import inspect

import pytest
from colorama import init
from termcolor import colored

current_dir = os.getcwd()

def checkConfig(path,file):
    
    os.chdir(path)

    os.chdir(current_dir)
    with open(file,"r") as f:
        config = json.load(f)

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
            print("passed")
            pass

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

    file_name = file_name.split(",")
    for name in file_name:
        if len(file_name) != len(set(file_name)):
            print(colored("Error while parsing config.json\nDuplicate file name on the same subfolder.","red"))
            sys.exit()
        else:
            pass

    for elem in f_name:
        if elem in sub_rep:
            return False
        else:
            pass

    return True

def test_normal():
    assert checkConfig(current_dir,"config_1.json") == True

def test_false():
    assert checkConfig(current_dir,"config_1.json") == True



