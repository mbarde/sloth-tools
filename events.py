import db
import threading
import time


class EventTable():

    def __init__(self, app, switchFunction, interval):
        self.app = app
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

    def checkEvents(self):
        with self.app.app_context():
            now = time.localtime()
            nowTimeStr = self.getTimeStr(now.tm_hour, now.tm_min)
            for event in self.events:
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
