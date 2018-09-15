"""
    By Jakub Koralewski.
    Get lessons from mobidziennik and save to a dict/list.
    TO-DO:
    - add special case conditions when zastępstwo, lekcja odwołana
    - use screenshotting in case the styles ever change
"""
from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import re
import config
import pprint
pp = pprint.PrettyPrinter(indent=4)

br = RoboBrowser()
br.open('https://lo2kalisz.mobidziennik.pl/dziennik/')
form = br.get_form()

form['haslo'] = config.PASSWORD
form['login'] = config.USER_NAME

br.submit_form(form)
br.open('https://lo2kalisz.mobidziennik.pl/dziennik/planzajec/?bez-zastepstw=1')


def determineDay(percent):
    percent = str(percent)
    if percent == '0.5':
        return 0
    elif percent == '20.5':
        return 1
    elif percent == '40.5':
        return 2
    elif percent == '60.5':
        return 3
    elif percent == '80.5':
        return 4
    else:
        return 0  # error


""" CASES:
    We need:
    - day of the week,
    - start.TimeTime,
    - end.TimeTime,
    - lessonName,
    - classroomName. #ok

    SPECIAL CASE:
    - 'zastępstwo'
    - 'lekcja odwołana'
    - inside title:
        - &lt; etc.
    """

# select <div class="plansc_cnt">
numOfLessons = i = numOfMatches = 0

calendar = {}
for bigDiv in br.find_all(class_='plansc_cnt_w'):
    numOfLessons += 1
    bigDiv = str(bigDiv)

    # RegEx the left value, ex.: style="width:19%;left:   two digits + (maybe)dot + (maybe) digit       %;"
    percent = re.search(r'style="width:\d\d%;left:(\d{1,2}.?\d?)%;', bigDiv)[1]

    title = re.search(
        r'title="(?P<startTime>\d\d:\d\d) - (?P<endTime>\d\d:\d\d)&lt;br /&gt;(?P<name>.*)&lt;br /&gt;(?P<info>.*) (?P<classroom>\(.*\))"', bigDiv)

    # SPECIAL CASES:
    # title="&lt;small&gt;Lekcja odwołana: Lekcja odwołana&lt;/small&gt;&lt;br /&gt;13:30 - 14:15&lt;br /&gt;informatyka PR&lt;br /&gt;3 e-11/14,3d-15/24,3h-15/16">
    # title="&lt;small&gt;zastępstwo&lt;/small&gt;&lt;br /&gt;10:50 - 11:35&lt;br /&gt;Język angielski&lt;br /&gt;3 d - Rzepiak Alina (Sala_(203))">
    #specialCase = re.search()

    # get start, end, name, classroom, which day it is and additional info
    # unknown error
    try:
        i += 1
        dayNum = determineDay(percent)
        startTime = title[1]
        endTime = title[2]
        name = title[3]
        info = title[4]
        classroom = title[5]
    except TypeError:
        pass

    # this is done for comparing number of tries against succeeded results
    try:
        title[0]
        numOfMatches += 1
    except:
        pass

    # save to dict
    calendar[numOfMatches] = {
        'name': name,
        'dayNum': dayNum,
        'startTime': startTime,
        'endTime': endTime,
        'classroom': classroom,
        'info': info,
    }

    """ print(
        '{title}\nstartTime: "{startTime}", endTime: "{endTime}", name: "{name}", info: "{info}", classroom: "{classroom}", dayNum: "{dayNum}"'.format(
            title=title[0], startTime= startTime,endTime=endTime,name=name,info=info,classroom=classroom,dayNum=dayNum
        )
    ) """

# if title has a <small></small> property, then it's a special case
# get text inside the <small></small> and save as one-time event!
