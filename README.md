# CSE6140-Project

Our project is written in Python. It takes as input the various graphs in DATA and can perform Branch and Bound (BnB.py), Approximation (Approx.py) and Local Search (LS1.py, LS2.py) 
algorithms. The code stores the solution and trace file in the output directory. The execuable can be run with the following command: 

python3 main.py --inst <filename> --alg [BnB/Approx/LS1/LS2] --cutoff <time> --seed <random seed> 

The filename can be any of the files in the DATA directory. Cutoff time is used to terminate the solution. Random seed is used for multiple runs (needed in 
local search algorithms).

QRTD and SQD plots can be generated by running binData.py and box plots can be generated by running boxData.py, with the plots stored
in the figs folder. timeTrialDataAnalysis.py reads trace files to ouput a table for use in the comprehensive time analysis part of the report.
utils.py provides a checking utility for ensure solutions are vertex covers.
