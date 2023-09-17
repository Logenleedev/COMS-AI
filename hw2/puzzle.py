import sys
from itertools import permutations
def createSudokuCsp():
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

    sudokuDomain = {}
    for row in sudokuBoard:
        for key in row:
            sudokuDomain[key] = list(domain)

    sudokuAssign = {}
    for key in sudokuDomain:
        sudokuAssign[key] = 0
    
    constrainList = []

    # Row constraints
    for row in sudokuBoard:
        constrainList += list(permutations(row, 2))

    transpose = list(zip(*sudokuBoard))

  
    # col constraints
    for col in transpose:
        constrainList += list(permutations(col, 2))

    # grid constraits

    for row_start in [0, 3, 6]:
        for col_start in [0, 3, 6]:
            box = []
            for i in range(row_start, row_start + 3):
                for j in range(col_start, col_start + 3):
                    box.append(sudokuBoard[i][j])
            constrainList += list(permutations(box, 2))
    constrainList = list(set(constrainList))        
  
    sudokuConstrain = {key:[] for key in sudokuDomain} 
   
    for val in constrainList:
        sudokuConstrain[val[0]].append(val) 
    


    return sudokuAssign, sudokuDomain, constrainList

def main(sudokuStrStart):
    createSudokuCsp()


if __name__ == "__main__":
    #Input sudoku string
    start = sys.argv[1]
    main(start)




 