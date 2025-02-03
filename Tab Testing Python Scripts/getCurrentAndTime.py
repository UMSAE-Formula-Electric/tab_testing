#Value of the filter, higher values result in a
#smoother final curve
FILTER_N_VALUE = 10

UPDATE_FREQUENCY = 10

# a value that filters out the noisy (lower) current values
# 50 seems to be a good value to filter out lower values but keep the overall average similar
CURRENT_BOUNDARY_CONDITION = 50

# import pandas as pd #Not used right now
import csv
# import matplotlib.pyplot as plt

#Converts a time string to a number of seconds where you can take a difference
def convertTime(time):
    time_l = time.split(":")
    return (float(time_l[0]) * 3600) + (float(time_l[1]) * 60) + (float(time_l[2])) + (float(time_l[3]) / 1000)


def isFloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

# def validStopTime(numTicks, currentValue):
#     validStopTime += numTicks
#     return validStopTime

def currentTickSum(currentValue, currSum):
    currSum += currentValue
    return currSum

x = []
y = []
readingCurrent = False

CurrentTimePairs = []
runSum = 0
runCount = 0
startTime = 0
stopTime = 0

filename = input("Enter file name\n> ")

validStopTime = False

# potentialStopTime is a time that could be correct IF the next 10 current values sum to zero
potentialStopTime = 0
ticks = 0
currSum = 0
prevCurrent = 0

timeString = ""
# comment this code block for -------
#-------------------------------------------------
# csvfile = open(filename,"r")

# data=csv.reader(csvfile,delimiter=",")
# with open(filename, "r") as csvfile:
#     for x in csvfile:
#         x.replace("\0", "")
#-------------------------------------------------

with open(filename, "r") as csvfile:
    
    #reader = csv.reader(x.replace('\0', '') for x in csvfile) # comment this later
    data=csv.reader(csvfile,delimiter=",")
    for line in data:
        if len(line) != 0:
            if line[0][0] == '[':
                vals = line[0].strip().split("]")
                output = vals[1].strip()

                if(isFloat(output)):
                    current = float(output)

                    ticks = ticks + 1
                    currSum = currentTickSum(current, currSum)
                    
                    # if the sum of UPDATE_FREQUENCY consecutive time values (ticks) equals 0 (currSum == 0), and we aren't at the start of the file (ticks != 0 and startTime != 0)
                    # if 10 (UPDATE_FREQUENCY value) consecutive 'ticks' of zeros (sum zero 10 times and get zero), then this is a valid stop time
                    if (ticks % UPDATE_FREQUENCY == 0 and ticks != 0 and currSum == 0 and startTime != 0):
                        validStopTime = True
                    
                    # reset current sum for every UPDATE_FREQUENCY number of ticks
                    if (ticks % UPDATE_FREQUENCY == 0):
                        currSum = 0
                    
                    #time = vals[0].split("-")[1].strip()
                    time = vals[0].replace("[", "")
                    if(readingCurrent == False):
                        if(current > CURRENT_BOUNDARY_CONDITION):    #Starting a new run (CHANGE BACK TO current > 0 LATER)
                            runSum += current
                            runCount += 1
                            startTime = convertTime(time)
                            print(time + " (START time)") #remove later (used for debugging purposes)
                            readingCurrent = True
                    else:
                        if(current > 0 or currSum > 0):    #Continuing the run
                            runSum += current

                            #if (current > 0):
                            
                            if (current > CURRENT_BOUNDARY_CONDITION):
                                runCount += 1
                                potentialStopTime = convertTime(time)
                                timeString = time
                        elif (prevCurrent > CURRENT_BOUNDARY_CONDITION): #to prevent the random zeros between data readings to count as a STOP time
                            validStopTime = False
                            
                        else:               #Stopping the run
                            if (validStopTime):
                                stopTime = potentialStopTime
                            
                                CurrentTimePairs.append([runSum/runCount, stopTime - startTime])    #Add the last run
                                readingCurrent = False
                                validStopTime = False
                                print(timeString + " (END time)") #remove later (used for debugging purposes)
                        prevCurrent = current
    

highestTimeDelta = 0
index = 0

for i in range(len(CurrentTimePairs)):
    if(CurrentTimePairs[i][1] > highestTimeDelta):
        highestTimeDelta = CurrentTimePairs[i][1]
        index = i

print(CurrentTimePairs)
print("Average Current: {:.2f} amps\nTime to break: {:.3f} seconds".format(CurrentTimePairs[index][0], CurrentTimePairs[index][1]))




                            




        
"""               
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

"""