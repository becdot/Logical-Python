# TODO:
### 1. Figure out how to represent negative binary values
###    - pos and neg subclass of Multi?
### 2. Enable multidmux (currently can only accept a one-bit input)?
### 3. Take out unnecessary functions (comparisons?)


class Bit:
    """A single-bit class, where bit = 0 or 1
    Operators are overloaded and defined in terms of nand"""

    def __init__(self, value):
        "Initialise Bit with a value or either 1 or 0"
        assert int(value) in [0, 1], "Bit must be either a 1 or 0!"
        self.value = int(value)

    def __str__(self):
        return str(self.value)

    def __int__(self):
        return int(self.value)

    def __mul__(self, other):
        return int(self.value * other)

    def __nonzero__(self):
        "Enables truth comparison of Bit instances"
        return self.value

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

    def mux(self, bit, sel):
        "If sel = 0, returns a; if sel = 1, returns b"
        return Bit(self & ~sel) | Bit(bit & sel)

    def dmux(self, sel):
        "If sel = 0, returns [a=input, b=0]; if sel = 1, returns [a=0, b=input]"
        return [Bit(self & ~sel), Bit(self & sel)]