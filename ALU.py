from bit import Bit
from multi import Multi, multimux, or_multiway, pad_to_digits

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
    if len(s) > 16:
        assert len(s[1:]) == 16
        return Multi(reversed(s[1:]))
    return Multi(reversed(s))

def inc(m):
    "Increases a Multi instance and returns a 16-bit value"
    m, one = pad_to_digits(16, m, Multi([Bit(1)]))
    return add_multi(m, one)

def alu(x, y, zx, nx, zy, ny, f, no):
    """Calculates a variety of functions on x and y, determined by the combination of control bits
        Outputs (out, zr, ng) where out is the 16-bit Multi result, and zr and ng are single Bits"""
    
    neg_one = Multi(Bit(digit) for digit in '1111111111111111')

    zero_x = x & Multi(~Bit(zx) for bit in range(16))
    zero_y = y & Multi(~Bit(zy) for bit in range(16))
    x2 = multimux(zero_x, ~zero_x, nx)
    y2 = multimux(zero_y, ~zero_y, ny)
    f_xy = multimux(x2 & y2, add_multi(x2, y2), f)
    out = multimux(f_xy, ~f_xy, no)
    zr = ~(or_multiway(out))
    ng = out[0]

    return (out, zr, ng)


