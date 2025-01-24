from graphs import Graph
import random
import math

def simulated_annealing(graph: Graph, k: int, T_0: float, T_f: float, alpha: float) -> list[int]:
    permutation = list(range(graph.vertices))
    # sort by degree
    adjecency_list = graph.get_adj_list()
    permutation.sort(key=lambda x: len(adjecency_list[x]), reverse=True)

    adjecency_matrix = graph.get_adj_matrix()

    def connectedness_delta(v1, v2):
        v1_connectedness = 0
        for v in range(k):
            if v1 != v and adjecency_matrix[permutation[v1]][permutation[v]]:
                v1_connectedness += 1
        v2_connectedness = 0
        for v in range(k):
            if v1 != v and adjecency_matrix[permutation[v2]][permutation[v]]:
                v2_connectedness += 1
        return v2_connectedness - v1_connectedness
    
    def is_clique():
        return sum([1 for i in range(k-1) for j in range(i + 1, k) if not adjecency_matrix[permutation[i]][permutation[j]]])
    
    T = T_0
    max_occurences = 8 * graph.vertices
    best_score = graph.vertices ** 2
    while T > T_f:

        v1 = random.randint(0, k - 1)
        v2 = random.randint(k, graph.vertices - 1)
        c_delta = connectedness_delta(v1, v2)
        
        if c_delta > 0 or random.random() < math.exp(c_delta / T):
            permutation[v1], permutation[v2] = permutation[v2], permutation[v1]
            clique_score = is_clique()
            if clique_score == 0:
                return permutation[:k]
            if clique_score < best_score:
                best_score = clique_score
        T *= alpha
    return None

    

graph = Graph.get_graph_from_dataset('c-fat200-2')
for i in range(20):
    print(simulated_annealing(graph, 24, 100, 0.001, 0.9996))
