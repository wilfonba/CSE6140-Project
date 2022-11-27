# Edge Deletion
import random
import networkx as nx
import time
import os
import random as rand
from output import printTraceFile
import math
import collections as col
from utils import checker

def Approx(inst, alg, cutOff, rSeed, G):
    random.seed(rSeed)

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

    G1 = G.copy()
    C = []  # list of the vertices for the Vertex Cover to be returned
    # getEdge = getRandomEdge
    getEdge = getMaxDegreeEdge
    
    start = time.time()
    while time.time() - start < cutOff:
        # select an edge (u,v) to be added to C
        E = G1.edges
        if len(E) == 0:  # C covers all the edges in G1
            break

        # Greedily get the edge to be added to C
        (u,v) = getEdge(E, G1)

        # remove the two endpoints u and v from the graph G1
        G1.remove_node(u)
        G1.remove_node(v)
        assert u not in C 
        assert v not in C
        C.append(u)
        C.append(v)

    duration = time.time() - start 

    # Trace File for the Greedy Approx algorithm is just one line (https://piazza.com/class/l725zf0sivy53i/post/151_f12)
    assert checker(G, C)
    printTraceFile(len(C), duration, traceFile)
    
    return C 

def getRandomEdge(E, G1) -> tuple:
    return random.choice(list(E))

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
