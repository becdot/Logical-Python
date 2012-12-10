cpdef class Bit:
    """A single-bit class, where bit = 0 or 1
    Operators are overloaded and defined in terms of nand"""

    def __init__(self, int value):
        "Initialise Bit with a value or either 1 or 0"
        assert int(value) in [0, 1], "Bit must be either a 1 or 0!"
        self.value = int(value)

    def __repr__(self):
        return str(self.value)

    def __int__(self):
        return int(self.value)

    def __mul__(self, other):
        return int(self.value * other)

    def __nonzero__(self):
        "Enables truth comparison of Bit instances"
        return self.value

    def __and__(self, Bit num1):
        "Overloads the & operator using the nand function"
        a = nand(self, num1)
        return nand(a, a)

    def __invert__(self):
        "Overloads ~ to return logical not of a bit, instead of bitwise not"
        return nand(self, self)

    def __or__(self, Bit num1):
        "Overloads the | operator using the nand function"
        return nand(~self, ~num1)

    def __xor__(self, Bit num1):
        "Overloads the ^ operator using the nand function"
        first = ~(self & ~num1)
        last = ~(num1 & ~self)
        return nand(first, last)


def nand(Bit bit1, Bit bit2):
    "nand = not(a and b), operating on two instances of bit.Bit"
    cdef int b1, b2
    b1, b2 = bit1.value, bit2.value
    return Bit(not(b1 and b2))

def mux(Bit bit1, Bit bit2, Bit sel):
    "If sel = 0, returns a; if sel = 1, returns b"
    return (bit1 & ~sel) | (bit2 & sel)

def dmux(Bit bit, Bit sel):
    "If sel = 0, returns [a=bit, b=0]; if sel = 1, returns [a=0, b=bit]"
    return [(bit & ~sel), (bit & sel)]
