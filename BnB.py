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
    # while (1 and i <= 100):
    #     if os.path.exists("OutputFiles/" + inst + "_" + alg +
    #                       "_" + str(cutOff) + "_" + str(i) + ".trace"):
    #         i = i + 1
    #         # print("Here")
    #     else:
    #         traceFile = open("OutputFiles/" + inst + "_" + alg +
    #                          "_" + str(cutOff) + "_" + str(i) + ".trace", "x")
    #         break
    while (1 and i <= 100):
        if os.path.exists("TestOutput/" + inst + "_" + alg +
                          "_" + str(cutOff) + "_" + str(i) + ".trace"):
            i = i + 1
            # print("Here")
        else:
            traceFile = open("TestOutput/" + inst + "_" + alg +
                             "_" + str(cutOff) + "_" + str(i) + ".trace", "x")
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
    # Define initial problem
    initial_vertex = list(G.nodes)[0]   # Pick max degree node
    parent = (-1, -1)                   # Set parent to oob
    B = list(G.nodes)                   # Initialize vc to nodes
    sizeB = len(list(G.nodes))          # Initialize upper bound
    G_prime = G.copy()                  # Create graph for in-place mod
    explored_set = []                   # Explored vertices
    include_set = []                    # Whether vertex is included

    frontier = []

    # frontier.append((initial_vertex, True, [], []))
    frontier.append((initial_vertex, False, [], []))
    frontier.append((initial_vertex, True, [], []))

    # frontier_history = []

    # Begin Exploring Frontier
    start = time.time()
    # for i in range(3):
    while frontier != [] and (time.time() - start < cutOff):
        # if len(frontier) == 0:
        #     break

        backtrack = False

        # Expand newest problem on frontier
        # print(frontier[-1])
        cur_vertex, included, C, C_exc = frontier.pop()

        # Construct current working graph
        G_prime = G.copy()
        if C != []:
            for node in C:
                G_prime.remove_node(node)
        if C_exc != []:
            for node in C_exc:
                G_prime.remove_node(node)

        # Remove vertex from subgraph
        if included == True:
            C.append(cur_vertex)
            neighbors = list(G_prime.neighbors(cur_vertex))
            # C_exc.extend(neighbors)
            G_prime.remove_node(cur_vertex)
            # for node in neighbors:
            #     G_prime.remove_node(node)

        elif included == False:
            # C_exc.append(cur_vertex)
            neighbors = list(G_prime.neighbors(cur_vertex))
            C.extend(neighbors)
            # G_prime.remove_node(cur_vertex)
            for node in neighbors:
                G_prime.remove_node(node)
            # print(C, C_exc)

        # Remove vertex from subgraph
        # if included == True:
        #     G_prime.remove_node(cur_vertex)
        # elif included == False:
        #     neighbors = list(G_prime.neighbors(cur_vertex))
        #     for node in neighbors:
        #         include_set.append(True)
        #         explored_set.append(node)
        #         G_prime.remove_node(node)

        # Regardless, add state
        # include_set.append(included)
        # explored_set.append(cur_vertex)

        # Check current solution
        sol = utils.checker(G, C)
        # if G_prime.number_of_edges() == 0:
        if sol == True:
            # print("Solution Found")
            if len(C) < len(B):
                # print("Solution Better")
                # If soln then update bounds
                B = C
                sizeB = len(B)
                # Print to trace
                duration = time.time() - start
                print(sizeB, duration)
                printTraceFile(len(C), duration, traceFile)
        else:
            # Else
            # Calculate lower bound
            # Create new subproblems
            # print("Consider subproblem")
            # if len(list(G_prime.nodes)) == 0:
            #     print("Empty Subgraph")
            if len(list(G_prime.nodes)) > 0:
                G_prime_lower_bound = compute_lower_bound_simple(G_prime)
                lower_bound = len(C) + G_prime_lower_bound
                # print(lower_bound)
                # print("Consider subproblem, bound: ",
                #       lower_bound, " sizeB: ", sizeB)
                if lower_bound < sizeB:
                    # If promising
                    # print("Add to Frontier")
                    best_ver = max(list(G_prime.degree), key=lambda x: x[1])[0]
                    # print("Best Vertex: ", best_ver)
                    frontier.append((best_ver, False, C.copy(), C_exc.copy()))
                    frontier.append((best_ver, True, C.copy(), C_exc.copy()))

    duration = time.time() - start

    # Return Best Solution
    C = B

    # Trace File
    assert checker(G, C)
    printTraceFile(len(C), duration, traceFile)

    return C

###############################################################

# Find neighbors of neighbors


def find_n_of_n(G_prime, neighbors, best_ver):
    n_of_ = []
    n_of_n = []
    for n in neighbors:
        n_ = list(G_prime.neighbors(n))
        n_of_.extend(n_)

    n_of_n = list(set(n_of_))
    n_of_n.remove(best_ver)

    return n_of_n

###############################################################


def compute_lower_bound_simple(G):
    # Simple lower bound given by K&T 10.2, pg. 556
    nodes = len(list(G.nodes))
    edges = len(list(G.edges))
    k = int(math.ceil(edges/nodes))
    # if k > nodes:
    #     k = nodes

    return k


def compute_lower_bound_simple2(G):
    # Simple lower bound given by K&T 10.2, pg. 556
    nodes = len(list(G.nodes))
    edges = len(list(G.edges))
    maxedge = max(list(G.degree), key=lambda x: x[1])[1]
    # if maxedge == 0:
    #     k = int(math.ceil(edges/nodes))
    #     return k
    k = int(math.ceil(edges/maxedge))
    # if k > nodes:
    #     k = nodes

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
