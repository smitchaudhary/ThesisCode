import numpy as np
import networkx as nx

class Mapping:
    def __init__(self, num_qubits, named_qubits = False, qubit_names = None):
        self.num_qubits = num_qubits
        self.named_qubits = named_qubits
        self.map = {}
        if named_qubits:
            assert len(qubit_names) == self.num_qubits, "You need to have as many named qubits as the number of qubits"
            for qubit in qubit_names:
                self.map[qubit] = "*"
        else:
            for i in range(self.num_qubits):
                self.map[i] = "*"
        self.length = 0

    def __str__(self):
        return f"The current mapping is {self.map}"

    def __len__(self):
        len = 0
        for assignment in self.map.values():
            if assignment != "*":
                len += 1
        return len

    def starting_mapping(self, mapping_dict):
        for qubit, assignment in mapping_dict.items():
            self.map[qubit] = assignment
        self.length = self.__len__()

    def update_mapping(self, qubit, assignment):
        if self.map[qubit] == "*":
            self.length += 1
        if assignment == "*":
            self.length -= 1
        self.map[qubit] = assignment

def heuristic(mapping, connectivity_graph):
    #for qubit in
    pass
