#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(18,GPIO.IN) # left button (white wire/red button)
GPIO.setup(19,GPIO.IN) # right button (orange wire/red button)
GPIO.setup(25,GPIO.IN) # select button (blue wire/blue button) 

#run command
# sudo ./DisplayPlayersChip.py --led-cols=64 --led-rows=32 --led-slowdown-gpio=4

# Function for displaying the Player's chip

options = RGBMatrixOptions()
options.hardware_mapping = 'adafruit-hat'

class DisplayChip(SampleBase):
    def __init__(self, *args, **kwargs):
        super(DisplayChip, self).__init__(*args, **kwargs)

    def run(self):
        print("in function call")
        chip_canvas = self.matrix.CreateFrameCanvas()

        #chipColor = graphics.Color(0, 0, 255)
        playerOneColor = graphics.Color(255, 0, 0)
        playerTwoColor = graphics.Color(0,0,255)

        # first position of chip
        chip_row_x1 = 38
        chip_col_y1 = 0
        chip_row_x2 = 38
        chip_col_y2 = 1
        # set bounds of the board
        board_bound_right = 38
        board_bound_left = 2
        # bounds for a line of grey and color graphics of black 
        bar_row_x1 = 0
        bar_col_y1 = 0
        bar_row_x2 = 41
        bar_col_y2 = 0 
        barColor = graphics.Color(0,0,0)
        chipColor = playerOneColor #initialize chip color for the first player
        

        while True:

            # draw a black line which will erase anything in the chip zone
            graphics.DrawLine(chip_canvas, bar_row_x1, bar_col_y1, bar_row_x2, bar_col_y2, barColor)
            graphics.DrawLine(chip_canvas, bar_row_x1, bar_col_y1+1, bar_row_x2, bar_col_y2+1, barColor)

            # draw chip
            graphics.DrawLine(chip_canvas, chip_row_x1, chip_col_y1, chip_row_x2, chip_col_y2, chipColor)
            graphics.DrawLine(chip_canvas, chip_row_x1+1, chip_col_y1, chip_row_x2+1, chip_col_y2, chipColor)

            chip_canvas = self.matrix.SwapOnVSync(chip_canvas) 

            while True:
                leftInput = GPIO.input(18)
                rightInput = GPIO.input(19)
                selectInput = GPIO.input(25)
                if(not leftInput):
                    print("piece moved left")
                    time.sleep(0.5) #changed time sleep to half a second
                    if((chip_row_x1 == board_bound_left) and (chip_row_x2 == board_bound_left)):
                        chip_row_x1 = board_bound_left
                        chip_row_x2 = board_bound_left
                        break
                    else:
                        chip_row_x1 -= 4
                        chip_row_x2 -= 4
                        # test to see how to call a function
                        # it needs to be outside of class definition!
                        # testFunc = Test_Function()
                        # testFunc.run(chip_canvas)
                        chip_canvas = self.matrix.SwapOnVSync(chip_canvas)
                        break
                elif(not rightInput):
                    print("piece moved right")
                    time.sleep(0.5) #see if this is enough time
                    if((chip_row_x1 == board_bound_right) and (chip_row_x2 ==board_bound_right)):
                        chip_row_x1 = board_bound_right
                        chip_row_x2 = board_bound_right
                        break
                    else:
                        chip_row_x1 += 4
                        chip_row_x2 += 4
                        chip_canvas = self.matrix.SwapOnVSync(chip_canvas)
                        break
                elif(not selectInput):
                    print("piece selected")
                    time.sleep(0.5)
                    if(chipColor is playerOneColor):
                        chipColor = playerTwoColor
                        break
                    else:
                        chipColor = playerOneColor
                        break
                else:
                    break 

'''
DELANEY COMMENTED THIS SECTION. NOT SURE ABOUT FUNCTIONALITY
class Test_Function(SampleBase):
    def __init__(self, *args, **kwargs):
            super(Test_Function, self).__init__(*args, **kwargs)

    def run(self, canvas):
            print("in test function")
            lineColor = graphics.Color(255, 0, 255)
            graphics.DrawLine(canvas, 0, 0, 0, 40, lineColor)
'''
            
#Main Function
if __name__=="__main__":
    test_frank = DisplayChip()
    if (not test_frank.process()):
       test_frank.print_help()      
