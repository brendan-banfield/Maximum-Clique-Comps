from graphs import Graph
import os
import pandas as pd
import matplotlib.pyplot as plt
import time
from numpy import mean
import random

protein_file_names = os.listdir("datasets/proteinProductGraphs")

graph_list = [Graph.get_graph_from_dataset(file) for file in protein_file_names if file != "proteinGraphsInfo.txt"]

df = pd.read_csv("randomGraphResults3.csv")



#plt.scatter(df['vertices'], df['bronKerbosch_time'], label="Bron-kerbosch")
#plt.scatter(df['vertices'], df['branch_and_bound_time'], label="Branch and Bound")


plt.scatter(df['vertices'], df['genetic_alg_time'], label="Genetic Algorithm", c="green")
plt.legend(loc="upper left")
plt.xlabel("Number of Vertices")
plt.ylabel("Runtime (seconds)")

plt.show()

