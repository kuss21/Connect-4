#!/usr/bin/env python
from samplebase import SampleBase #### file that has all the arguments and Ctrl+C commands
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time
import random
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
	YELLOW = 3

board = [[0 for i in range(amtOfCol)] for j in range(amtOfRow)]
for row in range(amtOfRow):
    for col in range(amtOfCol):
        board[row][col] = Piece.BLANK

PlayerTURN = [1]

# global array that shows the winner
# 0 => TIE
# 1 => Player 1 Wins
# 2 => Player 2 Wins
WINNER = [0]

# global array that shows if AI is selected
# 0 => NO AI
# 1 => AI ON
AISWITCH = [0]

# MAIN Function with everything being displayed and game functionality

# command to run:
## sudo python3 Connect4.py --led-rows=32 --led-cols=64 --led-slowdown-gpio=4 --led-brightness=80

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
    def endGame(self, player):
        #if(self.connected_four(player)):
        #    return True

        if(self.connected_four(player) is True):
            if player == Piece.RED:
                WINNER[0] = 1
            elif player == Piece.YELLOW:
                WINNER[0] = 2
            return True

        # check if game board is full
        for col in range(amtOfCol):
                if(board[amtOfRow-1][col] is Piece.BLANK):
                    return False
        
        #for row in range(amtOfRow):
        #    for col in range(amtOfCol):
        #        if(board[row][col] == Piece.BLANK):
        #            return False
        
        WINNER[0] = 0 #means it's a tie
        return True

    #check for wins on the board
    #code is referenced from TowardsDataScience.com
    def connected_four(self,player): #should be position if using Erik's function
	
        #check vertical
        for col in range(amtOfCol):
            count = 0
            for row in range(amtOfRow):
                if board[row][col] == player:
                    count +=1
                    if count == 4:
                        return True
                else:
                    count = 0

        #check horizontal 
        for row in range(amtOfRow):
            count = 0
            for col in range(amtOfCol):
                if board[row][col] == player:
                    count +=1
                    if count ==4:
                        return True
                else:
                    count = 0

        #check diagonal R-L 
        for col in range(amtOfCol-1,0,-1):
            count = 0
            for row in range(amtOfRow):
                count = 0
                for n in range(7):
                    if row+n >= amtOfRow or col-n < 0:
                        break
                    if board[row+n][col-n] == player:
                        count +=1
                        if count == 4:
                            return True
                    else:
                        count = 0

        #check diagonal L-R 
        for col in range(amtOfCol):
            count = 0
            for row in range(amtOfRow):
                count = 0
                for n in range(0,7,1):
                    if row+n >= amtOfRow or col+n >= amtOfCol:
                        break
                    if board[row+n][col+n] == player and board[row+n][col+n] is not Piece.BLANK:
                        count += 1
                        if count == 4:
                            return True
                    else:
                        count = 0
        
        # return False by default
        return False

    # function for checking for connected 3
    def connected_three(self, player):
        for col in range(amtOfCol):
            count = 0
            for row in range(amtOfRow):
                if board[row][col] == player:
                    count +=1
                    if count == 3:
                        return True
                else:
                    count = 0

        #check horizontal 
        for row in range(amtOfRow):
            count = 0
            for col in range(amtOfCol):
                if board[row][col] == player:
                    count +=1
                    if count == 3:
                        return True
                else:
                    count = 0

        #check diagonal R-L 
        for col in range(amtOfCol-1,0,-1):
            count = 0
            for row in range(amtOfRow):
                count = 0
                for n in range(7):
                    if row+n >= amtOfRow or col-n < 0:
                        break
                    if board[row+n][col-n] == player:
                        count +=1
                        if count == 3:
                    	    return True
                    else:
                        count = 0

	#check diagonal L-R 
        for col in range(amtOfCol):
            count = 0
            for row in range(amtOfRow):
                count = 0
                for n in range(7):
                    if row+n >= amtOfRow or col+n >= amtOfCol:
                        break
                    if board[row+n][col+n] == player:
                        count += 1
                        if count == 3:
                            return True
                    else:
                        count = 0
        # by default and if no connected 3
        return False

    # function for checking for connected 2
    def connected_two(self, player):
        for col in range(amtOfCol):
            count = 0
            for row in range(amtOfRow):
                if board[row][col] == player:
                    count +=1
                    if count == 2:
                        return True
                else:
                    count = 0

        #check horizontal 
        for row in range(amtOfRow):
            count = 0
            for col in range(amtOfCol):
                if board[row][col] == player:
                    count +=1
                    if count == 2:
                        return True
                else:
                    count = 0

        #check diagonal R-L 
        for col in range(amtOfCol-1,0,-1):
            count = 0
            for row in range(amtOfRow):
                count = 0
                for n in range(7):
                    if row+n >= amtOfRow or col-n < 0:
                        break
                    if board[row+n][col-n] == player:
                        count +=1
                        if count == 2:
                    	    return True
                    else:
                        count = 0

	#check diagonal L-R 
        for col in range(amtOfCol):
            count = 0
            for row in range(amtOfRow):
                count = 0
                for n in range(7):
                    if row+n >= amtOfRow or col+n >= amtOfCol:
                        break
                    if board[row+n][col+n] == player:
                        count += 1
                        if count == 2:
                            return True
                    else:
                        count = 0
        # by default and if no connected 2
        return False


    def addPieceVirtual(self, column, player):
        for row in range(amtOfRow):
            if(board[row][column] == Piece.BLANK or (board[row][column] is not Piece.RED and board[row][column] is not Piece.YELLOW)):
                board[row][column] = player
                return


    def removePiece(self, col):
        if(board[0][col] != Piece.BLANK):
            for i in range(amtOfRow):
                if(board[i][col] == Piece.BLANK):
                    board[i-1][col] = Piece.BLANK
                    return
            board[amtOfRow - 1][col] = Piece.BLANK
            return

    def comMove(self):
        if(self.connected_three(Piece.YELLOW) == True):
            for col in range(amtOfCol):
                if(self.colNotFull(col) is True):
                    self.addPieceVirtual(col, Piece.YELLOW)
                    if(self.connected_four(Piece.YELLOW) == True):
                        self.removePiece(col)
                        return col
                    self.removePiece(col)

        if(self.connected_three(Piece.RED) == True):
            for col in range(amtOfCol):
                if(self.colNotFull(col) is True):
                    self.addPieceVirtual(col, Piece.RED)
                    if(self.connected_four(Piece.RED) == True):
                        self.removePiece(col)
                        return col
                    self.removePiece(col)

        if(self.connected_two(Piece.YELLOW) == True):
            for col in range(amtOfCol):
                if(self.colNotFull(col) is True):
                    self.addPieceVirtual(col, Piece.YELLOW)
                    if(self.connected_three(Piece.YELLOW) == True):
                        self.removePiece(col)
                        return col
                    self.removePiece(col)

        if(self.connected_two(Piece.RED) == True):
            for col in range(amtOfCol):
                if(self.colNotFull(col) is True):
                    self.addPieceVirtual(col, Piece.RED)
                    if(self.connected_three(Piece.RED) == True):
                        self.removePiece(col)
                        return col
                    self.removePiece(col)


        while True:
            number = random.randint(0,9)
            if((board[amtOfRow-1][number] is Piece.BLANK) and board[amtOfRow-1][number] is not Piece.RED and board[amtOfRow-1][number] is not Piece.YELLOW):
                break
            continue
        return number 

    
    
    def colNotFull(self, col):
        if(board[amtOfRow-1][col] is Piece.BLANK):
            return True
        else:
            return False

    def welcome(self):
        wel_canvas = self.matrix.CreateFrameCanvas()
        wel_color = graphics.Color(255,255,0) #RED=(255,0,0), CORAL=(255,127,80), FOREST GREEN=(34,129,34), AQUAMARINE=(127,255,212)
        one_player = graphics.Color(255,0,0) #red
        two_player = graphics.Color(0,0,255) #blue
        font = graphics.Font()
        font.LoadFont('/home/pi/rpi-rgb-led-matrix/fonts/7x13.bdf')
        #text will take up 9 lines, cannot make smaller with this font
        pos_wel_x = 1 #this will make the text flush to the L
        pos_wel_y = 9 #this will make the text flush to the top
        wel_text = 'Connect 4'

        xpos_player_1 = 16 # halfway on the left attempt
        ypos_player = 20
        xpos_player_2 = 48 # halfway on the right attempt

        while True:
            graphics.DrawText(wel_canvas, font, pos_wel_x, pos_wel_y, wel_color, wel_text)
            graphics.DrawText(wel_canvas, font, xpos_player_1,ypos_player, one_player, '1') 
            graphics.DrawText(wel_canvas, font, xpos_player_2, ypos_player, two_player, '2')
            wel_canvas = self.matrix.SwapOnVSync(wel_canvas)
            
            leftInput = GPIO.input(18)
            rightInput = GPIO.input(19)
            selectInput = GPIO.input(25)

            if(not leftInput or not rightInput): #one of the red buttons pressed, one_player option
                start = time.time()
                while time.time() - start < 0.5:
                    continue
                wel_canvas.Clear()
                wel_canvas = self.matrix.SwapOnVSync(wel_canvas)
                #call functions with AI
                AISWITCH[0] = 1
                break

            if(not selectInput): #blue button pressed, two player option
                start = time.time()
                while time.time() - start < 0.5:
                    continue
                wel_canvas.Clear()
                wel_canvas = self.matrix.SwapOnVSync(wel_canvas)
                AISWITCH[0] = 0
                break
                #call functions without AI

        # End Message function
    def endMessage(self):
        end_canvas = self.matrix.CreateFrameCanvas()
        yellow_color = graphics.Color(255,255,0) ############SEND WINNER COLOR
        red_color = graphics.Color(255,0,0) ###########SEND Loser color
        tie_end_color = graphics.Color(128,0,255)
        tie_color = graphics.Color(0,255,17)
        font = graphics.Font()
        font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/7x13.bdf")

        cent_x = self.matrix.width /2
        cent_y = self.matrix.height /2
        
        while True:
            radius = 15
            while radius > 10:
                if WINNER[0] is 0:
                    graphics.DrawCircle(end_canvas,cent_x,cent_y,radius,tie_end_color)
                elif WINNER[0] is 1:
                    graphics.DrawCircle(end_canvas, cent_x, cent_y, radius, yellow_color)
                elif WINNER[0] is 2:
                    graphics.DrawCircle(end_canvas,cent_x, cent_y, radius, red_color)
                radius -=2
                end_canvas = self.matrix.SwapOnVSync(end_canvas)
            if WINNER[0] is 0:
                graphics.DrawText(end_canvas,font,cent_x-10,cent_y+4,tie_color,"TIE")
            elif WINNER[0] is 1:
                graphics.DrawText(end_canvas,font,cent_x-10,cent_y+4,red_color,"WIN")
            elif WINNER[0] is 2:
                graphics.DrawText(end_canvas,font,cent_x-10,cent_y+4,yellow_color,"WIN")
            end_canvas = self.matrix.SwapOnVSync(end_canvas)
            start = time.time()
            while time.time() - start < 7:
                end_canvas = self.matrix.SwapOnVSync(end_canvas)
                continue
            
            end_canvas.Clear()
            end_canvas = self.matrix.SwapOnVSync(end_canvas)
            self.run()


    def run(self):
        # first we will want to call the Welcome Message function to display a welcome message to the player(s)
    	# this will be where we select how many players

        # initialize the board to all BLANKs
        for row in range(amtOfRow):
            for col in range(amtOfCol):
                board[row][col] = Piece.BLANK


    	### call WelcomeMessage definition ###
        self.welcome()

    	# Next we want to draw the board and check if it's the end of the game (if winner)
	# creates a matrix called boxcanvas
        boxcanvas = self.matrix.CreateFrameCanvas()
        
        player = Piece.RED
        # sets boardColor of rows and columns as purple/violet
        boardColor = graphics.Color(133, 127, 148)
	    
        # increment amount
        inc_amt = 4
	
	# every time it goes to redraw the board, it'll check for a winner
        while(True):
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

            # initialize variables for drawing a vertical win condition
            verticalW_x1 = 47
            verticalW_y1 = 3
            verticalW_x2 = 47
            verticalW_y2 = 4
            verticalW_Color = graphics.Color(255, 0, 0) #this'll be red
            # draw winning conditions on the side of the board
            for verticalW in range(0,10,3):
                boxcanvas = self.matrix.SwapOnVSync(boxcanvas)
                graphics.DrawLine(boxcanvas, verticalW_x1, verticalW_y1+verticalW, verticalW_x2, verticalW_y2+verticalW, verticalW_Color)
                graphics.DrawLine(boxcanvas, verticalW_x1+1, verticalW_y1+verticalW, verticalW_x2+1, verticalW_y2+verticalW, verticalW_Color)

            # init variables for drawing a horizontal win condition
            horizW_x1 = 52
            horizW_y1 = 7
            horizW_x2 = 53
            horizW_y2 = 7
            horizW_Color = graphics.Color(255,255,0) #this'll be yellow
            # draw winning conditions on the side of the board
            for horizW in range(0, 10, 3):
                boxcanvas = self.matrix.SwapOnVSync(boxcanvas)
                graphics.DrawLine(boxcanvas, horizW_x1+horizW, horizW_y1, horizW_x2+horizW, horizW_y2, horizW_Color)
                graphics.DrawLine(boxcanvas, horizW_x1+horizW, horizW_y1+1, horizW_x2+horizW, horizW_y2+1, horizW_Color)


            # init variables for drawing a R-L diagonal win condition
            RLW_x1 = 45
            RLW_y1 = 20
            RLW_x2 = 45
            RLW_y2 = 21
            RLW_Color = graphics.Color(255, 255, 0) # this will be yellow
            # draw winning conditions on the side of the board
            for RLW in range(0, 7, 2):
                boxcanvas = self.matrix.SwapOnVSync(boxcanvas)
                graphics.DrawLine(boxcanvas, RLW_x1+RLW, RLW_y1+RLW, RLW_x2+RLW, RLW_y2+RLW, RLW_Color)
                graphics.DrawLine(boxcanvas, RLW_x1+RLW+1, RLW_y1+RLW, RLW_x2+RLW+1, RLW_y2+RLW, RLW_Color)

            # init variables for drawing a L-R diagonal win condition
            LRW_x1 = 55
            LRW_y1 = 26
            LRW_x2 = 55
            LRW_y2 = 27
            LRW_Color = graphics.Color(255,0,0) # this will be red
            # draw winning conditions on the side of the board
            for LRW in range(0, 7, 2):
                boxcanvas = self.matrix.SwapOnVSync(boxcanvas)
                graphics.DrawLine(boxcanvas, LRW_x1+LRW, LRW_y1-LRW, LRW_x2+LRW, LRW_y2-LRW, LRW_Color)
                graphics.DrawLine(boxcanvas, LRW_x1+LRW+1, LRW_y1-LRW, LRW_x2+LRW+1, LRW_y2-LRW, LRW_Color)

            boxcanvas = self.matrix.SwapOnVSync(boxcanvas)

            playerOneColor = graphics.Color(255, 0, 0)
            playerTwoColor = graphics.Color(255, 255, 0)

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
            while(AISWITCH[0] == 0):
                if(self.endGame(player) is True):
                    break
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
                            boxcanvas = self.matrix.SwapOnVSync(boxcanvas)
                            break
                    elif(not rightInput):
                        start = time.time()
                        while time.time() - start < 0.5:
                            boxcanvas = self.matrix.SwapOnVSync(boxcanvas)
                            continue
                        if((chip_row_x1 == board_bound_right) and (chip_row_x2 == board_bound_right)):
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
                        start = time.time()
                        while time.time() - start < 0.5:
                            boxcanvas = self.matrix.SwapOnVSync(boxcanvas)
                            continue


	                # if the column is full, you don't want to change players or the chipColor
                        if(board[amtOfRow - 1][colValue] is Piece.BLANK):
                            # call function to add a piece into the board
                            addPieceFunc = addPiece()
                            addPieceFunc.run(boxcanvas, colValue, player)
                            if(self.endGame(player) is False):
                                if(player is Piece.RED):
                                    chipColor = playerTwoColor
                                    player = Piece.YELLOW
                                    break
                                else:
                                    chipColor = playerOneColor
                                    player = Piece.RED
                                    break
                            else:
                                # if there is a winning combo
                                boxcanvas.Clear()
                                boxcanvas = self.matrix.SwapOnVSync(boxcanvas)
                                self.endMessage()
                        else:
                            break
                    else:
                        break 
                
            # while loop for AI
            while(AISWITCH[0] == 1):
                if(self.endGame(player) is True):
                    break
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
                    # For 1P, we want to have the AI make a move when it is there turn (player = YELLOW)
                    if(player is Piece.YELLOW):
                        # call comMove
                        colValueAI = self.comMove()
                        if(board[amtOfRow - 1][colValueAI] is Piece.BLANK or (board[amtOfRow - 1][colValueAI] is not Piece.RED and board[amtOfRow - 1][colValueAI] is not Piece.YELLOW)):
                            # call function to add a piece into the board
                            addPieceFunc = addPiece()
                            addPieceFunc.run(boxcanvas, colValueAI, player)
                            if(self.endGame(player) is False):
                                chipColor = playerOneColor
                                player = Piece.RED
                            else:
                                # if there is a winning combo
                                boxcanvas.Clear()
                                boxcanvas = self.matrix.SwapOnVSync(boxcanvas)
                                self.endMessage()
                    leftInput = GPIO.input(18)
                    rightInput = GPIO.input(19)
                    selectInput = GPIO.input(25)
                    if(not leftInput):
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
                            boxcanvas = self.matrix.SwapOnVSync(boxcanvas)
                            break
                    elif(not rightInput):
                        start = time.time()
                        while time.time() - start < 0.5:
                            boxcanvas = self.matrix.SwapOnVSync(boxcanvas)
                            continue
                        if((chip_row_x1 == board_bound_right) and (chip_row_x2 == board_bound_right)):
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
                        start = time.time()
                        while time.time() - start < 0.5:
                            boxcanvas = self.matrix.SwapOnVSync(boxcanvas)
                            continue

	                # if the column is full, you don't want to change players or the chipColor
                        if(board[amtOfRow - 1][colValue] is Piece.BLANK):
                            # call function to add a piece into the board
                            addPieceFunc = addPiece()
                            addPieceFunc.run(boxcanvas, colValue, player)
                            if(self.endGame(player) is False):
                                if(player is Piece.RED):
                                    chipColor = playerTwoColor
                                    player = Piece.YELLOW
                                    break
                                else:
                                    chipColor = playerOneColor
                                    player = Piece.RED
                                    break
                            else:
                                #start = time.time()
                                #while time.time() - start < 4:
                                #    boxcanvas = self.matrix.SwapOnVSync(boxcanvas)
                                #    continue
                                # if there is a winning combo
                                boxcanvas.Clear()
                                boxcanvas = self.matrix.SwapOnVSync(boxcanvas)
                                self.endMessage()
                        else:
                            break
                    else:
                        break 
                
            break

        # now we want to clear the canvas and show the End Message
        #start = time.time()
        #while time.time() - start < 4:
        #    boxcanvas = self.matrix.SwapOnVSync(boxcanvas)
        #    continue
        boxcanvas.Clear()
        boxcanvas = self.matrix.SwapOnVSync(boxcanvas)
        self.endMessage()



# function for adding a piece into the board
# to call, you need to initialize it to a variable
# then do variable.run(canvas, columnValue, player)
class addPiece(SampleBase):
    def __init__(self, *args, **kwargs):
        super(addPiece, self).__init__(*args, **kwargs)

    def run(self, canvas, column, player): 
        # color of player's chips
        playerOneColor = graphics.Color(255,0,0) # red
        playerTwoColor = graphics.Color(255, 255, 0) # yellow

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
            
            if(column >= 0 and column < amtOfCol):
                for row in range(amtOfRow):
                    if(board[amtOfRow-1][column] is not Piece.BLANK):
                        break
                    if(board[row][column] == Piece.BLANK):
                        board[row][column] = player
                        if(player == Piece.RED):
                            graphics.DrawLine(canvas, original_x+(column*4), original_y-(row*4), original_x+(column*4),  original_y-(row*4)+1, playerOneColor)
                            graphics.DrawLine(canvas, original_x+(column*4)+1, original_y-(row*4), original_x+(column*4)+1, original_y-(row*4)+1, playerOneColor)
                            break
                        elif(player == Piece.YELLOW):
                            graphics.DrawLine(canvas, original_x+(column*4), original_y-(row*4), original_x+(column*4),  original_y-(row*4)+1, playerTwoColor)
                            graphics.DrawLine(canvas, original_x+(column*4)+1, original_y-(row*4), original_x+(column*4)+1, original_y-(row*4)+1, playerTwoColor)
                            break
                break              


      # Main Function
if __name__=="__main__":
    test_official = ConnectFour()
    if (not test_official.process()):
       test_official.print_help() 
