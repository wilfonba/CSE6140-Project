def checker(G, C) -> bool:
    for e in G.edges:
        if (e[0] not in C) and (e[1] not in C):
            return False 
    return True
