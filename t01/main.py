import numpy as np

from beam_search import BeamSearchSolver
from genetic_algorithm import GeneticAlgorithmSolver
from utils import calculate_path_cost
from algorithms_tester import AlgorithmsTester

import pprint

pp = pprint.PrettyPrinter()

if(__name__=="__main__"):
    distance_matrix = np.array( # optimal solution is probably 291 for this distance matrix
        [0,29,82,46,68,52,72,42,51,55,29,74,23,72,46,
        29,0,55,46,42,43,43,23,23,31,41,51,11,52,21,
        82,55,0,68,46,55,23,43,41,29,79,21,64,31,51,
        46,46,68,0,82,15,72,31,62,42,21,51,51,43,64,
        68,42,46,82,0,74,23,52,21,46,82,58,46,65,23,
        52,43,55,15,74,0,61,23,55,31,33,37,51,29,59,
        72,43,23,72,23,61,0,42,23,31,77,37,51,46,33,
        42,23,43,31,52,23,42,0,33,15,37,33,33,31,37,
        51,23,41,62,21,55,23,33,0,29,62,46,29,51,11,
        55,31,29,42,46,31,31,15,29,0,51,21,41,23,37,
        29,41,79,21,82,33,77,37,62,51,0,65,42,59,61,
        74,51,21,51,58,37,37,33,46,21,65,0,61,11,55,
        23,11,64,51,46,51,51,33,29,41,42,61,0,62,23,
        72,52,31,43,65,29,46,31,51,23,59,11,62,0,59,
        46,21,51,64,23,59,33,37,11,37,61,55,23,59,0]).reshape((15, 15))

    '''
    solver_ga = GeneticAlgorithmSolver()
    solver_bs = BeamSearchSolver()

    res_ga, n_iterations_ga = solver_ga.solve(distance_matrix)
    res_bs = solver_bs.solve(distance_matrix)
    print('solution of ga=', res_ga,
          'weight of ga=', calculate_path_cost(res_ga, distance_matrix))
    print('solution of bs=', res_bs,
          'weight of bs=', calculate_path_cost(res_bs, distance_matrix))
    '''

    alg_tester = AlgorithmsTester(291, distance_matrix)
    alg_tester.perform_tests(
        avg_simulation_time=False,
        ga_fitness_over_max_iterations=False,
        ga_fitness_over_n_genes=False,
        ga_fitness_over_ratio_of_genes_to_generate=False,
        lb_fitness_over_kept_states=True)
    