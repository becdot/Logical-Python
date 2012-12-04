from bit import Bit

zero = Bit(0)
one = Bit(1)

class SR:
    """Implements an SR gate(s, r) whereby:
        SR(0, 0) -> Q (hold pattern)
        SR(0, 1) -> 0 (reset)
        SR(1, 0) -> 1 (set)
        SR(1, 1) -> not allowed
    self.q and self.nq are set to arbitrary numbers because the loop pattern of the SR gate 
    ensures that they will change as appropriate"""

    def __init__(self):
        self.q = zero
        self.nq = one
    def __call__(self, s, r):
        q1 = ~(r | self.nq)
        nq1 = ~(s | self.q)
        self.q = ~(r | nq1)
        self.nq = ~(s | q1)
        return self.q

class FF:
    """Implements a flip flop whereby:
        FF(0, 0) -> Q (hold)
        FF(0, 1) -> 0 (reset)
        FF(1, 0) -> Q (hold)
        FF(1, 1) -> 1 (set)
    It is also implemented in such a way that SR can never be called with the disallowed input"""

    def __init__(self):
        self.sr = SR()
    def __call__(self, data, clock):
        r = clock & ~data
        s = clock & data
        return self.sr(s, r)

class DFF:
    "Implements a DFF gate where two FF's are chained asynchronously together so that slave -> master output of previous cycle"
    def __init__(self):
        self.master = FF()
        self.slave = FF()
    def __call__(self, data, clock):
        master_q = self.master(data, clock)
        slave_q = self.slave(master_q, ~clock)
        return slave_q

