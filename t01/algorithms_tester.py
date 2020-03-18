import time
import json
import numpy as np

from genetic_algorithm import GeneticAlgorithmSolver
from beam_search import BeamSearchSolver
from plotter import Plotter

from constants import *
from utils import calculate_path_cost


class AlgorithmsTester:

    def __init__(self, optimal_solution, distance_matrix):
        self.start_time = time.gmtime()
        self.optimal_solution = optimal_solution
        self.distance_matrix = distance_matrix
        self.plotter = Plotter()

    def static_test_genetic_algorithm(self,
        number_of_simulations,
        n_genes=N_GENES,
        maximum_fitness_to_hold=MAXIMUM_FITNESS_TO_HOLD,
        ratio_of_genes_to_generate=RATIO_OF_GENES_TO_GENERATE,
        max_iterations=MAX_ITERATIONS,
        probability_of_mutation=PROBABILITY_OF_MUTATION):
        """
        Implement Waine

        Keyword Arguments:
            number_of_simultations {[type]} -- [description]
            n_genes {[type]} -- [description] (default: {N_GENES})
            ratio_of_genes_to_generate {[type]} -- [description] (default: {RATIO_OF_GENES_TO_GENERATE})
            max_iterations {[type]} -- [description] (default: {MAX_ITERATIONS})
            maximum_fitness_to_hold {[type]} -- [description] (default: {MAXIMUM_FITNESS_TO_HOLD})
            probability_of_mutation {[type]} -- [description] (default: {PROBABILITY_OF_MUTATION})
        """

        solver_ga = GeneticAlgorithmSolver(n_genes, maximum_fitness_to_hold, 
            max_iterations, ratio_of_genes_to_generate, probability_of_mutation)
        results = []
        for i in range(0, number_of_simulations):
            t0 = time.time()
            result, n_iterations, fitnesses = solver_ga.solve(self.distance_matrix)
            results.append(
                {"time": float(time.time()-t0),
                "result": list(result), 
                "weight": int(calculate_path_cost(result, self.distance_matrix)),
                "n_iterations": int(n_iterations),
                "params": solver_ga.get_parameters(),
                'fitnesses': fitnesses})

        return results

    def static_test_beam_search(self,
        number_of_simulations,
        k_states=K_STATES):
        """
        Implement Waine

        Arguments:
            number_of_simulations {[type]} -- [description]
        
        Keyword Arguments:
            k_states {[type]} -- [description] (default: {K_STATES})
        
        Returns:
            [type] -- [description]
        """
        solver_bs = BeamSearchSolver(k_states)
        results = []
        for i in range(0, number_of_simulations):
            t0 = time.time()
            result = solver_bs.solve(self.distance_matrix)
            results.append(
                {"time": float(time.time()-t0),
                "result": list(result),
                "weight": int(calculate_path_cost(result, self.distance_matrix)),
                "params": solver_bs.get_parameters()})
        return results

    def test_beam_search(self, number_of_simulations, range_k_states=[K_STATES]):
        """Test the beam search given the specified parameters
        Implement Waine

        Keyword Arguments:
            range_k_states {list} -- [description] (default: {[K_STATES]})
        
        Returns:
            [type] -- [description]
        """
        results = []
        for k in range_k_states:
            results.append(self.static_test_beam_search(number_of_simulations, k))

        return results

    def test_genetic_algorithm(self,
        number_of_simulations_for_each_configuration,
        n_genes=[N_GENES],
        maximum_fitness_to_hold=[MAXIMUM_FITNESS_TO_HOLD],
        ratio_of_genes_to_generate=[RATIO_OF_GENES_TO_GENERATE],
        max_iterations=[MAX_ITERATIONS],
        probability_of_mutation=[PROBABILITY_OF_MUTATION]):
        """Test the genetic algorithm given the specified parameters
        Implement Waine

        Arguments:
            number_of_simulations_for_each_configuration {[type]} -- [description]
        
        Keyword Arguments:
            n_genes {list} -- [description] (default: {[N_GENES]})
            maximum_fitness_to_hold {list} -- [description] (default: {[MAXIMUM_FITNESS_TO_HOLD]})
            ratio_of_genes_to_generate {list} -- [description] (default: {[RATIO_OF_GENES_TO_GENERATE]})
            max_iterations {list} -- [description] (default: {[MAX_ITERATIONS]})
            probability_of_mutation {list} -- [description] (default: {[PROBABILITY_OF_MUTATION]})
        
        Returns:
            [type] -- [description]
        """
        results = []
        for n_gen in n_genes:
            for max_fit in maximum_fitness_to_hold:
                for r_gen_generate in ratio_of_genes_to_generate:
                    for max_it in max_iterations:
                        for prob_of_mutation in probability_of_mutation:
                            results.append(self.static_test_genetic_algorithm(
                                number_of_simulations_for_each_configuration,
                                n_gen, max_fit, r_gen_generate, max_it,
                                prob_of_mutation
                            ))
        return results

    def test_ga_fitness_over_max_iterations(self):
        """average weight for each iteration until the solution is found
        Implement Ian
        """
        results = self.test_genetic_algorithm(10, maximum_fitness_to_hold=[150], max_iterations=[150])[0]
        new_results = []
        for i in range(len(results[0]['fitnesses'])):
            res = [{'weight': result['fitnesses'][i]} for result in results]
            new_results.append(res)
        iterations = [i + 1 for i in range(150)]
        weights = [self.average_weight(result) for result in new_results]
        self.plotter.plot_line(iterations, weights)
        self.plotter.save_plots('Iteração', 'Distãncia', 'fit_over_ite', 'Distância da solução X Iteração')
        # self.plotter.flush()
        

    def test_ga_fitness_over_n_genes(self):
        """average weight over number of genes in the population
        Implement Waine
        """
        n_genes = [5, 10, 25, 50, 100, 150, 250]
        results = self.test_genetic_algorithm(10, n_genes=n_genes)
        # self.save_dicts_as_json(results, "fitness_over_n_genes")
        fitness = [self.average_weight(result) for result in results]
        self.plotter.plot_line(n_genes, fitness)
        self.plotter.save_plots('População', 'Distância', 'fit_over_ngenes', 'Distância da solução x tamanho da população')
        # points = np.array([[r["params"]["n_genes"], r["weight"]] for r in results])
        # self.plotter.plot_points(points[:, 0], points[:, 1])
        # self.plotter.save_plots('Tamanho da população', 'Fitness', 'fit_over_n_genes_points', 'Fitness x Tamanho da população')

    def test_ga_fitness_over_ratio_of_genes_to_generate(self):
        """average weight over the quantity of new genes generated in each iteration
        Implement Waine
        """
        ratio_of_genes_to_generate = [0.5, 1, 2.5, 5, 7.5, 10]
        results = self.test_genetic_algorithm(10, 
            ratio_of_genes_to_generate=ratio_of_genes_to_generate)
        # self.save_dicts_as_json(results, "fitness_over_ratio_of_genes")
        fitness = [self.average_weight(result) for result in results]
        self.plotter.plot_line(ratio_of_genes_to_generate, fitness)
        self.plotter.save_plots('Razão', 'Distância', 'fit_over_ratio', 'Distância da solução x razão de indivíduos gerados')
        # points = np.array([[float(r["params"]["ratio_of_genes_to_generate"]), r['weight']]
        #     for r in results])
        # self.plotter.plot_points(points[:, 0], points[:, 1])
        # self.plotter.save_plots('Razão', 'Distância', 'fit_over_weight', 'Distância da solução x razão de indivíduos gerados')
        #self.plotter.flush()

    def test_lb_fitness_over_kept_states(self):
        """average weight of simulations over the number of generated and kept states in each iteration
        Implement Ian
        """
        kept_states = list(range(16))[1:]
        results = self.test_beam_search(100, range_k_states=kept_states)
        weights = [self.average_weight(result) for result in results]
        self.plotter.plot_line(kept_states, weights)
        self.plotter.save_plots('Estados em memória', 'Distância', 'fit_over_mem', 'Distância da solução x Estados em memória')

    def test_averages(self):
        """Test average time and weight of each algorithm
        Implement Waine
        """
        res_bs = self.test_beam_search(100)[0]
        res_ga = self.test_genetic_algorithm(100)[0]

        # Beam Search
        bs_avg_time = sum([result["time"] for result in res_bs]) / len(res_bs)
        bs_avg_fitness = sum([result["weight"] for result in res_bs]) / len(res_bs)
        bs_best_fitness = self.select_best_result(res_bs)['weight']
        print('avg time of beam search: {}'.format(bs_avg_time))
        print('avg fitness of beam search: {}'.format(bs_avg_fitness))
        print('best fitness of beam search: {}'.format(bs_best_fitness))

        # Genetic Algorithm
        ga_avg_time = sum([result["time"] for result in res_ga]) / len(res_ga)
        ga_avg_fitness = sum([result["weight"] for result in res_ga]) / len(res_ga)
        ga_best_fitness = self.select_best_result(res_ga)['weight']
        print('avg time of genetic algorithm: {}'.format(ga_avg_time))
        print('avg fitness of genetic algorithm: {}'.format(ga_avg_fitness))
        print('best fitness of genetic algorithm: {}'.format(ga_best_fitness))

    def average_weight(self, results):
        return sum([result['weight'] for result in results]) / len(results)

    def select_best_result(self, results, field='weight', compare='lt'):
        """
        Implement Ian
        """
        best = 0
        for index, result in enumerate(results[1:]):
            if compare == 'lt':
                if results[best][field] > result[field]:
                    best = index
            elif compare == 'gt':
                if results[best][field] < result[field]:
                    best = index
        return results[best]

    def save_dicts_as_json(self, list_of_dicts, dict_name):
        """Save the passed dictionaries as a json file
        Implement Waine

        Arguments:
            list_of_dicts {[type]} -- [description]
        """
        filename = "tmp/" + time.strftime("%Y-%m-%d %H:%M:%S",
            self.start_time)+ dict_name + ".json"

        print("Saving", dict_name)

        with open(filename, 'w') as f:
            f.write(json.dumps(list_of_dicts))
    
    def perform_tests(self, 
        avg_simulation=True, 
        ga_fitness_over_max_iterations=True,
        ga_fitness_over_n_genes=True,
        ga_fitness_over_ratio_of_genes_to_generate=True,
        lb_fitness_over_kept_states=True):
        """Peform a battery of tests on each algorithm
        
        Keyword Arguments:
            avg_simulation_time {bool} -- [description] (default: {True})
            ga_fitness_over_max_iterations {bool} -- [description] (default: {True})
            ga_fitness_over_n_genes {bool} -- [description] (default: {True})
            ga_fitness_over_ratio_of_genes_to_generate {bool} -- [description] (default: {True})
            lb_fitness_over_kept_states {bool} -- [description] (default: {True})
        """

        if(avg_simulation):
            print("Started avg_simulation_time")
            self.test_averages()
            print("Finished avg_simulation_time")

        if(ga_fitness_over_max_iterations):
            print("Started ga_fitness_over_max_iterations")
            self.test_ga_fitness_over_max_iterations()
            print("Finished ga_fitness_over_max_iterations")
            
        if(ga_fitness_over_n_genes):
            print("Started ga_fitness_over_n_genes")
            self.test_ga_fitness_over_n_genes()
            print("Finished ga_fitness_over_n_genes")

        if(ga_fitness_over_ratio_of_genes_to_generate):
            print("Started ga_fitness_over_ratio_of_genes_to_generate")
            self.test_ga_fitness_over_ratio_of_genes_to_generate()
            print("Finished ga_fitness_over_ratio_of_genes_to_generate")

        if(lb_fitness_over_kept_states):
            print("Started lb_fitness_over_kept_states")
            self.test_lb_fitness_over_kept_states()
            print("Finished lb_fitness_over_kept_states")
