import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.OUT)


def on():
    GPIO.output(16,GPIO.HIGH)

def off():
    GPIO.output(16,GPIO.LOW)