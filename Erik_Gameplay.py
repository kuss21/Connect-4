#variables for size of board, if changed, need to fix the array for the board in playGame()
amtOfRow = 7
amtOfCol = 6
from enum import Enum, unique
@unique
class Piece(Enum):
	BLANK = 1
	RED = 2
	YELLOW = 3

#functions
#drawBoard draws the current state of the board, the board that is passed stores ' ', 'X', and 'O' 
#and will print what is in each postion of the array (needs to be changed later to zeros and ones for
#encoding and memory optimization)
def drawBoard(boardToPrint):
	for row in range(amtOfRow):
		line = '|'
		for col in range(amtOfCol):
			if(boardToPrint[row][col] == Piece.BLANK):
				line += ' '
			elif(boardToPrint[row][col] == Piece.RED):
				line += 'O'
			elif(boardToPrint[row][col] == Piece.YELLOW):
				line += 'X'
			line += '|'
		print(line)
	print('-----------------')

#add Piece adds the 'piece' (string of the player, either 'X' or 'O') into the column specified
def addPiece(currentBoard, column, player):
	for row in range(amtOfRow):
		if(currentBoard[amtOfRow - row - 1][column] == Piece.BLANK):
			currentBoard[amtOfRow - row - 1][column] = player
			return

#playPiece waits for a user to input a valid column to put the piece in the board using addPiece
def playPiece(currentBoard, player):
	while(1):
		print('Enter a Column')
		col = int(input())
		if(col >= 0 and col < amtOfCol):
			addPiece(currentBoard, col, player)
			return

#endGame checks to see if the game is done by seeing if there are any empty spaces left (currently doesn't
#check for wins (lines of four))
def endGame(currentBoard):
	for row in range(amtOfRow):
		for col in range(amtOfCol):
			if(currentBoard[row][col] == Piece.BLANK):
				return False
	return True

#set up for a virtual implementation of Connect Four for testing AI or other needs
#to use playGame, needs the functions under the AI section and a 'playGame()' function call
#playGame currently does not find wins, and does not have check if the column is already full (turn for that 
#piece will be lost and next players turn will occur)
#to stop the current iteration of playGame before the board is full, enter any non integer character in the
#command line and hit enter and an error will occur
def playGame():
	#variable for board, need to change for different sizes of boards, also need to change 'amtOfRow' and 'amtOfCol'
	board = [[Piece.BLANK, Piece.BLANK, Piece.BLANK, Piece.BLANK, Piece.BLANK, Piece.BLANK], 
		   [Piece.BLANK, Piece.BLANK, Piece.BLANK, Piece.BLANK, Piece.BLANK, Piece.BLANK], 
           [Piece.BLANK, Piece.BLANK, Piece.BLANK, Piece.BLANK, Piece.BLANK, Piece.BLANK],
           [Piece.BLANK, Piece.BLANK, Piece.BLANK, Piece.BLANK, Piece.BLANK, Piece.BLANK],
           [Piece.BLANK, Piece.BLANK, Piece.BLANK, Piece.BLANK, Piece.BLANK, Piece.BLANK],
           [Piece.BLANK, Piece.BLANK, Piece.BLANK, Piece.BLANK, Piece.BLANK, Piece.BLANK],
           [Piece.BLANK, Piece.BLANK, Piece.BLANK, Piece.BLANK, Piece.BLANK, Piece.BLANK],
           [Piece.BLANK, Piece.BLANK, Piece.BLANK, Piece.BLANK, Piece.BLANK, Piece.BLANK]]
	playerTurn = Piece.RED

	while(endGame(board) == False):
		playPiece(board, playerTurn)
		drawBoard(board)

		#test for wins (ai code)
		#, gameMask = get_position_mask_bitmap(board, playerTurn)
		#if(connected_four(gamePosition) == True):
		#	print('True')
		#else:
		#	print('False')


		if(playerTurn == Piece.RED):
			playerTurn = Piece.YELLOW
		else:
			playerTurn = Piece.RED

playGame()
