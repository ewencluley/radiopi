import subprocess
import time

import AdminServer
import Clock
import Radio

AdminServer.start_in_background()
try:
    from display.OledDisplay import OledDisplay
    display = OledDisplay()
except ModuleNotFoundError:
    from display.Display import Display
    display = Display()

try:
    while True:
        cmd = "hostname -I | cut -d\' \' -f1"
        IP = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)

        Clock.update()
        time_str = Clock.get_time()
        alarm = Clock.get_alarm()
        alarm_str = f'{str(alarm.hour).zfill(2)}:{str(alarm.minute).zfill(2)} [{Clock.get_days_str(alarm.day_of_week)}]'

        display.draw_text((20, 0), time_str, font=Display.big_font)
        if Clock.maybe_trigger_alarm() and not Radio.is_playing():
            Radio.play(triggered_by_alarm=True)
        Clock.maybe_stop_alarm()
        if not Clock.alarm_is_on() and Radio.is_playing() and Radio.was_triggered_by_alarm():
            Radio.stop()
        if Clock.alarm_is_on() and Clock.on_beat():
            display.draw_text((0, 16), '*** ALARM ***', font=Display.small_font)
        elif alarm.enabled:
            display.draw_text((0, 16), alarm_str, font=Display.small_font)

        display.draw_text((0, 25), str(IP), font=Display.small_font)

        display.update()
        time.sleep(0.01)
except KeyboardInterrupt:
    AdminServer.shutdown()
