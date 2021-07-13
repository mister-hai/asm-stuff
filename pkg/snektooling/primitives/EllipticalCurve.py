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
__author__  = "mr_hai - church of the subhacker"

__credits__ = {"contrib" : "Aadesh M Bagmar <aadeshbagmar@gmail.com>", "author": __author__}

__description__ = '''Calculates An eliptic curve function
https://en.wikipedia.org/wiki/Elliptic-curve_cryptography
'''
__docs__ = '''For current cryptographic purposes, an elliptic curve is a plane curve over
 a finite field (rather than the real numbers) which consists of the points 
 satisfying the equation:

    y^2 = x^3 + ax + b

along with a distinguished point at infinity, denoted ∞. The coordinates here 
are to be chosen from a fixed finite field of characteristic not equal to 2 or
3, or the curve equation will be somewhat more complicated.

This set together with the group operation of elliptic curves is an abelian 
group, with the point at infinity as an identity element. The structure of the
group is inherited from the divisor group of the underlying algebraic variety:

    Div0(E) → Pic0(E) ≃ E

The definition of elliptic curve also requires that the curve be non-singular. 
Geometrically, this means that the graph has no cusps, self-intersections, or 
isolated points. Algebraically, this holds if and only if the discriminant

    Δ = −16(4a^3 + 27b^2)

is not equal to zero. (Although the factor −16 is irrelevant to whether or not 
the curve is non-singular, this definition of the discriminant is useful in a 
more advanced study of elliptic curves.) 

The (real) graph of a non-singular curve has two components if its discriminant
is positive, and one component if it is negative. For example, in the graphs 
shown in figure to the right, the discriminant in the first case is 64, and in 
the second case is −368.


###############################################################################
###############################################################################


Let K be a field over which the curve is defined (i.e., the coefficients of the
defining equation or equations of the curve are in K) 
    and denote the curve by E.

Then the K-rational points of E are the points on E 
whose coordinates all lie in K, including the point at infinity. 

The set of K-rational points is denoted by E(K). 
    It, too, forms a group, because properties of polynomial equations show that 
        if P is in E(K), 
        then −P is also in E(K), 
        and if two of P, Q, and R are in E(K), then so is the third. 
    
    Additionally, if K is a subfield of L, then E(K) is a subgroup of E(L).

The above group can be described algebraically as well as geometrically. 
    Given the curve y^2 = x^3 + ax + b 
        over the field K (whose characteristic we assume to be neither 2 nor 3)
        
        and points 
            P = (xP, yP) 
            Q = (xQ, yQ) 
        
        on the curve, assume first that 
            xP ≠ xQ  
        
        Let y = sx + d be the line that intersects P and Q, which has the following slope:

            s = (yP − yQ) / (xP − xQ)

    Since K is a field, s is well-defined. 
    
    The line equation and the curve equation have an 
    identical y in the points xP, xQ, and xR.

        (sx + d)^2 = x^3 + ax + b

    which is equivalent to 
        0 = x^3 − (s^2 * x^2) − 2sdx + ax + b − d^2

To use ECC, all parties must agree on all the elements defining the elliptic 
curve, that is, the domain parameters of the scheme. 
The size of the field used is typically either prime 
    (and denoted as p) or is a power of two  2^m

the latter case is called the binary case, and also necessitates the 
choice of an auxiliary curve denoted by f. 
Thus the field is 
    defined by p in the prime case and the pair of m and f in the binary case. 

The elliptic curve is defined by the constants a and b used in its defining equation. 
    
Finally, the cyclic subgroup is defined by its generator (a.k.a. base point) G. 

For cryptographic application the order of G, that is the smallest positive number n 
such that n G = O 
(the point at infinity of the curve, and the identity element), is normally prime. 


USE CURVE25519!!!

    I no longer trust the constants. I believe the NSA has manipulated them through 
    their relationships with industry.
    — Bruce Schneier, The NSA Is Breaking Most Encryption on the Internet (2013)[16]

'''
__domainparams__ = '''
To use ECC, all parties must agree on all the elements defining the elliptic
curve, that is, the domain parameters of the scheme. 

The size of the field used is 

    typically either prime (and denoted as p)

    or is a power of two 2^m

the latter case is called the binary case, and also necessitates the choice of an 

    auxiliary curve denoted by f. 

Thus the field is defined by 
    
    p in the prime case 
    
    and the pair of m and f in the binary case.

The elliptic curve is defined by 
    the constants a and b used in its defining equation. 

Finally, the cyclic subgroup is defined by 
    its generator (a.k.a. base point) G. 

For cryptographic application the order of G, 
    that is the smallest positive number n 
    such that n G = O 

the point at infinity of the curve, and the identity element), 
is normally prime. 
    Since n is the size of a subgroup of E ( F p ) 
    it follows from Lagrange's theorem that the number h= 1/n * |E(Fp)| 

is an integer. 
In cryptographic applications this number h, 
called the cofactor, must be small ( h ≤ 4 {\displaystyle h\leq 4} h\leq 4) 
and, preferably, h = 1 {\displaystyle h=1} h=1. 

To summarize: in the prime case, the domain parameters are ( p , a , b , G , n , h ) 
 in the binary case, they are ( m , f , a , b , G , n , h )
'''

import math
import numpy
from typing import List, Tuple, Dict
#local imports
#from src.Utils import modulo_multiply,modulo_pow,modulo_div

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

class EllipticalCurve():
    '''represents an elliptical curve, given a,x,b
    y^2 = x^3 + ax + b 

Args:
    a (int): Coefficient for x^1
    b (int): Coefficient for x^0
    x (int): Finite field size K

syntatic representation of the ellipitcal curve function
rewrite this variable specifically when creating an inherited class.
algebraically rearrange the terms to isolate the y coordinate for any
given x coordinate
 e.g. :
>>> self.y2 = self.x**3 + (self.a*self.x)
>>> self.y  = -abs(math.sqrt(self.a*self.x + self.b + self.x**3))
'''
    def __init__(self,x,a,b)->None:
        # init is for setting up the field space K
        self.points = {}
        self.setofx = []
        self.setofy = []
        self.xmin = int
        self.xmax = int
        self.ymin = int
        self.xmax = int
        self.x = x
        self.a = a
        self.b = b

# the discriminant of a polynomial is a quantity that depends on the 
# coefficients and determines various properties of the roots. It is generally
# defined as a polynomial function of the coefficients of the original 
# polynomial. 
# The discriminant is widely used in polynomial factoring, number 
# theory, and algebraic geometry. It is often denoted by the symbol Δ .

#The discriminant of the quadratic polynomial
# 
#   ax^2 + bx + c 
# 
# with a≠0 is:
#
#    Δ = b^2 − 4ac 
#
        xmaxpowmod     = modulo_pow(b, 2, self.xmax)
        xmaxmodpow3    = modulo_pow(a, 3, self.xmax)
        xmaxmodmult4   = modulo_multiply(4, xmaxmodpow3, self.xmax)
        xmaxmodmult27  = modulo_multiply(27, xmaxpowmod, self.xmax)
        discriminant   = modulo_multiply(-16, (xmaxmodmult4 + xmaxmodmult27), self.xmax)

        self.discriminant = discriminant % self.xmax
        if not self.is_group():
            raise Exception("The curve does not satisfy condition for a group")
        self.order = len(self.find_coordinates()) + 1

    def __str__(self)->str:
        """Print the curve"""
        return "y^2 = x^3 + {}x + {} on finite field F({}).".format(self.a, self.b, self.xmax)

    def __eq__(self, other)->bool:
        """Check if two curves are equal
    Returns:
        Boolean value suggesting equality of the curves
        """
        return (self.a, self.b) == (other.a, other.b)

    def evaluate_lhs(self, y: int)->int:
        return modulo_pow(y, 2, self.xmax)

    def evaluate_rhs(self, x: int)->int:
        return (modulo_pow(x, 3, self.xmax) + modulo_multiply(x, self.a, self.xmax) + self.b) % self.xmax
 
    def is_group(self)->bool:
        """An Elliptic curve satisfies the condition to be a group only if the 
discriminant is non-zero
        Returns:
            Boolean whether it is a group or not.
        """
        return self.discriminant != 0

    def find_coordinates(self)->List[Tuple]:
        '''old code, used to slice from range(0..x)
        returns a '''
        coordinate_list = []
        for index in range(self.xmin, self.xmax):
            rhs = self.evaluate_rhs(index)
            y = math.sqrt(rhs)

            if y.is_integer():
                y = int(y)

                coordinate_list.append((index % self.xmax, y % self.xmax))
                coordinate_list.append((index % self.xmax, -y % self.xmax))

        return coordinate_list

    def findslope(self):
        '''s = (yP - yQ) / (xP - xQ)'''

    def plot_points(self, annotated_points: [])->None:
        coordinates = self.find_coordinates()
        x = [x[0] for x in coordinates]
        y = [x[1] for x in coordinates]

        fig, ax = numpy.plot.subplots()
        ax.scatter(x, y)
        numpy.plot.grid()

        for point in annotated_points:
            ax.annotate("{} ({}, {})".format(point.name, point.x, point.y),
                        (point.x, point.y), xytext=(point.x + 1.5, point.y + 0.5),
                        arrowprops=dict(facecolor='black', shrink=0.05))
        numpy.plot.show()

    def slicecurve(self):
        '''This function will fill an array with a set of points representing the curve
        within the slice limits '''
        for point in range(self.xmin, self.xmax):
            # the curve definition itself goes here
            # we add the basic solution here
            # set the x-coordinate to calculate a y-coordinate
            self.x = point
            # calculate the classical formula
            self.y2 = self.x**3 + (self.a*self.x)
            # solve for the y-coordinate
            self.y = -abs(math.sqrt(self.a*self.x + self.b + self.x**3))
            # add the calculated point to the set of all 
            # points in field K that intersect with the curve
            self.points.update((self.x,self.y))
            # use some RAM to make a set of x,y suitable for plotting
            self.setofx.append(self.x)
            self.setofy.append(self.y)
            # we have now sliced out the line from lim(xmin,xmax)

class Point:
    '''This is backwards, a curve is a collection of points
    This should be named "point reference" or similar as you feed it the 
    EllipticalCurve() Object rather than EllipticalCurve()
    inheriting from Point()'''
    def __init__(self, curve: EllipticalCurve, x: int, y: int, name: str="")->None:
        self.curve = curve
        self.x = x % self.curve.field
        self.y = y % self.curve.field
        self.name = name

        if not self.test_point():
            raise Exception("The given point ({}, {}) is not on the curve {}.".format(self.x, self.y, curve))

    def test_point(self)->bool:
        return self.curve.evaluate_lhs(self.y) == self.curve.evaluate_rhs(self.x)

    def plot_point(self)->None:
        self.curve.plot_points({self.name: (self.x, self.y)})

    def __neg__(self):
        return Point(self.curve, self.x, -self.y, "{}'".format(self.name))

    def __str__(self)->str:
        return "Point {} = ({}, {})".format(self.name, self.x, self.y)

    def __eq__(self, other):
        return (self.curve, self.x, self.y) == (other.curve, other.x, other.y)

    def __add__(self, Q):
        """
        Args:
            Q: Adding a point to self
        Returns:
            Point object after adding a point
        """

        if isinstance(Q, Ideal):
            return self

        x1 = self.x
        y1 = self.y
        x2 = Q.x
        y2 = Q.y
        #if the points are the same
        if (x1, y1) == (x2, y2):
            if y1 == 0:
                return Ideal(self.curve)
            modpowKx2 = modulo_pow(x1, 2, self.curve.field)
            modmultKy2 = modulo_multiply(2, y1, self.curve.field)
            modmultKy3 = modulo_multiply(3, modpowKx2,self.curve.field)
            numerator = (modmultKy3 + self.curve.a) % self.curve.field
            denominator = modmultKy2 % self.curve.field

            slope = modulo_div(numerator, denominator, self.curve.field)
        else:
            if x1 == x2:
                return Ideal(self.curve)

            numerator = (y2 - y1) % self.curve.field
            denominator = (x2 - x1) % self.curve.field
            slope = modulo_div(numerator, denominator, self.curve.field)

        x3 = (modulo_pow(slope, 2, self.curve.field) - x2 - x1) % self.curve.field
        y3 = (modulo_multiply(slope, (x3 - x1) % self.curve.field, self.curve.field) + y1) % self.curve.field

        return Point(self.curve, x3, -y3)

    def __mul__(self, n: int):
        """
        Multiplying a scalar to a point in a field.
        Args:
            n (int): Scalar to multiple
        Returns:
            Point object
        """
        if n < 0:
            return -self * -n
        if n == 0:
            return Ideal(self.curve)
        else:
            Q = self
            R = self if n & 1 == 1 else Ideal(self.curve)
            i = 2
            while i <= n:
                Q = Q + Q

                if n & i == i:
                    R = Q + R
                i = i << 1
        return R

    def __rmul__(self, n: int):
        return self * n

class Ideal(Point):
    def __init__(self, curve):
        self.curve = curve
        self.x = 0
        self.y = 0

    def __str__(self)->str:
        return "Ideal"

    def __neg__(self):
        return self

    def __add__(self, Q):
        return Q
