from bit import Bit, dmux, mux
from multi import Multi, multimux, dmux_multiway, multimux_multiway, pad_to_digits, pad_multi
from ALU import half_adder, full_adder, add_multi, inc, alu
from sequential import SR, FF, DFF, SingleRegister, Register, RAM, RAM8, RAM64, RAM512, RAM4K, RAM16K, PC
from computer import CPU

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
zero16 = Multi([zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero])
one16 = Multi([zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, one])
two16 = Multi([zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, one, zero])
three16 = Multi([zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, one, one])
four16 = Multi([zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, one, zero, zero])
eight16 = Multi([zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, zero, one, zero, zero, zero])

a12345 = Multi(from_num(12345)[1:])
a23456 = Multi(from_num(23456)[1:])
a1000 = Multi(from_num(1000)[1:])
a1001 = Multi(from_num(1001)[1:])
a14 = Multi(from_num(14)[1:])
a999 = Multi(from_num(999)[1:])
a21 = Multi(from_num(21)[1:])
a2 = Multi(from_num(2)[1:])
a32767 = Multi(from_num(32767)[1:])


i0 = Multi(Bit(digit) for digit in "0011000000111001")
i1 = Multi(Bit(digit) for digit in "1110110000010000")
i2 = Multi(Bit(digit) for digit in "0101101110100000")
i3 = Multi(Bit(digit) for digit in "1110000111010000")
i4 = Multi(Bit(digit) for digit in "0000001111101000")
i5 = Multi(Bit(digit) for digit in "1110001100001000")
i6 = Multi(Bit(digit) for digit in "0000001111101001")
i7 = Multi(Bit(digit) for digit in "1110001110011000")
i8 = Multi(Bit(digit) for digit in "0000001111101000")
i9 = Multi(Bit(digit) for digit in "1111010011010000")
i10 = Multi(Bit(digit) for digit in "0000000000001110")
i11 = Multi(Bit(digit) for digit in "1110001100000100")
i12 = Multi(Bit(digit) for digit in "0000001111100111")
i13 = Multi(Bit(digit) for digit in "1110110111100000")
i14 = Multi(Bit(digit) for digit in "1110001100001000")
i15 = Multi(Bit(digit) for digit in "0000000000010101")
i16 = Multi(Bit(digit) for digit in "1110011111000010")
i17 = Multi(Bit(digit) for digit in "0000000000000010")
i18 = Multi(Bit(digit) for digit in "1110000010010000")
i19 = Multi(Bit(digit) for digit in "0000001111101000")
i20 = Multi(Bit(digit) for digit in "1110111010010000")

o11111 = from_num(11111)
o11110 = from_num(11110)
o11109 = from_num(11109)

pc0 = Multi(from_num(0)[1:])
pc1 = Multi(from_num(1)[1:])
pc2 = Multi(from_num(2)[1:])
pc3 = Multi(from_num(3)[1:])
pc4 = Multi(from_num(4)[1:])
pc5 = Multi(from_num(5)[1:])
pc6 = Multi(from_num(6)[1:])
pc7 = Multi(from_num(7)[1:])
pc8 = Multi(from_num(8)[1:])
pc9 = Multi(from_num(9)[1:])
pc10 = Multi(from_num(10)[1:])
pc11 = Multi(from_num(11)[1:])
pc12 = Multi(from_num(12)[1:])
pc13 = Multi(from_num(13)[1:])
pc14 = Multi(from_num(14)[1:])
pc15 = Multi(from_num(15)[1:])
pc16 = Multi(from_num(16)[1:])
pc17 = Multi(from_num(17)[1:])
pc18 = Multi(from_num(18)[1:])
pc19 = Multi(from_num(19)[1:])
pc20 = Multi(from_num(20)[1:])
pc21 = Multi(from_num(21)[1:])
pc22 = Multi(from_num(22)[1:])
pc23 = Multi(from_num(23)[1:])
pc24 = Multi(from_num(24)[1:])

class TestLogic(unittest.TestCase):
    def test_computer(self):
        c = CPU()

        # 0+
        outM, writeM, address, pc, D = c(zero16, i0, zero, one)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(pc0), str(pc0), str(zero16)))
        # 1
        outM, writeM, address, pc, D = c(zero16, i0, zero, zero)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)),
                            (str(outM), str(zero), str(a12345), str(pc1), str(zero16)))
        # 1+
        outM, writeM, address, pc, D = c(zero16, i1, zero, one)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a12345), str(pc1), str(from_num(12345))))
        # 2
        outM, writeM, address, pc, D = c(zero16, i1, zero, zero)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a12345), str(pc2), str(from_num(12345))))
        # 2+
        outM, writeM, address, pc, D = c(zero16, i2, zero, one)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a12345), str(pc2), str(from_num(12345))))
        # 3
        outM, writeM, address, pc, D = c(zero16, i2, zero, zero)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a23456), str(pc3), str(from_num(12345))))
        # 3+
        outM, writeM, address, pc, D = c(zero16, i3, zero, one)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a23456), str(pc3), str(from_num(11111))))
        # 4
        outM, writeM, address, pc, D = c(zero16, i3, zero, zero)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a23456), str(pc4), str(from_num(11111))))
        # 4+
        outM, writeM, address, pc, D = c(zero16, i4, zero, one)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a23456), str(pc4), str(from_num(11111))))
        # 5
        outM, writeM, address, pc, D = c(zero16, i4, zero, zero)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a1000), str(pc5), str(from_num(11111))))
        # 5+
        outM, writeM, address, pc, D = c(zero16, i5, zero, one)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(o11111), str(one), str(a1000), str(pc5), str(from_num(11111))))
        # 6
        outM, writeM, address, pc, D = c(zero16, i5, zero, zero)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(o11111), str(one), str(a1000), str(pc6), str(from_num(11111))))
        # 6+
        outM, writeM, address, pc, D = c(zero16, i6, zero, one)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a1000), str(pc6), str(from_num(11111))))
        # 7
        outM, writeM, address, pc, D = c(zero16, i6, zero, zero)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a1001), str(pc7), str(from_num(11111))))
        # 7+
        outM, writeM, address, pc, D = c(zero16, i7, zero, one)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(o11110), str(one), str(a1001), str(pc7), str(from_num(11110))))
        # 8
        outM, writeM, address, pc, D = c(zero16, i7, zero, zero)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(o11109), str(one), str(a1001), str(pc8), str(from_num(11110))))
        # 8+
        outM, writeM, address, pc, D = c(zero16, i8, zero, one)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a1001), str(pc8), str(from_num(11110))))
        # 9
        outM, writeM, address, pc, D = c(zero16, i8, zero, zero)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a1000), str(pc9), str(from_num(11110))))
        # 9+
        outM, writeM, address, pc, D = c(o11111, i9, zero, one)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a1000), str(pc9), str(from_num(-1))))
        # 10
        outM, writeM, address, pc, D = c(o11111, i9, zero, zero)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a1000), str(pc10), str(from_num(-1))))
        # 10+
        outM, writeM, address, pc, D = c(o11111, i10, zero, one)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a1000), str(pc10), str(from_num(-1))))
        # 11
        outM, writeM, address, pc, D = c(o11111, i10, zero, zero)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)),
                            (str(outM), str(zero), str(a14), str(pc11), str(from_num(-1))))
        # 11+
        outM, writeM, address, pc, D = c(o11111, i11, zero, one)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a14), str(pc11), str(from_num(-1))))
        # 12
        outM, writeM, address, pc, D = c(o11111, i11, zero, zero)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a14), str(pc14), str(from_num(-1))))
        # 12+
        outM, writeM, address, pc, D = c(o11111, i12, zero, one)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a14), str(pc14), str(from_num(-1))))
        # 13
        outM, writeM, address, pc, D = c(o11111, i12, zero, zero)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a999), str(pc15), str(from_num(-1))))
        # 13+
        outM, writeM, address, pc, D = c(o11111, i13, zero, one)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a999), str(pc15), str(from_num(-1))))
        # 14
        outM, writeM, address, pc, D = c(o11111, i13, zero, zero)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)),
                            (str(outM), str(zero), str(a1000), str(pc16), str(from_num(-1))))
        # 14+
        outM, writeM, address, pc, D = c(o11111, i14, zero, one)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(from_num(-1)), str(one), str(a1000), str(pc16), str(from_num(-1))))
        # 15
        outM, writeM, address, pc, D = c(o11111, i14, zero, zero)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(from_num(-1)), str(one), str(a1000), str(pc17), str(from_num(-1))))
        # 15+
        outM, writeM, address, pc, D = c(o11111, i15, zero, one)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a1000), str(pc17), str(from_num(-1))))
        # 16
        outM, writeM, address, pc, D = c(o11111, i15, zero, zero)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a21), str(pc18), str(from_num(-1))))
        # 16+
        outM, writeM, address, pc, D = c(o11111, i16, zero, one)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a21), str(pc18), str(from_num(-1))))
        # 17
        outM, writeM, address, pc, D = c(o11111, i16, zero, zero)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a21), str(pc21), str(from_num(-1))))
        # 17+
        outM, writeM, address, pc, D = c(zero16, i17, zero, one)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(o11110), str(one), str(a21), str(pc21), str(from_num(-1))))
        # 18
        outM, writeM, address, pc, D = c(o11111, i17, zero, zero)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(o11109), str(one), str(a2), str(pc22), str(from_num(-1))))
        # 18+
        outM, writeM, address, pc, D = c(o11111, i18, zero, one)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a2), str(pc22), str(from_num(1))))
        # 19
        outM, writeM, address, pc, D = c(o11111, i18, zero, zero)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a2), str(pc23), str(from_num(1))))
        # 19+
        outM, writeM, address, pc, D = c(o11111, i19, zero, one)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a2), str(pc23), str(from_num(1))))
        # 110
        outM, writeM, address, pc, D = c(o11111, i19, zero, zero)
        self.assertEquals((str(outM), str(writeM), str(address), str(pc), str(D)), 
                            (str(outM), str(zero), str(a1000), str(pc24), str(from_num(1))))


"""
|time| inM  |  instruction   |reset| outM  |writeM |addre| pc  |DRegiste|
# |0+  |     0|0011000000111001|  0  |*******|   0   |    0|    0|      0 |
# |1   |     0|0011000000111001|  0  |*******|   0   |12345|    1|      0 |
# |1+  |     0|1110110000010000|  0  |*******|   0   |12345|    1|  12345 |
# |2   |     0|1110110000010000|  0  |*******|   0   |12345|    2|  12345 |
# |2+  |     0|0101101110100000|  0  |*******|   0   |12345|    2|  12345 |
# |3   |     0|0101101110100000|  0  |*******|   0   |23456|    3|  12345 |
# |3+  |     0|1110000111010000|  0  |*******|   0   |23456|    3|  11111 |
# |4   |     0|1110000111010000|  0  |*******|   0   |23456|    4|  11111 |
# |4+  |     0|0000001111101000|  0  |*******|   0   |23456|    4|  11111 |
# |5   |     0|0000001111101000|  0  |*******|   0   | 1000|    5|  11111 |
# |5+  |     0|1110001100001000|  0  |  11111|   1   | 1000|    5|  11111 |
# |6   |     0|1110001100001000|  0  |  11111|   1   | 1000|    6|  11111 |
# |6+  |     0|0000001111101001|  0  |*******|   0   | 1000|    6|  11111 |
# |7   |     0|0000001111101001|  0  |*******|   0   | 1001|    7|  11111 |
# |7+  |     0|1110001110011000|  0  |  11110|   1   | 1001|    7|  11110 |
# |8   |     0|1110001110011000|  0  |  11109|   1   | 1001|    8|  11110 |
# |8+  |     0|0000001111101000|  0  |*******|   0   | 1001|    8|  11110 |
# |9   |     0|0000001111101000|  0  |*******|   0   | 1000|    9|  11110 |
|9+  | 11111|1111010011010000|  0  |*******|   0   | 1000|    9|     -1 |
|10  | 11111|1111010011010000|  0  |*******|   0   | 1000|   10|     -1 |
|10+ | 11111|0000000000001110|  0  |*******|   0   | 1000|   10|     -1 |
|11  | 11111|0000000000001110|  0  |*******|   0   |   14|   11|     -1 |
|11+ | 11111|1110001100000100|  0  |*******|   0   |   14|   11|     -1 |
|12  | 11111|1110001100000100|  0  |*******|   0   |   14|   14|     -1 |
|12+ | 11111|0000001111100111|  0  |*******|   0   |   14|   14|     -1 |
|13  | 11111|0000001111100111|  0  |*******|   0   |  999|   15|     -1 |
|13+ | 11111|1110110111100000|  0  |*******|   0   |  999|   15|     -1 |
|14  | 11111|1110110111100000|  0  |*******|   0   | 1000|   16|     -1 |
|14+ | 11111|1110001100001000|  0  |     -1|   1   | 1000|   16|     -1 |
|15  | 11111|1110001100001000|  0  |     -1|   1   | 1000|   17|     -1 |
|15+ | 11111|0000000000010101|  0  |*******|   0   | 1000|   17|     -1 |
|16  | 11111|0000000000010101|  0  |*******|   0   |   21|   18|     -1 |
|16+ | 11111|1110011111000010|  0  |*******|   0   |   21|   18|     -1 |
|17  | 11111|1110011111000010|  0  |*******|   0   |   21|   21|     -1 |
|17+ | 11111|0000000000000010|  0  |*******|   0   |   21|   21|     -1 |
|18  | 11111|0000000000000010|  0  |*******|   0   |    2|   22|     -1 |
|18+ | 11111|1110000010010000|  0  |*******|   0   |    2|   22|      1 |
|19  | 11111|1110000010010000|  0  |*******|   0   |    2|   23|      1 |
|19+ | 11111|0000001111101000|  0  |*******|   0   |    2|   23|      1 |
|20  | 11111|0000001111101000|  0  |*******|   0   | 1000|   24|      1 |
|20+ | 11111|1110111010010000|  0  |*******|   0   | 1000|   24|     -1 |
|21  | 11111|1110111010010000|  0  |*******|   0   | 1000|   25|     -1 |
|21+ | 11111|1110001100000001|  0  |*******|   0   | 1000|   25|     -1 |
|22  | 11111|1110001100000001|  0  |*******|   0   | 1000|   26|     -1 |
|22+ | 11111|1110001100000010|  0  |*******|   0   | 1000|   26|     -1 |
|23  | 11111|1110001100000010|  0  |*******|   0   | 1000|   27|     -1 |
|23+ | 11111|1110001100000011|  0  |*******|   0   | 1000|   27|     -1 |
|24  | 11111|1110001100000011|  0  |*******|   0   | 1000|   28|     -1 |
|24+ | 11111|1110001100000100|  0  |*******|   0   | 1000|   28|     -1 |
|25  | 11111|1110001100000100|  0  |*******|   0   | 1000| 1000|     -1 |
|25+ | 11111|1110001100000101|  0  |*******|   0   | 1000| 1000|     -1 |
|26  | 11111|1110001100000101|  0  |*******|   0   | 1000| 1000|     -1 |
|26+ | 11111|1110001100000110|  0  |*******|   0   | 1000| 1000|     -1 |
|27  | 11111|1110001100000110|  0  |*******|   0   | 1000| 1000|     -1 |
|27+ | 11111|1110001100000111|  0  |*******|   0   | 1000| 1000|     -1 |
|28  | 11111|1110001100000111|  0  |*******|   0   | 1000| 1000|     -1 |
|28+ | 11111|1110101010010000|  0  |*******|   0   | 1000| 1000|      0 |
|29  | 11111|1110101010010000|  0  |*******|   0   | 1000| 1001|      0 |
|29+ | 11111|1110001100000001|  0  |*******|   0   | 1000| 1001|      0 |
|30  | 11111|1110001100000001|  0  |*******|   0   | 1000| 1002|      0 |
|30+ | 11111|1110001100000010|  0  |*******|   0   | 1000| 1002|      0 |
|31  | 11111|1110001100000010|  0  |*******|   0   | 1000| 1000|      0 |
|31+ | 11111|1110001100000011|  0  |*******|   0   | 1000| 1000|      0 |
|32  | 11111|1110001100000011|  0  |*******|   0   | 1000| 1000|      0 |
|32+ | 11111|1110001100000100|  0  |*******|   0   | 1000| 1000|      0 |
|33  | 11111|1110001100000100|  0  |*******|   0   | 1000| 1001|      0 |
|33+ | 11111|1110001100000101|  0  |*******|   0   | 1000| 1001|      0 |
|34  | 11111|1110001100000101|  0  |*******|   0   | 1000| 1002|      0 |
|34+ | 11111|1110001100000110|  0  |*******|   0   | 1000| 1002|      0 |
|35  | 11111|1110001100000110|  0  |*******|   0   | 1000| 1000|      0 |
|35+ | 11111|1110001100000111|  0  |*******|   0   | 1000| 1000|      0 |
|36  | 11111|1110001100000111|  0  |*******|   0   | 1000| 1000|      0 |
|36+ | 11111|1110111111010000|  0  |*******|   0   | 1000| 1000|      1 |
|37  | 11111|1110111111010000|  0  |*******|   0   | 1000| 1001|      1 |
|37+ | 11111|1110001100000001|  0  |*******|   0   | 1000| 1001|      1 |
|38  | 11111|1110001100000001|  0  |*******|   0   | 1000| 1000|      1 |
|38+ | 11111|1110001100000010|  0  |*******|   0   | 1000| 1000|      1 |
|39  | 11111|1110001100000010|  0  |*******|   0   | 1000| 1001|      1 |
|39+ | 11111|1110001100000011|  0  |*******|   0   | 1000| 1001|      1 |
|40  | 11111|1110001100000011|  0  |*******|   0   | 1000| 1000|      1 |
|40+ | 11111|1110001100000100|  0  |*******|   0   | 1000| 1000|      1 |
|41  | 11111|1110001100000100|  0  |*******|   0   | 1000| 1001|      1 |
|41+ | 11111|1110001100000101|  0  |*******|   0   | 1000| 1001|      1 |
|42  | 11111|1110001100000101|  0  |*******|   0   | 1000| 1000|      1 |
|42+ | 11111|1110001100000110|  0  |*******|   0   | 1000| 1000|      1 |
|43  | 11111|1110001100000110|  0  |*******|   0   | 1000| 1001|      1 |
|43+ | 11111|1110001100000111|  0  |*******|   0   | 1000| 1001|      1 |
|44  | 11111|1110001100000111|  0  |*******|   0   | 1000| 1000|      1 |
|44+ | 11111|1110001100000111|  1  |*******|   0   | 1000| 1000|      1 |
|45  | 11111|1110001100000111|  1  |*******|   0   | 1000|    0|      1 |
|45+ | 11111|0111111111111111|  0  |*******|   0   | 1000|    0|      1 |
|46  | 11111|0111111111111111|  0  |*******|   0   |32767|    1|      1 |
"""


if __name__ == "__main__":
    unittest.main(module='test_computer')