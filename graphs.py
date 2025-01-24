import random
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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
        
    def populate_adj_matrix_from_adj_list(self) -> None:
        self.adj_matrix = [[0 for _ in range(self.vertices)] for _ in range(self.vertices)]
        for v in range(self.vertices):
            for u in self.adj_list[v]:
                self.adj_matrix[v][u] = 1
                self.adj_matrix[u][v] = 1
        
    def get_adj_list(self) ->  list[list[int]]:
        if self.adj_list is None:
            self.populate_adj_list()
        return self.adj_list
    
    def get_adj_matrix(self) ->  list[list[bool]]:
        if self.adj_matrix is None:
            self.populate_adj_matrix()
        return self.adj_matrix
    
    def remove_small_vertices(self, k_min) -> None:
        adj_list = self.get_adj_list()
        adj_list_dict = dict(zip(range(len(adj_list)), adj_list))
        
        vertices_to_remove = [v for (v, neighbors) in adj_list_dict.items() if len(neighbors) < k_min]
        
        
        while vertices_to_remove:
            for v in vertices_to_remove:
                for neighbor in adj_list[v]:
                    adj_list[neighbor].remove(v)
            for v in vertices_to_remove:
                del adj_list_dict[v]
            
            vertices_to_remove = [v for (v, neighbors) in adj_list_dict.items() if len(neighbors) < k_min]

        remappings = {}
        remap_idx = 0
        keys = adj_list_dict.keys()
        for v in keys:
            remappings[v] = remap_idx
            remap_idx += 1
        
        new_adj_list = []
        for v in keys:
            new_adj_list.append([remappings[neighbor] for neighbor in adj_list_dict[v]])

        self.adj_list = new_adj_list
        self.vertices = len(new_adj_list)
        self.populate_adj_matrix_from_adj_list()


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
    

    def visualize_algorithm(self, algorithm_instance, dt) -> None:
        # algorithm_instance: A pre-initialized instance of a class that solves the clique problem. Must implement:
        #    - algorithm_instance.current_active_nodes() -> list[int] of the nodes that should be colored active at the current timestep
        #    - algorithm_instance.update() -> None, updates the state of the algorithm by one step
        active_color = "black"
        inactive_color = "lightgray"

        x_positions = []
        y_positions = []
        for _ in range(self.vertices):
            x_positions.append(random.randint(0, 100))
            y_positions.append(random.randint(0, 100))
        fig, ax = plt.subplots()
        ax.set_xlim(0,100)
        ax.set_ylim(0,100)
        points = ax.scatter(x_positions, y_positions, color=inactive_color)
        active_nodes = algorithm_instance.current_active_nodes()
        points.set_color([active_color if v in active_nodes else inactive_color for v in range(self.vertices)])

        # for v in range(self.vertices):
        #     for u in self.adj_list[v]:
        #         ax.plot([x_positions[v], x_positions[u]], [y_positions[v], y_positions[u]], color=inactive_color)

        def update_display(i):
            algorithm_instance.update()
            active_nodes = algorithm_instance.current_active_nodes()
            points.set_color([active_color if v in active_nodes else inactive_color for v in range(self.vertices)])
       
        ani = animation.FuncAnimation(fig, update_display, list(range(1000)), interval=dt)
        plt.show()
    
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
    graph = Graph.get_graph_from_dataset('p_hat300-3')
    # graph = Graph(5, [(0, 1), (1, 2), (0, 2), (3, 1), (3, 4)] )
    print(graph.vertices)
    adj_list = graph.get_adj_list()
    # print([len(adj_list[i]) for i in range(graph.vertices)])
    graph.remove_small_vertices(35)
    print(graph.vertices)
    # print([len(adj_list[i]) for i in range(graph.vertices)])
