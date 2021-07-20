# -*- coding: utf-8 -*-
#!/usr/bin/python3.9
################################################################################
##  Pybash-sh; fuzzing harness generator - Vintage 2021 Python 3.9            ##
################################################################################                
#  YOU HAVE TO PROVIDE THE MODULES YOU CREATE AND THEY MUST FIT THE SPEC      ##
#                                                                             ##
#     You can fuck up the backend all you want but if I can't run the module  ##
#     you provide, nor understand it, you have to then follow the original    ##
#     terms of the GPLv3 and open source all modified code so I can see       ##
#     what's going on.                                                        ##
#                                                                             ##
# Licenced under GPLv3-modified                                               ##
# https://www.gnu.org/licenses/gpl-3.0.en.html                                ##
#                                                                             ##
# The above copyright notice and this permission notice shall be included in  ##
# all copies or substantial portions of the Software.                         ##
#                                                                             ##
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  ##
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    ##
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE ##
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER      ##
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,#
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN   ##
# THE SOFTWARE.                                                               ##
################################################################################
"""
core.py
"""

TESTING = True
import sys,os
import logging
import pkgutil
import inspect
import traceback
import threading
import subprocess
from pathlib import Path
from importlib import import_module

from util import greenprint,yellowboldprint,blueprint,redprint,errormessage,makeyellow
from util import info_message,critical_message

class GenPerpThreader():
    '''
    General Purpose threading implementation that accepts a generic programmatic entity

GOING TO ADD SUPPORT FOR SHELL EXANSION AVOIDANCE    
p1 = Popen(["grep", "-v", "not"], stdin=PIPE, stdout=PIPE)
p2 = Popen(["cut", "-c", "1-10"], stdin=p1.stdout, stdout=PIPE, close_fds=True)
p1.stdin.write('Hello World\n')
p1.stdin.close()
result = p2.stdout.read() 
assert result == "Hello Worl\n"

    '''
    def __init__(self,function_to_thread):
        self.thread_function = function_to_thread
        self.function_name   = getattr(self.thread_function.__name__)
        self.threader(self.thread_function,self.function_name)

    def threader(self, thread_function, name):
        info_message("Thread {}: starting".format(self.function_name))
        thread = threading.Thread(None,self.thread_function, self.function_name)
        thread.start()
        info_message("Thread {}: finishing".format(name))

class CommandDict():
    def __init__(self,dictstep:dict):
        '''init stuff
        ONLY ONE COMMAND, WILL THROW ERROR IF NOT TO SPEC
Basic shell command 
    {
    'NAME':{
        "loc": \"""ls -la\""".format(),
        "pass":"PASS MESSAGE",
        "fail":"FAIL MESSAGE",
        "info":"INFO MESSAGE"        
    }
        '''
        #check stuff
        keys = dictstep.keys()
        #  one command -----  only four fields
        assert len(keys) > 1 and len(keys[0]) != 4
        #raise exception if failure to match
        self.name     = dictstep.keys[0]
        try:
            self.cmd  = dictstep['loc']
            self.info = dictstep['info']
            self.pass = dictstep["pass"]
            self.fail = dictstep["fail"]
        except Exception:
            errormessage("[-] JSON Input Failed to MATCH SPECIFICATION!\n\n    ")

    def failfunc(self):
        '''
        called when the command fails to validate
        '''
        pass

    def __repr__(self):
        greenprint("Command:")
        print(self.name)
        greenprint("Command String:")
        print(self.cmd)

class PyBashyRun(object):
    '''
Do not call this class
    '''
    def __init__(self, jsonfunction:dict):
        self.func = CommandDict(jsonfunction)

    def exec_command(self, 
                    command,
                    blocking = True, 
                    shell_env = True):
        '''
        Internal use only
        '''
        try:
            if blocking == True:
                step = subprocess.Popen(command,
                                        shell=shell_env,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        close_fds=True)                                        
                output, error = step.communicate()
                for output_line in output.decode().split('\n'):
                    info_message(output_line)
                for error_lines in error.decode().split('\n'):
                    critical_message(error_lines)
                return step
            elif blocking == False:
                # TODO: not implemented yet                
                pass
        except Exception as derp:
            yellowboldprint("[-] Interpreter Message: exec_command() failed!")
            return derp

class PybashyRunFunction(PyBashyRun):
    ''' 
    This is the class you should use to run 

    ''' 
    def run(self ):
        '''
        Run a specific Command
        '''
        try:
            loc     = getattr(self.func,'loc')
            passmsg = getattr(self.func,'pass')
            failmsg = getattr(self.func,'fail')
            infomsg = getattr(self.func,'info')
            yellowboldprint(info_message)
            try:
                self.exec_command(loc)
                print(passmsg)
                return True
            except Exception:
                errormessage(failmsg)
                return False
        except Exception:
            errormessage("[-] Error in PybashyRunFunction.run")
            return False
        


class PybashyRunSingleJSON(PyBashyRun):
    ''' 
    This is the class you should use to run one off commands, established inline,
    deep in a complex structure that you do not wish to pick apart
    The input should contain only a single json Command() item and format()
    {   
        "IPTablesAcceptNAT": {
            "command"         : "iptables -t nat -I PREROUTING 1 -s {} -j ACCEPT".format(self.remote_IP),
            "info_message"    : "[+] Accept All Incomming On NAT Subnet",
            "success_message" : "[+] Command Sucessful", 
            "failure_message" : "[-] Command Failed! Check the logfile!"           
        }
    }
    ''' 
    def __init__(self, JSONCommandToRun:dict):
        newcmd = PybashyRunFunction(JSONCommandToRun)
        GenPerpThreader(newcmd)
        # huh... I hope that really is all it takes... that seemed simple!
