# -*- coding: utf-8 -*-
#!/usr/bin/python3.9
################################################################################
##  Probability Mass Function for learning/hacking - Vintage 2021 Python 3.9  ##
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
https://github.com/AllenDowney/PythonCounterPmf/

In probability and statistics, a probability mass function (PMF) is a function 
that gives the probability that a discrete random variable is exactly equal to 
some value.[1] Sometimes it is also known as the discrete density function. The
 probability mass function is often the primary means of defining a discrete 
 probability distribution, and such functions exist for either scalar or 
 multivariate random variables whose domain is discrete. 

>>> num_throws = 10000
>>> outcomes = np.zeros(num_throws)
>>> for i in range(num_throws):
>>>     # let's roll the die
>>>     outcome = np.random.choice(['1', '2', '3', '4', '5', '6'])
>>>     outcomes[i] = outcome

>>> val, cnt = np.unique(outcomes, return_counts=True)
>>> prop = cnt / len(outcomes)

>>> # Now that we have rolled our die 10000 times, let's plot the results
>>> plt.bar(val, prop)
>>> plt.ylabel("Probability")
>>> plt.xlabel("Outcome")
>>> plt.show()
>>> plt.close()
'''
from collections import Counter

class MassProbabilityFunction(Counter):
    """Probability Distribution - Mass Probability
INHERITS FROM: Counter
    Dict subclass for counting hashable items.  Sometimes called a bag
    or multiset.  Elements are stored as dictionary keys and their counts
    are stored as dictionary values.
    >>> c = Counter('abcdeabcdabcaba')  # count elements from a string

"""

    def normalize(self):
        """Normalizes the PMF so the probabilities add to 1."""
        total = float(sum(self.values()))
        for key in self:
            self[key] /= total

    def __add__(self, other):
        """
Adds two distributions.
The result is the distribution of sums of values from the two.
        """
        pmf = MassProbabilityFunction()
        for key1, prob1 in self.items():
            for key2, prob2 in other.items():
                pmf[key1 + key2] += prob1 * prob2
        return pmf

    def __hash__(self):
        """Returns an integer hash value."""
        return id(self)
    
    def __eq__(self, other):
        return self is other
    
    def rendersetlist(self):
        return list(zip(*sorted(self.items())))

    def renderforplot(self):
        """Returns values and their probabilities, suitable for plotting."""
        return zip(*sorted(self.items()))

    def is_subset(self, other):
        """Checks whether self is a subset of other. """
        for char, count in self.items():
            if other[char] < count:
                return False
        return True
