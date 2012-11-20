class Bit:
    """A single-bit class, where bit = 0 or 1
    Operators are overloaded and defined in terms of nand"""

    def __init__(self, value):
        assert value in [0, 1], "Bit must be either a 1 or 0!"
        self.value = int(value)

    def __str__(self):
        return str(self.value)

    def __nonzero__(self):
        if self.value:
            return True
        return False

    @staticmethod
    def nand(num1, num2):
        return Bit(not(num1.value and num2.value))

    def __and__(self, num1):
        a = Bit.nand(self, num1)
        return Bit.nand(a, a)

    def __invert__(self):
        return Bit.nand(self, self)

    def __or__(self, num1):
        return Bit.nand(~self, ~num1)

    def __xor__(self, num1):
        first = ~(self & ~num1)
        last = ~(num1 & ~self)
        return Bit.nand(first, last)

# class Multi:
    
#     def __init__(self, num):
#         try:
#             bnum = bin(num)
#         except TypeError:
#             bnum = num
#         b = bnum.index('b') + 1
#         self.value = [Bit(int(digit)) for digit in bnum[b:]]

#         if bnum.startswith('-'): 
#             self.neg = True
#         else:
#             self.neg = False

#     def binary(self):
#         bin_str = ''.join([str(digit) for digit in self.value])
#         bin_str = '0b' + bin_str
#         if self.neg:
#             bin_str = '-' + bin_str
#         return bin_str    
    

#     def __str__(self):
#         return self.binary()


# print Multi(8)
# print int(Multi(8).binary(), 2)
# print Multi(0)
# print Multi(-1)

### Logic function!

def mux(a, b, sel):
    "If sel = 0, returns a; if sel = 1, returns b"

    return (a & ~sel | (b & sel))  

def dmux(a, sel):
    "If sel = 0, returns (a=input, b=0); if sel = 1, returns (a=0, b=input)"

    return ((a & ~sel), (a & sel))

def and16(a, b):
    "Returns a 16-bit number where out[0] = (a[0] and b[0]), etc.."

