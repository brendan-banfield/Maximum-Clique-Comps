from graphs import Graph
import time
import simulatedAnnealing
import branch_and_bound
import bronKerbosch
import genetic_alg


import multiprocessing

# seconds_in_hour = 60 * 60
# max_time_allowed = 2 * seconds_in_hour
max_time_allowed = 600


def run_random_tests(solvers: list, random_files: list[str]):
    with open('randomGraphResults.csv', 'w') as results_file:
        fieldnames = ['graph_name', 'vertices', 'edges', 'edge_density', 'degree_variance', 'clustering_coefficient', 'k', 'bronKerbosch_time', 'bronKerbosch_max_found', 'bronKerbosch_success', 'branch_and_bound_time', 'branch_and_bound_max_found', 'branch_and_bound_success', 'simulated_annealing_time', 'simulated_annealing_max_found', 'simulated_annealing_success', 'genetic_alg_time', 'genetic_alg_max_found', 'genetic_alg_success']
        
        results_file.write(','.join(fieldnames) + '\n')
        for random_file in random_files:
            new_line = run_random_test(solvers, random_file)
            results_file.write(','.join([str(x) for x in new_line]) + '\n')

def run_random_test(solvers: list, random_file: str):
    
    graph = Graph.get_graph_from_dataset(random_file)

    # file format:
    # Vertices: 25
    # Edges: 265
    # Edge Density: 0.8833333333333333
    # Degree Variance: 3.4800000000000013
    # Clustering Coefficient: 0.6895652173913044
    # p edge 25
    with open(f'datasets/randomGraphs/{random_file}', 'r') as f:
        num_vertices = int(f.readline().split(': ')[1])
        num_edges = int(f.readline().split(': ')[1])
        edge_density = float(f.readline().split(': ')[1])
        degree_variance = float(f.readline().split(': ')[1])
        clustering_coefficient = float(f.readline().split(': ')[1])

        

    print(f'Running tests on {random_file} with size {graph.vertices}, {num_edges} edges, {edge_density} edge density, {degree_variance} degree variance, {clustering_coefficient} clustering coefficient...')
    k = 0
    results = []
    for (solver_class, num_trials, args, kwargs, is_exact) in solvers:
        # print(f'{solver_class.__name__}:')
        tot_time = 0
        cliques_found = []
        max_clique_found = 0
        for _ in range(num_trials):
            if solver_class.is_decision_problem:
                solver = solver_class(graph, k, *args, **kwargs)
            else:
                solver = solver_class(graph, *args, **kwargs)


            # for reasons I don't understand, this threading adds a ton of overhead
            # since approximation algorithms run quickly anyway, we don't need timeout protection on them
            # so we can skip the overhead by only threading the exact algorithms
            if is_exact:

                manager = multiprocessing.Manager()
                return_dict = manager.dict()
                thread = multiprocessing.Process(target=run_random_test_timeout, args=(solver, return_dict))
                thread.start()

                thread.join(max_time_allowed)
                if thread.is_alive():
                    thread.terminate()
                    thread.join()
                
                if 'completed' in return_dict:
                    clique_found = return_dict['clique_found']
                    time_taken = return_dict['time_taken']
                else:
                    # alg timed out
                    clique_found = 0
                    time_taken = max_time_allowed
            else:
                return_dict = {}
                run_random_test_timeout(solver, return_dict)
                clique_found = return_dict['clique_found']
                time_taken = return_dict['time_taken']

            tot_time += time_taken
            
            if is_exact or clique_found > k:
                k = clique_found
            cliques_found.append(clique_found)

            # print(f'Algorithm {solver_class.__name__} took time: {time2 - time1}. Succeeded: {solver.succeeded}')
        results.append((solver_class.__name__, tot_time / num_trials, cliques_found))
        # print(f'Algorithm {solver_class.__name__} took time: {time2 - time1}. Succeeded: {solver.succeeded}')

    formatted_results = []
    print(f'Graph {random_file} has size {graph.vertices} and max clique {k}')
    for alg_name, time_taken, cliques_found in results:
        max_clique_found = max(cliques_found)
        success_rate = cliques_found.count(k) / len(cliques_found)
        formatted_results.append(time_taken)
        formatted_results.append(max_clique_found)
        formatted_results.append(success_rate)
        print(f"Algorithm {alg_name} took average time: {time_taken:.2} and found a best clique of size {max_clique_found}. Success rate: {success_rate:.0%}")

    return [random_file, graph.vertices, num_edges, edge_density, degree_variance, clustering_coefficient, k] + formatted_results
    

def run_random_test_timeout(solver, return_dict):
    time1 = time.time()
    solver.run()
    time2 = time.time()
    clique_found = solver.get_maximum_clique()
    return_dict['clique_found'] = clique_found
    return_dict['time_taken'] = time2 - time1
    return_dict['completed'] = True
    return
    

if __name__ == '__main__':

    bronKerboschClass = [bronKerbosch.Pivot_Solver, 1, [], {}, True]

    branch_and_boundClass = [branch_and_bound.Branch_and_Bound_Solver, 1, [], {}, True]

    T_0 = 100
    T_f = 0.001
    alpha = 0.9998
    simulatedAnnealingClass = [simulatedAnnealing.Simulated_Annealing_Solver, 10, [T_0, T_f, alpha], {}, False]

    genetic_algClass = [genetic_alg.Genetic_Solver, 10, [], {}, False]
    n_0 = 120
    edge_probability = 0.99

    v_sizes = [25, 50, 100, 200, 400]
    num_graphs = 25
    random_files = []
    for v_size in v_sizes:
        for g_idx in range(num_graphs):
            random_files.append('v' + str(v_size) + '/' + str(g_idx))

    for random_file in random_files:
        try:
            graph = Graph.get_graph_from_dataset(random_file)
        except:
            print(f'Failed to load graph from {random_file}')
            # raise FileNotFoundError
    run_random_tests([bronKerboschClass, branch_and_boundClass, genetic_algClass, simulatedAnnealingClass], random_files)
    # test_increasing_graphs([bronKerboschClass, branch_and_boundClass, simulatedAnnealingClass, genetic_algClass], n_0, edge_probability)


