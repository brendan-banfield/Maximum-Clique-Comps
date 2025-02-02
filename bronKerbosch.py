from graphs import Graph

class Bron_Kerbosch_Solver:
    def __init__(self, graph: Graph):
        # self.compsub_R = [] -- implement this as global?
        self.graph = graph
        self.adjacencyList = self.graph.get_adj_list()
        #print(self.adjacencyList)
        self.maximal_cliques = []


    def no_pivot_solver(self, candidates_P, compsub_R, not_X):
        #print("candidates 1: {0}".format(candidates_P))
        if not candidates_P:
            #print("i am done for now")
            if not not_X:
                self.maximal_cliques.append(compsub_R)
            return
        
        #print("i am above")
        for v in candidates_P:
            #print("i am in loop and v = {0}".format(v))
            compsub_R.append(v)

            new_candidates_P = [] #intersection nbrs(v). see below
            for node in candidates_P:
                if node in self.adjacencyList[v]:
                    new_candidates_P.append(node)
            
            new_not_X = [] #intersection nbrs(v). see below
            for node in not_X:
                if node in self.adjacencyList[v]:
                    new_not_X.append(node)
            # print("candidates: " + new_candidates_P)
            # print("compsub: " + compsub_R)
            # print("not: " + new_not_X)
            #print("candidates before: {0}".format(candidates_P))
            self.no_pivot_solver(new_candidates_P, compsub_R, new_not_X)
            #print("v: {0}".format(v))
            #print("candidates after: {0}".format(candidates_P))
            candidates_P.remove(v)
            not_X.append(v)
    
    def get_maximum_clique():
        pass

    def run(self):
        candidates = [i for i in range(self.graph.vertices)]
        #print(candidates)
        compsub = []
        not_x = []
        self.no_pivot_solver(candidates, compsub, not_x)
        #return biggest clique


if __name__ == "__main__":
    graph = Graph.get_graph_from_dataset('C250.9')
    solver = Bron_Kerbosch_Solver(graph)
    solver.run()
    print(solver.maximal_cliques)


    