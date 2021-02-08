import os
import sys
import argparse
import keyboard

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

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", type = str, required = True, help = "Project Name")
parser.add_argument("-l", "--language", type = str, required = True, help = "Coding Language" )
parser.add_argument("-e", "--editor", type = str, required = True, help = "Text Editor")
parser.add_argument("-p", "--path", type = str, required = False, help = "Project Path")

group = parser.add_mutually_exclusive_group()
group.add_argument("-g", "--git", action = "store_true", help = "Create Repository")

args = parser.parse_args()

print(args.name, args.language, args.editor, args.path)

def check_lan(lan):
    if lan == 'python3':
        if os.system("python --version") != 0:
            print("Language/Compiler not installed.")
            return False
        else: 
            return True
                
    elif lan == 'haskell':
        if os.system("ghci --version") != 0: 
            print("Language/Compiler not installed.")
            return False
        else: 
            return True
            
    elif lan == 'c':
        if os.system("gcc --version") != 0:
            print("Language/Compiler not installed.")
            return False
        else: 
            return True
        
    elif lan == 'java':
        if os.system("java -version") != 0:
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
        os.mkdir(name)
    except FileExistsError:
        raise Exception("Duplicate name, choose another name.")
    
    os.chdir(os.getcwd()) # Change to the new folder
    os.mkdir("src") # Create 'src' folder 
    os.mkdir("docs") # Create 'docs' folder
    os.mkdir("lib") # Create 'lib' folder

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
    if check_lan(args.language):
        # Creates the project folder.
        new_folder(args.path,args.name)
        print("Project folder created.")
    

