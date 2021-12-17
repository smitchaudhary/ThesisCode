from utils import *
import networkx as nx

C = Circuit(3)
C.add_gate((2,1),'X')

A = [((2,1), 'X'), (1, 'Z')]
C.add_multiple_gates(A)

G = nx.Graph()
G.add_edges_from([(1,2), (2,3)])
Q = Chip(G)
print(nx.density(G))

map = Mapping(3)
d = {1 : 1, 2 : 2}
map.starting_mapping(d)

print(Q.predicate(map, C))

A = [1, 2, 3, 4, 5, 6, 7, 8]
B = [A[x:x+5] for x in range(0, 8, 5)]
print(B)
