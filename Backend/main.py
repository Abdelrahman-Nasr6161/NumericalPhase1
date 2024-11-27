from unittest import result
from flask import Flask , render_template , request
from flask.json import jsonify
import numpy as np
import ast
import time

from torch import res
from functions import MatrixSolver
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
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

        x0 = int(data.get("x0", 4))  # Default to 0 if x0 is missing
        mode = data.get("mode")
        its = data.get("its")
        epsilon = data.get("epsilon")
        operation = int(data.get("operation", -1))  # Default to -1 if operation is missing

        # Process the augmented matrix
        matrix = augmented_matrix[:, :-1]
        b = augmented_matrix[:, -1]

        # print(f"{matrix}  \n {b} \n {mode} \n {its} \n {epsilon} \n {operation} \n {x0}")

        Solver = MatrixSolver()
        start = time.time()
        try :
            if operation == 1 or operation == 2 or operation == 5 or operation == 6:
                    x , result = Solver.handle(matrix , b , operation , epsilon , its , x0 , mode)
                    end = time.time()
                    elapsed =  end - start
                    print(x , result , elapsed , sep="\n")
                    return jsonify({"x" : x.tolist(),
                                    "result" : result.tolist(),
                                    "time_taken" : elapsed})
            elif operation == 3 or operation == 4:
                    x = Solver.handle(matrix , b , operation , epsilon , its , x0 , mode)
                    end = time.time()
                    elapsed =  end - start
                    print(x , elapsed , sep="\n")
                    return jsonify({"x" : x.tolist(),
                                    "time_taken" : elapsed})
            elif operation == 7:
                    x,L = Solver.handle(matrix , b , operation , epsilon , its , x0 , mode)
                    end = time.time()
                    elapsed =  end - start
                    print(x , L , elapsed , sep="\n")
                    return jsonify({"x" : x.tolist(),
                                    "L" : L.tolist()})
        except:
            error = Solver.handle(matrix , b , operation , epsilon , its , x0 , mode)
            return jsonify({"error" : error})

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

    
    

if __name__ == "__main__":
    app.run(debug=True)