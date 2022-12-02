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
    # Preprocess G to remove isolated nodes and presort according to node degree
    G.remove_nodes_from(list(nx.isolates(G)))
    G_sorted = sorted(G.nodes(), key=lambda n: G.degree(n), reverse=True)
    H = nx.Graph()
    H.add_nodes_from(G_sorted)
    H.add_edges_from(G.edges(data=True))
    G = H

    # Initialize variables
    C_init = []              # list of the vertices for the Vertex Cover to be returned
    C_list = [[], []]
    C = []
    C_exc = []
    # Used to control lower bound, s.t. frontier updated with new point first
    C_bounds = [float('-inf'), 0]
    G_prime = G.copy()
    B = list(G.nodes)   # Initialize upper bound to all vertices
    sizeB = len(B)      # Size for priority queue
    # initial_level = 0   # Starting index for subproblem
    counter = itertools.count()           # Count when entering heap
    count = next(counter)

    # Push starting problem to heap
    frontier = []
    hq.heapify(frontier)
    hq.heappush(frontier, (sizeB, count, C_init, C_exc))

    # Explore Frontier
    start = time.time()
    while frontier != [] and (time.time() - start < cutOff):
        # Choose most promising configuration
        # heappop according to lower_bound as key
        if len(frontier) == 0:
            break
        lower_bound, count, C, C_exc = hq.heappop(frontier)

        # Print Status
        # print(lower_bound, count, C, "|", end='\r')

        # Construct G_prime according to C, C_exc
        C_list = [[], []]
        C_exc_list = [[], []]
        if C == []:
            explored_ver = C_exc
        elif C_exc == []:
            explored_ver = C
        else:
            explored_ver = C.copy()
            explored_ver.append(C_exc)

        vertices = G.nodes
        unexplored_ver = [x for x in vertices if x not in explored_ver]
        G_prime = G.subgraph(unexplored_ver)

        # Determine best vertex according to degree
        best_ver = max(list(G_prime.degree), key=lambda x: x[1])[0]

        # Find neighboring points
        neighbors = list(G.neighbors(best_ver))

        # Expand into two subchoices
        # Choice 1: Add best_ver to C
        # Remove neighbors from consideration
        C_new = C.copy()
        C_new.append(best_ver)
        C_exc_new = C_exc.copy()
        C_exc_new.extend(neighbors)
        C_list[0] = C_new
        C_exc_list[0] = C_exc_new

        # Choice 2: Do not add best_ver to C
        # Add all neighbors to consideration
        C_new = C.copy()
        C_new.extend(neighbors)
        C_exc_new = C_exc.copy()
        C_exc_new.append(best_ver)
        C_list[1] = C_new
        C_exc_list[1] = C_exc_new

        # Check if C is a vertex cover
        for i in range(len(C_list)):
            C = C_list[i]
            C_exc = C_exc_list[i]
            bound_limit = C_bounds[i]
            sol = utils.checker(G, C)
            if sol == True:
                if len(C) < len(B):
                    B = C
                    sizeB = len(B)
                    # Print to trace
                    duration = time.time() - start
                    printTraceFile(len(C), duration, traceFile)
            else:  # If promising, add new subproblem to frontier
                # Construct new subgraph
                explored_ver = C.copy()
                explored_ver.append(C_exc)
                vertices = G.nodes
                unexplored_ver = [x for x in vertices if x not in explored_ver]
                G_prime = G.subgraph(unexplored_ver)

                # Determine best vertex according to degree
                G_prime_lower_bound = compute_lower_bound_simple2(G_prime)
                new_lower_bound = len(C) + G_prime_lower_bound
                max_deg_node = max(list(G_prime.degree), key=lambda x: x[1])[1]
                degree_bound = max(-max_deg_node, bound_limit)
                # degree_bound = -max_deg_node

                if max_deg_node > 0:  # Check to see if subproblem is feasible
                    if new_lower_bound < sizeB:
                        count = next(counter)
                        hq.heappush(frontier, (degree_bound, -count, C, C_exc))

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


def compute_lower_bound_simple2(G):
    # Simple lower bound given by K&T 10.2, pg. 556
    nodes = len(list(G.nodes))
    edges = len(list(G.edges))
    maxedge = max(list(G.degree))[1]
    if maxedge == 0:
        k = int(math.ceil(edges/nodes))
        return k
    k = int(math.ceil(edges/maxedge))
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
