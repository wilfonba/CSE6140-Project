import random
import networkx as nx
import time
import os
import random as rand
from output import printTraceFile
import math
import collections as col
from utils import checker
import sys
import networkx as nx
import random
import BnB
from Approx import Approx
from LS1 import LS1
from LS2 import LS2
from output import printSolutionFile
import heapq as hq
import itertools
import utils
import time


def BnB(inst, alg, cutOff, rSeed, G):
    random.seed(rSeed)

    i = 0  # standard iterator
    while (1 and i <= 100):
        if os.path.exists("OutputFiles/" + inst + "_" + alg + "_" + str(cutOff) + "_" +
                          str(rSeed) + "_" + str(i) + ".trace"):
            i = i + 1
            # print("Here")
        else:
            traceFile = open("OutputFiles/" + inst + "_" + alg + "_" + str(cutOff) + "_" +
                             str(rSeed) + "_" + str(i) + ".trace", "x")
            break

    # Begin BnB
    # Initialize variables
    C_init = []              # list of the vertices for the Vertex Cover to be returned
    C_list = [[], []]
    G_prime = G.copy()
    B = list(G.nodes)   # Initialize upper bound to all vertices
    sizeB = len(B)      # Size for priority queue
    initial_level = 0   # Starting index for subproblem
    counter = itertools.count()           # Count when entering heap
    count = next(counter)

    # Push starting problem to heap
    pq = []
    hq.heapify(pq)
    hq.heappush(pq, (sizeB, count, C_init, initial_level))

    # Explore Frontier
    start = time.time()
    while pq != False and (time.time() - start < cutOff):
        if len(pq) == 0:
            break
        # Choose most promising configuration
        # heappop according to lower_bound as key
        lower_bound, count, C, level = hq.heappop(pq)

        # Expand into two subchoices
        # Choice 1: Do not add V[level] to C
        C_list = [C.copy(), C.copy()]
        # Choice 2: Do add V[level] to C
        C_list[1].append(list(G.nodes)[level])
        level = level + 1

        # Check solution for each new configuration
        for C in C_list:
            count = next(counter)
            sol = utils.checker(G, C)
            if sol == True:
                if len(C) < len(B):
                    B = C  # Update upper bound if better soln found
                    sizeB = len(B)
            else:  # Add new subproblem to heap
                if level + 1 <= len(list(G.nodes)):  # Ensure level is inbounds
                    G_prime = G.subgraph(G.nodes - C)
                    new_lower_bound = compute_lower_bound(G_prime)
                    if new_lower_bound < sizeB:
                        hq.heappush(pq, (new_lower_bound, count, C, level))

    duration = time.time() - start

    # Return Best Solution
    C = B

    # Trace File
    assert checker(G, C)
    printTraceFile(len(C), duration, traceFile)

    return C

###############################################################


def compute_lower_bound(G):
    # Simple lower bound given by K&T 10.2, pg. 556
    nodes = len(list(G.nodes))
    edges = len(list(G.edges))
    k = int(math.ceil(edges/nodes))
    if k > nodes:
        k = nodes

    return k
