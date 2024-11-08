import numpy as np
import time
class MatrixSolver:

    significant_digits : float
    def handle(self,matrix,b,operator, epsilon, its, x0):
        if operator == 1:
            try :
                x,result = self.Gauss_Elimination(matrix,b)
                return {"answer" : x.tolist() , "matrix" : result.tolist()}
            except :
                error = self.Gauss_Elimination(matrix,b)
                return error
        elif operator == 2:
            try :
                x,result = self.Gauss_Jordan_Elimination(matrix,b)
                return {"answer" : x.tolist() , "matrix" : result.tolist()}
            except :
                error = self.Gauss_Jordan_Elimination(matrix,b)
                return error
        elif operator == 4:
            try :
                x = self.Jacobi(matrix,b, epsilon, its, x0)
                return {"answer" : x.tolist() , "matrix" : None}
            except :
                error = self.Jacobi(matrix,b, epsilon, its, x0)
                return error
        elif operator == 5:
            try :
                x = self.LUCroutsForm(matrix,b)
                return {"answer" : x.tolist() , "matrix" : None}
            except :
                error = self.LUCroutsForm(matrix,b)
                return error
        elif operator == 6:
            try :
                x = self.LUCholeskyForm(matrix,b)
                return {"answer" : x.tolist() , "matrix" : None}
            except :
                error = self.LUCholeskyForm(matrix,b)
                return error                

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


    def forward_substitution(self, augmented_matrix, n):
        x = np.zeros(n)
        for i in range(n):
            if augmented_matrix[i, i] == 0:
                return "System has no unique solution."
            x[i] = augmented_matrix[i, -1] / augmented_matrix[i, i]
            for j in range(i + 1, n):
                augmented_matrix[j, -1] -= augmented_matrix[j, i] * x[i]
        # Handle negative zero values
        x = np.where(x == -0.0, 0.0, x)

        return x, augmented_matrix       


    def backward_Elimination(self,augmented_matrix,n):
        for i in range(n-1, -1, -1):
                # Normalize the pivot row (make the pivot element equal to 1)
                augmented_matrix[i] /= augmented_matrix[i, i]
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
            
            x, augmented_matrix = self.backward_substitution(augmented_matrix,n)

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

    def Jacobi(self, A: np.ndarray, b: np.ndarray, epsilon=1e-9, iterations=50, x=None):
        try:
            # Initialise x with zeros if none was given
            if (x is None):
                x = np.zeros(A.shape[0])

            # Creating the matrices needed, based on equation x = D_Inverse*(b-(A-D)*x) 
            D = np.diag(A) # Retunrs 1-D vector of diagonal elements
            D_inverse = np.diag(1/D) # Creates a 2-D matrix of it
            AminusD = A - np.diag(D)
            for it in range(iterations):
                
                xNew = np.dot(D_inverse, (b - np.dot(AminusD, x)))
                
                if np.linalg.norm(xNew - x) < epsilon:
                    print(f"Done in {it+1} iterations")
                    return xNew
                
                x = xNew
            
            return xNew
        
        except ZeroDivisionError as e:
            return str(e)

    
    def LUCroutsForm(self,A: np.ndarray, B: np.ndarray):
        L = np.zeros_like(A)
        U = np.zeros_like(A)
        n = len(B)
        for i in range(A.shape[0]):
            for j in range(i):
                L[i][j] = A[i][j]
                A[i] -= L[i][j] * U[j]
            L[i][i] = A[i][i] #i==j (diagonal)
            if L[i][i] != 0:
                U[i] = A[i] / L[i][i]
            else:  # infinite number of solution or no solution
                return "System has no unique solution or no solution."
        #solve the equation        
        augmented_L = np.hstack((L, B.reshape(-1, 1)))
        Y, augmented_L = self.forward_substitution(augmented_L,n)
        augmented_U = np.hstack((U, Y.reshape(-1, 1)))
        X, augmented_U = self.backward_substitution(augmented_U,n)
        return X


    def LUCholeskyForm(self,A: np.ndarray, B: np.ndarray):
        L = np.zeros_like(A)
        for i in range(A.shape[0]):
            for j in range(i):
                s=np.sum(L[i][:j]*L[j][:j])
                L[i][j]=(A[i][j]-s)/L[j][j]
            s=np.sum(L[i][:i]**2)
            L[i][i]=np.sqrt(A[i][i]-s)
        U=L.T   #U = L transpose
        n=len(B)
        #solve the equation     
        augmented_L = np.hstack((L, B.reshape(-1, 1)))
        Y, augmented_L = self.forward_substitution(augmented_L,n)
        augmented_U = np.hstack((U, Y.reshape(-1, 1)))
        X, augmented_U = self.backward_substitution(augmented_U,n)
        return X    

