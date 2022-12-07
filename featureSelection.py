#Summary of the project: search through feature tree and find the set of feature(s) that provide the best accuracy
import csv 
import random
import copy
import math

def main():
    print("Welcome to Hannah Bach's Feature Selection Algorithm.")
    search = input("Type the number of the algorithm you want to run: \
    \nEnter '1' to use Forward Selection. \nEnter '2' to use Backward Elimination.\n")
    # search  = 0 #delete this later and uncomment lines 6&7

    # file = "Small_Data_6.txt"
    file = "Small_Data_88.txt"
    # file = "Small_Data_96.txt"
    # file = "Large_Data_6.txt" #41 columns, 40 feature columns
    # file = "Large_Data_21.txt"
    # file = "Large_Data_96.txt"
    data = getData(file)
    # numRows = len(data)
    # numFeat = len(data[0])-1
    # print("numRows:", numRows, ", numFeat:", numFeat)

    if(search == '1'):
        searchName = "Forward Selection"
        forwardSelectionSearch(data,file)

    if(search == '2'):
        searchName = "Backward Elimination"
        backwardEliminationSearch(data)

#REFERENCE: https://stackoverflow.com/questions/16448912/counting-number-of-columns-in-text-file-with-python
def getData(file):
    with open(file) as f:
        reader = csv.reader(f, delimiter=' ', skipinitialspace=True)
        first_row = next(reader)
        numFeatures = len(first_row) - 1 #subtract 1 to remove the first column representing the classes
        numRows = len(f.readlines())+1

        print("Number of features:", numFeatures) #checking
        print("Number of rows:", numRows)

        f.seek(3) #https://www.geeksforgeeks.org/python-seek-function/; set an offset of 3 since data starts at index 3 for each line
        data = []
        
        for i in range(numRows):
            rawRow = f.readline().split()
            # print(rawRow)
            dataRow = []
            for j in range(len(rawRow)):
                # print(rawRow[j])
                dataRow.append(float(rawRow[j])) #convert scientific notation to float; REFERENCE: https://stackoverflow.com/questions/23636509/convert-string-in-scientific-notation-to-float
            # print(dataRow)
            data.append(dataRow)
    # print(data[2][1:], "TEST")
    # print(data[2][0], "TEST")
    return data

#k-fold cross validation
def leaveOneOutCrossValidation(data, currentFeatureSet, featureToAdd, searchFlag):
    numRows = len(data) #total num of objects in data set
    numFeat = len(data[0])-1
    # print("numRows:", numRows, ", numFeat:", numFeat)\

    numberCorrectlyClassified = 0
    currentFS = copy.copy(currentFeatureSet)
    if(searchFlag):
        currentFS.append(featureToAdd)
        print(f"Current feature set with {featureToAdd} added:", currentFS)

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
    # print(numberCorrectlyClassified)
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
        print(f"\nOn the {i}th level of the search tree.")
        featureToAdd = 0
        bestAccuracy = 0
        
        for k in range(1,numFeatures):

            if(k not in currentFeatureSet): #don't add a feature that's already in the current feature set
                print(f"--Considering adding the {k} feature.")
                accuracy = leaveOneOutCrossValidation(data, currentFeatureSet, k, True) #gets the accuracy if we were to add feature k to our current existing feature set
                
                if(accuracy > bestAccuracy):
                    bestAccuracy = accuracy
                    featureToAdd = k
                    print(bestAccuracy, f"BEST at LEVEL {i}")

        currentFeatureSet.append(featureToAdd) #<-- picks best feature set for each level

        if(bestAccuracy > bestFeatureSetAccuracy): #<-- finds best feature set from all levels
            bestFeatureSetOverall = copy.copy(currentFeatureSet)
            bestFeatureSetAccuracy = bestAccuracy

        # print(f"On level {i}, I added feature {featureToAdd} to the current feature set.")
        # print(f"Current Feature Set at level {i}:", currentFeatureSet, "\n")
    print(f"\nThe best feature set is {bestFeatureSetOverall} with an accuracy of {bestFeatureSetAccuracy} for dataset {file}.")


def backwardEliminationSearch(data):
    numFeatures = len(data[0])

    currentFeatureSet = []
    for k in range(1,numFeatures):
        currentFeatureSet.append(k)
    # print(currentFeatureSet)

    for i in range(1,numFeatures): #disregard the first column since it's not a feature but a class
        print(f"On the {i}th level of the search tree.")
        featureToRemove = 0
        bestAccuracy = 0
        
        for k in range(1,numFeatures):

            if(k in currentFeatureSet): #check if a feature k is in the current feature set
                print(f"--Considering removing the {k} feature.")
                accuracy = leaveOneOutCrossValidation(data, currentFeatureSet, k, False)

                if(accuracy > bestAccuracy):
                    bestAccuracy = accuracy
                    featureToRemove = k
                    print(bestAccuracy, "BEST")
        
        print(f"On level {i}, I removed feature {featureToRemove} from the current feature set of {currentFeatureSet}.")    
        currentFeatureSet.remove(featureToRemove)
        print(f"Current Feature Set at this level {i} after removing {featureToRemove}:", currentFeatureSet, "\n")



if __name__ == '__main__':
    main()