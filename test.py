from bit import Bit, nand, mux, dmux
from multi import Multi, pad_multi, pad_to_digits, multimux, or_multiway,\
        multimux_multiway, dmux_multiway
from ALU import half_adder, full_adder, add_multi, inc, from_num

import unittest

zero = Bit(0)
one = Bit(1)

m_fifteen = Multi([one, one, one, one])
m_fourteen = Multi([one, one, one, zero])
m_eight = Multi([one, zero, zero, zero])
m_three = Multi([one, one])
m_one = Multi([zero, zero, one])
m_zero = Multi([zero])

neg_one = Multi(Bit(digit) for digit in '1111111111111111')
neg_two = Multi(Bit(digit) for digit in '1111111111111110')
neg_three = Multi(Bit(digit) for digit in '1111111111111101')
neg_four = Multi(Bit(digit) for digit in '1111111111111100')
neg_eight = Multi(Bit(digit) for digit in '1111111111111000')
neg_fourteen = Multi(Bit(digit) for digit in '1111111111100100')
neg_fifteen = pad_to_digits(16, from_num(-15))[0]

zero16 = Multi([zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero])
one16 = Multi([zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, one])
three16 = Multi([zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, one, one])
four16 = pad_to_digits(16, Multi([one, zero, zero]))[0]
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
        "Checks the comparison operators (>, <, etc) on Multi instances"

        self.assertTrue(m_one > m_zero)
        self.assertTrue(m_zero > neg_four)
        self.assertTrue(m_eight >= one16)
        self.assertTrue(m_fifteen != m_fourteen)
        self.assertTrue(m_eight != neg_eight)
        self.assertTrue(m_three == three16)
        self.assertTrue(m_three == Multi([one, one]))
        self.assertTrue(zero16 < m_one)
        self.assertTrue(neg_two < neg_one)        
        self.assertTrue(m_fourteen <= m_16384)
        self.assertTrue(neg_four <= neg_one)        


    def test_Multi_to_decimel(self):
        "Binary -> decimel"
        self.assertEquals(Multi.to_decimel(m_fifteen), 15)
        self.assertEquals(Multi.to_decimel(m_eight), 8)
        self.assertEquals(Multi.to_decimel(m_one), 1)
        self.assertEquals(Multi.to_decimel(m_zero), 0)
        self.assertEquals(Multi.to_decimel(neg_one), -1)
        self.assertEquals(Multi.to_decimel(neg_two), -2)
        self.assertEquals(Multi.to_decimel(neg_three), -3)
        self.assertEquals(Multi.to_decimel(neg_four), -4)


    def test_Multi_pad(self):
        "Checks that Multi instances of uneven length are padded appropriately, and that instances of equal length are returned unchanged"

        self.assertEquals(tuple([str(m) for m in pad_multi(m_one, m_zero)]), (str(m_one), str(Multi([zero, zero, zero]))))
        self.assertEquals(tuple([str(m) for m in pad_multi(m_zero, m_one)]), (str(Multi([zero, zero, zero])), str(m_one)))
        self.assertEquals(tuple([str(m) for m in pad_multi(m_three, m_zero)]), (str(m_three), str(Multi([zero, zero]))))
        self.assertEquals(tuple([str(m) for m in pad_multi(m_zero, m_one)]), (str(Multi([zero, zero, zero])), str(m_one)))
        self.assertEquals(tuple([str(m) for m in pad_multi(m_eight, m_one)]), (str(m_eight), str(Multi([zero, zero, zero, one]))))
        self.assertEquals(tuple([str(m) for m in pad_multi(m_fourteen, m_fifteen)]), (str(m_fourteen), str(m_fifteen)))

    def test_Multi_pad_to_digits_with_two_inputs(self):
        """Checks that Multi arrays are padded to the specified number of digits, instances of equal length are returned unchanged,
        and that a digit that is too low will return the original Multi instances"""

        three4 = Multi([zero, zero, one, one])
        zero3 = Multi([zero, zero, zero])
        zero4 = Multi([zero, zero, zero, zero])
        one4 = Multi([zero, zero, zero, one])

        self.assertEquals(tuple([str(m) for m in pad_to_digits(4, m_eight, m_one)]), (str(m_eight), str(one4)))
        self.assertEquals(tuple([str(m) for m in pad_to_digits(4, m_one, m_eight)]), (str(one4), str(m_eight)))
        self.assertEquals(tuple([str(m) for m in pad_to_digits(3, m_zero, m_one)]), (str(zero3), str(m_one)))
        self.assertEquals(tuple([str(m) for m in pad_to_digits(4, m_three, m_zero)]), (str(three4), str(zero4)))
        self.assertEquals(tuple([str(m) for m in pad_to_digits(1, m_one, m_zero)]), (str(m_one), str(m_zero)))
        self.assertEquals(tuple([str(m) for m in pad_to_digits(4, m_three, m_one)]), (str(three4), str(one4)))

    def test_Multi_pad_to_digits_with_variable_inputs(self):
        """Checks that Multi arrays are padded to the specified number of digits, instances of equal length are returned unchanged,
        and that a digit that is too low will return the original Multi instances"""

        three4 = Multi([zero, zero, one, one])
        zero3 = Multi([zero, zero, zero])
        zero4 = Multi([zero, zero, zero, zero])
        one4 = Multi([zero, zero, zero, one])

        self.assertEquals(tuple([str(m) for m in pad_to_digits(3, m_zero)]), (str(zero3),))
        self.assertEquals(tuple([str(m) for m in pad_to_digits(4, m_three)]), (str(three4),))
        self.assertEquals(tuple([str(m) for m in pad_to_digits(1, m_one)]), (str(m_one),))
        self.assertEquals(tuple([str(m) for m in pad_to_digits(4, m_three)]), (str(three4),))
        self.assertEquals(tuple([str(m) for m in pad_to_digits(4, m_zero, m_one, m_eight)]), (str(zero4), str(one4), str(m_eight)))
        self.assertEquals(tuple([str(m) for m in pad_to_digits(4, m_eight, m_one, m_eight)]), (str(m_eight), str(one4), str(m_eight)))
        self.assertEquals(tuple([str(m) for m in pad_to_digits(4, m_fourteen, m_fifteen)]), (str(m_fourteen), str(m_fifteen)))

    def test_Multi_and(self):
        "Checks that the multibit & returns the correct values and pads Multi arrays of different sizes appropriately"
        "Tested with negative numbers"

        zero4 = Multi([zero, zero, zero, zero])
        two4 = Multi([zero, zero, one, zero])
        
        self.assertEquals(str(m_eight & m_zero), str(zero4))
        self.assertEquals(str(m_eight & m_one), str(zero4))
        self.assertEquals(str(m_eight & m_fifteen), str(m_eight))
        self.assertEquals(str(m_three & m_fourteen), str(two4))
        self.assertEquals(str(m_one & m_three), str(m_one))
        self.assertEquals(str(eight16 & neg_eight), str(eight16))
        self.assertEquals(str(eight16 & neg_four), str(eight16))
        self.assertEquals(str(zero16 & neg_one), str(zero16))
        self.assertEquals(str(neg_three & m_fourteen), str(pad_to_digits(16, from_num(12))[0]))
        self.assertEquals(str(neg_one & neg_three), str(neg_three))

    def test_Multi_not(self):
        "Checks that the multibit ~ flips all the signs of a Multi array"

        self.assertEquals(str(~m_fifteen), str(Multi([zero, zero, zero, zero])))
        self.assertEquals(str(~m_eight), str(Multi([zero, one, one, one])))
        self.assertEquals(str(~m_three), str(Multi([zero, zero])))
        self.assertEquals(str(~m_one), str(Multi([one, one, zero])))
        self.assertEquals(str(~m_zero), str(Multi([one])))

    def test_Multi_or(self):
        "Checks that multibit | returns the correct value and pads Multi arrays of different sizes appropriately"

        self.assertEquals(str(m_eight | m_zero), str(m_eight))
        self.assertEquals(str(m_eight | m_one), str(Multi([one, zero, zero, one])))
        self.assertEquals(str(m_eight | m_fifteen), str(m_fifteen))
        self.assertEquals(str(m_three | m_one), str(Multi([zero, one, one])))
        self.assertEquals(str(m_one | m_fourteen), str(m_fifteen))

    def test_multimux(self):

        zero3 = Multi([zero, zero, zero])

        self.assertEquals(str(multimux(m_eight, m_zero, zero)), str(m_eight))
        self.assertEquals(str(multimux(m_eight, m_fifteen, one)), str(m_fifteen))
        self.assertEquals(str(multimux(m_zero, m_one, zero)), str(zero3))
        self.assertEquals(str(multimux(m_zero, m_one, one)), str(m_one))

    def test_or_multiway(self):

        self.assertTrue(str(or_multiway(m_eight)))
        self.assertTrue(str(or_multiway(m_fifteen)))
        self.assertTrue(str(or_multiway(m_one)))
        self.assertTrue(str(or_multiway(m_zero)))

    def test_multimux_multiway(self):

        one4 = Multi([zero, zero, zero, one])
        zero4 = Multi([zero, zero, zero, zero])

        self.assertEquals(str(multimux_multiway(Multi([one]), m_fifteen, m_fourteen)), str(m_fourteen))
        self.assertEquals(str(multimux_multiway(Multi([one, one]), m_fifteen, m_fourteen, m_zero, m_one)), str(one4))
        self.assertEquals(str(multimux_multiway(Multi([zero, one]), m_three, m_zero, m_fifteen, m_fourteen)), str(zero4))
        self.assertEquals(str(multimux_multiway(Multi([one, zero, zero]), m_zero, m_three, m_fourteen, m_eight, m_one, m_zero, 
                                                m_fifteen, m_fourteen)), str(m_eight))
        self.assertEquals(str(multimux_multiway(Multi([zero, one, zero]), m_zero, m_three, m_fourteen, m_eight, m_one, m_zero, 
                                                      m_fifteen, m_fourteen)), str(m_fourteen))

    def test_dmux_multiway(self):
        m_one = Multi([one])
        m_zero = Multi([zero])

        a = dmux_multiway(m_one, m_zero)
        b = dmux_multiway(m_one, Multi([zero, one]))
        c = dmux_multiway(m_one, Multi([one, one]))
        d = dmux_multiway(m_one, Multi([zero, one, one]))
        
        self.assertEquals([str(bit) for bit in a], [str(Multi([one])), str(Multi([zero]))])
        self.assertEquals([str(bit) for bit in b], [str(Multi([zero])), str(Multi([one])), str(Multi([zero])), str(Multi([zero]))])
        self.assertEquals([str(bit) for bit in c], [str(Multi([zero])), str(Multi([zero])), str(Multi([zero])), str(Multi([one]))])
        self.assertEquals([str(bit) for bit in d], [str(Multi([zero])), str(Multi([zero])), str(Multi([zero])), str(Multi([one])), 
                                                    str(Multi([zero])), str(Multi([zero])), str(Multi([zero])), str(Multi([zero]))])

    def test_half_adder(self):
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

        self.assertEquals(str(add_multi(m_one, m_three)), str(four16))
        self.assertEquals(str(add_multi(m_one, m_16384)), str(m_16385))
        self.assertEquals(str(add_multi(m_zero, m_one)), str(one16))
        self.assertEquals(str(add_multi(m_fourteen, m_one)), str(fifteen16))
        self.assertEquals(str(add_multi(m_three, m_three)), 
            str(Multi([zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, one, one, zero])))

    def test_inc(self):

        self.assertEquals(str(inc(m_16384)), str(m_16385))
        self.assertEquals(str(inc(m_zero)), str(one16))
        self.assertEquals(str(inc(m_three)), str(four16))




if __name__ == "__main__":
    unittest.main()