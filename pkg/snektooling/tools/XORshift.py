# -*- coding: utf-8 -*-
#!/usr/bin/python3.9
################################################################################
##       Entropy thing for learning/hacking - Vintage 2021 Python 3.9         ##
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

from Utils import errorprinter
from VonNeumanExtractor import VonNeumanExtractor
class XORShift():
    def __init__(self):
        pass

    def XORBox(self, seed, number_of_itterations):
        '''Performs XOR and shuffling operations on a grid of PRN/CSPRN
        to simply generate an even more secure byte array '''
        XORFinal = []
        datafield = []

        try:
            # to begin with, we wrap everything in an itterator to perform 
            # multiple passes of the XOR/shift, allowing us to use the randomness
            # extractor to create a new number 
            for current_itteration in range(number_of_itterations): 
            # think of this loop as defining an X,Y coordinate system
            # we are taking byte fields and stretching them into a line
            # equal to thier size
            # but one number (index) we define on the fly, inside the loop
            # for x_coordinate in y_coordinate:
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
                    #Row B
                    for byte in datafield[index == 1]:
                        #row operations
                        pass
                    # ... And so on
                VonNeumanExtractor(XORFinal, datafield)
        except Exception:
            errorprinter("[-] Could not XOR bytes: ")
        return XORFinal

