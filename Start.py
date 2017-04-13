import os
import time
import copy

AI_POSITION = True
PLAYER_POSITION = False



class Ai:
    outcomes = []

    def __init__(self, board, score, score_vs, player, round):
        self.board = board
        self.score = score
        self.score_vs = score_vs
        self.player = player
        self.round = round
        self.lookingAt = AI_POSITION

    def isPosMine(self, x,y):
        if self.board[x][y] == self.player:
            return True
        else:
            return False
        #if x<0 or y<0 or x>=len(self.board) or y>=len(self.board): return False
        #if self.board[y][x] == self.lookingAt: return True
        #return False


    def isPosTheirs(self,x,y):
        if self.board[x][y] != self.player and self.board[x][y] != 0:
            return True
        else:
            return False
        #if x<0 or y<0 or x>=len(self.board) or y>=len(self.board): return False
        #if self.board[y][x] == (not self.lookingAt): return True
        #return False


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
        self.board = self.board
        self.board[coords[0]][coords[1]] = True
        consecutive = self.getConsecutive()
        self.board[coords[0]][coords[1]] = None
        return consecutive


    def valueBoard(self,moveBoard):
        self.board = moveBoard
        return self.getConsecutive()


    def generateMoves(self,board):
        coords = set()
        print(len(board))
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] != 0:
                    cols = range(max(i-2,0),min(i+3,len(board)))
                    rows = range(max(j-2,0),min(j+3,len(board)))
                    points_to_add = {(p_i,p_j) for p_i in rows for p_j in cols if (p_i,p_j) not in coords and board[p_i][p_j]==0}
                    coords.update(points_to_add)
        return coords


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
                tree[move] = self.thinkDownTree(movedBoard,stepsRemaining=stepsRemaining-1,personMoving=(not personMoving))
                movedBoard[move[0]][move[1]] = None
            return tree
        else:
            return self.getScore(self.valueBoard(board))


    def makeMove(self):
        tree = self.thinkDownTree(self.board,stepsRemaining=2)
        print({move: self.get_best_move_from_branch(branch) for move, branch in tree.items()})
        x = self.get_best_move_from_tree(tree)
        return xl

    def MinMax(self):

        move_make = self.makeMove()
        print(move_make)

        return {"x": "6", "y": "7"}