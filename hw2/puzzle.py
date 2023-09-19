import sys
from itertools import permutations
from copy import deepcopy
from queue import *
import numpy as np

sudokuAssign = None
sudokuDomain = None
constrainList = None
sudokuConstraint = None
domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
word = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
number = ['1', '2', '3', '4', '5', '6', '7', '8', '9']




def AC3(sudokuAssign, sudokuDomain, constraintList):
    global sudokuConstraint
    q = Queue()

    for c in constraintList:
        q.put(c)

    while q.empty() == False:
        temp = q.get()
        Xi = temp[0]
        Xj = temp[1]
        
        flag = False

        for value in sudokuDomain[Xi]:
            all_match = True
            
            for other_value in sudokuDomain[Xj]:
                if other_value != value:
                    all_match = False
                    break

            if all_match:
                sudokuDomain[Xi].remove(value)
                flag = True


        if flag:
            if sudokuDomain[Xi] == []:
                return (False, sudokuAssign, sudokuDomain)
                
            neighbours = [Xk for Xi, Xk in sudokuConstraint[Xi]]
            for Xk in neighbours:

                q.put((Xk,Xi))

    for key,value in sudokuDomain.items():
        if len(value) == 1:
            sudokuAssign[key] = value[0]

    return (True, sudokuAssign, sudokuDomain)

    
    
def createSudokuCsp():
    global sudokuConstraint
    
    
    
    
    sudokuBoard = [['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'],
                   ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9'],
                   ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                   ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9'],
                   ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9'],
                   ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9'],
                   ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9'],
                   ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9'],
                   ['I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9']]
 

    sudokuDomain = {}

    for row in sudokuBoard:
        for key in row:
            sudokuDomain[key] = list(domain)
    
    # sudokuAssign = {key:0 for key in sudokuDomain}

    sudokuAssign = {}
    for key in sudokuDomain:
        sudokuAssign[key] = 0


   
    constraintList = []
    
    for row in sudokuBoard:       
        constraintList += list(permutations(row,2))

    
    Transpose = np.array(sudokuBoard).T.tolist() # use numpy array to transpose list 

    for col in Transpose:       
        constraintList += list(permutations(col, 2))
        
    #Constraints within each 3x3 square

    for row in [0,3,6]:
        for col in [0,3,6]:
            box = []
            for i in range(row, row+3):
                for j in range(col, col+3):
                    val = sudokuBoard[i][j]
                    box.append(val)

            constraintList += list(permutations(box,2))

    constraintList = list(set(constraintList))
    
   
    sudokuConstraint = {}
    for key in sudokuDomain:
        sudokuConstraint[key] = []

    

    for val in constraintList:
        xi = val[0]
        sudokuConstraint[xi].append(val) 
    
  
    return (sudokuAssign, sudokuDomain, constraintList)

def consistent(sudokuAssign, sudokuDomain, chosenKey, value):
    global sudokuConstraint
    
    constraintList = sudokuConstraint[chosenKey]
    for xi, xj in constraintList:
        if value == xj:
            return False 
    return True

def inference(X, D, chosenKey, value):
    

    global sudokuConstraint
    
    constraintList = sudokuConstraint[chosenKey]
    for xi, xj in constraintList:
        check = xj
        if X[check] == 0: 
            if value in D[check]:
                D[check].remove(value)
            else:
                if D[check] == []: 
                    return (False, X, D)
    return (True, X, D)
    
def backtracking(X, D):  

    flag = True
    
    for key, value in X.items():
        if value == 0:
            flag = False

    if flag:
        return (flag, X, D)

    chosenKey = None
    MRV = 10000
    for row in word:
        for col in number:
            hash_key = row + col
            if X[hash_key] == 0: #Consider only unassigned variables
                value = D[hash_key]
                if len(value) < MRV:
                    MRV = min(MRV, len(value))
                    chosenKey = hash_key 

    for value in D[chosenKey]:
        if consistent(X, D, chosenKey, value):
            X_New = deepcopy(X)
            D_New = deepcopy(D)
            X_New[chosenKey] = value
            D_New[chosenKey] = [value]

            a, b, c= inference(X_New, D_New, chosenKey, value)
            if a == True:
                resultBTS = backtracking(b,c)
                if resultBTS[0] == True:
                    return resultBTS
    return (False, X, D)

    






def main(sudokuStrStart):
    temp = createSudokuCsp()
    sudokuAssign = temp[0]
    sudokuDomain = temp[1]
    constrainList = temp[2]

  


    index = -1
    letter_head = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    number_head = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in letter_head:
        for j in number_head:
            hash = i + j
            index += 1
            sudokuAssign[hash] = int(sudokuStrStart[index])
            if int(sudokuStrStart[index]) != 0:
                sudokuDomain[hash] = [int(sudokuStrStart[index])]
    
    sudukuAssignCopy = deepcopy(sudokuAssign)
    sudukuDomainCopy = deepcopy(sudokuDomain)
    constrainListCopy = deepcopy(constrainList)


 


    ref , new_assign, new_domain= AC3(sudukuAssignCopy, sudukuDomainCopy,  constrainListCopy)
    algo_name_1 = 'AC3'
 

    if ref:
        sudokuAssign = new_assign
        sudokuDomain = new_domain

    flag = True

    
    # if flag is False, then use BTS
    for key, value in new_assign.items():
        if value == 0:
            flag = False

    if not flag:
      
        a, b, c = backtracking(deepcopy(sudokuAssign), deepcopy(sudokuDomain))

        algo_name_1 = "BTS"

        finish_state = ''

        for i in letter_head:
            for j in number_head:
                hash = i + j
                finish_state += str(b[hash])
        finish_state += " " + algo_name_1

        # write file
        file = open("output.txt", "w")
    
        file.write(finish_state)
        file.close()

   
if __name__ == "__main__":
    #Input sudoku string
    start = sys.argv[1]
    main(start)




 