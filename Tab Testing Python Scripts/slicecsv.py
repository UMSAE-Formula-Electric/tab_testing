# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 14:21:52 2021

@author: brend
"""

#Value of the filter, higher values result in a
#smoother final curve
FILTER_N_VALUE = 10;

# import pandas as pd #Not used right now
import csv
import matplotlib.pyplot as plt

x = []
y = []

filename = input("Enter file name")

with open(filename,"r") as csvfile:
    plots=csv.reader(csvfile,delimiter=",")
    for row in plots:
        if(len(row) == 5):
            if (not row[0] == '') and (not row[1] == '') and (not row[2] == '') and (not row[4] == ''):
                try:
                    #print(row)
                    if(float(row[4]) < 9000 and float(row[4]) > 5):
                        y.append(float(row[4]))
                    else:
                        y.append(0)
                    x.append((60 * 60 * int(row[0])) + (60 * int(row[1])) + int(row[2]) + (int(row[3]) / 1000))
                except:
                    print(row)
                    print("^ THIS CAUSED A WHOOPS\n")
               
from scipy.signal import lfilter

b = [1.0 / FILTER_N_VALUE] * FILTER_N_VALUE
a = 1
yy = lfilter(b,a,y)
total = 0
nums = 0

for val in range(len(yy)):
    aVal = float(yy[val])
    if(aVal > 10 and aVal < 1000):
        #print(total)
        total = total + aVal
        #print(nums)
        nums = nums + 1
        
        
avgAmp = total / nums
print("Avg amps: {0:.4f} A".format(avgAmp))

total = 0
nums = 0

startTime = 0;
endTime = 0;


for val in range(len(x)):
    aVal = float(x[val])
    if(yy[val] > 50 and yy[val] < 5000 and startTime == 0):
        startTime = aVal
        print("Start time: {0}".format(startTime))
    
    if(startTime > 0 and yy[val] == 0 and endTime == 0):
        endTime = aVal
        print("End time: {0}".format(endTime))
        
totalTime = endTime - startTime
print("Took {0:.2f} s to fuse".format(totalTime))

avgSamples = len(x) / totalTime

print("Avg sample rate: {0:.2f} Hz".format(avgSamples))


#print(endTime)

plt.figure(dpi=200)
plt.plot(x,yy)
bound = x[int(len(x) - len(x) * 0.1)]
#plt.axis([min(x), max(x), max(y) - (max(y) * .4), max(y) * 0.8])
plt.show()
