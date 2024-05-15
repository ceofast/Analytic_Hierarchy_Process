import numpy as np

class Calculation:
    @staticmethod
    def calc_average(criteria, length):
        """
        Calculate the average priorities for each criterion based on a comparison matrix.
        
        Parameters:
            criteria (numpy.ndarray): A square matrix where each element represents the relative importance of a criterion.
            length (int): The size of one dimension of the square matrix, i.e., the number of criteria.
        
        Returns:
            numpy.ndarray: An array containing the average priority of each criterion.
        """
        sum_c = np.sum(criteria, axis=0)
        c_average = criteria / sum_c
        average_criteria = np.mean(c_average, axis=1)
        return average_criteria

    @staticmethod
    def mux_array(c1, c2, c3, c4, all_criteria):
        """
        Multiply matrices to aggregate criteria evaluations into a single priority vector.
        
        Parameters:
            c1, c2, c3, c4 (numpy.ndarray): Arrays representing the criteria evaluations.
            all_criteria (numpy.ndarray): A matrix representing the weights or importance assigned to each set of criteria.
        
        Returns:
            numpy.ndarray: The resultant vector after matrix multiplication, representing the aggregated priority of criteria.
        """
        result = np.dot(np.array([c1, c2, c3, c4]).T, all_criteria)
        return result

    @staticmethod
    def consistency_vector(all_criteria, average_criteria):
        """
        Calculate the consistency index of the decision matrix to evaluate the consistency of the comparisons made between the criteria.
        
        Parameters:
            all_criteria (numpy.ndarray): The decision matrix containing the relative weights of criteria.
            average_criteria (numpy.ndarray): The vector containing the average priorities derived from the decision matrix.
        
        Returns:
            float: The calculated inconsistency index, which indicates the level of consistency in the judgments.
        """
        weighted_sum_vector = np.dot(all_criteria, average_criteria) / average_criteria
        calc_val = np.mean(weighted_sum_vector)
        m_inconsistency_index = (calc_val - len(average_criteria)) / (len(average_criteria) - 1)
        return m_inconsistency_index
