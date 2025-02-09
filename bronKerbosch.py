from graphs import Graph

class Bron_Kerbosch_Solver:
    is_decision_problem = False
    def __init__(self, graph: Graph):
        self.graph = graph
        self.adjacencySets = self.graph.get_adj_sets()
        self.maximal_cliques = []
        self.maximum_clique = set()
        self.succeeded = False

    '''solves Bron Kerbosch without a pivot vertex'''
    def no_pivot_solver(self, P, R, X):
        if not P:
            if not X:
                self.maximal_cliques.append(R)
            return
        
        list_P = list(P)
        while list_P:
            v = list_P[0]
            new_R = R.copy()
            new_R.add(v)
            nbrs_v = self.adjacencySets[v]
            new_P = P & nbrs_v
            new_X = X & nbrs_v
            self.no_pivot_solver(new_P, new_R, new_X)
            P.remove(v)
            list_P.remove(v)
            X.add(v)

    '''solves Bron Kerbosch with a pivot vertex'''
    def pivot_solver(self, P, R, X):
        if not P:
            if not X:
                if self.maximum_clique:
                    if len(R) > len(self.maximum_clique):
                        self.maximum_clique = R
                else:
                    self.maximum_clique = R
                #self.maximal_cliques.append(R)
            return
        
        max_nbrs = 0
        pivot_nbrs = set()
        for node in (P | X):
            nbrs_of_node = self.adjacencySets[node]
            if len(nbrs_of_node & P) > max_nbrs:
                max_nbrs = len(nbrs_of_node & P)
                pivot_nbrs = nbrs_of_node

        loop_P = P - pivot_nbrs
        list_P = list(loop_P)
        while list_P:
            v = list_P[0]      
            new_R = R.copy()
            new_R.add(v)
            nbrs_v = self.adjacencySets[v]
            new_P = P & nbrs_v
            new_X = X & nbrs_v
            self.pivot_solver(new_P, new_R, new_X)
            P.remove(v)
            list_P.remove(v)
            X.add(v)
    
    '''Finds the maximum clique among the maximal cliques produced.'''
    def get_maximum_clique(self):
        max_clique_val = 0
        if self.maximal_cliques:
            for i in range(len(self.maximal_cliques)):
                curr_max = len(self.maximal_cliques[i])
                if curr_max > max_clique_val:
                    max_clique_val = curr_max
            self.succeeded = True
        return max_clique_val

    def found_clique(self):
        return self.succeeded

    '''Creates the input sets for the solver function, and calls the function.
    Returns the # of elements of the maximum clique.
    Could be easily changed to return the clique itself.'''
    def run(self):
        P = {i for i in range(self.graph.vertices)}
        R = set()
        X = set()
        # self.no_pivot_solver(P, R, X)
        self.pivot_solver(P, R, X)
        #return self.get_maximum_clique()
        clique_size = len(self.maximum_clique)
        if clique_size > 0:
            self.succeeded = True
        return len(self.maximum_clique)


if __name__ == "__main__":
    # baby_graph = Graph(5, [(0, 1), (1, 2), (0, 2), (3, 1), (3, 4)])
    # solver = Bron_Kerbosch_Solver(baby_graph)
    # graph = Graph(7, [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3), (1,4), (3,4), (4,6), (3,5)])
    # solver = Bron_Kerbosch_Solver(graph)
    # med_graph = Graph(25, [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (0, 15), (0, 16), (0, 17), (0, 18), (0, 19), (0, 20), (0, 21), (0, 22), (0
    #     , 23), (0, 24), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (1, 16), (1, 17), (1, 18), (1, 19), (1, 20), (1, 21), (1, 
    #     22), (1, 23), (1, 24), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (2, 11), (2, 12), (2, 13), (2, 14), (2, 15), (2, 16), (2, 17), (2, 18), (2, 19), (2, 20), (2, 21), (2, 22), (2, 23), (2, 24), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14), (3, 15), (3, 16), (3, 17), (3, 18), (3, 19), (3, 20), (3, 21), (3, 22), (3, 23), (3, 24), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (4, 15), (4, 16), (4, 17), (4, 18), (4, 19), (4, 20), (4, 21), (4, 22), (4, 23), (4, 24), (5, 
    #     6), (5, 7), (5, 8), (5, 9), (5, 10), (5, 11), (5, 12), (5, 13), (5, 14), (5, 15), (5, 16), (5, 17), (5, 18), (5, 19), (5, 20), (5, 21), (5, 22), (5, 23), (5, 24), (6, 7), (6, 8), (6, 9), (6, 10), (6, 11), (6, 12), (6, 13), (6, 14), (6, 15), (6, 16), (6, 17), (6, 18), (6, 19), (6, 20), (6, 21), (6, 22), (6, 23), (6, 24), (7, 8), (7, 9), (7, 10), (7, 11), (7, 12), (7, 13), (7, 15), (7, 16), (7, 17), (7, 18), (7, 19), (7, 21), (7, 22), (7, 23), (7, 24), (8, 9), (8, 10), (8, 11), (8, 12), (8, 13), (8, 14), (8, 15), (8, 16), (8, 17), (8, 18), (8, 20), (8, 21), (8, 22), (8, 23), (9, 10), (9, 11), (9, 12), (9, 13), (9, 14), (9, 15), (9, 16), (9, 17), (9, 18), (9, 19), (9, 20), (9, 21), (9, 22), (9, 23), (9, 24), (10, 11), (10, 12), (10, 13), (10, 14), (10, 15), (10, 16), (10, 17), (10, 18), (10, 19), (10, 20), (10, 21), (10, 22), (10, 23), (10, 24), (11, 12), (11, 13), (11, 14), (11, 15), (11, 16), (11, 17), (11, 18), (11, 19), (11, 20), (11, 21), (11, 
    #     22), (11, 23), (11, 24), (12, 13), (12, 14), (12, 15), (12, 16), (12, 17), (12, 18), (12, 20), (12, 21), (12, 22), (12, 23), (12, 24), (13, 14), (13, 15), (13, 16), (13, 17), (13, 18), (13, 19), (13, 20), (13, 21), (13, 23), (13, 24), (14, 15), (14, 16), (14, 17), (14, 18), (14, 19), (14, 20), (14, 22), (14, 23), (14, 24), (15, 16), (15, 17), (15, 18), (15, 19), (15, 20), (15, 21), (15, 22), (15, 23), (15, 24), (16, 17), (16, 18), (16, 19), (16, 20), (16, 21), (16, 22), (16, 23), (16, 24), (17, 18), (17, 19), (17, 20), (17, 21), (17, 22), (17, 23), (17, 24), (18, 19), (18, 20), (18, 21), (18, 22), (18, 23), (18, 24), (19, 20), (19, 21), (19, 22), (19, 23), (19, 24), (20, 21), (20, 22), (20, 23), (20, 24), (21, 22), (21, 23), (21, 24), (22, 23), (22, 24), (23, 24)])
    # solver = Bron_Kerbosch_Solver(med_graph)  
    hard_graph = Graph.get_graph_from_dataset('C125.9')
    solver = Bron_Kerbosch_Solver(hard_graph)  
    print(solver.run())
    print(solver.maximum_clique)
    #print(solver.maximal_cliques)
    #Graph.test_algorithm(Bron_Kerbosch_Solver)
    


    