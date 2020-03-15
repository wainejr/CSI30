import time

from genetic_algorithm import GeneticAlgorithmSolver
from beam_search import BeamSearchSolver

from constants import *
from utils import calculate_path_cost

class AlgorithmsTester:

    def __init__(self, optimal_solution, distance_matrix):
        self.optimal_solution = optimal_solution
        self.distance_matrix = distance_matrix

    def static_test_genetic_algorithm(self,
        number_of_simulations,
        n_genes=N_GENES,
        maximum_fitness_to_hold=MAXIMUM_FITNESS_TO_HOLD,
        number_of_genes_to_generate=NUMBER_OF_GENES_TO_GENERATE,
        max_iterations=MAX_ITERATIONS,
        probability_of_mutation=PROBABILITY_OF_MUTATION):
        """[summary]
        
        Keyword Arguments:
            number_of_simultations {[type]} -- [description]
            n_genes {[type]} -- [description] (default: {N_GENES})
            number_of_genes_to_generate {[type]} -- [description] (default: {NUMBER_OF_GENES_TO_GENERATE})
            max_iterations {[type]} -- [description] (default: {MAX_ITERATIONS})
            maximum_fitness_to_hold {[type]} -- [description] (default: {MAXIMUM_FITNESS_TO_HOLD})
            probability_of_mutation {[type]} -- [description] (default: {PROBABILITY_OF_MUTATION})
        """

        solver_ga = GeneticAlgorithmSolver(n_genes, maximum_fitness_to_hold, 
            max_iterations, number_of_genes_to_generate, probability_of_mutation)
        results = []
        for i in range(0, number_of_simulations):
            t0 = time.time()
            result, n_iterations = solver_ga.solve(self.distance_matrix)
            results.append(
                {"time": time.time()-t0, 
                "result": result, 
                "weight": calculate_path_cost(result, self.distance_matrix),
                "n_iterations": n_iterations,
                "params": solver_ga.get_parameters()})

        return results