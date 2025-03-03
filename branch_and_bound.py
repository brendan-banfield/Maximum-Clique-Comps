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

Loosened up the pruning a little bit and it seemes to be running fine on on p_hat300-1 now.
Except the maxclique should be these guys: [17,48,106,148,170,196,224,254]
But B&B returns: [19,47,53,123,204,219,270,299]
They're both size 8, but there could be multiple max cliques of the same size so I'm calling it good.
Let me know if this causes any other results to break - Kellen 2/24

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
        self.initial_clique = []

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

            if len(Q) + max_color >= len(Qmax):

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
    # Graph.test_algorithm(Branch_and_Bound_Solver)
    graph = Graph.get_graph_from_dataset('v25/2')
    solver = Branch_and_Bound_Solver(graph)
    import time
    start_time = time.time()
    solver.run()
    end_time = time.time()
    # alg finds: [23, 22, 21, 14, 12, 11, 9, 8, 7, 5, 4, 3, 1, 0]
    # (sorted: [0, 1, 3, 4, 5, 7, 8, 9, 11, 12, 14, 21, 22, 23])
    # correct max clique: [0, 1, 3, 4, 5, 7, 8, 9, 11, 12, 19, 21, 22, 23, 24]
    print(f"Max clique found is size: {solver.get_maximum_clique()}")
    print(f"clique elements: {solver.max_clique_vertices}")
    print(f"Time taken: {end_time - start_time} seconds")
    # clique = solver.max_clique_vertices
    # print(f"Vertices in clique: {clique}")
    
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