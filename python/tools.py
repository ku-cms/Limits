# tools.py

import os
import csv
import numpy as np

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

# linear function
def f_linear(m, b, x):
    return m * x + b

# get slope (m) and y-intercept (b) given two points
def get_params_linear(point_1, point_2):
    x_1 = point_1[0]
    y_1 = point_1[1]
    x_2 = point_2[0]
    y_2 = point_2[1]
    m = 0.0
    b = 0.0
    if x_1 == x_2:
        print("ERROR: x_1 = x_2 = {0}; cannot get params.".format(x_1))
    else:
        m = (y_2 - y_1) / (x_2 - x_1)
        b = (y_1 * x_2 - y_2 * x_1) / (x_2 - x_1)
    return [m, b]

# for an x value, get closest two data points on either side in x
def getNeighbors(x, data):
    neighbors = []
    
    diff_1  = 1e10
    diff_2  = 1e10
    point_1 = [0.0, 0.0]
    point_2 = [0.0, 0.0]
    set_point_1 = False
    set_point_2 = False
    
    for point in data:
        point_x = point[0]
        diff    = point_x - x 
        if diff < 0:
            if abs(diff) < diff_1:
                diff_1      = abs(diff)
                point_1     = point
                set_point_1 = True
        if diff > 0:
            if abs(diff) < diff_2:
                diff_2      = abs(diff)
                point_2     = point
                set_point_2 = True
    
    if set_point_1:
        neighbors.append(point_1)
    else:
        print("ERROR: Did not set point 1 for x = {0}".format(x))
    if set_point_2:
        neighbors.append(point_2)
    else:
        print("ERROR: Did not set point 2 for x = {0}".format(x))
    
    return neighbors

# get x, y values from data
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

# Get flat data: set y values to mean y value over a specified range
def getFlatData(data, x_range):
    result  = []
    x_min   = x_range[0]
    x_max   = x_range[1]
    y_vals  = [row[1] for row in data if x_min < row[0] < x_max]
    y_mean  = np.mean(y_vals)
    #print("y_vals = {0}".format(y_vals))
    print("In getFlatData(): y_mean = {0:.3f} over the x range {1}".format(y_mean, x_range))
    for row in data:
        x = row[0]
        if x_min < x < x_max:
            y = y_mean
            new_row = [x, y]
            result.append(new_row)
        else:
            result.append(row)
    return result

# Get linear smooth data: for x step size, set y values using linear fit between two points
def getLinearSmoothData(data, x_range, step):
    result  = []
    # assume integer values
    x_min   = x_range[0]
    x_max   = x_range[1]
    for x in range(x_min, x_max + 1):
        if x == x_min or x == x_max or x % step == 0:
            # get closest points on either side of x value
            neighbors   = getNeighbors(x, data)
            if len(neighbors) == 2:
                # for two neighbors, use a line to find y value
                point_1     = neighbors[0]
                point_2     = neighbors[1]
                # get parameters for a line between these points
                params  = get_params_linear(point_1, point_2)
                m       = params[0]
                b       = params[1]
                # get y value on line for x value
                y       = f_linear(m, b, x)
                new_row = [x, y]
                print("x: {0}, point_1: {1}, point_2: {2}, new_row: {3}".format(x, point_1, point_2, new_row))
                result.append(new_row)
            elif len(neighbors) == 1:
                # for one neighbor, use that point's y value
                point   = neighbors[0]
                y       = point[1]
                new_row = [x, y]
                print("x: {0}, point: {1}, new_row: {2}".format(x, point, new_row))
                result.append(new_row)
            elif len(neighbors) == 0:
                # for zero neighbors, print error 
                print("ERROR: No neighbors found for x = {0}".format(x))
    for row in data:
        x = row[0]
        if x > x_max: 
            result.append(row)
    return result


