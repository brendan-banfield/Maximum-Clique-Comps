from lib.graphs import Graph
import time


class Branch_and_Bound_Solver:
    is_decision_problem = False
    def __init__(self, graph: Graph):
        self.graph = graph
        self.completed = False
        self.succeeded = False
        self.max_clique = 0
        self.max_clique_vertices = []
        self.initial_clique = []

    def get_maximum_clique(self) -> int:
        if not self.completed:
            self.run()
        return self.max_clique

    def run(self):
        # Initializes a list of vertices
        num_vertices = self.graph.vertices
        R = list(range(num_vertices))

        # Returns a coloring of the graph
        # ex: if C = [[0,2],[1,4],[3]], then nodes 0 and 2 have color 0, nodes 1 and 4 have color 1, and node 3 has color 2
        C = self.color_sort(R, self.graph)
        
        # Run recursive algorithm
        solution = self.max_clique_recurse(R, C, self.graph, Q=[], Qmax=[])

        self.max_clique_vertices = solution
        self.max_clique = len(solution)
        self.completed = True
        self.succeeded = True

    # Returns a subgraph of the vertices inputted
    def create_subgraph(self, parent_graph, vertices):

        edges = [
                (u, v) for (u, v) in parent_graph.edges if u in vertices and v in vertices
            ]

        return Graph(parent_graph.vertices, edges)
    
    
    # Returns the list of adjacent nodes to the given node
    def get_neighbors(self, graph, node):
        return graph.get_adj_list()[node]
    
    
    # Returns a list of intersecting elements
    def get_intersect(self, list1, list2):
        return list(set(list1) & set(list2))
    

    def get_max_color(self, C, R):
        max_color = -1
        max_color_node = None
        color = -1
        
        # Loop over the nodes in R to find the one with the highest color
        for node in R:

            # Check the color of the node (node corresponds to an index in R)
            for color_index, color_list in enumerate(C):
                if node in color_list:
                    color = color_index
            
                # Update max_color and max_color_node if needed
                if color > max_color:
                    max_color = color
                    max_color_node = node

        return max_color_node, max_color

    def color_sort(self, R, graph):

        C = []

        for i in range(len(R)):
            p = R[i]  # Current node
            k = 1  # Start with the first color

            # Get the neighbors of the node
            p_neighbors = self.get_neighbors(graph, p)
            
            # Ensure C has enough color classes
            while len(C) < k:
                C.append([])  # Add a new empty color class if needed
            
            # Assign the node to the first available color class
            while len(self.get_intersect(C[k-1], p_neighbors)) > 0:  # Check for intersection with color class
                k += 1
                # Ensure C has enough color classes
                while len(C) < k:
                    C.append([])  # Add a new empty color class if needed

            # Update the color assignment
            C[k-1].append(p)  # Add the node to the correct color class

        return C

    def max_clique_recurse(self, R, C, graph, Q, Qmax):
        while R:  # While there are still vertices to process
            p, max_color = self.get_max_color(C, R)

            if p is None:
                break
            
            R.remove(p)  # Remove the node from R

            p_neighbors = self.get_neighbors(graph, p)

            intersecting_neighbors = self.get_intersect(R, p_neighbors)  # Neighbors of p in R

            if len(Q) + max_color >= len(Qmax):

                Q.append(p)  # Add p to the clique
            
                # If intersection is not empty, continue exploring
                if intersecting_neighbors:
                    C_prime = []  # Prepare a new coloring for the intersecting subgraph
                    new_graph = self.create_subgraph(graph, intersecting_neighbors)
                    C_prime = self.color_sort(intersecting_neighbors, new_graph)
                    Qmax = self.max_clique_recurse(intersecting_neighbors, C_prime, new_graph, Q, Qmax)  # Recurse into the subgraph
            
                elif len(Q) > len(Qmax):  # If we found a larger clique
                    Qmax = Q[:]
                    # Remove the p from Q before returning the max clique or else it breaks
                    Q.remove(p)
                    return Qmax

                Q.remove(p)  # Remove p from the clique for backtracking
            
            else:
                return Qmax

def main():
    graph = Graph.get_graph_from_dataset('v25/2')
    solver = Branch_and_Bound_Solver(graph)
    start_time = time.time()
    solver.run()
    end_time = time.time()
    # alg finds: [23, 22, 21, 14, 12, 11, 9, 8, 7, 5, 4, 3, 1, 0]
    # (sorted: [0, 1, 3, 4, 5, 7, 8, 9, 11, 12, 14, 21, 22, 23])
    # correct max clique: [0, 1, 3, 4, 5, 7, 8, 9, 11, 12, 19, 21, 22, 23, 24]
    print(f"Max clique found is size: {solver.get_maximum_clique()}")
    print(f"clique elements: {solver.max_clique_vertices}")
    print(f"Time taken: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()