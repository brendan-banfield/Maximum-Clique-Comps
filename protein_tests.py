from algorithms.lib.graphs import Graph

from algorithms import simulated_annealing
from algorithms import branch_and_bound
from algorithms import bron_kerbosch
from algorithms import genetic_alg

import time
import multiprocessing

seconds_in_hour = 60 * 60
max_time_allowed = 2 * seconds_in_hour


def run_protein_tests(solvers: list, protein_files: list):
    for protein_file in protein_files:
        run_protein_test(solvers, protein_file)

def run_protein_test(solvers: list, protein_file: str):
    
    graph = Graph.get_graph_from_dataset(protein_file)
    print(f'Running tests on {protein_file} with size {graph.vertices}...')
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
                thread = multiprocessing.Process(target=run_protein_test_timeout, args=(solver, return_dict))
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
                run_protein_test_timeout(solver, return_dict)
                clique_found = return_dict['clique_found']
                time_taken = return_dict['time_taken']

            tot_time += time_taken
            
            if is_exact or clique_found > k:
                k = clique_found
            cliques_found.append(clique_found)

            # print(f'Algorithm {solver_class.__name__} took time: {time2 - time1}. Succeeded: {solver.succeeded}')
        results.append((solver_class.__name__, tot_time / num_trials, cliques_found))
        # print(f'Algorithm {solver_class.__name__} took time: {time2 - time1}. Succeeded: {solver.succeeded}')

    
    print(f'Graph {protein_file} has size {graph.vertices} and max clique {k}')
    for alg_name, time_taken, cliques_found in results:
        max_clique_found = max(cliques_found)
        success_rate = cliques_found.count(k) / len(cliques_found)
        print(f"Algorithm {alg_name} took average time: {time_taken:.2} and found a best clique of size {max_clique_found}. Success rate: {success_rate:.0%}")
    

def run_protein_test_timeout(solver, return_dict):
    time1 = time.time()
    solver.run()
    time2 = time.time()
    clique_found = solver.get_maximum_clique()
    return_dict['clique_found'] = clique_found
    return_dict['time_taken'] = time2 - time1
    return_dict['completed'] = True
    return
    

if __name__ == '__main__':

    bronKerboschClass = [bron_kerbosch.Pivot_Solver, 1, [], {}, True]

    branch_and_boundClass = [branch_and_bound.Branch_and_Bound_Solver, 1, [], {}, True]

    T_0 = 100
    T_f = 0.001
    alpha = 0.9998
    simulatedAnnealingClass = [simulated_annealing.Simulated_Annealing_Solver, 10, [T_0, T_f, alpha], {}, False]

    genetic_algClass = [genetic_alg.Genetic_Solver, 10, [], {}, False]
    n_0 = 120
    edge_probability = 0.99
    protein_files = [
        '1allA_3dbjC_41',
        '1f82A_1zb7A_5',
        '1KZKA_3KT2A_78',
        '2FDVC_1PO5A_83',
        '2UV8I_2J6IA_13107',
        '2W00B_3H1TA_10858',
        '2W4JA_2A2AD_0',
        '3HRZA_2HR0A_476',
        '3P0KA_3GWLB_0',
        '3ZY0D_3ZY1A_110'
    ]

    for protein_file in protein_files:
        
        try:
            graph = Graph.get_graph_from_dataset(protein_file)
        except:
            print(f'Failed to load graph from {protein_file}')
            raise FileNotFoundError
    run_protein_tests([bronKerboschClass, branch_and_boundClass, genetic_algClass, simulatedAnnealingClass], protein_files)
    # test_increasing_graphs([bronKerboschClass, branch_and_boundClass, simulatedAnnealingClass, genetic_algClass], n_0, edge_probability)


