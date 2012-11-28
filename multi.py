from bit import Bit

import math

class Multi:
    "TODO -- negative Multibit values are not handled properly"
    
    def __init__(self, bit_list):
        "Multi is a list of Bits"
        self.value = [bit for bit in bit_list]

    def __len__(self):
        return len(self.value)

    def __str__(self):
        return ''.join(str(bit) for bit in self.value)

    def __iter__(self):
        for bit in self.value:
            yield bit

    def __getitem__(self, index):
        return self.value[index]

    def __lt__(self, mult):
        if self.value < mult.value:
            return True
        return False

    def __le__(self, mult):
        if self.value <= mult.value:
            return True
        return False

    def __gt__(self, mult):
        if self.value > mult.value:
            return True
        return False

    def __ge__(self, mult):
        if self.value >= mult.value:
            return True
        return False
    def __eq__(self, mult):
        if self.value == mult.value:
            return True
        return False

    def __ne__(self, mult):
        if self.value != mult.value:
            return True
        return False

    def to_decimel(self):
        "Converts a Multi instance to a decimel representation"
        return sum([(bit * 2**i) for i, bit in enumerate(reversed(self.value))])

    def from_num(self):
        "Enables construction of a Multi instance using a number or binary number"
        try:
            bnum = bin(self)
        except TypeError:
            bnum = self
        b = bnum.index('b') + 1

        return Multi([Bit(int(digit)) for digit in bnum[b:]])

    def pad_multi(self, mult):
        "Takes two Multi arrays and pads the shorter one with Bit(0) -- only works for positive numbers"
        if not (len(self) - len(mult)):
            return (self, mult)
        longest = Multi(max(self, mult, key=len))
        shortest = Multi(min(self, mult, key=len))
        diff = len(longest) - len(shortest)
        for i in range(diff):
            shortest.value.insert(0, Bit(0))
        assert len(longest) == len(shortest)

        if longest == self:
            return (longest, shortest)
        return (shortest, longest)

    def pad_to_digits(self, digits, *mult):
        "Takes two Multi arrays and pads them to a specified number of digits"
        print self, [str(i) for i in mult]
        base = Multi([Bit(0)])
        m = [Multi(m) for m in mult]
        m.insert(0, Multi(self))
        print "m", [str(i) for i in m]
        pad_m = [base.pad_multi(instance) for instance in m]
        print "pad_m", [str(i) for j in pad_m for i in j]
        if len(pad_m[0]) >= digits:
            return (m)
        diff = digits - len(pad_m[0])
        for i in range(diff):
            for instance in m:
                instance.value.insert(0, Bit(0))
        return (m)
 
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

    def multimux(self, mult, sel):
        "Takes two Multi instances and a 1-Bit sel and returns m1 if sel = 0 and m2 if sel = 1"
        a, b = self.pad_multi(mult)
        return Multi([pair[0].mux(pair[1], sel) for pair in zip(a.value, b.value)])

    def or_multiway(self):
        "Iterates through a Multi instance and returns Bit(1) if any bits = 1, and Bit(0) if all bits = 0"
        base = Bit(0)
        for bit in self:
            base = (base | bit)
        return base

    @staticmethod
    def multimux_multiway(sel, *m_list):
        "Takes a variable number of Multi instances (must be a power of two) and returns the Multi instance indicated by the selector"
        log = int(math.log(len(m_list), 2))
        assert len(sel) == log, "sel must be {0} bits".format(log)
        assert len(m_list) in [2**i for i in range(16)], "The list of variables must be a power of two"

        def reduce_winner(sel, winner_list):
            if len(winner_list) == 1:
                return winner_list[0]
            pow_two = int(math.log(len(winner_list), 2))
            curr_sel = sel[-pow_two]
            return reduce_winner(sel, [winner_list[i].multimux(winner_list[i + pow_two], curr_sel) 
                                        for i, m in enumerate(winner_list) 
                                        if (i + pow_two) < len(winner_list)])

        return Multi(reduce_winner(sel, m_list))

    def dmux_multiway(self, sel):
        "Takes an input and a selector and returns a list of Bits where the sel Bit = input, and all others Bits = 0"
        num_outputs = 2**len(sel)

        def expand_winner(winner_list, s):
            if len(winner_list) == num_outputs:
                return winner_list
            if len(winner_list) == 1:
                index = 0
            else:
                index = int(math.log(len(winner_list), 2))
            winners = [Bit.dmux(winner, s[index]) for winner in winner_list] # Split winners using dmux
            winners = [instance for sublist in winners for instance in sublist] # Collapse list
            return expand_winner(winners, s)

        return expand_winner(self, sel)