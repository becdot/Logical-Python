cdef class Bit:
    """A single-bit class, where bit = 0 or 1
    Operators are overloaded and defined in terms of nand"""

    cdef public int value

    def __init__(self, val):
        "Initialise Bit with a value or either 1 or 0"
        self.value = int(val)

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

one = Bit(1)
zero = Bit(0)

def nand(Bit bit1, Bit bit2):
    "nand = not(a and b), operating on two instances of bit.Bit"
    cdef int val1, val2
    val1, val2 = bit1.value, bit2.value
    return zero if (val1 and val2) else one

def mux(Bit bit1, Bit bit2, sel):
    "If sel = 0, returns a; if sel = 1, returns b"
    return (bit1 & ~sel) | (bit2 & sel)

def dmux(Bit bit, Bit sel):
    "If sel = 0, returns [a=bit, b=0]; if sel = 1, returns [a=0, b=bit]"
    return [(bit & ~sel), (bit & sel)]