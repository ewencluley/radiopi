#!/usr/bin/python3

import time

import AdminServer
import Clock
import Radio
import LED
from Button import Button

AdminServer.start_in_background()
try:
    from display.OledDisplay import OledDisplay
    display = OledDisplay()
except ModuleNotFoundError:
    from display.Display import Display
    display = Display()


def on_button_release(held_for):
    if held_for > 2 and Clock.alarm_is_on():
        Clock.stop_alarm()


def on_button_pressed():
    pass


display.set_contrast(1)
try:
    #button = Button(20, on_button_pressed, on_button_release)
    while True:
        display.clear()
        Clock.update()
        time_str = Clock.get_time()
        alarm = Clock.get_alarm()
        alarm_str = f'{str(alarm.hour).zfill(2)}:{str(alarm.minute).zfill(2)} [{Clock.get_days_str(alarm.day_of_week)}]'

        display.draw_text((20, 0), time_str, font=display.big_font)
        if Clock.maybe_trigger_alarm() and not Radio.is_playing():
            volume = Radio.get_volume()
            Radio.set_volume(0)
            if not Radio.play(triggered_by_alarm=alarm):
                print("Failed to play chosen station, playing fallback mp3.")
                Radio.play_mp3('radioError.mp3')
            Radio.fadein(volume)
            AdminServer.broadcast_state()
        Clock.maybe_stop_alarm()
        if not Clock.alarm_is_on() and Radio.is_playing() and Radio.was_triggered_by_alarm():
            Radio.stop()
            AdminServer.broadcast_state()
        if Clock.alarm_is_on() and Clock.on_beat():
            display.draw_text((0, 16), '*** ALARM ***', font=display.small_font)
            LED.on()
        elif alarm.enabled:
            display.draw_text((0, 16), alarm_str, font=display.small_font)
            LED.off()
        current_radio_station = str(Radio.state.current_station.name)
        display.draw_text((0, 25), f'{current_radio_station} - {Radio.get_volume()}%', font=display.small_font)

        display.update()
        time.sleep(0.10)
except KeyboardInterrupt:
    AdminServer.shutdown()
