



def rootinplace():
    '''establishes this scripts operating location and relative code locations'''
    env = [projectroot,outputdirectory,]

    setpaths(env)
    if INSTALL:
        if 'radare2' in listofpackages:
            pulllatestrelease('radareorg','radare2')
        if 'metasploit' in listofpackages:
            metasploitinstall()
    

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
