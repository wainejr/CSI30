from t01.constants import K_STATES
from t01.utils import calculate_path_cost, select_best_paths
import random

class BeamSearchSolver:
    def __init__(self):
        pass

    def solve(self, matrix):
        self.distance_matrix = matrix
        states = self.generate_k_initial_states()
        # print('initial state=', states)
        for index in range(matrix.shape[0]):
            successor_states = []
            for state in states:
                successor_states.extend(self.generate_successors_of_state(state))
            # print('successor states=', successor_states)
            states = self.filter_successors_states(successor_states)
            # print('final filtered states=', states)
        return states[0]

    def generate_k_initial_states(self):
        """Generate K inital states for algorithm
        Implement Waine
        """
        # Generate unique initial states
        return [[random.randrange(self.distance_matrix.shape[0])]
                for i in range(K_STATES)]

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
        return select_best_paths(states, self.distance_matrix)