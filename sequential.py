from bit import Bit, mux
from multi import Multi, multimux, dmux_multiway, multimux_multiway
from ALU import inc

zero = Bit(0)
one = Bit(1)

class SR:
    """Implements an SR gate(s, r) whereby:
        SR(0, 0) -> Q (hold pattern)
        SR(0, 1) -> 0 (reset)
        SR(1, 0) -> 1 (set)
        SR(1, 1) -> not allowed
    self.q and self.nq are set to arbitrary numbers because all inputs will stabilize via the looping pattern"""

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
    It is also implemented in such a way that the SR gate can never be called with the disallowed (1, 1) input"""

    def __init__(self):
        self.sr = SR()
    def __call__(self, data, clock):
        r = clock & ~data
        s = clock & data
        return self.sr(s, r)

class DFF:
    """Implements a DFF gate where the slave -> master output of previous cycle
        Change occurs on the FALLING edge of the clock (i.e. 1 -> 0)"""
    def __init__(self):
        self.master = FF()
        self.slave = FF()
    def __call__(self, data, clock):
        master_q = self.master(data, clock)
        slave_q = self.slave(master_q, ~clock)
        return slave_q

class SingleRegister:
    """if load(t) = 1, out(t + 1) = in(t)
        if load(t) = 0, out(t + 1) = out(t) (no change)
        returns a single bit on the falling edge of the clock"""

    def __init__(self):
        self.dff = DFF()
        self.value = zero
    def __call__(self, bit, load, clock):
        initial_mux = mux(self.value, bit, load)
        self.value = self.dff(initial_mux, clock)
        return self.value

class Register:
    """if load(t) = 1, out(t + 1) = in(t)
        if load(t) = 0, out(t + 1) = out(t) (no change)
        returns a Multibit instance on the falling edge of the clock"""

    def __init__(self):
        self.reg = [SingleRegister() for i in range(16)]
    def __call__(self, multi, load, clock):
        return Multi(pair[0](pair[1], load, clock) for pair in zip(self.reg, multi))


class RAM:
    "Sets up the basic rules for a RAM block, that can be called with the name of a RAM type to build from (e.g. RAM64 -> RAM8)"

    make_from = None

    def __init__(self):
        if not self.make_from:
            raise Exception, "make_from is not defined" 
        self.reg = [self.make_from() for i in range(8)]

    def __call__(self, multi, load, address, clock):
        input_address = Multi(address[-1:-4:-1])
        reg_address = Multi(address[-4:-(len(address) + 1):-1])
        inputs = dmux_multiway(Multi([load]), input_address)
        regs = [Multi(pair[0](multi, pair[1], reg_address, clock)) for pair in zip(self.reg, inputs)]        
        return multimux_multiway(input_address, *regs)

class RAM8(RAM):
    "Block of 8 Registers that inherits from RAM. Takes a 3-bit address"
    make_from = Register

    def __call__(self, multi, load, address, clock):
        inputs = dmux_multiway(Multi([load]), address)
        regs = [Multi(pair[0](multi, pair[1], clock)) for pair in zip(self.reg, inputs)]
        return multimux_multiway(address, *regs)        

class RAM64(RAM):
    "Block of 8 RAM8s that inherits from RAM. Takes a 6-bit address"
    make_from = RAM8

class RAM512(RAM):
    "Block of 8 RAM64s that inherits from RAM. Takes a 9-bit address"
    make_from = RAM64

class RAM4K(RAM):
    "Block of 8 RAM64s that inherits from RAM. Takes a 12-bit address"
    make_from = RAM512

class RAM16K(RAM):
    "Block of 8 RAM4Ks that inherits from RAM. Takes a 14-bit address"
    make_from = RAM4K
    def __call__(self, multi, load, address, clock):
        input_address = Multi(address[-1:-4:-1])
        reg_address = Multi(address[-3:-(len(address) + 1):-1])
        inputs = dmux_multiway(Multi([load]), input_address)
        regs = [Multi(pair[0](multi, pair[1], reg_address, clock)) for pair in zip(self.reg, inputs)]        
        return multimux_multiway(input_address, *regs)


class PC:
    """ if reset(t-1):
            out(t) = 0
        elif load(t-1):
            out(t) = in(t-1)
        elif inc(t-1):
            out(t) = out(t-1) + 1 (integer addition)
        else:
            out(t) = out(t-1)"""

    def __init__(self):
        self.reg = Register()
        self.value = Multi(zero for i in range(16)) # zero
    def __call__(self, multi, load, increase, reset, clock):
        # if load, inc, or reset are set, load should be set for the register
        reg_load = load | increase | reset
        # if inc = 1, return (value + 1), else return value
        if_increase = multimux(self.value, inc(self.value), increase)
        # if load = 1, return multi, else return if_increase
        if_out = multimux(if_increase, multi, load)
        # if reset = 1, return 0, else return if_out
        if_reset = multimux(if_out, Multi(zero for i in range(16)), reset)

        self.value = self.reg(if_reset, reg_load, clock)
        return self.value

