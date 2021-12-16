from utils import *
import networkx as nx
'''
try:
    A = nx.Graph([11])
    print("Here")
except Exception as ex:
    if type(ex) is nx.NetworkXError:
        print(f"To give the configuration of the chip, you have to input one of the following:\n")
        print(f"Edge List : List of 2-tuples denoting nodes connected with edges : [(1, 2), (1, 3)]")
        print(f"Dictionary of Dictionaries : A dictionary of dictionaries adjacency representation.")
        print(f"Dictionart of lists : A dictionary with key as a node and values as a list of all connected nodes")
        print(f"For other supported types, check : https://networkx.org/documentation/stable/reference/convert.html")
    raise
'''
C = Circuit(3)
C.add_gate((2,1),'X')

A = [(2,1), 'X', ]
