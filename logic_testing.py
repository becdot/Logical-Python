import unittest

from logic2 import *


class test_logic(unittest.TestCase):

    zero = Bit(0)
    one = Bit(1)

    # def test_num_to_bin(self):
    #     self.assertEquals(num_to_bin(0), '0b0')
    #     self.assertEquals(num_to_bin(8), '0b1000')
    #     self.assertEquals(num_to_bin(-2), '-0b10')
    #     self.assertEquals(num_to_bin('0b1'), '0b1')
    #     self.assertEquals(num_to_bin('0b10'), '0b10')
    #     self.assertEquals(num_to_bin('-0b01'), '-0b01')

    # def test_num_to_right_bits(self):
    #     self.assertEquals(num_to_right_bits(8, 8), '0b00001000')
    #     self.assertEquals(num_to_right_bits('0b1000', 8), '0b00001000')
    #     self.assertEquals(num_to_right_bits(0, 8), '0b00000000')
    #     self.assertEquals(num_to_right_bits('0b0', 4), '0b0000')
    #     self.assertEquals(num_to_right_bits(-1, 4), '-0b0001')
    #     self.assertEquals(num_to_right_bits('0b01', 4), '0b0001')
    #     self.assertEquals(num_to_right_bits(4, 3), '0b100')
    #     self.assertEquals(num_to_right_bits('0b100', 3), '0b100')


    def test_nand(self):
        "Defines a truth table for nand"
        print zero, one
        self.assertTrue(nand(zero, zero).value)
        self.assertTrue(nand(zero, one).value)
        self.assertTrue(nand(one, zero).value)
        self.assertFalse(nand(one, one).value)

    # def test_nand_bits(self):
    #     "nand should only accept 1-bit values for a and b"
    #     x = Logic()
    #     self.assertRaises(AssertionError, nand, 0, 2)
    #     self.assertRaises(AssertionError, nand, 1, 10)

    # def test___invert__(self):
    #     "Defines a truth table for invert(re-defined as not)"
    #     self.assertTrue((~zero).value)
    #     self.assertFalse((~one).value)

    # def test___and__(self):
    #     "Defines a truth table for and"
    #     self.assertFalse((zero & zero).value)
    #     self.assertFalse((zero & one).value)
    #     self.assertFalse((one & zero).value)
    #     self.assertTrue((one & one).value)

    # def test___or__(self):
    #     "Defines a truth table for or"
    #     self.assertFalse((zero | zero).value)
    #     self.assertTrue((zero | one).value)
    #     self.assertTrue((one | zero).value)
    #     self.assertTrue((one | one).value)

    # def test___xor__(self):
    #     "Defines a truth table for xor"
    #     self.assertFalse((zero ^ zero).value)
    #     self.assertTrue((zero ^ one).value)
    #     self.assertTrue((one ^ zero).value)
    #     self.assertFalse((one ^ one).value)

    # def test_mux(self):
    #     "Defines a truth table for mux"

    #     self.assertFalse(mux(zero, zero, zero).value)
    #     self.assertFalse(mux(zero, zero, one).value)
    #     self.assertFalse(mux(zero, one, zero).value)
    #     self.assertTrue(mux(zero, one, one).value)
    #     self.assertTrue(mux(one, zero, zero).value)
    #     self.assertFalse(mux(one, zero, one).value)
    #     self.assertTrue(mux(one, one, zero).value)
    #     self.assertTrue(mux(one, one, one).value)

    # # def test_mux_bits(self):
    # #     "mux should only accept 1-bit values for a, b, and sel"
    # #     x = Logic()
    # #     self.assertRaises(AssertionError, x.mux, 0, 1, 2)
    # #     self.assertRaises(AssertionError, x.mux, 0, 10, 1)
    # #     self.assertRaises(AssertionError, x.mux, 2, 10, 3)

    # def test_dmux(self):
    #     "Defines a truth table for dmux"
    #     a, b = dmux(zero, zero)
    #     self.assertFalse(a.value)
    #     self.assertFalse(b.value)
    #     a, b = dmux(zero, one)
    #     self.assertFalse(a.value)
    #     self.assertFalse(b.value)
    #     a, b = dmux(one, zero)
    #     self.assertTrue(a.value)
    #     self.assertFalse(b.value)
    #     a, b = dmux(one, one)
    #     self.assertFalse(a.value)
    #     self.assertTrue(b.value)

    # def test_dmux_bits(self):
    #     "dmux should only accept 1-bit values for input and sel"
    #     x = Logic()
    #     self.assertRaises(AssertionError, x.dmux, 0, 10)
    #     self.assertRaises(AssertionError, x.dmux, 2, 1)
    #     self.assertRaises(AssertionError, x.dmux, 4, 5)


    # def test_and16(self):
    #     "Checks that and16(a, b) calculates 'and' bitwise and returns the correct 16-bit number"
    #     self.assertEquals(and16(8, 0), '0b0000000000000000')
    #     self.assertEquals(and16('0b0000000000001000', -1), '0b0000000000001000')
    #     self.assertEquals(and16(3, 1), '0b0000000000000001')
    #     self.assertEquals(and16('0b0011', '-0b1100'), '0b0000000000000000')

    # def test_not16(self):
    #     "Checks that not16(a) calculates 'not' bitwise and returns the correct 16-bit number"
    #     self.assertEquals(not16(8), '-0b0000000000001001')
    #     self.assertEquals(not16(-1), '0b0000000000000000')
    #     self.assertEquals(not16('0b00000000'), '-0b0000000000000001')
    #     self.assertEquals(not16('0b0011'), '-0b0000000000000100')

    # def test_0r16(self):
    #     "Checks that and16(a, b) calculates 'or' bitwise and returns the correct 16-bit number"
    #     self.assertEquals(or16(8, 0), '0b0000000000001000')
    #     self.assertEquals(or16('0b0000000000001000', -1), '-0b0000000000000001')
    #     self.assertEquals(or16(2, 1), '0b0000000000000011')
    #     self.assertEquals(or16('0b0011', '-0b0100'), '-0b0000000000000001')  


    # def test_ormultiway(self):
    #     "Checks that the output is correct"
    #     self.assertTrue(ormultiway(8))
    #     self.assertTrue(ormultiway('0b1000'))
    #     self.assertTrue(ormultiway('-0b1'))
    #     self.assertFalse(ormultiway(0))
    #     self.assertFalse(ormultiway('0b0'))      



if __name__ == "__main__":
    unittest.main()