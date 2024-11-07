from flask import Flask , render_template , request
from flask.json import jsonify
import numpy as np
import ast
import time
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

    sol = MatrixSolver()
    start_time = time.time()
    result = sol.handle(matrix,b,operation,epsilon,its,x0)
    end_time = time.time()
    elapsed_time = end_time - start_time
    if elapsed_time < 1e-6:  # Set a threshold to avoid zero time
        elapsed_time = 1e-6 
    elapsed_time = "{:.6e}".format(elapsed_time)
    return jsonify({"result" : result , "time" : elapsed_time})
    
    
    

if __name__ == "__main__":
    app.run(debug=True)