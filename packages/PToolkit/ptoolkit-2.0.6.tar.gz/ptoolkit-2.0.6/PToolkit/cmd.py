import sys, os
import shutil
from PToolkit import __file__ as PTOOLKIT_path
from PToolkit import __version__ as PTOOLKIT_VERSION
PTOOLKIT_PATH = PTOOLKIT_path.replace("\\__init__.py", "")

class CMD():
    def __init__(self, terminalpath, args):
        self.terminalcommands = {}
        self.terminalpath = terminalpath
        self.arguments = args[1:]

    def Add_command(self, command, **options):
            def wrapper(func):
                
                self.terminalcommands[command] = func
                
                return func
            
            return wrapper
    
    def Excute_command(self):

        if len(self.arguments) == 0:
            print(f"PToolkit version {PTOOLKIT_VERSION} installed at {PTOOLKIT_PATH}")
            print(f'Run "PToolkit help" for more info')

        else:
            command = self.arguments[0]
            
            try:
                self.terminalcommands[command](self.terminalpath, self.arguments[1:])
            
            except KeyError as e:
                print("ERROR: Unkown command")

console_path = os.getcwd()
arguments = sys.argv
P = CMD(console_path, arguments)

@P.Add_command("help")
def Help_PToolkit(terminalpath, arguments):
    """Help command lists all commands available"""
    print("Commands: ")
    for name, func in P.terminalcommands.items(): 
        print(f"\t{name}: {func.__doc__}")

@P.Add_command("newproject")
def Create_new_project(terminalpath, arguments):
    """Create a new project. Arguments: <projectname>"""
    try:
        project_path = terminalpath+f"\\{arguments[0]}"
        shutil.copytree(PTOOLKIT_PATH+"\\Labcontrol\\newproject", project_path)

        if not os.path.isfile(project_path+"\\.state"):
            f = open(project_path+"\\.state", "w")
            f.close()

        if not os.path.isdir(project_path+"\\scripts"):
            os.mkdir(project_path+"\\scripts")

        if not os.path.isdir(project_path+"\\profiles"):
            os.mkdir(project_path+"\\profiles")
        
        if not os.path.isdir(project_path+"\\log"):
            os.mkdir(project_path+"\\log")

        print(f"SUCCES: Created project {arguments[0]}")

    except IndexError as e:
        print("ERROR: No project name was given")

    except Exception as e:
        print("ERROR: Folder already exists")

@P.Add_command("newinterface")
def Create_new_interface(terminalpath, arguments):
    """Create a new interface. Arguments: <interfacename>"""
    name = arguments[0]
    try:
        shutil.copyfile(PTOOLKIT_PATH+"\\Labcontrol\\newproject\\interfaces\\blankinterface.py", terminalpath+f"\\{name}.py")
        print(f"SUCCES: Created interface {arguments[0]}")

    except IndexError as e:
        print("ERROR: No interrface name was given")

    except Exception as e:
        print("ERROR: Interface already exists")

@P.Add_command("get_uCOM_p")
def Create_new_interface(terminalpath, arguments):
    """Add uCOM micro python version to folder"""
    try:
        shutil.copyfile(PTOOLKIT_PATH+"\\uCOM\\uCOM_python.py", terminalpath+f"\\uCOM_python.py")
        print(f"SUCCES: Added uCOM to folder")
    except Exception as e:
        print(f"ERROR: {e}")

@P.Add_command("get_uCOM_cpp")
def Create_new_project(terminalpath, arguments):
    """Add uCOM c++ version to folder"""
    try:
        shutil.copytree(PTOOLKIT_PATH+"\\uCOM\\uCOM_cpp", terminalpath+f"\\uCOM")
        print(f"SUCCES: Added uCOM to folder")

    except Exception as e:
        print(f"ERROR: {e}")


def main():
    P.Excute_command()


"""
command list:

newproject <project name>
newinterface <interface name>
help

"""