#!/usr/bin/python

import threading as Threading
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(18,GPIO.IN)
GPIO.setup(19,GPIO.IN)
GPIO.setup(25,GPIO.IN)

leftPress = Threading.Event()
dropPress = Threading.Event()
rightPress = Threading.Event()

while True:
    leftInput = GPIO.input(18)
    if (not leftInput):
        leftPress.set()
        print("piece moved left")	
        leftPress.clear()
        leftPress.wait()
	#else
		#leftPress.set()
		

    downInput = GPIO.input(25)
    if (not downInput):
        dropPress.set()
        print("piece dropped")
        dropPress.clear()
        dropPress.wait()
	#else
		#dropPress.set()

	
    rightInput = GPIO.input(19)
    if (not rightInput):
        rightPress.set()
        print("piece moved right")
        rightPress.clear
        rightPress.wait()
	#else
		#rightPress.set	
