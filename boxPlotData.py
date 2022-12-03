import numpy as np
import os
import glob
import csv
from itertools import zip_longest

trials = 25
INST = ['star2','power']
cutOff = 10
ALG = ['LS1','LS2']
nBins = 11*cutOff


for inst in INST:
    for alg in ALG:
        if inst == 'star2':
            exact = 4452
            if alg == 'LS1':
                qualities = [4.0,4.2,4.4,4.6,4.8,5.0]
            else:
                qualities = [2.8,3.0,3.2,3.4,3.6,3.8]
        else:
            exact = 2203
            if alg == 'LS1':
                qualities = [0.6,0.8,1.0,1.2,1.4,1.6]
            else:
                qualities = [1.0,1.2,1.4,1.6,1.8,2.0]
            
        bins = np.zeros((nBins,100))
        count = np.zeros((nBins,100))

        f = open(alg + "_bins.txt",'w')
        traces = []
        data = []
        path = 'OutputFiles/' + inst + '_' + alg + '*.trace'
        for name in glob.glob(path):
            traces.append(name)
        for i in range(100):
            f = open(traces[i])
            for line in f:
                t = line.split(', ')
                for i in range(2):
                    t[i] = float(t[i].replace("\n",""))
                t[1] = ((t[1]-exact)/exact)*100
                data.append(t)

        bd = [[],[],[],[],[],[]]
        for q in range(6):
            for d in data:
                if abs(d[1] - qualities[q]) < 0.05:
                    print(d[1])
                    bd[q].append(d[0])

        filename = inst + "_" + alg + "_boxData.csv"
        with open(filename,"w+") as f:
            writer = csv.writer(f)
            writer.writerow(qualities)
            for values in zip_longest(*bd):
                writer.writerow(values)