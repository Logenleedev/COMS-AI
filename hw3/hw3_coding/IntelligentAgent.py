

import numpy as np
from BaseAI import BaseAI
import time
from ComputerAI import ComputerAI
from random import randint
import itertools
from Grid import Grid
from Displayer import Displayer
from copy import deepcopy



playerAllowance = 0.02
playerTimeLimit = 0.2 - playerAllowance # Time Limit before Losing
playerPrevTime = 0
totDiff = 0
total_Cell = 0
MAXDEPTH = 4
playerAlarm = False
probability = 0.9
        
def playerUpdateAlarm():
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
    


def evaluateUtility(grid):    
    global playerPrevTime
    global playerTimeLimit
    global total_Cell
    global totDiff
    total_Cell = len(grid.getAvailableCells())
    h1 = total_Cell / (grid.size*grid.size)

    
    

    for i in range(grid.size - 1):
        for j in range(len(grid.map[i])):
            totDiff += abs(grid.map[i][j] - grid.map[i+1][j])

    for i in range(grid.size):
        for j in range(len(grid.map[i])-1):
            totDiff += abs(grid.map[i][j] - grid.map[i][j + 1])

   
    for row in grid.map:
        for cell in row:
            total_Cell += cell

    h2 = totDiff/(2 * total_Cell) 
    


    return h1 - h2    
    
def minPlay(grid,alpha,beta):
    global playerTimeLimit
    global playerPrevTime
    global total_Cell
    global totDiff
    global playerAlarm
   
    if grid.depth >= MAXDEPTH or (not grid.canMove()):
        return (None, evaluateUtility(grid))
        

    minUtility = np.inf
    _ = None
    

    
    for value in [2, 4]:
        for cell in grid.getAvailableCells():
            childGrid = grid.clone()
            update_depth = grid.depth + 1 
            childGrid.depth = update_depth
            childGrid.insertTile(cell,value)
            temp = maxPlay(childGrid, alpha, beta)
            utility = temp[1]

            if utility < minUtility:
                a = cell
                b = utility
                (minMove, minUtility) = (a, b)
                
            if minUtility <= alpha:
                break
            
            if minUtility < beta:
                beta = min(minUtility, beta)

            if playerAlarm == True or playerUpdateAlarm() == True:
                break
            
        if playerAlarm == True or playerUpdateAlarm() == True:
            break
                
    return (minMove, minUtility)
        
def maxPlay(grid,alpha,beta):
    global playerPrevTime
    global total_Cell
    global playerTimeLimit
    global playerAlarm
    global totDiff

    if grid.depth >= MAXDEPTH or (not grid.canMove()):
        return (None, evaluateUtility(grid))


    temp = (None, -np.inf)
    maxUtility = temp[1]
    

    
    for move in grid.getAvailableMoves():
        childGrid = grid.clone()
        update_depth = grid.depth + 1 
        childGrid.depth = update_depth
        childGrid.move(move)
        temp = minPlay(childGrid, alpha, beta)
        utility = temp[1]
        
        if utility > maxUtility:
            (maxMove, maxUtility) = (move, utility)
            
        if maxUtility >= beta:
            break
        
        if maxUtility > alpha:
            alpha = max(maxUtility, alpha)
            
        if playerAlarm == True or playerUpdateAlarm() == True:
            break
          

    return (maxMove, maxUtility)
    
class IntelligentAgent(BaseAI):        

    def getMove(self, grid):
        global playerTimeLimit
        global playerAlarm
        global total_Cell
        global totDiff
        global playerPrevTime
        playerAlarm = False
        playerPrevTime = time.process_time()
        grid.depth = 0
        temp = maxPlay(grid, -np.inf, np.inf)
 
        return temp[0]
        
        
        
        # # Selects a random move and returns it
        # moveset = grid.getAvailableMoves()
        # print(random.choice(moveset)[0])
        # return random.choice(moveset)[0] if moveset else None