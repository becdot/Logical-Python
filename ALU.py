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
    m1, m2 = m1.pad_to_digits(m2, 16)
    carry = half_adder(m1[-1], m2[-1])[1]

    s = []
    for i in range(len(m1) - 1):
        carry = full_adder(m1[i], m2[i], carry)[1]
        s.append(full_adder(m1[i + 1], m2[i + 1], carry)[0])
    return Multi(s)