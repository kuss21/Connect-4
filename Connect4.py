#!/usr/bin/env python
from samplebase import SampleBase #### file that has all the arguments and Ctrl+C commands
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

PlayerTURN = [1]

# MAIN Function with everything being displayed and game functionality

# command to run:
## sudo python3 Connect4.py --led-rows=32 --led-cols=64 --led-slowdown-gpio=4 --led-brightness =80

# there are 10 columns
# one column is 2x32
# there are 7 rows
# one row is 2x42
# The chip size is 2x2 pixels

options = RGBMatrixOptions()
options.hardware_mapping = 'adafruit-hat'

# class that holds all functions

class ConnectFour(SampleBase):
    def __init__(self, *args, **kwargs):
        super(ConnectFour, self).__init__(*args, **kwargs)
        self.parser.add_argument('-t', default='Connect 4')

    #endGame checks to see if the game is done by seeing if there are any empty spaces left (currently doesn't
    #check for wins (lines of four))
    def endGame(self):
        if(self.connected_four(self.get_position_mask_bitmap())):
            return True

        for row in range(amtOfRow):
            for col in range(amtOfCol):
                if(board[row][col] == Piece.BLANK):
                    return False
        return True

    #changing an array into a bitstring
    #code is referenced from TowardsDataScience.com
    def get_position_mask_bitmap(self):
        bitmap = ""
        for col in range (0, amtOfCol, 1):
            for row in range (0, amtOfRow, 1):
                if board[row][col] == PlayerTURN:
                    bitmap = "1" + bitmap
                else:
                    bitmap = "0" + bitmap
		#add an extra zero into the bitstring to help with checking for diagonal wins
		#this is similar to adding an extra row full of blanks 
                bitmap = "0" + bitmap
        return int(bitmap, 2)

    #check for wins on the board
    #code is referenced from TowardsDataScience.com
    def connected_four(self,position):
	#check for win vertical 
        for col in range(amtOfCol):
            inRow = 0
            for index in range(amtOfRow + 1):
                shift = (col * (amtOfRow + 1)) + index
                if((position >> shift) & 1) == 1:
                    inRow += 1
                else:
                    inRow = 0

                if inRow == 4:
                    return True

	#check for win horizontal
        for row in range(amtOfRow):
            inRow = 0
            for index in range(amtOfCol):
                shift = (row) + (index * (amtOfRow + 1))
                if((position >> shift) & 1) == 1:
                    inRow += 1
                else:
                    inRow = 0

                if inRow == 4:
                    return True

	#check for bottom left to top right diagonal
        for row in range(amtOfRow + 2):
            for col in range(amtOfCol - 1):
                shift = row + (col * (amtOfRow + 2))
                if((position >> shift) & 1) == 1:
                    inRow += 1
                else:
                    inRow = 0

                if inRow == 4:
                    return True

	#check for top left to bottom right diagonal
        for row in range(amtOfRow):
            for col in range(amtOfCol + 2):
                shift = row + (col * amtOfRow)
                if((position >> shift) & 1) == 1:
                    inRow += 1
                else:
                    inRow = 0

                if inRow == 4:
                    return True


        return False


    def run(self):
        # first we will want to call the Welcome Message function to display a welcome message to the player(s)
    	# this will be where we select how many players

    	### call WelcomeMessage definition ###


    	# Next we want to draw the board and check if it's the end of the game (if winner)
        print("in DrawBoard function")
	# creates a matrix called boxcanvas
        boxcanvas = self.matrix.CreateFrameCanvas()
	   
        # sets boardColor of rows and columns as purple/violet
        boardColor = graphics.Color(133, 127, 148)
	    
        # increment amount
        inc_amt = 4
	    
	# every time it goes to redraw the board, it'll check for a winner
        while(self.endGame() == False):
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
            boxcanvas = self.matrix.SwapOnVSync(boxcanvas)

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
            boxcanvas = self.matrix.SwapOnVSync(boxcanvas)

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

            print("in DisplayChip function call")
	    #canvas = self.matrix.CreateFrameCanvas()
            boxcanvas = self.matrix.SwapOnVSync(boxcanvas)

	    #chipColor = graphics.Color(0, 0, 255)
            playerOneColor = graphics.Color(255, 0, 0)
            playerTwoColor = graphics.Color(255, 255, 0)

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

	    # everytime it has to redraw the Player's chip or a placed chip, it'll check if there's a winner
            while(self.endGame() == False):
                print(self.endGame())
                boxcanvas = self.matrix.SwapOnVSync(boxcanvas)
	        # draw a black line which will erase anything in the chip zone
                graphics.DrawLine(boxcanvas, bar_row_x1, bar_col_y1, bar_row_x2, bar_col_y2, barColor)
                graphics.DrawLine(boxcanvas, bar_row_x1, bar_col_y1+1, bar_row_x2, bar_col_y2+1, barColor)
                boxcanvas = self.matrix.SwapOnVSync(boxcanvas)
	        # draw chip
                graphics.DrawLine(boxcanvas, chip_row_x1, chip_col_y1, chip_row_x2, chip_col_y2, chipColor)
                graphics.DrawLine(boxcanvas, chip_row_x1+1, chip_col_y1, chip_row_x2+1, chip_col_y2, chipColor)

                boxcanvas = self.matrix.SwapOnVSync(boxcanvas) 

                while True:
                    leftInput = GPIO.input(18)
                    rightInput = GPIO.input(19)
                    selectInput = GPIO.input(25)
                    if(not leftInput):
	                #print("piece moved left")
	                #time.sleep(0.1) #changed time sleep to half a second
                        start = time.time()
                        while time.time() - start < 0.5:
                            boxcanvas = self.matrix.SwapOnVSync(boxcanvas)
                            continue
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
                            boxcanvas = self.matrix.SwapOnVSync(boxcanvas)
                            break
                    elif(not rightInput):
	                #print("piece moved right")
	                #time.sleep(0.1) #see if this is enough time
                        start = time.time()
                        while time.time() - start < 0.5:
                            boxcanvas = self.matrix.SwapOnVSync(boxcanvas)
                            continue
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
                            boxcanvas = self.matrix.SwapOnVSync(boxcanvas)
                            break
                    elif(not selectInput):
	                #print("piece selected")
                        start = time.time()
                        while time.time() - start < 0.5:
                            boxcanvas = self.matrix.SwapOnVSync(boxcanvas)
                            continue

	                # call function to add a piece into the board
                        addPieceFunc = addPiece()
                        addPieceFunc.run(boxcanvas, colValue)

	                # if the column is full, you don't want to change players or the chipColor
                        if(board[amtOfRow - 1][colValue] is Piece.BLANK):
                            if(chipColor is playerOneColor):
                                chipColor = playerTwoColor
                                break
                            else:
                                chipColor = playerOneColor
                                break
                        else:
                            break
                    else:
                        break 
	
        
           
class addPiece(SampleBase):
    def __init__(self, *args, **kwargs):
        super(addPiece, self).__init__(*args, **kwargs)

    def run(self, canvas, column): # WILL NEED TO ADD WHICH PLAYER'S TURN IT IS
        print("in addPiece function")

        #chip_canvas = self.matrix.CreateFrameCanvas()

        # color of player's chips
        playerOneColor = graphics.Color(255,0,0) # red
        playerTwoColor = graphics.Color(255, 255, 0) # yellow
        
        if(PlayerTURN[0] == 1):
            # first player to go will be player 1
            player = Piece.RED
            PlayerTURN[0] += 1
        else:
            player = Piece.BLUE
            PlayerTURN[0] -= 1
        #print(player)

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

                        #time.sleep(10)
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

                            player = Piece.BLUE
                            print("setting player to ", player)
                            break
                        elif(player == Piece.BLUE):
                            print("drawing blue chip in row:", row)
                            graphics.DrawLine(canvas, original_x+(column*4), original_y-(row*4), original_x+(column*4),  original_y-(row*4)+1, playerTwoColor)
                            #x_coord = original_x+(col*4)
                            #print("x coord:", x_coord)
                            #y_coord = original_y-(row*4)
                            #print("y coord:", y_coord)

                            graphics.DrawLine(canvas, original_x+(column*4)+1, original_y-(row*4), original_x+(column*4)+1, original_y-(row*4)+1, playerTwoColor)
                            #canvas = self.matrix.SwapOnVSync(canvas)

                            player = Piece.RED

                            break
                break              


      # Main Function
if __name__=="__main__":
    test_official = ConnectFour()
    if (not test_official.process()):
       test_official.print_help() 
