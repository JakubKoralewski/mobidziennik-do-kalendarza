"""
    By Jakub Koralewski
    Gets calendar from get_mobidziennik_lessons.py and saves to .ics.
    https://icalendar.org/validator.html
    """
from get_mobidziennik_lessons import calendar
from icalendar import Calendar, Event
from datetime import datetime, date, timedelta
import pytz
import os
import random
import string

c = Calendar()
e = Event()

c.add('prodid', '-//JakubKoralewski//github.com//')
c.add('version', '2.0')


def randomWord(length):
    letters = string.ascii_letters
    return ''.join((random.choice(letters)) for i in range(length))


for i in calendar.keys():
    e = Event()
    name = calendar[i]['name']
    dayNum = int(calendar[i]['dayNum'])
    startTime = calendar[i]['startTime']
    endTime = calendar[i]['endTime']
    classroom = calendar[i]['classroom']
    info = calendar[i]['info']
    todaysDate = datetime.today()
    todaysDay = date.isoweekday(todaysDate)
    uid = str(todaysDate).replace(" ", "") + \
        str(randomWord(8))+'@github.com'

    # split 14:36 into 14 and 36
    startHour = int(startTime[0:2])
    startMinutes = int(startTime[3:6])
    endHour = int(endTime[0:2])
    endMinutes = int(endTime[3:6])

    # get the day from which to start adding
    mondayDelta = todaysDay - 1
    firstMonday = todaysDate - timedelta(days=mondayDelta)

    # print(firstMonday)
    summary = '{} - {}'.format(name, classroom)
    crlf = chr(13)+chr(10)
    description = '{}\r\nLekcja: {}\r\nKlasa: {}'.format(
        info, name, classroom)

    year = date.today().year
    month = date.today().month
    day = firstMonday + timedelta(days=dayNum)
    day = day.day
    print('day: {}'.format(day))

    e.add('summary', summary)
    e.add('description', description)
    e.add('dtstart', datetime(year, month, day, startHour, startMinutes))
    e.add('dtend', datetime(year, month, day, endHour, endMinutes))
    e.add('uid', uid)
    e.add('dtstamp', todaysDate)
    if month >= 9:
        e.add('rrule', {'freq': 'weekly', 'until': datetime(year+1, 6, 30)})
    else:
        e.add('rrule', {'freq': 'weekly', 'until': datetime(year, 6, 30)})

    c.add_component(e)
    print(e)

with open('calendar.ics', 'wb') as calendar:
    calendar.write(c.to_ical())
