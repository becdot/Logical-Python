from bit import Bit
from multi import Multi

import itertools

def half_adder(b1, b2):
    "Takes two Bit inputs and outputs two Bits (sum, carry) where sum = LSB of b1, b2 and carry = MSB of m1, m2"
    return ((b1 ^ b2), (b1 & b2))

def full_adder(b1, b2, b3):
    bits = [half_adder(pair[0], pair[1]) for pair in itertools.combinations([b1, b2, b3], 2)]
    carry, s = Bit(0), Bit(0)
    for t in bits:
        carry = (carry | t[1])
        s = (s | t[0])
    sum = ~(~carry ^ s)
    return (sum, carry)

