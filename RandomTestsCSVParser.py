import matplotlib.pyplot as plt


num_algs = 4
times = [[] for _ in range(num_algs)]
successes = [[] for _ in range(num_algs)]
best_found = [[] for _ in range(num_algs)]
names = []
sizes = []
clique_sizes = []

def read_line(line):
    # graph_name,vertices,edges,edge_density,degree_variance,clustering_coefficient,k,bronKerbosch_time,bronKerbosch_max_found,bronKerbosch_success,branch_and_bound_time,branch_and_bound_max_found,branch_and_bound_success,simulated_annealing_time,simulated_annealing_max_found,simulated_annealing_success,genetic_alg_time,genetic_alg_max_found,genetic_alg_success

    line = line.split(",")
    data_dict = {}
    data_dict["name"] = line[0]
    data_dict["size"] = int(line[1])
    data_dict["edges"] = int(line[2])
    data_dict["edge_density"] = float(line[3])
    data_dict["degree_variance"] = float(line[4])
    data_dict["clustering_coefficient"] = float(line[5])
    data_dict["clique_size"] = float(line[6])
    data_dict["bronKerbosch_time"] = float(line[7])
    data_dict["bronKerbosch_max_found"] = int(line[8])
    data_dict["bronKerbosch_success"] = float(line[9])
    data_dict["branch_and_bound_time"] = float(line[10])
    data_dict["branch_and_bound_max_found"] = int(line[11])
    data_dict["branch_and_bound_success"] = float(line[12])
    data_dict["genetic_alg_time"] = float(line[13])
    data_dict["genetic_alg_max_found"] = int(line[14])
    data_dict["genetic_alg_success"] = float(line[15])
    data_dict["simulated_annealing_time"] = float(line[16])
    data_dict["simulated_annealing_max_found"] = int(line[17])
    data_dict["simulated_annealing_success"] = float(line[18])
    return data_dict


with open("randomGraphResults7.csv", "r") as f:

    lines = f.readlines()

data = [read_line(line) for line in lines[1:]]
# data = [read_line(line) for line in lines[101:]]
xs = [d["size"] for d in data]
edges = [d["edges"] for d in data]
edge_densities = [d["edge_density"] for d in data]
bk_times = [d["bronKerbosch_time"] for d in data]
bb_times = [d["branch_and_bound_time"] for d in data]
sa_times = [d["simulated_annealing_time"] for d in data]
ga_times = [d["genetic_alg_time"] for d in data]
sa_success = [d["simulated_annealing_success"] for d in data]
ga_success = [d["genetic_alg_success"] for d in data]
bk_success = [d["bronKerbosch_success"] for d in data]
bb_success = [d["branch_and_bound_success"] for d in data]

start_idx = xs.index(60)
end_idx = xs.index(75)
dot_size = 50
plt.scatter(edge_densities[start_idx:end_idx], bk_times[start_idx:end_idx], label="Bron Kerbosch", sizes=[dot_size])
plt.scatter(edge_densities[start_idx:end_idx], bb_times[start_idx:end_idx], label="Branch and Bound", sizes=[dot_size])
plt.scatter(edge_densities[start_idx:end_idx], sa_times[start_idx:end_idx], label="Simulated Annealing", sizes=[dot_size])
plt.scatter(edge_densities[start_idx:end_idx], ga_times[start_idx:end_idx], label="Genetic Algorithm", sizes=[dot_size])
plt.legend()
ax = plt.gca()
ax.set_xlabel("Edge Density")
ax.set_ylabel("Time (s)")
plt.title("Algorithm runtimes for |V|=50")
plt.show()

start_idx = xs.index(100)
end_idx = xs.index(200)
plt.scatter(edge_densities[start_idx:end_idx], bk_times[start_idx:end_idx], label="Bron Kerbosch", sizes=[dot_size])
plt.scatter(edge_densities[start_idx:end_idx], bb_times[start_idx:end_idx], label="Branch and Bound", sizes=[dot_size])
plt.scatter(edge_densities[start_idx:end_idx], sa_times[start_idx:end_idx], label="Simulated Annealing", sizes=[dot_size])
plt.scatter(edge_densities[start_idx:end_idx], ga_times[start_idx:end_idx], label="Genetic Algorithm", sizes=[dot_size*0.2])
plt.legend()
ax = plt.gca()
plt.title("Algorithm runtimes for |V|=100")
ax.set_xlabel("Edge Density")
ax.set_ylabel("Time (s)")
plt.show()



plt.scatter(edge_densities[start_idx:end_idx], ga_success[start_idx:end_idx], label="gen alg", sizes=[dot_size])
plt.scatter(edge_densities[start_idx:end_idx], sa_success[start_idx:end_idx], label="sim ann", sizes=[dot_size*0.2])
# plt.scatter(edge_densities[start_idx:end_idx], bk_success[start_idx:end_idx], label="bk")
# plt.scatter(edge_densities[start_idx:end_idx], bb_success[start_idx:end_idx], label="bb")
plt.legend()
plt.show()

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

sim_ann_dict = {}
gen_alg_dict = {}
for i in range(len(sa_success)):
    if xs[i] in sim_ann_dict:
        sim_ann_dict[xs[i]].append(sa_success[i])
    else:
        sim_ann_dict[xs[i]] = [sa_success[i]]
    if xs[i] in gen_alg_dict:
        gen_alg_dict[xs[i]].append(ga_success[i])
    else:
        gen_alg_dict[xs[i]] = [ga_success[i]]
xs = sorted(list(sim_ann_dict.keys()))
sim_ann_ys = [sum(sim_ann_dict[x])/len(sim_ann_dict[x]) for x in xs]
gen_alg_ys = [sum(gen_alg_dict[x])/len(gen_alg_dict[x]) for x in xs]
plt.plot(xs, sim_ann_ys, label="Simulated Annealing")
plt.plot(xs, gen_alg_ys, label="Genetic Algorithm")
plt.legend()
plt.show()