# Implementation of Simmulated Annealing
import random
import networkx as nx
import time
import os
import random as rand
from output import printTraceFile
import math
import collections as col

def getScore(C, G, gSE):
    cost = len(gSE) - len(G.edges(C))
    return cost

def LS1(inst, alg, cutOff, rSeed, G):
    i = 0 # standard iterator
    while (1 and i <= 100):
        if os.path.exists("OutputFiles/" + inst + "_" + alg + "_" + str(cutOff) + "_" + \
                str(rSeed) + "_" + str(i) + ".trace"):
            i = i + 1
            print("Here")
        else:
            traceFile = open("OutputFiles/" + inst + "_" + alg + "_" + str(cutOff) + "_" + \
                str(rSeed) + "_" + str(i) + ".trace", "x")
            break

    G1 = G.copy() # Copy of G for greedy IC
    gSD = sorted(G1.degree, key=lambda x: x[1], reverse=True)
    gSE = sorted([sorted(i) for i in list(G.edges())])
    gN = sorted(G.nodes())
    N = len(G.nodes())
    C = [] # Array containing nodes in MVC

    # Simulated Annealing Parameters
    T0 = 5.0 
    beta = 2

    # Initialize stopwatch
    t0 = time.time()
    
    # Determine an IC using Maximum Degree Greedy, C is a VC of the original G
    while (len(nx.edges(G1)) > 0): 
        G1.remove_node(gSD[0][0])
        C.append(gSD[0][0])
        gSD.remove(gSD[0])

    # Simulated annealing iteration
    while ((time.time() - t0) < cutOff):
        T = T0*(1 - int(cutOff)/(time.time() - t0))**beta # update temperature

        if (sorted([sorted(i) for i in list(G.edges(C))]) == gSE): # C is a vertex cover
            tC = time.time()
            printTraceFile(len(C), tC - t0, traceFile)
            Cstar = C
            C.pop(random.randrange(len(C)))
        else:
            Cscore = getScore(C, G, gSE)

            v = gN[random.randrange(len(gN))]
            
            Ct = C.copy()
            if (v in C):
                Ct.remove(v)
                degFactor = 1 - len(G.edges(v))/N
            else:
                Ct = Ct + [v]
                degFactor = 1 + len(G.edges(v))/N

            Ctscore = getScore(Ct, G, gSE)

            if Ctscore < Cscore:
                C = Ct.copy()
            else:
                if math.exp(min((Cscore - Ctscore)*degFactor/T,1)) > random.random():
                    C = Ct.copy()

    return Cstar