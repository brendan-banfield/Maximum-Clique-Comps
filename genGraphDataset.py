'''
Generate Graph datasets for testing.
'''

from graphs import Graph
import random
import os

v_sizes = [25, 50, 100, 200, 400]
num_graphs = 100

rand_graph_path = 'datasets/randomGraphs/v'
if not os.path.isdir('datasets/randomGraphs'):
    os.mkdir('datasets/randomGraphs')
if not os.path.isdir(rand_graph_path):
    os.mkdir(rand_graph_path)

if __name__ == '__main__':
    for v_size in v_sizes:
        if not os.path.isdir(rand_graph_path + str(v_size)):
            os.mkdir(rand_graph_path + str(v_size))
        for g_idx in range(num_graphs):
            g = Graph.create_random_graph(v_size, random.random())

            
            edge_strs = [f"e {edge[0]} {edge[1]}\n" for edge in g.edges]
            with open(rand_graph_path + str(v_size) + '/' + str(g_idx), 'w') as file:
                file.write(f"Vertices: {g.vertices}\n")
                file.write(f"Edges: {len(g.edges)}\n")
                file.write(f"Edge Density: {g.edge_density()}\n")
                file.write(f"Degree Variance: {g.degree_variance()}\n")
                file.write(f"Clustering Coefficient: {g.clustering_coefficient()}\n")
                file.write(f"p edge {g.vertices}\n")
                file.writelines(edge_strs)

