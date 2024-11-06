import numpy as np

class MatrixSolver:

    significant_digits : float

    def forward_Elimination(self,augmented_matrix,n):
        for i in range(n):
                # Find the row with the maximum absolute value in column i
                max_row = np.argmax(np.abs(augmented_matrix[i:n, i])) + i
                augmented_matrix[[i, max_row]] = augmented_matrix[[max_row, i]]

                # Check if the pivot element is zero or very close to zero
                if np.abs(augmented_matrix[i, i]) < 1e-12:
                    return "Pivot element is zero or very small, cannot proceed."

                # Perform the row reduction
                for j in range(i + 1, n):
                    factor = augmented_matrix[j, i] / augmented_matrix[i, i]
                    augmented_matrix[j, i:] -= factor * augmented_matrix[i, i:]
                return augmented_matrix
        


    def backward_Elimination(self,augmented_matrix,n):
        for i in range(n-1, -1, -1):
                # Normalize the pivot row (make the pivot element equal to 1)
                augmented_matrix[i] /= augmented_matrix[i, i]
                print(augmented_matrix)
                # Eliminate the elements above the pivot
                for j in range(i-1, -1, -1):  # Go through rows above the pivot
                    factor = augmented_matrix[j, i]
                    augmented_matrix[j, i:] -= factor * augmented_matrix[i, i:]
        return augmented_matrix



    def backward_substitution(self,augmented_matrix,n):
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            if augmented_matrix[i, i] == 0:
                return "System has no unique solution."
            x[i] = augmented_matrix[i, -1] / augmented_matrix[i, i]
            augmented_matrix[:i, -1] -= augmented_matrix[:i, i] * x[i]
        # Handle negative zero values
        x = np.where(x == -0.0, 0.0, x)
        return x , augmented_matrix
    


    def Gauss_Elimination(self, A: np.ndarray, B: np.ndarray):
        try:
            n = len(B)
            augmented_matrix = np.hstack((A, B.reshape(-1, 1)))

            augmented_matrix = self.forward_Elimination(augmented_matrix,n)
            
            x, augmented_matrix = self.backward_Elimination(augmented_matrix,n)

            return x, augmented_matrix
        except ZeroDivisionError as e:
            return str(e)
        


    def Gauss_Jordan_Elimination(self, A: np.ndarray, B: np.ndarray):
        try:
            n = len(B)
            augmented_matrix = np.hstack((A, B.reshape(-1, 1)))

            augmented_matrix = self.forward_Elimination(augmented_matrix,n)

            augmented_matrix = self.backward_Elimination(augmented_matrix,n)
            
            # Handle negative zero values
            augmented_matrix = np.where(augmented_matrix == -0.0, 0.0, augmented_matrix)
            x = augmented_matrix[:,-1]
            return x, augmented_matrix
        except ZeroDivisionError as e:
            return str(e)
