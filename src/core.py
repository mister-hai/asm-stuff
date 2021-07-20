# -*- coding: utf-8 -*-
#!/usr/bin/python3.9
################################################################################
##  Pybash Takes JSON, READ - Vintage 2021 Python 3.9                         ##
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
import sys
import traceback
import threading
import subprocess

def errorprinter(message):
    '''Will display the error from the current "Frame Context" 
    Generally you supply an error string in the form of :
    
    "[-] ERROR: something happened in {some name here}" 

    If the exception handler throws an error, That error will be printed'''
    exc_type, exc_value, exc_tb = sys.exc_info()
    trace = traceback.TracebackException(exc_type, exc_value, exc_tb) 
    try:
        print( message + ''.join(trace.format_exception_only()))
        #traceback.format_list(trace.extract_tb(trace)[-1:])[-1]
        print('LINE NUMBER >>>' + str(exc_tb.tb_lineno))
    except Exception:
        print("EXCEPTION IN ERROR HANDLER!!!")
        print(message + ''.join(trace.format_exception_only()))

class GenPerpThreader():
    '''
    General Purpose threading implementation that accepts a generic programmatic entity
    '''
    def __init__(self,function_to_thread, threadname):
        self.thread_function = function_to_thread
        self.function_name   = threadname
        self.threader(self.thread_function,self.function_name)

    def threader(self, thread_function, name):
        print("Thread {}: starting".format(self.function_name))
        thread = threading.Thread(None,self.thread_function, self.function_name)
        thread.start()
        print("Thread {}: finishing".format(name))
    '''
Basic shell command 
def returnval():
asdf = {
    'NAME':{
        "loc": "ls -la".format(),
        "pass":"PASS MESSAGE",
        "fail":"FAIL MESSAGE",
        "info":"INFO MESSAGE"
        }
    }
ONLY ONE COMMAND, WILL THROW ERROR IF NOT TO SPEC
    '''

class CommandDict():
    def __init__(self,dictstep:dict):
        #check stuff
        try:
            name = list(dictstep.keys())[0]
            #  one command #only four fields
            if len(dictstep.keys()) == 1 and len(dictstep.get(name)) == 4:
                #raise exception if failure to match
                self.name = name
                self.loc  = dictstep[name]['loc']
                self.info = dictstep[name]['info']
                self.succ = dictstep[name]["succ"]
                self.fail = dictstep[name]["fail"]
        except Exception:
            print("[-] JSON Input Failed to MATCH SPECIFICATION!\n\n")
    
    def __repr__(self):
        print("Command:")
        print(self.name)
        print("Command String:")
        print(self.loc)

class PyBashyRun(object):
    '''
Do not call this class
    '''
    def __init__(self, jsonfunction:dict):
        self.func = CommandDict(jsonfunction)
        self.name = self.func.name

    def failfunc(self):
        '''
        called when the command fails to validate
        '''
        pass

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
                    print(output_line)
                for error_lines in error.decode().split('\n'):
                    print(error_lines)
                return step
            elif blocking == False:
                # TODO: not implemented yet                
                pass
        except Exception as derp:
            print("[-] Interpreter Message: exec_command() failed!")
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
            passmsg = getattr(self.func,'succ')
            failmsg = getattr(self.func,'fail')
            infomsg = getattr(self.func,'info')
            print(print)
            try:
                self.exec_command(loc)
                print(passmsg)
                return True
            except Exception:
                errorprinter(failmsg)
                return False
        except Exception:
            errorprinter("[-] Error in PybashyRunFunction.run")
            return False
        


class PybashyRunSingleJSON():
    ''' 
    This is the class you should use to run one off commands, established inline,
    deep in a complex structure that you do not wish to pick apart
    The input should contain only a single json Command() item and format()
    {   
        "IPTablesAcceptNAT": {
            "command"         : "iptables -t nat -I PREROUTING 1 -s {} -j ACCEPT".format(self.remote_IP),
            "print"    : "[+] Accept All Incomming On NAT Subnet",
            "success_message" : "[+] Command Sucessful", 
            "failure_message" : "[-] Command Failed! Check the logfile!"           
        }
    }
    ''' 
    def __init__(self, JSONCommandToRun:dict):
        newcmd = PybashyRunFunction(JSONCommandToRun)
        GenPerpThreader(newcmd.run, newcmd.name)
        # huh... I hope that really is all it takes... that seemed simple!


if __name__ == "__main__":
    def testreturnval():
        return {'NAME':{
                "loc": "ls -la",
                "succ":"PASS MESSAGE",
                "fail":"FAIL MESSAGE",
                "info":"INFO MESSAGE"
                }
            }
    #testing comand dict operations
    test = CommandDict(testreturnval())
    test.__repr__()
    #testing the run function
    PybashyRunSingleJSON(testreturnval())
