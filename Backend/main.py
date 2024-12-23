from flask import Flask  , request
from flask.json import jsonify
import numpy as np
import time

# from torch import res
from MatrixSolver import MatrixSolver
from flask_cors import CORS

from Rootfinder import RootFinder

app = Flask(__name__)
CORS(app)
@app.route('/alphabetical',methods =["POST"])
def alpha():
    data = request.get_json()
    matrix = data.get("matrix")
    Solver = MatrixSolver()
    result = Solver.alphabeticalSolution(matrix)
    try:
        result_serializable = {str(key): str(value) for key, value in result.items()}
    except:
        if result == "No Solution For Matrix":
             return {"error" : result}
        else:
             result_serializable = result
    print(result_serializable)
    return result_serializable
@app.route('/', methods=["POST"])
def home():
    try:
        # Parse incoming JSON data
        data = request.get_json()
        # Extract data from JSON
        augmented_matrix = data.get("matrix")
        if not augmented_matrix:
            return jsonify({"error": "Matrix data is missing"}), 400
        augmented_matrix = np.array(augmented_matrix, dtype=float)

        x0 = data.get("x0")
        x0 = np.array(x0)
        # print(x0)
        # return jsonify("hello")
        significant_digits = data.get("significant_digits")
        # mode = data.get("mode")
        its = data.get("its")
        epsilon = data.get("epsilon")
        operation = int(data.get("operation", 1)) 

        # Process the augmented matrix
        matrix = augmented_matrix[:, :-1]
        b = augmented_matrix[:, -1]
        Solver = MatrixSolver()
        start = time.time()
        try :
            if operation == 1 or operation == 2 or operation == 5 or operation == 6:
                    x , result = Solver.handle(matrix , b , operation , epsilon , its , x0 , significant_digits)
                    end = time.time()
                    elapsed =  end - start
                    elapsed = float(np.clip(elapsed , 1e-6, None))
                    print(x , result , elapsed , sep="\n")
                    return jsonify({"x" : x.tolist(),
                                    "result" : result.tolist(),
                                    "time_taken" : elapsed})
            elif operation == 3 or operation == 4:
                    x , iterations = Solver.handle(matrix , b , operation , epsilon , its , x0 , significant_digits)
                    end = time.time()
                    elapsed =  end - start
                    elapsed = float(np.clip(elapsed , 1e-6, None))
                    print(x , elapsed , sep="\n")
                    return jsonify({"x" : x.tolist(),
                                    "time_taken" : elapsed , 
                                    "iterations" : iterations,
                                    "time_taken" : elapsed})
            elif operation == 7:
                    x,L = Solver.handle(matrix , b , operation , epsilon , its , x0 , significant_digits)
                    end = time.time()
                    elapsed =  end - start
                    elapsed = float(np.clip(elapsed , 1e-6, None))
                    print(x , L , elapsed , sep="\n")
                    return jsonify({"x" : x.tolist(),
                                    "L" : L.tolist(),
                                    "time_taken" : elapsed})
        except:
            error = Solver.handle(matrix , b , operation , epsilon , its , x0 , significant_digits)
            return jsonify({"error" : error})
    except:
        return jsonify({"error" : "an error has occured"})
@app.route('/roots', methods=["POST"])
def root():
    data = request.get_json()
    function = data.get("function")
    operation = data.get("operation")
    significat_digits = data.get("significant_digits")
    max_its = data.get("max_its")
    x0 = data.get("x0")
    x1 = data.get("x1")
    xl = data.get("xl")
    xu = data.get("xu")
    Root = RootFinder()
if __name__ == "__main__":
    app.run(debug=True)