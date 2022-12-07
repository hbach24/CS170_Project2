#Summary of the project: search through feature tree and find the set of feature(s) that provide the best accuracy
import csv 
import random

def main():
    print("Welcome to Hannah Bach's Feature Selection Algorithm.")
    search = input("Type the number of the algorithm you want to run: \
    \nEnter '1' to use Forward Selection. \nEnter '2' to use Backward Elimination.\n")
    # search  = 0 #delete this later and uncomment lines 6&7

    file = "Small_Data_6.txt"
    # file = "Small_Data_88.txt"
    # file = "Small_Data_96.txt"
    # file = "Large_Data_6.txt" #41 columns, 40 feature columns
    # file = "Large_Data_21.txt"
    # file = "Large_Data_96.txt"
    data = getData(file)

    if(search == '1'):
        searchName = "Forward Selection"
        forwardSelectionSearch(data)

    if(search == '2'):
        searchName = "Backward Elimination"
        backwardEliminationSearch(1)

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
        # print(data)
    return data

def leaveOneOutCrossValidation(data, currentFeatureSet, featureToAdd):
    acc = random.random()
    return acc

def forwardSelectionSearch(data):
    numFeatures = len(data[0])
    # print(numFeatures-1)

    currentFeatureSet = []
   
    for i in range(1,numFeatures): #disregard the first column since it's not a feature but a class
        print(f"On the {i}th level of the search tree.")
        featureToAdd = 0
        bestAccuracy = 0
        
        for k in range(1,numFeatures):

            if(k not in currentFeatureSet): #don't add a feature that's already in the current feature set
                print(f"--Considering adding the {k} feature.")
                accuracy = leaveOneOutCrossValidation(data, currentFeatureSet, k)

                if(accuracy > bestAccuracy):
                    bestAccuracy = accuracy
                    featureToAdd = k
        
#level 1: currentFeatureSet = [4] ; level 2: currentFeatureSet = [4,5] 
            # feature = data[i][j]
        currentFeatureSet.append(featureToAdd)
        print(f"On level {i}, I added feature {featureToAdd} to the current feature set.")
        print(f"Current Feature Set at level {i}:", currentFeatureSet, "\n")



def backwardEliminationSearch(data):
    print("backward")


if __name__ == '__main__':
    main()