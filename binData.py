import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


cutOff = 10
ALG = ['LS1','LS2']
nBins = 11*cutOff

for inst in ['star2', 'power']:
    if(inst == 'star2'):
        exact = 4452

    if(inst == 'power'):
        exact = 2203

    for alg in ALG:
        f = open(alg + "_bins.txt",'w')
        traces = []
        data = []
        path = 'OutputFiles/' + inst + '_' + alg + '*.trace'
        seed = 0
        for name in glob.glob(path):
            
            for k in range(0, 100):
                if(name[k] == '.'):
                    break
            k = k + 3
            for j in range(k,100):
                if(name[j] == '_'):
                    break
            traces.append([name, seed])
            seed = seed + 1 

        nseeds = seed

        bins = np.zeros((nBins,100, nseeds))
        count = np.zeros((nBins,100, nseeds))


        for i in range(nseeds):
            f = open(traces[i][0])
            seed = traces[i][1]
            for line in f:
                t = line.split(', ')
                for i in range(2):
                    t[i] = float(t[i].replace("\n",""))
                t.append(seed)
                data.append(t)
                #print(data)

        for i in data:
            relSQ = ((i[1] - exact)/exact)  
            #Ignore Rel Err above 10%
            if(i[0]*10 > 110):
                continue
            bins[int(np.floor(i[0] * 10)):,int(np.floor(10*relSQ*100)):, i[2]] = 1



        #First Part
        #(Fixed % relative error asumme < 10)
        if(inst == "power"):
            if(alg == 'LS1'):
                q = 2.4 
            else:
                q = 0.8
        if(inst == "star2"):
            if(alg == 'LS1'):
                q = 4.2
            else:
                q = 3.2

        X = np.arange(0, 110, 1)
        X = X / 10
        Y = np.zeros((110,))

        

        for i in range(110):      
            Y[i] = (np.sum(bins[i, int(np.floor(10*q)), :])/nseeds)*100.0


        plt.figure()
        plt.plot(X, Y)
        plt.xlabel("Time (s)")
        plt.ylabel("Succes (%)")
        plt.title("Rel Err = " + str(q) + " %")
        plt.savefig("figs/part1/" + str(alg) + "_" + str(inst) + "_" + str(q) + ".png")

        #Second Part
        #Fixed Cutoff time (in seconds)
        if(inst == "power"):
            if(alg == 'LS1'):
                t = 3 
            else:
                t = 0.5
        if(inst == "star2"):
            if(alg == 'LS1'):
                t = 3 
            else:
                t = 0.5


        X2 = np.arange(0, 10, 0.1)
        Y2 = np.zeros((np.size(X2)))

        for j in range(0, 100):
            Y2[j] = (np.sum(bins[int(10*t) , j, :])/nseeds)*100

        plt.figure()
        plt.plot(X2, Y2)
        plt.xlabel("Rel Err (%)")
        plt.ylabel("Succes (%)")
        plt.title("Time = " + str(t) + " (s)")
        plt.savefig("figs/part2/" + str(alg) + "_" + str(inst) + "_" + str(t) + ".png")





    #for i in range(110):
    #    for j in range(100):
    #            bins[i,j] = bins[i,j]/count[:i+1,:j+1].sum()

    #fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    # Make data.
    #Y = np.arange(0, 11, 0.1)
    #X = np.arange(0, 100, 1)
    #X, Y = np.meshgrid(X, Y)

    # Plot the surface.
    #surf = ax.plot_surface(Y, X, bins, cmap=cm.coolwarm,linewidth=0, antialiased=False)
    #plt.show()

