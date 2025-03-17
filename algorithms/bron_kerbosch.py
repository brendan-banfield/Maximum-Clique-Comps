from lib.graphs import Graph

class Bron_Kerbosch_Solver:
    is_decision_problem = False
    def __init__(self, graph: Graph):
        self.graph = graph
        self.adjacencySets = self.graph.get_adj_sets()
        self.maximum_clique_size = 0
        self.succeeded = False
    
    def solver(self):
        raise NotImplementedError("Subclasses must implement this method")

    '''Returns the size of the maximum clique.'''
    def get_maximum_clique(self):
        if self.maximum_clique_size > 0:
            self.succeeded = True
        return self.maximum_clique_size

    def found_clique(self):
        return self.succeeded

    '''Creates the input sets for the solver function, and calls the function.
    Returns the # of elements of the maximum clique.
    Could be easily changed to return the clique itself.'''
    def run(self):
        P = {i for i in range(self.graph.vertices)}
        R = set()
        X = set()
        self.solver(P, R, X)
        return self.get_maximum_clique()
        

class No_Pivot_Solver(Bron_Kerbosch_Solver):
    '''solves Bron Kerbosch without a pivot vertex'''
    def solver(self, P, R, X):
        if not P:
            if not X:
                if self.maximum_clique_size > 0:
                    if len(R) > self.maximum_clique_size:
                        self.maximum_clique_size = len(R)
                else:
                    self.maximum_clique_size = len(R)
            return
        
        list_P = list(P)
        while list_P:
            v = list_P[0]
            new_R = R.copy()
            new_R.add(v)
            nbrs_v = self.adjacencySets[v]
            new_P = P & nbrs_v
            new_X = X & nbrs_v
            self.solver(new_P, new_R, new_X)
            P.remove(v)
            list_P.remove(v)
            X.add(v)



class Pivot_Solver(Bron_Kerbosch_Solver):
    '''solves Bron Kerbosch with a pivot vertex'''
    def solver(self, P, R, X):
        if not P:
            if not X:
                if self.maximum_clique_size > 0:
                    if len(R) > self.maximum_clique_size:
                        self.maximum_clique_size = len(R)
                else:
                    self.maximum_clique_size = len(R)
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
            self.solver(new_P, new_R, new_X)
            P.remove(v)
            list_P.remove(v)
            X.add(v)

if __name__ == "__main__":
    Graph.test_algorithm(Pivot_Solver)
    