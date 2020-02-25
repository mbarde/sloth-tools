def bits2int(bitlist):
    out = 0
    for bit in bitlist:
        out = (out << 1) | bit
    return out


def int2bits(n):
    if not isinstance(n, int):
        return [0] * 7
    return [1 if digit == '1' else 0 for digit in bin(n)[2:]]


def weekdays2bits(weekdaysDict):
    bitlist = []
    weekdays = getWeekdays()
    for day in weekdays:
        if day in weekdaysDict:
            bitlist.append(1)
        else:
            bitlist.append(0)
    return bitlist


def getWeekdays():
    return ['monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday']


def sqlrow2dict(row):
    return dict(zip(row.keys(), row))
