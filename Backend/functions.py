import numpy as np

def Gauss_Elimination(A : np.ndarray ,B : np.ndarray):
    n = len(B)

    augmented_matrix = np.hstack((A, B.reshape(-1,1)))

    for i in range(n):
        max_row = np.argmax(np.abs(augmented_matrix[i:n,i])) + i
        augmented_matrix[[i,max_row]] = augmented_matrix[[max_row,i]]

        for j in range(i+1,n):
            factor = augmented_matrix[j,i] / augmented_matrix[i,i]
            augmented_matrix [j,i:] -= factor * augmented_matrix[i,i:]
    x = np.zeros(n)
    for i in range(n-1,-1,-1):
        x[i] = augmented_matrix[i, -1] / augmented_matrix[i, i]
        augmented_matrix[:i, -1] -= augmented_matrix[:i, i] * x[i]
    return x , augmented_matrix
    
A = np.array([[2, -1, 1], [1, 3, 2], [1, 2, 3]],dtype = float) 
B = np.array([5,10,15])
x , matrix = Gauss_Elimination(A,B)
x , matrix = np.round(x, 2) , np.round(matrix,2)
print (f"x = \n {x} \n the matrix is \n{matrix}")