from graphs import Graph
import random
import math

class Simulated_Annealing_Solver:
    is_decision_problem = True
    def __init__(self, graph: Graph, k: int, T_0: float, T_f: float, alpha: float, visualize: bool = False):
        self.graph = graph
        self.k = k
        self.T_0 = T_0
        self.T_f = T_f
        self.T = T_0
        self.alpha = alpha
        self.completed = False
        self.succeeded = False
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
        v2 = random.randint(self.k, self.graph.vertices - 1)
        c_delta = self.connectedness_delta(v1, v2)
        
        if c_delta > 0 or random.random() < math.exp(c_delta / self.T):
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
            
        self.T *= self.alpha
        if self.T < self.T_f:
            self.completed = True

    def current_active_nodes(self):
        return self.permutation[:self.k]
    
    def is_completed(self):
        return self.completed
    
    def found_clique(self):
        return self.succeeded
        

    def run(self):
        while not self.completed:
            self.update()
        return f"Succeeded: {self.succeeded}, best score: {self.best_score}"

Graph.test_algorithm(Simulated_Annealing_Solver, 100, 0.001, 0.9998)

graph = Graph.get_graph_from_dataset('hamming8-4')
solver = Simulated_Annealing_Solver(graph, 16, 100, 0.001, 0.9998) 
graph.visualize_algorithm(solver, 0.01, False)
for i in range(20):
    solver = Simulated_Annealing_Solver(graph, 16, 100, 0.001, 0.9998) 
    print(solver.run())
    # if solver.succeeded:
    print(solver.best_nodes)
    # print(simulated_annealing(graph, 44, 100, 0.001, 0.9998))
