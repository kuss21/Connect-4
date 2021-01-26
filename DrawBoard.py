#!/usr/bin/env python
from PIL import Image
from PIL import ImageDraw
from samplebase import SampleBase #### file that has all the arguments and Ctrl+C commands
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time

# Function for drawing a board
# there are 10 columns
# one column is 2x32
# there are 7 rows
# one row is 2x42
# The chip size is 2x2 pixels

options = RGBMatrixOptions()
options.hardware_mapping = 'adafruit-hat'

class DrawBoard(SampleBase):
  def __init__(self, *args, **kwargs):
    super(DrawBoard, self).__init__(*args, **kwargs)
    
  def run(self):
    # creates a matrix called boxcanvas
    boxcanvas = self.matrix.CreateFrameCanvas()
    
    # sets boardColor of rows and columns as purple/violet
    boardColor = graphics.Color(128,0,128)
    
    while_x = True
     
    # increment amount
    inc_amt = 4
    
    while while_x is True:
        # postion variables for drawing the board
        # position for the columns
        # this sets the first column at (0,2) and y = (0,31) (it's a straight line down)
        # this means that the first column leaves 2 blank pixels above it
        col_pos_x1 = 0
        col_pos_y1 = 2
        col_pos_x2 = 0
        col_pos_y2 = 31
    
        # position for the rows
        # the first row will be at (0,2) to (41,2) (it's a horizontal line over)
        # above the first row will be 2 blank pixels
        row_pos_x1 = 0
        row_pos_y1 = 2
        row_pos_x2 = 41
        row_pos_y2 = 2
    
        ### variable for loops ###
    
        # initial values of the column and row count
        col_init_count = 0
        row_init_count = 0
    
        # column should be 42 because there are 42 individual columns
        # row should be 30 because there are 30 individual rows
        # both row and column count board lines and places for chips
        col_count = 42
        row_count = 30
 
        # draw in one column at a time in the for loop
        for x in range(col_init_count, col_count, inc_amt): # keep incrementing until x reaches the value 41, which should be end of board
            graphics.DrawLine(boxcanvas, col_pos_x1, col_pos_y1, col_pos_x2, col_pos_y2, boardColor) ## draw a line for the column
            # increment the x coordinates by 1 to draw the next column and draw the line
            col_pos_x1 += 1 
            col_pos_x2 += 1
            graphics.DrawLine(boxcanvas, col_pos_x1, col_pos_y1, col_pos_x2, col_pos_y2, boardColor)
            # increment position of x coordinates by 3 (leaves a blank 2x1 space for the chip)
            col_pos_x1 += 3
            col_pos_x2 += 3
            boxcanvas = self.matrix.SwapOnVSync(boxcanvas)
        # now go back to the beginning of for loop with incremented value of col_position + 3
        # ! MIGHT NEED TO HAVE A CHECKER HERE TO MAKE SURE COL_POS_(X OR Y) AREN'T > COL_COUNT ! #
      
        # draw in one row at a time in a for loop
        for y in range(row_init_count, row_count, inc_amt): # keep incrementing until y reaches the value 29, which should be the end of the board
            graphics.DrawLine(boxcanvas, row_pos_x1, row_pos_y1, row_pos_x2, row_pos_y2, boardColor) ## draw a line for the row
            # increment the y coordinates by 1 to draw the next row and draw the line
            row_pos_y1 += 1 
            row_pos_y2 += 1
            graphics.DrawLine(boxcanvas, row_pos_x1, row_pos_y1, row_pos_x2, row_pos_y2, boardColor)
            # increment position of y coordinates by 3 (leaves a blank 2x1 space for the chip)
            row_pos_y1 += 3 
            row_pos_y2 += 3
            boxcanvas = self.matrix.SwapOnVSync(boxcanvas)
        # now go back to the beginning of for loop with incremented value of row_position + 3
        # ! MIGHT NEED TO HAVE A CHECKER HERE TO MAKE SURE COL_POS_Y AREN'T > ROW_COUNT ! #

   
# Main Function
if __name__=="__main__":
    test_frank = DrawBoard()
    if (not test_frank.process()):
        test_frank.print_help()
