from bit import Bit, dmux, mux
from multi import Multi, multimux, dmux_multiway, multimux_multiway, pad_to_digits, pad_multi
from ALU import half_adder, full_adder, add_multi, inc, alu
from sequential import SR, FF, DFF, SingleRegister, Register, RAM, RAM8, RAM64, RAM512, RAM4K, RAM16K, PC

class CPU(object):
    m_zero = Multi([Bit(digit) for digit in '0000000000000000'])
    
    def __init__(self):
        self.D = Register()
        self.A = Register()
        self.PC = PC()
        self.Dval = CPU.m_zero
        self.Aval = CPU.m_zero
        self.PCval = CPU.m_zero
        self.outM = CPU.m_zero
    def __call__(self, inM, instruction, reset, clock):
        # if instruction[0] = 0, instruction is A instruction and should go into the A register
        # if instruction[0] = 0, instruction is C instruction and the ALU output should go into the A register
        A_in = multimux(instruction, self.outM, instruction[0])
        # A_load = 1 if instruction[0] = 0 (A type) 
        # or instruction[0] = 1 AND instruction[10] = 1 (C instruction pointing to the A register)
        # else A_load = 0
        A_load = ~instruction[0] | instruction[10]
        # if instruction[11] = 1, D_load = 1, else d_load = 0
        D_load = instruction[0] & instruction[11]

        # set the A and D registers
        self.Aval = self.A(A_in, A_load, clock)

        # if instruction[12] = 0, ALU should take the output of A register
        # if instruction[12] = 1, ALU should take the output of M register
        ALU_in = multimux(self.Aval, inM, instruction[3])

        # ALU
        self.outM, zr, ng = alu(x=self.Dval, y=ALU_in, zx=instruction[4], nx=instruction[5], 
                            zy=instruction[6], ny=instruction[7], f=instruction[8], no=instruction[9])

        self.Dval = self.D(self.outM, D_load, clock)
        self.Dval = self.D(self.outM, D_load, Bit(0))

        # if i=instruction[0] = 1 and d3 = 1, writeM = 1, else writeM = 0
        writeM = instruction[0] & instruction[12]

        # jump conditions = (j2 AND ng) OR (j1 AND zr) OR (j0 AND po)
        po = ~(zr | ng)
        jump_if = (instruction[13] & ng) | (instruction[14] & zr) | (instruction[15] & po)
        # only jump if instruction[1] (C instruction)
        jump_if = mux(Bit(0), jump_if, instruction[0])

        # PC
        self.PCval = self.PC(multi=self.Aval, load=jump_if, increase=Bit(1), reset=reset, clock=clock)
        return (self.outM, writeM, Multi(self.Aval[1:]), Multi(self.PCval[1:]), self.Dval)
