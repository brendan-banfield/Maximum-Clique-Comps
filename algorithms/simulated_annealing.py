from lib.graphs import Graph
import random
import math
import sys

class Simulated_Annealing_Solver:
    is_decision_problem = True
    def __init__(self, graph: Graph, k: int, T_0: float, T_f: float, alpha: float):
        self.graph = graph
        self.k = k
        self.T_0 = T_0
        self.T_f = T_f
        self.T = T_0
        self.alpha = alpha
        self.completed = False
        self.succeeded = False

        self.improved_score = 0
        self.total_iterations = 0
        self.setup()

    def connectedness_delta(self, v1, v2):
        # v1_connectedness = sum([1 for v in range(k) if v1 != v and adjecency_matrix[permutation[v1]][permutation[v]]])
        # v2_connectedness = sum([1 for v in range(k) if v1 != v and adjecency_matrix[permutation[v2]][permutation[v]]])
        # return v2_connectedness - v1_connectedness
        # the 1 liner below does that ^
    
        return sum([self.adjecency_matrix[self.permutation[v2]][self.permutation[v]] - self.adjecency_matrix[self.permutation[v1]][self.permutation[v]] for v in range(self.k) if v != v1])

    def num_missing_edges(self):
        return sum([1 for i in range(self.k-1) for j in range(i + 1, self.k) if not self.adjecency_matrix[self.permutation[i]][self.permutation[j]]])

    def setup(self):
        self.permutation = list(range(self.graph.vertices))
        self.adjecency_matrix = self.graph.get_adj_matrix()
        self.adjecency_list = self.graph.get_adj_list()

        # sort by degree
        self.permutation.sort(key=lambda x: len(self.adjecency_list[x]), reverse=True)
        self.running_clique_score = self.num_missing_edges()
        self.best_score = self.running_clique_score
        self.best_nodes = self.permutation[:self.k]
        if self.running_clique_score == 0:
            self.completed = True
            self.succeeded = True
        
    def update(self):
        if self.completed:
            return
        v1 = random.randint(0, self.k - 1)

        misses = 0
        connectedness_cache = {}
        cache_hits = {}
        while misses < 8 * self.graph.vertices:
        # while misses < 8 * self.graph.vertices:
            v2 = random.randint(self.k, self.graph.vertices - 1)
            if v2 in connectedness_cache:
                c_delta = connectedness_cache[v2]
            else:
                c_delta = self.connectedness_delta(v1, v2)
                connectedness_cache[v2] = c_delta
            if c_delta >= 0:
                break
            misses += 1

        if c_delta > 0:
            self.improved_score += 1
        self.total_iterations += 1
        
        if c_delta >= 0 or random.random() < math.exp(c_delta / self.T):
            self.permutation[v1], self.permutation[v2] = self.permutation[v2], self.permutation[v1]
            self.running_clique_score -= c_delta
            if self.running_clique_score < self.best_score:
                self.best_score = self.running_clique_score
                self.best_nodes = self.permutation[:self.k]
            if self.running_clique_score == 0:
                self.completed = True
                self.succeeded = True
                return
                # return f"Succeeded: {permutation[:k]}"
        # print(self.T)
        self.T *= self.alpha
        if self.T < self.T_f:
            self.completed = True

    def current_active_nodes(self):
        return self.permutation[:self.k]
    
    def is_completed(self):
        return self.completed
    
    def found_clique(self):
        return self.succeeded
        
    def get_maximum_clique(self):
        if self.succeeded:
            return self.k
        return 0

    def run(self):
        while not self.completed:
            self.update()
        # print(f"Improved score {self.improved_score} / {self.total_iterations}")
        return f"Succeeded: {self.succeeded}, best score: {self.best_score}"
    

    def binary_search(graph, T_0, T_f, alpha, k_min = 3, num_attempts = 2, k_max = None):
        k = k_min
        while k_min != k_max:
            if k_max == None:
                k = k_min * 2
            else:
                k = (k_min + k_max + 1) // 2
            succeeded = False
            for _ in range(num_attempts):
                solver = Simulated_Annealing_Solver(graph, k, T_0, T_f, alpha)
                solver.run()
                succeeded = solver.succeeded
                if succeeded:
                    break
            if succeeded:
                k_min = k
                print(f"Succeeded with k = {k}. New bounds: {k_min}, {k_max}")
            else:
                print(f"Failed with k = {k}. New bounds: {k_min}, {k_max}")
                k_max = k - 1
            
        print(f"Final k: {k_min}")

if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        graph = Graph.get_graph_from_dataset(args[1])
    else:
        graph = Graph.get_graph_from_dataset("keller4")
    
    successes = 0
    for i in range(5):
        solver = Simulated_Annealing_Solver(graph, 11, 100, 0.001, 0.9995) 
        solver.run()
        if solver.succeeded:
            successes += 1
        print(solver.succeeded)
            
        #print(solver.best_nodes)
        # print(simulated_annealing(graph, 44, 100, 0.001, 0.9998))
    print(successes / 5)
