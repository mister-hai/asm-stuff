
import re
import pkg.r2pipe as r2pipe
import sys,os

# this is going to be an exercise in modeling discrete objects

#the hex codes for the ASM instructions
# necessary for an exploit
# this is to be set for the system we scan
asmdict = {"x86":{
                'ret': 0xc3,
                'nop': 0x90
                }
            "armlv6":{
                'ret': 0xc3,
                'nop': 0x00                
            }
        }

class BufferOverflow(object):
    def __init__(self):
        pass
    
#this is going to be written in go?
def popreturn():
    '''pop return : If none of the registers point directly to the shellcode,
but you can see an address on the stack (first, second, … address on the stack)
that points to the shellcode, then you can load that value into EIP by first 
putting a pointer to pop ret, or pop pop ret, or pop pop pop ret 
(all depending on the location of where the address is found on the stack) 
into EIP. '''
    index1 = "pop ret"
    index2 = "pop pop ret"
    index3 = "pop pop pop ret"

class Machine(object):
    def __init__(self, FileInput):
        self.filename = FileInput
        asdf = Disassembler(filename, choice)

class RollingWindow(object):
    '''Represents a window into the application, we scan for gadgets
    from the beginning, while rolling the window BACKWARDS through the ASM
    
    returns a LIST of LISTS of instructions?
        { 'rop1': {"addr" : ROPGADGET} , 'rop2': {"addr" :ROPGADGET} , ... }
    '''
    def __init__(self,ret4thissys = whatwescanfor, filename):
        ROPGADGET = "pop pop" + ret4thissys
        test = { 'rop1': {"addr" : ROPGADGET} , 'rop2': {"addr" :ROPGADGET}}

whatwescan = RollingWindow()

# metaclass to represent a disassembled file
class DisassembledFile():
    def __init__(self, hex_string: str, filename:str):
        setattr(self, "HexString", hex_string)


class Radare2Disassembler():
    '''assigns data to a metaclass DisassembledFile()
    
     '''
    def __init__(self, FileInput):
        self.disassemble(FileInput)

    def disassemble(self,filename):
        herp = DisassembledFile("",filename)
        self.FileInput = filename

        self.radarpipe = r2pipe.open(filename)
        #setattr(herp, "__name__", FileInput)
        #setattr(herp, "__qualname__", FileInput)

        # sets fields on new meta entity
        setattr(herp, "Symbols", self.radarpipe.cmdj("isj"))
        setattr(herp, "Sections", self.radarpipe.cmdj("iSj"))
        setattr(herp, "Info", self.radarpipe.cmdj("ij"))
        setattr(herp, "arch", getattr(herp, "Info")["bin"]["arch"])
        setattr(herp, "bintype", getattr(herp, "Info")["bin"]["bintype"])
        setattr(herp, "bits", getattr(herp, "Info")["bin"]["bits"])
        setattr(herp, "binos", getattr(herp, "Info")["bin"]["os"])
        return herp
