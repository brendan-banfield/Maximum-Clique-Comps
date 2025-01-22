import random
import os

class Graph:
    def __init__(self, num_vertices: int, edges: list[tuple], max_clique_size = None, max_clique_elements = None):
        self.vertices: int = num_vertices

        # edges is a list of tuples where each tuple is an edge
        # e.g. [(0, 1), (1, 2)]
        self.edges: list[tuple] = edges

        self.max_clique_size = max_clique_size
        self.max_clique_elements = max_clique_elements

        self.adj_list: list[list[int]] = None
        self.adj_matrix: list[list[bool]] = None

    def populate_adj_list(self) -> None:
        self.adj_list = [[] for _ in range(self.vertices)]
        for edge in self.edges:
            self.adj_list[edge[0]].append(edge[1])
            self.adj_list[edge[1]].append(edge[0])

    def populate_adj_matrix(self) -> None:
        self.adj_matrix = [[0 for _ in range(self.vertices)] for _ in range(self.vertices)]
        for edge in self.edges:
            self.adj_matrix[edge[0]][edge[1]] = 1
            self.adj_matrix[edge[1]][edge[0]] = 1
        
    def get_adj_list(self) ->  list[list[int]]:
        if self.adj_list is None:
            self.populate_adj_list()
        return self.adj_list
    
    def get_adj_matrix(self) ->  list[list[bool]]:
        if self.adj_matrix is None:
            self.populate_adj_matrix()
        return self.adj_matrix

    '''
    Runs an algorithm on the graph and returns the results
    algorithm: callable, should have the following signature:
        algorithm(graph: Graph, k, *args, **kwargs) -> list[int]
    and return None if it did not find a clique of size k, or a list of vertices in the clique if it did.
    k: int, the size of the clique to find
    *args: any arguments to be passed to the algorithm
    **kwargs: any keyword arguments to be passed to the algorithm
    returns: list of integers or None
    '''
    def test_algorithm(self, algorithm: callable, k, *args, **kwargs) -> list[int]:
        return algorithm(self, k, *args, **kwargs)
    
    '''
    Make a random graph with num_vertices vertices and edge_probability probability of an edge between any two vertices
    num_vertices: int
    edge_probability: float between 0 and 1
    returns: Graph object

    '''
    def create_random_graph(num_vertices, edge_probability) -> 'Graph':
        edges = []
        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                if random.random() < edge_probability:
                    edges.append((i, j))
        new_graph = Graph(num_vertices, edges)
        return new_graph
    
    def get_graph_from_dataset(dataset_name: str) -> 'Graph':
        DIMACS_names = [os.path.splitext(name)[0] for name in os.listdir('datasets/DIMACS/')]
        if dataset_name in DIMACS_names:
            return Graph.import_DIMACS_graph(dataset_name)
        else:
            raise ValueError(f'Dataset {dataset_name} not found')
        

    def import_DIMACS_graph(dataset_name: str) -> 'Graph':
        with open(f'datasets/DIMACS/{dataset_name}.clq', 'r') as f:
            lines = f.readlines()
            cur_line = 0
            # while not lines[cur_line].startswith('c Graph Size:'):
            #     cur_line += 1
            # clique_size = int(lines[cur_line].split()[5])

            # while not lines[cur_line].startswith('c Clique Elements are:'):
            #     cur_line += 1   
            # cur_line += 1
            # clique = []
            # while len(lines[cur_line]) > 2:
            #     clique_line = lines[cur_line].split()[1:]
            #     clique_members = [int(x) - 1 for x in clique_line]
            #     clique += clique_members
            #     cur_line += 1
            # assert len(clique) == clique_size

            while not lines[cur_line].startswith('p'):
                cur_line += 1
            num_vertices = int(lines[cur_line].split()[2])
            num_edges = int(lines[cur_line].split()[3])
            edges = []
            for line in lines[cur_line + 1:]:
                if line[0] == 'e':
                    edges.append((int(line.split()[1]) - 1, int(line.split()[2]) - 1))
            return Graph(num_vertices, edges)
            # return Graph(num_vertices, edges, max_clique_size=clique_size, max_clique_elements=clique)

if __name__ == '__main__':
    graph = Graph.create_random_graph(5, 0.5)
    print(graph.get_adj_matrix())
