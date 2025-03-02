from graphs import Graph
import time
import simulatedAnnealing
import branch_and_bound
import bronKerbosch
import genetic_alg


import multiprocessing

seconds_in_hour = 60 * 60
max_time_allowed = 2 * seconds_in_hour


def run_DIMACS_tests(solvers: list, DIMACS_files: list):
    for DIMACS_file in DIMACS_files:
        run_DIMACS_test(solvers, DIMACS_file)

def run_DIMACS_test(solvers: list, DIMACS_file: str):
    
    graph = Graph.get_graph_from_dataset(DIMACS_file)
    print(f'Running tests on {DIMACS_file} with size {graph.vertices}...')
    k = max_cliques[DIMACS_file]
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
                thread = multiprocessing.Process(target=run_DIMACS_test_timeout, args=(solver, return_dict))
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
                run_DIMACS_test_timeout(solver, return_dict)
                clique_found = return_dict['clique_found']
                time_taken = return_dict['time_taken']

            tot_time += time_taken
            
            cliques_found.append(clique_found)

            # print(f'Algorithm {solver_class.__name__} took time: {time2 - time1}. Succeeded: {solver.succeeded}')
        results.append((solver_class.__name__, tot_time / num_trials, cliques_found))
        # print(f'Algorithm {solver_class.__name__} took time: {time2 - time1}. Succeeded: {solver.succeeded}')

    
    print(f'Graph {DIMACS_file} has size {graph.vertices} and max clique {k}')
    for alg_name, time_taken, cliques_found in results:
        max_clique_found = max(cliques_found)
        success_rate = cliques_found.count(k) / len(cliques_found)
        print(f"Algorithm {alg_name} took average time: {time_taken:.2} and found a best clique of size {max_clique_found}. Success rate: {success_rate:.0%}")
    

def run_DIMACS_test_timeout(solver, return_dict):
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
    max_cliques = {
        'c-fat200-1': 12,
        'c-fat500-1': 14,
        'johnson16-2-4': 8,
        'johnson32-2-4': 16,
        'keller4': 11,
        'keller5': 27,
        'keller6': 59,
        'hamming10-2': 512,
        'hamming8-2': 128,
        'san200_0.7_1': 30,
        'san400_0.5_1': 13,
        'san400_0.9_1': 100,
        'sanr200_0.7': 18,
        'sanr400_0.5': 13,
        'san1000': 15,
        'brock200_1': 21,
        'brock400_1': 27,
        'brock800_1': 23,
        'p_hat300-1': 8,
        'p_hat500-1': 9,
        'p_hat700-1': 11,
        'p_hat1000-1': 10,
        'p_hat1500-1': 12,
        'MANN_a27': 126,
        'MANN_a45': 345
    }
    files = [
        'c-fat200-1',
        'c-fat500-1',
        'johnson16-2-4',
        'johnson32-2-4',
        'keller4',
        'keller5',
        'keller6',
        'hamming10-2',
        'hamming8-2',
        'san200_0.7_1',
        'san400_0.5_1',
        'san400_0.9_1',
        'sanr200_0.7',
        'sanr400_0.5',  
        'san1000',
        'brock200_1',
        'brock400_1',
        'brock800_1',
        'p_hat300-1',
        'p_hat500-1',
        'p_hat700-1',
        'p_hat1000-1',
        'p_hat1500-1',
        'MANN_a27',
        'MANN_a45'

    ]
    for DIMACS_file in files:
        
        try:
            graph = Graph.get_graph_from_dataset(DIMACS_file)
        except:
            print(f'Failed to load graph from {DIMACS_file}')
            raise FileNotFoundError
        try:
            max_clique_size = max_cliques[DIMACS_file]
        except:
            print(f"dict key {DIMACS_file} missing")
            raise KeyError
    run_DIMACS_tests([simulatedAnnealingClass], files)
    # run_DIMACS_tests([bronKerboschClass, branch_and_boundClass, genetic_algClass, simulatedAnnealingClass], files)
    # test_increasing_graphs([bronKerboschClass, branch_and_boundClass, simulatedAnnealingClass, genetic_algClass], n_0, edge_probability)


