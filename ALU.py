from bit import Bit
from multi import Multi

import itertools

def half_adder(b1, b2):
    "Takes two Bit inputs and outputs two Bits (sum, carry) where sum = LSB of b1, b2 and carry = MSB of m1, m2"
    sum = (b1 ^ b2)
    carry = (b1 & b2)
    return (sum, carry)

def full_adder(b1, b2, b3):
    "Takes three bit inputs and outputs (sum, carry)"
    bits = [half_adder(pair[0], pair[1]) for pair in itertools.combinations([b1, b2, b3], 2)]
    carry, s = Bit(0), Bit(0)
    for t in bits:
        carry = (carry | t[1])
        s = (s | t[0])
    sum = ~(~carry ^ s)
    return (sum, carry)

def add_multi(m1, m2):
    "Adds two Multi instances by doing partial adds of the individual bits (indexed from the right), and returns a 16-bit Multi instance"
    m1, m2 = Multi.pad_to_digits(m1, 16, m2)
    first_sum = half_adder(m1[15], m2[15])[0]
    s = [first_sum]
    for i in range(15, -1, -1):
        carry = half_adder(m1[i], m2[i])[1]
        sum = full_adder(m1[i - 1], m2[i - 1], carry)[0]
        s.append(sum)
    s.reverse()
    return Multi(s[1:]) # cut out the overflow