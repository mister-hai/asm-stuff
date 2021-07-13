# -*- coding: utf-8 -*-
#!/usr/bin/python3.9
################################################################################
##      Mersenne Twist for learning/hacking - Vintage 2021 Python 3.9         ##
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
'''
This tutorial uses code from the following sources:
https://github.com/yinengy/Mersenne-Twister-in-Python

The general algorithm is characterized by the following 
quantities (some of these explanations make sense only 
after reading the rest of the algorithm):

For a w-bit word length, the Mersenne Twister generates integers 
    
    in the range [0, 2^w−1]. 
    
    w: word size (in number of bits)

    n: degree of recurrence

    m: middle word, an offset used in the recurrence relation defining 
        the series x, 1 ≤ m < n

    r: separation point of one word, or the number of bits of the
        lower bitmask, 0 ≤ r ≤ w − 1

    a: coefficients of the rational normal form twist matrix

    b, c: TGFSR(R) tempering bitmasks

    s, t: TGFSR(R) tempering bit shifts

    u, d, l: additional Mersenne Twister tempering bit shifts/masks
    

with the restriction that 2nw−r − 1 is a Mersenne prime. This 
choice simplifies the primitivity test and k-distribution test 
that are needed in the parameter search. 


'''



class MersenneTwist():
    '''seed with a good CSPRN

    Inputs:
        seed == 32-bit data item
    
    Outputs:
        32-bit pseudo random number
    Uses a mersenne twister to generate random numbers'''
    def __init__(self):
        # coefficients for MT19937
        (self.wordsize, self.degreeofrecurrance, self.middleword, self.r) = (32, 624, 397, 31)
        self.twistmatrixcoefficient = 0x9908B0DF
        (self.u, self.d) = (11, 0xFFFFFFFF)
        (self.s, self.b) = (7, 0x9D2C5680)
        (self.t, self.c) = (15, 0xEFC60000)
        self.l = 18
        self.f = 1812433253
        # make an array to store the state of the generator
        self.MT = [0 for i in range(self.degreeofrecurrance)]
        self.index = self.degreeofrecurrance+1
        self.lower_mask = 0xFFFFFFFF #int(bin(1 << r), 2) - 0b1
        self.upper_mask = 0x00000000 #int(str(-~lower_mask)[-w:])
        
        #print(extract_number())
    
    def seedtwister(self,seed):
        '''initialize the generator from a seed'''
        self.mt_seed(seed)

    def mt_seed(self, seed):
        # global self.index = int
        # self.index = n
        self.MT[0] = seed
        for i in range(1, self.degreeofrecurrance):
            temp = self.f * (self.MT[i-1] ^ (self.MT[i-1] >> (self.wordsize-2))) + i
            self.MT[i] = temp & 0xffffffff

    # Extract a tempered value based on MT[index]
    # calling twist() every n numbers
    def extract_number(self):
        ''' call this function after MersenneTwist.seedtwister(seed)
 to return a value'''
        self.index = int
        if self.index >= self.degreeofrecurrance:
            self.twist()
            self.index = 0

        y = self.MT[self.index]
        y = y ^ ((y >> self.u) & self.d)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ (y >> self.l)

        self.index += 1
        return y & 0xffffffff
    
    # Generate the next n values from the series x_i
    def twist(self):
        for i in range(0, self.degreeofrecurrance):
            x = (self.MT[i] & self.upper_mask) + (self.MT[(i+1) % self.degreeofrecurrance] & self.lower_mask)
            xA = x >> 1
            if (x % 2) != 0:
                xA = xA ^ self.twistmatrixcoefficient
            self.MT[i] = self.MT[(i + self.middleword) % self.degreeofrecurrance] ^ xA

    def random(self):
        """ return uniform ditribution in [0,1) """
        # a = (self.extract_number() / 10**8) % 1
        # return float('%.08f' % a)
        return self.extract_number() / 4294967296  # which is 2**w

    def randint(self, a, b):
        """ return random int in [a,b) """
        n = self.random()
        return int(n/(1/(b-a)) + a)

    def shuffle(self, X):
        """ shuffle the sequence """
        newX = list(X)
        for i in range(10*len(X)):
            i=i
            a = self.randint(0, len(X))
            b = self.randint(0, len(X))
            newX[a], newX[b] = newX[b], newX[a]

        return newX

    def choice(self, X, replace=True, size=1):
        """ choice an element randomly in the sequence 
            size: the number of element to be chosen
        """
        newX = list(X)
        if size == 1:
            return newX[self.randint(0, len(newX))]
        else:
            if replace:
                return [newX[self.randint(0, len(newX))] for i in range(size)]
            else:
                l = []
                for i in range(size):
                    i = i
                    if len(newX) != 0:
                        a = self.randint(0, len(newX))
                        l += [newX[a]]
                        newX.remove(newX[a])
                return l

    def bern(self, p):
        """ generate a Bernoulli Random Variable
            p: the probability of True
        """
        return self.random() <= p

    def binomial(self, n, p):
        """ generate a Binomial Random Variable
            n: total times
            p: probability of success
        """
        a = [self.bern(p) for n in range(n)]
        return a.count(True)

    def geometric(self, p):
        """ generate a Geometric Random Variable
            p: probability of success
        """
        u = self.random()
        b = 0
        k = 1
        while b < u:
            b += (1-p)**(k-1)*p
            k += 1

        return k - 1