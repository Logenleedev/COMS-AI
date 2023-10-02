import sys
import numpy as np
import csv 
from collections import namedtuple
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

splitset = None


def algorithms(kernelChoice):
    global splitset
    

    if kernelChoice == 'linear':
        parameters = {'kernel': ('linear',), 'C': [0.1, 0.5, 1, 5, 10, 50, 100]}
        estimator = svm.SVC()

    elif kernelChoice == 'poly':
        parameters = {'kernel': ('poly',), 'C': [0.1, 1, 3], 'degree': [4, 5, 6], 'gamma': [0.1, 0.5]}
        estimator = svm.SVC()

    elif kernelChoice == 'rbf':
        parameters = {'kernel': ('rbf',), 'C': [0.1, 0.5, 1, 5, 10, 50, 100], 'gamma': [0.1, 0.5, 1, 3, 6, 10]}
        estimator = svm.SVC()

    elif kernelChoice == 'logisticregression':
        parameters = {'C': [0.1, 0.5, 1, 5, 10, 50, 100]}
        estimator = LogisticRegression()

    elif kernelChoice == 'knn':
        parameters = {'n_neighbors': range(1, 51), 'leaf_size': range(5, 61, 5)}
        estimator = KNeighborsClassifier()

    elif kernelChoice == 'decisiontrees':
        parameters = {'max_depth': range(1, 51), 'min_samples_split': range(2, 11)}
        estimator = DecisionTreeClassifier()

    elif kernelChoice == 'randomforest':
        parameters = {'max_depth': range(1, 51), 'min_samples_split': range(2, 11)}
        estimator = RandomForestClassifier()

    
    clf = GridSearchCV(estimator, parameters, cv=5, n_jobs=10)
    clf.fit(splitset.X_train, splitset.y_train)
    print(kernelChoice, clf.best_estimator_)
    classifier = clf.best_estimator_

    trainScoreBest = clf.best_score_

    testScore = classifier.score(splitset.X_test, splitset.y_test)
    return trainScoreBest, testScore 

def main():  

    

    data = np.genfromtxt(sys.argv[1], delimiter=",",skip_header=1) #skip header while reading


    X = data[:,:-1] 
    y = data[:,-1]


    dataset = namedtuple('dataset', 'X_train X_test y_train y_test')

    output = train_test_split(X, y, test_size=0.4, random_state=42, stratify = y)
    global splitset
    splitset = dataset._make(output)

    file = open('output3.csv','w',newline='')
    writer = csv.writer(file)    

    
    #Call various learning algorithm
    train, test = algorithms('linear')
    writer.writerow(['svm_linear', train, test])
    
    train, test = algorithms('poly')
    writer.writerow(['svm_polynomial', train, test])

    train, test = algorithms('rbf')
    writer.writerow(['svm_rbf', train, test])

    train, test = algorithms('logisticregression')
    writer.writerow(['logistic', train, test])
    
    train, test = algorithms('knn')
    writer.writerow(['knn', train, test])

    train, test = algorithms('decisiontrees')
    writer.writerow(['decision_tree', train, test])

    train, test = algorithms('randomforest')
    writer.writerow(['random_forest', train, test])

    file.close()
    
if __name__ == "__main__":
    main()
