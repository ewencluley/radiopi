import time
from collections import namedtuple
import json

Alarm = namedtuple("Alarm", "day_of_week, hour minute enabled")


class Clock:
    current_time = time.localtime()

    def __init__(self) -> None:
        self.alarm = Clock._load_alarm()

    def save_alarm(self):
        serialized_alarm = json.dumps(self.alarm._asdict())
        with open("alarm.json", "w") as f:
            f.write(serialized_alarm)

    @staticmethod
    def _load_alarm():
        try:
            with open("alarm.json", "r") as f:
                serialized_alarm = f.read()
                return Alarm(**json.loads(serialized_alarm))
        except FileNotFoundError:
            return Alarm(hour=0, minute=0, day_of_week=[], enabled=False)


clock = Clock()


def update():
    clock.current_time = time.localtime()


def get_time():
    return time.strftime("%H:%M:%S", clock.current_time)


def should_alarm():
    return clock.alarm and clock.alarm.enabled \
           and (clock.current_time.tm_wday in clock.alarm.day_of_week) \
           and (clock.current_time.tm_hour == clock.alarm.hour) \
           and (clock.current_time.tm_min == clock.alarm.minute)


def set_alarm(alarm: Alarm):
    clock.alarm = alarm
    clock.save_alarm()


def get_alarm():
    return clock.alarm


def on_beat():
    return clock.current_time.tm_sec % 2 == 0


def get_days_str(ordinals):
    if ordinals == [0, 1, 2, 3, 4, 5, 6]:
        return 'All Days'
    if ordinals == [0, 1, 2, 3, 4]:
        return 'Weekdays'
    if ordinals == [5, 6]:
        return 'Weekend'
    return ','.join([['M', 'Tu', 'W', 'Th', 'F', 'Sa', 'Su'][i] for i in ordinals])
