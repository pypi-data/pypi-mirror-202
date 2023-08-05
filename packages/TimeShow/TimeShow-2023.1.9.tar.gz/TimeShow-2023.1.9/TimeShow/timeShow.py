from PyQt6.QtCore import *
import os


#How to Import:input "import TimeShow.timeShow"
#Usage:TimeShow.timeShow.[name]

class NetworkNotConnected(Exception):
    pass

def RunSpyderGUI():
    os.system(r"spyder %run .\\timeShow.py")

def ChooseDateFormat(format):
    return 'Qt.DateFormat.' + format

def JudgeWhetherToConnectWLAN():
    if not os.system('ping baidu.com -n 1'):
        return True
    else:
        return False

def raiseErrorNoWLAN():
    if not JudgeWhetherToConnectWLAN():
        raise NetworkNotConnected('NetWork Not Connected.')

class ShowDate_Day_Time:
    def ShowDay():
        raiseErrorNoWLAN()
        now = QDate.currentDate()
        print(now.toString(eval(ChooseDateFormat())))

    def ShowDateTime():
        raiseErrorNoWLAN()
        datetime = QDateTime.currentDateTime()
        print(datetime.toString(eval(ChooseDateFormat())))

    def showTime():
        raiseErrorNoWLAN()
        time = QTime.currentTime()
        print(time.toString(eval(ChooseDateFormat())))

    def showUTCDateTime():
        raiseErrorNoWLAN()
        now = QDateTime.currentDateTime()
        print(now.toUTC().toString(eval(ChooseDateFormat())))

    def showDaysDifference(n):
        raiseErrorNoWLAN()
        difference = QDate(n)
        now = QDate.currentDate()
        print(now.daysTo(difference))
    class ShowDaysIn:
        def showDaysInMonth(y,m):
            raiseErrorNoWLAN()
            print(QDate(y,m,1).daysInMonth())

        def showDaysInYear(y):
            raiseErrorNoWLAN()
            print(QDate(y,1,1).daysInYear())

    def showUnixDate():
        raiseErrorNoWLAN()
        print(QDateTime.fromSecsSinceEpoch(QDateTime.currentDateTime().toSecsSinceEpoch()).toString(eval(ChooseDateFormat())))

    def showJulianDay():
        raiseErrorNoWLAN()
        print(QDate.currentDate().toJulianDay())

    def showTimeZone():
        raiseErrorNoWLAN()
        print(QDateTime.currentDateTime().timeZoneAbbreviation())

def JudgeisDaylightTime():
    raiseErrorNoWLAN()
    if QDateTime.currentDateTime().isDaylightTime():
        print('The current date falls into DST time')
    else:
        print('The current date does not fall into DST time')
