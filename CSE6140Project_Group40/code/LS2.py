# Local Search 2
#
# Computes Max independent set by first computing a maximal independent 
# set and computing 2-improvements until no such improvement can be found. 
# Once this is done, the code is restarted 
#
# inputs:
#   inst:   The graph instance
#   alg:    The algorithm be ran (for printing trace files)
#   cutOff: A cutoff time in seconds
#   rSeed:  An integer random seed
#   G:      The input graph as a networkx graph
# Output:
#   C: the best vertex cover found

import networkx as nx
import time
import os
import random as rand
from output import printTraceFile
import collections as col
import numpy as np



def LS2(inst, alg, cutOff, rSeed, G):


    i = 0 # standard iterator
    while (1 and i <= 100):
        if os.path.exists("../output/" + inst + "_" + alg + "_" + str(cutOff) + "_" + \
                str(rSeed) + "_" + str(i) + ".trace"):
            i = i+1
        else:
            traceFile = open("../output/" + inst + "_" + alg + "_" + str(cutOff) + "_" + \
                str(rSeed) + "_" + str(i) + ".trace", "x")
            break

    G1 = G.copy() # Copy of G for greedy IC
    gV = np.array(G.nodes()).astype(int)
    gE = np.array(G.edges()).astype(int)
    gE = gE[gE[:, 0].argsort()]
    NV = len(gV)
    NE = np.shape(gE)[0]

    gV = np.sort(gV).astype(str)

    for i in range(NE):
        if(gE[i][0] > gE[i][1]):
            temp = gE[i][0].copy()
            gE[i][0] = gE[i][1].copy()
            gE[i][1] = temp

    gE = gE[np.argsort(gE[:,0])]

    tau = np.zeros((NV,), dtype = int)
    last_iter = np.zeros((NV,), dtype = int)
    is_sol = np.zeros((NV,), dtype = bool)
    candidates = np.zeros((NV,), dtype = bool)

    #Initialize a Maximal Solution
    for i in range(NV):
        if(tau[i] == 0):
            is_sol[i] = 1
            neighb = np.array(list(G[gV[i]])).astype(int) - 1
            for j in neighb :
                tau[j] += 1
        else:
            continue  

    prev_soln = len(np.where(is_sol == True)[0]) 
    best_soln = prev_soln       
    candidates[np.where(is_sol == True)[0]] = True

    count = 0
    nrestarts = 1000

    t0 = time.time()

    while(count < nrestarts):
        count += 1

        prev_soln = len(np.where(is_sol == True)[0]) 
    
        #Local Search over all possible 2-improvements
        while(1):         

            for x in np.where(candidates == True)[0]:
                neighb = np.array(list(G[gV[x]])).astype(int) - 1
                valid_neighb = neighb[np.where(tau[neighb] == 1)[0]]

                if(len(valid_neighb) >= 2):
                    for i in range(len(valid_neighb)):
                        for j in range(i+1, len(valid_neighb)):

                            u = valid_neighb[i] 
                            v = valid_neighb[j]

                            neighbu = np.array(list(G[gV[u]])).astype(int) - 1
                            if(v  in neighbu):
                                continue
                            neighbv = np.array(list(G[gV[v]])).astype(int) - 1

                            candidates[u] = True
                            candidates[v] = True
                            candidates[x] = False

                            is_sol[u] = True
                            is_sol[v] = True
                            is_sol[x] = False

                            tau[neighb] -= 1
                            tau[neighbu] += 1                    
                            tau[neighbv] += 1

                            for w in neighb[np.where(tau[neighb] == 1)[0]]:
                                neighbw =  np.array(list(G[gV[w]])).astype(int) - 1
                                neighbw = neighbw[np.where(is_sol[neighbw] == True)[0]]
                                candidates[neighbw] = True

                            break

                        if(tau[x] == 2):
                            break

                    if(tau[x] == 2):
                        break

                    candidates[x] = False
                    
                else:
                    candidates[x] = False


            new_soln = len(np.where(is_sol == True)[0])
            if(new_soln == prev_soln):
                break
            prev_soln = new_soln

        #Ensure the solution is maximal    
        for i in range(NV):
            if(tau[i] == 0 and is_sol[i] == False):
                is_sol[i] = True
                candidates[i] = True
                neighb = np.array(list(G[gV[i]])).astype(int) - 1
                for j in neighb :
                    tau[j] += 1
            else:
               continue

        new_soln = len(np.where(is_sol == True)[0])

        last_iter[np.where(is_sol == False)[0]] += 1
        last_iter[np.where(is_sol == True)[0]]= 0 

        #If improvement print new solution
        if(new_soln > best_soln):
            best_soln = new_soln    
            print("soln", (NV - new_soln))    
            C = [] 
            for i in np.where(is_sol == False)[0]:
                C.append(i)
            tf = time.time()
            printTraceFile(len(C), tf - t0, traceFile)
            if(tf - t0  > cutOff):
                print(tf - t0)
                return C

        #Perturb New Solution
        #Add a new element that has not been included for a while
        pertbs = np.where(last_iter == np.amax(last_iter))[0]
        elem = pertbs[np.random.randint(np.size(pertbs))]
        is_sol[elem] = True
        candidates[elem] = True
        
        #Remove neighbors of current element
        neighb = np.array(list(G[gV[elem]])).astype(int) - 1 
        tau[neighb[np.where(is_sol[neighb] == False)[0]]] += 1
        remove_elem = neighb[np.where(is_sol[neighb] == True)[0]]
        is_sol[remove_elem] = False
        candidates[remove_elem] = False
        tau[remove_elem] += 1

        #Adjust tau values of neighboring elements of removed elements
        for k in remove_elem:
            neighbk = np.array(list(G[gV[k]])).astype(int) - 1

            tau[neighbk] -= 1

            for w in neighbk[np.where(tau[neighbk] == 1)[0]]:
                neighbw =  np.array(list(G[gV[w]])).astype(int) - 1
                neighbw = neighbw[np.where(is_sol[neighbw] == True)[0]]
                candidates[neighbw] = True

        #Make the solution maximal        
        for i in range(NV):
            if(tau[i] == 0 and is_sol[i] == False):
                is_sol[i] = True
                candidates[i] = True
                neighb = np.array(list(G[gV[i]])).astype(int) - 1
                for j in neighb :
                    tau[j] += 1
            else:
                continue

    return C