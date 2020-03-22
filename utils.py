import json


def bits2int(bitlist):
    out = 0
    for bit in bitlist:
        out = (out << 1) | bit
    return out


def int2bits(n):
    weekdaysCount = 7
    if not isinstance(n, int):
        return [0] * weekdaysCount
    bits = [1 if digit == '1' else 0 for digit in bin(n)[2:]]
    # make sure to return always list with 7 items:
    bits = [0] * (weekdaysCount - len(bits)) + bits
    return bits


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


def config2dict(filename):
    with open(filename, 'r') as configFile:
        data = configFile.read()
    obj = json.loads(data)
    return obj
