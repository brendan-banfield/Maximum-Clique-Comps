'''
This program returns the largest clique and the size of it.

I removed the print statements from this one, so it should
run faster and have cleaner output.

It DOES require that, in graphs.py, populate_adj_list() looks like:

def populate_adj_list(self) -> None:
        self.adj_list = [[] for _ in range(self.vertices)]

        for edge in self.edges:
            while len(self.adj_list) - 1 < edge[1]:
                self.adj_list.append([])
            self.adj_list[edge[0]].append(edge[1])
            self.adj_list[edge[1]].append(edge[0])

The only difference is the while-loop that adds an empty list to the end of the adj_list
to prevent the program from hitting an indexing error. I don't know if changing this would
break anyone else's code, so I'm just keeping the modified version in my local repository.
- Kellen

Fixed; create_subgraph was creating a graph using the same vertex labels as the parent graph, but setting a lower number of vertices,
so there were out of bounds edges. I made the subgraph have the same vertex count as the original. This might not be optimal, we can look at it later.
- Brendan

In the case where it would add a vertex that it shouldn't have, it just needed to remove p from Q after reassigning Qmax
before returning. Otherwise, p would still be in Q when it returned and never be properly cleared.
- Kellen

'''

from graphs import Graph


class Branch_and_Bound_Solver:
    is_decision_problem = False
    def __init__(self, graph: Graph):
        self.graph = graph
        self.completed = False
        self.succeeded = False
        self.max_clique = 0
        self.max_clique_vertices = []

    def get_maximum_clique(self) -> int:
        if not self.completed:
            self.run()
        return self.max_clique

    def run(self):
        # Initializes a list of vertices
        num_vertices = self.graph.vertices
        R = self.populate_R(num_vertices)

        # Returns a list of the nodes from R
        # The indices of this list represents the nodes' colors
        # ex: if C = [1,2,3], then node 1 has color 0, node 2 has color 1, and node 3 has color 2
        C = self.ColorSort(R, self.graph)

        Q = []  # Initialize the current clique
        Qmax = []  # Initialize the maximum clique

        # Runs the branch and bound
        Qmax = self.MaxClique(R, C, self.graph, Q, Qmax)

        # Spits out the results
        # print('Final max clique:')
        # print(Qmax)
        # print('Final max clique size:')
        # print(len(Qmax))
        self.max_clique_vertices = Qmax
        self.max_clique = len(Qmax)
        self.completed = True
        self.succeeded = True

    def update(self):
        pass

    
    # Returns a subgraph of the vertices inputted
    def create_subgraph(self, parent_graph, vertices):

        edges = [
                (u, v) for (u, v) in parent_graph.edges if u in vertices and v in vertices
            ]

        return Graph(parent_graph.vertices, edges)
    
    
    # Returns the list of adjacent nodes to the given node
    # 
    # From what I can tell none of these failsafes can/should be reached. I'll leave this for now, but 
    # we may want to remove it so that we get error messages if something actually does go wrong
    # - Brendan
    def get_neighbors(self, graph, node):

        adj_list = graph.get_adj_list()

        if type(node) == list:
            node = node[0]
            
        if adj_list == [[]]:
            neighbors = []

        elif len(adj_list) <= node:
            neighbors = []

        else:
            neighbors = adj_list[node]
        
        return neighbors
    
    
    # Returns a list of intersecting elements
    def get_intersect(self, list1, list2):
        return list(set(list1) & set(list2))
        # intersection = []
        # for element in list1:
        #     if element in list2:
        #         intersection.append(element)
        # return intersection
    

    # Adds all of our vertices to R (as ints starting from 0)
    def populate_R(self, num_vertices):
        R = []
        for i in range(0, num_vertices):
            R.append(i)  
        return R

    def get_max_color(self, C, R):
        max_color = -1
        max_color_node = None
        color = -1
        
        # Loop over the nodes in R to find the one with the highest color
        for node in R:

            # Check the color of the node (node corresponds to an index in R)
            # We expect C to be a list of color classes
            for color_index, index_list in enumerate(C):
                if type(index_list) == list:
                    if node in index_list:
                        color = color_index  # The color of the node is its index in C

                elif node == index_list:
                    color = color_index
            
                # Update max_color and max_color_node if needed
                if color > max_color:
                    max_color = color
                    max_color_node = node

        return max_color_node, max_color

    def ColorSort(self, R, graph):

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

    def MaxClique(self, R, C, graph, Q, Qmax):
        while R:  # While there are still vertices to process
            p, max_color = self.get_max_color(C, R)

            if p is None:
                break
            
            R.remove(p)  # Remove the node from R

            p_neighbors = self.get_neighbors(graph, p)

            intersecting_neighbors = self.get_intersect(R, p_neighbors)  # Neighbors of p in R

            if len(Q) + max_color > len(Qmax):

                Q.append(p)  # Add p to the clique
            
                # If intersection is not empty, continue exploring
                if intersecting_neighbors:
                    C_prime = []  # Prepare a new coloring for the intersecting subgraph
                    new_graph = self.create_subgraph(graph, intersecting_neighbors)
                    C_prime = self.ColorSort(intersecting_neighbors, new_graph)
                    Qmax = self.MaxClique(intersecting_neighbors, C_prime, new_graph, Q, Qmax)  # Recurse into the subgraph
            
                elif len(Q) > len(Qmax):  # If we found a larger clique
                    Qmax = Q[:]
                    # Remove the p from Q before returning the max clique or else it breaks
                    Q.remove(p)
                    return Qmax

                Q.remove(p)  # Remove p from the clique for backtracking
            
            else:
                return Qmax

def main():
    # Just have it set to the med_graph from graphs.py
#    my_graph = Graph(25, [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (0, 15), (0, 16), (0, 17), (0, 18), (0, 19), (0, 20), (0, 21), (0, 22), (0
#        , 23), (0, 24), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (1, 16), (1, 17), (1, 18), (1, 19), (1, 20), (1, 21), (1, 
#        22), (1, 23), (1, 24), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (2, 11), (2, 12), (2, 13), (2, 14), (2, 15), (2, 16), (2, 17), (2, 18), (2, 19), (2, 20), (2, 21), (2, 22), (2, 23), (2, 24), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14), (3, 15), (3, 16), (3, 17), (3, 18), (3, 19), (3, 20), (3, 21), (3, 22), (3, 23), (3, 24), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (4, 15), (4, 16), (4, 17), (4, 18), (4, 19), (4, 20), (4, 21), (4, 22), (4, 23), (4, 24), (5, 
#        6), (5, 7), (5, 8), (5, 9), (5, 10), (5, 11), (5, 12), (5, 13), (5, 14), (5, 15), (5, 16), (5, 17), (5, 18), (5, 19), (5, 20), (5, 21), (5, 22), (5, 23), (5, 24), (6, 7), (6, 8), (6, 9), (6, 10), (6, 11), (6, 12), (6, 13), (6, 14), (6, 15), (6, 16), (6, 17), (6, 18), (6, 19), (6, 20), (6, 21), (6, 22), (6, 23), (6, 24), (7, 8), (7, 9), (7, 10), (7, 11), (7, 12), (7, 13), (7, 15), (7, 16), (7, 17), (7, 18), (7, 19), (7, 21), (7, 22), (7, 23), (7, 24), (8, 9), (8, 10), (8, 11), (8, 12), (8, 13), (8, 14), (8, 15), (8, 16), (8, 17), (8, 18), (8, 20), (8, 21), (8, 22), (8, 23), (9, 10), (9, 11), (9, 12), (9, 13), (9, 14), (9, 15), (9, 16), (9, 17), (9, 18), (9, 19), (9, 20), (9, 21), (9, 22), (9, 23), (9, 24), (10, 11), (10, 12), (10, 13), (10, 14), (10, 15), (10, 16), (10, 17), (10, 18), (10, 19), (10, 20), (10, 21), (10, 22), (10, 23), (10, 24), (11, 12), (11, 13), (11, 14), (11, 15), (11, 16), (11, 17), (11, 18), (11, 19), (11, 20), (11, 21), (11, 
#        22), (11, 23), (11, 24), (12, 13), (12, 14), (12, 15), (12, 16), (12, 17), (12, 18), (12, 20), (12, 21), (12, 22), (12, 23), (12, 24), (13, 14), (13, 15), (13, 16), (13, 17), (13, 18), (13, 19), (13, 20), (13, 21), (13, 23), (13, 24), (14, 15), (14, 16), (14, 17), (14, 18), (14, 19), (14, 20), (14, 22), (14, 23), (14, 24), (15, 16), (15, 17), (15, 18), (15, 19), (15, 20), (15, 21), (15, 22), (15, 23), (15, 24), (16, 17), (16, 18), (16, 19), (16, 20), (16, 21), (16, 22), (16, 23), (16, 24), (17, 18), (17, 19), (17, 20), (17, 21), (17, 22), (17, 23), (17, 24), (18, 19), (18, 20), (18, 21), (18, 22), (18, 23), (18, 24), (19, 20), (19, 21), (19, 22), (19, 23), (19, 24), (20, 21), (20, 22), (20, 23), (20, 24), (21, 22), (21, 23), (21, 24), (22, 23), (22, 24), (23, 24)])
    
    # Graph.test_algorithm(Branch_and_Bound_Solver)
    graph = Graph.get_graph_from_dataset('c-fat200-1')
    solver = Branch_and_Bound_Solver(graph)
    solver.run()
    print(f"Max clique found is size: {solver.get_maximum_clique()}")
    clique = solver.max_clique_vertices
    print(f"Vertices in clique: {clique}")
    
# Tells us which vertices in the "max clique" shouldn't be in the max clique
# I'm keeping it because it may be useful if it breaks again
#    for i in clique:
#        for j in clique:
#            if i > j:
#                if not graph.get_adj_matrix()[i][j]:
#                    print(f"Error: {i} and {j} are not connected")

    # Graph.test_algorithm(Branch_and_Bound_Solver)

if __name__ == "__main__":
    main()
