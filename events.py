from random import randint
from utils import addOffsetToTimeTuple
from utils import getSunriseTime
from utils import getSunsetTime
from utils import int2bits
from utils import sqlrow2dict

import db
import threading
import time


class EventTable():

    def __init__(self, app, config, switchFunction, interval):
        self.app = app
        self.config = config
        self.events = []
        self.interval = interval
        self.switchFunction = switchFunction

        now = time.localtime()
        self.lastCheckTimeStr = self.getTimeStr(now.tm_hour, now.tm_min)
        self.loadFromDB()
        self.checkEvents()

    def loadFromDB(self):
        conn = db.get_db()
        sql = 'SELECT * FROM event'
        self.events = conn.execute(sql).fetchall()
        self.events = [sqlrow2dict(event) for event in self.events]
        self.computeDynamicTimes()
        # self.printEvents()

    # @TOOO: dynamic events need to be re-computed at least one time per day
    def computeDynamicTimes(self):
        for event in self.events:
            if event['mode'] == 1:
                sunrise = getSunriseTime(
                    self.config['longitude'],
                    self.config['latitude'])
                (event['hour'], event['minute']) = addOffsetToTimeTuple(
                    sunrise, event['sunriseOffset'])
            if event['mode'] == 2:
                sunset = getSunsetTime(
                    self.config['longitude'],
                    self.config['latitude'])
                (event['hour'], event['minute']) = addOffsetToTimeTuple(
                    sunset, event['sunsetOffset'])
            if event['randomOffset'] != 0:
                randomOffset = randint(-event['randomOffset'], event['randomOffset'])
                (event['hour'], event['minute']) = addOffsetToTimeTuple(
                    (event['hour'], event['minute']), randomOffset)

    def checkEvents(self):
        with self.app.app_context():
            now = time.localtime()
            nowTimeStr = self.getTimeStr(now.tm_hour, now.tm_min)
            for event in self.events:
                eventWeekdays = int2bits(event['weekdays'])
                if eventWeekdays[now.tm_wday] == 0:
                    continue
                eventTimeStr = self.getTimeStr(event['hour'], event['minute'])
                if (eventTimeStr > self.lastCheckTimeStr and eventTimeStr <= nowTimeStr):
                    self.performEvent(event)
            self.lastCheckTimeStr = nowTimeStr
            self.startTimer()

    def getTimeStr(self, hour, minute):
        hourStr = str(hour).zfill(2)
        minuteStr = str(minute).zfill(2)
        return hourStr + minuteStr

    def performEvent(self, event):
        print('Timed event for node {0}: Switch to {1}'.format(
            event['nodeIdRef'], event['switchOn']))
        stateId = 0
        if event['switchOn']:
            stateId = 1
        self.switchFunction(event['nodeIdRef'], stateId)

    def startTimer(self):
        threading.Timer(self.interval, self.checkEvents).start()

    # for debugging purposes
    def printEvents(self):
        for event in self.events:
            for key in event.keys():
                print('{0}: {1}'.format(key, event[key]))
            print('')
