from bit import Bit, nand, mux, dmux
from multi import Multi, multimux, or_multiway, multimux_multiway, dmux_multiway, pad_to_digits, pad_multi
from ALU import half_adder, full_adder, add_multi, inc, alu

import unittest

zero = Bit(0)
one = Bit(1)

def from_num(num):
    "Helper function to create a 16-bit Multi instance using a number"
    bnum = bin(num)
    b = bnum.index('b') + 1
    pos = Multi(Bit(digit) for digit in bnum[b:])
    pos.insert(0, Bit(0))
    pos = pad_to_digits(16, pos)[0]
    if bnum[0] == '-':
        neg = inc(~pos)
        if len(neg) > 16:
            return neg[1:]
        return Multi(neg)
    return Multi(pos)

m_fifteen = Multi([one, one, one, one])
m_fourteen = Multi([one, one, one, zero])
m_eight = Multi([one, zero, zero, zero])
m_three = Multi([one, one])
m_two = Multi([zero, one, zero])
m_one = Multi([zero, zero, one])
m_zero = Multi([zero])

neg_one = Multi(Bit(digit) for digit in '1111111111111111')
neg_two = Multi(Bit(digit) for digit in '1111111111111110')
neg_three = Multi(Bit(digit) for digit in '1111111111111101')
neg_four = Multi(Bit(digit) for digit in '1111111111111100')
neg_eight = Multi(Bit(digit) for digit in '1111111111111000')
neg_fourteen = Multi(Bit(digit) for digit in '1111111111100100')
neg_fifteen = Multi(Bit(digit) for digit in '1111111111110001')

zero16 = Multi([zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero])
one16 = Multi([zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, one])
two16 = Multi([zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, one, zero])
three16 = Multi([zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, one, one])
four16 = Multi([zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, one, zero, zero])
eight16 = Multi([zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, one, zero, zero, zero])
fourteen16 = Multi([zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, one, one, one, zero])
fifteen16 = Multi([zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, one, one, one, one])
m_16384  = Multi([zero, one, zero, one, zero, zero, one, zero, zero, one, zero, one, zero, one, zero, zero])
m_16385  = Multi([zero, one, zero, one, zero, zero, one, zero, zero, one, zero, one, zero, one, zero, one])




class TestLogic(unittest.TestCase):

    def test_nand(self):
        "Defines a truth table for nand"
        self.assertTrue(nand(zero, zero))
        self.assertTrue(nand(zero, one))
        self.assertTrue(nand(one, zero))
        self.assertFalse(nand(one, one))

    def test___invert__(self):
        "Defines a truth table for invert(re-defined as not)"
        self.assertTrue((~zero))
        self.assertFalse((~one))

    def test___and__(self):
        "Defines a truth table for and"
        self.assertFalse((zero & zero))
        self.assertFalse((zero & one))
        self.assertFalse((one & zero))
        self.assertTrue((one & one))

    def test___or__(self):
        "Defines a truth table for or"
        self.assertFalse((zero | zero))
        self.assertTrue((zero | one))
        self.assertTrue((one | zero))
        self.assertTrue((one | one))

    def test___xor__(self):
        "Defines a truth table for xor"
        self.assertFalse((zero ^ zero))
        self.assertTrue((zero ^ one))
        self.assertTrue((one ^ zero))
        self.assertFalse((one ^ one))

    def test_mux(self):
        "Defines a truth table for mux"
        self.assertFalse(mux(zero, zero, zero))
        self.assertFalse(mux(zero, zero, one))
        self.assertFalse(mux(zero, one, zero))
        self.assertTrue(mux(zero, one, one))
        self.assertTrue(mux(one, zero, zero))
        self.assertFalse(mux(one, zero, one))
        self.assertTrue(mux(one, one, zero))
        self.assertTrue(mux(one, one, one))

    def test_dmux(self):
        "Defines a truth table for dmux"
        a, b = dmux(zero, zero)
        self.assertFalse(a)
        self.assertFalse(b)
        a, b = dmux(zero, one)
        self.assertFalse(a)
        self.assertFalse(b)
        a, b = dmux(one, zero)
        self.assertTrue(a)
        self.assertFalse(b)
        a, b = dmux(one, one)
        self.assertFalse(a)
        self.assertTrue(b)

    def test_Multi_comparison(self):
        "Checks the comparison operators (>, <, etc) on both positive and negative Multi instances"

        self.assertTrue(m_fifteen != m_fourteen)
        self.assertTrue(m_eight != neg_eight)
        self.assertTrue(m_three == three16)
        self.assertTrue(m_three == Multi([one, one]))
      
    def test_Multi_to_decimal(self):
        "Binary -> decimal for both positive and negative numbers"
        self.assertEquals(Multi.to_decimal(m_fifteen), 15)
        self.assertEquals(Multi.to_decimal(m_eight), 8)
        self.assertEquals(Multi.to_decimal(m_one), 1)
        self.assertEquals(Multi.to_decimal(m_zero), 0)
        self.assertEquals(Multi.to_decimal(neg_one), -1)
        self.assertEquals(Multi.to_decimal(neg_two), -2)
        self.assertEquals(Multi.to_decimal(neg_three), -3)
        self.assertEquals(Multi.to_decimal(neg_four), -4)

    def test_Multi_pad(self):
        """Checks that positive and negative Multi instances of uneven length are padded appropriately.
            Also checks that instances of equal length are returned unchanged"""

        neg_one5 = Multi([one, one, one, one, one])
        neg_two6 = Multi([one, one, one, one, one, zero])
        neg_three8 = Multi([one, one, one, one, one, one, zero, one])


        self.assertEquals(tuple([str(m) for m in pad_multi(m_one, m_zero)]), (str(m_one), str(Multi([zero, zero, zero]))))
        self.assertEquals(tuple([str(m) for m in pad_multi(m_zero, m_one)]), (str(Multi([zero, zero, zero])), str(m_one)))
        self.assertEquals(tuple([str(m) for m in pad_multi(m_three, m_zero)]), (str(m_three), str(Multi([zero, zero]))))
        self.assertEquals(tuple([str(m) for m in pad_multi(m_zero, m_one)]), (str(Multi([zero, zero, zero])), str(m_one)))
        self.assertEquals(tuple([str(m) for m in pad_multi(m_eight, m_one)]), (str(m_eight), str(Multi([zero, zero, zero, one]))))
        self.assertEquals(tuple([str(m) for m in pad_multi(m_fourteen, m_fifteen)]), (str(m_fourteen), str(m_fifteen)))

        self.assertEquals(tuple([str(m) for m in pad_multi(neg_one5, m_zero)]), (str(neg_one5), str(Multi([zero, zero, zero, zero, zero]))))
        self.assertEquals(tuple([str(m) for m in pad_multi(m_zero, neg_one5)]), (str(Multi([zero, zero, zero, zero, zero])), str(neg_one5)))
        self.assertEquals(tuple([str(m) for m in pad_multi(neg_three8, neg_one5)]), (str(neg_three8), 
                                                                                    str(Multi([one, one, one, one, one, one, one, one]))))
        self.assertEquals(tuple([str(m) for m in pad_multi(neg_two6, neg_three8)]), (str(Multi([one, one, one, one, one, one, one, zero])), 
                                                                                    str(Multi([one, one, one, one, one, one, zero, one]))))
        self.assertEquals(tuple([str(m) for m in pad_multi(neg_two6, m_fourteen)]), (str(neg_two6), 
                                                                                    str(Multi([zero, zero, one, one, one, zero]))))

    def test_Multi_pad_to_digits_with_variable_inputs(self):
        """Checks that Multi arrays are padded to the specified number of digits, instances of equal length are returned unchanged,
        and that a digit that is too low will return the original Multi instances"""

        three4 = Multi([zero, zero, one, one])
        zero3 = Multi([zero, zero, zero])
        zero4 = Multi([zero, zero, zero, zero])
        one4 = Multi([zero, zero, zero, one])
        eight6 = Multi([zero, zero, one, zero, zero, zero])
        one6 = Multi([zero, zero, zero, zero, zero, one])
        zero6 = Multi([zero, zero, zero, zero, zero, zero])
        zero8 = Multi([zero, zero, zero, zero, zero, zero, zero, zero])
        three6 = Multi([zero, zero, zero, zero, one, one])
        neg_one5 = Multi([one, one, one, one, one])
        neg_one6 = Multi([one, one, one, one, one, one])
        neg_one8 = Multi([one, one, one, one, one, one, one, one])
        neg_two6 = Multi([one, one, one, one, one, zero])
        neg_two8 = Multi([one, one, one, one, one, one, one, zero])
        neg_three8 = Multi([one, one, one, one, one, one, zero, one])

        # Checks output with two positive inputs
        self.assertEquals([str(m) for m in pad_to_digits(4, m_eight, m_one)], [str(m_eight), str(one4)])
        self.assertEquals([str(m) for m in pad_to_digits(4, m_one, m_eight)], [str(one4), str(m_eight)])
        self.assertEquals([str(m) for m in pad_to_digits(6, m_eight, m_one)], [str(eight6), str(one6)])
        self.assertEquals([str(m) for m in pad_to_digits(6, m_one, m_eight)], [str(one6), str(eight6)])
        self.assertEquals([str(m) for m in pad_to_digits(3, m_zero, m_one)], [str(zero3), str(m_one)])
        self.assertEquals([str(m) for m in pad_to_digits(4, m_three, m_zero)], [str(three4), str(zero4)])
        self.assertEquals([str(m) for m in pad_to_digits(4, m_three, m_one)], [str(three4), str(one4)])
        # Checks that an exception is raised if digits is lower than the length of one or more Multi instances
        self.assertRaises(ValueError, pad_to_digits, *(1, m_one, m_zero))
        self.assertRaises(ValueError, pad_to_digits, *(1, neg_three))
        self.assertRaises(ValueError, pad_to_digits, *(6, m_eight, zero4, neg_two8))
        self.assertRaises(ValueError, pad_to_digits, *(6, neg_two8, m_eight, zero4))
        self.assertRaises(ValueError, pad_to_digits, *(6, neg_two8, neg_three8, zero4))
        # Checks output with variable positive inputs
        self.assertEquals([str(m) for m in pad_to_digits(6, m_zero)], [str(zero6)])
        self.assertEquals([str(m) for m in pad_to_digits(4, m_three)], [str(three4)])
        self.assertEquals([str(m) for m in pad_to_digits(4, m_zero, m_one, m_eight)], [str(zero4), str(one4), str(m_eight)])
        self.assertEquals([str(m) for m in pad_to_digits(4, zero3, m_three, m_eight)], [str(zero4), str(three4), str(m_eight)])
        self.assertEquals([str(m) for m in pad_to_digits(6, m_eight, m_three, m_eight)], [str(eight6), str(three6), str(eight6)])
        # Checks output with negative inputs
        self.assertEquals([str(m) for m in pad_to_digits(6, neg_one5)], [str(neg_one6)])
        self.assertEquals([str(m) for m in pad_to_digits(8, neg_two6)], [str(neg_two8)])
        self.assertEquals([str(m) for m in pad_to_digits(8, m_zero, neg_two8, neg_one5)], [str(zero8), str(neg_two8), str(neg_one8)])
        self.assertEquals([str(m) for m in pad_to_digits(6, zero3, neg_one6, m_eight)], [str(zero6), str(neg_one6), str(eight6)])
        
    def test_Multi_and(self):
        "Checks that the multibit & returns the correct values of positive and negative Multi arrays of different sizes"

        zero4 = Multi([zero, zero, zero, zero])
        two4 = Multi([zero, zero, one, zero])
        
        self.assertEquals(str(m_eight & m_zero), str(zero4))
        self.assertEquals(str(m_eight & m_zero), str(zero4))
        self.assertEquals(str(m_eight & m_one), str(zero4))
        self.assertEquals(str(m_eight & m_fifteen), str(m_eight))
        self.assertEquals(str(m_three & m_fourteen), str(two4))
        self.assertEquals(str(m_one & m_three), str(m_one))
        self.assertEquals(str(eight16 & neg_eight), str(eight16))
        self.assertEquals(str(eight16 & neg_four), str(eight16))
        self.assertEquals(str(zero16 & neg_one), str(zero16))
        self.assertEquals(str(neg_three & m_fourteen), str(from_num(12)))
        self.assertEquals(str(neg_one & neg_three), str(neg_three))

    def test_Multi_not(self):
        "Checks that the multibit ~ flips all the signs of a positive and negative Multi array"

        self.assertEquals(str(~m_fifteen), str(Multi([zero, zero, zero, zero])))
        self.assertEquals(str(~m_eight), str(Multi([zero, one, one, one])))
        self.assertEquals(str(~m_three), str(Multi([zero, zero])))
        self.assertEquals(str(~m_one), str(Multi([one, one, zero])))
        self.assertEquals(str(~m_zero), str(Multi([one])))

        self.assertEquals(str(~neg_one), str(from_num(0)))
        self.assertEquals(str(~neg_four), str(from_num(3)))
        self.assertEquals(str(~neg_two), str(from_num(1)))

    def test_Multi_or(self):
        "Checks that multibit | returns the correct value of positive and negative Multi arrays"

        self.assertEquals(str(m_eight | m_zero), str(m_eight))
        self.assertEquals(str(m_eight | m_one), str(Multi([one, zero, zero, one])))
        self.assertEquals(str(m_eight | m_fifteen), str(m_fifteen))
        self.assertEquals(str(m_three | m_one), str(Multi([zero, one, one])))
        self.assertEquals(str(m_one | m_fourteen), str(m_fifteen))

        self.assertEquals(str(neg_eight | m_zero), str(neg_eight))
        self.assertEquals(str(m_eight | neg_one), str(neg_one))
        self.assertEquals(str(neg_two | neg_three), str(neg_one))
        self.assertEquals(str(neg_eight | neg_three), str(neg_three))
        self.assertEquals(str(neg_two | m_two), str(neg_two))

    def test_multimux(self):
        "Checks that multimux(a, b) -> a if sel = 0, and b if sel = 1"

        zero3 = Multi([zero, zero, zero])

        self.assertEquals(str(multimux(m_eight, m_zero, zero)), str(m_eight))
        self.assertEquals(str(multimux(m_eight, m_fifteen, one)), str(m_fifteen))
        self.assertEquals(str(multimux(m_zero, m_one, zero)), str(zero3))
        self.assertEquals(str(multimux(m_zero, m_one, one)), str(m_one))
        self.assertEquals(str(multimux(neg_one, m_zero, zero)), str(neg_one))
        self.assertEquals(str(multimux(m_eight, neg_two, one)), str(neg_two))
        self.assertEquals(str(multimux(m_zero, neg_one, zero)), str(zero16))
        self.assertEquals(str(multimux(neg_one, m_one, one)), str(one16))

    def test_or_multiway(self):
        "Checks that or_multiway returns 1 if any bits in the number = 1, and 0 only if all bits = 0"

        self.assertTrue(or_multiway(m_eight))
        self.assertTrue(or_multiway(neg_three))
        self.assertTrue(or_multiway(m_one))
        self.assertTrue(or_multiway(neg_one))
        self.assertFalse(or_multiway(m_zero))

    def test_multimux_multiway(self):
        """Checks that multimux_multiway returns the correct value given an input of 2, 4, or 8 Multi instances 
            and a corresponding selector of 1, 2, or 3 digits"""

        one4 = Multi([zero, zero, zero, one])
        zero4 = Multi([zero, zero, zero, zero])

        self.assertEquals(str(multimux_multiway(Multi([one]), m_fifteen, m_fourteen)), str(m_fourteen))
        self.assertEquals(str(multimux_multiway(Multi([zero]), neg_one, m_fourteen)), str(neg_one))
        self.assertEquals(str(multimux_multiway(Multi([one, one]), m_fifteen, neg_two, m_zero, m_one)), str(one16))
        self.assertEquals(str(multimux_multiway(Multi([zero, one]), m_zero, neg_one, m_two, neg_three)), str(neg_one))
        self.assertEquals(str(multimux_multiway(Multi([one, zero, zero]), m_zero, neg_one, m_fourteen, neg_eight, m_one, m_zero, 
                                                m_fifteen, neg_three)), str(one16))
        self.assertEquals(str(multimux_multiway(Multi([zero, one, zero]), m_zero, m_three, m_fourteen, m_eight, m_one, m_zero, 
                                                      m_fifteen, m_fourteen)), str(m_fourteen))

    def test_dmux_multiway(self):
        """Checks that dmux_multiway returns the number of outputs indicated by the selector (1 -> 2, 2 -> 4, 3 -> 8), and sets the  
        Multi instance indicated by the selector equal to the input, and all other outputs zero"""
        m_one = Multi([one])
        m_zero = Multi([zero])

        a = dmux_multiway(m_one, m_zero)
        b = dmux_multiway(m_one, Multi([zero, one]))
        c = dmux_multiway(m_one, Multi([one, one]))
        d = dmux_multiway(m_one, Multi([zero, one, one]))
        e = dmux_multiway(m_zero, Multi([one, one]))
        
        self.assertEquals([str(bit) for bit in a], [str(Multi([one])), str(Multi([zero]))])
        self.assertEquals([str(bit) for bit in b], [str(Multi([zero])), str(Multi([one])), str(Multi([zero])), str(Multi([zero]))])
        self.assertEquals([str(bit) for bit in c], [str(Multi([zero])), str(Multi([zero])), str(Multi([zero])), str(Multi([one]))])
        self.assertEquals([str(bit) for bit in d], [str(Multi([zero])), str(Multi([zero])), str(Multi([zero])), str(Multi([one])), 
                                                    str(Multi([zero])), str(Multi([zero])), str(Multi([zero])), str(Multi([zero]))])
        self.assertEquals([str(bit) for bit in e], [str(Multi([zero])), str(Multi([zero])), str(Multi([zero])), str(Multi([zero]))])

    def test_half_adder(self):
        "Checks that the addition of 2 Bits will return the appropriate (sum, carry) bits"
        s, c = half_adder(zero, zero)
        self.assertFalse(s)
        self.assertFalse(c)
        s, c = half_adder(zero, one)
        self.assertTrue(s)
        self.assertFalse(c)        
        s, c = half_adder(one, zero)
        self.assertTrue(s)
        self.assertFalse(c)        
        s, c = half_adder(one, one)
        self.assertFalse(s)
        self.assertTrue(c)

    def test_full_adder(self):
        "Checks that the addition of 3 Bits will return the appropriate (sum, carry) bits"
        s, c = full_adder(zero, zero, zero)
        self.assertFalse(s)
        self.assertFalse(c)
        s, c = full_adder(zero, zero, one)
        self.assertTrue(s)
        self.assertFalse(c)
        s, c = full_adder(zero, one, zero)
        self.assertTrue(s)
        self.assertFalse(c)
        s, c = full_adder(zero, one, one)
        self.assertFalse(s)
        self.assertTrue(c)
        s, c = full_adder(one, zero, zero)
        self.assertTrue(s)
        self.assertFalse(c)
        s, c = full_adder(one, zero, one)
        self.assertFalse(s)
        self.assertTrue(c)
        s, c = full_adder(one, one, zero)
        self.assertFalse(s)
        self.assertTrue(c)
        s, c = full_adder(one, one, one)
        self.assertTrue(s)
        self.assertTrue(c)

    def test_add_multi(self):
        """Tests that the addition of two Multi instances return the correct 16-bit instance
            If the output has an overflow (beyond 16 bits) it is ignored"""
        six16 = Multi([zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, one, one, zero])

        self.assertEquals(str(add_multi(m_one, m_three)), str(four16))
        self.assertEquals(str(add_multi(m_one, m_16384)), str(m_16385))
        self.assertEquals(str(add_multi(m_zero, m_one)), str(one16))
        self.assertEquals(str(add_multi(m_fourteen, m_one)), str(fifteen16))
        self.assertEquals(str(add_multi(m_three, m_three)), str(six16))
        self.assertEquals(str(add_multi(neg_eight, Multi([zero, zero, one, zero, one]))), str(neg_three))
        self.assertEquals(str(add_multi(four16, neg_two)), str(two16))
        self.assertEquals(str(add_multi(m_zero, neg_one)), str(neg_one))        
        self.assertEquals(str(add_multi(neg_two, two16)), str(zero16))
        
    def test_inc(self):
        "Checks that inc(Multi) increases the value by 1"
        self.assertEquals(str(inc(m_16384)), str(m_16385))
        self.assertEquals(str(inc(m_zero)), str(one16))
        self.assertEquals(str(inc(m_three)), str(four16))
        self.assertEquals(str(inc(neg_one)), str(zero16))
        self.assertEquals(str(inc(neg_three)), str(neg_two))

    def test_alu(self):
        x = zero16
        y = neg_one
        
        self.assertEquals([str(bit) for bit in alu(x, y, one, zero, one, zero, one, zero)], [str(zero16), str(one), str(zero)]) # 0
        self.assertEquals([str(bit) for bit in alu(x, y, one, one, one, one, one, one)], [str(one16), str(zero), str(zero)]) # 1
        self.assertEquals([str(bit) for bit in alu(x, y, one, one, one, zero, one, zero)], [str(neg_one), str(zero), str(one)]) # -1
        self.assertEquals([str(bit) for bit in alu(x, y, zero, zero, one, one, zero, zero)], [str(zero16), str(one), str(zero)]) # x
        self.assertEquals([str(bit) for bit in alu(x, y, one, one, zero, zero, zero, zero)], [str(neg_one), str(zero), str(one)]) # y
        self.assertEquals([str(bit) for bit in alu(x, y, zero, zero, one, one, zero, one)], [str(neg_one), str(zero), str(one)]) # ~x
        self.assertEquals([str(bit) for bit in alu(x, y, one, one, zero, zero, zero, one)], [str(zero16), str(one), str(zero)]) # ~y
        self.assertEquals([str(bit) for bit in alu(x, y, zero, zero, one, one, one, one)], [str(zero16), str(one), str(zero)]) # -x
        self.assertEquals([str(bit) for bit in alu(x, y, one, one, zero, zero, one, one)], [str(one16), str(zero), str(zero)]) # -y
        self.assertEquals([str(bit) for bit in alu(x, y, zero, one, one, one, one, one)], [str(one16), str(zero), str(zero)]) # x + 1
        self.assertEquals([str(bit) for bit in alu(x, y, one, one, zero, one, one, one)], [str(zero16), str(one), str(zero)]) # y + 1
        self.assertEquals([str(bit) for bit in alu(x, y, zero, zero, one, one, one, zero)], [str(neg_one), str(zero), str(one)]) # x - 1
        self.assertEquals([str(bit) for bit in alu(x, y, one, one, zero, zero, one, zero)], [str(neg_two), str(zero), str(one)]) # y - 1
        self.assertEquals([str(bit) for bit in alu(x, y, zero, zero, zero, zero, one, zero)], [str(neg_one), str(zero), str(one)]) # x + y
        self.assertEquals([str(bit) for bit in alu(x, y, zero, one, zero, zero, one, one)], [str(one16), str(zero), str(zero)]) # x - y
        self.assertEquals([str(bit) for bit in alu(x, y, zero, zero, zero, one, one, one)], [str(neg_one), str(zero), str(one)]) # y - x
        self.assertEquals([str(bit) for bit in alu(x, y, zero, zero, zero, zero, zero, zero)], [str(zero16), str(one), str(zero)]) # x & y
        self.assertEquals([str(bit) for bit in alu(x, y, zero, one, zero, one, zero, one)], [str(neg_one), str(zero), str(one)]) # x | y

        x = Multi(from_num(17))
        y = three16

        self.assertEquals([str(bit) for bit in alu(x, y, one, zero, one, zero, one, zero)], [str(zero16), str(one), str(zero)]) # 0
        self.assertEquals([str(bit) for bit in alu(x, y, one, one, one, one, one, one)], [str(one16), str(zero), str(zero)]) # 1
        self.assertEquals([str(bit) for bit in alu(x, y, one, one, one, zero, one, zero)], [str(neg_one), str(zero), str(one)]) # -1
        self.assertEquals([str(bit) for bit in alu(x, y, zero, zero, one, one, zero, zero)], [str(x), str(zero), str(zero)]) # x
        self.assertEquals([str(bit) for bit in alu(x, y, one, one, zero, zero, zero, zero)], [str(y), str(zero), str(zero)]) # y
        self.assertEquals([str(bit) for bit in alu(x, y, zero, zero, one, one, zero, one)], [str(~x), str(zero), str(one)]) # ~x
        self.assertEquals([str(bit) for bit in alu(x, y, one, one, zero, zero, zero, one)], [str(~y), str(zero), str(one)]) # ~y
        self.assertEquals([str(bit) for bit in alu(x, y, zero, zero, one, one, one, one)], [str(from_num(-17)), 
                                                                                                str(zero), str(one)]) # -x
        self.assertEquals([str(bit) for bit in alu(x, y, one, one, zero, zero, one, one)], [str(neg_three), str(zero), str(one)]) # -y
        self.assertEquals([str(bit) for bit in alu(x, y, zero, one, one, one, one, one)], [str(inc(x)), str(zero), str(zero)]) # x + 1
        self.assertEquals([str(bit) for bit in alu(x, y, one, one, zero, one, one, one)], [str(inc(y)), str(zero), str(zero)]) # y + 1
        self.assertEquals([str(bit) for bit in alu(x, y, zero, zero, one, one, one, zero)], [str(from_num(16)), 
                                                                                                str(zero), str(zero)]) # x - 1
        self.assertEquals([str(bit) for bit in alu(x, y, one, one, zero, zero, one, zero)], [str(two16), str(zero), str(zero)]) # y - 1
        self.assertEquals([str(bit) for bit in alu(x, y, zero, zero, zero, zero, one, zero)], [str(from_num(20)),
                                                                                                str(zero), str(zero)]) # x + y
        self.assertEquals([str(bit) for bit in alu(x, y, zero, one, zero, zero, one, one)], [str(from_num(14)), 
                                                                                                str(zero), str(zero)]) # x - y
        self.assertEquals([str(bit) for bit in alu(x, y, zero, zero, zero, one, one, one)], [str(from_num(-14)), 
                                                                                            str(zero), str(one)]) # y - x
        self.assertEquals([str(bit) for bit in alu(x, y, zero, zero, zero, zero, zero, zero)], [str(one16), str(zero), str(zero)]) # x & y
        self.assertEquals([str(bit) for bit in alu(x, y, zero, one, zero, one, zero, one)], [str(from_num(19)),
                                                                                            str(zero), str(zero)]) # x | y


if __name__ == "__main__":
    unittest.main(module='test_combinational')
