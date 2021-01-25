#!/usr/bin/python

#importing proper libraries
import RPi.GPIO as GPIO
import time

#initializing ability to use pins as input
GPIO.setmode(GPIO.BCM)

#setting corresponding pins as input
GPIO.setup(27,GPIO.IN)
GPIO.setup(22,GPIO.IN)
GPIO.setup(24,GPIO.IN)

#defining variables for each button at a specified pin
pieceLeft = GPIO.input(27)
pieceRight = GPIO.input(22)
dropPiece = GPIO.input(24)

#define inputs for debounce purposes
previousInputLeft = 0
previousInputRight = 0
previousInputDrop = 0

#check state of debounce input and button press
#if the button has been pressed update debounce variable
#after updtating debounce variable, sleep to prevent multiple presses
while True:
    if ((previousInputLeft) and pieceLeft):
        print("piece moved left")
       # previousInputLeft = pieceLeft
        time.sleep(0.05)
        break

#check state of debounce input and button press
#if the button has been pressed update debounce variable
#after updtating debounce variable, sleep to prevent multiple presses
while True:
    if ((not previousInputRight) and pieceRight):
        print("piece moved right")
       # previousInputRight = pieceRight
        time.sleep(0.05)
        break

#check state of debounce input and button press
#if the button has been pressed update debounce variable
#after updtating debounce variable, sleep to prevent multiple presses
while True:
    if ((not previousInputDrop) and dropPiece):
        print("piece has been dropped")
        #previousInputDrop = dropPiece
        time.sleep(0.05)
        break
