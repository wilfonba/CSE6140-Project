import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

trials = 25
inst = 'star2'
cutOff = 10
ALG = ['LS1','LS2']
exact = 4542
nBins = 11*cutOff

for alg in ALG:
    bins = np.zeros((nBins,100))
    count = np.zeros((nBins,100))

    f = open(alg + "_bins.txt",'w')
    traces = []
    data = []
    path = 'OutputFiles/' + inst + '_' + alg + '*.trace'
    for name in glob.glob(path):
        traces.append(name)
        print(name)
    for i in range(100):
        f = open(traces[i])
        for line in f:
            t = line.split(', ')
            for i in range(2):
                t[i] = float(t[i].replace("\n",""))
            data.append(t)

    for i in data:
        relSQ = ((i[1] - exact)/exact)
        bins[int(np.floor(i[0] * 10)):,int(np.floor(relSQ*100)):] = bins[int(np.floor(i[0] * 10)):,int(np.floor(relSQ*100)):] + 1
        count[int(np.floor(i[0] * 10)),int(np.floor(relSQ*100))] = count[int(np.floor(i[0] * 10)),int(np.floor(relSQ*100))] + 1

    for i in range(55):
        for j in range(100):
                bins[i,j] = bins[i,j]

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    # Make data.
    Y = np.arange(0, 11, 0.1)
    X = np.arange(0, 100, 1)
    X, Y = np.meshgrid(X, Y)

    # Plot the surface.
    surf = ax.plot_surface(Y, X, bins, cmap=cm.coolwarm,linewidth=0, antialiased=False)
    plt.show()

