# This file contains a commonly used uitily function

def checker(G, C) -> bool:
    # Checks if a set is a vertex cover
    # Inputs:
    #   G: the graph
    #   C: a list of the vertices
    for e in G.edges:
        if (e[0] not in C) and (e[1] not in C):
            return False 
    return True
