import flet as ft
import numpy as np
from requests import post
def get_child(controls , key):
    child = [control for control in controls.controls if control.key == key][0]
    return child
def send_to_backend(event , page : ft.Column):
    error_message = None
    x0 = []
    criteria = None
    mode = None
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
    significant_text : ft.TextField = get_child(suboptions , "significant_digits")
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
            mode_select : ft.Dropdown = get_child(suboptions , "mode_select")
            mode = int(mode_select.value)
            criteria_text : ft.TextField = get_child(suboptions , "criteria_text_field")
            criteria = float(criteria_text.value)
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
        "epsilon" : criteria,
        "its" : criteria,
        "mode" : mode,
        "significant_digits" : significant_digits
    }
    response = post("http://127.0.0.1:5000" , json=data)
    answers = response.json()
    handleAnswer(page , answers)

def handleAnswer(page : ft.Column , answer):
    significant_text = get_child(get_child(page, "suboptions") , "significant_digits")
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
            label = ft.Text(value=f"{i:.{significant_digits}f}")
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
                text = ft.Text(value=f"{i:.{significant_digits}f}")
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
    dialog.content = dialog_content
    page.page.open(dialog)
    page.page.update()



