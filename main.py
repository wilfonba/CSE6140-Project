# Main "executable" for calling the MVC algorithms
# Command Line Arguments:
#   -inst <filename>
#   -alg <BnB|Approx|LS1|LS2>
#       BnB : Branch and Bound
#       Approx : 
#       LS1 : Simmulated Annealing
#       LS2 :
#   -time <cutoff in seconds>
#   -seed <random seed>

import sys
import networkx as nx
import random
import BnB
from Approx import Approx
from LS1 import LS1
from LS2 import LS2
from output import printSolutionFile

# Function for reading the .graph files and creating a networkx graph
def readInstance(inst):
    f = open("DATA/" + inst + ".graph", 'r')
    lines = f.readline().split(" ")
    V = int(lines[0])
    E = int(lines[1])

    lines = []
    for i in range(1, V + 1):
        lines.append(str(i) + " " + f.readline().strip())

    G = nx.parse_adjlist(lines)
    return G


# Reading input arguments
# inst = str(sys.argv[2])
# alg =  str(sys.argv[4])
# cutOff = float(sys.argv[6])
# rSeed = int(sys.argv[8])
inst = 'dummy2'
alg = "BnB"
cutOff = 100
rSeed = 234

print("Running " + alg + " on instance " + inst + " with time limit " + str(cutOff) + \
     " seconds and random seed " + str(rSeed))

# Read the given instance file 
G = readInstance(inst)

# Set the random seed 
random.seed(rSeed)

if (alg == "BnB"):
    # run BnB
    a = 1 # filler
    C = BnB(inst, alg, cutOff, rSeed, G)
elif (alg == "Approx"):
    # Run Approx
    a = 2 # filler
    C = Approx(inst, alg, cutOff, rSeed, G)
elif (alg == "LS1"):
    # Run LS1
    C = LS1(inst, alg, cutOff, rSeed, G)
elif (alg == "LS2"):
    C = LS2(inst, alg, cutOff, rSeed, G)
else:
    print("Invalid algorithm")

printSolutionFile(inst, alg, cutOff, rSeed, len(C), C)