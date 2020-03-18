import random
import time

from constants import N_GENES, \
    MAXIMUM_FITNESS_TO_HOLD, \
    RATIO_OF_GENES_TO_GENERATE, \
    MAX_ITERATIONS, \
    PROBABILITY_OF_MUTATION
from utils import calculate_path_cost, select_best_paths


class GeneticAlgorithmSolver:

    def __init__(self, n_genes=N_GENES, 
                 maximum_fitness_to_hold=MAXIMUM_FITNESS_TO_HOLD, 
                 max_iterations=MAX_ITERATIONS,
                 ratio_of_genes_to_generate=RATIO_OF_GENES_TO_GENERATE,
                 probability_of_mutation=PROBABILITY_OF_MUTATION):

        self.past_fitness = []
        self.iteration = 0

        self.n_genes = n_genes
        self.maximum_fitness_to_hold = maximum_fitness_to_hold
        self.max_iterations = max_iterations
        self.ratio_of_genes_to_generate = ratio_of_genes_to_generate
        self.probability_of_mutation = probability_of_mutation

    def get_parameters(self):
        return {
            "n_genes": int(self.n_genes),
            "maximum_fitness_to_hold": int(self.maximum_fitness_to_hold),
            "max_iterations": int(self.max_iterations),
            "ratio_of_genes_to_generate": float(self.ratio_of_genes_to_generate),
            "probability_of_mutation": int(self.probability_of_mutation),
        }

    def set_n_genes(self, n_genes):
        self.n_genes = n_genes
    
    def set_maximum_fitness_to_hold(self, maximum_fitness_to_hold):
        self.maximum_fitness_to_hold = maximum_fitness_to_hold
    
    def set_max_iterations(self, max_iterations):
        self.max_iterations = max_iterations
    
    def set_ratio_of_genes_to_generate(self, ratio_of_genes_to_generate):
        self.ratio_of_genes_to_generate = ratio_of_genes_to_generate

    def set_probability_of_mutation(self, probability_of_mutation):
        self.probability_of_mutation = probability_of_mutation

    def solve(self, matrix, stop_only_max_iteration=False):
        self.past_fitness = []
        self.iteration = 0

        self.distance_matrix = matrix
        genes = self.generate_n_initial_genes()
        it = 0

        condition_stop = lambda self, it: \
            self.stop_condtion() or it >= self.max_iterations

        if(stop_only_max_iteration):
            condition_stop = lambda self, it: it >= self.max_iterations

        while not condition_stop(self, it):
            genes = self.generate_new_genes(genes)
            # print('genes generated=', genes)
            genes = self.select_best_genes(genes)
            # print('best genes=', genes)
            self.past_fitness.append(calculate_path_cost(genes[0], self.distance_matrix))
            if len(self.past_fitness) > self.maximum_fitness_to_hold:
                self.past_fitness.pop(0)
            # print('past fitness=', self.past_fitness)cc
            it += 1
        return genes[0]+[genes[0][0]], it, self.past_fitness

    def generate_n_initial_genes(self):
        """Generate N random genes for initialization
        Implement Waine
        """
        permutation = list(range(self.distance_matrix.shape[0]))
        return [random.sample(permutation, len(permutation)) for i in range(self.n_genes)]

    def select_best_genes(self, genes):
        """Filter population to only superior genes
        Implement Ian

        Arguments:
            genes {[type]} -- [description]
        """
        return select_best_paths(genes, self.distance_matrix, self.n_genes, make_loop=True)

    def get_acumulated_inverse_cost(self, genes):
        """Generate a list with the acumulated cost for genes
        Implement Waine

        Arguments:
            genes {}
        """
        acumulated_inverse_cost = [1/calculate_path_cost(
            genes[0]+[genes[0][0]], self.distance_matrix)]

        for i in range(1, len(genes)):
            acumulated_inverse_cost.append(
                1/calculate_path_cost(genes[i]+[genes[i][0]], self.distance_matrix)
                + acumulated_inverse_cost[i-1])
        return [i/acumulated_inverse_cost[-1] for i in acumulated_inverse_cost]

    def get_crossover_pair(self, acumulated_cost):
        """Generate pair index of genes for the use of crossover
        Implement Waine

        Arguments:
            acumulated_cost {list} -- Acumulated cost list to use
        """

        rand1, rand2 = random.random(), \
                random.random()

        idx1, idx2 = 0, 0

        for i in range(1, len(acumulated_cost)):
            if(rand1 >= acumulated_cost[i-1] 
               and rand1 <= acumulated_cost[i]):
                idx1 = i

            if(rand2 >= acumulated_cost[i-1] 
               and rand2 <= acumulated_cost[i]):
                idx2 = i

        return idx1, idx2

    def generate_new_genes(self, genes):
        """Generate new genes based on the passed genes, using crossover and mutation
        Implement Waine

        Arguments:
            genes {List} -- List of genes in current state, used to generate new genes
        """
        new_genes = []
        acumulated_inverse_cost = self.get_acumulated_inverse_cost(genes)

        while len(new_genes) < self.n_genes*self.ratio_of_genes_to_generate:
            idx1, idx2 = self.get_crossover_pair(acumulated_inverse_cost)
            new_gene1, new_gene2 = self.crossover(genes[idx1], genes[idx2])
            new_genes.extend([self.mutate(new_gene1), self.mutate(new_gene2)])
        return genes + new_genes

    def crossover(self, gene1, gene2):
        """Crossover the elements of two genes to generate two new genes
        Implement Waine

        Arguments:
            gene1 {List} -- First gene to use
            gene2 {List} -- Second gene to use
        """
        assert len(gene1) == len(gene2)
        idx_cut = random.randrange(len(gene1))
        return gene1[:idx_cut] + [i for i in gene2 if i not in gene1[:idx_cut]], \
            gene2[:idx_cut] + [i for i in gene1 if i not in gene2[:idx_cut]]

    def mutate(self, gene):
        """Mutate a gene changing swaping two of its chromossomes
        Implement Ian
        Arguments:
            gene {List} -- gene to mutate
        """
        will_mutate = random.randint(0, 100) < self.probability_of_mutation
        if will_mutate:
            shuffled = [i for i in range(self.distance_matrix.shape[0])]
            random.shuffle(shuffled)
            mutation_points = sorted(shuffled[:2])
            gene[mutation_points[0]], gene[mutation_points[1]] = \
                gene[mutation_points[1]], gene[mutation_points[0]]
        return gene

    def stop_condtion(self):
        """Condition to stop the algorithm, it stops when the last n fitnesses of populations are the same
        Implement Ian
        """
        if (len(self.past_fitness)
            and self.past_fitness[0] == self.past_fitness[-1]
            and len(self.past_fitness) == self.maximum_fitness_to_hold):
            # print('getting out in iteration {} with fitness'.format(self.iteration), self.past_fitness[-1])
            return True
        self.iteration += 1
        return False
