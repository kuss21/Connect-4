#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(18,GPIO.IN) # left button (white wire/red button)
GPIO.setup(19,GPIO.IN) # right button (orange wire/red button)
GPIO.setup(25,GPIO.IN) # select button (blue wire/blue button) 

options = RGBMatrixOptions()

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


class addPiece(SampleBase):
    def __init__(self, *args, **kwargs):
        super(addPiece, self).__init__(*args, **kwargs)

    def run(self):
        print("in addPiece function")

        chip_canvas = self.matrix.CreateFrameCanvas()

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
            
            # first let's ask the user for an input of which column to input the chip
            print('Enter a column')
            col = int(input())
            print('Column is equal to', col)
            if(col >= 0 and col < amtOfCol):
                chip_canvas = self.matrix.SwapOnVSync(chip_canvas)
             
                for row in range(amtOfRow):
                    if(board[amtOfRow-1][col] is not Piece.BLANK):
                        print("column full")
                        chip_canvas = self.matrix.SwapOnVSync(chip_canvas)
                        break
                    if(board[row][col] == Piece.BLANK):
                        board[row][col] = player
                        if(player == Piece.RED):
                            print("drawing chip in row:", row)
                            graphics.DrawLine(chip_canvas, original_x+(col*4), original_y-(row*4), original_x+(col*4),  original_y-(row*4)+1, playerOneColor)
                            x_coord = original_x+(col*4)
                            print("x coord:", x_coord)
                            y_coord = original_y-(row*4)
                            print("y coord:", y_coord)

                            graphics.DrawLine(chip_canvas, original_x+(col*4)+1, original_y-(row*4), original_x+(col*4)+1, original_y-(row*4)+1, playerOneColor)
                            chip_canvas = self.matrix.SwapOnVSync(chip_canvas)
                            break
                        

#Main Function
if __name__=="__main__":
    test_frank = addPiece()
    if (not test_frank.process()):
       test_frank.print_help()    
