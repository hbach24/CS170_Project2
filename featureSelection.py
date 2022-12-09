#Summary of the project: search through feature tree and find the set of feature(s) that provide the best accuracy
import csv 
import random
import copy
import math
import time

def main():
    # file = "Small_Data_6.txt"
    # file = "Small_Data_88.txt"
    # file = "Small_Data_96.txt"
    # file = "Large_Data_6.txt" #41 columns, 40 feature columns
    # file = "Large_Data_21.txt"
    # file = "Large_Data_96.txt"


    print("Welcome to Hannah Bach's Feature Selection Algorithm.")
    file = input("Type in the name of the file to test: ")
    data = getData(file)
    numRows = len(data)
    numFeat = len(data[0])-1

    search = input("Type the number of the algorithm you want to run: \
    \n\tEnter '1' to use Forward Selection. \n\tEnter '2' to use Backward Elimination.\n")

    print(f"This dataset has {numFeat} features (not including the class attribute), with {numRows} objects.")
    
    allFeatSet = []
    for k in range(1,numFeat+1):
        allFeatSet.append(k)
    # print(allFeatSet)
    print(f"Running nearest neighbor with all {numFeat} features, using 'leaving-one-out' evaluation, I get an accuracy of {round(leaveOneOutCrossValidation(data, allFeatSet, 0, -1)*100, 2)}%\n")   

    print("BEGINNING SEARCH.")    
    if(search == '1'):
        searchName = "Forward Selection"
        duration = time.time()
        forwardSelectionSearch(data,file)
        t1 = time.time() - duration
        print("Time elapsed: ", round(t1,4), "seconds")
    

    if(search == '2'):
        searchName = "Backward Elimination"
        duration = time.time()
        backwardEliminationSearch(data,file)
        t1 = time.time() - duration
        print("Time elapsed: ", round(t1,4), "seconds")

#REFERENCE: https://stackoverflow.com/questions/16448912/counting-number-of-columns-in-text-file-with-python
def getData(file):
    with open(file) as f:
        reader = csv.reader(f, delimiter=' ', skipinitialspace=True)
        first_row = next(reader)
        numFeatures = len(first_row) - 1 #subtract 1 to remove the first column representing the classes
        numRows = len(f.readlines())+1

        f.seek(3) #https://www.geeksforgeeks.org/python-seek-function/; set an offset of 3 since data starts at index 3 for each line
        data = []
        
        for i in range(numRows):
            rawRow = f.readline().split()
            # print(rawRow)
            dataRow = []
            for j in range(len(rawRow)):
                dataRow.append(float(rawRow[j])) #convert scientific notation to float; REFERENCE: https://stackoverflow.com/questions/23636509/convert-string-in-scientific-notation-to-float
            data.append(dataRow)
    return data

#k-fold cross validation
def leaveOneOutCrossValidation(data, currentFeatureSet, featureToAdd, searchFlag):
    numRows = len(data) #total num of objects in data set
    numFeat = len(data[0])-1

    numberCorrectlyClassified = 0
    currentFS = copy.copy(currentFeatureSet)

    if(searchFlag == True): #forward selection search
        currentFS.append(featureToAdd)

    elif(searchFlag == False): #backward elimination search
        currentFS.remove(featureToAdd)

    #Perform k-fold cross validation
    for i in range(numRows):
        objectToClassify = data[i][1:] #only take the features; i is the object/row
        classObjectToClassify = int(data[i][0])
        
        # print(f"Looping over i, at the {i+1} location.")
        # print(f"The {i+1}th object is in class {classObjectToClassify}")
        nearestNeighborDistance = float('inf')
        nearestNeighborLocation = float('inf')
        nearestNeighborLabel = -1

        for k in range(numRows): #classify by comparing object i to every other object in the dataset
            sum = 0
            distance = 0
            if(k!=i): #make sure not to be comparing the curr object i with itself
                # print(f"Ask if {i+1} is the nearest neighbor of {k+1}")

                #Calculating the Euclidean Distance between object i and object k using only the features in the current feature set
                for j in range(len(currentFS)):
                    featureNum = currentFS[j]
                    sum += pow((data[i][featureNum] - data[k][featureNum]), 2)

                distance = math.sqrt(sum)
                if(distance < nearestNeighborDistance):
                    nearestNeighborDistance = distance
                    nearestNeighborLocation = k
                    nearestNeighborLabel = int(data[k][0])

        if(classObjectToClassify == nearestNeighborLabel):
            numberCorrectlyClassified +=1
    accuracy = numberCorrectlyClassified/numRows
    return accuracy


def forwardSelectionSearch(data,file):
    numFeatures = len(data[0])
    # print(numFeatures-1)

    currentFeatureSet = []
    bestFeatureSetOverall = []
    bestFeatureSetAccuracy = float('-inf')
   
   #START SEARCH
    for i in range(1,numFeatures): #disregard the first column since it's not a feature but a class
        # print(f"\nOn the {i}th level of the search tree.")
        featureToAdd = 0
        bestAccuracy = 0
        
        for k in range(1,numFeatures):

            if(k not in currentFeatureSet): #don't add a feature that's already in the current feature set
                # print(f"--Considering adding the {k} feature.") ****
                accuracy = leaveOneOutCrossValidation(data, currentFeatureSet, k, True) #gets the accuracy if we were to add feature k to our current existing feature set
                tempFeatureSet = copy.copy(currentFeatureSet)
                tempFeatureSet.append(k)
                print(f"Using feature(s) {tempFeatureSet} accuracy is {round(accuracy*100, 2)}%")
                
                if(accuracy > bestAccuracy): #<-- picks best feature for each level
                    bestAccuracy = accuracy
                    featureToAdd = k

        currentFeatureSet.append(featureToAdd) #<-- picks best feature set for each level
        print(f"Feature set {currentFeatureSet} was best, accuracy is {round(bestAccuracy*100, 2)}%\n")
        
        if(bestAccuracy > bestFeatureSetAccuracy): #<-- finds best feature set from all levels
            bestFeatureSetOverall = copy.copy(currentFeatureSet)
            bestFeatureSetAccuracy = bestAccuracy

        # print(f"On level {i}, I added feature {featureToAdd} to the current feature set.")
        # print(f"Current Feature Set at level {i}:", currentFeatureSet, "\n")
    print("\nFinished Search!!!")
    print(f"The best feature set is {bestFeatureSetOverall} with an accuracy of {round(bestFeatureSetAccuracy*100, 2)}% for dataset {file}.")


def backwardEliminationSearch(data,file):
    numFeatures = len(data[0])
    # print(numFeatures-1)

    currentFeatureSet = []
    for k in range(1,numFeatures):
        currentFeatureSet.append(k)
    print("Starting with feature set:", currentFeatureSet, "\n")
    tempFeatureSet = copy.copy(currentFeatureSet)


    bestFeatureSetOverall = []
    bestFeatureSetAccuracy = leaveOneOutCrossValidation(data, tempFeatureSet, 0, -1) #need to consider the full set's accuracy before removing features
   
    print(f"Using feature(s) {tempFeatureSet} accuracy is {round(bestFeatureSetAccuracy*100, 2)}%")
    print(f"Feature set {tempFeatureSet} was best, accuracy is {round(bestFeatureSetAccuracy*100, 2)}%\n")

   #START SEARCH
    for i in range(1,numFeatures): #disregard the first column since it's not a feature but a class
        # print(f"\nOn the {i}th level of the search tree.")
        featureToRemove = 0
        bestAccuracy = 0
        for k in range(1,numFeatures):

            if(k in currentFeatureSet): #don't remove a feature that's not in the current feature set
                tempFeatureSet = copy.copy(currentFeatureSet)
                tempFeatureSet.remove(k)

                if(len(tempFeatureSet) != 0): #ignore an empty feature set
                    accuracy = leaveOneOutCrossValidation(data, currentFeatureSet, k, False) #gets the accuracy if we were to add feature k to our current existing feature set
                
                    print(f"Using feature(s) {tempFeatureSet} accuracy is {round(accuracy*100, 2)}%")
                    
                    if(accuracy > bestAccuracy):
                        bestAccuracy = accuracy
                        featureToRemove = k

        if(len(currentFeatureSet) != 1):
            currentFeatureSet.remove(featureToRemove)
            print(f"Feature set {currentFeatureSet} was best, accuracy is {round(bestAccuracy*100, 2)}%\n")
        
        if(bestAccuracy > bestFeatureSetAccuracy): #<-- finds best feature set from all levels
            bestFeatureSetOverall = copy.copy(currentFeatureSet)
            bestFeatureSetAccuracy = bestAccuracy

    print("Finished Search!!!")
    print(f"The best feature set is {bestFeatureSetOverall} with an accuracy of {round(bestFeatureSetAccuracy*100, 2)}% for dataset {file}.")


if __name__ == '__main__':
    main()