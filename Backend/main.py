from flask import Flask , render_template , request
from flask.json import jsonify
import numpy as np
import ast
import time

# from torch import res
from functions import MatrixSolver
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/' , methods = ["POST"])
def home():
    
    augmented_matrix = request.form['matrix']
    augmented_matrix = ast.literal_eval(augmented_matrix)
    augmented_matrix = np.array(augmented_matrix, dtype=float)
    
    matrix = augmented_matrix[:,:-1]
    
    b = augmented_matrix[:, -1]

    operation = int(request.form['operation'])

    its = int(request.form["its"])

    epsilon = float(request.form["epsilon"])

    x0 = int(request.form["x0"])

    mode = int(request.form["mode"])
    sol = MatrixSolver()
    start_time = time.time()
    result = sol.handle(matrix,b,operation,epsilon,its,x0,mode)
    end_time = time.time()
    elapsed_time = end_time - start_time
    if elapsed_time < 1e-6:  # Set a threshold to avoid zero time
        elapsed_time = 1e-6 
    elapsed_time = "{:.6e}".format(elapsed_time)
    if(operation == 1 or operation == 2 or operation == 5 or operation == 6):
        answer = result["answer"]
        matrix = result["matrix"]
        print(f"answer is {answer}")
        print(f"matrix is {matrix}")
        return jsonify({"answer" : answer , "matrix" : matrix ,"time" : elapsed_time})
    elif(operation == 3 or operation == 4):
        answer = result["answer"]
        iterations = result["iterations"]
        return jsonify({"answer" : answer , "iterations" : iterations , "time" : elapsed_time})
    elif(operation == 7):
        answer = result["answer"]
        L = result["L"]
        return jsonify({"answer" : answer , "L" : L, "time" : elapsed_time})
    
    
    
    

if __name__ == "__main__":
    app.run(debug=True)