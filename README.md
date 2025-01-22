# Maximum-Clique-Comps

# graphs.py
To use graphs.py:
```
import graphs.py
your_graph = graphs.Graph(num_vertices, edges)
```
where edges is a list of tuples, e.g. graphs.Graph(3, [(1, 2), (0, 2), (1, 0)] is a fully connected graph of order 3.
Use the functions your_graph.get_adj_list() and your_graph.get_adj_matrix() to populated the list/matrix (if needed) and return it.
Graphs can also be imported by name from the DIMACS data set, or created randomly.
