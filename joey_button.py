#!/usr/bin/python

import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(27,GPIO.IN)
prev_input = 0

while True:
    input = GPIO.input(27)
    if (not input):
        print("piece moved left")
        time.sleep(1)
        
