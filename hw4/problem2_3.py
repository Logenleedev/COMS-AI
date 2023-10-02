import sys
import numpy as np
import csv 

alpha = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 0.98]
iteration = [100] * len(alpha)


def linearRegression(inputFile, inputX, inputLabel, mean, std):
    global alpha
    global iteration
    weight_size = inputX.shape[1]
    weight = np.zeros(weight_size)


    file = open('output2.csv','w',newline='')
    writer = csv.writer(file)

    for alpha, iterationMax in zip(alpha,iteration):
        risk = []
        
        for _ in range(iterationMax):
           
            fx = inputX.dot(weight)
            risk.append((1/(2*inputX.shape[0]))*sum((fx-inputLabel.flatten())**2))
            #Update weight vector
            temp1 = (fx[:, None] - inputLabel).flatten()
           
            temp2 = (inputX*temp1[:,None]).sum(axis=0)

            
            weight = weight - (alpha / iterationMax) * temp2
        # Initialize temp variables
        val = [alpha, iterationMax] 

        for w in weight:
            val.append(w)

        writer.writerow(val)
    file.close()

    

def normalizeData(arr):


    normalized = np.empty_like(arr)
    mean = np.mean(arr, axis=0)
    std = np.std(arr, axis=0)
    normalized = (arr - mean) / std
    
    return normalized, mean, std
def main():  

    inputFile = np.genfromtxt(sys.argv[1], delimiter=',')

    inputTemp = inputFile[:,:-1]

    inputTemp, mean, std = normalizeData(inputTemp)

    inputX = np.c_[np.ones(inputFile.shape[0]), inputTemp]

    inputLabel = inputFile[:,-1:]

    linearRegression(inputFile, inputX, inputLabel, mean, std)
    
if __name__ == "__main__":
    main()
