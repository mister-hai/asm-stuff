import os
import pathlib

#lolz
from pkg.snektooling.util.net.httpdownloader import HTTPDownloadRequest

scriptdir = lambda : pathlib.Path(__file__).parent.resolve()

def rootinplace():
    '''establishes this scripts operating location and relative code locations'''
    env = [projectroot,outputdirectory]

    setpaths(env)
    if 'radare2' in listofpackages:
        pulllatestrelease('radareorg','radare2')
    if 'metasploit' in listofpackages:
        metasploitinstall()
    
def appendtoselfandlock():
    '''
    Appends variables to end of immutable file for install information
    '''
    NEWVARS = '''

    '''
    with open(__file__, "w") as herp:
        herp.newlines(NEWVARS)
        herp.close()
    #now we lock this file to prevent the user from
    #accidentally reinstalling stuff and ruining 
    # the ENV we have created
    chattrself(__file__)

def setpaths(installdirs:list):
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
import pathlib


def chattrself(placement:str,flags:str='-i'):
    '''
    This defaults to SELF if empty

    Makes file immutable after install to persist settings

    chattr -i ./self
    '''
    if placement == None:
            placement = __file__
    return {
            "chattr": {
            "loc"   : "chattr {} {}".format(flags, placement ),
            "info"  : "[+] Changing File Attributes on :\n{}".format(placement),
            "succ"  : "[+] Success!", 
            "fail"  : "[-] Command Failed! Check the logfile!"           
            }}

def chatter2(location:str):
    '''
    Directly Uses a lower level interface to lock files
    '''
    # Taken from ext2fs/ext2_fs.h.
    import fcntl
    import struct
    EXT2_IMMUTABLE_FL = 0x00000010
    EXT2_IOC_SETFLAGS = 0x40086602
    fd = os.open(location, os.O_RDWR)
    f = struct.pack('i', EXT2_IMMUTABLE_FL)
    fcntl.ioctl(fd, EXT2_IOC_SETFLAGS, f)
    os.close(fd)


def installropper():
    '''
    https://github.com/sashs/Ropper/archive/refs/heads/master.zip
    target = 'https://github.com/sashs/Ropper/archive/refs/tags/v1.13.6.tar.gz'

    '''

def downloadtarfile(filename:str, target:str):
    newrequest = HTTPDownloadRequest(url = target, filter=False)
    newrequest.makerequest()
    file = newrequest.tarfileblob
    tarfile = open(filename,'wb')
    tarfile.write(newrequest.tarfileblob)
    tarfile.close()

def installpwndbg():
    '''
    Release:
        https://github.com/pwndbg/pwndbg/archive/refs/tags/2021.06.22.tar.gz
    Dev:
        https://github.com/sashs/Ropper/archive/refs/heads/master.zip
    '''
    url = "https://github.com/pwndbg/pwndbg/archive/refs/heads/dev.zip"
    downloadtarfile('pwndbg.tar.gz',url)

def pulllatestrelease(profile:str,repo:str="",method = 1):
    '''
>>> releaseurl = pulllatestrelease(profile = 'radare2org', repo = 'radare2')
>>> returncode = runshellsteps(releaseurl)
    '''
    if method == 1:
        return {
        'method1':{
            "loc": """curl --silent "https://api.github.com/{profile}/{repo}/releases/latest" \
| jq -r .tag_name""".format(profile = profile,repo = repo),
            "pass":"",
            "fail":"",
            "info":""        
            }
        }
     #if they dont support releases
    elif method == 2:
        return { 
            "method2":{
            "loc": """curl --silent "https://api.github.com/repos/{profile}/{repo}/tags" | jq -r '.[0].name'""".format(profile = profile,repo = repo),
            "pass":"success message",
            "fail":"",
            "info":""        
        }
    }
