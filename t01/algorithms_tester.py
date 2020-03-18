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
        """[summary]
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
        """[summary]
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
        """[summary]
        Implement Waine

        Keyword Arguments:
            range_k_states {list} -- [description] (default: {[K_STATES]})
        
        Returns:
            [type] -- [description]
        """
        results = []
        for k in range_k_states:
            results.extend(self.static_test_beam_search(number_of_simulations, k))

        return results

    def test_genetic_algorithm(self,
        number_of_simulations_for_each_configuration,
        n_genes=[N_GENES],
        maximum_fitness_to_hold=[MAXIMUM_FITNESS_TO_HOLD],
        ratio_of_genes_to_generate=[RATIO_OF_GENES_TO_GENERATE],
        max_iterations=[MAX_ITERATIONS],
        probability_of_mutation=[PROBABILITY_OF_MUTATION]):
        """[summary]
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
                            results.extend(self.static_test_genetic_algorithm(
                                number_of_simulations_for_each_configuration,
                                n_gen, max_fit, r_gen_generate, max_it,
                                prob_of_mutation
                            ))
        return results

    def test_ga_fitness_over_max_iterations(self):
        """[summary]
        Implement Ian
        """
        results = self.test_genetic_algorithm(10, maximum_fitness_to_hold=[150], max_iterations=[150])[0]
        result = self.select_best_result(results)
        iterations = [i + 1 for i in range(len(result['fitnesses']))]
        self.plotter.plot_line(iterations, result['fitnesses'])
        self.plotter.save_plots('Iteração', 'Fitness', 'fit_over_ite', 'Fitness X Iteração')
        # self.plotter.flush()
        

    def test_ga_fitness_over_n_genes(self):
        """[summary]
        Implement Waine
        """
        n_genes = [5, 10, 25, 50, 100, 150, 250]
        results = self.test_genetic_algorithm(5, n_genes=n_genes)
        # self.save_dicts_as_json(results, "fitness_over_n_genes")
        # fitness = [self.select_best_result(result)['weight'] for result in results]
        # self.plotter.plot_line(n_genes, fitness)
        points = np.array([[r["params"]["n_genes"], r["weight"]] for r in results])
        self.plotter.plot_points(points[:, 0], points[:, 1])
        self.plotter.save_plots('Tamanho da população', 'Fitness', 'fit_over_n_genes_points', 'Fitness x Tamanho da população')

    def test_ga_fitness_over_ratio_of_genes_to_generate(self):
        """[summary]
        Implement Waine
        """
        ratio_of_genes_to_generate = [0.5, 1, 2.5, 5, 7.5, 10]
        results = self.test_genetic_algorithm(5, 
            ratio_of_genes_to_generate=ratio_of_genes_to_generate)
        # self.save_dicts_as_json(results, "fitness_over_ratio_of_genes")
        #fitness = [self.select_best_result(result)['weight'] for result in results]
        #self.plotter.plot_line(ratio_of_genes_to_generate, fitness)
        #self.plotter.save_plots('Ratio', 'Fitness', 'fit_over_rat', 'Fitness x Ratio')
        #self.plotter.flush()
        points = np.array([[float(r["params"]["ratio_of_genes_to_generate"]), r['weight']]
            for r in results])
        self.plotter.plot_points(points[:, 0], points[:, 1])
        self.plotter.save_plots('Ratio', 'Weight', 'fit_over_weight', 'Weight x Ratio')
        #self.plotter.flush()

    def test_lb_fitness_over_kept_states(self):
        """[summary]
        Implement Ian
        """
        kept_states = list(range(16))[1:]
        print('kept', kept_states)
        results = self.test_beam_search(50, range_k_states=kept_states)
        #results = [self.select_best_result(result) for result in results]
        #fitness = [result['weight'] for result in results]
        #self.plotter.plot_line(kept_states, fitness)
        #self.plotter.save_plots('Estados em memória', 'Fitness', 'fit_over_mem', 'Fitness x Estados em memória')
        #self.plotter.flush()
        points= np.array([[r["params"]["k_states"], r["weight"]] for r in results])
        self.plotter.plot_points(points[:,0], points[:,1])
        self.plotter.save_plots('Estados em memória', 'Fitness', 'fit_over_mem_points', 'Fitness x Estados em memória')

    def test_avg_simulation_time(self):
        """[summary]
        Implement Waine
        """
        res_bs = self.test_beam_search(100)[0]
        print('res', res_bs)
        res_ga = self.test_genetic_algorithm(100)[0]
        avg_bs = sum([result["time"] for result in res_bs]) / len(res_bs)
        print('avg time of beam search: {}'.format(avg_bs))
        # self.save_dicts_as_json(res_bs, "avg_time_bs")
        # self.save_dicts_as_json(res_ga, "avg_time_ga")
        # continue to plot...

    def select_best_result(self, results, field='weight', compare='lt'):
        """[summary]
        Implement Ian
        """
        best = 0
        for index, result in enumerate(results[1:]):
            if compare == 'lt':
                if results[best][field] < result[field]:
                    best = index
            elif compare == 'gt':
                if results[best][field] > result[field]:
                    best = index
        return results[best]

    def save_dicts_as_json(self, list_of_dicts, dict_name):
        """[summary]
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
        avg_simulation_time=True, 
        ga_fitness_over_max_iterations=True,
        ga_fitness_over_n_genes=True,
        ga_fitness_over_ratio_of_genes_to_generate=True,
        lb_fitness_over_kept_states=True):
        """[summary]
        
        Keyword Arguments:
            avg_simulation_time {bool} -- [description] (default: {True})
            ga_fitness_over_max_iterations {bool} -- [description] (default: {True})
            ga_fitness_over_n_genes {bool} -- [description] (default: {True})
            ga_fitness_over_ratio_of_genes_to_generate {bool} -- [description] (default: {True})
            lb_fitness_over_kept_states {bool} -- [description] (default: {True})
        """

        if(avg_simulation_time):
            print("Started avg_simulation_time")
            self.test_avg_simulation_time()
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
