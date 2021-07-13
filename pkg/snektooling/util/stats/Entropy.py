# -*- coding: utf-8 -*-
#!/usr/bin/python3.9
################################################################################
##       Entropy stuff for learning/hacking - Vintage 2021 Python 3.9         ##
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
__docs__ = '''Calculates Entropy using Equations from wikipedia

Entropy is a measure of what the password could have been so it does not really 
relate to the password itself, but to the selection process.

We define the entropy as the value S
such the best guessing attack will require, on average, S/2 guesses. 

"Average" here is an important word. We assume that the "best attacker" 
knows all about what passwords are more probable to be chosen than others, and 
will do his guessing attack by beginning with the most probable passwords. The 
model is the following: we suppose that the password is generated with a program 
on a computer; the program is purely deterministic and uses a cryptographically 
strong PRNG as source of alea (e.g. /dev/urandom on a Linux system, or 
CryptGenRandom() on Windows). The attacker has a copy of the source code of the 
program; what the attacker does not have is a copy of the random bits that the 
PRNG actually produced.

Entropy is easy to compute if the random parts of the selection process are 
uniform (e.g. with dice or a computer with a good PRNG -- as opposed to a human
being making a "random" chance in his head). For instance, if you have a list 
of 2000 words and choose one among them (uniformly), then the entropy is S=2000
. Entropy is often expressed in bits: an entropy of n bits is what you get out 
of a sequence of n bits which have been selected uniformly and independently of
each other (e.g. by flipping a coin for each bit); it is a simple logarithmic 
scale: "n bits of entropy" means "entropy is S=2n" (and the attack cost is 
then 2n−1 on average).

If you think of a password as two halves chosen independently of each other, 
then the total entropy is the product of the entropies of each half; when 
expressed with bits, this becomes a sum, because that's what logarithms do: 
they transform multiplications into sums. So if you take two words, randomly and 
independently (i.e. never ruling out any combination, even if the two words turn 
out to be the same), out of a list of 2000, then the total entropy is 2000⋅2000=4000000
. Expressed in bits, each word implies an entropy of about 11 bits 
(because 211 is close to 2000), and the total entropy is close to 22 bits
 (and, indeed, 222 is close to 4000000).
 
A decimal digit has entropy 10, as long as it is chosen randomly and uniformly and 
independently from all other random parts of the password. Since 10=23.321928... 
then each digit adds about 3.32 extra bits to the entropy.


measure the entropy of the generated bit stream coming out of your code. 
If it's maximum, it's 1 bit /bit, 8 bits /byte or 100% 
depending on your measurement scale. 

Here is a simple explanation regarding password entropy, and depending on what needs to be measured. Let's first assume two following two points:

    The password has a specific "length" (consisting of its number of characters, some of - or all of which - may be duplicate/identical and/or repeat consecutively).
    Any character in the password has been chosen from a single common library or "range" of unique characters and chosen randomly using a cryptographically secure process.

Formula:

    Log2(Possible combinations)= overall password entropy

    Range^Length=Possible combinations (can also be rounded as 2^overall password entropy)
    Log2(Range) = Entropy per character
    Entropy per character * Length = overall password entropy

Example Test:

    Range = 2048 unique character values (or 2048 unique words)
    Length =12 characters (or 12 words, some or all of which may repeat)
    Possibilities = 5444517870735015415413993718908291383296 or 2048^12
    Overall Entropy = 132 or log2(possibilities)
    Entropy per character (or per word if words are used) = 11 or log2(2048)

Another way to double-check roughly (depending on precision available if dealing with decimals and not whole number results): 2^(log2(Range)*Length) == (2^Entropy)

In Python3: 2**(int(math.log2(2048))*12) == int(2**132)
'''

import math
import numpy
import numpy as np 
from app.src.util.stats.ProbabilityMassFunction import MassProbabilityFunction as mpf
from app.src.util.Utils import errorprinter

class Entropy():
    '''Calculates Entropy of a provided set'''
    def __init__(self, csprn:list, bitsornats = "bits"):
        self.set = []
        self.e = 2.71828
        try:
            if bitsornats == "bits":
                self.b = 2
            elif bitsornats == "nats":
                self.b = self.e
        except Exception:
            errorprinter("[-] Unexpected Value for Entropy(bitsornats:str) ")

        # we are passing a set of CSPRN :
        # H(x) = Entropy([CSPRN, ...]) = loop(PMF([CSPRN] * logE(PMF([CSPRN])))

        #from index to end of list
        self.i = 0
        #print(csprn)
        self.n = len(csprn)
        self.csprn = csprn
        for i in range(self.n):
            # set to calculate item at specified index
            self.i = i
            #calculate the function for indicated entity
            #returns a Counter object
            probabilities = mpf(csprn[self.i])
            # normalize the set to obtain a dict of probabilities
            # for each event occuring
            probabilities.normalize()
            #returns values and thier probabilities in the form:
            #
            normalization = probabilities.rendersetlist()[0][1]
            #self.calculate(self.csprn,self.e)
            itementropicvalue = normalization * math.log(normalization,self.b)
            # append to the set we will sum together to provide the final value
            self.set.append(itementropicvalue)

    def sigma(self):
        return  numpy.sum(self.set)
