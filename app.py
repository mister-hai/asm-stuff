# -*- coding: utf-8 -*-
#!/usr/bin/python3.9
#ROPGadget scan tool ONLY!!!!
#stop feature creeping on init
# who the fuck am I kidding, look at all ther different titles lying around
################################################################################
##       Automated Fuzzing Harness Generator - Vintage 2021 Python 3.9        ##
################################################################################                
# Licenced under GPLv3                                                        ##
# https://www.gnu.org/licenses/gpl-3.0.en.html                                ##
#                                                                             ##
# The above copyright notice and this permission notice shall be included in  ##
# all copies or substantial portions of the Software.                         ##
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
################################################################################
TESTING = True
"""
main file
"""
################################################################################
##############                      IMPORTS                    #################
################################################################################

import sys,os
import argparse
import os,sys
import requests
import subprocess
import configparser
from src.util import errormessage,greenprint,redprint,blueprint

import ipaddress
from ipaddress import IPv4Address, IPv4Interface


PROGRAM_DESCRIPTION = """
A program to help you to hack binaries.         
"""
TESTING = True

################################################################################
##############             COMMAND LINE ARGUMENTS              #################
################################################################################

parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
parser.add_argument('--workspacepath',
                        dest = 'workspace',
                        action  = "store" ,
                        default = "workspace" ,
                        help = "path to lib",
                        required=True
                        )
#parser.add_argument('--',
#                        dest = '',
#                        action  = "store",
#                        default = "" ,
#                        help = "",
#                        required=True
#                        )
#parser.add_argument('--database',
#                        dest = 'database',
#                        action  = "store",
#                        default = "" ,
#                        help = "",
#                        required=True
#                        )
parser.add_argument('--use-config',
                        dest = 'useconfig',
                        action  = "store_true",
                        default = False ,
                        help = " use this flag for using the config file",
                        required=False
                        )
parser.add_argument('--configset',
                        dest = 'configset',
                        action  = "store",
                        default = "DEFAULT" ,
                        help = " use this flag to select which configuration to use",
                        required=False
                        )
parser.add_argument('--outputdir', 
                        dest = 'outputdir',
                        action  = "store",
                        default = False ,
                        help = "Output directory",
                        required=True
                        )
#parser.add_argument('--compilerflags',
#                        dest = 'compilerflags',
#                        action  = "store",
#                        default = False ,
#                        help = "compiler flags (include)",
#                        required=False
#                        )
#parser.add_argument('--headers',
#                        dest = 'headers',
#                        action  = "store",
#                        default = False ,
#                        help = "header files, CSV string",
#                        required=False)
#parser.add_argument('--debug',
#                        dest = 'debug',
#                        action  = "store_true",
#                        default = False ,
#                        help = "display debugging information \n DEFAULT: On"
#                        )
arguments = parser.parse_args()
 
###############################################################################
##                     CONFIGURATION FILE PARSER                             ##
###############################################################################
try:
    #parse args to get defaults
    arguments = parser.parse_args()
    # get configs from the specified/default set
    config = configparser.ConfigParser()
    configset = arguments.configset
    #start installing packages later
    listofpackages = config[configset]['packages'].split(',')
    arguments = parser.parse_args()
    if arguments.config == True:
        projectroot            = config[configset]['projectroot']
        outputdirectory        = config[configset]['outputdirectory']
    elif arguments.config == False:
        projectroot            = arguments.projectroot
        outputdirectory        = arguments.outputdirectory
except Exception:
    errormessage("[-] Configuation File could not be parsed!")
    sys.exit(1)

greenprint("[+] Loaded Commandline Arguments")

def rootinplace():
    '''establishes this scripts operating location and relative code locations'''
    env = [projectroot,
           outputdirectory,
           ]
    setenv(env)
    if 'radare2' in listofpackages:
        pulllatestrelease('radareorg','radare2')
    if 'metasploit' in listofpackages:
        metasploitinstall()
    

def setenv(installdirs:list):
    '''sets the PATH variables for operation'''
    try:
        #validation for future expansions
        if len(installdirs) > 1:
            #make the installation directories
            for projectdirectory in installdirs:
                os.makedirs(projectdirectory, exist_ok=False)
            #set path to point to those directories
            os.environ["PATH"] += os.pathsep + os.pathsep.join(installdirs)
    except Exception:
        errormessage("[-] Failure to set Environment, Check Your Permissions Schema")

def makedirs():
    '''
    makes directories for project
    '''
    pass

def setnewnamespace():
    '''
    using internals to set a namespaec, this is sandboxing in action
    '''
    pass
def setusers():
    '''
    :param: groups
    '''
    #sudo usermod kvm libvirt docker ubridge wireshark
    pass

def vboxrun():
    pass

def qemurun():
    pass

def setifaceaddr(ipaddr:IPv4Address,netmask:int, device = 'eno1'):
    '''
    Sets interface address
    '''
    return '''ip link set dev {device} down
    ip addr add {ipaddr}/{netmask} dev {device}
    ip link set dev {device} up'''.format().splitlines()

#strippedlist = list(filter("",array))
stripempties = lambda array: [i for i in array if i]

def subprocArray(list_of_shell_commands):
    '''
    works with triple quoted bash scripts, no shell expansion
    example:

>>> def setifaceaddr(ipaddr:IPv4Address,netmask:int, device = 'eno1'):
>>>     return \'''ip link set dev {device} down
>>>     ip addr add {ipaddr}/{netmask} dev {device}
>>>     ip link set dev {device} up\'''.format().splitlines()

>>> cmd_list = setifaceaddr("192.168.1.1", 24, "eno1")
>>> returncode = subprocArray(cmd_list)
    '''
    #remove empty strings
    list_of_shell_commands = stripempties(list_of_shell_commands)
    for each in list_of_shell_commands:
        subprocess.call()
        pass            

def mdns():
    '''
    Resolves mdns for the Pi.
    sudo apt-get install libnss-mdns avahi-utils avahi-daemon
    avahi-resolve --verbose
    '''
def installradare2():
    '''
    #https://github.com/radareorg/radare2/releases
    Wrapper just in case
    '''
    releaseurl = pulllatestrelease(profile = 'radare2org', repo = 'radare2')
    returncode = runshellcommand(releaseurl)

def installpwndbg():
    '''
    Release:
        https://github.com/pwndbg/pwndbg/archive/refs/tags/2021.06.22.tar.gz
    Dev:
        https://github.com/sashs/Ropper/archive/refs/heads/master.zip
    '''
    url = "https://github.com/pwndbg/pwndbg/archive/refs/heads/dev.zip"
    requests.get(url=url,)


def pulllatestrelease(profile:str,repo:str=""):
    '''
>>> releaseurl = pulllatestrelease(profile = 'radare2org', repo = 'radare2')
>>> returncode = runshellcommand(releaseurl)
    '''
    stepsdict =  {
        #START basic shell command
        # NAME
        'meth1':{
            # LINE OF CODE
            "loc": """curl --silent "https://api.github.com/{profile}/{repo}/releases/latest" \
| jq -r .tag_name""".format(profile = profile,
                            repo = repo),
            #PASS MESSAGE
            "pass":"",
            #FAIL MESSAGE
            "fail":"",
            #INFO MESSAGE
            "info":""        
        },
        #END: Basic shell command
        #if they dont support releases
        "meth2":{
            "loc": """curl --silent "https://api.github.com/repos/{profile}/{repo}/tags" | jq -r '.[0].name'""".format(profile = profile,repo = repo),
            "pass":"success message",
            "fail":"",
            "info":""        
        }
    }
    for each in stepsdict:
        ## TODO check the operations of eval vs exec 
        # splitting by lines versus block o text?
        download = subprocess.call(each.get['loc'])
        if download:
            print(each['pass'])
            break
        else:
            print(each['fail'])
            continue
    os.chmod(download,mode = "+x")

def metasploitinstall():
    '''
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && \
chmod 755 msfinstall && \
./msfinstall
    '''

def msfdb():
    '''
    only run when setting up
    '''
    return {   
        "msfdb_init": {
            "command"         : "example_command {}".format(""),
            "info_message"    : "[+] INFORMATION",
            "success_message" : "[+] Command Sucessful", 
            "failure_message" : "[-] Command Failed! Check the logfile!"           
        }
    }

def msfrpcd(operation:str, ipaddr:IPv4Address = "127.0.0.1",password:str = "root"):
    return {
        "msf_rpcd": {
            "command"         : "sudo msfrpcd -P {} -a {} -S".format(password,ipaddr),
            "info_message"    : "[+] INFORMATION",
            "success_message" : "[+] Command Sucessful", 
            "failure_message" : "[-] Command Failed! Check the logfile!"           
        }
    }

def armitage():
    locs = '''
    export MSF_DATABASE_CONFIG=~/.msf4/database.yml
    java -jar armitage.jar
    '''
        
    return {
        "examplename": {
            "command"         : "example_command {}".format(""),
            "info_message"    : "[+] INFORMATION",
            "success_message" : "[+] Command Sucessful", 
            "failure_message" : "[-] Command Failed! Check the logfile!"           
        },
        "examplename": {
            "command"         : "example_command {}".format(""),
            "info_message"    : "[+] INFORMATION",
            "success_message" : "[+] Command Sucessful", 
            "failure_message" : "[-] Command Failed! Check the logfile!"           
        }
    
    
    
    }

def msfrpc(action:str,ip:IPv4Address,port:int):
    '''OPTIONS:
    -P <opt>  Specify the password to access msfrpcd
    -S        Disable SSL on the RPC socket
    -U <opt>  Specify the username to access msfrpcd
    -a <opt>  Connect to this IP address
    -p <opt>  Connect to the specified port instead of 55553
    '''
    pass

if __name__ == '__main__':
    rootinplace()
#    scanmodule = Scanner()
    #root the scanner in place
#    scanmodule.scancode()
    #scanmodule.genharness()
