import unittest

from logic2 import *


zero = Bit(0)
one = Bit(1)
nand = Bit.nand

m_eight = Multi([one, zero, zero, zero])
m_three = Multi([zero, zero, one, one])
m_zero = Multi([zero, zero, zero, zero])
m_one = Multi([zero, zero, zero, one])
m_n_one = Multi([one, one, one, one], neg=True)
m_n_two = Multi([one, one, one, zero], neg=True)

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
        self.assertFalse(Bit.mux(zero, zero, zero))
        self.assertFalse(Bit.mux(zero, zero, one))
        self.assertFalse(Bit.mux(zero, one, zero))
        self.assertTrue(Bit.mux(zero, one, one))
        self.assertTrue(Bit.mux(one, zero, zero))
        self.assertFalse(Bit.mux(one, zero, one))
        self.assertTrue(Bit.mux(one, one, zero))
        self.assertTrue(Bit.mux(one, one, one))

    def test_dmux(self):
        "Defines a truth table for dmux"
        a, b = Bit.dmux(zero, zero)
        self.assertFalse(a)
        self.assertFalse(b)
        a, b = Bit.dmux(zero, one)
        self.assertFalse(a)
        self.assertFalse(b)
        a, b = Bit.dmux(one, zero)
        self.assertTrue(a)
        self.assertFalse(b)
        a, b = Bit.dmux(one, one)
        self.assertFalse(a)
        self.assertTrue(b)

    def test_Multi_binary(self):
        """Checks that the binary() function returns what it should
            PROBLEM -- Multi[zero, zero] -> '0b00', whereas bin(0) -> '0b0'"""
        self.assertEquals(m_eight.binary(), '0b1000')
        self.assertEquals(m_zero.binary(), '0b0000')
        self.assertEquals(m_n_one.binary(), '-0b1111')
        self.assertEquals(m_n_two.binary(), '-0b1110')

    def test_Multi_and(self):
        self.assertEquals(str(m_eight & m_zero), str(m_zero))
        self.assertEquals(str(m_eight & m_one), str(m_zero))
        self.assertEquals(str(m_eight & m_n_one), str(m_eight))
        self.assertEquals(str(m_three & m_n_two), str(Multi([zero, zero, one, zero])))

    def test_radix(self):
        print m_n_one.radix()
        print m_n_two.radix()


if __name__ == "__main__":
    unittest.main()