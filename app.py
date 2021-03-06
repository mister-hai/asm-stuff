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
from  src.core import CommandDict,PybashyRunSingleJSON
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
    # and make global, 
    global config
    # this is an acceptable use of globals
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


def runshellsingleton(functionproto):
    '''
    Runs a function as shell command if it fits the spec
        Please dont feed me bad data
        I am not user friendly
     do NOT forget the () !!!
    >>> runshellsingleton(functionproto())
    '''
    #testing comand dict operations
    cmd = CommandDict(functionproto)
    cmd.__repr__()
    #testing the run function
    PybashyRunSingleJSON(functionproto)

def metasploitinstall():
    '''
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && \
chmod 755 msfinstall && \
./msfinstall
    '''

def msfdb(operation = "init"):
    '''
    only run when certain you need it
    '''
    return {   
        "msfdb_init": {
            "loc"         : "msfdb {}".format(operation),
            "info"    : "[+] INFORMATION",
            "succ" : "[+] Command Sucessful", 
            "fail" : "[-] Command Failed! Check the logfile!"           
        }
    }

def msfrpcd(operation:str, ipaddr:IPv4Address = "127.0.0.1",password:str = "root"):
    return {
        "msf_rpcd": {
            "loc"  : "sudo msfrpcd -P {} -a {} -S".format(password,ipaddr),
            "info" : "[+] INFORMATION",
            "succ" : "[+] Command Sucessful", 
            "fail" : "[-] Command Failed! Check the logfile!"           
        }
    }

def armitage():
    '''
    Performed on program start:
        export MSF_DATABASE_CONFIG=~/.msf4/database.yml

    Current Command:
        java -jar armitage.jar
    '''
        
    return {
        "examplename": {
            "loc"         : "example_command {}".format(""),
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
