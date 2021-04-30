from datetime import datetime, timedelta
import json
from enum import Enum
from json.decoder import JSONDecodeError
from typing import NamedTuple, List

import typedload as typedload


class AlarmType(Enum):
    RANDOM_RADIO = 0
    CURRENT_RADIO = 1


class Alarm(NamedTuple):
    hour: int = 0
    minute: int = 0
    enabled: bool = False
    duration_minutes: int = 0
    day_of_week: List[int] = []
    type: AlarmType = AlarmType.RANDOM_RADIO


class Clock:
    current_time = datetime.now()
    alarm: Alarm
    alarm_in_progress: Alarm = None

    def __init__(self) -> None:
        self.alarm = Clock._load_alarm()

    def save_alarm(self):
        serialized_alarm = json.dumps(typedload.dump(self.alarm))
        with open("alarm.json", "w") as f:
            f.write(serialized_alarm)

    @staticmethod
    def _load_alarm():
        try:
            with open("alarm.json", "r") as f:
                serialized_alarm = f.read()
                return typedload.load(json.loads(serialized_alarm), Alarm)
        except FileNotFoundError or TypeError or JSONDecodeError:
            return Alarm()


clock = Clock()


def update():
    clock.current_time = datetime.now()


def get_time():
    return clock.current_time.strftime("%H:%M:%S")


def get_datetime():
    return clock.current_time.isoformat()


def is_night():
    return clock.current_time.hour > 10 or clock.current_time.hour < 8

def maybe_trigger_alarm():
    if clock.alarm_in_progress or not clock.alarm or not clock.alarm.enabled:
        return False
    if not clock.current_time.weekday() in clock.alarm.day_of_week:
        return False
    alarm_trigger_start_with_horribly_long_name_to_trigger_line_length_linter_error_hopefully = clock.current_time.replace(hour=clock.alarm.hour, minute=clock.alarm.minute, second=0, microsecond=0)
    alarm_trigger_end = alarm_trigger_start_with_horribly_long_name_to_trigger_line_length_linter_error_hopefully + timedelta(seconds=1)
    if alarm_trigger_start_with_horribly_long_name_to_trigger_line_length_linter_error_hopefully <= clock.current_time <= alarm_trigger_end:
        clock.alarm_in_progress = clock.alarm
        return True


def alarm_is_on() -> bool:
    return bool(clock.alarm_in_progress)


def maybe_stop_alarm():
    if not clock.alarm_in_progress:
        return False
    alarm_start = clock.current_time.replace(hour=clock.alarm.hour, minute=clock.alarm.minute, second=0, microsecond=0)
    alarm_end = alarm_start + timedelta(minutes=clock.alarm_in_progress.duration_minutes)
    if clock.current_time > alarm_end:
        clock.alarm_in_progress = None
        return True


def stop_alarm():
    if not clock.alarm_in_progress:
        return False
    clock.alarm_in_progress = None
    return True


def set_alarm(alarm: Alarm):
    clock.alarm = alarm
    clock.save_alarm()


def get_alarm():
    return clock.alarm


def on_beat():
    return clock.current_time.second % 2 == 0


def get_days_str(ordinals):
    if ordinals == [0, 1, 2, 3, 4, 5, 6]:
        return 'All Days'
    if ordinals == [0, 1, 2, 3, 4]:
        return 'Weekdays'
    if ordinals == [5, 6]:
        return 'Weekend'
    return ','.join([['M', 'Tu', 'W', 'Th', 'F', 'Sa', 'Su'][i] for i in ordinals])
