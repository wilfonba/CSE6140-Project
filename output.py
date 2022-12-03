import os

# Function to print solution file


def printSolutionFile(inst, alg, cutOff, rSeed, qual, MVC):
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

# Function to update trace file


def printTraceFile(qual, time, file):
    file.write(str('%.4f' % time) + ", " + str(qual) + "\n")
