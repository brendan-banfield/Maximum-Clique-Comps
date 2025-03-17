# Not Clique-bait: Algorithmic Approaches to the Maximum Clique Problem
Carleton College Computer Science Comps 2025
Authors: Brendan Banfield, Aaron Banse, Kellen Knop, Sophie Quinn

# Project Description:
We found and implemented four algorithms that solve the Maximum Clique problem. We compared their runtimes and gauged their performances on different types of graphs. To find out more, visit our website on the [CS Comps Archive](https://www.cs.carleton.edu/cs_comps/) 

# Table of Contents:
- algorithms
    - lib
        - graphs.py
    - branch_and_bound.py
    - bronKerbosch.py
    - bruteForce.py
    - genetic_alg.py
    - simulatedAnnealing.py
- datasets
    - DIMACS

test files:
- DIMACS_tests.py
- experiments.py
- gen_graph_dataset.py (generate random graphs for random_tests)
- increasing_graph_tests.py
- protein_tests.py
- random_tests.py

data parsing files:
- DIMACS_tests_parser.py
- increasing_graph_output_parser.py
- random_tests_parser.py
- random_tests_parser.py


# Where we got our data
- [DIMACS](https://iridia.ulb.ac.be/~fmascia/maximum_clique/DIMACS-benchmark) benchmark datasets from 1992-93
- [protein product graphs](https://e6.ijs.si/~matjaz/maxclique/ProteinProduct/) based on [this paper](https://pubs.acs.org/doi/10.1021/ci4002525) from Depolli et al. (2013)
- generated our own graphs with randomly populated edges based on a given edge density


# graphs.py
To use graphs.py:
```
import libs.graphs
your_graph = graphs.Graph(num_vertices, edges)
```
where edges is a list of tuples, e.g. graphs.Graph(3, [(1, 2), (0, 2), (1, 0)]) is a fully connected graph of order 3.
Use the functions your_graph.get_adj_list() and your_graph.get_adj_matrix() to populate and return the list/matrix (if needed).
Graphs can also be imported by name from the DIMACS data set, protein data set, or created randomly.
