import numpy as np

def Jacobi(A: np.ndarray, b: np.ndarray, epsilon=1e-9, iterations=50, x=None, mode=2):
    # 'mode' is what determines wether to use iterations or epsilon for solving 
    # 'mode' = 1 is iterations, 'mode' = 2 is epsilon (absolute relative error)
    # if 'mode' is negative it means Gauess Seidel is applied and not Jacobi
    try:
        max_its = 2000
        GaussSeidel = False
        if (mode<0):
            GaussSeidel = True
            mode = abs(mode)

        if (mode!=1 and mode!=2):
            raise ValueError("Unknown Mode choosen in Jacobi.")
        
        # Initialise x with zeros if none was given
        if (x is None):
            x = np.zeros(A.shape[0])

        # Testing if any diagonal element is 0
        D = np.diag(A)
        if np.any(D == 0):
            raise ValueError("Matrix contains zero diagonal elements, Jacobi method cannot proceed.")
        
        curr_it = 0
        while(True):
            
            # Each iteration, we iterate over all x apply the rule 
            x_new = x.copy()
            for i in range(A.shape[0]):
                
                x_new[i] = b[i]
                for j in range(A.shape[0]):
                    if (i==j):
                        continue
                    if (GaussSeidel): x_new[i] -= A[i][j]*x_new[j]
                    else: x_new[i] -= A[i][j]*x[j]

                x_new[i] /= A[i][i]  
            
            # Check if "iterations" has passed
            if (mode==1):
                if (curr_it > iterations):
                    print("Iterations", curr_it)
                    return x_new
            
                 # If a max number of iterations has passed or the values of x diverge (near infinity-wise)
                if (curr_it > max_its or np.isinf(np.linalg.norm(np.dot(A, x) - b))):
                    # print("Max iterations passed with no convergence")
                    if (GaussSeidel): print("Divergence occured in Gauss Seidel")
                    else: print("Divergence occured in Jacobi")
                    print("Iterations", curr_it)
                    return x_new

            # Check absolute relative error OR divergence
            elif (mode==2):
                
                condition = True
                for i in range(A.shape[0]):
                    # Checking absolute relative error of every x, if even one value x hasn't converged (abs error > epsilon)
                    if ( not (abs(x[i] - x_new[i]) < epsilon) ):
                        condition = False
                if (condition):
                    # Convergence
                    print("Iterations", curr_it)
                    return x_new
                
                # If a max number of iterations has passed or the values of x diverge (near infinity-wise)
                if (curr_it > max_its or np.isinf(np.linalg.norm(np.dot(A, x) - b))):
                    # print("Max iterations passed with no convergence")
                    if (GaussSeidel): print("Divergence occured in Gauss Seidel")
                    else: print("Divergence occured in Jacobi")
                    print("Iterations", curr_it)
                    return x_new

            x = x_new 
            curr_it+=1

        return x_new
    
    except ZeroDivisionError as e:
        return str(e)
    except ValueError as e:
        return str(e)
        

def GaussSeidel(A: np.ndarray, b: np.ndarray, epsilon=1e-9, iterations=50, x=None, mode=2):
    return Jacobi(A, b, epsilon, iterations, x, mode=-mode)
    

# Wrong answer
A = np.array([[3.0, 1.0, 4.0],
           [2.0, 1.0, 5.0],
           [5.0, -1.0, -5.0]])

b = np.array([11.0, 13.0, -9.0])

# Wrong answer
nA_converge = np.array([
    [1.0, 3.0, 2.0],
    [2.0, 1.0, 3.0],
    [3.0, 2.0, 1.0]
])
nb_converge = np.array([4.0, 5.0, 6.0])

# Works as intended 
A_converge = np.array([
    [4.0, 1.0, 2.0],
    [1.0, 3.0, 1.0],
    [2.0, 1.0, 5.0]
])
b_converge = np.array([4.0, 5.0, 6.0])

# A_converge = np.array([
#     [14, 12, 2.0],
#     [5, 5.36, 0],
#     [1, 1, 3]
# ])
# b_converge = np.array([-5, 2, -2])

print("Jacobi")
x = Jacobi(nA_converge,nb_converge, mode=2)
print(x)

print()

print("Gauss Seidel")
x2 = GaussSeidel(nA_converge,nb_converge, mode=2)
print(x2)

####
print()
print()
####

print("Jacobi")
x = Jacobi(A_converge,b_converge, mode=2)
print(x)

print()

print("Gauss Seidel")
x2 = GaussSeidel(A_converge,b_converge, mode=2)
print(x2)