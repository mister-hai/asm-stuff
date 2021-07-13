# -*- coding: utf-8 -*-
#!/usr/bin/python3.9
################################################################################
##       Entropy csprn for learning/hacking - Vintage 2021 Python 3.9         ##
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
__docs__ = '''Randomness Extractor
 
    can be shown to produce a uniform output even if the distribution 
    of input bits is not uniform so long as:
        - each bit has the same probability of being one 
        - there is no correlation between successive bits.
    
From Wikipedia:
   From the input stream, his extractor took bits, two at a time 
   (first and second, then third and fourth, and so on). 
   If the two bits matched, no output was generated. 
   If the bits differed, the value of the first bit was output. 

An extractor is strong if concatenating the seed with the extractor's output 
yields a distribution that is still close to uniform. 
'''

def VonNeumanExtractor(data1,data2):
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

