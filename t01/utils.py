def check_if_path_is_valid_solution(path, number_of_nodes):
    """Receives a path as a list and returns a boolean indicating whether this path is a solution
    Implemented Ian
    """
    max_permitted_sum = (n * (n + 1))/2
    return len(path) > 1  and path[0] == path[-1] and sum(path[:(len(path) - 1)]) == max_permitted_sum

def calculate_path_cost(path, distance_matrix):
    """Calculates the cost of a path as a list based on the distance matrix and return
    Implemented Waine
    """
    return sum([distance_matrix[path[i], path[i+1]] for i in range(0, len(path)-1)])
