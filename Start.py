import os
import time
import copy


AI_POSITION = True
PLAYER_POSITION = False

class Ai:

	outcomes = []

	def __init__(self,game):
		self.game = game
		self.lookingAt = AI_POSITION

	def isPosMine(self, x,y):
		if x<0 or y<0 or x>=len(self.board) or y>=len(self.board): return False
		if self.board[y][x] == self.lookingAt: return True
		return False		

	def isPosTheirs(self,x,y):
		if x<0 or y<0 or x>=len(self.board) or y>=len(self.board): return False	
		if self.board[y][x] == (not self.lookingAt): return True
		return False

	def findConsecutiveVertical(self,x,y):
		score = 0
		for i in range(5):
			y+=1
			if self.isPosTheirs(x,y): return 0
			if self.isPosMine(x,y): score+=1
		return score

	def findConsecutiveHorizontal(self,x,y):
		score = 0
		for i in range(5):
			x+=1
			if self.isPosTheirs(x,y): return 0
			if self.isPosMine(x,y): score+=1
		return score



	def findConsecutiveDiagonalRight(self,x,y):
		score = 0
		for i in range(5):
			x+=1
			y+=1
			if self.isPosTheirs(x,y): return 0
			if self.isPosMine(x,y): score+=1
		return score
	
	def findConsecutiveDiagonalLeft(self,x,y):
		score = 0
		for i in range(5):
			x-=1
			y+=1
			if self.isPosTheirs(x,y): return 0
			if self.isPosMine(x,y): score+=1
		return score
				
	positionFunctions = [findConsecutiveVertical,findConsecutiveHorizontal,findConsecutiveDiagonalRight,findConsecutiveDiagonalLeft]

	def getConsecutive(self):
		points = {}
		for i in range(len(self.board)):
			for j in range(len(self.board[i])):
				for positionFunction in self.positionFunctions:
					score = positionFunction(self,i,j)
					if score>0:
						if score not in points: points[score] = 1
						else: points[score] += 1
				
		return points
	def valueGameState(self,coords):
		
		self.board = self.game.board
		self.board[coords[0]][coords[1]] = True

		consecutive = self.getConsecutive()
		self.game.board[coords[0]][coords[1]] = None

		return consecutive

	def valueBoard(self,moveBoard):
		self.board = moveBoard
		return self.getConsecutive()


	def generateMoves(self,board):
		coords = set()
		for i in range(len(board)):
			for j in range(len(board)):
				if board[i][j] != None:
					cols = range(max(i-2,0),min(i+3,len(board)))
					rows = range(max(j-2,0),min(j+3,len(board)))
					points_to_add = {(p_i,p_j) for p_i in rows for p_j in cols if (p_i,p_j) not in coords and board[p_i][p_j]==None}
					coords.update(points_to_add)
		return coords

#	def getMaxKey(self,score):
#
#		return (max(score.keys()),score[max(score.keys())])


	def compareScores(self,score,highScore):
		return score>highScore

	def getScore(self,scores):
		score = 0
		for number,points in scores.items(): 
			score+= 4**number*points
		return score

	def getBestMove(self,board,movingYou):
		moves = self.generateMoves(board)
		bestMove = (None,-float("inf"))
		for move in moves:
			self.lookingAt=movingYou==AI_POSITION
			score = self.getScore(self.valueGameState(move))
			self.lookingAt = movingYou==PLAYER_POSITION
			score -= 1.5*self.getScore(self.valueGameState(move))
			if self.compareScores(score,bestMove[1]):
				bestMove = (move,score)
		
		return bestMove

	def get_best_move_from_branch(self,branch,person_moving = AI_POSITION):
		best_score = float("inf")
		best_move = None
		if person_moving:
			best_score *= -1
		if isinstance(branch,dict):
			for score in branch.values():
				move_score = self.get_best_move_from_branch(score,person_moving = (not person_moving))
				if person_moving:
					if best_score < move_score and person_moving:
						best_score = move_score
				else:
					if best_score > move_score and not person_moving:
						best_score = move_score
		else:
			best_score = branch
		return best_score
						
					

	def get_best_move_from_tree(self,tree,person_moving = AI_POSITION):

		best_move = None
		best_score = float("inf")
		if person_moving:
			best_score *= -1

		for move, branch in tree.items():
			score = self.get_best_move_from_branch(branch,person_moving = (not person_moving))
			if person_moving:
				if score >= best_score and person_moving:
					best_score = score

					best_move = move
			else:
				if score <= best_move and not person_moving:
					best_score = score
					best_move = move
		print(best_move)
		print(best_score)
		return best_move




	def thinkDownTree(self, board, stepsRemaining,personMoving=AI_POSITION):
		
		if stepsRemaining >0:
			tree = {}
			moves = self.generateMoves(board)
			for move in moves:
				movedBoard = board
				movedBoard[move[0]][move[1]] = personMoving
				#import pdb;pdb.set_trace()
				tree[move] = self.thinkDownTree(movedBoard,stepsRemaining=stepsRemaining-1,personMoving=(not personMoving))
				movedBoard[move[0]][move[1]] = None
			return tree
		else:
			#import pdb;pdb.set_trace()
			return self.getScore(self.valueBoard(board))

	def makeMove(self):
		tree = self.thinkDownTree(self.game.board,stepsRemaining=2)
		print({move: self.get_best_move_from_branch(branch) for move, branch in tree.items()})
		x = self.get_best_move_from_tree(tree)
		return x 
		

# class PenteGame:

# 	def __init__(self,game_size=15):
# 		self.gameSize = game_size
# 		self.board = [[None for i in range(self.gameSize)] for i in range(self.gameSize)]
# 		self.over = False
# 		self.ai = Ai(self)		


# 	def printBoard(self):
# 		os.system('clear')
# 		for i in range(self.gameSize):
# 			for j in range(self.gameSize):
# 				if self.board[i][j] == None: 
# 					if self.gameSize/2-.5 == i == j: print("*",end=" ")
# 					else:print("+",end=" ")
				
# 				elif self.board[i][j] == False: print("X",end=" ")
# 				else: print("O",end=" ")
# 			print("") 

# 	def moveCheck(self):
# 		pass	

# 	def makeMove(self,x,y):
# 		self.board[y][x] = False
# 		self.moveCheck()
# 		self.printBoard()

# 	def checkInput(self,input):
# 		try:
# 			input[0] = int(input[0])
# 			input[1] = int(input[1])
# 		except TypeError:
# 			print("Please Enter a corrert Position")			

# 	def makeAiMove(self,coords):
#                 self.board[coords[0]][coords[1]] = True
#                 self.moveCheck()
#                 self.printBoard()


# 	def gameLoop(self):
# 		self.printBoard()
# 		while self.over == False:
# 			move = input("Please enter your move in the format x y:").split()
		
# 			self.checkInput(move)
# 			self.makeMove(move[0],move[1])
# 			self.makeAiMove(self.ai.makeMove())
					

# # game=PenteGame()

# # game.gameLoop()
# import os
# import time
# import copy


class PenteGame:

	def __init__(self,game_size=15):
		self.gameSize = game_size
		self.board = [[None for i in range(self.gameSize)] for i in range(self.gameSize)]
		self.over = False
		self.ai = Ai(self)		


	def printBoard(self):
		os.system('clear')
		for i in range(self.gameSize):
			for j in range(self.gameSize):
				if self.board[i][j] == None: 
					if self.gameSize/2-.5 == i == j: print("*",end=" ")
					else:print("+",end=" ")
				
				elif self.board[i][j] == False: print("X",end=" ")
				else: print("O",end=" ")
			print("") 

	def moveCheck(self):
		pass	

	def makeMove(self,x,y):
		if self.board[y][x] == None:self.board[y][x] = False
		else: return False
		self.moveCheck()
		self.printBoard()
		return True

	def checkInput(self,input):
		try:
			input[0] = int(input[0])
			input[1] = int(input[1])
		except TypeError:
			print("Please Enter a corrert Position")			

	def makeAiMove(self,coords):
                self.board[coords[1]][coords[0]] = True
                self.moveCheck()
                self.printBoard()


	def gameLoop(self):
		self.printBoard()
		while self.over == False:
			move = input("Please enter your move in the format x y:").split()
				
			self.checkInput(move)
				
						
			if self.makeMove(move[0],move[1]):
				if input("Is this the move you want to make (Y/N):").lower() != 'y':
					self.board[move[1]][move[0]]=None
					self.printBoard()
				else:self.makeAiMove(self.ai.makeMove())
					

game=PenteGame()

game.gameLoop()


