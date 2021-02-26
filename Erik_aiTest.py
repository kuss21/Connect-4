#virtual Connect Four board for AI testing
#variables for size of board, if changed, need to fix the array for the board in playGame()
amtOfRow = 6
amtOfCol = 10
from enum import Enum, unique
@unique
class Piece(Enum):
	BLANK = 1
	RED = 2
	YELLOW = 3
import sys
print(sys.getrecursionlimit())

#variables used for decision tree
#count = 0

#functions
#drawBoard draws the current state of the board, the board that is passed stores ' ', 'X', and 'O' 
#and will print what is in each postion of the array (needs to be changed later to zeros and ones for
#encoding and memory optimization)
def drawBoard(boardToPrint):
	for row in range(amtOfRow):
		line = '|'
		for col in range(amtOfCol):
			if(boardToPrint[amtOfRow - row - 1][col] == Piece.BLANK):
				line += ' '
			elif(boardToPrint[amtOfRow - row - 1][col] == Piece.RED):
				line += 'O'
			elif(boardToPrint[amtOfRow - row - 1][col] == Piece.YELLOW):
				line += 'X'
			line += '|'
		print(line)
	print('-----------------')

#add Piece adds the 'piece' (string of the player, either 'X' or 'O') into the column specified
def addPiece(currentBoard, column, player):
	for row in range(amtOfRow):
		if(currentBoard[row][column] == Piece.BLANK):
			currentBoard[row][column] = player
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
def endGame(currentBoard, player):
	if(connected_four(get_position_mask_bitmap(currentBoard, player))):
		return True

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
	#https://www.geeksforgeeks.org/python-using-2d-arrays-lists-the-right-way/
	#used for creating a dynamic 2d array 
	board = [[0 for i in range(amtOfCol)] for j in range(amtOfRow)]
	for row in range(amtOfRow):
		for col in range(amtOfCol):
			board[row][col] = Piece.BLANK

	playerTurn = Piece.RED

	while(endGame(board, playerTurn) == False):
		if(playerTurn == Piece.RED):
			playerTurn = Piece.YELLOW
		else:
			playerTurn = Piece.RED

		playPiece(board, playerTurn)
		drawBoard(board)

		print(bin(combineTwoBitMask(board)))


		#used for testing




#AI Parts
#changing an array into a bitstring
#code is referenced from TowardsDataScience.com
def get_position_mask_bitmap(board, player):
	bitmap = ""
	for col in range (0, amtOfCol, 1):
		for row in range (0, amtOfRow, 1):
			if board[row][col] == player:
				bitmap = "1" + bitmap
			else:
				bitmap = "0" + bitmap
		#add an extra zero into the bitstring to help with checking for diagonal wins
		#this is similar to adding an extra row full of blanks 
		bitmap = "0" + bitmap
	return int(bitmap, 2)


#check for wins on the board
#code is referenced from TowardsDataScience.com
def connected_four(position):
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

#recursive code to make a decision tree
from treelib import Node, Tree

def treeIdentifier(board):
	bitmap = ""
	for col in range (0, amtOfCol, 1):
		for row in range (0, amtOfRow, 1):
			if board[row][col] == Piece.RED:
				bitmap = "R" + bitmap
			elif board[row][col] == Piece.YELLOW:
				bitmap = "Y" + bitmap
			else:
				bitmap = "O" + bitmap
	return bitmap

def colNotFull(board, col):
	if(board[amtOfRow - 1][col] == Piece.BLANK):
		return True
	else:
		return False

#issue was that no arguments were passed into the colNotFull. Corrections from Abbasi were noted and tweaked back to original due to our own error
#from the start
def create_Tree(treeBase, parent, tempBoard, player, leaf):
	#the .copy function is suppose to make a shallow
	if(player == Piece.RED):
		player = Piece.YELLOW
	else:
		player = Piece.RED

	for i in range(amtOfCol):

		if(endGame(tempBoard, Piece.RED) or endGame(tempBoard, Piece.YELLOW)):
			print("end game found")
			return
		if(colNotFull(tempBoard,i)):

			#used to print out the two boards(original and temp) to keep track of what is happening

			addPiece(tempBoard, i, player)
			print("temp")
			drawBoard(tempBoard)
			position = treeIdentifier(tempBoard)
			tempNode = tree.get_node(position)
			if(tempNode == None):
				tree.create_node(position, position, parent=parent)
				if(leaf == 100):
					return
				create_Tree(treeBase, position, tempBoard, player, leaf + 1)
		removePiece(tempBoard, i)


def removePiece(board, col):
	if(board[0][col] != Piece.BLANK):
		for i in range(amtOfRow):
			if(board[i][col] == Piece.BLANK):
				board[i-1][col] = Piece.BLANK
				return
		board[amtOfRow - 1][col] = Piece.BLANK
		return


#function used in the main code to play the game
##create_Tree()
#playGame()

tree = Tree()
tree.create_node("base", "base")
node = tree.get_node("base")
board = [[0 for i in range(amtOfCol)] for j in range(amtOfRow)]
for row in range(amtOfRow):
	for col in range(amtOfCol):
		board[row][col] = Piece.BLANK
leaf = 0
create_Tree(tree, "base", board, Piece.RED, leaf)
tree.show()
#file = open("tree.txt", "w")
#file.write(tree.show())
#file.close()



