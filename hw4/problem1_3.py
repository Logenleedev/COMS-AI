import sys
import numpy as np
import csv 
from matplotlib import pyplot as plt

weight = None
        
def pla(inputFile, inputX, inputLabel):
    global weight
    weight_size = inputX.shape[1]
    weight = np.zeros(weight_size)
    

    file = open('output1.csv','w',newline='')
    writer = csv.writer(file)

    flag = 1

    while flag:
        flag = 0
        
        for temp in list(zip(inputX, inputLabel)):
            x, label = temp
            fxi = x.dot(weight)

            if fxi == 0:
                fxi = -1
            if label*fxi <= 0: #an error occurred
                weight = weight + label*x 
                flag = 1

        writer.writerow(weight)



         

    file.close()


                 
def main():  
    inputFile = np.genfromtxt(sys.argv[1], delimiter=',')
    inputTemp = inputFile[:, :-1]
    
    add_ones = np.ones(inputFile.shape[0])
    inputX = np.c_[inputTemp, add_ones]


    inputLabel = inputFile[:,-1:]

    pla(inputFile, inputX, inputLabel)
    
if __name__ == "__main__":
    main()
