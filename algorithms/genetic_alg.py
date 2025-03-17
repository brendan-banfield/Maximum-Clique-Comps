from lib.graphs import Graph
import random
import numpy as np
import sys
'''
run
pip install bitarray
if missing import
'''
from bitarray import bitarray

class Genetic_Solver:
    is_decision_problem = False
    def __init__(self, graph: Graph, population_size: int = 500, visualize: bool = False, stagnancy: int = 50, num_cuts_init: int = 10, mutate_prob_init: float = .5):
        self.graph = graph
        self.N = self.graph.vertices
        self.reordered_vertices = None
        self.population_size = population_size
        self.stagnancy = stagnancy
        
        # algorithm variables
        self.succeeded = False
        self.population = []
        self.mutate_prob = mutate_prob_init
        self.num_cuts = num_cuts_init
        self.twenty_gen_count = 0
        self.stagnant_count = 0
        
        self.setup()

    def get_maximum_clique(self) -> int:
        return self.best_clique_size

    def setup(self):
        self.adj_list = self.graph.get_adj_list()
        self.adj_matrix = self.graph.get_adj_matrix()
        # this isn't actually reordered vertices. It's an array of indices of the vertices in the graph. So the "first vertex" in the 
        # new ordering is the vertex in self.reordered_vertices[0]
        self.reordered_vertices = sorted(range(self.N), key=lambda x: len(self.adj_list[x]), reverse=True)
        self.graph.populate_bitvectors()

    def run(self):
        self.population = self.generate_initial_chromosomes()
        while self.stagnant_count < self.stagnancy:
            self.update()
        self.best_clique = max(self.population, key=lambda chrom: self.fitness(chrom))
        
        # ensure is actually clique
        assert self.graph.is_clique(self.best_clique), "Solution found was not clique"
        self.best_clique_size = self.fitness(self.best_clique)
        return f"Largest clique found was {self.best_clique.to01()} with {self.fitness(self.best_clique)} nodes."
        

    def update(self):
        # create children from randomly selected parents
        p1,p2 = self.select_parents()
        c1,c2 = self.crossover(p1,p2)
        self.mutate(c1,c2)
        
        # greedily reduce child chromosome to clique
        self.extract_clique(c1)
        self.extract_clique(c2)
        # greedily make cliques as large as possible
        self.improve_clique(c1)
        self.improve_clique(c2)
        
        # replace members of population with children based on fitness
        self.replace(p1,p2,c1,c2)
        
        # update variables
        self.twenty_gen_count += 1
        if self.twenty_gen_count == 20:
            self.twenty_gen_count = 0
            if self.mutate_prob > .05:
                self.mutate_prob -= .05
            if self.num_cuts > 2:
                self.num_cuts -= 2
            

    def generate_initial_chromosomes(self):
        chromosomes = []
        for _ in range(self.population_size):
            chromosomes.append(self.generate_chromosome())
        return chromosomes
    
    def generate_chromosome(self):
        # create empty subset
        subset = bitarray([0 for _ in range(self.N)])
        # add a random vertex to subset
        v_0 = random.randint(0, self.N - 1)
        subset[v_0] = 1
        # shuffle list of vertex indices in adjaceny list of v_0
        nbr_idx_shuffle = self.graph.get_adj_list()[v_0].copy()
        random.shuffle(nbr_idx_shuffle)
        
        # check all neighbors to see if they can be added
        for v in nbr_idx_shuffle:
            # check if v is adjacent to every vertex in subset
            if self.vert_adjacent_all(v,subset):
                # if so, add to subset
                subset[v] = 1
        
        # subset is a clique
        return subset

    def fitness(self, clique):
        return clique.count()

    def fitness_scaled(self, clique):
        scale_fn = np.sqrt
        return scale_fn(self.fitness(clique))
    
    def select_parents(self):
        # scale clique size with np.sqrt. Since cliques are all locally maximal, clique.count() >= 2 if graph connected,
        # and clique.count() >= 1 always.
        fitness_vals = np.array([self.fitness(clique) for clique in self.population])
        fitness_vals = fitness_vals / sum(fitness_vals)
        pop_idx = range(self.population_size)
        
        # select parents
        p1_idx, p2_idx = np.random.choice(pop_idx, p=fitness_vals, size=2)
        return self.population[p1_idx], self.population[p2_idx]
    
    def crossover(self, p1, p2):
        indices = list(range(len(p1)))
        # sample num_cuts indices with replacement
        cut_points = np.random.choice(indices, size=self.num_cuts, replace=False)
        
        # children should be separate objects as parent replacement is not gauranteed
        c1 = p1.copy()
        c2 = p2.copy()
        
        # 2 cut points per cut
        for i in range(int(self.num_cuts / 2)):
            # crossover from cut point 2i to 2i+1
            c1[cut_points[2*i]:cut_points[2*i + 1]] = p2[cut_points[2*i]:cut_points[2*i + 1]]
            c2[cut_points[2*i]:cut_points[2*i + 1]] = p1[cut_points[2*i]:cut_points[2*i + 1]]
        
        return c1, c2
    
    def mutate(self, c1, c2):
        # mutate c1
        if random.random() < self.mutate_prob:
            gene = random.randint(0,len(c1)-1)
            c1[gene] = 0 if c1[gene] else 1
        # mutate c2
        if random.random() < self.mutate_prob:
            gene = random.randint(0,len(c1)-1)
            c2[gene] = 0 if c2[gene] else 1
    
    def extract_clique(self, subgraph):
        while not self.graph.is_clique(subgraph):
            # find and remove lowest degree vertex
            lowest_deg = self.N
            lowest_deg_v = 0
            for v in range(self.N):
                # only consider verts in subgraph
                if subgraph[v]:
                    # only consider degree w.r.t subgraph
                    deg = (self.graph.get_bitvectors()[v] & subgraph).count()
                    if deg < lowest_deg:
                        lowest_deg = deg
                        lowest_deg_v = v
            subgraph[lowest_deg_v] = 0
    
    def improve_clique(self, clique):
        # induces some randomness in selection order
        i = random.randint(0,self.N-1)
        for v in range(i,self.N):
            # if vert not in clique and connected to all in clique
            if not clique[v] and self.vert_adjacent_all(v,clique):
                clique[v] = 1
        for v in range(i):
            # if vert not in clique and connected to all in clique
            if not clique[v] and self.vert_adjacent_all(v,clique):
                clique[v] = 1
    
    def replace(self, p1, p2, c1, c2):
        best_child = c1 if self.fitness(c1) > self.fitness(c2) else c2
        if self.hamming_dist(p1,best_child) < self.hamming_dist(p2,best_child):
            similar_parent = p1
            other_parent = p2
        else:
            similar_parent = p2
            other_parent = p1
        
        # if we make an improvement, set stagnancy to 0
        if self.fitness(best_child) > self.fitness(similar_parent): # test if improves on similar parent
            similar_parent[:] = best_child # need [:] to modify inplace
            self.stagnant_count = 0
        elif self.fitness(best_child) > self.fitness(other_parent): # test if improves on other parent
            other_parent[:] = best_child
            self.stagnant_count = 0
        elif self.fitness(best_child) > min([self.fitness(chrom) for chrom in self.population]): # test if improves on worst member of population
            worst_chrom = min(self.population, key=lambda chrom: self.fitness(chrom))
            worst_chrom[:] = best_child
            self.stagnant_count = 0
        else:
            self.stagnant_count += 1
    
    def hamming_dist(self,bit1,bit2):
        return (bit1 ^ bit2).count()
    
    def vert_adjacent_all(self, vert_id, subgraph):
        adjacent_to = self.graph.get_bitvectors()[vert_id] & subgraph
        return adjacent_to.count() == subgraph.count()


if __name__ == '__main__':
    args = sys.argv
    if len(args) > 1:
        graph = Graph.get_graph_from_dataset(args[1])
    else:
        graph = Graph.get_graph_from_dataset("keller4")
    
    solver = Genetic_Solver(graph)
    print(solver.run())
        