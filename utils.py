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


def getSunriseTime(longitude, latitude):
    from sun import Sun
    coords = {'longitude': longitude, 'latitude': latitude}
    sun = Sun()
    sunset = sun.getSunriseTime(coords)
    return utc2local_time(sunset['hr'], sunset['min'])


def getSunsetTime(longitude, latitude):
    from sun import Sun
    coords = {'longitude': longitude, 'latitude': latitude}
    sun = Sun()
    sunset = sun.getSunsetTime(coords)
    return utc2local_time(sunset['hr'], sunset['min'])


def timetuple2str(time_tuple):
    hourStr = str(time_tuple[0]).zfill(2)
    minuteStr = str(time_tuple[1]).zfill(2)
    return '{0}:{1}'.format(hourStr, minuteStr)


def addOffsetToTimeTuple(timeTuple, offsetInMin):
    offHours = int(offsetInMin / 60)
    offMinutes = offsetInMin - (offHours * 60)
    return (timeTuple[0] + offHours, timeTuple[1] + offMinutes)


def event2str(event, html=False):
    res = ''

    if event['mode'] == 0:
        res = timetuple2str((event['hour'], event['minute']))

    elif event['mode'] == 1:
        if html is True:
            res = '<span title="sunrise">🌅</span>'
        else:
            res = '🌅'
        if event['sunriseOffset'] != 0:
            if html is True:
                tmpStr = '<span class="small"> {0} {1} min.</span>'
            else:
                tmpStr = ' {0} {1} min.'
            if event['sunriseOffset'] > 0:
                res += tmpStr.format('+', str(event['sunriseOffset']))
            else:
                res += tmpStr.format('-', str(event['sunriseOffset']*-1))

    elif event['mode'] == 2:
        if html is True:
            res = '<span title="sunset">🌇</span>'
        else:
            res = '🌇'
        if event['sunsetOffset'] != 0:
            if html is True:
                tmpStr = '<span class="small"> {0} {1} min.</span>'
            else:
                tmpStr = ' {0} {1} min.'
            if event['sunsetOffset'] > 0:
                res += tmpStr.format('+', str(event['sunsetOffset']))
            else:
                res += tmpStr.format('-', str(event['sunsetOffset']*-1))

    if event['randomOffset'] != 0:
        rStr = '(rand. +/- {0} min.)'
        if html is True:
            rStr = '<span title="random offset {0} min." class="small">' + rStr + '</span>'
        res += ' ' + rStr.format(event['randomOffset'])

    if event['switchOn'] == 0:
        switchOnStr = 'off'
    else:
        switchOnStr = 'on'
    res += ' → ' + switchOnStr

    return res


TIMED_EVENT_MODES = {
    'fixed': 0,
    'sunrise': 1,
    'sunset': 2,
}
