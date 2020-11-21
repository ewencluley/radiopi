from threading import Thread

import RPi.GPIO as GPIO
from time import sleep

clk = 17
dt = 4

volume_increment = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


class Volume:
    GPIO.setmode(GPIO.BCM)
    volume = 70

    def get_volume(self):
        return self.volume

    def update_volume(self):
        try:
            while True:
                clk_state = GPIO.input(clk)
                dt_state = GPIO.input(dt)
                new_volume = self.volume
                if clk_state != self.clkLastState:
                    if dt_state != clk_state:
                        new_volume += volume_increment
                    else:
                        new_volume -= volume_increment
                    self.volume = max(0, min(100, new_volume))
                    self.volume_update_callback(self.volume)
                self.clkLastState = clk_state
                sleep(0.01)
        finally:
            GPIO.cleanup()

    def __init__(self, volume_update_callback, volume) -> None:
        self.volume_update_callback = volume_update_callback
        self.clkLastState = GPIO.input(clk)
        self.volume = volume
        Thread(target = self.update_volume, daemon=True).start()
