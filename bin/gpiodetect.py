#!/usr/bin/env python3

import signal
import sys
import RPi.GPIO as GPIO

BUTTON_GPIO = 12

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def both(channel):
    print("event")

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=both, bouncetime=300)

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
