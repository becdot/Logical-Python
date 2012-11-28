from bit import Bit
from multi import Multi, pad_to_digits

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
    m1, m2 = pad_to_digits(16, m1, m2)
    sum, carry = half_adder(m1[15], m2[15])
    s = [sum]
    for i in range(14, -1, -1):
        sum = full_adder(m1[i], m2[i], carry)[0] # disjointed so that sum can use the old carry value instead of the new one
        carry = full_adder(m1[i], m2[i], carry)[1]
        s.append(sum)
    return Multi(reversed(s))

def inc(m):
    "Increases a Multi instance and returns a 16-bit value"
    m, one = pad_to_digits(16, m, Multi([Bit(1)]))
    return add_multi(m, one)