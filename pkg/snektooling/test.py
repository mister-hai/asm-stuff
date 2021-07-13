###############################################################################
#                             Core Imports
###############################################################################
import math
import numpy
from matplotlib import pyplot as plt

###############################################################################
#                              Local Imports
###############################################################################
from pkg.snektooling.util.stats.Entropy import Entropy
from pkg.snektooling.util.stats.Entropy import Entropy
from pkg.snektooling.util.Utils import errorprinter,GenPerpThreader
from pkg.snektooling.primitives.EllipticalCurve import EllipticalCurve,Point
from pkg.snektooling.util.Utils import modulo_multiply,modulo_pow,randombytepool
from pkg.snektooling.util.stats.ProbabilityMassFunction import MassProbabilityFunction as mpf


###############################################################################
#                            Testing / Statistics
###############################################################################
###############################################################################
#                       Plotting Elliptical Curves
###############################################################################
class PlotCurve():
    '''Plots an EllipticalCurve() with pyplot
>>> curve = EllipticalCurve(FieldSizeK:int ,a:int, b:int)'''
    def __init(self,CurveFunction:EllipticalCurve,
                    scaled = False, 
                    plotxmin = -128,
                    plotxmax =  128,
                    plotymin = -128,
                    plotymax =  128):
        # grab the information from the curve object            
        self.curve = CurveFunction
        self.x = self.curve.setofx
        self.y = self.curve.setofy
        #set plot boundries
        if scaled == True:
            raise NotImplementedError(message = "[-] Scaled plotting not implemented yet")
        elif scaled == False:
            self.plotxmin = plotxmin
            self.plotxmax = plotxmax
            self.plotymin = plotymin
            self.plotymax = plotymax
        #establish labels
        plt.title("Elliptical-Curve") 
        plt.xlabel("x")
        plt.ylabel("y") 
        #graph plot
        # x and y can be either an array, a list, or a single number
        # but sets of points must corellate by index
        # (x1,x2,x3),(y1,y2,y3) == (x1,y1),(x2,y2),(x3,y3)
        plt.plot(self.x,self.y) 
        plt.show()

class Test():
    def __init__(self):
        self.poolsize = 32 # numbers
        self.wordsize = 32 # bytes
        self.randompool = []
        self.poolofsha256randos = []

    def TestEC(self,x,a,b)->None:
        e = EllipticalCurve(x, a, b)
        # # e.plot_curve().show()
        print(e)
        p = Point(e, 2, 5, "P")
        q = 4 * p

        q.name = "2P"
        e.plot_points([p, q])
        return (modulo_multiply(26, 19, 37))

    def runtest(self):
        print("[+] Initiating Test of the Entropy() Class")
        #asdf = self.randombytepool(32)
        #print(asdf)
        ent = Entropy(randombytepool(self.poolsize,self.wordsize))
        print("Entropy of a pool of {} sha256 hashes of the numbers 0-{}".format(self.poolsize,self.wordsize))
        print(ent.sigma())

        #asdf = self.randombytepool(32)
        #print(asdf)
        ent = Entropy(randombytepool(self.poolsize,self.wordsize))
        print("Entropy of a pool of {} real random {}-bit numbers".format(self.poolsize,self.wordsize))
        print(ent.sigma())
