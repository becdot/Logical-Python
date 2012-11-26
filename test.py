import unittest

from logic import *


zero = Bit(0)
one = Bit(1)
nand = Bit.nand

m_fifteen = Multi([one, one, one, one])
m_fourteen = Multi([one, one, one, zero])
m_eight = Multi([one, zero, zero, zero])
m_three = Multi([one, one])
m_one = Multi([zero, zero, one])
m_zero = Multi([zero])


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

    def test_Multi_to_decimel(self):
        "Binary -> decimel"
        "TODO -- check against negative numbers"
        self.assertEquals(Multi.to_decimel(m_fifteen), 15)
        self.assertEquals(Multi.to_decimel(m_eight), 8)
        self.assertEquals(Multi.to_decimel(m_one), 1)
        self.assertEquals(Multi.to_decimel(m_zero), 0)


    def test_Multi_and(self):
        "Checks that the multibit & returns the correct values and pads Multi arrays of different sizes appropriately"
        "TODO - pad_multi changes the underlying Multi arrays, needs fixing"

        m_fifteen = Multi([one, one, one, one])
        m_fourteen = Multi([one, one, one, zero])
        m_eight = Multi([one, zero, zero, zero])
        m_three = Multi([one, one])
        m_one = Multi([zero, zero, one])
        m_zero = Multi([zero])

        self.assertEquals(str(m_eight & m_zero), str(m_zero))
        self.assertEquals(str(m_eight & m_one), str(m_zero))
        self.assertEquals(str(m_eight & m_fifteen), str(m_eight))
        self.assertEquals(str(m_three & m_fourteen), str(Multi([zero, zero, one, zero])))
        self.assertEquals(str(m_one & m_three), str(m_one))

    def test_Multi_not(self):
        "Checks that the multibit ~ flips all the signs of a Multi array"
        "TODO - Once pad_multi is fixed to not modify underlying Multi arrays, move test values outside the test function"

        m_fifteen = Multi([one, one, one, one])
        m_fourteen = Multi([one, one, one, zero])
        m_eight = Multi([one, zero, zero, zero])
        m_three = Multi([one, one])
        m_one = Multi([zero, zero, one])
        m_zero = Multi([zero])

        self.assertEquals(str(~m_fifteen), str(Multi([zero, zero, zero, zero])))
        self.assertEquals(str(~m_eight), str(Multi([zero, one, one, one])))
        self.assertEquals(str(~m_three), str(Multi([zero, zero])))
        self.assertEquals(str(~m_one), str(Multi([one, one, zero])))
        self.assertEquals(str(~m_zero), str(Multi([one])))

    def test_Multi_or(self):
        "Checks that multibit | returns the correct value and pads Multi arrays of different sizes appropriately"
        "TODO - pad_multi changes the underlying Multi arrays, needs fixing"

        m_fifteen = Multi([one, one, one, one])
        m_fourteen = Multi([one, one, one, zero])
        m_eight = Multi([one, zero, zero, zero])
        m_three = Multi([one, one])
        m_one = Multi([zero, zero, one])
        m_zero = Multi([zero])

        self.assertEquals(str(m_eight | m_zero), str(m_eight))
        self.assertEquals(str(m_eight | m_one), str(Multi([one, zero, zero, one])))
        self.assertEquals(str(m_eight | m_fifteen), str(m_fifteen))
        self.assertEquals(str(m_three | m_one), str(Multi([zero, zero, one, one])))
        self.assertEquals(str(m_one | m_fourteen), str(m_fifteen))

    def test_multimux(self):

        m_fifteen = Multi([one, one, one, one])
        m_fourteen = Multi([one, one, one, zero])
        m_eight = Multi([one, zero, zero, zero])
        m_three = Multi([one, one])
        m_one = Multi([zero, zero, one])
        m_zero = Multi([zero])

        self.assertEquals(str(Multi.multimux(m_eight, m_zero, zero)), str(m_eight))
        self.assertEquals(str(Multi.multimux(m_eight, m_fifteen, one)), str(m_fifteen))
        self.assertEquals(str(Multi.multimux(m_zero, m_one, zero)), str(m_zero))
        self.assertEquals(str(Multi.multimux(m_zero, m_one, one)), str(m_one))

    def test_or_multiway(self):

        m_fifteen = Multi([one, one, one, one])
        m_fourteen = Multi([one, one, one, zero])
        m_eight = Multi([one, zero, zero, zero])
        m_three = Multi([one, one])
        m_one = Multi([zero, zero, one])
        m_zero = Multi([zero])

        self.assertTrue(str(Multi.or_multiway(m_eight)))
        self.assertTrue(str(Multi.or_multiway(m_fifteen)))
        self.assertTrue(str(Multi.or_multiway(m_one)))
        self.assertTrue(str(Multi.or_multiway(m_zero)))

    def test_multimux_multiway(self):

        m_fifteen = Multi([one, one, one, one])
        m_fourteen = Multi([one, one, one, zero])
        m_eight = Multi([one, zero, zero, zero])
        m_three = Multi([one, one])
        m_one = Multi([zero, zero, one])
        m_zero = Multi([zero])

        self.assertEquals(str(Multi.multimux_multiway(Multi([one]), m_fifteen, m_fourteen)), str(m_fourteen))
        self.assertEquals(str(Multi.multimux_multiway(Multi([one, one]), m_fifteen, m_fourteen, m_zero, m_one)), str(m_one))
        self.assertEquals(str(Multi.multimux_multiway(Multi([zero, one]), m_three, m_zero, m_fifteen, m_fourteen)), str(m_zero))
        self.assertEquals(str(Multi.multimux_multiway(Multi([one, zero, zero]), m_zero, m_three, m_fourteen, m_eight, m_one, m_zero, 
                                                      m_fifteen, m_fourteen)), str(m_eight))
        self.assertEquals(str(Multi.multimux_multiway(Multi([zero, one, zero]), m_zero, m_three, m_fourteen, m_eight, m_one, m_zero, 
                                                      m_fifteen, m_fourteen)), str(m_fourteen))

    def test_dmux_multiway(self):
        m_fifteen = Multi([one, one, one, one])
        m_fourteen = Multi([one, one, one, zero])
        m_eight = Multi([one, zero, zero, zero])
        m_three = Multi([one, one])
        m_one = Multi([zero, zero, one])
        m_zero = Multi([zero])

        a = Multi.dmux_multiway(Multi([one]), Multi([zero]))
        b = Multi.dmux_multiway(Multi([one]), Multi([zero, one]))
        c = Multi.dmux_multiway(Multi([one]), Multi([one, one]))
        d = Multi.dmux_multiway(Multi([one]), Multi([zero, one, one]))
        self.assertEquals(Multi.dmux_multiway([str(bit) for bit in a], 
                                                [str(Multi([one])), str(Multi([zero]))]))
        # self.assertEquals(Multi.dmux_multiway([str(bit) for bit in b], 
        #                                     [str(Multi([zero])), str(Multi([one])), str(Multi([zero])), str(Multi([zero]))]))
        # self.assertEquals(Multi.dmux_multiway([str(bit) for bit in c], 
        #                                     [str(Multi([zero])), str(Multi([zero])), str(Multi([zero])), str(Multi([one]))]))
        # self.assertEquals(Multi.dmux_multiway([str(bit) for bit in d], 
        #                                     [str(Multi([zero])), str(Multi([zero])), str(Multi([zero])), str(Multi([one])), 
        #                                     str(Multi([zero])), str(Multi([zero])), str(Multi([zero])), str(Multi([zero]))]))



if __name__ == "__main__":
    unittest.main()