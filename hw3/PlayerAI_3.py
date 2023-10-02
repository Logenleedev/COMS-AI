# -*- coding: utf-8 -*-

import time
import numpy as np
import itertools
from random import randint
from copy import deepcopy
from BaseAI_3 import BaseAI
from Grid_3 import Grid
from Displayer_3  import Displayer
from ComputerAI_3 import ComputerAI



playerAllowance = 0.02
playerTimeLimit = 0.2 - playerAllowance # Time Limit before Losing
playerPrevTime = 0
totDiff = 0
totCell = 0
playerAlarm = False
probability = 0.9
MAXDEPTH = 4
        
def playerUpdateAlarm():
    global playerTimeLimit
    global playerPrevTime
    global playerAlarm
    if abs(time.process_time() - playerPrevTime) >= playerTimeLimit:
        playerAlarm = True
    else: 
        playerAlarm = False
    return playerAlarm
    
def terminalTest(grid):
    global MAXDEPTH
    if grid.depth >= MAXDEPTH or (not grid.canMove()):
        return True
    else:
        return False  

def evaluateUtility(grid):    

    global totCell
    global totDiff
    totCell = len(grid.getAvailableCells())
    h1 = totCell/(grid.size*grid.size)

    
    

    for i in range(grid.size - 1):
        for j in range(len(grid.map[i])):
            totDiff += abs(grid.map[i][j] - grid.map[i+1][j])

    for i in range(grid.size):
        for j in range(len(grid.map[i])-1):
            totDiff += abs(grid.map[i][j] - grid.map[i][j + 1])

   
    for row in grid.map:
        for cell in row:
            totCell += cell

    h2 = totDiff/(2*totCell) #Divided by 2 to ensure maximum normalised value is 1
    


    return h1 - h2    
    
def minPlay(grid,alpha,beta):
    global playerTimeLimit
    global playerPrevTime
    global playerAlarm
   
    if terminalTest(grid) == True:
        return (None, evaluateUtility(grid))
        

    (_, minUtility) = (None, np.inf)
    

    
    for value in [2, 4]:
        for cell in grid.getAvailableCells():
            childGrid = grid.clone()
            childGrid.depth = grid.depth + 1 #Increment the depth of node
            childGrid.insertTile(cell,value)
            temp = maxPlay(childGrid, alpha, beta)
            utility = temp[1]

            if utility < minUtility:
                (minMove, minUtility) = (cell, utility)
                
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
    global playerTimeLimit
    global playerPrevTime
    global playerAlarm

    if terminalTest(grid) == True:
        return (None, evaluateUtility(grid))


    temp = (None, -np.inf)
    maxUtility = temp[1]
    

    
    for move in grid.getAvailableMoves():
        childGrid = grid.clone()
        childGrid.depth = grid.depth + 1 
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
    
class PlayerAI(BaseAI):        
    def __init__(self):      
        pass
        
    def getMove(self, grid):
        global playerTimeLimit
        global playerPrevTime
        global playerAlarm
        playerAlarm = False
        playerPrevTime = time.process_time()
        grid.depth = 0
        temp = maxPlay(grid, -np.inf, np.inf)
        return temp[0]