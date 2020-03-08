from constants import N_GENES, MAXIMUM_FITNESS_TO_HOLD, NUMBER_OF_GENES_TO_GENERATE, MAX_ITERATIONS
from utils import calculate_path_cost


class GeneticAlgorithmSolver:

    def __init__(self):
        self.past_fitness = []
        pass

    def solve(self, matrix):
        genes = self.generate_n_initial_genes()
        it = 0
        while !self.stop_condtion() and it < MAX_ITERATIONS:
            genes = self.generate_new_genes(genes)
            genes = self.select_best_genes(genes)
            self.past_fitness.append(calculate_path_cost(self.select_best_gene(genes)))
            if len(self.past_fitness) > MAXIMUM_FITNESS_TO_HOLD:
                self.past_fitness.pop(0)
            it += 1
        return self.select_best_gene(genes)

    def generate_n_initial_genes(self):
        """[summary]
        Implement Waine

        """
        pass

    def select_best_genes(self, genes):
        """[summary]
        Implement Ian

        Arguments:
            genes {[type]} -- [description]
        """
        pass

    def generate_new_genes(self, genes):
        """[summary]
        Implement Waine

        Arguments:
            genes {[type]} -- [description]
        """
        pass

    def crossover(self, gene1, gene2):
        """[summary]
        Implement Waine
        
        Arguments:
            gene1 {[type]} -- [description]
            gene2 {[type]} -- [description]
        """
        pass

    def mutate(self, gene):
        """[summary]
        Implement Ian
        Arguments:
            gene {[type]} -- [description]
        """
        pass

    def select_best_gene(self, genes):
        """[summary]
        Implement Ian

        Arguments:
            genes {[type]} -- [description]
        """
        pass

    def stop_condtion(self):
        """[summary]
        Implement Ian
        """
        pass



