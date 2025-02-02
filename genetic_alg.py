# based on this paper:
# https://h3turing.cs.hbg.psu.edu/mspapers/sources/bo-huang.pdf


from graphs import Graph
'''
run
pip install bitarray
if missing import
'''
from bitarray import bitarray

class Genetic_Solver:
    def __init__(self, graph: Graph, k: int, population_size: int, mutation_rate: float, visualize: bool = False):
        self.graph = graph
        self.reordered_vertices = None
        self.k = k
        self.completed = False
        self.succeeded = False
        self.setup()

    def setup(self):
        self.adj_list = self.graph.get_adj_list()
        self.adj_matrix = self.graph.get_adj_matrix()
        # this isn't actually reordered vertices. It's an array of indices of the vertices in the graph. So the "first vertex" in the 
        # new ordering is the vertex in self.reordered_vertices[0]
        self.reordered_vertices = sorted(range(self.graph.vertices), key=lambda x: len(self.adj_list[x]), reverse=True)
        self.graph.populate_bitvectors()

    def run(self):
        while not self.completed:
            self.update()

    def update(self):
        # TODO
        pass


    def generate_initial_chromosomes(self, n):
        chromosomes = []
        for _ in range(n):
            chromosomes.append(self.generate_chromosome())
        self.generate_chromosome()
    
    def generate_chromosome(self):
        # TODO: generate chromosomes as bit arrays
        pass
    

graph = Graph.get_graph_from_dataset('hamming8-4')
solver = Genetic_Solver(graph, 4, 100, 0.01)
solver.run()
print('done')