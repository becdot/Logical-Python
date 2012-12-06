from bit import Bit
from multi import Multi, multimux, or_multiway, multimux_multiway, dmux_multiway, pad_to_digits, pad_multi
from ALU import inc
from sequential import SR, FF, DFF, SingleRegister, Register, RAM, RAM8, RAM64, RAM512, RAM4K, RAM16K, PC

import unittest

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

zero = Bit(0)
one = Bit(1)

neg_one = Multi(Bit(digit) for digit in '1111111111111111')
neg_two = Multi(Bit(digit) for digit in '1111111111111110')
neg_three = Multi(Bit(digit) for digit in '1111111111111101')
neg_four = Multi(Bit(digit) for digit in '1111111111111100')
neg_eight = Multi(Bit(digit) for digit in '1111111111111000')

zero16 = Multi([zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero])
one16 = Multi([zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, one])
two16 = Multi([zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, one, zero])
three16 = Multi([zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, one, one])
four16 = Multi([zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, one, zero, zero])
eight16 = Multi([zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, one, zero, zero, zero])
m_16384  = Multi([zero, one, zero, one, zero, zero, one, zero, zero, one, zero, one, zero, one, zero, zero])
m_16385  = Multi([zero, one, zero, one, zero, zero, one, zero, zero, one, zero, one, zero, one, zero, one])

zero3 = Multi([zero, zero, zero])
zero6 = Multi([zero, zero, zero, zero, zero, zero])
zero9 = Multi(Bit(i) for i in '000000000')
one3 = Multi([zero, zero, one])
three3 = Multi([zero, one, one])
four3 = Multi([one, zero, zero])
thirteen6 = Multi([zero, zero, one, one, zero, one])
fortyseven6 = Multi([one, zero, one, one, one, one])
sixtythree6 = Multi([one, one, one, one, one, one])
oneC_9 = Multi(Bit(i) for i in '001100100')
oneC_12 = Multi(Bit(i) for i in '000001100100')
oneC_14 = Multi(Bit(i) for i in '00000001100100')
threeC = Multi(Bit(i) for i in '100101100')
fiveC = Multi(Bit(i) for i in '111110100')
threeK = Multi(Bit(i) for i in '101110111000')
threeK_14 = Multi(Bit(i) for i in '00101110111000')
fortynintyfive = Multi(Bit(i) for i in '111111111111')
sixteenthreeeightythree = Multi(Bit(i) for i in '11111111111111')



class TestLogic(unittest.TestCase):

    def test_sr(self):
        """Implements an SR gate(s, r) whereby:
        SR(0, 0) -> Q (hold pattern)
        SR(0, 1) -> 0 (reset)
        SR(1, 0) -> 1 (set)
        SR(1, 1) -> not allowed"""

        sr = SR()
        self.assertFalse(sr(zero, zero))
        self.assertFalse(sr(zero, one))
        self.assertTrue(sr(one, zero))
        self.assertTrue(sr(zero, zero))
        self.assertTrue(sr(zero, zero))
        self.assertFalse(sr(zero, one))
        self.assertFalse(sr(zero, zero))

    def test_FF(self):
        """FF(0, 0) -> Q (hold)
        FF(0, 1) -> 0 (reset)
        FF(1, 0) -> Q (hold)
        FF(1, 1) -> 1 (set)"""

        ff = FF()
        self.assertFalse(ff(zero, zero))
        self.assertFalse(ff(zero, one))
        self.assertFalse(ff(one, zero))
        self.assertTrue(ff(one, one))
        self.assertTrue(ff(zero, zero))
        self.assertTrue(ff(one, zero))
        self.assertFalse(ff(zero, one))
        self.assertFalse(ff(zero, zero))

    def test_DFF(self):
        """FF(0, 0) -> Q (hold)
        FF(0, 1) -> 0 (reset)
        FF(1, 0) -> Q (hold)
        FF(1, 1) -> 1 (set)"""

        dff = DFF()
        self.assertFalse(dff(zero, zero)) #(0, 0)
        self.assertFalse(dff(zero, one)) #(0, 0)
        self.assertFalse(dff(one, zero)) #(0, 0)
        self.assertFalse(dff(one, one)) #(1, 0)
        self.assertTrue(dff(one, zero)) #(1, 1)
        self.assertTrue(dff(zero, zero)) #(1, 1)
        self.assertTrue(dff(zero, one)) #(0, 1)
        self.assertFalse(dff(zero, zero)) #(0, 0)
        self.assertFalse(dff(one, one)) #(1, 0)
        self.assertTrue(dff(zero, zero)) #(1, 1)

    def test_SingleRegister(self):
        "DFF changes on the falling edge, instead of the rising edge"
        bit = SingleRegister()

        self.assertFalse(bit(zero, zero, one))
        self.assertFalse(bit(zero, zero, zero))
        self.assertFalse(bit(zero, one, one))
        self.assertFalse(bit(zero, one, zero))
        self.assertFalse(bit(one, zero, one))
        self.assertFalse(bit(one, zero, zero))
        self.assertFalse(bit(one, one, one))
        self.assertTrue(bit(one, one, zero))
        self.assertTrue(bit(zero, zero, one))
        self.assertTrue(bit(zero, zero, zero))
        self.assertTrue(bit(one, zero, one))
        self.assertTrue(bit(one, zero, zero))
        self.assertTrue(bit(zero, one, one))
        self.assertFalse(bit(zero, one, zero))
        self.assertFalse(bit(one, one, one))
        self.assertTrue(bit(one, one, zero))
        self.assertTrue(bit(zero, zero, one))
        self.assertTrue(bit(zero, zero, zero))
        self.assertTrue(bit(zero, one, one))
        self.assertFalse(bit(zero, one, zero))

    def test_Register(self):
        reg = Register()
        self.assertEquals(str(reg(zero16, zero, one)), str(zero16))
        self.assertEquals(str(reg(zero16, zero, zero)), str(zero16))
        self.assertEquals(str(reg(zero16, one, one)), str(zero16))
        self.assertEquals(str(reg(zero16, one, zero)), str(zero16))
        self.assertEquals(str(reg(m_16384, zero, one)), str(zero16))
        self.assertEquals(str(reg(m_16384, zero, zero)), str(zero16))
        self.assertEquals(str(reg(m_16385, zero, one)), str(zero16))
        self.assertEquals(str(reg(m_16385, zero, zero)), str(zero16))
        self.assertEquals(str(reg(m_16384, one, one)), str(zero16))
        self.assertEquals(str(reg(m_16384, one, zero)), str(m_16384))
        self.assertEquals(str(reg(m_16384, zero, one)), str(m_16384))
        self.assertEquals(str(reg(m_16384, zero, zero)), str(m_16384))
        self.assertEquals(str(reg(neg_eight, one, one)), str(m_16384))
        self.assertEquals(str(reg(neg_eight, one, zero)),str(neg_eight))
        self.assertEquals(str(reg(neg_one, zero, one)), str(neg_eight))
        self.assertEquals(str(reg(neg_one, zero, zero)), str(neg_eight))
        self.assertEquals(str(reg(neg_one, one, one)), str(neg_eight))
        self.assertEquals(str(reg(neg_one, one, zero)), str(neg_one))

    def test_RAM8(self):
        "Takes a 3-bit address"
        ram = RAM8()

        self.assertEquals(str(ram(zero16, zero, zero3, one)), str(zero16))
        self.assertEquals(str(ram(zero16, zero, zero3, zero)), str(zero16))
        self.assertEquals(str(ram(zero16, one, zero3, one)), str(zero16))
        self.assertEquals(str(ram(zero16, one, zero3, zero)), str(zero16))
        self.assertEquals(str(ram(neg_one, one, one3, one)), str(zero16))
        self.assertEquals(str(ram(neg_one, one, one3, zero)), str(neg_one))
        self.assertEquals(str(ram(neg_one, zero, zero3, one)), str(zero16))
        self.assertEquals(str(ram(neg_one, zero, zero3, zero)), str(zero16))
        self.assertEquals(str(ram(three16, zero, three3, one)), str(zero16))
        self.assertEquals(str(ram(three16, zero, three3, zero)), str(zero16))
        self.assertEquals(str(ram(three16, one, three3, one)), str(zero16))
        self.assertEquals(str(ram(three16, one, three3, zero)), str(three16))
        self.assertEquals(str(ram(three16, zero, three3, one)), str(three16))
        self.assertEquals(str(ram(three16, zero, three3, zero)), str(three16))
        self.assertEquals(str(ram(three16, zero, one3, one)), str(neg_one))
        self.assertEquals(str(ram(three16, zero, one3, zero)), str(neg_one))
        self.assertEquals(str(ram(four16, zero, one3, one)), str(neg_one))
        self.assertEquals(str(ram(four16, zero, one3, zero)), str(neg_one))
        self.assertEquals(str(ram(four16, one, four3, one)), str(zero16))
        self.assertEquals(str(ram(four16, one, four3, zero)), str(four16))

    def test_RAM64(self):
        "Takes a 6-bit address"
        ram = RAM64()

        self.assertEquals(str(ram(zero16, zero, zero6, one)), str(zero16))
        self.assertEquals(str(ram(zero16, zero, zero6, zero)), str(zero16))
        self.assertEquals(str(ram(zero16, one, zero6, one)), str(zero16))
        self.assertEquals(str(ram(zero16, one, zero6, zero)), str(zero16))
        self.assertEquals(str(ram(from_num(13), zero, zero6, one)), str(zero16))
        self.assertEquals(str(ram(from_num(13), zero, zero6, zero)), str(zero16))
        self.assertEquals(str(ram(from_num(13), one, thirteen6, one)), str(zero16))
        self.assertEquals(str(ram(from_num(13), one, thirteen6, zero)), str(from_num(13)))
        self.assertEquals(str(ram(from_num(13), zero, zero6, one)), str(zero16))
        self.assertEquals(str(ram(from_num(13), zero, zero6, zero)), str(zero16))
        self.assertEquals(str(ram(from_num(47), zero, fortyseven6, one)), str(zero16))
        self.assertEquals(str(ram(from_num(47), zero, fortyseven6, zero)), str(zero16))
        self.assertEquals(str(ram(from_num(47), one, fortyseven6, one)), str(zero16))
        self.assertEquals(str(ram(from_num(47), one, fortyseven6, zero)), str(from_num(47)))
        self.assertEquals(str(ram(from_num(47), zero, fortyseven6, one)), str(from_num(47)))
        self.assertEquals(str(ram(from_num(47), zero, fortyseven6, zero)), str(from_num(47)))
        self.assertEquals(str(ram(from_num(47), zero, fortyseven6, one)), str(from_num(47)))
        self.assertEquals(str(ram(from_num(47), zero, thirteen6, zero)), str(from_num(13)))
        self.assertEquals(str(ram(from_num(63), zero, thirteen6, one)), str(from_num(13)))
        self.assertEquals(str(ram(from_num(63), zero, thirteen6, zero)), str(from_num(13)))
        self.assertEquals(str(ram(from_num(63), one, sixtythree6, one)), str(zero16))
        self.assertEquals(str(ram(from_num(63), one, sixtythree6, zero)), str(from_num(63)))

    def test_RAM512(self):
        "Takes a 9-bit address"
        ram = RAM512()


        self.assertEquals(str(ram(zero16, zero, zero9, one)), str(zero16))
        self.assertEquals(str(ram(zero16, zero, zero9, zero)), str(zero16))
        self.assertEquals(str(ram(zero16, one, zero9, one)), str(zero16))
        self.assertEquals(str(ram(zero16, one, zero9, zero)), str(zero16))
        self.assertEquals(str(ram(from_num(100), zero, zero9, one)), str(zero16))
        self.assertEquals(str(ram(from_num(100), zero, zero9, zero)), str(zero16))
        self.assertEquals(str(ram(from_num(100), one, oneC_9, one)), str(zero16))
        self.assertEquals(str(ram(from_num(100), one, oneC_9, zero)), str(from_num(100)))
        self.assertEquals(str(ram(from_num(100), zero, zero9, one)), str(zero16))
        self.assertEquals(str(ram(from_num(100), zero, zero9, zero)), str(zero16))
        self.assertEquals(str(ram(from_num(300), zero, threeC, one)), str(zero16))
        self.assertEquals(str(ram(from_num(300), zero, threeC, zero)), str(zero16))
        self.assertEquals(str(ram(from_num(300), one, threeC, one)), str(zero16))
        self.assertEquals(str(ram(from_num(300), one, threeC, zero)), str(from_num(300)))
        self.assertEquals(str(ram(from_num(300), zero, threeC, one)), str(from_num(300)))
        self.assertEquals(str(ram(from_num(300), zero, threeC, zero)), str(from_num(300)))
        self.assertEquals(str(ram(from_num(300), zero, threeC, one)), str(from_num(300)))
        self.assertEquals(str(ram(from_num(300), zero, oneC_9, zero)), str(from_num(100)))
        self.assertEquals(str(ram(from_num(500), zero, oneC_9, one)), str(from_num(100)))
        self.assertEquals(str(ram(from_num(500), zero, oneC_9, zero)), str(from_num(100)))
        self.assertEquals(str(ram(from_num(500), one, fiveC, one)), str(zero16))
        self.assertEquals(str(ram(from_num(500), one, fiveC, zero)), str(from_num(500)))

    def test_RAM4K(self):
        "Takes a 12-bit address"
        ram = RAM4K()


        self.assertEquals(str(ram(zero16, zero, zero6, one)), str(zero16))
        self.assertEquals(str(ram(zero16, zero, zero6, zero)), str(zero16))
        self.assertEquals(str(ram(zero16, one, zero6, one)), str(zero16))
        self.assertEquals(str(ram(zero16, one, zero6, zero)), str(zero16))
        self.assertEquals(str(ram(from_num(100), zero, zero6, one)), str(zero16))
        self.assertEquals(str(ram(from_num(100), zero, zero6, zero)), str(zero16))
        self.assertEquals(str(ram(from_num(100), one, oneC_12, one)), str(zero16))
        self.assertEquals(str(ram(from_num(100), one, oneC_12, zero)), str(from_num(100)))
        self.assertEquals(str(ram(from_num(100), zero, zero6, one)), str(zero16))
        self.assertEquals(str(ram(from_num(100), zero, zero6, zero)), str(zero16))
        self.assertEquals(str(ram(from_num(3000), zero, threeK, one)), str(zero16))
        self.assertEquals(str(ram(from_num(3000), zero, threeK, zero)), str(zero16))
        self.assertEquals(str(ram(from_num(3000), one, threeK, one)), str(zero16))
        self.assertEquals(str(ram(from_num(3000), one, threeK, zero)), str(from_num(3000)))
        self.assertEquals(str(ram(from_num(3000), zero, threeK, one)), str(from_num(3000)))
        self.assertEquals(str(ram(from_num(3000), zero, threeK, zero)), str(from_num(3000)))
        self.assertEquals(str(ram(from_num(3000), zero, threeK, one)), str(from_num(3000)))
        self.assertEquals(str(ram(from_num(3000), zero, oneC_12, zero)), str(from_num(100)))
        self.assertEquals(str(ram(from_num(4095), zero, oneC_12, one)), str(from_num(100)))
        self.assertEquals(str(ram(from_num(4095), zero, oneC_12, zero)), str(from_num(100)))
        self.assertEquals(str(ram(from_num(4095), one, fortynintyfive, one)), str(zero16))
        self.assertEquals(str(ram(from_num(4095), one, fortynintyfive, zero)), str(from_num(4095)))

    # INCREDIBLY SLOW, be careful in uncommenting!
    # def test_RAM16K(self):
    #     "Takes a 14-bit address"
    #     ram = RAM16K()

    #     self.assertEquals(str(ram(zero16, zero, zero6, one)), str(zero16))
    #     self.assertEquals(str(ram(zero16, zero, zero6, zero)), str(zero16))
    #     self.assertEquals(str(ram(zero16, one, zero6, one)), str(zero16))
    #     self.assertEquals(str(ram(zero16, one, zero6, zero)), str(zero16))
    #     self.assertEquals(str(ram(from_num(100), zero, zero6, one)), str(zero16))
    #     self.assertEquals(str(ram(from_num(100), zero, zero6, zero)), str(zero16))
    #     self.assertEquals(str(ram(from_num(100), one, oneC_14, one)), str(zero16))
    #     self.assertEquals(str(ram(from_num(100), one, oneC_14, zero)), str(from_num(100)))
    #     self.assertEquals(str(ram(from_num(100), zero, zero6, one)), str(zero16))
    #     self.assertEquals(str(ram(from_num(100), zero, zero6, zero)), str(zero16))
    #     self.assertEquals(str(ram(from_num(3000), zero, threeK_14, one)), str(zero16))
    #     self.assertEquals(str(ram(from_num(3000), zero, threeK_14, zero)), str(zero16))
    #     self.assertEquals(str(ram(from_num(3000), one, threeK_14, one)), str(zero16))
    #     self.assertEquals(str(ram(from_num(3000), one, threeK_14, zero)), str(from_num(3000)))
    #     self.assertEquals(str(ram(from_num(3000), zero, threeK_14, one)), str(from_num(3000)))
    #     self.assertEquals(str(ram(from_num(3000), zero, threeK_14, zero)), str(from_num(3000)))
    #     self.assertEquals(str(ram(from_num(3000), zero, threeK_14, one)), str(from_num(3000)))
    #     self.assertEquals(str(ram(from_num(3000), zero, oneC_14, zero)), str(from_num(100)))
    #     self.assertEquals(str(ram(from_num(16383), zero, oneC_14, one)), str(from_num(100)))
    #     self.assertEquals(str(ram(from_num(16383), zero, oneC_14, zero)), str(from_num(100)))
    #     self.assertEquals(str(ram(from_num(16383), one, sixteenthreeeightythree, one)), str(zero16))
    #     self.assertEquals(str(ram(from_num(16383), one, sixteenthreeeightythree, zero)), str(from_num(16383)))


    def test_PC(self):
        "pc(input, load, increase, reset, clock) -> Multi instance corresponding to control bits"

        pc = PC()

        self.assertEqual(str(pc(zero16, zero, zero, zero, one)), str(zero16))
        self.assertEqual(str(pc(zero16, zero, zero, zero, zero)), str(zero16))
        self.assertEqual(str(pc(zero16, zero, one, zero, one)), str(zero16))
        self.assertEqual(str(pc(zero16, zero, one, zero, zero)), str(one16))
        self.assertEqual(str(pc(neg_four, zero, one, zero, one)), str(one16))
        self.assertEqual(str(pc(neg_four, zero, one, zero, zero)), str(two16))
        self.assertEqual(str(pc(neg_four, one, one, zero, one)), str(two16))
        self.assertEqual(str(pc(neg_four, one, one, zero, zero)), str(neg_four))
        self.assertEqual(str(pc(neg_four, zero, one, zero, one)), str(neg_four))
        self.assertEqual(str(pc(neg_four, zero, one, zero, zero)), str(neg_three))
        self.assertEqual(str(pc(neg_four, zero, one, zero, one)), str(neg_three))
        self.assertEqual(str(pc(neg_four, zero, one, zero, zero)), str(neg_two))
        self.assertEqual(str(pc(eight16, one, zero, zero, one)), str(neg_two))
        self.assertEqual(str(pc(eight16, one, zero, zero, zero)), str(eight16))
        self.assertEqual(str(pc(eight16, one, zero, one, one)), str(eight16))
        self.assertEqual(str(pc(eight16, one, zero, one, zero)), str(zero16))
        self.assertEqual(str(pc(eight16, one, one, zero, one)), str(zero16))
        self.assertEqual(str(pc(eight16, one, one, zero, zero)), str(eight16))
        self.assertEqual(str(pc(eight16, one, one, one, one)), str(eight16))
        self.assertEqual(str(pc(eight16, one, one, one, zero)), str(zero16))
        self.assertEqual(str(pc(eight16, zero, one, zero, one)), str(zero16))
        self.assertEqual(str(pc(eight16, zero, one, zero, zero)), str(one16))

if __name__ == "__main__":
    unittest.main()