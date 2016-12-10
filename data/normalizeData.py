# Teerapat Jenrungrot
# CL57 Fall 2016

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dataFrame = pd.read_csv("data_corelab.csv")

set(dataFrame['Species'])

# Use only Fence lizard and side-blotched 
dataFrame = dataFrame[dataFrame['Species'].notnull()]
dataFrame['StandardizedSpecies'] = np.nan

# Fence lizards
for name in ['Baby Fence', 'Fence', 'Juvenile Fence', \
             'Juvenile Western Fence', 'Western Fence']:
    dataFrame.loc[dataFrame['Species'] == name, 'StandardizedSpecies'] = 'Fence'

# Side-blotched lizards
for name in ['Juvenile Side-Blotched', 'Side-Blotched']:
    dataFrame.loc[dataFrame['Species'] == name, 'StandardizedSpecies'] = 'Side-Blotched'
    
# Remove any other types of lizards
dataFrame = dataFrame.drop('Species', axis=1)
dataFrame = dataFrame[dataFrame['StandardizedSpecies'].notnull()]

temp_hr = pd.to_datetime(dataFrame['Time']).dt.hour % 12 + 12
temp_min1 = (pd.to_datetime(dataFrame['Time']).dt.minute / 10).astype(int)
temp_min2 = pd.to_datetime(dataFrame['Time']).dt.minute % 10
temp_min = temp_min1.astype(str).str.cat(temp_min2.astype(str), sep="")
temp_combined = temp_hr.astype(str).str.cat(temp_min.astype(str), sep=':')
dataFrame['normalizedTime'] = temp_combined
dataFrame = dataFrame.drop('Time', axis=1)

dataFrame['Sun conditions'] = dataFrame['Sun conditions'].str.capitalize()
dataFrame.loc[dataFrame['Sun conditions'] == 'Sun', 'Sun conditions'] = 'Sunny'
dataFrame['Normalized Sun conditions'] = np.nan

# Sunny
for name in ['Full sun', 'Partial sun', 'Sunny']:
    dataFrame.loc[dataFrame['Sun conditions'] == name, 'Normalized Sun conditions'] = 'Sun'

for name in ['Overcast']:
    dataFrame.loc[dataFrame['Sun conditions'] == name, 'Normalized Sun conditions'] = 'Overcast'
    
# Shade
for name in ['Partial shade', 'Shade']:
    dataFrame.loc[dataFrame['Sun conditions'] == name, 'Normalized Sun conditions'] = 'Shade'

dataFrame = dataFrame[dataFrame['Normalized Sun conditions'].notnull()]
set(dataFrame['Normalized Sun conditions'])

dataFrame = dataFrame.drop(dataFrame.columns[0:2].append(dataFrame.columns[4:7]), axis=1)
cols = [dataFrame.columns[3], 
        dataFrame.columns[2], 
        dataFrame.columns[0], 
        dataFrame.columns[1], 
        dataFrame.columns[4]]


dataFrame = dataFrame[cols]
dataFrame.columns = ['Time','Species','Temperature','Height','Condition']

dataFrame.to_csv( "normalizedData.csv", index=False)