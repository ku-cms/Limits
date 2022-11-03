# tools.py

import os
import csv

# creates directory if it does not exist
def makeDir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

# check if string is a float
def isfloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def getXYVals(data):
    x_vals = []
    y_vals = []
    for row in data:
        x = row[0]
        y = row[1]
        x_vals.append(x)
        y_vals.append(y)
    return x_vals, y_vals

# takes a csv file as input and outputs data in a matrix
def getData(input_file):
    data = []
    with open(input_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return data

# return cleaned data:
# - only keep rows that are not emtpy and where every string entry is a float
# - convert strings to floats 
def getCleanData(data):
    result = []
    for row in data:
        skip_row = False
        # skip empty rows
        if not row:
            skip_row = True
        # skip rows that have at least one entry that is not a float
        for x in row:
            if not isfloat(x):
                skip_row = True
                break
        if skip_row:
            continue
        else:
            new_row = [float(x) for x in row]
            result.append(new_row)
    return result

# Get x=M1, y=M_1-M_2 data from x=M_1, y=M_2 data (i.e. get DM vs. M data)
def getDMvsMData(data):
    result = []
    for row in data:
        # assume m1 > m2
        m1 = row[0]
        m2 = row[1]
        x  = m1
        y  = m1 - m2
        new_row = [x, y]
        result.append(new_row)
    return result

