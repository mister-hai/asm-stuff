# -*- coding: utf-8 -*-
#!/usr/bin/python3.9
################################################################################
## Diffie-Hellman Key Generator for learning/hacking - Vintage 2021 Python 3.9##
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

#https://github.com/cardwizard/EllipticCurves/

from typing import Tuple
from src.EllipticalCurve import Point, EllipticalCurve

def generate_keys(p: int, a: int, b: int, G: Tuple, n: int)->Point:
    """
    Generates keys according to the Diffie Hellman Algorithm
    Args:
        p (int): Prime field size
        a (int): Coefficient of x^1 in the Elliptic Curve
        b (int): Coefficient of x^0 in the Elliptic Curve
        G (Point): Generator Point on the curve
        n (int): Private Key
    Returns:
        Generated key.
    """
    elliptic_curve = EllipticalCurve(a, b, p)
    generator = Point(elliptic_curve, G[0], G[1], "Generator")
    generated_point = generator * n
    return generated_point
