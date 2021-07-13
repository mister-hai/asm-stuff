# -*- coding: utf-8 -*-
#!/usr/bin/python3.9
################################################################################
##                  Uniformity Check - Vintage 2021 Python 3.9                ##
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
__description__ = '''Calculates The uniformity of a sample

'''
__url__ = '''
'''
__docs__ = '''
'''
import numpy

class UniformityCheck():
    def __init__(self):
        pass
    def uniformity(self, x):
        '''Will return a number describing the uniformity of the data fed to it
    Accepts arrays of integers/floats'''
        return lambda x : 1 - 0.5*sum( abs(x - numpy.average(x)) )/(len(x)*numpy.average(x))
    
    def check_uniformity(self,setofprn):
        '''In statistics, the bias (or bias function) of an estimator is the 
    difference between this estimator's expected value and the true value of the
    parameter being estimated. An estimator or decision rule with zero bias is 
    called unbiased. In statistics, "bias" is an objective property of an estimator.
    Bias can also be measured with respect to the median, rather than the mean 
    (expected value), in which case one distinguishes median-unbiased from the 
    usual mean-unbiasedness property.'''
        uniformityarray = []
        for csprn in setofprn:
            # comparing csprn from pool to csprn after uniformity c
            #we have to compare each number for the distance between the values
            # we save the value representing the distance between the  two
            # in its own array and average those into one number, representing 
            # the bias, we want numbers close to 0?
            uniformityarray.append(self.uniformity(csprn))
