

import numpy as np
from BaseAI import BaseAI
import time
from ComputerAI import ComputerAI
from random import randint
import itertools
from Grid import Grid
from Displayer  import Displayer
from copy import deepcopy



playerAllowance = 0.02
playerTimeLimit = 0.2 - playerAllowance 
playerPrevTime = 0
totDiff = 0
total_Cell = 0
MAXDEPTH = 5
playerAlarm = False



class helper:
    # Helper class for IntelligentAgent
    
    '''
     * Evaluates the utility of the given grid state.
     * Higher utility = better state.
     * Utility is based on:
     * - Number of empty cells (more empty cells = higher utility)
     * - Monotonicity of grid values (monotonic = higher utility) 
     * - Tile values in corners (higher values in corners = higher utility)
    '''
    def playerUpdateAlarm(self):
        # Checks if the time limit for the player's turn has been exceeded, 
        # and sets the playerAlarm flag accordingly. Uses global variables 
        # for the previous turn time, time limit, and playerAlarm flag.

        global playerPrevTime
        global playerTimeLimit
        global MAXDEPTH
        global totDiff
        global playerAlarm
        difference = abs(time.process_time() - playerPrevTime)
        if  difference >= playerTimeLimit:
            playerAlarm = True
        else: 
            playerAlarm = False
        return playerAlarm
        


    def evaluateUtility(self, grid):
        """
          Evaluates the utility of the given grid state for 2048.
          
          Higher utility indicates a better game state. Utility is calculated
          based on:
          
          - Number of empty cells (more empty cells = higher utility)  
          - Monotonicity of grid values (monotonic = higher utility)
          - Tile values in corners (higher corner values = higher utility)
          
          Parameters:
            grid (Grid): The game grid to evaluate
          
          Returns:
            int: The utility score for the given grid state  
        """
          
        score = 0

        # Add score for empty cells
        for row in grid.map:
            for cell in row:
                if cell == 0:
                    score += 1

        # Add score for monotonicity
        for row in range(3):
            for col in range(3):
                if grid.map[row][col] >= grid.map[row][col+1]:
                    score += 1
                if grid.map[col][row] >= grid.map[col+1][row]:  
                    score += 1

        # Add score based on position 
        weights = [[20, 7, 5, 1], 
                    [10, 5, 2, 1],
                    [5, 2, 1, 0.5],
                    [2, 1, 0.5, 0.2]]
                    
        for row in range(4):
            for col in range(4):
                score += weights[row][col] * grid.map[row][col]

        return score
        
    def minPlay(self, grid, alpha, beta):
        # Minimax search for minimizing player 
        
        global playerTimeLimit
        global playerPrevTime
        global total_Cell
        global totDiff
        global playerAlarm
   
    
        if grid.depth >= MAXDEPTH or (not grid.canMove()):
            return (None, self.evaluateUtility(grid))
            

        minUtility = np.inf
        _ = None
        
       
        
        for value in [2, 4]:
            for cell in grid.getAvailableCells():
                childGrid = grid.clone()
                update_depth = grid.depth + 1 
                childGrid.depth = update_depth
                childGrid.insertTile(cell,value)
                temp = self.maxPlay(childGrid, alpha, beta)
                utility = temp[1]

                if utility < minUtility:
                    a = cell
                    b = utility
                    (minMove, minUtility) = (a, b)
                    
                if minUtility <= alpha:
                    break
                
                if minUtility < beta:
                    beta = min(minUtility, beta)

                if playerAlarm == True or self.playerUpdateAlarm() == True:
                    break
                
            if playerAlarm == True or self.playerUpdateAlarm() == True:
                break
                    
        return (minMove, minUtility)
       
    def get_moveList(self, input):
        '''
         * Converts a list of move tuples to a list of just the move directions.
         * 
         * @param input List of move tuples, each containing (direction, utility)
         * @return List containing just the move directions
        '''

        temp = []

        for element in input:
            temp.append(element[0])
        
        return temp
        
    def maxPlay(self, grid, alpha, beta):
        # Maximize player's utility by recursively generating possible moves up to MAXDEPTH or until no moves are possible. Performs alpha-beta pruning to avoid exploring less optimal branches. Returns the optimal move and its utility.
        
        global playerPrevTime
        global total_Cell
        global playerTimeLimit
        global playerAlarm
        global totDiff

        if grid.depth >= MAXDEPTH or (not grid.canMove()):
            return (None, self.evaluateUtility(grid))


        temp = (None, -np.inf)
        maxUtility = temp[1]
        
        moveList = self.get_moveList(grid.getAvailableMoves())

        for move in moveList:
            childGrid = grid.clone()
            update_depth = grid.depth + 1 
            childGrid.depth = update_depth
            childGrid.move(move)
            temp = self.minPlay(childGrid, alpha, beta)
            utility = temp[1]
            
            if utility > maxUtility:
                (maxMove, maxUtility) = (move, utility)
                
            if maxUtility >= beta:
                break
            
            if maxUtility > alpha:
                alpha = max(maxUtility, alpha)
                
            if playerAlarm == True or self.playerUpdateAlarm() == True:
                break
            
        
        return (maxMove, maxUtility)

    
class IntelligentAgent(BaseAI):
           
    """
    Evaluates the next move for the Intelligent Agent player in the 2048 game. 
    Performs minimax search with alpha-beta pruning to find the optimal move.
    """
    def getMove(self, grid):
        global playerTimeLimit
        global playerAlarm
        global total_Cell
        global totDiff
        global playerPrevTime
        playerAlarm = False
        playerPrevTime = time.process_time()
        grid.depth = 0
        help = helper()
        temp = help.maxPlay(grid, -np.inf, np.inf)

        return temp[0]
        