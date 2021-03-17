#!/usr/bin/python

import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(18,GPIO.IN)
GPIO.setup(19,GPIO.IN)
GPIO.setup(25,GPIO.IN)
prev_input = 0

while True:
    leftInput = GPIO.input(18)
    #print(leftInput)
    if (not leftInput):
        print("piece moved left")
        print(leftInput)
        time.sleep(1)
        
    downInput = GPIO.input(25)
    if (not downInput):
        print("piece dropped")
        time.sleep(1)

    rightInput = GPIO.input(19)
    if (not rightInput):
        print("piece moved right")
        time.sleep(1)
