#Summary of the project: search through feature tree and find the set of feature(s) that provide the best accuracy
import csv 

def main():
    print("Welcome to Hannah Bach's Feature Selection Algorithm.")
    # search = input("Type the number of the algorithm you want to run: \
    # \nEnter '1' to use Forward Selection. \nEnter '2' to use Backward Elimination.\n")
    search  = 0 #delete this later and uncomment lines 6&7

    # file = "Small_Data_6.txt"
    # file = "Small_Data_88.txt"
    # file = "Small_Data_96.txt"
    # file = "Large_Data_6.txt" #41 columns, 40 feature columns
    file = "Large_Data_21.txt"
    # file = "Large_Data_96.txt"
    data = getData(file)

    if(search == '1'):
        searchName = "Forward Selection"
        forwardSelectionSearch(1)

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
        print(data)
    return data



def forwardSelectionSearch(data):
    print("forward")

def backwardEliminationSearch(data):
    print("backward")


if __name__ == '__main__':
    main()