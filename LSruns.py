import os
import random as r

trials = 100
inst = 'power'
cutOff = 5
ALG = ['LS1']

for alg in ALG:
    for i in range(trials):
        seed = r.randint(1,100000)
        print("Running Trial " + str(i) + " with algorithm " + alg)
        os.system("python3 main.py -inst " + inst + " -alg " + alg + " -cutOff " + \
            str(cutOff) + " -rseed " + str(seed) + " > temp.txt")

