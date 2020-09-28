import time
from collections import namedtuple


Alarm = namedtuple("Alarm", "day_of_week, hour minute")


class Clock:
    alarm_time = Alarm(day_of_week={0, 1, 2, 3, 4, 5, 6}, hour=9, minute=49)
    current_time = time.localtime()


clock = Clock()


def update():
    clock.current_time = time.localtime()


def get_time():
    return time.strftime("%H:%M:%S", clock.current_time)


def should_alarm():
    return clock.alarm_time and (clock.current_time.tm_wday in clock.alarm_time.day_of_week) \
           and (clock.current_time.tm_hour == clock.alarm_time.hour) \
           and (clock.current_time.tm_min == clock.alarm_time.minute)


def set_alarm(alarm: Alarm):
    clock.alarm_time = alarm
