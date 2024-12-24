import flet as ft
import numpy as np
from requests import post
from sympy import symbols, sympify, lambdify
import plotly.graph_objects as go
import dash
from dash import dcc, html
import threading
import webview

def get_child(controls , key):
    child = [control for control in controls.controls if control.key == key][0]
    return child
def send_to_backend(event , page : ft.Column):
    error_message = None
    x0 = []
    criteria_its = None
    criteria_eps = None
    significant_digits = None
    operation_dropdown : ft.Dropdown = get_child(page , "operation_dropdown")
    try:
        operator_type = int(operation_dropdown.value)
    except:
        "Please Select Operation Type"
    matrix_container : ft.Column = get_child(page , "matrix_container")
    cells = matrix_container.controls
    matrix = []
    for rows in cells:
        row = []
        for item in rows.controls:
            if isinstance(item , ft.TextField):
                try :
                    value = float(item.value)
                    row.append(value)
                except:
                    error_message = "Please only enter numerals"
        matrix.append(row)
    
    suboptions : ft.Column = get_child(page , "suboptions")
    significant_text : ft.TextField = get_child(get_child(suboptions , "significant_row"), "significant_digits")
    try:
        significant_digits = int(significant_text.value)
        significant_digits = int(np.clip(significant_digits , 1 , 15))
    except:
        significant_digits = 4
    suboptions : ft.Column = get_child(page , "suboptions")
    if operator_type == 5:
        suboperator : ft.Dropdown = get_child(suboptions,"LU_sub")
        try:
            operator_type+=(int(suboperator.value)-1) 
        except:
            "Please choose a valid LU Decomposition Method"
    elif operator_type in {3,4}:
        try:
            
            criteria_its_text : ft.TextField = get_child(suboptions , "its_text_field")
            criteria_its = float(criteria_its_text.value)

            criteria_eps_text : ft.TextField = get_child(suboptions , "eps_text_field")
            criteria_eps = float(criteria_eps_text.value)

        except:
            error_message = "Please select a valid iteration method and criteria"
        intitial_guess_row : ft.Row = get_child(suboptions , "initial_guess_row")
        for item in intitial_guess_row.controls:
            if isinstance(item , ft.TextField):
                try:
                    value = float(item.value)
                    x0.append(value)
                except:
                    error_message = "Please enter valid initial guesses"
    if error_message:
        # Create a Snackbar with the error message
        snack_bar = ft.SnackBar(content=ft.Text(error_message, color="black"))
        
        page.page.overlay.append(snack_bar)

        snack_bar.open = True
        
        page.page.update()
        # Update the page to reflect the change
    
        return

        
    data = {
        "matrix" : matrix,
        "operation" : operator_type,
        "x0" : x0,
        "epsilon" : criteria_eps,
        "its" : criteria_its,
        # "mode" : mode,
        "significant_digits" : significant_digits
    }
    response = post("http://127.0.0.1:5000" , json=data)
    answers = response.json()
    handleAnswer(page , answers)

def handleAnswer(page : ft.Column , answer):
    suboptions = get_child(page , "suboptions")
    significant_row = get_child(suboptions , "significant_row")
    significant_text = get_child(significant_row , "significant_digits")
    significant_digits = None
    try:
        significant_digits = int(significant_text.value)
        significant_digits = int(np.clip(significant_digits,1,15))
    except:
        significant_digits = 4
    dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Result", size=26, color="blue"),  # Larger font for headline
            actions=[
                ft.TextButton("Okay", on_click=lambda e: page.page.close(dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
    dialog_content = ft.Column(key="dialog_content")
    if "x" in answer:
        x_vector = ft.Text(value="Result X Vector : ",size=24 , color="blue")
        x = answer['x']
        x_column = ft.Column(key="x_column")
        for i in x:
            label = ft.Text(value=f"{i:.{significant_digits}g}")
            x_column.controls.append(label)
        dialog_content.controls.append(x_vector)
        dialog_content.controls.append(x_column)
    if 'result' in answer:
        result = answer['result']
        result_vector = ft.Text(value="Resultant Matrix : ",size=24 , color="blue")
        result_answer = ft.Column(key="result_answer")
        for row in result:
            r = ft.Row()
            for i in row:
                text = ft.Text(value=f"{i:.{significant_digits}g}")
                r.controls.append(text)
            result_answer.controls.append(r)
        dialog_content.controls.append(result_vector)
        dialog_content.controls.append(result_answer)
    if 'L' in answer:
        result = answer['L']
        result_vector = ft.Text(value="L Matrix : ",size=24 , color="blue")
        result_answer = ft.Column(key="result_answer")
        for row in result:
            r = ft.Row()
            for i in row:
                text = ft.Text(value=str(i))
                r.controls.append(text)
            result_answer.controls.append(r)
        dialog_content.controls.append(result_vector)
        dialog_content.controls.append(result_answer)
    if 'iterations' in answer:
        iterations = answer['iterations']
        text = ft.Text(size=24 , value=f"Number of iterations taken = {iterations}")
        dialog_content.controls.append(text)
    if 'time_taken' in answer:
        time  = answer['time_taken']
        time_taken = ft.Text(size=24 , value=f"Time taken = {time}" , color="blue")
        dialog_content.controls.append(time_taken)
    if 'error' in answer:
        error = answer['error']
        error_text = ft.Text(size=24 , value=f"Error was found : {error}", color="red")
        dialog_content.controls.append(error_text)
    dialog.content = dialog_content
    page.page.open(dialog)
    page.page.update()

        
def alphaBackend(event ,page : ft.Column):
    error_message = None
    matrix_container = get_child(page , "matrix_container")
    matrix = []
    for rows in matrix_container.controls:
        row = []
        for item in rows.controls:
            if isinstance(item , ft.TextField):
                try:
                    value = str(item.value)[0]
                    if not value.isalpha():
                        error_message = "Please enter only alphabets"
                    row.append(value)
                except:
                    error_message = "Please enter only alphabets"
        matrix.append(row)
    data = {
        "matrix" : matrix
    }
    response = post("http://127.0.0.1:5000/alphabetical" , json=data)
    answers = response.json()
    handleAlphaAnswers(page , answers)
def handleAlphaAnswers(page : ft.Column , answers ):
    dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Result", size=26, color="blue"),  # Larger font for headline
            actions=[
                ft.TextButton("Okay", on_click=lambda e: page.page.close(dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
    dialog_content = ft.Column()
    if 'x' in answers:
        x = answers['x']
        text = ft.Text(size= 50 , value=f"X = {x}")
        dialog_content.controls.append(text)
    
    if 'y' in answers:
        y = answers['y']
        text = ft.Text(size= 50 , value=f"y = {y}")
        dialog_content.controls.append(text)
    if 'z' in answers:
        z = answers['z']
        text = ft.Text(size= 50 , value=f"z = {z}")
        dialog_content.controls.append(text)
    if 'x' not in answers:
        text = ft.Text(size = 50 , value="The system has NO solutions")
        dialog_content.controls.append(text)
    dialog.content = dialog_content
    page.page.open(dialog)
    page.page.update()

def send_to_backend_root(event , page : ft.Column):

    function_string = None
    oper_type : ft.Dropdown = get_child(page , "operation_dropdown_root")
    oper_type = int(oper_type.value)
    significant_digits = None
    epsilon = None
    iterations = None
    x0 = None
    x1 = None #Secant 
    xl = None
    xu = None

    error_message = None
    
    suboptions : ft.Column = get_child(page , "suboptions_root")

    
    # Works Correct
    try:
        function_string : ft.TextField = get_child(get_child(page, "function_input_col"), "funtion_input_string")
        function_string = function_string.value
        x = symbols('x')
        function_sympy = sympify(function_string)

    except:
        error_message = "Please enter a valid form of the function"

    # Works Correct
    significant_text : ft.TextField = get_child(get_child(suboptions , "significant_row_root"), "significant_digits_root")
    try:
        significant_digits = int(significant_text.value)
        significant_digits = int(np.clip(significant_digits, 1, 15))
    except:
        significant_digits = 15
    
    # Works Correct
    epsilon_text : ft.TextField = get_child(get_child(suboptions , "epsilon_row_root"), "epsilon_root")
    try:
        epsilon = abs(float(epsilon_text.value))
    except:
        epsilon = 0.00001

    # Works Correct
    iterations_text : ft.TextField = get_child(get_child(suboptions , "iterations_row_root"), "iterations_root")
    try:
        iterations = int(iterations_text.value)
        iterations = int(np.clip(iterations, 1, None))
    except:
        iterations = 50

    # Works Correct
    if oper_type in {1, 2}:
        try:
            xl : ft.TextField = get_child(get_child(suboptions , "initial_interval_row"), "xl") 
            xu : ft.TextField = get_child(get_child(suboptions , "initial_interval_row"), "xu")
            xl = float(xl.value)
            xu = float(xu.value)

        except:
            error_message = "Please only enter numerals"

    # Works Correct
    elif oper_type in {3, 4, 5, 6}:

        try:
            x0 : ft.TextField = get_child(get_child(suboptions , "initial_x_row"), "x0")
            x0 = float(x0.value)

            if oper_type == 6:
                x1 : ft.TextField = get_child(get_child(suboptions , "initial_x_row"), "x-1")
                x1 = float(x1.value)

        except: 
            error_message = "Please only enter numerals"          
        

    if error_message:
        # Create a Snackbar with the error message
        snack_bar = ft.SnackBar(content=ft.Text(error_message, color="black"))
        
        page.page.overlay.append(snack_bar)

        snack_bar.open = True
        
        page.page.update()
        # Update the page to reflect the change
    
        return


    data = {
        "function" : function_string,
        "operation" : oper_type,
        "significant_digits" : significant_digits,
        "epsilon" : epsilon,
        "max_its" : iterations,
        "x0" : x0,
        "x1" : x1,
        "xl" : xl,
        "xu" : xu,
    }

    print(data)

    response = post("http://127.0.0.1:5000/roots" , json=data)
    answer = response.json()
    if "result" in answer:
        result = answer["result"]

    elif "error" in answer:
        result = answer["error"]

    # answer = {
    #     # 'root' : 3.2485,
    #     'root' : -0.00475896,
    #     'iterations' : 43,
    #     'relative_error' : 0.000006,
    #     'significant_figures' : 9,
    #     'time_taken' : 0.6,
    #     # 'error' : None,
    # }
    
    print(answer)
    handleAnswerRoot(page , result)


def handleAnswerRoot(page : ft.Column, answer):

    suboptions = get_child(page , "suboptions_root")
    significant_digits = None
    significant_text : ft.TextField = get_child(get_child(suboptions , "significant_row_root"), "significant_digits_root")
    try:
        significant_digits = int(significant_text.value)
        significant_digits = int(np.clip(significant_digits, 1, 15))
    except:
        significant_digits = 15

    dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Result", size=26, color="blue"),  # Larger font for headline
            actions=[
                ft.TextButton("Okay", on_click=lambda e: page.page.close(dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
    )

    dialog_content = ft.Column(key="dialog_content")

    # A Solve button to display the approximate root if exists, 
    # number of iterations , 
    # approximate relative error , 
    # number of correct significant figures, and the 
    # execution time.

    
    if 'root' in answer:
        result_text = ft.Text(value=f"Approximate Root Result: {answer['root']:.{significant_digits}g}",size=24 , color="blue")
        dialog_content.controls.append(result_text)

    if 'iterations' in answer:
        iterations = answer['iterations']
        text = ft.Text(size=24 , value=f"Number of iterations taken = {iterations}")
        dialog_content.controls.append(text)

    if "relative_error" in answer:
        eps_a = answer['relative_error']
        text = ft.Text(size=24 , value=f"Approximate relative error = {eps_a}")
        dialog_content.controls.append(text)

    if "significant_figures" in answer:
        correct_sfs = answer['significant_figures']
        text = ft.Text(size=24 , value=f"Number of correct significant figures = {correct_sfs}")
        dialog_content.controls.append(text)

    if 'time_taken' in answer:
        time  = answer['time_taken']
        text = ft.Text(size=24 , value=f"Time taken = {time}")
        dialog_content.controls.append(text)

    if "error" in answer:
        error = answer["error"]
        error_text = ft.Text(value=f"Error: {error}", size=24, color="red")
        dialog_content.controls.clear()
        dialog_content.controls.append(error_text)

    dialog.content = dialog_content
    page.page.open(dialog)
    page.page.update()

def start_webview():
    threading.current_thread().name = "MainThread"
    webview.create_window("Plotly Chart", "http://localhost:8050", width=800, height=600)
    webview.start()

def plot_function(event, page : ft.Column):


    oper_type : ft.Dropdown = get_child(page , "operation_dropdown_root")
    oper_type = int(oper_type.value)

    function_string : ft.TextField = get_child(get_child(page, "function_input_col"), "funtion_input_string")
    function_string = function_string.value

    x1 = get_child(get_child(page, "graph_row"), "graph_input_1")
    x2 = get_child(get_child(page, "graph_row"), "graph_input_2")

    try:
        x1 = round(float(x1.value))
        x2 = round(float(x2.value))
    except:
        print("Graph range exception")

    
    dash_thread = threading.Thread(target=create_plot, args=(function_string, x1, x2, oper_type), daemon=True)
    dash_thread.start()
    # Start WebView
    threading.Thread(target=start_webview).start()

    # plot_file, error = create_plot(function_string, x1, x2, oper_type)
    # if plot_file:
    #     # Open the saved graph in the default web browser
    #     webbrowser.open(plot_file)
    # else:
    #     # Show error message
    #     page.snack_bar = ft.SnackBar(ft.Text(f"Error: {error}"))
    #     page.snack_bar.open = True
    #     page.update()


def create_plot(function_string, x1, x2, oper_type):
    try:
        print("About to run dash")
        app = dash.Dash(__name__)

        x = symbols('x')
        
        func = sympify(function_string)
        func_num = lambdify(x, func, modules=["numpy"])
        
        resolution = 100  # Points per unit
        num_points = int(abs(x2 - x1) * resolution)
        
        # Generate x values and calculate y values
        x_vals = np.linspace(x1, x2, max(num_points, 2))
        # x_vals = np.linspace(50, 50)
        y_vals = func_num(x_vals)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=f'f(x) = {function_string}'))
        
        # Add y = x if operation is fixed-point
        if oper_type == 3:
            fig.add_trace(go.Scatter(x=x_vals, y=x_vals, mode='lines', name='y = x', line=dict(dash='dash')))
                
        fig.update_layout(
            title="Graph of the Function",
            xaxis=dict(
                title="x",
                zeroline=True,
                zerolinecolor="black",
                showline=True,
                linecolor="black",
                mirror=True
            ),
            yaxis=dict(
                title="f(x)",
                zeroline=True,
                zerolinecolor="black",
                showline=True,
                linecolor="black",
                mirror=True
            ),
            template="plotly_white",
        )
        
        app.layout = html.Div(children=[
            html.H1("Dynamic Function Plot", style={"text-align": "center"}),
            dcc.Graph(figure=fig)  # Interactive Plotly chart
        ])

        app.run_server(debug=False, port=8050, use_reloader=False)
           
        # plot_file = "plot.html"
        # fig.write_html(plot_file)
        # return plot_file, None
    
    except Exception as e:
        return str(e)
