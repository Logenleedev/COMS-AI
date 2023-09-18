import sys
from itertools import permutations
from copy import deepcopy
from queue import *

sudokuAssign = None
sudokuDomain = None
constrainList = None
sudokuConstraint = None




def AC3(sudokuAssign, sudokuDomain, constraintList):
    global sudokuConstraint
    q = Queue()

    for c in constraintList:
        q.put(c)

    while not q.empty():
        temp = q.get()
        Xi = temp[0]
        Xj = temp[1]
        
        flag = False
        for x in sudokuDomain[Xi]:
            if not any(y != x for y in sudokuDomain[Xj]):
                sudokuDomain[Xi].remove(x)
                flag = True

        if flag:
            if not sudokuDomain[Xi]:
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
    
 
    domain = [1,2,3,4,5,6,7,8,9]
    
    sudokuBoard = [['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'],
                   ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9'],
                   ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                   ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9'],
                   ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9'],
                   ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9'],
                   ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9'],
                   ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9'],
                   ['I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9']]
 
    sudokuDomain = {key:list(domain) for row in sudokuBoard for key in row}
    
    sudokuAssign = {key:0 for key in sudokuDomain}


    constraintList = []
    
    for row in sudokuBoard:       
        constraintList = constraintList + list(permutations(row,2))

    Transpose = list(map(list, zip(*sudokuBoard)))  #Transpose the
    
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
    
    sudokuConstraint = {key:list([]) for key in sudokuDomain} 

    for val in constraintList:
        sudokuConstraint[val[0]].append(val) 
    
    # print(constraintList)
    return sudokuAssign, sudokuDomain, constraintList

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


 


    a , b, c= AC3(sudukuAssignCopy, sudukuDomainCopy,  constrainListCopy)
    print(c)
   
if __name__ == "__main__":
    #Input sudoku string
    start = sys.argv[1]
    main(start)




 