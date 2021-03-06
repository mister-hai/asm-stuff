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
https://en.wikipedia.org/wiki/Elliptic-curve_cryptography
'''
__docs__ = '''

###############################################################################
Add these to the __docs__ var as a dict
https://en.wikipedia.org/wiki/Nothing-up-my-sleeve_number
###############################################################################

In cryptography, Curve25519 is an elliptic curve offering 128 bits of security 
(256 bits key size) and designed for use with the elliptic curve Diffie–Hellman 
(ECDH) key agreement scheme.

It is one of the fastest ECC curves and is not covered by any known patents

    The reference implementation is public domain software


The original Curve25519 paper defined it as a Diffie–Hellman (DH) function. 
Daniel J. Bernstein has since proposed that the name Curve25519 be used for the 
underlying curve, and the name X25519 for the DH function.

The curve used is 
    y^2 = x^3 + 486662*x^2 + x 

A Montgomery curve, over the prime field defined by the prime number 
    2^255 − 19

and it uses the base point 
    x=9 

This point generates a cyclic subgroup whose order is the prime 
    2^252 + 27742317777372353535851937790883648493 

this subgroup has a co-factor of 
    8

meaning the number of elements in the subgroup is 
    1/8 

that of the elliptic curve group. 
Using a prime order subgroup prevents mounting a Pohlig–Hellman attack.

https://en.wikipedia.org/wiki/Pohlig%E2%80%93Hellman_algorithm

You can use this attack, when the order of the field of the elliptic curve 
is not prime ( you can use it with a prime field, too, but it is not useful)
    
The Pohlig-Hellman algorithm reduces the discrete logarithm from a group of 
composite order to subgroups of prime order. For instance, with an elliptic 
curve and a point P
    whose order is a composite integer q=p1⋅p2, 

and we want to find k:

    such that Q=[k]P for a given point Q. 
    
    Then, since [p2]P is a point of order p1. 
    
    Let:
        Q2=[p2]Q,andP2=[p2]P

    and now we have Q2=[kmodp1]P2. 
    
    Generic discrete logarithm algorithms 
    can then be used to get to obtain kmodp1.

With Q1=[p1]Q and P1=[p1]P, we obtain kmodp2 and the 
    Chinese Remainder Theorem can be used to solve the 
    following system of equations: 
    x⋅(p/f1)P=(p/f1)Q, 
    x⋅(p/f2)P=(p/f2)Q, 
    ... ,
     x⋅(p/fn)P=(p/fn)Q. 
     
     So this can be used to calculate the private key 
     by just knowing the public key. 

Then, the security depends mainly on the largest prime 
in the decomposition of q. That's why points whose order
 q is a large prime is chosen.

Curve25519 is constructed such that it avoids many potential implementation 
pitfalls.[7]
By design, it is immune to timing attacks and it accepts any 32-byte string
as a valid public key and does not require validating that a given point 
belongs to the curve, or is generated by the base point. 
'''
import os,sys
import math
import numpy

from pkg.snektooling.primitives.EllipticalCurve import EllipticalCurve

class Curve25519(EllipticalCurve):
    '''represents a Curve25519 elliptical curve
   y^2 = x^3 + 486662*x^2 + x  
   
   INHERITS FROM EllipticalCurve()

    soln1: 
        y = -sqrt(x) sqrt(x^2 + 486662 x + 1)
   '''
    def __init__(self,limits:tuple):
        '''Inputs are:
    limits:tuple == (xmin:int, xmax:int)'''
        #starts at 9 on the x plane       
        self.x = 9
        #validate inputs
        if (limits[0] != limits[1]) and (limits[0] > limits[1]):
            self.xmin = limits[0]
            self.xmax = limits[1]
        else:
            raise ValueError("[-] ERROR: Lim1 equal or greater than Lim2, use Point()\
                 or ReverseSlice() to obtain those values")
        #special technical coefficient I dont understand
        self.a = 486662
        self.b = self.x ** 2
        self.y2 = (self.x ** 3) + (self.a*self.x)
        self.y = -abs(math.sqrt(self.x)) * math.sqrt(self.x**2 + self.a * self.x + 1)

    def curve(self):
        for point in range(self.xmin, self.xmax):
            # the curve definition itself goes here
            # set the function to calculate for y
            # at the currently indexed point x
            self.x = point
            self.y2 = self.x**3 + (self.a*self.x)
            self.y = -abs(math.sqrt(self.x)) * math.sqrt(self.x**2 + self.a * self.x + 1)
            # add the calculated point to the set of all 
            # points in field K that intersect with the curve
            self.points.update((self.x,self.y))
