# Not Clique-bait: Algorithmic Approaches to the Maximum Clique Problem
Carleton College Winter Term Comps 2025
Authors: Brendan Banfield, Aaron Banse, Kellen Knop, Sophie Quinn

# Project Description:
We found and implemented four algorithms that solve the Maximum Clique problem. We compared their runtimes and gauged their performances on both dense and sparse graphs. To find out more, visit our website: 

# Table of Contents:
- algorithms
    - branch_and_bound.py
    - bronKerbosch.py
    - bruteForce.py
    - genetic_alg.py
    - simulatedAnnealing.py
- datasets
    - DIMACS
    - proteinProductGraphs
- graphs.py
- testing
    - DIMACSTests.py
    - increasingGraphOutputParser.py
    - increasingGraphTests.py



# graphs.py
To use graphs.py:
```
import graphs.py
your_graph = graphs.Graph(num_vertices, edges)
```
where edges is a list of tuples, e.g. graphs.Graph(3, [(1, 2), (0, 2), (1, 0)]) is a fully connected graph of order 3.
Use the functions your_graph.get_adj_list() and your_graph.get_adj_matrix() to populated the list/matrix (if needed) and return it.
Graphs can also be imported by name from the DIMACS data set, protein data set, or created randomly.
