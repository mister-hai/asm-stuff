# -*- coding: utf-8 -*-
#!/usr/bin/python3.9
################################################################################
##   Crypto tools and control flows for hacking - Vintage 2021 Python 3.9     ##
################################################################################                
# Licenced under GPLv3-modified                                               ##
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
"""
################################################################################
##############                      IMPORTS                    #################
################################################################################
import os
import cpp
import lief
import argparse
import subprocess
import pandas as pd
from subprocess import DEVNULL, STDOUT
from ast import literal_eval

################################################################################
##############           SYSTEM AND ENVIRONMENT                #################
################################################################################

def error_printer(message):
    exc_type, exc_value, exc_tb = sys.exc_info()
    trace = traceback.TracebackException(exc_type, exc_value, exc_tb) 
    try:
        redprint( message + ''.join(trace.format_exception_only()))
        #traceback.format_list(trace.extract_tb(trace)[-1:])[-1]
        blueprint('LINE NUMBER >>>' + str(exc_tb.tb_lineno))
    except Exception:
        yellow_bold_print("EXCEPTION IN ERROR HANDLER!!!")
        redprint(message + ''.join(trace.format_exception_only()))

class GenPerpThreader():
    '''
    General Purpose threading implementation that accepts a generic programmatic entity
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

################################################################################
##############                        CORE                     #################
################################################################################

class Command():
    def __init__(self, cmd_name , command_struct):
        '''init stuff
        ONLY ONE COMMAND, WILL THROW ERROR IF NOT TO SPEC
        '''
        self.name                = cmd_name
        try:
            self.cmd_line        = command_struct.get("command")
            self.info_message    = command_struct.get("info_message")
            self.success_message = command_struct.get("success_message")
            self.failure_message = command_struct.get("failure_message")
        except Exception:
            error_printer("[-] JSON Input Failed to MATCH SPECIFICATION!\n\n    ")

    def __repr__(self):
        greenprint("Command:")
        print(self.name)
        greenprint("Command String:")
        print(self.cmd_line)

class ExecutionPool():
    def __init__(self):
        '''todo : get shell/environ setup and CLEAN THIS SHIT UP MISTER'''
        self.set_actions = {}

    def get_actions_from_set(self, command_set : CommandSet):
        for attribute in command_set.items():
            if attribute.startswith("__") != True:
                self.set_actions.update({attribute : getattr(command_set,attribute)})

    def run_set(self, command_set : CommandSet):
        for field_name, field_object in command_set.items:
            if field_name in basic_items:
                command_line    = getattr(field_object,'cmd_line')
                success_message = getattr(field_object,'success_message')
                failure_message = getattr(field_object,'failure_message')
                info_message    = getattr(field_object,'info_message')
                yellow_bold_print(info_message)
                try:
                    self.exec_command(command_line)
                    print(success_message)
                except Exception:
                    error_printer(failure_message)

    def run_function(self,command_set, function_to_run ):
        '''
        '''
        try:
            #requesting a specific Command()
            command_object  = command_set.command_list.get(function_to_run)
            command_line    = getattr(command_object,'cmd_line')
            success_message = getattr(command_object,'success_message')
            failure_message = getattr(command_object,'failure_message')
            info_message    = getattr(command_object,'info_message')
            yellow_bold_print(info_message)
            try:
                self.exec_command(command_line)
                print(success_message)
            except Exception:
                error_printer(failure_message)
            # running the whole CommandSet()
        except Exception:
            error_printer(failure_message)

    def exec_command(self, command, blocking = True, shell_env = True):
        '''TODO: add formatting'''
        try:
            if blocking == True:
                step = subprocess.Popen(command,shell=shell_env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
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
            yellow_bold_print("[-] Interpreter Message: exec_command() failed!")
            return derp

class PybashyRunFunction():
    ''' 
    This is the class you should use to run one off functions, established inline,
    deep in a complex structure that you do not wish to pick apart
    The function should contain only a "steps" variable and format()
    ''' 
    def __init__(self, FunctionToRun):
        NewFunctionSet       = FunctionSet()
        #get name of function
        new_function.name  = getattr(FunctionToRun, "__name__")
        steps              = getattr(FunctionToRun, "steps")
        #itterate over the steps to get each individual action/command
        # added to the FunctionSet as a Command() via the 
        for step in steps:
            for command_name in step.keys():
                cmd_dict = step.get(command_name)
                #add the step to the functionset()
                NewFunctionSet.AddCommandDict(command_name,cmd_dict)

class PybashyRunSingleJSON():
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
        # grab the name
        NewCommandName = JSONCommandToRun.keys[0]
        # craft the command
        NewCommand = Command(NewCommandName,JSONCommandToRun)
        # init an execution pool to run commands
        execpool   = ExecutionPool()
        # run the command in a new thread
        GenPerpThreader(execpool.exec_command(NewCommand))
        # huh... I hope that really is all it takes... that seemed simple!

################################################################################
##############             COMMAND LINE ARGUMENTS              #################
################################################################################

parser = argparse.ArgumentParser(description="""\

A program to help you to automatically create fuzzing harnesses.         
""")
parser.add_argument('--librarypath',
                        dest = 'library',
                        action  = "store" ,
                        default = "" ,
                        help = "path to lib",
                        required=True
                        )
parser.add_argument('--codeqlpath',
                        dest = 'codeqlpath',
                        action  = "store",
                        default = "" ,
                        help = "path to codeql modules, database, and binary",
                        required=True
                        )
parser.add_argument('--database',
                        dest = 'database',
                        action  = "store",
                        default = "" ,
                        help = "Codeql database",
                        required=True
                        )
parser.add_argument('--multiharness',
                        dest = 'multiharness',
                        action  = "store_true",
                        default = False ,
                        help = " use this flag for multiple argument harnesses",
                        required=False
                        )

parser.add_argument('--outputdir', 
                        dest = 'outputdir',
                        action  = "store",
                        default = False ,
                        help = "Output directory",
                        required=True
                        )
parser.add_argument('--compilerflags',
                        dest = 'compilerflags',
                        action  = "store",
                        default = False ,
                        help = "compiler flags (include)",
                        required=False
                        )
parser.add_argument('--headers',
                        dest = 'headers',
                        action  = "store",
                        default = False ,
                        help = "header files, CSV string",
                        required=False)
parser.add_argument('--debug',
                        dest = 'debug',
                        action  = "store_true",
                        default = False ,
                        help = "display debugging information"
                        )
parser.add_argument('--detection', 
                        dest = 'detection',
                        action  = "store",
                        default = 'headers' ,
                        help = "'headers' to Auto-detect headers \n\
                            'functions' for function definitions? what is this dogin?.", required=True)
arguments = parser.parse_args()

cwd = lambda : os.getcwd()

def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

################################################################################
##############                  CODE SCANNER                   #################
################################################################################

#commands, top down

# if automatic detection of headers

#SEG1
#if arguments.detection == 'headers':
# "cp " + cwd + "/onearglocation.ql " + arguments.ql, shell=True)
# "cd "+ arguments.ql + ";" +arguments.ql+ "codeql query run onearglocation.ql -o " + arguments.output + "onearg.bqrs -d " + arguments.ql + arguments.database +";" + arguments.ql + "codeql bqrs decode --format=csv " + arguments.output + "onearg.bqrs -o " + arguments.output + "onearg.csv", shell=True)

#SEG2
#elif int(arguments.detection) == 1:
#"cp " + cwd + "/oneargfunc.ql " + arguments.ql, shell=True)
#            subprocess.check_output("cd "+ arguments.ql + ";" +arguments.ql+ "codeql query run oneargfunc.ql -o " + arguments.output + "onearg.bqrs -d " + arguments.ql + arguments.database +";" + arguments.ql + "codeql bqrs decode --format=csv " + arguments.output + "onearg.bqrs -o " + arguments.output + "onearg.csv", shell=True)
class Scanner(object):
    def __init__(self,arguments:parse):
        #false for single arg harness
        self.multiharnessbool = arguments.multiharness
        if not self.multiharnessbool:
            self.shared_objects = []
            self.object_functions    = {"output":[],"object":[]}
            self.total_functions     = {"function":[], "type":[],"type_or_loc":[]}
            self.defined_functions   = {"function":[], "type":[],"object": [],"type_or_loc":[]}
            self.elf_functions       = {"function":[], "type":[],"object": [],"type_or_loc":[]}
            self.shared_functions    = {"function":[], "type":[],"object": [],"type_or_loc":[]}
        #SEG1
        if arguments.detection == 'headers':
            pass
        #SEG2
        elif int(arguments.detection) == 1:
            pass
    os.chdir(arguments.library)
    for filename in os.listdir(arguments.library):
        if "shared object" in subprocess.run(["file", filename], stdout=subprocess.PIPE).stdout.decode('utf-8'):
            print("Found shared object " + filename)
            shared_objects.append(filename)
    for obj in shared_objects:
        object_functions["output"].append(subprocess.run(["readelf", "-a",obj], stdout=subprocess.PIPE).stdout.decode('utf-8'))
        object_functions["object"].append(obj)
    data = pd.read_csv(arguments.output + "onearg.csv")
    total_functions["function"] = list(data.f)
    total_functions["type"] = list(data.t)
    total_functions["type_or_loc"] = list(data.g)
    for index, define in enumerate(object_functions["output"]):
        for index2, cur in enumerate(total_functions["function"]):
            if (str(cur) in define):
                defined_functions["function"].append(cur)
                defined_functions["type"].append(total_functions["type"][index2])
                defined_functions["object"].append(object_functions["object"][index])
                defined_functions["type_or_loc"].append(total_functions["type_or_loc"][index2])
    for i in range(len(defined_functions["function"])):
        if ".so" not in str(defined_functions["object"][i]):
            elf = lief.parse(arguments.library + str(defined_functions["object"][i]))
            try:
                addr = elf.get_function_address(str(defined_functions["function"][i]))
            except: 
                continue
            elf.add_exported_function(addr, str(defined_functions["function"][i]))
            elf[lief.ELF.DYNAMIC_TAGS.FLAGS_1].remove(lief.ELF.DYNAMIC_FLAGS_1.PIE) 
            outfile = "lib%s.so" % str(defined_functions["function"][i])
            elf.write(outfile)
            elf_functions["function"].append(str(defined_functions["function"][i]))
            elf_functions["type"].append(str(defined_functions["type"][i]))
            elf_functions["object"].append(outfile)
            elf_functions["type_or_loc"].append(str(defined_functions["type_or_loc"][i]))
        else:
            shared_functions["function"].append(str(defined_functions["function"][i]))
            shared_functions["type"].append(str(defined_functions["type"][i]))
            shared_functions["object"].append(str(defined_functions["object"][i]))
            shared_functions["type_or_loc"].append(str(defined_functions["type_or_loc"][i]))
    for index3 in range(len(shared_functions["function"])):
        header_section = ""
        if not arguments.headers:
            if int(arguments.detection) == 0:
                header_section = "#include \"" + os.path.basename(shared_functions["type_or_loc"][index3]) + "\"\n\n"
            else:
                header_section = ""
        else: 
            header_list = arguments.headers.split(",")
            for x in header_list:
                header_section+= "#include \"" + x + "\"\n\n"
                
        if int(arguments.detection) == 0: 
            main_section = "int LLVMFuzzerTestOneInput(" + str(shared_functions["type"][index3]) + " Data, long Size) {\n\t" + str(shared_functions["function"][index3]) + "(Data);\n\treturn 0;\n}"
        else: 
           main_section = str(shared_functions["type_or_loc"][index3]) + " " + str(shared_functions["function"][index3]) + "(" + str(shared_functions["type"][index3])+ " testcase);\n" + "int LLVMFuzzerTestOneInput(" + str(shared_functions["type"][index3]) + " Data, long Size) {\n\t" + str(shared_functions["function"][index3]) + "(Data);\n\treturn 0;\n}" 
        full_source = header_section + main_section
        filename = "".join([c for c in str(shared_functions["function"][index3]) if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        f = open(arguments.output + filename +".c", "w")
        f.write(full_source)
        if int(arguments.detection) == 0:
            if arguments.flags is not None and int(arguments.debug) == 1:
                env = os.environ.copy()
                subprocess.Popen("clang -g -fsanitize=address,undefined,fuzzer " + arguments.flags + " -L " + arguments.output + " -L " +arguments.library + " -I" + os.path.dirname(shared_functions["type_or_loc"][index3]) + " -l:" + str((shared_functions["object"][index3])) + " " + arguments.output + filename +".c -o " + arguments.output + filename, env=env, shell=True)
            elif arguments.flags is not None and int(arguments.debug) == 0:
                env = os.environ.copy()
                subprocess.Popen("clang -g -fsanitize=address,undefined,fuzzer " + arguments.flags + " -L " + arguments.output + " -L " +arguments.library + " -I" + os.path.dirname(shared_functions["type_or_loc"][index3]) + " -l:" + str((shared_functions["object"][index3])) + " " + arguments.output + filename +".c -o " + arguments.output + filename, env=env, shell=True, stdout=DEVNULL, stderr=STDOUT)
            elif arguments.flags is None and int(arguments.debug) == 1:
               env = os.environ.copy()
               subprocess.Popen("clang -g -fsanitize=address,undefined,fuzzer -L " + arguments.output + " -L " +arguments.library + " -I" + os.path.dirname(shared_functions["type_or_loc"][index3]) + " -l:" + str((shared_functions["object"][index3])) + " " + arguments.output + filename +".c -o " + arguments.output + filename, env=env, shell=True)
            else:
               env = os.environ.copy()
               subprocess.Popen("clang -g -fsanitize=address,undefined,fuzzer -L " + arguments.output + " -L " +arguments.library + " -I" + os.path.dirname(shared_functions["type_or_loc"][index3]) + " -l:" + str((shared_functions["object"][index3])) + " " + arguments.output + filename +".c -o " + arguments.output + filename, env=env, shell=True, stdout=DEVNULL, stderr=STDOUT)
        else:
            if arguments.flags is not None and int(arguments.debug) == 1:
                env = os.environ.copy()
                subprocess.Popen("clang -g -fsanitize=address,undefined,fuzzer " + arguments.flags + " -L " + arguments.output + " -L " +arguments.library + " -l:" + str((shared_functions["object"][index3])) + " " + arguments.output + filename +".c -o " + arguments.output + filename, env=env, shell=True)
            elif arguments.flags is not None and int(arguments.debug) == 0:
                env = os.environ.copy()
                subprocess.Popen("clang -g -fsanitize=address,undefined,fuzzer " + arguments.flags + " -L " + arguments.output + " -L " +arguments.library + " -l:" + str((shared_functions["object"][index3])) + " " + arguments.output + filename +".c -o " + arguments.output + filename, env=env, shell=True, stdout=DEVNULL, stderr=STDOUT)
            elif arguments.flags is None and int(arguments.debug) == 1:
               env = os.environ.copy()
               subprocess.Popen("clang -g -fsanitize=address,undefined,fuzzer -L " + arguments.output + " -L " +arguments.library + " -l:" + str((shared_functions["object"][index3])) + " " + arguments.output + filename +".c -o " + arguments.output + filename, env=env, shell=True)
            else:
               env = os.environ.copy()
               subprocess.Popen("clang -g -fsanitize=address,undefined,fuzzer -L " + arguments.output + " -L " +arguments.library + " -l:" + str((shared_functions["object"][index3])) + " " + arguments.output + filename +".c -o " + arguments.output + filename, env=env, shell=True, stdout=DEVNULL, stderr=STDOUT)
    if (int(arguments.detection) == 1):
        for index4 in range(len(elf_functions["function"])):
            header_section = ""
            if not arguments.headers:
                    header_section = ""
            else: 
                header_list = arguments.headers.split(",")
                for x in header_list:
                    header_section+= "#include \"" + x + "\"\n\n"               
            main_section = "#include <stdlib.h>\n#include <dlfcn.h>\n\nvoid* library=NULL;\ntypedef " + str(elf_functions["type_or_loc"][index4]) + "(*" + str(elf_functions["function"][index4]) + "_t)(" + str(elf_functions["type"][index4]) + ");\n" + "void CloseLibrary()\n{\nif(library){\n\tdlclose(library);\n\tlibrary=NULL;\n}\n}\nint LoadLibrary(){\n\tlibrary = dlopen(\"" + arguments.library + str(elf_functions["object"][index4]) + "\",RTLD_LAZY);\n\tatexit(CloseLibrary);\n\treturn library != NULL;\n}\nint LLVMFuzzerTestOneInput(" + str(elf_functions["type"][index4]) + " Data, long Size) {\n\tLoadLibrary();\n\t" + str(elf_functions["function"][index4]) + "_t " + str(elf_functions["function"][index4]) + "_s = (" + str(elf_functions["function"][index4]) + "_t)dlsym(library,\"" + str(elf_functions["function"][index4]) + "\");\n\t" + str(elf_functions["function"][index4]) + "_s(Data);\n\treturn 0;\n}"
            full_source = header_section + main_section
            filename = "".join([c for c in str(elf_functions["function"][index4]) if c.isalpha() or c.isdigit() or c==' ']).rstrip()
            f = open(arguments.output + filename +".c", "w")
            f.write(full_source)
            if arguments.flags is not None and int(arguments.debug) == 1:
                env = os.environ.copy()
                print("clang -g -fsanitize=address,undefined,fuzzer " + arguments.flags + " " + arguments.output + filename +".c -o " + arguments.output + filename)
                subprocess.Popen("clang -g -fsanitize=address,undefined,fuzzer " + arguments.flags + " " + arguments.output + filename +".c -o " + arguments.output + filename, env=env, shell=True)
            elif arguments.flags is not None and int(arguments.debug) == 0:
                env = os.environ.copy()
                subprocess.Popen("clang -g -fsanitize=address,undefined,fuzzer " + arguments.flags + " " + arguments.output + filename +".c -o " + arguments.output + filename, env=env, shell=True, stdout=DEVNULL, stderr=STDOUT)
            elif arguments.flags is None and int(arguments.debug) == 1:
               env = os.environ.copy()
               subprocess.Popen("clang -g -fsanitize=address,undefined,fuzzer " + arguments.output + filename +".c -o " + arguments.output + filename, env=env, shell=True)
            else:
               env = os.environ.copy()
               subprocess.Popen("clang -g -fsanitize=address,undefined,fuzzer " + arguments.output + filename +".c -o " + arguments.output + filename, env=env, shell=True, stdout=DEVNULL, stderr=STDOUT) 
elif (int(arguments.mode) == 1):
    shared_objects=[]
    func_objects=[]
    object_functions={"output":[],"object":[]}
    cwd = os.getcwd()
    if (int(arguments.detection) == 0):
        subprocess.check_output("cp " + cwd + "/multiarglocation.ql " + arguments.ql, shell=True)
        subprocess.check_output("cd "+ arguments.ql + ";" +arguments.ql+ "codeql query run multiarglocation.ql -o " + arguments.output + "multiarg.bqrs -d " + arguments.ql + arguments.database +";" + arguments.ql + "codeql bqrs decode --format=csv " + arguments.output + "multiarg.bqrs -o " + arguments.output + "multiarg.csv", shell=True)
    elif (int(arguments.detection) == 1):
        subprocess.check_output("cp " + cwd + "/multiargfunc.ql " + arguments.ql, shell=True)
        subprocess.check_output("cd "+ arguments.ql + ";" +arguments.ql+ "codeql query run multiargfunc.ql -o " + arguments.output + "multiarg.bqrs -d " + arguments.ql + arguments.database +";" + arguments.ql + "codeql bqrs decode --format=csv " + arguments.output + "multiarg.bqrs -o " + arguments.output + "multiarg.csv", shell=True)
    data = pd.read_csv(arguments.output + "multiarg.csv")
    total_functions = data.drop_duplicates().groupby(["f", "g"], as_index=False)["t"].agg(list)
    print(total_functions)
    os.chdir(arguments.library)
    defined_functions = pd.DataFrame(columns=["f","t","g","object"])
    for filename in os.listdir(arguments.library):
        if "shared object" in subprocess.run(["file", filename], stdout=subprocess.PIPE).stdout.decode('utf-8'):
            print("Found shared object " + filename)
            shared_objects.append(filename)
    for obj in shared_objects:
        object_functions["output"].append(subprocess.run(["readelf", "-a",obj], stdout=subprocess.PIPE).stdout.decode('utf-8'))
        object_functions["object"].append(obj)
    for index, defe in enumerate(object_functions["output"]):
        for index2, cur in enumerate(total_functions["f"]):
            if (str(cur) in defe):
                func_objects.append(object_functions["object"][index])
                defined_functions = defined_functions.append([total_functions.iloc[index2,:]])
    defined_functions["object"] = func_objects
    defined_functions = defined_functions.to_dict(orient='list')
    elf_functions={"function":[], "type":[],"object": [],"type_or_loc":[]}
    shared_functions={"function":[], "type":[],"object": [],"type_or_loc":[]}
    for i in range(len(defined_functions["f"])):
        if ".so" not in str(defined_functions["object"][i]):
            elf = lief.parse(arguments.library + str(defined_functions["object"][i]))
            try:
                addr = elf.get_function_address(str(defined_functions["f"][i]))
            except: 
                continue
            elf.add_exported_function(addr, str(defined_functions["f"][i]))
            elf[lief.ELF.DYNAMIC_TAGS.FLAGS_1].remove(lief.ELF.DYNAMIC_FLAGS_1.PIE) 
            outfile = "lib%s.so" % str(defined_functions["f"][i])
            elf.write(outfile)
            elf_functions["function"].append(str(defined_functions["f"][i]))
            elf_functions["type"].append(str(defined_functions["t"][i]))
            elf_functions["object"].append(outfile)
            elf_functions["type_or_loc"].append(str(defined_functions["g"][i]))
        else:
            shared_functions["function"].append(str(defined_functions["f"][i]))
            shared_functions["type"].append(str(defined_functions["t"][i]))
            shared_functions["object"].append(str(defined_functions["object"][i]))
            shared_functions["type_or_loc"].append(str(defined_functions["g"][i]))
    for index3 in range(len(shared_functions["function"])):
        header_section = ""
        if not arguments.headers:
            if (int(arguments.detection) == 0):
                header_section += "#include <fuzzer/FuzzedDataProvider.h>\n#include <stddef.h>\n#include <stdint.h>\n#include <string.h>\n" + "#include \"" + os.path.basename(shared_functions["type_or_loc"][index3]) + "\"\n\n"
            else:
                header_section += "#include <fuzzer/FuzzedDataProvider.h>\n#include <stddef.h>\n#include <stdint.h>\n#include <string.h>\n"            
        else: 
            header_list = arguments.headers.split(",")
            header_section += "#include <fuzzer/FuzzedDataProvider.h>\n#include <stddef.h>\n#include <stdint.h>\n#include <string.h>\n"
            for x in header_list:
                header_section+= "#include \"" + x + "\"\n\n"
        stub = ""
        marker = 1
        param = ""
        header_args = ""
        for ty in literal_eval(shared_functions["type"][index3]):
            if ty.count('*') == 1:
                if "long" in ty or "int" in ty or "short" in ty and "long double" not in ty:  
                   stub  += "auto data" + str(marker) + "= provider.ConsumeIntegral<" + ty.replace("*", "") + ">();\n" + ty.replace("*", "") + "*pointer"+ str(marker) + " = &data" + str(marker) + ";\n" 
                   param += "pointer" + str(marker) + ", "
                   header_args += ty + "pointer" + str(marker) + ", "
                elif "char" in ty or "string" in ty:
                   stub  += "auto data" + str(marker) + "= provider.ConsumeIntegral<" + ty.replace("*", "") + ">();\n" + ty.replace("*", "") + "*pointer"+ str(marker) + " = &data" + str(marker) + ";\n"
                   param += "pointer" + str(marker) + ", "
                   header_args += ty + "pointer" + str(marker) + ", "
                elif "float" in ty or "double" in ty:
                    stub  += "auto data" + str(marker) + "= provider.ConsumeFloatingPoint<" + ty.replace("*", "") +">();\n" + ty.replace("*", "") + "*pointer"+ str(marker) + " = &data" + str(marker) + ";\n"
                    param += "pointer" + str(marker) + ", "
                    header_args += ty + "pointer" + str(marker) + ", "
                elif "bool" in ty:
                    stub  += "auto data" + str(marker) + "= provider.ConsumeBool();\n" + ty + "pointer"+ str(marker) + " = &data" + str(marker) + ";\n"
                    param += "pointer" + str(marker) + ", "
                    header_args += ty + "pointer" + str(marker) + ", "
                else: 
                    continue    
            elif ty.count('*') == 2:
                if "long" in ty or "int" in ty or "short" in ty and "long double" not in ty:  
                   stub  += "auto data" + str(marker) + "= provider.ConsumeIntegral<" + ty.replace("*", "") + ">();\n" + ty.replace("*", "") + "*pointer"+ str(marker) + " = &data" + str(marker) + ";\n" + ty.replace("*", "") + "**doublepointer"+str(marker) + " = &pointer"+ str(marker) + ";\n"  
                   param += "doublepointer" + str(marker) + ", "
                   header_args += ty + "doublepointer" + str(marker) + ", "
                elif "char" in ty or "string" in ty:
                   stub  += "auto data" + str(marker) + "= provider.ConsumeIntegral<" + ty.replace("*", "") + ">();\n" + ty.replace("*", "") + "*pointer"+ str(marker) + " = &data" + str(marker) + ";\n" + ty.replace("*", "") + "**doublepointer"+str(marker) + " = &pointer"+ str(marker) + ";\n" 
                   param += "doublepointer" + str(marker) + ", "
                   header_args += ty + "doublepointer" + str(marker) + ", "
                elif "float" in ty or "double" in ty:
                    stub  += "auto data" + str(marker) + "= provider.ConsumeFloatingPoint<" + ty.replace("*", "") + ">();\n" + ty.replace("*", "") + "*pointer"+ str(marker) + " = &data" + str(marker) + ";\n" + ty.replace("*", "") + "**doublepointer"+str(marker) + " = &pointer"+ str(marker) + ";\n"  
                    param += "doublepointer" + str(marker) + ", "
                    header_args += ty + "doublepointer" + str(marker) + ", "
                elif "bool" in ty:
                    stub  += "auto data" + str(marker) + "= provider.ConsumeBool();\n" + ty.replace("*", "") + "*pointer" + str(marker) + " = &data" + str(marker) + ";\n" + ty.replace("*", "") + "**doublepointer"+str(marker) + " = &pointer"+ str(marker) + ";\n"    
                    param += "doublepointer" + str(marker) + ", "
                    header_args += ty + "doublepointer" + str(marker) + ", "                    
                else: 
                    continue
            else:
                if "long" in ty or "int" in ty or "short" in ty and "long double" not in ty:  
                   stub  += "auto data" + str(marker) + "= provider.ConsumeIntegral<" + ty +">();\n" 
                   param += "data" + str(marker) + ", "
                   header_args += ty + " data" + str(marker) + ", "
                elif "char" in ty or "string" in ty:
                   stub  += "auto data" + str(marker) + "= provider.ConsumeIntegral<" + ty +">();\n"
                   param += "data" + str(marker) + ", "
                   header_args += ty + " data" + str(marker) + ", "
                elif "float" in ty or "double" in ty:
                    stub  += "auto data" + str(marker) + "= provider.ConsumeFloatingPoint<" + ty +">();\n"
                    param += "data" + str(marker) + ", "
                    header_args += ty + " data" + str(marker) + ", "
                elif "bool" in ty:
                    stub  += "auto data" + str(marker) + "= provider.ConsumeBool();\n"
                    param += "data" + str(marker) + ", "
                    header_args += ty + " data" + str(marker) + ", "
                else: 
                    continue
            marker+= 1
        param = rreplace(param,', ','',1)
        header_args = rreplace(header_args,', ','',1)
        if (int(arguments.detection) == 0):
            main_section = "extern \"C\" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {\n\tFuzzedDataProvider provider(data, size);\n\t" + stub + str(shared_functions["function"][index3]) + "(" + param + ");\nreturn 0;\n}"
        else:
            main_section = str(shared_functions["type_or_loc"][index3]) + " " + str(shared_functions["function"][index3]) +"(" + header_args + ");\n\nextern \"C\" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {\n\tFuzzedDataProvider provider(data, size);\n\t" + stub + str(shared_functions["function"][index3]) + "(" + param + ");\nreturn 0;\n}"
        full_source = header_section + main_section
        filename = "".join([c for c in str(shared_functions["function"][index3]) if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        f = open(arguments.output + filename +".cc", "w")
        f.write(full_source)
        if int(arguments.detection) == 0:
            if arguments.flags is not None and int(arguments.debug) == 1:
                env = os.environ.copy()
                print("clang++ -g -fsanitize=address,undefined,fuzzer " + arguments.flags + " -L " + arguments.output + " -L " +arguments.library + " -I" + os.path.dirname(shared_functions["type_or_loc"][index3]) + " -l:" + str((shared_functions["object"][index3])) + " " + arguments.output + filename +".cc -o " + arguments.output + filename)
                subprocess.Popen("clang++ -g -fsanitize=address,undefined,fuzzer " + arguments.flags + " -L " + arguments.output + " -L " +arguments.library + " -I" + os.path.dirname(shared_functions["type_or_loc"][index3]) + " -l:" + str((shared_functions["object"][index3])) + " " + arguments.output + filename +".cc -o " + arguments.output + filename, env=env, shell=True)
            elif arguments.flags is not None and int(arguments.debug) == 0:
                env = os.environ.copy()
                subprocess.Popen("clang++ -g -fsanitize=address,undefined,fuzzer " + arguments.flags + " -L " + arguments.output + " -L " +arguments.library + " -I" + os.path.dirname(shared_functions["type_or_loc"][index3]) + " -l:" + str((shared_functions["object"][index3])) + " " + arguments.output + filename +".cc -o " + arguments.output + filename, env=env, shell=True, stdout=DEVNULL, stderr=STDOUT)
            elif arguments.flags is None and int(arguments.debug) == 1:
               env = os.environ.copy()
               subprocess.Popen("clang++ -g -fsanitize=address,undefined,fuzzer -L " + arguments.output + " -L " +arguments.library + " -I" + os.path.dirname(shared_functions["type_or_loc"][index3]) + " -l:" + str((shared_functions["object"][index3])) + " " + arguments.output + filename +".cc -o " + arguments.output + filename, env=env, shell=True)
            else:
               env = os.environ.copy()
               subprocess.Popen("clang++ -g -fsanitize=address,undefined,fuzzer -L " + arguments.output + " -L " +arguments.library + " -I" + os.path.dirname(shared_functions["type_or_loc"][index3]) + " -l:" + str((shared_functions["object"][index3])) + " " + arguments.output + filename +".cc -o " + arguments.output + filename, env=env, shell=True, stdout=DEVNULL, stderr=STDOUT)
        else:
            if arguments.flags is not None and int(arguments.debug) == 1:
                env = os.environ.copy()
                subprocess.Popen("clang++ -g -fsanitize=address,undefined,fuzzer " + arguments.flags + " -L " + arguments.output + " -L " +arguments.library + " -l:" + str((shared_functions["object"][index3])) + " " + arguments.output + filename +".cc -o " + arguments.output + filename, env=env, shell=True)
            elif arguments.flags is not None and int(arguments.debug) == 0:
                env = os.environ.copy()
                subprocess.Popen("clang++ -g -fsanitize=address,undefined,fuzzer " + arguments.flags + " -L " + arguments.output + " -L " +arguments.library + " -l:" + str((shared_functions["object"][index3])) + " " + arguments.output + filename +".cc -o " + arguments.output + filename, env=env, shell=True, stdout=DEVNULL, stderr=STDOUT)
            elif arguments.flags is None and int(arguments.debug) == 1:
               env = os.environ.copy()
               subprocess.Popen("clang++ -g -fsanitize=address,undefined,fuzzer -L " + arguments.output + " -L " +arguments.library + " -l:" + str((shared_functions["object"][index3])) + " " + arguments.output + filename +".cc -o " + arguments.output + filename, env=env, shell=True)
            else:
               env = os.environ.copy()
               subprocess.Popen("clang++ -g -fsanitize=address,undefined,fuzzer -L " + arguments.output + " -L " +arguments.library + " -l:" + str((shared_functions["object"][index3])) + " " + arguments.output + filename +".cc -o " + arguments.output + filename, env=env, shell=True, stdout=DEVNULL, stderr=STDOUT)
    if (int(arguments.detection) == 1):
        for index4 in range(len(elf_functions["function"])):
            header_section = ""
            if not arguments.headers:
                    header_section += "#include <fuzzer/FuzzedDataProvider.h>\n#include <stddef.h>\n#include <stdint.h>\n#include <string.h>\n"            
            else: 
                header_list = arguments.headers.split(",")
                header_section += "#include <fuzzer/FuzzedDataProvider.h>\n#include <stddef.h>\n#include <stdint.h>\n#include <string.h>\n"
                for x in header_list:
                    header_section+= "#include \"" + x + "\"\n"
            stub = ""
            marker = 1
            param = ""
            header_args = ""
            for ty in literal_eval(elf_functions["type"][index4]):
                if ty.count('*') == 1:
                    if "long" in ty or "int" in ty or "short" in ty and "long double" not in ty:  
                       stub  += "auto data" + str(marker) + "= provider.ConsumeIntegral<" + ty.replace("*", "") + ">();\n" + ty.replace("*", "") + "*pointer"+ str(marker) + " = &data" + str(marker) + ";\n" 
                       param += "pointer" + str(marker) + ", "
                       header_args += ty + "pointer" + str(marker) + ", "
                    elif "char" in ty or "string" in ty:
                       stub  += "auto data" + str(marker) + "= provider.ConsumeIntegral<" + ty.replace("*", "") + ">();\n" + ty.replace("*", "") + "*pointer"+ str(marker) + " = &data" + str(marker) + ";\n"
                       param += "pointer" + str(marker) + ", "
                       header_args += ty + "pointer" + str(marker) + ", "
                    elif "float" in ty or "double" in ty:
                        stub  += "auto data" + str(marker) + "= provider.ConsumeFloatingPoint<" + ty.replace("*", "") +">();\n" + ty.replace("*", "") + "*pointer"+ str(marker) + " = &data" + str(marker) + ";\n"
                        param += "pointer" + str(marker) + ", "
                        header_args += ty + "pointer" + str(marker) + ", "
                    elif "bool" in ty:
                        stub  += "auto data" + str(marker) + "= provider.ConsumeBool();\n" + ty + "pointer"+ str(marker) + " = &data" + str(marker) + ";\n"
                        param += "pointer" + str(marker) + ", "
                        header_args += ty + "pointer" + str(marker) + ", "
                    else: 
                        continue    
                elif ty.count('*') == 2:
                    if "long" in ty or "int" in ty or "short" in ty and "long double" not in ty:  
                       stub  += "auto data" + str(marker) + "= provider.ConsumeIntegral<" + ty.replace("*", "") + ">();\n" + ty.replace("*", "") + "*pointer"+ str(marker) + " = &data" + str(marker) + ";\n" + ty.replace("*", "") + "**doublepointer"+str(marker) + " = &pointer"+ str(marker) + ";\n"  
                       param += "doublepointer" + str(marker) + ", "
                       header_args += ty + "doublepointer" + str(marker) + ", "
                    elif "char" in ty or "string" in ty:
                       stub  += "auto data" + str(marker) + "= provider.ConsumeIntegral<" + ty.replace("*", "") + ">();\n" + ty.replace("*", "") + "*pointer"+ str(marker) + " = &data" + str(marker) + ";\n" + ty.replace("*", "") + "**doublepointer"+str(marker) + " = &pointer"+ str(marker) + ";\n" 
                       param += "doublepointer" + str(marker) + ", "
                       header_args += ty + "doublepointer" + str(marker) + ", "
                    elif "float" in ty or "double" in ty:
                        stub  += "auto data" + str(marker) + "= provider.ConsumeFloatingPoint<" + ty.replace("*", "") + ">();\n" + ty.replace("*", "") + "*pointer"+ str(marker) + " = &data" + str(marker) + ";\n" + ty.replace("*", "") + "**doublepointer"+str(marker) + " = &pointer"+ str(marker) + ";\n"  
                        param += "doublepointer" + str(marker) + ", "
                        header_args += ty + "doublepointer" + str(marker) + ", "
                    elif "bool" in ty:
                        stub  += "auto data" + str(marker) + "= provider.ConsumeBool();\n" + ty.replace("*", "") + "*pointer" + str(marker) + " = &data" + str(marker) + ";\n" + ty.replace("*", "") + "**doublepointer"+str(marker) + " = &pointer"+ str(marker) + ";\n"    
                        param += "doublepointer" + str(marker) + ", "
                        header_args += ty + "doublepointer" + str(marker) + ", "                    
                    else: 
                        continue
                else:
                    if "long" in ty or "int" in ty or "short" in ty and "long double" not in ty:  
                       stub  += "auto data" + str(marker) + "= provider.ConsumeIntegral<" + ty +">();\n" 
                       param += "data" + str(marker) + ", "
                       header_args += ty + " data" + str(marker) + ", "
                    elif "char" in ty or "string" in ty:
                       stub  += "auto data" + str(marker) + "= provider.ConsumeIntegral<" + ty +">();\n"
                       param += "data" + str(marker) + ", "
                       header_args += ty + " data" + str(marker) + ", "
                    elif "float" in ty or "double" in ty:
                        stub  += "auto data" + str(marker) + "= provider.ConsumeFloatingPoint<" + ty +">();\n"
                        param += "data" + str(marker) + ", "
                        header_args += ty + " data" + str(marker) + ", "
                    elif "bool" in ty:
                        stub  += "auto data" + str(marker) + "= provider.ConsumeBool();\n"
                        param += "data" + str(marker) + ", "
                        header_args += ty + " data" + str(marker) + ", "
                    else: 
                        continue
                marker+= 1
            param = rreplace(param,', ','',1)
            header_args = rreplace(header_args,', ','',1)
            main_section = "#include <stdlib.h>\n#include <dlfcn.h>\n\nvoid* library=NULL;\ntypedef " + str(elf_functions["type_or_loc"][index4]) + "(*" + str(elf_functions["function"][index4]) + "_t)(" + header_args + ");\nvoid CloseLibrary()\n{\nif(library){\n\tdlclose(library);\n\tlibrary=NULL;\n}\n}\nint LoadLibrary(){\n\tlibrary = dlopen(\"" + arguments.library + str(elf_functions["object"][index4]) + "\",RTLD_LAZY);\n\tatexit(CloseLibrary);\n\treturn library != NULL;\n}\nextern \"C\" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {\n\tFuzzedDataProvider provider(data, size);\n\t\n\tLoadLibrary();\n\t" + stub + str(elf_functions["function"][index4]) + "_t " + str(elf_functions["function"][index4]) + "_s = (" + str(elf_functions["function"][index4]) + "_t)dlsym(library,\"" + str(elf_functions["function"][index4]) + "\");\n\t" + str(elf_functions["function"][index4]) + "_s(" + param + ");\n\treturn 0;\n}" 
            full_source = header_section + main_section
            filename = "".join([c for c in str(elf_functions["function"][index4]) if c.isalpha() or c.isdigit() or c==' ']).rstrip()
            f = open(arguments.output + filename +".cc", "w")
            f.write(full_source)
            if arguments.flags is not None and int(arguments.debug) == 1:
                env = os.environ.copy()
                subprocess.Popen("clang++ -g -fsanitize=address,undefined,fuzzer " + arguments.flags + " " + arguments.output + filename +".cc -o " + arguments.output + filename, env=env, shell=True)
            elif arguments.flags is not None and int(arguments.debug) == 0:
                env = os.environ.copy()
                subprocess.Popen("clang++ -g -fsanitize=address,undefined,fuzzer " + arguments.flags + " " + arguments.output + filename +".cc -o " + arguments.output + filename, env=env, shell=True, stdout=DEVNULL, stderr=STDOUT)
            elif arguments.flags is None and int(arguments.debug) == 1:
               env = os.environ.copy()
               subprocess.Popen("clang++ -g -fsanitize=address,undefined,fuzzer " + arguments.output + filename +".cc -o " + arguments.output + filename, env=env, shell=True)
            else:
               env = os.environ.copy()
               subprocess.Popen("clang++ -g -fsanitize=address,undefined,fuzzer " + arguments.output + filename +".cc -o " + arguments.output + filename, env=env, shell=True, stdout=DEVNULL, stderr=STDOUT) 
else:
    print("Invalid Mode")

###############################################################################
'''
Type getParameterTypeElement(Parameter p) {
  result = p.getUnspecifiedType()
  or
  result = getParameterTypeElement(p).(PointerType).getBaseType().getUnspecifiedType()
}

Type getParameterBaseType(Parameter p) {
  result = getParameterTypeElement(p) and not result instanceof PointerType
}

from Function f, Type t, string g 
where not exists(Parameter p | p = f.getAParameter() | getParameterBaseType(p) instanceof Struct) and
t = f.getAParameter().getType() and
g = f.getType().toString()
select f, t, g
'''
###############################################################################
'''
Type getParameterTypeElement(Parameter p) {
  result = p.getUnspecifiedType()
  or
  result = getParameterTypeElement(p).(PointerType).getBaseType().getUnspecifiedType()
}

Type getParameterBaseType(Parameter p) {
  result = getParameterTypeElement(p) and not result instanceof PointerType
}

from Function f, Type t, string g 
where not exists(Parameter p | p = f.getAParameter() | getParameterBaseType(p) instanceof Struct) and
t = f.getAParameter().getType() and
g = min(f.getADeclarationLocation().getContainer().toString())
select f, t, g
'''
###############################################################################
'''
from Function f, Variable v, string x, string t, string g
where
	f.getNumberOfParameters() = 1 and
	v = f.getParameter(0) and
	not (v.getUnspecifiedType() instanceof Struct) and
	not (v.getUnspecifiedType().(PointerType).getBaseType+().getUnspecifiedType() instanceof Struct) and
	x = v.getUnspecifiedType().toString() and
	x != "..(*)(..)" and
	g = f.getType().toString() and
	t = v.getType().toString()
select f, t, g
'''