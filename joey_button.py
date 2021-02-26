#!/usr/bin/python

import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(5,GPIO.IN)
GPIO.setup(12,GPIO.IN)
GPIO.setup(16,GPIO.IN)
prev_input = 0

while True:
    leftInput = GPIO.input(5)
    if (not leftInput):
        print("piece moved left")
        time.sleep(1)
        
    downInput = GPIO.input(12)
    if (not downInput):
        print("piece dropped")
        time.sleep(1)

    rightInput = GPIO.input(16)
    if (not rightInput):
        print("piece moved right")
        time.sleep(1)
