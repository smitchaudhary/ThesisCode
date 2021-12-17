import numpy as np
import networkx as nx

class Mapping:
    # Can and should I convert the entire mapping as part of the Chip class?
    '''
    Mapping Class represents different (partial) mappings.
    '''
    def __init__(self, num_qubits, named_qubits = False, qubit_names = None):
        # Do not use named qubits for now.
        '''
        Initialise the mapping.
        Parameters:
            num_qubits : int
                The number of qubits in the system.
            named_qubits : bool
                If qubits are named or simply indexed with integers. If True, they are named andhave to provide names. Defaults to False.
        Returns:
            None
        '''
        self.num_qubits = num_qubits
        self.named_qubits = named_qubits
        self.map = {}
        if named_qubits:
            assert len(qubit_names) == self.num_qubits, "You need to have as many named qubits as the number of qubits"
            for qubit in qubit_names:
                self.map[qubit] = "*"
        else:
            for i in range(self.num_qubits):
                self.map[i+1] = "*"
        self.length = 0

    def __str__(self):
        '''
        Special function to output the mapping dictionary when printed an object of class Mapping.
        '''
        return f"The current mapping is {self.map}"

    def __len__(self):
        '''
        Special function to output the length of the dictionary when checked the length of mapping. Length is the number of assignments made.
        '''
        len = 0
        for assignment in self.map.values():
            if assignment != "*":
                len += 1
        return len

    def starting_mapping(self, mapping_dict):
        '''
        The initial mapping that you want to start with.
        Parameters:
            mapping_dict : Dictionary
                Dictionary containing the qubits as keys and their assignments as values.
        Returns:
            None
        '''
        for qubit, assignment in mapping_dict.items():
            self.map[qubit] = assignment
        self.length = self.__len__()

    def update_mapping(self, qubit, assignment):
        '''
        Update the mapping
        Parameters:
            qubit : int or named qubit
                The qubit whose assignment is to be changed.
            assignment : "*" or int
                The new assignment of the qubit.
        Returns:
            None
        '''
        if self.map[qubit] == "*":
            self.length += 1
        if assignment == "*":
            self.length -= 1
        self.map[qubit] = assignment

class Chip:
    '''
    Chip class represnts the topology of the physical chip on which the circuit needs to be mapped.
    '''
    def __init__(self, connectivity_graph):
        '''
        Initialise an instance of Chip class.
        Parameters:
            connectivity_graph : one of the supported types to construct a networkxGraph
        Returns:
            None
        '''
        if type(connectivity_graph) is not nx.Graph:
            try:
                connectivity_graph = nx.Graph(connectivity_graph)
            except Exception as ex:
                if type(ex) is nx.NetworkXError:
                    print(f"To give the configuration of the chip, you have to input one of the following:\n")
                    print(f"Edge List : List of 2-tuples denoting nodes connected with edges : [(1, 2), (1, 3)]")
                    print(f"Dictionary of Dictionaries : A dictionary of dictionaries adjacency representation.")
                    print(f"Dictionart of lists : A dictionary with key as a node and values as a list of all connected nodes")
                    print(f"For other supported types, check : https://networkx.org/documentation/stable/reference/convert.html")
                raise
        self.connectivity_graph = connectivity_graph
        self.num_qubits = nx.number_of_nodes(self.connectivity_graph)
        self.density = nx.density(self.connectivity_graph)

    def __len__(self):
        '''
        Special function to output the size of the chip (number of qubits).
        '''
        print(self.num_qubits)

    def predicate(self, mapping, slice_of_two_qubit_gates):
        '''
        The predicate that tells you if some (partial) assignment is valid or not for the particular chip.
        Parameters:
            mapping : Mapping
                An object of Mapping class to represent the current (partial) assignment.
            slice_of_two_qubit_gates : list
                The two qubit gates in a circuit slice that needs to be mapped.
        Returns:
            validity: bool
                True if the (partial) assignment is valid. False if it is invalid.
        '''
        validity = True
        two_qubit_gates = circuit.two_qubit_gates
        inverse_map = {v : k for k, v in mapping.map.items()}
        for qubits, gates in two_qubit_gates:
            q1, q2 = qubits
            physicalQ1, physicalQ2 = inverse_map[q1], inverse_map[q2]
            if self.connectivity_graph.has_edge(physicalQ1, physicalQ2):
                continue
            else:
                validity = False
                break
        return validity

class Circuit:
    '''
    Circuit class to represnt a circuit object.
    '''
    def __init__(self, num_qubits):
        '''
        Initialise the Circuit class
        Parameters:
            num_qubits : int
                Number of qubits in the circuit
        Returns:
            None
        '''
        # Add functionality to have named_qubits and if the input qubit is out of range, raise an error.
        self.num_qubits = num_qubits
        self.gates = []
        self.two_qubit_gates = []

    def __len__(self):
        '''
        Special function to output the size of the circuit (number of two-qubit gates).
        '''
        return len(two_qubit_gates)

    def __str__(self):
        '''
        Special function to output the text diagram of the circuit.
        '''
        # Add code here to draw a text diagram of the circuit.
        pass

    def size(self):
        '''
        Size of the circuit. Gives the number of qubits, number of gates and number of two-qubit gates.
        '''
        return f'Number of qubits: {self.num_qubits}\nNumber of gates: {len(self.gates)} \nTwo-qubit gates: {len(self.two_qubit_gates)}'

    def add_gate(self, qubits, gate):
        '''
        Add gate to the circuit.
        Parameters:
            qubits: int or 2-tuple
                Qubit or pair of qubits on which the gate acts.
            gate: str
                Which gate is applied.
        Returns :
            None
        '''
        # Add functionality to have named_qubits and if the input qubit is out of range, raise an error.
        self.gates.append((qubits, gate))
        if type(qubits) is tuple:
            assert len(qubits) == 2, f"Only single qubit and 2-qubit gates are allowed. \n In case of single qubit gate, do not give a tuple as input."
            self.two_qubit_gates.append((qubits, gate))

    def add_multiple_gates(self, gate_list):
        '''
        Add multiple gates to the circuit.
        Parameters:
            gate_list : list
                List of tuples. Each tuple includes the qubit(s) and the gate applied on it.
        Returns :
            None
        '''
        for qubits, gate in gate_list:
            self.add_gate(qubits, gate)

    def sliciing(self, chip):
        '''
        Break the circuit down into many slices to be able to map smaller parts first
        Parameters :
            chip : An instance of Chip class
                The chip architecture. Based on the degree of coneectivity, slice the circtuit.
        Returns :
            slices : list
                A list of slices of the array. Each slice is a list of two-qubit gates
        '''
        density = chip.density
        num_of_two_qubit_gates = len(self.two_qubit_gates)
        slice_size = max( int(density*num_of_two_qubit_gates), 1) # slice_size = 1 if int(density*num_qubits) = 0
        slices = [self.two_qubit_gates[i:i+slice_size] for i in range(0, num_of_two_qubit_gates, slice_size)]
        return slices

    def map_it(self, chip, mapping): # Not correct. Have to fix this.
        slices = self.slicing(chip)
        for slice in slices:
            if len(mapping) == self.num_qubits and chip.predicate(mapping, slice):
                print(f"The correct mapping is {mapping.map}")
