from bitc import Bit, nand, mux, dmux
from multic import Multi, multimux, or_multiway, multimux_multiway, dmux_multiway, pad_multi, pad_to_digits

import unittest

zero = Bit(0)
one = Bit(1)

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
      
    def test_Multi_to_decimel(self):
        "Binary -> decimel for both positive and negative numbers"
        self.assertEquals(Multi.to_decimel(m_fifteen), 15)
        self.assertEquals(Multi.to_decimel(m_eight), 8)
        self.assertEquals(Multi.to_decimel(m_one), 1)
        self.assertEquals(Multi.to_decimel(m_zero), 0)
        self.assertEquals(Multi.to_decimel(neg_one), -1)
        self.assertEquals(Multi.to_decimel(neg_two), -2)
        self.assertEquals(Multi.to_decimel(neg_three), -3)
        self.assertEquals(Multi.to_decimel(neg_four), -4)

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
        self.assertEquals(str(m_eight & m_one), str(zero4))
        self.assertEquals(str(m_eight & m_fifteen), str(m_eight))
        self.assertEquals(str(m_three & m_fourteen), str(two4))
        self.assertEquals(str(m_one & m_three), str(m_one))
        self.assertEquals(str(eight16 & neg_eight), str(eight16))
        self.assertEquals(str(eight16 & neg_four), str(eight16))
        self.assertEquals(str(zero16 & neg_one), str(zero16))
        self.assertEquals(str(neg_three & m_fourteen), str(Multi([Bit(digit) for digit in "0000000000001100"])))
        self.assertEquals(str(neg_one & neg_three), str(neg_three))

    def test_Multi_not(self):
        "Checks that the multibit ~ flips all the signs of a positive and negative Multi array"

        self.assertEquals(str(~m_fifteen), str(Multi([zero, zero, zero, zero])))
        self.assertEquals(str(~m_eight), str(Multi([zero, one, one, one])))
        self.assertEquals(str(~m_three), str(Multi([zero, zero])))
        self.assertEquals(str(~m_one), str(Multi([one, one, zero])))
        self.assertEquals(str(~m_zero), str(Multi([one])))

        self.assertEquals(str(~neg_one), str(zero16))
        self.assertEquals(str(~neg_four), str(three16))
        self.assertEquals(str(~neg_two), str(one16))

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


if __name__ == "__main__":
    unittest.main()