import matplotlib.pyplot as plt


num_algs = 3
times = [[] for _ in range(num_algs)]
succeeded = [[] for _ in range(num_algs)]
sizes = []
clique_sizes = []
with open("increasingGraphsOutput.txt", "r") as f:
    lines = f.readlines()
    i = 0
    while i < len(lines):
        # line 1 format: 'Graph size: n, max clique k'
        graph_info = lines[i].split()
        graph_size = int(graph_info[2][:-1])
        clique_size = int(graph_info[5])
        sizes.append(graph_size)
        clique_sizes.append(clique_size)

        # line 2 format: 'Algorithm Bron_Kerbosch_Solver took time: 1.3113021850585938e-05. Succeeded: True'
        Bron_Kerbosh_info = lines[i + 1].split()
        Bron_Kerbosh_time = float(Bron_Kerbosh_info[4][:-1])
        Bron_Kerbosh_succeeded = True
        times[0].append(Bron_Kerbosh_time)
        succeeded[0].append(Bron_Kerbosh_succeeded)

        Branch_and_Bound_info = lines[i + 2].split()
        Branch_and_Bound_time = float(Branch_and_Bound_info[4][:-1])
        Branch_and_Bound_succeeded = True
        times[1].append(Branch_and_Bound_time)
        succeeded[1].append(Branch_and_Bound_succeeded)

        Simulated_Annealing_info = lines[i + 3].split()
        Simulated_Annealing_time = float(Simulated_Annealing_info[4][:-1])
        Simulated_Annealing_succeeded = Simulated_Annealing_info[-1] == "True"
        times[2].append(Simulated_Annealing_time)
        succeeded[2].append(Simulated_Annealing_succeeded)

        i += 5


# plt.plot(sizes, clique_sizes, label="Clique Size")
# plt.show()

cutoff = 80
plt.plot(sizes[:cutoff], times[0][:cutoff], label="Bron Kerbosch")
plt.plot(sizes[:cutoff], times[1][:cutoff], label="Branch and Bound")
plt.plot(sizes[:cutoff], times[2][:cutoff], label="Simulated Annealing")
plt.show()

plt.plot(sizes, succeeded[2], label="Simulated Annealing")
plt.show()