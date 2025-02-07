from graphs import Graph

class Bron_Kerbosch_Solver:
    is_decision_problem = False
    def __init__(self, graph: Graph):
        self.graph = graph
        self.adjacencyList = self.graph.get_adj_list()
        self.maximal_cliques = []
        self.succeeded = False

    '''solves Bron Kerbosch without a pivot vertex'''
    def no_pivot_solver(self, candidates_P, compsub_R, not_X):
        print("compsub: {0}".format(compsub_R))
        print("candidates: {0}".format(candidates_P))
        print("not: {0}".format(not_X))
        if not candidates_P:
            if not not_X:
                self.maximal_cliques.append(compsub_R)
            return
        
        i = 0
        while i < len(candidates_P):
            v = candidates_P[i]
            new_compsub_R = compsub_R.copy()
            new_compsub_R.append(v)

            new_candidates_P = [] 
            for node in candidates_P:
                if node in self.adjacencyList[v]:
                    new_candidates_P.append(node)
            
            new_not_X = [] 
            if not_X:
                for node in not_X:
                    if node in self.adjacencyList[v]:
                        new_not_X.append(node)
            self.no_pivot_solver(new_candidates_P, new_compsub_R, new_not_X)
            candidates_P.remove(v)
            not_X.append(v)

    '''solves Bron Kerbosch with a pivot vertex'''
    #choosing pivot based on og paper version 1
    def pivot_solver(self, P, R, X):
        if not P:
            if not X:
                self.maximal_cliques.append(R)
            return
        
        pivot = 0
        max_nbrs = 0
        pivot_nbrs = set()
        print(P | X)
        for node in (P | X):
            print(node)
            # node = int(node)
            nbrs_of_node = set(self.adjacencyList[int(node)])
            if len(nbrs_of_node & P) > max_nbrs:
                max_nbrs = len(nbrs_of_node & P)
                pivot = int(node)
                pivot_nbrs = nbrs_of_node


        loop_P = P - pivot_nbrs
        list_P = list(loop_P)
        # for node in P:
            # if P(i) in self.adjacencyList(pivot):        
            #     v = P[i]
            # if node not in self.adjacencyList[pivot]:
        i = 0
        while i < len(list_P):
            v = list_P[i]      
            new_R = R.copy()
            new_R.add(v)

            
            nbrs_v = set(self.adjacencyList[v])
            new_P = P & nbrs_v
            
            new_X = X & nbrs_v

            self.pivot_solver(new_P, new_R, new_X)
            P.remove(v)
            list_P.remove(v)
            X.add(v)
    
    '''finds the maximum clique among the maximal cliques produced'''
    def get_maximum_clique(self):
        max_clique_val = 0
        if self.maximal_cliques:
            max_clique_val = len(self.maximal_cliques[0])
            max_clique_index = 0
            for i in range(1, len(self.maximal_cliques)):
                value = len(self.maximal_cliques[i])
                if value > max_clique_val:
                    max_clique_index = i
                    max_clique_val = value
            self.succeeded = True
        return max_clique_val

    def found_clique(self):
        return self.succeeded

    def run(self):
        # candidates = {}
        # for i in range(self.graph.vertices):
        #     candidates.append((i, len(self.adjacencyList[i])))

        # candidates = {i for i in range(self.graph.vertices)}
        candidates = set()
        for i in range(self.graph.vertices):
            candidates.add(i)
        compsub = set()
        not_x = set()
        # self.no_pivot_solver(candidates, compsub, not_x)
        self.pivot_solver(candidates, compsub, not_x)
        return self.get_maximum_clique()


if __name__ == "__main__":
    # baby_graph = Graph(5, [(0, 1), (1, 2), (0, 2), (3, 1), (3, 4)])
    # solver = Bron_Kerbosch_Solver(baby_graph)
    graph = Graph(7, [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3), (1,4), (3,4), (4,6), (3,5)])
    solver = Bron_Kerbosch_Solver(graph)
    print(solver.run())
    print(solver.maximal_cliques)
    #Graph.test_algorithm(Bron_Kerbosch_Solver)
    


    