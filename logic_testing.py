import unittest

from logic import *


class test_logic(unittest.TestCase):

    def test_num_to_bin(self):
        self.assertEquals(num_to_bin(0), '0b0')
        self.assertEquals(num_to_bin(8), '0b1000')
        self.assertEquals(num_to_bin(-2), '-0b10')
        self.assertEquals(num_to_bin('0b1'), '0b1')
        self.assertEquals(num_to_bin('0b10'), '0b10')
        self.assertEquals(num_to_bin('-0b01'), '-0b01')

    def test_num_to_bits(self):
        self.assertEquals(num_to_right_bits(8, 8), '0b00001000')
        self.assertEquals(num_to_right_bits('0b1000', 8), '0b00001000')
        self.assertEquals(num_to_right_bits(0, 8), '0b00000000')
        self.assertEquals(num_to_right_bits('0b0', 4), '0b0000')
        self.assertEquals(num_to_right_bits(-1, 4), '-0b0001')
        self.assertEquals(num_to_right_bits('0b01', 4), '0b0001')
        self.assertEquals(num_to_right_bits(4, 3), '0b100')
        self.assertEquals(num_to_right_bits('0b100', 3), '0b100')


    def test_nand(self):
        "Defines a truth table for nand"
        self.assertTrue(nand(0, 0))
        self.assertTrue(nand(0, 1))
        self.assertTrue(nand(1, 0))
        self.assertFalse(nand(1, 1))

    def test_nand_bits(self):
        "nand should only accept 1-bit values for a and b"
        self.assertRaises(AssertionError, nand, 0, 2)
        self.assertRaises(AssertionError, nand, 1, 10)

    def test_mux(self):
        "Defines a truth table for mux"
        self.assertFalse(mux(0, 0, 0))
        self.assertFalse(mux(0, 0, 1))
        self.assertFalse(mux(0, 1, 0))
        self.assertTrue(mux(0, 1, 1))
        self.assertTrue(mux(1, 0, 0))
        self.assertFalse(mux(1, 0, 1))
        self.assertTrue(mux(1, 1, 0))
        self.assertTrue(mux(1, 1, 1))

    def test_mux_bits(self):
        "mux should only accept 1-bit values for a, b, and sel"
        self.assertRaises(AssertionError, mux, 0, 1, 2)
        self.assertRaises(AssertionError, mux, 0, 10, 1)
        self.assertRaises(AssertionError, mux, 2, 10, 3)

    def test_dmux(self):
        "Defines a truth table for dmux"
        a, b = dmux(0, 0)
        self.assertFalse(a)
        self.assertFalse(b)
        a, b = dmux(0, 1)
        self.assertFalse(a)
        self.assertFalse(b)
        a, b = dmux(1, 0)
        self.assertTrue(a)
        self.assertFalse(b)
        a, b = dmux(1, 1)
        self.assertFalse(a)
        self.assertTrue(b)

    def test_dmux_bits(self):
        "dmux should only accept 1-bit values for input and sel"
        self.assertRaises(AssertionError, dmux, 0, 10)
        self.assertRaises(AssertionError, dmux, 2, 1)
        self.assertRaises(AssertionError, dmux, 4, 5)

    def test_ormultiway(self):
        "Checks that the output is correct"
        self.assertTrue(ormultiway(8))
        self.assertTrue(ormultiway('0b1000'))
        self.assertTrue(ormultiway('-0b1'))
        self.assertFalse(ormultiway(0))
        self.assertFalse(ormultiway('0b0'))

    def test_and16(self):
        "Checks that and16(a, b) calculates 'and' bitwise and returns the correct 16-bit number"
        self.assertEquals(and16(8, 0), '0b0000000000000000')
        self.assertEquals(and16('0b0000000000001000', -1), '0b0000000000001000')
        self.assertEquals(and16(3, 1), '0b0000000000000001')
        self.assertEquals(and16('0b0011', '-0b1100'), '0b0000000000000000')

    def test_not16(self):
        "Checks that not16(a) calculates 'not' bitwise and returns the correct 16-bit number"
        self.assertEquals(not16(8), '-0b0000000000001001')
        self.assertEquals(not16(-1), '0b0000000000000000')
        self.assertEquals(not16('0b00000000'), '-0b0000000000000001')
        self.assertEquals(not16('0b0011'), '-0b0000000000000100')

    def test_0r16(self):
        "Checks that and16(a, b) calculates 'or' bitwise and returns the correct 16-bit number"
        self.assertEquals(or16(8, 0), '0b0000000000001000')
        self.assertEquals(or16('0b0000000000001000', -1), '-0b0000000000000001')
        self.assertEquals(or16(2, 1), '0b0000000000000011')
        self.assertEquals(or16('0b0011', '-0b0100'), '-0b0000000000000001')        



if __name__ == "__main__":
    unittest.main()