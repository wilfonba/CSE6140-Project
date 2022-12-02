import random
import networkx as nx
import time
import os
import random as rand
from output import printTraceFile
import math
import collections as col
import numpy as np
import sys
from utils import checker
import csv

###############################################################

def getMaxDegreeEdge(E, G1) -> tuple:
    maxDegree = 0
    max_u, max_v = -1, -1
    for e in E:
        u, v = e[0], e[1]
        u_degree = G1.degree[u]
        v_degree = G1.degree[v]
        degree = u_degree + v_degree
        if maxDegree < degree:
            maxDegree = degree 
            max_u = u 
            max_v = v
    return max_u, max_v

###############################################################

def greedyIC(G, nE):
    GT = G.copy()
    E = GT.edges()
    VC = []
    while(len(E) != 0):
        E = GT.edges()
        (u,v) = getMaxDegreeEdge(E, GT)
        
        GT.remove_node(u)
        GT.remove_node(v)

        VC.append(u)
        VC.append(v)   
    return VC

###############################################################

def removeNode(VC,ucE,dscores,v,G,eWS,confChange):
    dscores[int(v)-1] = -dscores[int(v)-1]
    confChange[int(v)-1] = 0
    for u in G.neighbors(v):
        if u not in VC:
            ucE.append((str(v),str(u)))
            ucE.append((str(u),str(v)))
            confChange[int(u)-1] = 1
            dscores[int(u)-1] += eWS[str(v)][str(u)]
        else:
            dscores[int(u)-1] -= eWS[str(v)][str(u)]

###############################################################

def addNode(VC,ucE,dscores,v,G,eWS,confChange):
    dscores[int(v)-1] = -dscores[int(v)-1]
    for u in G.neighbors(str(v)):
        if u not in VC:
            ucE.remove((str(v),str(u)))
            ucE.remove((str(u),str(v)))
            dscores[int(u)-1] -= eWS[str(v)][str(u)]
            confChange[int(u)-1] = 1
        else:
            dscores[int(u)-1] += eWS[str(v)][str(u)]

###############################################################    

def LS1(inst, alg, cutOff, rSeed, G):
    i = 0 # standard iterator
    while (1 and i <= 100):
        if os.path.exists("OutputFiles/" + inst + "_" + alg + "_" + str(cutOff) + "_" + \
                str(rSeed) + "_" + str(i) + ".trace"):
            i = i + 1
        else:
            traceFile = open("OutputFiles/" + inst + "_" + alg + "_" + str(cutOff) + "_" + \
                str(rSeed) + "_" + str(i) + ".trace", "x")
            break

    nV = len(G.nodes) # number of nodes
    nE = len(G.edges) # number of edges
    ucE = [] # array of uncovered edges

    gamma = 0.5*nV # mean edge weight for forgetting
    rho = 0.3 # "forget" parameter

    eWS = nx.convert.to_dict_of_dicts(G, edge_data=1)
    dScores = [0]*(nV)
    confChange = [1]*(nV)

    #VC1 = greedyIC(G, nE)
    VC = list(G.nodes())

    with open('VCIC.txt', newline='') as f:
        reader = csv.reader(f)
        VC1 = list(reader)

    VC1 = VC1[0]

    for i in G.nodes():
        if i not in VC1:
            removeNode(VC, ucE, dScores, str(i), G, eWS, confChange)
            VC.remove(str(i))

    t0 = time.time()

    while (time.time() - t0 < cutOff):
        while len(ucE) == 0:
            printTraceFile(len(VC), time.time() - t0, traceFile)
            VCStar = VC.copy()
            maxC = -float('inf')
            for v in VC:
                if dScores[int(v)-1] > maxC:
                    maxC = dScores[int(v)-1]
                    optV = v
            removeNode(VC,ucE,dScores,str(optV),G,eWS,confChange)
            VC.remove(optV)

        # Step 1: Remove node with max improvement
        maxC = -float('inf')
        for v in VC:
            if dScores[int(v)-1] > maxC:
                maxC = dScores[int(v)-1]
                optV = v
        removeNode(VC,ucE,dScores,str(optV),G,eWS,confChange)
        VC.remove(optV)

        # Step 2: Add node from random uncovered edge
        rE = random.choice(ucE)
        rE = [int(rE[0]),int(rE[1])]
        if confChange[rE[0]-1] == 0 and rE[1] not in VC: 
            bV = rE[1]
        elif confChange[rE[1]-1] == 0 and rE[0] not in VC:
            bV = rE[0]
        else:
            if dScores[rE[0]-1] > dScores[rE[1]-1]:
                bV = rE[0]
            else:
                bV = rE[1]

        addNode(VC,ucE,dScores,bV,G,eWS,confChange)
        VC.append(str(bV))

        # Update edge weights and score functions
        for e in ucE:
            eWS[e[0]][e[1]] += 1				
            dScores[int(e[0])-1] += 1

        # Calculate mean edge weight
        total = int(0)
        for e in G.edges():
            total += int(eWS[e[0]][e[1]])
        mW = total/len(eWS)

        # Update edge weights
        if mW > gamma:
            dScores = [0]*(nV+1)
            ucE = []
            VC1 = VC
            VC = list(G.nodes())
            
            for i in G.nodes():
                if i not in VC1:
                    removeNode(VC, ucE, dScores, str(i), G, eWS, confChange)
                    VC.remove(str(i))
            for e in G.edges():
                eWS[e[0]][e[1]] = rho*eWS[e[0]][e[1]]

    print("Result: " + str(len(VCStar)))
    checker(G,VCStar)
    return VCStar