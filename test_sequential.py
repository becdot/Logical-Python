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
thirteen16 = from_num(13)
fortyseven6 = Multi([one, zero, one, one, one, one])
fortyseven16 = from_num(47)
sixtythree6 = Multi([one, one, one, one, one, one])
sixtythree16 = from_num(63)
oneC_9 = Multi(Bit(i) for i in '001100100')
oneC_12 = Multi(Bit(i) for i in '000001100100')
oneC_14 = Multi(Bit(i) for i in '00000001100100')
oneC16 = from_num(100)
threeC = Multi(Bit(i) for i in '100101100')
threeC16 = from_num(300)
fiveC = Multi(Bit(i) for i in '111110100')
fiveC16 = from_num(500)
threeK = Multi(Bit(i) for i in '101110111000')
threeK_14 = Multi(Bit(i) for i in '00101110111000')
threeK16 = from_num(3000)
fortynintyfive = Multi(Bit(i) for i in '111111111111')
fortynintyfive16 = from_num(4095)
sixteenthreeeightythree = Multi(Bit(i) for i in '11111111111111')
sixteenthreeeightythree16 = from_num(16383)



class TestLogic(unittest.TestCase):

    def test_sr(self):
        """Implements an SR gate(s, r) whereby:
        SR(0, 0) -> Q (hold pattern)
        SR(0, 1) -> 0 (reset)
        SR(1, 0) -> 1 (set)
        SR(1, 1) -> not allowed"""

        sr = SR()
        self.assertFalse(sr(one, one))
        self.assertFalse(sr(zero, one))
        self.assertTrue(sr(one, zero))
        self.assertTrue(sr(one, one))
        self.assertTrue(sr(one, one))
        self.assertFalse(sr(zero, one))
        self.assertFalse(sr(one, one))

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
        self.assertEquals(str(ram(thirteen16, zero, zero6, one)), str(zero16))
        self.assertEquals(str(ram(thirteen16, zero, zero6, zero)), str(zero16))
        self.assertEquals(str(ram(thirteen16, one, thirteen6, one)), str(zero16))
        self.assertEquals(str(ram(thirteen16, one, thirteen6, zero)), str(thirteen16))
        self.assertEquals(str(ram(thirteen16, zero, zero6, one)), str(zero16))
        self.assertEquals(str(ram(thirteen16, zero, zero6, zero)), str(zero16))
        self.assertEquals(str(ram(fortyseven16, zero, fortyseven6, one)), str(zero16))
        self.assertEquals(str(ram(fortyseven16, zero, fortyseven6, zero)), str(zero16))
        self.assertEquals(str(ram(fortyseven16, one, fortyseven6, one)), str(zero16))
        self.assertEquals(str(ram(fortyseven16, one, fortyseven6, zero)), str(fortyseven16))
        self.assertEquals(str(ram(fortyseven16, zero, fortyseven6, one)), str(fortyseven16))
        self.assertEquals(str(ram(fortyseven16, zero, fortyseven6, zero)), str(fortyseven16))
        self.assertEquals(str(ram(fortyseven16, zero, fortyseven6, one)), str(fortyseven16))
        self.assertEquals(str(ram(fortyseven16, zero, thirteen6, zero)), str(thirteen16))
        self.assertEquals(str(ram(sixtythree16, zero, thirteen6, one)), str(thirteen16))
        self.assertEquals(str(ram(sixtythree16, zero, thirteen6, zero)), str(thirteen16))
        self.assertEquals(str(ram(sixtythree16, one, sixtythree6, one)), str(zero16))
        self.assertEquals(str(ram(sixtythree16, one, sixtythree6, zero)), str(sixtythree16))

    def test_RAM512(self):
        "Takes a 9-bit address"
        ram = RAM512()


        self.assertEquals(str(ram(zero16, zero, zero9, one)), str(zero16))
        self.assertEquals(str(ram(zero16, zero, zero9, zero)), str(zero16))
        self.assertEquals(str(ram(zero16, one, zero9, one)), str(zero16))
        self.assertEquals(str(ram(zero16, one, zero9, zero)), str(zero16))
        self.assertEquals(str(ram(oneC16, zero, zero9, one)), str(zero16))
        self.assertEquals(str(ram(oneC16, zero, zero9, zero)), str(zero16))
        self.assertEquals(str(ram(oneC16, one, oneC_9, one)), str(zero16))
        self.assertEquals(str(ram(oneC16, one, oneC_9, zero)), str(oneC16))
        self.assertEquals(str(ram(oneC16, zero, zero9, one)), str(zero16))
        self.assertEquals(str(ram(oneC16, zero, zero9, zero)), str(zero16))
        self.assertEquals(str(ram(threeC16, zero, threeC, one)), str(zero16))
        self.assertEquals(str(ram(threeC16, zero, threeC, zero)), str(zero16))
        self.assertEquals(str(ram(threeC16, one, threeC, one)), str(zero16))
        self.assertEquals(str(ram(threeC16, one, threeC, zero)), str(threeC16))
        self.assertEquals(str(ram(threeC16, zero, threeC, one)), str(threeC16))
        self.assertEquals(str(ram(threeC16, zero, threeC, zero)), str(threeC16))
        self.assertEquals(str(ram(threeC16, zero, threeC, one)), str(threeC16))
        self.assertEquals(str(ram(threeC16, zero, oneC_9, zero)), str(oneC16))
        self.assertEquals(str(ram(fiveC16, zero, oneC_9, one)), str(oneC16))
        self.assertEquals(str(ram(fiveC16, zero, oneC_9, zero)), str(oneC16))
        self.assertEquals(str(ram(fiveC16, one, fiveC, one)), str(zero16))
        self.assertEquals(str(ram(fiveC16, one, fiveC, zero)), str(fiveC16))

    def test_RAM4K(self):
        "Takes a 12-bit address"
        ram = RAM4K()


        self.assertEquals(str(ram(zero16, zero, zero6, one)), str(zero16))
        self.assertEquals(str(ram(zero16, zero, zero6, zero)), str(zero16))
        self.assertEquals(str(ram(zero16, one, zero6, one)), str(zero16))
        self.assertEquals(str(ram(zero16, one, zero6, zero)), str(zero16))
        self.assertEquals(str(ram(oneC16, zero, zero6, one)), str(zero16))
        self.assertEquals(str(ram(oneC16, zero, zero6, zero)), str(zero16))
        self.assertEquals(str(ram(oneC16, one, oneC_12, one)), str(zero16))
        self.assertEquals(str(ram(oneC16, one, oneC_12, zero)), str(oneC16))
        self.assertEquals(str(ram(oneC16, zero, zero6, one)), str(zero16))
        self.assertEquals(str(ram(oneC16, zero, zero6, zero)), str(zero16))
        self.assertEquals(str(ram(threeK16, zero, threeK, one)), str(zero16))
        self.assertEquals(str(ram(threeK16, zero, threeK, zero)), str(zero16))
        self.assertEquals(str(ram(threeK16, one, threeK, one)), str(zero16))
        self.assertEquals(str(ram(threeK16, one, threeK, zero)), str(threeK16))
        self.assertEquals(str(ram(threeK16, zero, threeK, one)), str(threeK16))
        self.assertEquals(str(ram(threeK16, zero, threeK, zero)), str(threeK16))
        self.assertEquals(str(ram(threeK16, zero, threeK, one)), str(threeK16))
        self.assertEquals(str(ram(threeK16, zero, oneC_12, zero)), str(oneC16))
        self.assertEquals(str(ram(fortynintyfive16, zero, oneC_12, one)), str(oneC16))
        self.assertEquals(str(ram(fortynintyfive16, zero, oneC_12, zero)), str(oneC16))
        self.assertEquals(str(ram(fortynintyfive16, one, fortynintyfive, one)), str(zero16))
        self.assertEquals(str(ram(fortynintyfive16, one, fortynintyfive, zero)), str(fortynintyfive16))

    # # INCREDIBLY SLOW, be careful in uncommenting!
    def test_RAM16K(self):
        "Takes a 14-bit address"
        ram = RAM16K()

        self.assertEquals(str(ram(zero16, zero, zero6, one)), str(zero16))
        self.assertEquals(str(ram(zero16, zero, zero6, zero)), str(zero16))
        self.assertEquals(str(ram(zero16, one, zero6, one)), str(zero16))
        self.assertEquals(str(ram(zero16, one, zero6, zero)), str(zero16))
        self.assertEquals(str(ram(oneC16, zero, zero6, one)), str(zero16))
        self.assertEquals(str(ram(oneC16, zero, zero6, zero)), str(zero16))
        self.assertEquals(str(ram(oneC16, one, oneC_14, one)), str(zero16))
        self.assertEquals(str(ram(oneC16, one, oneC_14, zero)), str(oneC16))
        self.assertEquals(str(ram(oneC16, zero, zero6, one)), str(zero16))
        self.assertEquals(str(ram(oneC16, zero, zero6, zero)), str(zero16))
        self.assertEquals(str(ram(threeK16, zero, threeK_14, one)), str(zero16))
        self.assertEquals(str(ram(threeK16, zero, threeK_14, zero)), str(zero16))
        self.assertEquals(str(ram(threeK16, one, threeK_14, one)), str(zero16))
        self.assertEquals(str(ram(threeK16, one, threeK_14, zero)), str(threeK16))
        self.assertEquals(str(ram(threeK16, zero, threeK_14, one)), str(threeK16))
        self.assertEquals(str(ram(threeK16, zero, threeK_14, zero)), str(threeK16))
        self.assertEquals(str(ram(threeK16, zero, threeK_14, one)), str(threeK16))
        self.assertEquals(str(ram(threeK16, zero, oneC_14, zero)), str(oneC16))
        self.assertEquals(str(ram(sixteenthreeeightythree16, zero, oneC_14, one)), str(oneC16))
        self.assertEquals(str(ram(sixteenthreeeightythree16, zero, oneC_14, zero)), str(oneC16))
        self.assertEquals(str(ram(sixteenthreeeightythree16, one, sixteenthreeeightythree, one)), str(zero16))
        self.assertEquals(str(ram(sixteenthreeeightythree16, one, sixteenthreeeightythree, zero)), str(sixteenthreeeightythree16))


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
    unittest.main(module='test_sequential')