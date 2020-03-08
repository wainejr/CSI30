from constants import K_STATES
from utils import calculate_path_cost
import random

class BeamSearchSolver:
    def __init__(self):
        pass

    def solve(self, matrix):
        self.distance_matrix = matrix
        states = self.generate_k_initial_states()
        for index in range(matrix.shape[0]):
            successor_states = []
            for state in states:
                successor_states.extend(self.generate_successors_of_state(state))
            states = self.filter_successors_states(successor_states)
        return self.select_best_state(states)

    def generate_k_initial_states(self):
        """Generate K inital states for algorithm
        Implement Waine
        """
        # Generate unique initial states
        return [[random.randrange(self.distance_matrix.shape[0])]
                for i in range(K_STATES)]

    def generate_successors_of_state(self, state):
        """[summary]
        Implement Ian

        Arguments:
            state {[type]} -- [description]
        """
        pass

    def filter_successors_states(self, states):
        """Filters the successor states generated using the path cost
        as objective function
        Implement Waine
        
        Arguments:
            states {List} -- List of states to filtrate
        """
        return sorted(states,
            key=lambda f: calculate_path_cost(f, self.distance_matrix))[:K_STATES]

    def select_best_state(self, states):
        """
        Implement Ian
        
        Arguments:
            states {List} -- [description]
        """
        pass
