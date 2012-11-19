# and, not, or and xor are already defined

def test_bit_input(num, bit_len):
    # bin(num) = 0bnum == # binary bits + 2
    if len(bin(num)) == bit_len + 2:
        return True
    return False

def nand(a, b):
    assert (test_bit_input(a, 1) and test_bit_input(b, 1))

    return not(a&b)

def mux(a, b, sel):
    assert (test_bit_input(a, 1) and test_bit_input(b, 1) and test_bit_input(sel, 1))

    return (a and not sel) or (b and sel)

def dmux(input, sel):
    assert (test_bit_input(input, 1) and test_bit_input(sel, 1))

    x, y = (input and not sel), (input and sel)
    return (x, y)

