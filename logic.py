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

    def nott(self, a):
        "Returns not(a)"
        return self.nand(a, a)

    def __and__(self, a, b):
        "Overloads the & operator, defined in terms of nand"
        c = self.nand(a, b)
        return self.nand(c, c)

    def __or__(self, a, b):
        "Overloads the | operator, defined in terms of nand"
        x = self.nand(a, a)
        y = self.nand(b, b)
        return self.nand(x, y)

    def __xor__(self, a, b):
        "Overloads the ^ operator, defined in terms of nand"
        notb = self.nand(b, b)
        nota = self.nand(a, a)
        a_and_notb = self.nand(self.nand(a, notb), self.nand(a, notb))
        b_and_nota = self.nand(self.nand(b, nota), self.nand(b, nota))
        not_aandnotb = self.nand(a_and_notb, a_and_notb)
        not_bandnota = self.nand(b_and_nota, b_and_nota)
        return self.nand(not_aandnotb, not_bandnota)

    def mux(self, a, b, sel):
        "If sel = 0, returns a; if sel = 1, returns b"
        assert (self.test_bit_input(a, 1) and self.test_bit_input(b, 1) and self.test_bit_input(sel, 1))

        return (a & self.nott(sel) | (b & sel))  

    def dmux(self, a, sel):
        "If sel = 0, returns (a=input, b=0); if sel = 1, returns (a=0, b=input)"
        assert (self.test_bit_input(a, 1) and self.test_bit_input(sel, 1))

        x, y = (a & self.nott(sel), (a & sel))
        return (x, y)






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



