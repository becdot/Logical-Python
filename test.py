import unittest

from logic2 import *


zero = Bit(0)
one = Bit(1)

nand = Bit.nand

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


if __name__ == "__main__":
    unittest.main()