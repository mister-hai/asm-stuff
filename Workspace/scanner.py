'''

here is an algorithm to find these gadgets; 

1- We search the binary for all “ret” (c3) byte. 

2- We go backwards to see if the previous byte contains a valid 
    instruction. We reverse to the maximum number of bytes that
    can make a valid instruction (20 bytes).

3- We then record all valid instruction sequences found in the 
    binary or linked libraries. 
'''