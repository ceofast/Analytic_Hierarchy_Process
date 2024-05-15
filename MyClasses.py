import numpy as np

class Calculation:
    @staticmethod
    def validate_matrix(matrix):
        """
        Validate the properties of the matrix to ensure it is suitable for AHP calculations.

        Parameters:
            matrix (np.ndarray): A square numpy matrix containing the pairwise comparison values.

        Raises:
            ValueError: If the matrix is not a square matrix, not a numpy array, or contains elements less than or equal to zero.
        """
        if not isinstance(matrix, np.ndarray):
            raise ValueError("Matrix must be a numpy array.")
        if matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Matrix must be square.")
        if np.any(matrix <= 0):
            raise ValueError("Matrix elements must be greater than zero.")

    @staticmethod
    def calc_average(criteria, length):
        """
        Calculate the priority vector by normalizing the criteria matrix and averaging over columns.

        Parameters:
            criteria (np.ndarray): The criteria matrix for which the average is to be calculated.
            length (int): The number of criteria, which should correspond to the dimension of the matrix.

        Returns:
            np.ndarray: The priority vector derived from the criteria matrix.
        """
        Calculation.validate_matrix(criteria)
        sum_c = np.sum(criteria, axis=0)
        c_average = criteria / sum_c
        average_criteria = np.mean(c_average, axis=1)
        return average_criteria

    @staticmethod
    def mux_array(c1, c2, c3, c4, all_criteria):
        """
        Aggregate multiple criteria evaluations into a single priority vector using matrix multiplication.

        Parameters:
            c1, c2, c3, c4 (np.ndarray): Arrays of criteria evaluations.
            all_criteria (np.ndarray): A matrix of weights or importance assigned to each criterion.

        Returns:
            np.ndarray: The resultant priority vector.
        """
        result = np.dot(np.array([c1, c2, c3, c4]).T, all_criteria)
        return result

    @staticmethod
    def consistency_vector(all_criteria, average_criteria):
        """
        Calculate the consistency ratio (CR) to evaluate the consistency of the pairwise comparison matrix.

        Parameters:
            all_criteria (np.ndarray): The pairwise comparison matrix.
            average_criteria (np.ndarray): The priority vector derived from the pairwise comparison matrix.

        Returns:
            float: The consistency ratio, a measure of how consistent the comparisons were.
        """
        RI = [0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41]  # Extended RI values for larger matrices
        n = all_criteria.shape[0]
        if n >= len(RI):
            raise ValueError("RI value not defined for n = {}".format(n))
        weighted_sum_vector = np.dot(all_criteria, average_criteria) / average_criteria
        lambda_max = np.mean(weighted_sum_vector)
        CI = (lambda_max - n) / (n - 1)
        CR = CI / RI[n]
        return CR
