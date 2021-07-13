# -*- coding: utf-8 -*-
#!/usr/bin/python3.9
################################################################################
##       Elliptic Curve for learning/hacking - Vintage 2021 Python 3.9        ##
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
__description__ = '''Calculates An eliptic curve function
https://en.wikipedia.org/wiki/One-way_compression_function
'''
__url__ = '''https://en.wikipedia.org/wiki/One-way_compression_function'''
__docs__ = '''
https://en.wikipedia.org/wiki/Avalanche_effect
A compression function mixes two fixed length inputs and produces a single fixed
length output of the same size as one of the inputs. This can also be seen as
that the compression function transforms one large fixed-length input into a
shorter, fixed-length output.

For instance, input A might be 128 bits, input B 128 bits and they are compressed
together to a single output of 128 bits. This is equivalent to having a single
256-bit input compressed to a single output of 128 bits.

Some compression functions do not compress by half, but instead by some other factor.
For example, input A might be 256 bits, and input B 128 bits, which are compressed to
a single output of 128 bits. That is, a total of 384 input bits are compressed
together to 128 output bits.

The mixing is done in such a way that full avalanche effect is achieved. That is,
every output bit depends on every input bit. 

The strict avalanche criterion (SAC) is a formalization of the avalanche effect. 
It is satisfied if, whenever a single input bit is complemented, each of the output 
bits changes with a 50% probability. The SAC builds on the concepts of completeness 
and avalanche and was introduced by Webster and Tavares in 1985.[3]

Higher-order generalizations of SAC involve multiple input bits. Boolean functions 
which satisfy the highest order SAC are always bent functions, also called maximally 
nonlinear functions, also called "perfect nonlinear" functions.[4] 

More precisely, the rate represents the 
    ratio between the number of processed bits of 
        input m  
        the output bit-length n of the block cipher, 
        and the necessary block cipher operations s to produce these n output bits. 
        
Generally, the usage of fewer block cipher operations results in a better overall 
performance of the entire hash function, but it also leads to a smaller hash-value
which could be undesirable. The rate is expressed by the formula:

Rh= |mi| / s * n 

The hash function can only be considered secure if at 
least the following conditions are met:

    The block cipher has no special properties that distinguish it from ideal ciphers, 
    such as weak keys or keys that lead to identical or related encryptions
    (fixed points or key-collisions).
    
    The resulting hash size is big enough. According to the birthday attack a security 
    level of 280 (generally assumed to be infeasible to compute today)[citation needed] 
    is desirable thus the hash size should be at least 160 bits.
    
    The last block is properly length padded prior to the hashing. 
    (See Merkle–Damgård construction.) Length padding is normally implemented and handled
    internally in specialised hash functions like SHA-1 etc.

'''
import hashlib
from app.src.util.Utils import errorprinter
from app.src.tools.BlockChunker import Chunker

class OneWayCompression():
    '''This is going to be a asfaghzdjh Function '''
    def __init__(self,outputlength: int, input1:bytes, input2:bytes):
        #cheeky fuckers, gotta validate data
        # (input1 / input2) must be bigger than output length
        # we want to compress data, not EXpress it lol
        try:
            mixingfactor = (len(input1) / len(input2)) / outputlength
            if (mixingfactor) <= 0 :
                raise ValueError("[-] Data output length does not work with provided parameters, check your data source")
            else:
                self.inputlen1 = len(input1)
                self.inputlen2 = len(input2)
                self.outputsize = outputlength
                self.chunker = Chunker()
        except Exception:
            errorprinter(Exception)

    def XORBox(self, seed, number_of_itterations):
        '''Performs XOR and shuffling operations on a grid of PRN/CSPRN
        to simply generate an even more secure byte array '''
        # Output mathy words
        XORFinal = []
        # FieldSpace K
        datafield = []

        try:
            for current_itteration in range(number_of_itterations): 
            # loop defining an X,Y coordinate system
            # for x_coordinate in Field Space K:
                for index in datafield:
                    # index + 1 is over one column to the right
                    # index - 1 is to the left
                    # Row A-D is this loop here, each data item is a Row
                    # 8-bits x 4 slots = 32-bits wide for 8-bit ascii chars
                    for byte in datafield[index]:
                        # row operations
                        # use index to access other rows as thus:
                        # data2[index] == data1[index] == current column, named row
                        pass
                self.extractor(XORFinal, datafield)
        except Exception:
            errorprinter("[-] Could not XOR bytes: ")
        return XORFinal

    def extractor(self, data1,data2):
        '''Von Neumann extractor'''
        datafield = []
        for bytefield1,bytefield2 in data1,data2:
            # if they are equal
            if bytefield1 == bytefield2:
                #discard the number
                pass
                # if they unequal
            elif bytefield1 != bytefield2:
                #save the first number
                datafield.append(bytefield1)
        return datafield


    def squish(self,bytefeed:bytes,chunksze:int,slicestep = 1):#, wordsize = 32 ):
        '''feedandseed:bytes should be a stream of random bytes'''
        split1 = []
        split2 = []
        counter1 = 0
        counter2 = 0
        pipeline1injection = ""
        #split the input streams into chunks and prepare to funnel to operations
        for thing1,thing2 in bytefeed,bytefeed:
            split1.append(self.chunker.chunker(thing1,chunksze,slicestep))
            counter1 = counter1 + 1
            split2.append(self.chunker.chunker(thing2,chunksze,slicestep))
            counter2 = counter2 +1
        #######################################################################
        # Pipeline 1, left side
        for each in split1:
            # feed the x-bit wide chunk of random data 
            # with (insert selected data here) TO BE DECIDED
            randomnesextract1 = self.extractor(each,pipeline1injection)
            hashedextract = hashlib.sha256(randomnesextract1)
        
        #######################################################################
        # Pipeline2, right side
        # try #1 :
        # I will operate on right pipe with seed
        for each in split2:
            pass

        for index1,index2 in range(self.inputlen1),range(self.inputlen2):
            #XORBox maybe?
            # multiple extractors
            index1 = index1
            index2 = index2
            #self.extractor(data1,data2)
            #self/extractor(data1,)

            pass
