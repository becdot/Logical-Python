Logical-Python
==============

A Python implementation of the logic hardware defined in [The Elements of Computing Systems](http://www.nand2tetris.org).  All functions (except a few helper functions) are defined in terms of nand (not(and)), which is considered a primitive and defined using Python built-ins.

There are two basic classes, Bit and Multi, which are used to represent a single bit (1 or 0) or a list of bits, respectively.  Bitwise operators are overloaded on both of these classes (and (&), or (|), invert (~)) so that Bit or Multi instances can be easily compared.  Additional classes, including Registers and RAM, are defined in sequential.py to form clocked objects that can remember their state (essential for building computer memory).  

####Truth tables for the Bit class:
```
# and
0 & 0 == 0
0 & 1 == 0
1 & 0 == 0
1 & 1 == 1

# or
0 | 0 == 0
0 | 1 == 1
1 | 0 == 1
1 | 1 == 1

# invert
# this is different than the built-in Python implementation, which uses the twos-complement method
# so ~0 == -1, ~1 == -2.  Because the Bit class only operates on 0 or 1, ~ is equivalent to logical not
~0 == 1
~1 == 0
```

####Truth tables for the Multi class
```
zero, one = Bit(0), Bit(1)
m1 = Multi([zero, one, zero, zero, zero]) # eight
m2 = Multi([zero, zero, one, one, zero]) # six

# and
m1 & m2 == Multi([zero, zero, zero, zero, zero]) # zero
# or
m1 | m2 == Multi([zero, one, one, one, zero]) # fourteen
# invert (using the twos-complement method for representing signed numbers)
~m2 == Multi([one, one, zero, zero, one]) #negative seven 
```