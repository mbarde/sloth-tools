from sun import Sun
from datetime import datetime
import time


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


coords = {'longitude': 7.56, 'latitude': 50.356}

sun = Sun()

# Sunrise time UTC (decimal, 24 hour format)
print(sun.getSunriseTime(coords))

# Sunset time UTC (decimal, 24 hour format)
sunset = sun.getSunsetTime(coords)
print(utc2local_time(sunset['hr'], sunset['min']))
