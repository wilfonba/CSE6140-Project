import os

# Function to print solution file
def printSolutionFile(inst, alg, cutoff, rSeed, qual, MVC):
    # Remove .sol file if it already exists
    if os.path.exists("OutputFiles/" + inst + "_" + alg + "_" + str(cutoff) + "_" + str(rSeed) + ".sol"):
        os.remove("OutputFiles/" + inst + "_" + alg + "_" + str(cutoff) + "_" + str(rSeed) + ".sol")
    f = open("OutputFiles/" + inst + "_" + alg + "_" + str(cutoff) + "_" + str(rSeed) + ".sol", "x")
    
    f.write(str(qual) + "\n")
    for i in range(0,qual):
        f.write(str(MVC[i]) + ", ")
    
    f.close()

# Function to update trace file
def printTraceFile(qual, time, file):
    file.write(str('%.4f' % time)+ ", " + str(qual) + "\n")
