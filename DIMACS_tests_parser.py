import matplotlib.pyplot as plt


num_algs = 4
times = [[] for _ in range(num_algs)]
successes = [[] for _ in range(num_algs)]
best_found = [[] for _ in range(num_algs)]
names = []
sizes = []
clique_sizes = []
with open("outputs/DIMACSTests.txt", "r") as f:
    # format of lines for each test:
    # 'Running tests on {DIMACS_file} with size {graph.vertices}...'
    # 'Graph {DIMACS_file} has size {graph.vertices} and max clique {k}'
    # "Algorithm {alg_name} took average time: {time_taken:.2} and found a best clique of size {max_clique_found}. Success rate: {success_rate:.0%}"
    # ^ 3x more

    lines = f.readlines()
    i = 0
    while i < len(lines):
        # line 2
        graph_info = lines[i+1].split()
        graph_name = graph_info[1]
        graph_size = int(graph_info[4])
        clique_size = int(graph_info[8])
        names.append(graph_name)
        sizes.append(graph_size)
        clique_sizes.append(clique_size)

        # line 3
        Bron_Kerbosh_info = lines[i + 2].split()
        Bron_Kerbosh_time = float(Bron_Kerbosh_info[5])
        Bron_Kerbosh_success = 100
        times[0].append(Bron_Kerbosh_time)
        successes[0].append(Bron_Kerbosh_success)

        # line 4
        Branch_and_Bound_info = lines[i + 3].split()
        Branch_and_Bound_time = float(Branch_and_Bound_info[5])
        Branch_and_Bound_success = 100
        times[1].append(Branch_and_Bound_time)
        successes[1].append(Branch_and_Bound_success)

        Genetic_Alg_info = lines[i + 5].split()
        Genetic_Alg_time = float(Genetic_Alg_info[5])
        Genetic_Alg_best_found = int(Genetic_Alg_info[13][:-1])
        Genetic_Alg_succeeded = int(Genetic_Alg_info[16][:-1])
        times[2].append(Genetic_Alg_time)
        successes[2].append(Genetic_Alg_succeeded)
        best_found[2].append(Genetic_Alg_best_found)

        Simulated_Annealing_info = lines[i + 4].split()
        Simulated_Annealing_time = float(Simulated_Annealing_info[5])
        Simulated_Annealing_best_found = int(Simulated_Annealing_info[13][:-1])
        Simulated_Annealing_succeeded = int(Simulated_Annealing_info[16][:-1])
        times[3].append(Simulated_Annealing_time)
        successes[3].append(Simulated_Annealing_succeeded)
        best_found[3].append(Simulated_Annealing_best_found)


        i += 6


# plt.plot(sizes, clique_sizes, label="Clique Size")
# plt.show()

cutoff = len(sizes)
plt.scatter(sizes[:cutoff], times[0][:cutoff], label="Bron Kerbosch")
plt.scatter(sizes[:cutoff], times[1][:cutoff], label="Branch and Bound")
# plt.scatter(sizes[:cutoff], times[2][:cutoff], label="Simulated Annealing")
# plt.scatter(sizes[:cutoff], times[3][:cutoff], label="Genetic Algorithm")
plt.legend()
ax = plt.gca()
# ax.set_ylim([0, 50])
# ax.set_xlim([0, 1000])
plt.show()

plt.scatter(sizes, successes[2], label="Simulated Annealing")
plt.scatter(sizes, successes[3], label="Genetic Algorithm")
plt.legend()
plt.show()