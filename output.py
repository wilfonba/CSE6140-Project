# This file includes two functions to print solution files and
# Trace files.

import os

def printSolutionFile(inst, alg, cutOff, rSeed, qual, MVC):
    # Prints a solution file
    # Inputs:
    #   inst:   the instance for which the vertex cover was found
    #   alg:    the algorithm used for the run
    #   cutOff: the cutoff time in seconds used for the run
    #   rSeed:  the random seed used for the run
    #   qual:   the integer number of vertices in the solution
    #   MVC:    a list of the vertices in the minimum vertex cover
    i = 0  # standard iterator
    if alg == 'BnB' or 'Approx':
        while (1 and i <= 100):
            if os.path.exists("OutputFiles/" + inst + "_" + alg + "_" + str(cutOff) + "_" +
                              str(i) + ".sol"):
                i = i + 1
            else:
                f = open("OutputFiles/" + inst + "_" + alg + "_" + str(cutOff) + "_" +
                         str(i) + ".sol", "x")
                break
    else:
        while (1 and i <= 100):
            if os.path.exists("OutputFiles/" + inst + "_" + alg + "_" + str(cutOff) + "_" +
                              str(rSeed) + "_" + str(i) + ".sol"):
                i = i + 1
            else:
                f = open("OutputFiles/" + inst + "_" + alg + "_" + str(cutOff) + "_" +
                         str(rSeed) + "_" + str(i) + ".sol", "x")
                break

    f.write(str(qual) + "\n")
    for i in range(0, qual):
        f.write(str(MVC[i]) + ",")

    f.close()


def printTraceFile(qual, time, file):
    # Prints a trace file
    # Inputs: 
    #   qual: an integer number of vertices in the current solution
    #   time: a float for the current execution time
    #   file: a file objet which to write the trace to
    file.write(str('%.4f' % time) + ", " + str(qual) + "\n")
