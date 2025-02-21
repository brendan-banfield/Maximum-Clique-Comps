from graphs import Graph
import time
import simulatedAnnealing
import branch_and_bound
import bronKerbosch
import genetic_alg



def run_DIMACS_tests(solvers: list, DIMACS_files: list):
    for DIMACS_file in DIMACS_files:
        run_DIMACS_test(solvers, DIMACS_file)

def run_DIMACS_test(solvers: list, DIMACS_file: str):
    
    graph = Graph.get_graph_from_dataset(DIMACS_file)
    print(f'Running tests on {DIMACS_file} with size {graph.vertices}...')
    k = 0
    results = []
    for (solver_class, num_trials, args, kwargs, is_exact) in solvers:
        # print(f'{solver_class.__name__}:')
        tot_time = 0
        successes = 0
        max_clique_found = 0
        for _ in range(num_trials):
            if solver_class.is_decision_problem:
                solver = solver_class(graph, k, *args, **kwargs)
            else:
                solver = solver_class(graph, *args, **kwargs)
            time1 = time.time()
            solver.run()
            time2 = time.time()
            tot_time += time2 - time1
            clique_found = solver.get_maximum_clique()
            
            if is_exact:
                k = clique_found
            if k == clique_found:
                successes += 1

            max_clique_found = max(max_clique_found, clique_found)
            # print(f'Algorithm {solver_class.__name__} took time: {time2 - time1}. Succeeded: {solver.succeeded}')
        results.append((solver_class.__name__, tot_time / num_trials, max_clique_found, successes / num_trials))
        # print(f'Algorithm {solver_class.__name__} took time: {time2 - time1}. Succeeded: {solver.succeeded}')

    
    print(f'Graph {DIMACS_file} has size {graph.vertices} and max clique {k}')
    for alg_name, time_taken, max_clique_found, success_rate in results:
        print(f"Algorithm {alg_name} took average time: {time_taken:.2} and found a best clique of size {max_clique_found}. Success rate: {success_rate:.0%}")
    

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
    DIMACS_files = [
        'c-fat200-1',
        'c-fat500-1',
        'johnson32-2-4',
        'keller4',
        'keller5',
        'keller6',
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
    for DIMACS_file in DIMACS_files:
        
        try:
            graph = Graph.get_graph_from_dataset(DIMACS_file)
        except:
            print(f'Failed to load graph from {DIMACS_file}')
            raise FileNotFoundError
    run_DIMACS_tests([bronKerboschClass, branch_and_boundClass, simulatedAnnealingClass, genetic_algClass], DIMACS_files)
    # test_increasing_graphs([bronKerboschClass, branch_and_boundClass, simulatedAnnealingClass, genetic_algClass], n_0, edge_probability)


