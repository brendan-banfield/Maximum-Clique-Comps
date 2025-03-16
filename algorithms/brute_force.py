from lib.graphs import Graph
from math import pow
from bitarray import bitarray

class Brute_Force_Solver:
    is_decision_problem = True
    def __init__(self, g: Graph, k: int, visualize: bool = False):
        self.g = g
        self.k = k
        self.permutation: bitarray = bitarray([0 for _ in range(g.vertices)])
        self.cliques_found: list[bitarray] = []
        
    def next_permutation(self):
        # increment bitarray, counting in binary where 0th index is first digit.
        i = 0
        while self.permutation[i] != 0:
            # carry the 1s
            self.permutation[i] = 0
            i += 1
        self.permutation[i] = 1
        if len(self.permutation) < 10:
            pass
        
    def found_clique(self):
        for clique in self.cliques_found:
            if clique.count(1) == self.k:
                return True
        return False
    
    def run(self):
        # there are 2^|V|-1 nonempty subsets of V
        for _ in range(int(pow(2, self.g.vertices))-1):
            self.next_permutation()
            if self.g.is_clique(self.permutation.copy()):
                self.cliques_found.append(self.permutation.copy())
        
        return max([clique.count(1) for clique in self.cliques_found])


Graph.test_algorithm(Brute_Force_Solver)