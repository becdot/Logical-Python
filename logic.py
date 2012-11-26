import math

# To-do:
### 1. Figure out how to represent negative binary values
###    - pos and neg subclass of Multi?


class Bit:
    """A single-bit class, where bit = 0 or 1
    Operators are overloaded and defined in terms of nand"""

    def __init__(self, value):
        "Initialise Bit with a value or either 1 or 0"
        assert value in [0, 1], "Bit must be either a 1 or 0!"
        self.value = int(value)

    def __str__(self):
        return str(self.value)

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

    @staticmethod
    def mux(a, b, sel):
        "If sel = 0, returns a; if sel = 1, returns b"
        return (a & ~sel | (b & sel))  

    @staticmethod
    def dmux(a, sel):
        "If sel = 0, returns (a=input, b=0); if sel = 1, returns (a=0, b=input)"
        return ((a & ~sel), (a & sel))

class Multi:
    "TODO -- negative Multibit values are not handled properly"
    
    def __init__(self, bit_list):
        "Multi is a list of Bits, with an optional parameter for a negative value"
        self.value = [bit for bit in bit_list]

    def __len__(self):
        return len(self.value)

    def __str__(self):
        return ''.join(str(bit) for bit in self.value)

    def __iter__(self):
        for bit in self.value:
            yield bit

    def __getitem__(self, key):
        return self.value[key]

    def to_decimel(self):
        sum = 0
        for i, bit in enumerate(reversed(self.value)):
            sum += (bit * 2**i)
        return sum

    @staticmethod
    def from_num(num):
        "Enables construction of a Multi instance using a number or binary number"
        try:
            bnum = bin(num)
        except TypeError:
            bnum = num
        b = bnum.index('b') + 1

        return Multi([Bit(int(digit)) for digit in bnum[b:]])

    def pad_multi(self, m1):
        "Takes two Multi arrays and pads the shorter one with Bit(0) -- only works for positive numbers"
        "TODO - Modify this so that it does not change the underlying values"
        if not (len(self) - len(m1)):
            return (self, m1)
        longest = max(self, m1, key=len)
        shortest = min(self, m1, key=len)
        diff = len(longest) - len(shortest)
        for i in range(diff):
            shortest.value.insert(0, Bit(0))
        assert len(longest) == len(shortest)
        return (longest, shortest)
 
    def __and__(self, mult):
        "Overloads the & operator so out[0] = (a[0] & b[0]), etc..."
        m1, m2 = self.pad_multi(mult)
        return Multi([(pair[0] & pair[1]) for pair in zip(m1.value, m2.value)])

    def __invert__(self):
        "Overloads the ~ operator so that out[0] = ~in[0], out[1] = ~in[1] etc..."
        return Multi([~bit for bit in self.value])

    def __or__(self, mult):
        "Overloads the | operator so that out[0] = (a[0] | b[0]), etc"
        m1, m2 = self.pad_multi(mult)
        return Multi([(pair[0] | pair[1]) for pair in zip(m1.value, m2.value)])

    @staticmethod
    def multimux(m1, m2, sel):
        "Takes two Multi instances and a 1-Bit sel and returns m1 if sel = 0 and m2 if sel = 1"
        a, b = Multi.pad_multi(m1, m2)
        return Multi([((pair[0] & ~sel) | (pair[1] & sel)) for pair in zip(a.value, b.value)])

    @staticmethod
    def multior_multiway(m1):
        "Iterates through a Multi instance and returns Bit(1) if any bits = 1, and Bit(0) if all bits = 0"
        base = Bit(0)
        for bit in m1:
            base = (base | bit)
        return base

    @staticmethod
    def multimux_multiway(sel, *m_list):
        log = int(math.log(len(m_list), 2))
        assert len(sel) == log, "sel must be {0} bits".format(log)

        def reduce_winner(winner_list, sel):
            if len(winner_list) == 1:
                return winner_list[0]
            pow_two = int(math.log(len(winner_list), 2))
            curr_sel = sel[-pow_two]
            return reduce_winner(
                [Multi.multimux(m1=winner_list[i], m2=winner_list[i + pow_two], sel=curr_sel) 
                            for i, m in enumerate(winner_list) if (i + pow_two) < len(winner_list)], 
                sel)


        return reduce_winner(m_list, sel)







