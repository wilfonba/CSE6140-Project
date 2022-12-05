# This file reads trace files and creates a table in LaTeX's tabular
# syntax for use for the comprehensive time analysis section of the report

import os
import random as r
import glob
import numpy as np

trials = 10
graphs = []
path = 'DATA/*.graph'
for name in glob.glob(path):
    name = name.split('.')[0]
    name = name.split('/')[1]
    graphs.append(name)
print(graphs)
graphs.remove('dummy1')
graphs.remove('dummy2')

exactSols = {'jazz' : 158, 'karate' : 14, 'football' : 94, 'as-22july06' : 3303, \
            'hep-th' : 3926, 'star' : 6902, 'star2' : 4542, 'netscience' : 899, \
            'email' : 594, 'delaunay_n10' : 703, 'power' : 2203}

dataOut = []
for i in range(len(graphs)):
    dataOut.append([])
for i in range(len(graphs)):
    dataOut[i].append(graphs[i])
    for j in range(12):
        dataOut[i].append(0)

ALG = ['Approx','LS1','LS2']
for alg in ALG:
    algIdx = ALG.index(alg)
    for inst in graphs:
        instIdx = graphs.index(inst)
        traces = []
        path = 'OutputFiles/timeTrials/' + inst + '_' + alg + '*.trace'
        for name in glob.glob(path):
            traces.append(name)
        
        d = []
        for j in range(len(traces)):
            d.append([])

        i = 0
        for trial in traces:
            f = open(trial)
            for line in f:
                line = line.replace('\n','')
                line = line.split(',')
                d[i].append([float(line[0]),int(line[1])])
            i += 1

        worstSol = float(0)
        for i in range(10):
            if d[i][len(d[i])-1][1] > worstSol:
                worstSol = d[i][len(d[i])-1][1]

        times = []
        for i in range(10):
            for j in range(len(d[i])):
                if d[i][j][1] == worstSol and len(times) <= 10:
                    times.append(d[i][j][0])
        
        print(len(times), alg, inst, len(times))
        print(dataOut)
        dataOut[instIdx][3*algIdx+1] = np.mean(times)
        dataOut[instIdx][3*algIdx+2] = worstSol
        dataOut[instIdx][3*algIdx+3] = (worstSol - exactSols[inst])/exactSols[inst]*100

f = open("timeData.txt","x")
for i in range(len(graphs)):
    line = ''
    line += dataOut[i][0]
    line += ' & '
    for j in range(len(alg)):
        line += str('%4.4f' % dataOut[i][j*3+1])
        line += ' & '
        line += str(int(dataOut[i][j*3+2]))
        line += ' & '
        line += str('%.4f' % dataOut[i][j*3+3])
        line += ' & '
    line += "\\\\ \n"
    f.write(line)