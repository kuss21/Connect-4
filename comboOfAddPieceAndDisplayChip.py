#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(18,GPIO.IN) # left button (white wire/red button)
GPIO.setup(19,GPIO.IN) # right button (orange wire/red button)
GPIO.setup(25,GPIO.IN) # select button (blue wire/blue button) 

amtOfRow = 7
amtOfCol = 10
from enum import Enum, unique
@unique
class Piece(Enum):
	BLANK = 1
	RED = 2
	BLUE = 3

board = [[0 for i in range(amtOfCol)] for j in range(amtOfRow)]
for row in range(amtOfRow):
    for col in range(amtOfCol):
        board[row][col] = Piece.BLANK

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

        # !! NEED TO SWITCH AROUND ROW AND COL NAMES (THEY GOT MIXED UP)!!
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
        
        colValue = amtOfCol - 1

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
                        colValue -= 1
                        if(colValue < 0):
                            colValue = 0
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
                        colValue += 1
                        if(colValue is amtOfCol or colValue > amtOfCol):
                            colValue = amtOfCol-1 #should set colValue = 9
                        chip_canvas = self.matrix.SwapOnVSync(chip_canvas)
                        break
                elif(not selectInput):
                    print("piece selected")
                    time.sleep(0.5)
                    addPieceFunc = addPiece()
                    addPieceFunc.run(chip_canvas, colValue)
                    if(chipColor is playerOneColor):
                        chipColor = playerTwoColor
                        break
                    else:
                        chipColor = playerOneColor
                        break
                else:
                    break 



#function to add Piece

class addPiece(SampleBase):
    def __init__(self, *args, **kwargs):
        super(addPiece, self).__init__(*args, **kwargs)

    def run(self, canvas, column): # WILL NEED TO ADD WHICH PLAYER'S TURN IT IS
        print("in addPiece function")

        #chip_canvas = self.matrix.CreateFrameCanvas()

        # color of player's chips
        playerOneColor = graphics.Color(255,0,0) # red
        playerTwoColor = graphics.Color(0,0,255) # blue

        # first player to go will be player 1
        player = Piece.RED

        # so as you move along the columns and rows
        # you will want to move over four for each column you move to
        # this is the same for rows
        # so, to move over one column from the original coordinates, you want to do
        # original_x + (col*4)
        
        while True:
            # first position of a placed chip 
            # it will be in the bottom left corner of the board
            # also the left corner of the chip piece
            # this coordinate is (2,28)
            original_x = 2
            original_y = 28
            #print("value of column:", column)
            
            if(column >= 0 and column < amtOfCol):
                #canvas = self.matrix.SwapOnVSync(canvas)
             
                for row in range(amtOfRow):
                    print("in for loop")
                    if(board[amtOfRow-1][column] is not Piece.BLANK):
                        print("column full", board[amtOfRow-1][column])
                        time.sleep(10)
                        #canvas = self.matrix.SwapOnVSync(canvas)
                        break
                    if(board[row][column] == Piece.BLANK):
                        board[row][column] = player
                        if(player == Piece.RED):
                            print("drawing chip in row:", row)
                            graphics.DrawLine(canvas, original_x+(column*4), original_y-(row*4), original_x+(column*4),  original_y-(row*4)+1, playerOneColor)
                            #x_coord = original_x+(col*4)
                            #print("x coord:", x_coord)
                            #y_coord = original_y-(row*4)
                            #print("y coord:", y_coord)

                            graphics.DrawLine(canvas, original_x+(column*4)+1, original_y-(row*4), original_x+(column*4)+1, original_y-(row*4)+1, playerOneColor)
                            #canvas = self.matrix.SwapOnVSync(canvas)
                            break
                break        

#Main Function
if __name__=="__main__":
    test_frank = DisplayChip()
    if (not test_frank.process()):
       test_frank.print_help()      
