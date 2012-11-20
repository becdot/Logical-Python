class Bit:
    """A single-bit class, where bit = 0 or 1
    Operators are overloaded and defined in terms of nand"""

    def __init__(self, value):
        "Initialise Bit with a value or either 1 or 0"
        assert value in [0, 1], "Bit must be either a 1 or 0!"
        self.value = int(value)

    def __str__(self):
        return str(self.value)

    def __nonzero__(self):
        "Enables truth comparison of Bit instances"
        if self.value:
            return True
        return False

    @staticmethod
    def nand(num1, num2):
        """nand = not(a and b)
        Defined as a static method because belongs logically within Bit, but syntaxtically outside it"""
        return Bit(not(num1.value and num2.value))

    def __and__(self, num1):
        "Overloads the & operator using the nand function"
        a = Bit.nand(self, num1)
        return Bit.nand(a, a)

    def __invert__(self):
        "Overloads ~ to return logical not of a bit, instead of bitwise not"
        return Bit.nand(self, self)

    def __or__(self, num1):
        "Overloads the | operator using the nand function"
        return Bit.nand(~self, ~num1)

    def __xor__(self, num1):
        "Overloads the | operator using the nand function"
        first = ~(self & ~num1)
        last = ~(num1 & ~self)
        return Bit.nand(first, last)

    @staticmethod
    def mux(a, b, sel):
        "If sel = 0, returns a; if sel = 1, returns b"
        return (a & ~sel | (b & sel))  

    @staticmethod
    def dmux(a, sel):
        "If sel = 0, returns (a=input, b=0); if sel = 1, returns (a=0, b=input)"
        return ((a & ~sel), (a & sel))

class Multi:
    
    def __init__(self, bit_list, neg=False):
        "Multi is a list of Bits, with an optional parameter for a negative value"
        self.value = [bit for bit in bit_list]
        self.neg = neg

    def __len__(self):
        return len(self.value)

    def __str__(self):
        return self.binary()

    def binary(self):
        "Turns a list of bits into a python binary representation (e.g. '0b1000')"
        bin_str = ''.join([str(digit) for digit in self.value])
        bin_str = '0b' + bin_str
        if self.neg:
            bin_str = '-' + bin_str
        return bin_str 

    @staticmethod
    def from_num(num):
        "Enables construction of a Multi instance using a number or binary number"
        try:
            bnum = bin(num)
        except TypeError:
            bnum = num
        b = bnum.index('b') + 1

        if bnum.startswith('-'): 
            neg = True
        else:
            neg = False
        return Multi([Bit(int(digit)) for digit in bnum[b:]], neg=neg)
 
    def __and__(self, mult):
        assert len(self) == len(mult), "List lengths do not match: {0} and {1}".format(len(self), len(mult))

        
        return Multi([(pair[0] & pair[1]) for pair in zip(self.value, mult.value)], neg=(self.neg or mult.neg))




