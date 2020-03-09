import random

from constants import N_GENES, \
    MAXIMUM_FITNESS_TO_HOLD, \
    NUMBER_OF_GENES_TO_GENERATE, \
    MAX_ITERATIONS, \
    PROBABILITY_OF_MUTATION
from utils import calculate_path_cost, select_best_paths


class GeneticAlgorithmSolver:

    def __init__(self):
        self.past_fitness = []
        pass

    def solve(self, matrix):
        self.distance_matrix = matrix
        genes = self.generate_n_initial_genes()
        it = 0
        while not self.stop_condtion() and it < MAX_ITERATIONS:
            genes = self.generate_new_genes(genes)
            print('genes generated=', genes)
            genes = self.select_best_genes(genes)
            print('best genes=', genes)
            self.past_fitness.append(calculate_path_cost(genes[0], self.distance_matrix))
            if len(self.past_fitness) > MAXIMUM_FITNESS_TO_HOLD:
                self.past_fitness.pop(0)
            print('past fitness=', self.past_fitness)
            it += 1
        return genes[0]

    def generate_n_initial_genes(self):
        """Generate N random genes for initialization
        Implement Waine
        """
        permutation = list(range(self.distance_matrix.shape[0]))
        return [random.sample(permutation, len(permutation)) for i in range(N_GENES)]

    def select_best_genes(self, genes):
        """[summary]
        Implement Ian

        Arguments:
            genes {[type]} -- [description]
        """
        return select_best_paths(genes, self.distance_matrix, N_GENES)

    def generate_new_genes(self, genes):
        """Generate new genes based on the passed genes, using crossover and mutation
        Implement Waine

        Arguments:
            genes {List} -- List of genes in current state, used to generate new genes
        """
        new_genes = []
        while len(new_genes) < NUMBER_OF_GENES_TO_GENERATE:
            idx1, idx2 = random.randrange(len(genes)), \
                random.randrange(len(genes))
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
        return gene1[:idx_cut] + gene2[idx_cut:], \
            gene2[:idx_cut] + gene1[idx_cut:]

    def mutate(self, gene):
        """Mutate a gene changing swaping two of its chromossomes
        Implement Ian
        Arguments:
            gene {List} -- gene to mutate
        """
        will_mutate = random.randint(0, 100) < PROBABILITY_OF_MUTATION
        if will_mutate:
            shuffled = [i for i in range(self.distance_matrix.shape[0])]
            random.shuffle(shuffled)
            mutation_points = sorted(shuffled[:2])
            gene[mutation_points[0]], gene[mutation_points[1]] = gene[mutation_points[1]], gene[mutation_points[0]]
        return gene

    def stop_condtion(self):
        """[summary]
        Implement Ian
        """
        return False



