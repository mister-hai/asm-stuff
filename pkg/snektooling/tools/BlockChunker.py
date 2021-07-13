# -*- coding: utf-8 -*-
#!/usr/bin/python3.9
################################################################################
##         Variable Bit Width Data Chunker - Vintage 2021 Python 3.9          ##
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
__description__ = '''Chunks Data for passing into a block cipher
'''
__url__ = '''
'''
__docs__ = '''
'''
class Chunker():
    def __init_(self, chunksize = 512, slicestepsize = 1):
        self.chunks = []
        self.chunksize = chunksize
        self.slicestepsize = slicestepsize

    def chunker(self, datainput:bytes , chunksize:int, slicestepsize:int)->bytes:
        '''operates on a stream of input, chunking to specified bytelength
    output.append([datainput[0:chunksize:slicestepsize]])
    
    Typically it will be 128,256,512 bits. Pad with 0's in the last block for the unchunker'''
        output = []
        for lengthindex in range(chunksize):
            lengthindex = lengthindex
            output.append([datainput[0:chunksize:slicestepsize]])
        return output

    def unchunker(self, datainput:bytes , chunksize:int, slicestepsize:int)->bytes:
        '''used after a block operation to reassemble the chunks
        pads the last block with 0's until the byte width is reached'''
        pass