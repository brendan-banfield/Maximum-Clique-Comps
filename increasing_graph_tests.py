from algorithms.lib.graphs import Graph
import time

from algorithms import simulated_annealing
from algorithms import branch_and_bound
from algorithms import bron_kerbosch

def test_increasing_graphs(solvers: list, starting_size, edge_probability):
    # each element in solver_classes should be (algorithm_class, *args, **kwargs)
    n = starting_size
    while True:
        graph = Graph.create_random_graph(n, edge_probability)
        k = 0
        results = []
        for (solver_class, args, kwargs) in solvers:
            # print(f'{solver_class.__name__}:')
            if solver_class.is_decision_problem:
                solver = solver_class(graph, k, *args, **kwargs)
            else:
                solver = solver_class(graph, *args, **kwargs)
            time1 = time.time()
            solver.run()
            time2 = time.time()
            if not solver_class.is_decision_problem:
                k = solver.get_maximum_clique()
            results.append((solver_class.__name__, time2 - time1, solver.succeeded))
            # print(f'Algorithm {solver_class.__name__} took time: {time2 - time1}. Succeeded: {solver.succeeded}')

        
        print(f'Graph size: {n}, max clique {k}')
        for alg_name, time_taken, succeeded in results:
            print(f"Algorithm {alg_name} took time: {time_taken}. Succeeded: {succeeded}")
        n += 1
    

if __name__ == '__main__':

    bronKerboschClass = [bron_kerbosch.Bron_Kerbosch_Solver, [], {}]

    branch_and_boundClass = [branch_and_bound.Branch_and_Bound_Solver, [], {}]

    T_0 = 100
    T_f = 0.001
    alpha = 0.9998
    simulatedAnnealingClass = [simulated_annealing.Simulated_Annealing_Solver, [T_0, T_f, alpha], {}]
    n_0 = 5
    edge_probability = 0.99
    test_increasing_graphs([bronKerboschClass, branch_and_boundClass, simulatedAnnealingClass], n_0, edge_probability)


