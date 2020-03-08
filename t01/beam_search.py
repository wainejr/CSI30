from constants import K_STATES


class BeamSearchSolver:
    def __init__(self):
        pass

    def solve(self, matrix):
        self.distance_matrix = matrix
        states = self.generate_k_initial_states()
        for index in range(matrix.shape[0]):
            successor_states = []
            for state in states:
                successor_states.extend(self.generate_successor_of_state(state))
            states = self.filter_successor_states(successor_states)
        return self.select_best_state(states)

    def generate_k_initial_states(self):
        """[summary]
        Implement Waine

        """
        pass

    def generate_successor_of_state(self, state):
        """[summary]
        Implement Ian

        Arguments:
            state {[type]} -- [description]
        """
        pass

    def filter_successor_states(self, states):
        """
        Implement Waine
        
        Arguments:
            states {List} -- [description]
        """
        pass

    def select_best_state(self, states):
        """
        Implement Ian
        
        Arguments:
            states {List} -- [description]
        """
        pass
