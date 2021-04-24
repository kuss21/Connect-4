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

import random

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

def connected_three(position, player):
	#check for win vertical 
	#for col in range(amtOfCol):
		#inRow = 0
		#for index in range(amtOfRow + 1):
			#shift = (col * (amtOfRow + 1)) + index
			#if((position >> shift) & 1) == 1:
				#inRow += 1
			#else:
				#inRow = 0

			#if inRow == 3:
				#return True

	#check for win horizontal
	#for row in range(amtOfRow):
		#inRow = 0
		#for index in range(amtOfCol):
			#shift = (row) + (index * (amtOfRow + 1))
			#if((position >> shift) & 1) == 1:
				#inRow += 1
			#else:
				#inRow = 0

			#if inRow == 3:
				#return True

	#check for bottom left to top right diagonal
	#for row in range(amtOfRow + 2):
		#for col in range(amtOfCol - 1):
			#shift = row + (col * (amtOfRow + 2))
			#if((position >> shift) & 1) == 1:
				#inRow += 1
			#else:
				#inRow = 0

			#if inRow == 3:
				#return True

	#check for top left to bottom right diagonal
	#for row in range(amtOfRow):
		#for col in range(amtOfCol + 2):
			#shift = row + (col * amtOfRow)
			#if((position >> shift) & 1) == 1:
				#inRow += 1
			#else:
				#inRow = 0

			#if inRow == 3:
				#return True


	#return False

	for col in range(amtOfCol):
    	count = 0
        for row in range(amtOfRow):
#           if count == 4:
            #WIN condition
#           return True
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
                if count ==3:
                    return True
            else:
                count = 0

    #check diagonal R-L ##!!DIDN'T WORK!!##
    # SWEEP FROM R-L, CHECK OUT N AS WELL
    for col in range(amtOfCol-1,0,-1):
        count = 0
        for row in range(amtOfRow):
            for n in range(7):
                if row+n >= amtOfRow or col-n <= 0:
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
			#if board[row][col] ==player:
			for n in range(7):
				####### maybe 6 and see if row+n or col+n >amt col or row then break
				if row+n >= amtOfRow or col+n >= amtOfCol:
					break
				if board[row+n][col+n] == player:
					count += 1
					if count == 3:
						return True
				else:
					count = 0

def removePiece(board, col):
	if(board[0][col] != Piece.BLANK):
		for i in range(amtOfRow):
			if(board[i][col] == Piece.BLANK):
				board[i-1][col] = Piece.BLANK
				return
		board[amtOfRow - 1][col] = Piece.BLANK
		return

def comMove(board):
	if(connected_three(board, player) == True):
		for col in range(amtOfCol):
			addPiece(board, col, Piece.Yellow)
			if(connected_four(board, player) == True):
				removePiece(board, col)
				return col
			removePiece(board, col)

	if(connected_three(board, player) == True):
		for col in range(amtOfCol):
			addPiece(board, col, Piece.RED)
			if(connected_four(board, player) == True):
				removePiece(board, col)
				return col
			removePiece(board, col)

	return random.randint(0,9)

def colNotFull(board, col):
	if(board[amtOfRow - 1][col] == Piece.BLANK):
		return True
	else:
		return False


#everything below is not used (I think)

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

#issue was that no arguments were passed into the colNotFull. Corrections from Abbasi were noted and tweaked back to original due to our own error
#from the start
def create_Tree(treeBase, parent, tempBoard, player, leaf):
	#leaf is used to see how deep the tree will be and to have a set stopping point that can be controlled. The value of leaf has been changed
	#to try and find a depth that is deep enough to evaluate wins for the AI. Leaf is updated when create_tree is called again
	if(leaf==1):
		return
	#alternate the player color to account for turns
	if(player == Piece.RED):
		player = Piece.YELLOW
	else:
		player = Piece.RED

	#randomly select 2 column to place the current players piece. This value can be changed to increase or decrease the number of children
	#a current state has
	for i in range(10):
		#randomCol = random.randint(0,9)

		#check to see if the current state is an 4 in a row or full for either color
		if(endGame(tempBoard, Piece.RED) or endGame(tempBoard, Piece.YELLOW)):
			return

		#check to see if the current column the piece is going to be dropped in is full
		if(colNotFull(tempBoard,i)):
			#if the column is not full, add the piece to that column
			addPiece(tempBoard, i, player)

			#gets the binary state of the board 
			position = treeIdentifier(tempBoard)
			#checks to see if the binary state is already in the tree
			tempNode = tree.get_node(position)
			if(tempNode == None):
				#if the binary state is not in the tree, create the node to be added to the tree
				tree.create_node(position, position, parent=parent)
				#add the node to the tree and increase leaf ccount by 1 (which represents tree depth)
				create_Tree(treeBase, position, tempBoard, player, leaf + 1)
		#remove the temp piece that was added becasue the state with the piece is already passed through the previous function call
		removePiece(tempBoard, i)




def score_tree(board, player):
	if(endGame(board, Piece.RED) or endGame(board, Piece.YELLOW)):
		return

	for i in range(10):
		if(colNotFull(board,i)):
			addPiece(board, i, player)
			position = get_position_mask_bitmap(board, player)
			win = connected_three(position)
			removePiece(tempBoard,i)
			
			if(win == True):
				return i

	while(True)
		number = random.randint(0,9)
		if(colNotFull(board, number)):
			return random.randint(0,9)

#function used in the main code to play the game
##create_Tree()
#playGame()

#create a tree to be used for the decision tree
tree = Tree()
#set the base and get the base node to be passed into the create tree function
tree.create_node("base", "base")
node = tree.get_node("base")
#create a board to be used to keep track of the board states that the AI will go through
board = [[0 for i in range(amtOfCol)] for j in range(amtOfRow)]
for row in range(amtOfRow):
	for col in range(amtOfCol):
		board[row][col] = Piece.BLANK
#set the leaf value to 0 that will keep track of the tree's depth
leaf = 0
#start the recursive call of create_tree
create_Tree(tree, "base", board, Piece.RED, leaf)
tree.show()
#nodeList[] = Null 
nodeList=tree.children("base")
print(connected_three(nodeList[0].identifier))