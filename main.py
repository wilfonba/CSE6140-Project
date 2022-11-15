# Main "executable" for calling the MVC algorithms
# Command Line Arguments:
#   -inst <filename>
#   -alg <BnB|Approx|LS1|LS2>
#       BnB : Branch and Bound
#       Approx : 
#       LS1 :
#       LS2 :
#   -time <cutoff in seconds>
#   -seed <random seed>

import sys
import networkx as nx
import BnB
import Approx
import LS1
import LS2

# Function for reading the .graph files and creating a networkx graph
def readInstance(inst):
    f = open("DATA/" + inst, 'r')
    lines = f.readline().split(" ")
    V = int(lines[0])
    E = int(lines[1])

    lines = []
    for i in range(1, V + 1):
        lines.append(str(i) + " " + f.readline().strip())

    G = nx.parse_adjlist(lines)
    return G


# Reading input arguments
inst = str(sys.argv[2])
alg =  str(sys.argv[4])
time = int(sys.argv[6])
seed = int(sys.argv[8])

print("Running " + alg + " on instance " + inst + " with time limit " + str(time) + \
     " seconds and random seed " + str(seed))

# Read the given instance file 
G = readInstance(inst)