def bits2int(bitlist):
    out = 0
    for bit in bitlist:
        out = (out << 1) | bit
    return out


def int2bits(n):
    return [1 if digit == '1' else 0 for digit in bin(n)[2:]]
