from constants import K_STATES
from utils import calculate_path_cost, select_best_paths
import random

class BeamSearchSolver:
    def __init__(self, k_states=K_STATES):
        self.k_states = k_states

    def get_parameters(self):
        return {"k_states": int(self.k_states)}

    def solve(self, matrix):
        self.distance_matrix = matrix
        states = self.generate_k_initial_states()
        for index in range(matrix.shape[0]):
            successor_states = []
            for state in states:
                successor_states.extend(self.generate_successors_of_state(state))
            states = self.filter_successors_states(successor_states)

        return states[0]

    def generate_k_initial_states(self):
        """Generate K inital states for algorithm
        Implement Ian
        """
        # Generate unique initial states
        states = list(range(self.distance_matrix.shape[0]))
        random.shuffle(states)
        return [[state] for state in states[:self.k_states]]

    def generate_successors_of_state(self, state):
        """Generate all possible next states from state
        The next possibles paths choices are all nodes that are currently not in state
        Implement Ian

        Arguments:
            state {List[int]} -- state to use as base of successors states
        """
        if len(state) == self.distance_matrix.shape[0]: return [state + [state[0]]]
        return [
            state + [i]
            for i in range(self.distance_matrix.shape[0])
            if not i in state]

    def filter_successors_states(self, states):
        """Filters the successor states generated using the path cost
        as objective function
        Implement Waine
        
        Arguments:
            states {List} -- List of states to filtrate
        """
        return select_best_paths(states, self.distance_matrix, number_of_remaining_paths=self.k_states)