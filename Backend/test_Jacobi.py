import numpy as np

def Jacobi(A: np.ndarray, b: np.ndarray, epsilon=1e-9, iterations=50, x=None):

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

A = np.array([[2.0,1.0],
           [5.0,7.0]])

b = np.array([11.0,13.0])

x = Jacobi(A,b)


print(x)