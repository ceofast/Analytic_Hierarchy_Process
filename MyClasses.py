import numpy as np

class Calculation:
    @staticmethod
    def validate_matrix(matrix):
        if not isinstance(matrix, np.ndarray):
            raise ValueError("Matrix must be a numpy array.")
        if matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Matrix must be square.")
        if np.any(matrix <= 0):
            raise ValueError("Matrix elements must be greater than zero.")

    @staticmethod
    def calc_average(criteria, length):
        Calculation.validate_matrix(criteria)
        sum_c = np.sum(criteria, axis=0)
        c_average = criteria / sum_c
        average_criteria = np.mean(c_average, axis=1)
        return average_criteria

    @staticmethod
    def mux_array(c1, c2, c3, c4, all_criteria):
        result = np.dot(np.array([c1, c2, c3, c4]).T, all_criteria)
        return result

    @staticmethod
    def consistency_vector(all_criteria, average_criteria):
        RI = [0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41]  # Extended RI values for larger matrices
        n = all_criteria.shape[0]
        if n >= len(RI):
            raise ValueError("RI value not defined for n = {}".format(n))
        weighted_sum_vector = np.dot(all_criteria, average_criteria) / average_criteria
        lambda_max = np.mean(weighted_sum_vector)
        CI = (lambda_max - n) / (n - 1)
        CR = CI / RI[n]
        return CR
