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
    # Preprocess G to remove isolated nodes
    G.remove_nodes_from(list(nx.isolates(G)))
    # Initialize variables
    C_init = []              # list of the vertices for the Vertex Cover to be returned
    C_list = [[], []]
    G_prime = G.copy()
    B = list(G.nodes)   # Initialize upper bound to all vertices
    sizeB = len(B)      # Size for priority queue
    initial_level = 0   # Starting index for subproblem
    counter = itertools.count()           # Count when entering heap
    count = next(counter)
    min_bound = compute_lower_bound_simple(G)  # Minimum feasible bound

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
            # If C is already larger than B
            # Do not consider as a solution
            if len(C) > len(B):
                break
            count = next(counter)
            sol = utils.checker(G, C)
            if sol == True:
                if len(C) < len(B):
                    B = C  # Update upper bound if better soln found
                    sizeB = len(B)
                    # Print to trace
                    duration = time.time() - start
                    printTraceFile(len(C), duration, traceFile)
            else:  # Add new subproblem to heap
                if level + 1 <= len(list(G.nodes)):  # Ensure level is inbounds
                    G_prime = G.subgraph(list(G.nodes)[level:])
                    new_lower_bound = len(
                        C) + compute_lower_bound(cutOff, rSeed, G_prime)
                    # new_lower_bound = len(C) + compute_lower_bound_simple(G_prime)
                    if new_lower_bound < sizeB:
                        if new_lower_bound >= min_bound:
                            hq.heappush(pq, (new_lower_bound, count, C, level))

    duration = time.time() - start

    # Return Best Solution
    C = B

    # Trace File
    assert checker(G, C)
    printTraceFile(len(C), duration, traceFile)

    return C

###############################################################


def compute_lower_bound_simple(G):
    # Simple lower bound given by K&T 10.2, pg. 556
    nodes = len(list(G.nodes))
    edges = len(list(G.edges))
    k = int(math.ceil(edges/nodes))
    if k > nodes:
        k = nodes

    return k

###############################################################


def compute_lower_bound(cutOff, rSeed, G):
    # Adapted from Seongmin's approximation algorithm
    random.seed(rSeed)

    i = 0  # standard iterator

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
        (u, v) = getEdge(E, G1)

        # remove the two endpoints u and v from the graph G1
        G1.remove_node(u)
        G1.remove_node(v)
        assert u not in C
        assert v not in C
        C.append(u)
        C.append(v)

    duration = time.time() - start

    # Trace File for the Greedy Approx algorithm is just one line (https://piazza.com/class/l725zf0sivy53i/post/151_f12)
    # assert checker(G, C)
    sizeC = len(C)
    lowerboundC = int(math.ceil(1/2 * sizeC))

    return lowerboundC


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
