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
Utilities and boiler plate
"""

################################################################################
##############                   IMPORTS                       #################
################################################################################
import time
import sys,os
import hashlib
import inspect
import logging
import pkgutil
import secrets
import socket
import traceback
import threading
import subprocess
import cryptography
from pathlib import Path
from binascii import hexlify
from cryptography.fernet import Fernet
try:
    import colorama
    from colorama import init
    init()
    from colorama import Fore, Back, Style
    if TESTING == True:
        COLORMEQUALIFIED = True
except ImportError as derp:
    print("[-] NO COLOR PRINTING FUNCTIONS AVAILABLE, Install the Colorama Package from pip")
    COLORMEQUALIFIED = False

################################################################################
##############               LOGGING AND ERRORS                #################
################################################################################
LOGLEVEL            = 'DEV_IS_DUMB'
LOGLEVELS           = [1,2,3,'DEV_IS_DUMB']
log_file            = 'pybashy'
logging.basicConfig(filename=log_file, format='%(asctime)s %(message)s', filemode='w')
logger              = logging.getLogger()
script_cwd          = Path().absolute()
script_osdir        = Path(__file__).parent.absolute()

redprint          = lambda text: print(Fore.RED + ' ' +  text + ' ' + Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
blueprint         = lambda text: print(Fore.BLUE + ' ' +  text + ' ' + Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
greenprint        = lambda text: print(Fore.GREEN + ' ' +  text + ' ' + Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
yellow_bold_print = lambda text: print(Fore.YELLOW + Style.BRIGHT + ' {} '.format(text) + Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
makeyellow        = lambda text: Fore.YELLOW + ' ' +  text + ' ' + Style.RESET_ALL if (COLORMEQUALIFIED == True) else text
makered           = lambda text: Fore.RED + ' ' +  text + ' ' + Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makegreen         = lambda text: Fore.GREEN + ' ' +  text + ' ' + Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makeblue          = lambda text: Fore.BLUE + ' ' +  text + ' ' + Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
debug_message     = lambda message: logger.debug(blueprint(message)) 
info_message      = lambda message: logger.info(greenprint(message))   
warning_message   = lambda message: logger.warning(yellow_bold_print(message)) 
error_message     = lambda message: logger.error(redprint(message)) 
critical_message  = lambda message: logger.critical(yellow_bold_print(message))

is_method          = lambda func: inspect.getmembers(func, predicate=inspect.ismethod)

def errorprinter(message):
    '''Will display the error from the current "Frame Context" 
    Generally you supply an error string in the form of :
    
    "[-] ERROR: something happened in {some name here}" 
    
    If the exception handler throws an error, That error will be printed'''
    exc_type, exc_value, exc_tb = sys.exc_info()
    trace = traceback.TracebackException(exc_type, exc_value, exc_tb) 
    try:
        redprint( message + ''.join(trace.format_exception_only()))
        #traceback.format_list(trace.extract_tb(trace)[-1:])[-1]
        blueprint('LINE NUMBER >>>' + str(exc_tb.tb_lineno))
    except Exception:
        yellow_bold_print("EXCEPTION IN ERROR HANDLER!!!")
        redprint(message + ''.join(trace.format_exception_only()))


################################################################################
##############                PyAES FUNCTIONS                  #################
################################################################################
# The MIT License (MIT)
#
# Copyright (c) 2014 Richard Moore
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Why to_bufferable?
# Python 3 is very different from Python 2.x when it comes to strings of text
# and strings of bytes; in Python 3, strings of bytes do not exist, instead to
# represent arbitrary binary data, we must use the "bytes" object. This method
# ensures the object behaves as we need it to.
def to_bufferable(binary):
    return binary

def _get_byte(c):
    return ord(c)

try:
    xrange
except:
    def to_bufferable(binary):
        if isinstance(binary, bytes):
            return binary
        return bytes(ord(b) for b in binary)

    def _get_byte(c):
        return c

def append_PKCS7_padding(data):
    pad = 16 - (len(data) % 16)
    return data + to_bufferable(chr(pad) * pad)

def strip_PKCS7_padding(data):
    if len(data) % 16 != 0:
        raise ValueError("invalid length")

    pad = _get_byte(data[-1])

    if pad > 16:
        raise ValueError("invalid padding byte")

    return data[:-pad]

################################################################################
##############            MATHMATICAL FUNCTIONS                #################
################################################################################
#   Primary Author: Aadesh M Bagmar <aadeshbagmar@gmail.com>
#   Purpose: Mathematical Helper functions

from typing import Tuple

def modulo_multiply(a: int, b: int, mod: int) -> int:
    """Evaluates a * b % mod"""
    if mod == 0:
        raise Exception("Divide by zero error")
    return ((a % mod) * (b % mod)) % mod

def modulo_pow(a: int, b: int, mod: int) -> int:
    """Evaluates a^b % mod.
    Args:
        a (int): Base
        b (int): Power
        mod (int): Modulo
    Returns:
        a ^ b % mod"""
    result = 1
    while b:
        result = modulo_multiply(result, a, mod)
        b -= 1
    return result % mod

def egcd(a: int, b: int)->Tuple[int, int, int]:
    """Extended Euclidean algorithm to compute the gcd
    Taken from https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
    Returns:
        A tuple (g, x, y) where a*x + b*y = gcd(x, y)"""
    if a == 0:
        return (b, 0, 1)
    g, x, y = egcd(b % a, a)
    return (g, y - (b // a) * x, x)

def modulo_div(a: int, b: int, mod: int) -> int:
    """Evaluates (a / b) % mod"""
    return modulo_multiply(a, mulinv(b, mod), mod)

def mulinv(b: int, n: int) -> int:
    """Multiplicative inverse of b modulo n"""
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n
    raise Exception("Modular Inverse does not exist")

################################################################################
##############              RANDOM DATA SOURCES                #################
################################################################################

#def source4(thread):
#    thread_id = threading.get_ident(thread)
#    asdf = time.pthread_getcpuclockid(thread_id)
#    Return the clk_id of the thread-specific CPU-time clock for the specified thread_id.
#    Use threading.get_ident() or the ident attribute of threading.Thread objects to get a suitable value for thread_id.
#    Warning
#    Passing an invalid or expired thread_id may result in undefined behavior, such as segmentation fault.

def source1(bytesize):
    '''return os.urandom(self.bytesize)'''
    return os.urandom(bytesize)

def source2(bytesize):
    '''return secrets.randbits(self.bytesize)'''
    return secrets.randbits(bytesize)
    
def source3():
    '''return time.time_ns()'''
    timenow = time.time_ns()
    return timenow

def tcpsocket():
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
            conn.sendall(data)


def randombytes(bytesize):
    return secrets.token_bytes(bytesize)

def randombytepool(poolsize,bytesize):
    '''fills a pool with random bytes'''
    randompool = []
    for i in range(poolsize):
        i=i
        randompool.append(randombytes(bytesize))
    return randompool

def fillthepoolSHA256CounterMode(poolsize):
    '''fills a pool with sha256 hashes from a counter run to lim(x)'''
    poolofsha256randos = []
    for i in range(poolsize):
        herp = hashlib.sha256()
        herp.update(i)
        poolofsha256randos.append(herp.digest())
    return poolofsha256randos
    

################################################################################
##############                   CRYPTOGRAPHY                  #################
################################################################################

class Key():
    ''' turns a string into a key byte array, or generates a secure random key'''
    def __init__(self,load:bool,generate:bool,KeyfileName:str, bitlength = 32):
        self.bitsize = bitlength
        if generate == True:
            self.CreateKeyFernet(KeyfileName)

    def CreateKeyFernet(self,name:str):
        """Generates a key and save it into a file"""
        key = Fernet.generate_key()
        key_file = open(name, "wb", encoding = "utf-8")
        key_file.write(key)
        key_file.close()

    def CreateKeySecrets(self):
        return secrets.randbits(self.bitsize)

    def LoadKeyFernet(self,name:str):
        """Loads the key from the current directory."""
        return open(name, "rb").read()

class Hash():
    '''implementation of multiple hashing algorhithms to obtain key bytes from 
a string and salt
typeofhash = "sha256" || "sha512" || "md5"
'''
    def __init__(self, typeofhash:int, password:str):
        #after salting the passwords with a PBKDF...
        self.type   = typeofhash
        try:
            if typeofhash == "sha256":
                self.Digest = self.sha256(bytes(password))
            elif typeofhash=="sha512":
                self.Digest = self.sha512(bytes(password))
            elif typeofhash == "md5":
                self.Digest = self.md5(bytes(password))
            else:
                raise Exception
        except Exception:
            print("[-] Error in HashString.__init__")
            SystemExit

    def md5(self,keybytes:bytes):
        ''' returns a sha512 digest of a password after salting with PBKDF'''
        herp = hashlib.md5()
        herp.update(keybytes)
        return herp.digest()

    def sha256(self,keybytes:bytes,encoding =  "utf-8"):
        ''' returns a sha256 digest of a password after salting with PBKDF'''
        herp = hashlib.sha256()
        herp.update(keybytes)
        return herp.digest()

    def sha512(self,keybytes:bytes,encoding =  "utf-8"):
        ''' returns a sha512 digest of a password after salting with PBKDF'''
        herp = hashlib.sha512()
        herp.update(keybytes)
        return herp.digest()

class Seed():
    '''You must invoke a high entropic value in the system from which a
 ciphertext is derived from a plaintext'''
    def __init__(self,source = "internal"):

        pass

class PBKDF():
    '''Implementation of multiple Password Based Key Derivation Algorhithms
    password and salt must be bytes-like objects. 
    salt should be about 16 or more bytes from a proper source    
        n      = CPU/Memory cost factor
        r      = block size
        p      = parallelization factor 
        maxmem = limits memory 
                    - (OpenSSL 1.1.0 defaults to 32 MiB). 
        dklen  = length of the derived key.
'''
    def __init__(self, salt:str, password:str, bitsrequired:int):
        pass

    def pbkdf2(self, type:str,password:bytes,salt:bytes):
        '''returns the hex encoding of the key, derived from a password string'''
        derivedkey = hashlib.pbkdf2_hmac(type, password, salt, 100000)
        return derivedkey.hex()

    def ScryptKey(self, password,salt,n,r,p):
        '''returns the hex encoding of the key, derived from a password string'''
        derivedkey = hashlib.scrypt(password, salt, n, r, p, maxmem=0, dklen=64)
        return derivedkey.hex()

class Salt():
    '''used to generate a salt
    Salt factor 5 seems reasonable at first glance
    itteration value
    '''
    def __init__(self,bytesize:int, saltfactor = 5):
        self.entropypoolcoefficient = saltfactor
        self.poursalt(bytesize)
    
    def poursalt(self, bytesize:int):
        #herp = EntropyPool(bytesize, 3)
        #return herp.SaltMine(bytesize)
        pass

class Encrypt():
    ''''''
    def __init__(self, plaintext, salt, password):
        pass
    
    def Fernet(self, key, salt, plaintext):
        herp = Fernet(key)
        ciphertext = herp.encrypt(plaintext)
        return ciphertext
    
    def aesGCM(self):
        pass

class Decrypt():
    def __init__(self):
        pass

    def Fernet(self, key, salt, plaintext):
        herp = Fernet(key)
        ciphertext = herp.decrypt(plaintext)
        return ciphertext

################################################################################
##############           SYSTEM AND ENVIRONMENT                #################
################################################################################
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