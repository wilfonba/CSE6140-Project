# Implementation of Simmulated Annealing
import random
import networkx as nx
import time
import os
import random as rand
from output import printSolutionFile, printTraceFile

def LS1(inst, alg, cutOff, rSeed, G):
    i = 0 # standard iterator
    while (1 and i <= 10):
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
    C = [] # Array containing nodes in MVC

    # Simulated Annealing Parameters
    T0 = 500.0 
    beta = 3.0

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

        if (len(G.edges(C) - G.edges()) == 0): # C is a vertex cover
            tC = time.time()
            printTraceFile(len(C), tC - t0, traceFile)
            Cstar = C
        else:
            a = 50

    printSolutionFile(inst, alg, cutOff, rSeed, len(C), C)
