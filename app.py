#ROPGadget scan tool ONLY!!!!
#stop feature creeping on init


PROGRAM_DESCRIPTION = ""
TESTING = True

import re
import pkg.r2pipe as r2pipe
import sys,os
import inspect
import traceback
import subprocess
import argparse
try:
    import colorama
    from colorama import init
    init()
    from colorama import Fore, Back, Style
# Not from the documentation on colorama
    if TESTING == True:
        COLORMEQUALIFIED = True
except ImportError as derp:
    herp_a = derp
    print("[-] NO COLOR PRINTING FUNCTIONS AVAILABLE, Install the Colorama Package from pip")
    COLORMEQUALIFIED = False

redprint          = lambda text: print(Fore.RED + ' ' +  text + ' ' + Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
blueprint         = lambda text: print(Fore.BLUE + ' ' +  text + ' ' + Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
greenprint        = lambda text: print(Fore.GREEN + ' ' +  text + ' ' + Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
yellow_bold_print = lambda text: print(Fore.YELLOW + Style.BRIGHT + ' {} '.format(text) + Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)

def error_printer(message):
    exc_type, exc_value, exc_tb = sys.exc_info()
    trace = traceback.TracebackException(exc_type, exc_value, exc_tb) 
    blueprint('LINE NUMBER >>>' + str(exc_tb.tb_lineno))
    greenprint('[+]The Error That Occured Was :')
    redprint( message + ''.join(trace.format_exception_only()))
    yellow_bold_print("Some info:")
    exc_info = sys.exc_info()
    traceback.print_exception(*exc_info)

def setenv(installdirs:list):
    '''sets the environment for operating as a self contained package
    provide paths to submodules necessary for import as a list
    '''
    if len(installdirs) = 1:
        os.environ["PATH"] += os.pathsep + path
    elif len(installdirs) > 1:
        os.environ["PATH"] += os.pathsep + os.pathsep.join(pathlist)
    #powershell
    #$env:Path = "SomeRandomPath";  (replaces existing path) 
    #$env:Path += ";SomeRandomPath" (appends to existing path)

class LoadEnv(object):
    def __init__(self):
        snoodles
        {
            {"installpwntool" :'pip install --upgrade --editable ./pwntools',
                "info":"",
                "success":"",
                "fail":""
                },
            {"cmd" :'',
                "info":"",
                "success":"",
                "fail":""
                }
        
        }
        pass

    def exec_command(self, command, shell_env=True):
        '''Runs a python script with subprocess.Popen'''
    try:
        subprocess.Popen(command,shell=shell_env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output, error = step.communicate()
            for output_line in output.decode().split('\n'):
                print(output_line)
            for error_lines in error.decode().split('\n'):
                print(error_lines + " ERROR LINE")
        return True
    except Exception:
        error_printer("[-] Interpreter Message: exec_command() failed!")
        return False
