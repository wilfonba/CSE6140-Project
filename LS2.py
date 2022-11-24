import random
import networkx as nx
import time
import os
import random as rand
from output import printTraceFile
import math
import collections as col
import numpy as np



def LS2(inst, alg, cutOff, rSeed, G):


    i = 0 # standard iterator
    while (1 and i <= 100):
        if os.path.exists("OutputFiles/" + inst + "_" + alg + "_" + str(cutOff) + "_" + \
                str(rSeed) + "_" + str(i) + ".trace"):
            i = i+1
        else:
            traceFile = open("OutputFiles/" + inst + "_" + alg + "_" + str(cutOff) + "_" + \
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
    is_sol = np.zeros((NV,), dtype = bool)
    candidates = np.zeros((NV,), dtype = bool)



    #Initialize a Maximal Solution
    for i in range(NV-1, -1, -1):
        if(tau[i] == 0):
            is_sol[i] = 1
            neighb = np.array(list(G[gV[i]])).astype(int) - 1
            for j in neighb :
                tau[j] += 1
        else:
            continue  

    prev_soln = len(np.where(is_sol == True)[0])        


    #Initialize Candidates
    candidates[np.where(is_sol == True)[0]] = True
    
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

    print("soln", (NV - new_soln))    
    C = [] 
    for i in np.where(is_sol == False)[0]:
        C.append(i)       
    return C