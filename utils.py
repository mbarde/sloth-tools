from datetime import datetime

import json
import time


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


def utc2local_time(utc_hour, utc_minute):
    ''' (UTC hour, UTC minute) -> (local hour, local minute)
        we need to create a datetime object since timezone offset
        depends on actual date because of daylight saving times
    '''
    now = datetime.now()
    utc_datetime = now.replace(hour=utc_hour, minute=utc_minute)
    local_datetime = utc2local_datetime(utc_datetime)
    return (local_datetime.hour, local_datetime.minute)


def utc2local_datetime(utc):
    ''' UTC datetime -> local utc_datetime
    '''
    epoch = time.mktime(utc.timetuple())
    offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
    return utc + offset


def getSunsetTime(longitude, latitude):
    from sun import Sun
    coords = {'longitude': 7.56, 'latitude': 50.356}
    sun = Sun()
    sunset = sun.getSunsetTime(coords)
    return utc2local_time(sunset['hr'], sunset['min'])
