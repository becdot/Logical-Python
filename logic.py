class Logic:    

    ### Test or helper functions
    def test_bit_input(self, num, bit_len):
        "Returns true if the number matches its required bit length"
        if (num == 0 or num == 1) and bit_len != 1:
            return False
        if num > 0 and num.bit_length() != bit_len:
            return False
        return True

    # def num_to_bin(self, num):
    #     "Returns the binary representation of a number (8 -> '0b1000' or '0b1' -> '0b1')"
    #     if 'b' in str(num):
    #         return str(num)
    #     else:
    #         return bin(num)

    # def num_to_right_bits(self, num, bits):
    #     "Given a number, returns that number as the length of bits specified (2, 4 -> '0b0010')"
    #     num = num_to_bin(num)
    #     first = num[:num.index('b') + 1]
    #     last = num[num.index('b') + 1:]
    #     bits_to_add = bits - len(last)

    #     for i in range(bits_to_add):
    #         last = '0' + last
    #     return first + last


    ### Logic gates

    # Chapter 1
    def nand(self, a, b):
        "Returns not(a and b)"
        assert (self.test_bit_input(a, 1) and self.test_bit_input(b, 1))

        return not(a and b)

    def __invert__(self):
        "Returns not(a) -- DIFFERENT than the original invert, which worked bitwise"
        return 2

    def test_invert(self):
        print "not 0 ==", ~0
        print "not 1 ==", ~1



x = Logic()
x.test_invert()


    # New functions, in terms of nand

    # def __and__(self, a, b):
    #     "Overloads the & operator, defined in terms of nand"
    #     c = self.nand(a, b)
    #     return self.nand(c, c)
    # 
    # def __or__(self, a, b):
    #     "Overloads the | operator, defined in terms of nand"
    #     return self.nand(~a, ~b)
    # 
    # def __xor__(self, a, b):
    #     "Overloads the ^ operator, defined in terms of nand"
    #     x = ~(a & (~b))
    #     y = ~(b & (~a))
    #     return self.nand(x, y)
    # 
    # def mux(self, a, b, sel):
    #     "If sel = 0, returns a; if sel = 1, returns b"
    #     assert (self.test_bit_input(a, 1) and self.test_bit_input(b, 1) and self.test_bit_input(sel, 1))
    # 
    #     return (a & ~sel | (b & sel))  
    # 
    # def dmux(self, a, sel):
    #     "If sel = 0, returns (a=input, b=0); if sel = 1, returns (a=0, b=input)"
    #     assert (self.test_bit_input(a, 1) and self.test_bit_input(sel, 1))
    # 
    #     x, y = (a & ~sel, (a & sel))
    #     return (x, y)




    # Functions defined pythonically

    # def mux(a, b, sel):
    #     "If sel = 0, returns a; if sel = 1, returns b"
    #     assert (test_bit_input(a, 1) and test_bit_input(b, 1) and test_bit_input(sel, 1))

    #     return (a and not sel) or (b and sel)

    # def dmux(input, sel):
    #     "if sel = 0, returns (a=input, b=0); if sel = 1, returns (a=0, b=input)"
    #     assert (test_bit_input(input, 1) and test_bit_input(sel, 1))

    #     x, y = (input and not sel), (input and sel)
    #     return (x, y)

    # def and16(a, b):
    #     "Returns a 16-bit number where out[0] = (a[0] and b[0]), etc.."
    #     a, b = int(num_to_bin(a), 2), int(num_to_bin(b), 2)
    #     out = a & b
    #     return num_to_right_bits(out, 16)

    # def not16(a):
    #     "Returns a 16-bit number where out[0] = not a[0]"
    #     a = num_to_bin(a)
    #     out = ~int(a, 2)
    #     return num_to_right_bits(out, 16)

    # def or16(a, b):
    #     "Returns a 16-bit number where out[0] = (a[0] or b[0]), etc.."
    #     a, b = int(num_to_bin(a), 2), int(num_to_bin(b), 2)
    #     out = a | b
    #     return num_to_right_bits(out, 16)

    # def ormultiway(a):
    #     "Returns True if any bits in a are 1, else returns False"
    #     a = int(num_to_bin(a), 2)
    #     if a == 0:
    #         return False
    #     return True



