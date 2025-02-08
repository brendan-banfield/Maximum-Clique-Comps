'''
This returns the size of the largest clique found and it works.

This will be the version used for debugging because it has a lot of
useful print statements that let us know what's going on.

Based on the algorithms in this paper: http://insilab.org/articles/match2007.pdf
'''


# I'm having this one use modified_graphs because it will crash otherwise
import modified_graphs

def create_subgraph(parent_graph, vertices):

    print('create_subgraph: parent graph edges')
    print(parent_graph.edges)


    edges = [
            (u, v) for (u, v) in parent_graph.edges if u in vertices and v in vertices
        ]
    
    print('create_subgraph: vertices and edges')
    print(vertices)
    print(edges)
    

    return modified_graphs.Graph(len(vertices), edges)

# Returns the list of adjacent nodes to the given node
def get_neighbors(graph, node):

    adj_list = graph.get_adj_list()

    print('get_neighbors: adj_list')
    print(adj_list)
    
    if type(node) == list:
        node = node[0]
        
    if adj_list == [[]]:
        neighbors = []

    elif len(adj_list) <= node:
        neighbors = []

    else:
        neighbors = adj_list[node]
    
    print('get neighbors: ps neighbors')
    print(neighbors)
    return neighbors

# Returns a list of intersecting elements
def get_intersect(list1, list2):
    intersection = []
    for element in list1:
        if element in list2:
            intersection.append(element)
    return intersection

# Adds all of our vertices to R (as ints starting from 0)
def populate_R(num_vertices):
    R = []
    for i in range(0, num_vertices):
        R.append(i)  
    return R

def get_max_color(C, R):
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


def ColorSort(R, graph):

    C = []

    max_no = 1  # Keep track of the maximum color assigned
    kmin = len(C) - len(R) + 1  # Minimum color value 
    if kmin <= 0:
        kmin = 1

    j = 0

    for i in range(len(R)):
        p = R[i]  # Current node
        k = 1  # Start with the first color

        # Get the neighbors of the node
        p_neighbors = get_neighbors(graph, p)

        print('colorsort: p_neighbors')
        print(p_neighbors)
        
        # Ensure C has enough color classes
        while len(C) < k:
            C.append([])  # Add a new empty color class if needed
        
        # Assign the node to the first available color class
        while len(get_intersect(C[k-1], p_neighbors)) > 0:  # Check for intersection with color class
            k += 1
            # Ensure C has enough color classes
            while len(C) < k:
                C.append([])  # Add a new empty color class if needed
                max_no = len(C)

        # Update the color assignment
        C[k-1].append(p)  # Add the node to the correct color class
        if k < kmin:
            print('R updated')
            R[j] = R[i]
            j += 1  # Move the node in R to a valid position


    return C



def MaxClique(R, C, graph, Q, Qmax):
    while R:  # While there are still vertices to process
        p, max_color = get_max_color(C, R)

        print('p')
        print(p)

        print('maxcolor')
        print(max_color)

        if p is None:
            break
        
        R.remove(p)  # Remove the node from R

        print('R after removal')
        print(R)

        p_neighbors = get_neighbors(graph, p)
        intersecting_neighbors = get_intersect(R, p_neighbors)  # Neighbors of p in R

        print('q')
        print(Q)
        print('qmax')
        print(Qmax)
    

        if len(Q) + max_color > len(Qmax):

        
            Q.append(p)  # Add p to the clique
            print('Q after appending')
            print(Q)
        
            # If intersection is not empty, continue exploring
            if intersecting_neighbors:
                C_prime = []  # Prepare a new coloring for the intersecting subgraph
                new_graph = create_subgraph(graph, intersecting_neighbors)

                print('MaxClique: new graph adj list')
                print(new_graph.get_adj_list())
                C_prime = ColorSort(intersecting_neighbors, new_graph)
                print('C_prime coloring')
                print(C_prime)
                Qmax = MaxClique(intersecting_neighbors, C_prime, new_graph, Q, Qmax)  # Recurse into the subgraph
        
            elif len(Q) > len(Qmax):  # If we found a larger clique
                print('WE HIT OUR ELIF STATEMENT QMAX HAS BEEN UPDATED')
                Qmax = Q[:]
                print(Qmax)

                # VERY IFFY NOT SURE IF IT'LL WORK BUT LET'S FIND OUT
                return Qmax
 
            print('q before removal')
            print(Q)
            Q.remove(p)  # Remove p from the clique for backtracking

            print('q after removal')
            print(Q)
        
        else:
            print('max color')
            print(max_color)
            print('max clique found')
            print(Qmax)
            return Qmax



def main():
    my_graph = modified_graphs.Graph(6, [(0, 1), (0, 4), (1, 2), (1,3), (1,5),(2,3), (2,5), (3,4), (3,5), (4,5)])
    num_vertices = my_graph.vertices
    R = populate_R(num_vertices)

    
    C = ColorSort(R, my_graph)

    print("Initial Coloring:")
    print(C)
    

    Q = []  # Initialize the current clique
    Qmax = []  # Initialize the maximum clique

    Qmax = MaxClique(R, C, my_graph, Q, Qmax)

    print('final max clique')
    print(Qmax)
    print('final max clique size')
    print(len(Qmax))


    #nodes = [2,3]
    #test_graph = create_subgraph(my_graph, nodes)
    
    #C = ColorSort(R,C,test_graph)


# Run the main function
main()
