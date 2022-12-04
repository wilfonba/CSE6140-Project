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


# BnB function for executing Branch-and-Bound algorithm
#   along with required subfunctions.
#
# Inputs:
#   inst    - Output filename
#   alg     - "BnB" for output filename
#   cutOff  - Cutoff time in seconds
#   rSeed   - Unused
#   G       - Graph object for computing vertex cover
#
# Outputs:
#   C       - Best vertex cover found within cutoff
#
"""
BnB calculates a vertex cover using a Branch-and-Bound algorithm. 

Each step the algorithm explores the latest subproblem from a frontier set of pending subproblems. 
Each subproblem is defined as:
    F(i) = [current_vertex, included, (parent_vertex, parent_included)]

For each iteration the algorithm reduces the current subgraph depending on whether the current vertex is included or not included. If the vertex is included then it is added to the vertex cover and removed from the subgraph. If the vertex is not included then its neighbors are added to the vertex cover and removed from the subgraph. [Akiba et al. 2016]

Then the partial vertex cover C is checked to determine if it is a valid vertex cover to G. If so the algorithm is set to backtrack, and if the solution is better, B is overwritten with C. If not, the current subgraph is checked for its lower bound. If the subgraph is promising (LB < |B|) then the algorithm takes the highest degree node from the current subgraph and expands it into two new subproblems. One subproblem includes the new vertex in the vertex cover while the other excludes it. Otherwise, if not promising, the algorithm is set to backtrack. 

If the algorithm backtracks, it undoes the changes to the subgraph to return to the parent state. The algorithm continues until all subproblems in the frontier set have been considered or the time elapsed becomes greater than the cutoff time.
"""


def BnB(inst, alg, cutOff, rSeed, G):
    random.seed(rSeed)

    i = 0  # standard iterator
    while (1 and i <= 100):
        if os.path.exists("OutputFiles/" + inst + "_" + alg +
                          "_" + str(cutOff) + "_" + str(i) + ".trace"):
            i = i + 1
            # print("Here")
        else:
            traceFile = open("OutputFiles/" + inst + "_" + alg +
                             "_" + str(cutOff) + "_" + str(i) + ".trace", "x")
            break
    # while (1 and i <= 100):
    #     if os.path.exists("TestOutput/" + inst + "_" + alg +
    #                       "_" + str(cutOff) + "_" + str(i) + ".trace"):
    #         i = i + 1
    #         # print("Here")
    #     else:
    #         traceFile = open("TestOutput/" + inst + "_" + alg +
    #                          "_" + str(cutOff) + "_" + str(i) + ".trace", "x")
    #         break

    # Begin BnB
    # Preprocess G to remove isolated nodes and presort according to node degree
    G.remove_nodes_from(list(nx.isolates(G)))
    # G_sorted = sorted(G.nodes(), key=lambda n: G.degree(n), reverse=True)
    # H = nx.Graph()
    # H.add_nodes_from(G_sorted)
    # H.add_edges_from(G.edges(data=True))
    # G = H

    # Initialize variables
    # Define initial problem
    initial_vertex = list(G.nodes)[0]   # Pick max degree node
    B = list(G.nodes)                   # Initialize vc to nodes
    sizeB = len(list(G.nodes))          # Initialize upper bound
    G_prime = G.copy()                  # Create graph for in-place mod
    explored_set = []                   # Explored vertices
    include_set = []                    # Whether vertex is included

    # Initialize Frontier
    frontier = []
    frontier.append((initial_vertex, False, (-1, False)))
    frontier.append((initial_vertex, True, (-1, False)))

    # frontier_history = []

    # Begin Exploring Frontier
    start = time.time()
    # for i in range(25):
    while frontier != [] and (time.time() - start < cutOff):

        backtrack = False

        # Expand newest problem on frontier
        # print("Problem: ", frontier[-1])
        cur_vertex, included, parent = frontier.pop()

        # Construct current working graph
        # Changed, will be done in-place
        # G_prime = G.copy()
        # if C!=[]:
        #     for node in C:
        #         G_prime.remove_node(node)
        # if C_exc!=[]:
        #     for node in C_exc:
        #         G_prime.remove_node(node)

        # Remove vertex from subgraph
        if included == True:
            G_prime.remove_node(cur_vertex)
        elif included == False:
            neighbors = list(G_prime.neighbors(cur_vertex))
            for node in neighbors:
                include_set.append(True)
                explored_set.append(node)
                G_prime.remove_node(node)

        # Add current vertex to sets
        include_set.append(included)
        explored_set.append(cur_vertex)

        # Calculate C according to explored_set
        # and include_set
        C = []
        for i in range(len(explored_set)):
            if include_set[i] == True:
                C.append(explored_set[i])

        # Check current solution
        # sol = utils.checker(G, C) # Safer but slower
        # if sol == True:
        if G_prime.number_of_edges() == 0:
            # print("Solution Found")
            backtrack = True
            if len(C) < len(B):
                # print("Solution Better")
                # If soln then update bounds
                B = C
                sizeB = len(B)
                # Print to trace
                duration = time.time() - start
                # print(sizeB, duration)
                printTraceFile(len(C), duration, traceFile)
        else:
            # Else
            # Calculate lower bound
            # Create new subproblems
            # print("Consider subproblem")
            # if len(list(G_prime.nodes)) == 0:
            #     print("Empty Subgraph")
            if len(list(G_prime.nodes)) > 0:  # Make sure subgraph isn't empty
                G_prime_lower_bound = compute_lower_bound_simple(G_prime)
                # G_prime_lower_bound = compute_lower_bound_simple2(G_prime)
                # G_prime_lower_bound = compute_lower_bound(
                #     cutOff, rSeed, G_prime)
                lower_bound = len(C) + G_prime_lower_bound
                # print(lower_bound)
                # print("Consider subproblem, bound: ",
                #       lower_bound, " sizeB: ", sizeB)
                if lower_bound < sizeB:
                    # If promising
                    best_ver = max(list(G_prime.degree), key=lambda x: x[1])[0]
                    # print("Add vertex ", best_ver, " to Frontier")
                    frontier.append((best_ver, False, (cur_vertex, included)))
                    frontier.append((best_ver, True, (cur_vertex, included)))
                else:
                    backtrack = True

        if backtrack == True:
            if frontier != []:
                # Backtrack to next pending problem in frontier
                par_vertex, par_included = frontier[-1][2]
                # print("Reconstructing ver: ", par_vertex,
                #       "included: ", par_included)
                if par_vertex in explored_set:
                    # print("Parent vertex in explored set")
                    # Determine index in order to remove the
                    # appropriate number of points from explored
                    # set and add back to G_prime
                    index = explored_set.index(par_vertex) + 1
                    # print("Index: ", index, "Explored Set: ", len(explored_set))
                    # print("Nodes to add back: ", len(explored_set) - index)
                    # for i in range(index, len(explored_set)):
                    while index < len(explored_set):
                        # Add back vertex
                        removed_vertex = explored_set.pop()
                        removed_included = include_set.pop()
                        G_prime.add_node(removed_vertex)
                        # print("Added back vertex: ", removed_vertex)
                        neighbors = G.neighbors(removed_vertex)
                        subgraph_nodes = G_prime.nodes()
                        # Shrink Vertex Cover as we go
                        C = []
                        for i in range(len(explored_set)):
                            if include_set[i] == True:
                                C.append(explored_set[i])
                        # Add back edges
                        for neighbor in neighbors:
                            if neighbor in subgraph_nodes and neighbor not in C:
                                # print("Added back edge from neighbor: ", neighbor)
                                G_prime.add_edge(neighbor, removed_vertex)

                elif (par_vertex, par_included) == (-1, False):  # Returned to root node
                    explored_set = []
                    include_set = []
                    G_prime = G.copy()

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

    return k


def compute_lower_bound_simple2(G):
    # Simple lower bound given by Wang et al.
    nodes = len(list(G.nodes))
    edges = len(list(G.edges))
    maxedge = max(list(G.degree), key=lambda x: x[1])[1]
    k = int(math.ceil(edges/maxedge))

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
