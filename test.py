import unittest

from logic2 import *


zero = Bit(0)
one = Bit(1)

nand = Bit.nand

class TestLogic(unittest.TestCase):

    def test_nand(self):
        "Defines a truth table for nand"
        self.assertTrue(nand(zero, zero).value)
        self.assertTrue(nand(zero, one).value)
        self.assertTrue(nand(one, zero).value)
        self.assertFalse(nand(one, one).value)

    def test___invert__(self):
        "Defines a truth table for invert(re-defined as not)"
        self.assertTrue((~zero).value)
        self.assertFalse((~one).value)

    def test___and__(self):
        "Defines a truth table for and"
        self.assertFalse((zero & zero).value)
        self.assertFalse((zero & one).value)
        self.assertFalse((one & zero).value)
        self.assertTrue((one & one).value)

    def test___or__(self):
        "Defines a truth table for or"
        self.assertFalse((zero | zero).value)
        self.assertTrue((zero | one).value)
        self.assertTrue((one | zero).value)
        self.assertTrue((one | one).value)

    def test___xor__(self):
        "Defines a truth table for xor"
        self.assertFalse((zero ^ zero).value)
        self.assertTrue((zero ^ one).value)
        self.assertTrue((one ^ zero).value)
        self.assertFalse((one ^ one).value)

    def test_mux(self):
        "Defines a truth table for mux"
        self.assertFalse(mux(zero, zero, zero).value)
        self.assertFalse(mux(zero, zero, one).value)
        self.assertFalse(mux(zero, one, zero).value)
        self.assertTrue(mux(zero, one, one).value)
        self.assertTrue(mux(one, zero, zero).value)
        self.assertFalse(mux(one, zero, one).value)
        self.assertTrue(mux(one, one, zero).value)
        self.assertTrue(mux(one, one, one).value)

    def test_dmux(self):
        "Defines a truth table for dmux"
        a, b = dmux(zero, zero)
        self.assertFalse(a.value)
        self.assertFalse(b.value)
        a, b = dmux(zero, one)
        self.assertFalse(a.value)
        self.assertFalse(b.value)
        a, b = dmux(one, zero)
        self.assertTrue(a.value)
        self.assertFalse(b.value)
        a, b = dmux(one, one)
        self.assertFalse(a.value)
        self.assertTrue(b.value)


if __name__ == "__main__":
    unittest.main()