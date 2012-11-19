import unittest

from logic import *


class test_logic(unittest.TestCase):

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


if __name__ == "__main__":
    unittest.main()