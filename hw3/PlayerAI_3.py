# -*- coding: utf-8 -*-

import time
import numpy as np
import itertools
from random import randint
from BaseAI_3 import BaseAI
from Grid_3 import Grid
from Displayer_3  import Displayer
from ComputerAI_3 import ComputerAI

actionDic = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT"
}

playerAllowance = 0.02
playerTimeLimit = 0.2 - playerAllowance # Time Limit before Losing
playerPrevTime = 0
playerAlarm = False
tileValues = [2, 4]
probability = 0.9
MAXDEPTH = 4
        
def playerUpdateAlarm():
    global playerPrevTime
    global playerTimeLimit
    global playerPrevTime

    diff = abs(time.process_time() - playerPrevTime)

    if diff >= playerTimeLimit:
        playerAlarm = True
    else:
        playerAlarm = False

    
def terminalTest(grid):
    if grid.depth >= MAXDEPTH:
        return True
        
    if not grid.canMove():
        return True
    
    return False 
 

def evaluateUtility(grid):    
    aviableCells = len(grid.getAvailableCells())
    heuristic1 = aviableCells / (grid.size ** 2)

    totDiff = 0

    for i in range(grid.size - 1):
        for j in range(len(grid.map[i])):
            totDiff += abs(grid.map[i][j] - grid.map[i+1][j])

    # Along each row
    for i in range(grid.size):
        for j in range(len(grid.map[i])-1):
            totDiff += abs(grid.map[i][j] - grid.map[i][j + 1])

    totCell = 0
    for row in grid.map:
        for cell in row:
            totCell += cell
    
    h2 = totDiff / (2 * totCell)
    
    return heuristic1 - h2

    
def minPlay(grid,alpha,beta):
    pass
        
def maxPlay(grid,alpha,beta):
    pass
class PlayerAI(BaseAI):        
    def __init__(self):      
        pass
        
    def getMove(self, grid):
        pass

'''        
def getNewTileValue():
    if randint(0,99) < 100 * probability:
        return tileValues[0]
    else:
        return tileValues[-1];        
        
if __name__ == '__main__':
    g = Grid()
#    g.map[0][0] = 2
#    g.map[1][0] = 2
#    g.map[3][0] = 4
    
    g.map =[[2,  0,  0,  0],
            [2,  0,  0,  0],
            [0,  0,  0,  0],
            [0,  0,  0,  0]]

    computer = ComputerAI()
    player = PlayerAI()
    displayer = Displayer()
    key = 'a'
    
    while key != 'q' and g.canMove():
        for i in g.map:
            print(i)
        print('-------')
        print(g.getAvailableMoves())
        print('-------')

        #Player turn    
        newMove = player.getMove(g)
        print("Current Move: " + actionDic[newMove])
        g.move(newMove)
        
        #Computer turn
        newMove = computer.getMove(g)
        g.setCellValue(newMove, getNewTileValue())

        #Wait for user verification
        print("User input to continue")
#        key = input()              
'''