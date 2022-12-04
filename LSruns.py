import os
import random as r
import glob
import sys

trials = 1
graphs = []
path = 'DATA/*.graph'
for name in glob.glob(path):
    name = name.split('.')[0]
    name = name.split('/')[1]
    graphs.append(name)
cutOff = 1800
graphs = [str(sys.argv[2])]
print(graphs)
ALG = ['BnB']

for inst in graphs:
    for alg in ALG:
        for i in range(trials):
            seed = r.randint(1,100000)
            print("Running Trial " + str(i) + " of instance " + inst + " with algorithm " + alg)
            os.system("python3 main.py -inst " + inst + " -alg " + alg + " -cutOff " + \
                str(cutOff) + " -rseed " + str(seed) + " > temp.txt")

