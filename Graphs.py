import matplotlib.pyplot as plt
import numpy as np
#import seaborn as sns
#import pandas as pd

numActions = [47, 22, 34, 9, 9, 25, 8, 22, 12, 16, 71, 40]
time = [1322.79, 626.96, 545.77, 211.26, 141.71, 540.02, 237.30, 416.92, 
        228.17, 346.12, 1337.93, 802.91]

#Parameters
#4 forward, 9/10 right/left
#15 right, 15 right 70 forward

aMean = []
tMean = []
for i in numActions:
    aMean.append(np.average(numActions))
    tMean.append(np.average(time))
    
print(aMean[0])
print(tMean[0])

plt.figure()
plt.plot(numActions)
plt.plot(aMean)
plt.ylabel('Actions Taken', fontsize=30)
plt.xlabel('Episode',  fontsize=30)
plt.title("Actions per Episode",  fontsize=40)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.show()


plt.figure()
plt.plot(time)
plt.plot(tMean)
plt.ylabel('Time',  fontsize=30)
plt.xlabel('Episode',  fontsize=30)
plt.title("Time per Epsode",  fontsize=40)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.show()


scoresFile = open("LearningScores.txt", "r")

scores = []
for line in scoresFile:
    line = line.split()
    for i in line:
        scores.append(int(i))

plt.figure()
plt.plot(scores)
plt.ylabel('Score', fontsize=30)
plt.xlabel('Episode',  fontsize=30)
plt.title("Score per Episode",  fontsize=40)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.show()