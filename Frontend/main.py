from ast import mod
import ast
import glob
from operator import sub
from os import error
from turtle import width
from flask import request
import flet as ft
from matplotlib.streamplot import OutOfBounds
import numpy as np
from requests import post
from sklearn import model_selection
from torch import mode, res\

# Function to create matrix text boxes with variable labels
def create_matrix_with_labels(size: int):
    size = int(size)
    matrix = []
    for i in range(size):
        row = []
        for j in range(size + 1):  # To include the equal sign column
            # Create a text field
            cell = ft.TextField(width=40, text_align=ft.TextAlign.RIGHT, focused_border_color="red")

            # Add label (except for the last cell in each row)
            if j < size:
                label = ft.Text(f"x{j + 1}", size=12, color="red")
                row.append(ft.Row([cell, label], alignment=ft.MainAxisAlignment.START))
            else:
                label = ft.Text("=", color="white", size=12)
                row.append(ft.Row([label, cell], alignment=ft.MainAxisAlignment.START))

        matrix.append(row)
    return matrix

# Function to handle subcategory dropdown
def set_subCategories(e, operation_dropdown, sub_dropdown_container, size , page : ft.Page):
    
    oper = operation_dropdown.value

    # Clear previous sub-dropdown if it exists
    sub_dropdown_container.controls.clear()
    # If "LU Decomposition" (value = "3") is selected, add a subcategory dropdown

    if oper == "5":
        newDrop = ft.Dropdown(
            options=[
                ft.dropdown.Option(key="1", text="LU Doolittle Decomposition"),
                ft.dropdown.Option(key="2", text="LU Crout Decomposition"),
                ft.dropdown.Option(key="3", text="LU Cholesky Decomposition"),
            ],
            label="Select LU Method",
            width=500
        )
        sub_dropdown_container.controls.append(newDrop)
    elif oper == "3" or oper == "4":
        row = ft.Row()
        label = ft.Text("Select initial Guess : " , size=22)
        row.controls.append(label)
        for i in range(size):
            cell = ft.TextField(width=40, text_align=ft.TextAlign.RIGHT, focused_border_color="red")
            row.controls.append(cell)
        sub_dropdown_container.controls.append(row)
        newDrop = ft.Dropdown(
            options=
            [
                ft.dropdown.Option("1" , "Iteration based"),
                ft.dropdown.Option("2" , "Relative Error based")
            ],
            label= "Select Iteration mode",
            width=500,
            on_change= lambda e : set_mode(e , sub_dropdown_container , newDrop)
        )
        sub_dropdown_container.controls.append(newDrop)
    elif oper == "0":
        page.controls.pop(-2)
        page.controls.pop(-3)
        
    
    # Update the container to reflect changes
    sub_dropdown_container.update()
# Function to collect matrix and dropdown data
def send_to_backend(page: ft.Page, significant: ft.TextField):
    error_message = None
    mode_selection = None
    matrix_data = []
    operator = page.controls[2].controls[0].value  # Operation Type
    x0 = []
    significant_digits : int
    value_of_mode = None
    mode = None
    try:
        significant_digits = int(significant.value)
        significant_digits = int(np.clip(significant_digits, 1, 15))
    except:
        significant_digits = 4

    try:
        operator = int(operator)
    except:
        error_message = "Please Select a Valid Operation Type"
    if operator == 0:
        for row in page.controls[1].controls:  # Accessing the matrix rows
            rowdata = []
            for col in row.controls:
                if isinstance(col, ft.Row):
                    for cell in col.controls:
                        if isinstance(cell, ft.TextField):
                            try:
                                value = str(cell.value)[0]
                                rowdata.append(value)
                            except :
                                error_message = "Please enter valid Characters in all matrix cells."
            matrix_data.append(rowdata)
        if error_message:
            # Create a Snackbar with the error message
            snack_bar = ft.SnackBar(content=ft.Text(error_message, color="black"))

            # Append it to the page's overlay
            page.overlay.append(snack_bar)

            # Open the Snackbar
            snack_bar.open = True

            # Update the page to reflect the change
            page.update()

            return
        json = {"matrix" : matrix_data}
        print(json)
        response = post("http://127.0.0.1:5000/alphabetical" , json=json)
        print(response.json())
        result_message = ""
        i = 1
        if "error" not in response.json():
            for i,j in response.json().items():
                result_message += f"{i} = {j} \n"
        else:
            result_message+=f"Error : {response.json().get("error")}"
        digDialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Result", size=26, color="blue"),  # Larger font for headline
            content=ft.Text(result_message, size=22),  # Larger font for content
            actions=[
                ft.TextButton("Okay", on_click=lambda e: page.close(digDialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.open(digDialog)
        page.update()
        return
    elif operator == 1:
        operator = 1
    elif operator == 2:
        operator = 2
    elif operator == 5:  # Check for LU Decomposition subcategory
        sub_dropdown_container = page.controls[3]
        if sub_dropdown_container.controls:
            if sub_dropdown_container.controls[0].value is not None:
                operator = int(sub_dropdown_container.controls[0].value) + 4
            else:
                error_message = "Please select LU sub-operation"
    elif operator == 4 or operator == 3:
        try:
            for i in range(1,len(page.controls[3].controls[0].controls)):
                cell = page.controls[3].controls[0].controls[i]
                x0.append(float(cell.value))
        except:
            error_message = "Please enter initial Guess"
        try:
            # mode_selection = page.controls[3].controls
            mode = int(page.controls[3].controls[1].value)
            value_of_mode = float(page.controls[3].controls[3].value)
        except:
            error_message = "Please select Iteration method"

    # Get the matrix size
    dropdown = page.controls[0].controls[0]
    size = int(dropdown.value)

    # Access the matrix rows
    if operator != 0:
        for row in page.controls[1].controls:  # Accessing the matrix rows
            for col in row.controls:
                if isinstance(col, ft.Row):
                    for cell in col.controls:
                        if isinstance(cell, ft.TextField):
                            try:
                                value = float(cell.value)
                                matrix_data.append(value)
                            except ValueError:
                                error_message = "Please enter valid numbers in all matrix cells."
                                matrix_data.append(0.0)
    
    if error_message:
        # Create a Snackbar with the error message
        snack_bar = ft.SnackBar(content=ft.Text(error_message, color="black"))
        
        # Append it to the page's overlay
        page.overlay.append(snack_bar)
        
        # Open the Snackbar
        snack_bar.open = True
        
        # Update the page to reflect the change
        page.update()
    
        return

    # Convert matrix data to numpy array and reshape
    matrix_data = np.array(matrix_data, dtype=float)
    matrix_data = np.reshape(matrix_data, (size, size + 1))
    data_sent = {
        "matrix": matrix_data.tolist(),
        "x0": x0,
        "significant_digits" : significant_digits,
        "epsilon": value_of_mode,
        "its": value_of_mode,
        "mode": mode,
        "operation": operator
    }
    # print(f"{data_sent} is the data sent")
    # print(f" send the data : {data_sent}")
    response = post("http://127.0.0.1:5000", json=data_sent)
    
    # Assuming the response.json() returns a dictionary with the result.
    response_data = response.json()
    # print(f"{response_data} is the resposne received")
    # Now handle the response depending on the operation type
    if operator in {1, 2, 5, 6, 7}:
        result_message = None
        if 'error' in response_data:
            result_message = f"Error Found : {response_data.get("error")}"
        if 'x' in response_data:
            np.set_printoptions(precision=significant_digits, suppress= True)
            x = response_data.get('x')
            x = np.array(x)
            if (np.any(np.isnan(x))):
                result_message = f"Error was found during solution"
            else: 
                result_message = "x:\n" + str(x)  # Add "x" before the result matrix
        if 'result' in response_data:
            result_message += f"\n\nResult Matrix:\n{np.array2string(np.array(response_data.get('result')))}"
        if 'L' in response_data:
            result_message += f"\n\nL Matrix:\n{np.array2string(np.array(response_data.get('L')))}"
        if "error" not in response_data:
            result_message += f"\n\nTime Taken: {response_data.get('time_taken')}"
        
        digDialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Result", size=26, color="blue"),  # Larger font for headline
            content=ft.Text(result_message, size=22),  # Larger font for content
            actions=[
                ft.TextButton("Okay", on_click=lambda e: page.close(digDialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.open(digDialog)
        page.update()

    elif operator in {3, 4}:
        np.set_printoptions(precision=significant_digits , suppress= True)
        if 'x' in response_data:
            np.set_printoptions(precision=significant_digits , suppress= True)
            x = response_data.get('x')
            x = np.array(x)
            if (np.any(np.isnan(x))):
                result_message = f"Error was found during solution"
            else: 
                result_message = "x:\n" + str(x)  # Add "x" before the result matrix
        else:
            result_message = f"Error was found during solution"
        if 'iterations' in response_data:
            iterations = response_data.get("iterations")
            result_message += f"\n\n iterations taken = {iterations}"
        if "error" not in response_data:
            result_message += f"\n\nTime Taken: {response_data['time_taken']}"
        digDialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Solution", size=26, color="blue"),  # Larger font for headline
            content=ft.Text(result_message, size=22),  # Larger font for content
            actions=[
                ft.TextButton("Okay", on_click=lambda e: page.close(digDialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(digDialog)
        page.update()

    else:
        # In case of an error
        error_message = response_data.get('error', 'Unknown error')
        digDialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Error", size=26, color="red"),  # Larger font for error headline
            content=ft.Text(f"An error occurred: {error_message}", size=22),  # Larger font for error content
            actions=[
                ft.TextButton("Okay", on_click=lambda e: page.close(digDialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.open(digDialog)
        page.update()


def update_matrix(event, panel, matrix_container, dropdown_container):
    try:
        controls = dropdown_container.controls[0].controls
        retained = controls[0]
        controls.clear()
        controls.append(retained)
        for i in range(int(panel.controls[0].value)):
            cell = ft.TextField(width=40, text_align=ft.TextAlign.RIGHT, focused_border_color="red")
            controls.append(cell)
            dropdown_container.update()
    except:
        pass
    selected_size = int(panel.controls[0].value)
    matrix = create_matrix_with_labels(selected_size)
    # Clear the existing matrix controls
    matrix_container.controls.clear()

    # Add the new matrix to the matrix container
    for row in matrix:
        matrix_container.controls.append(ft.Row(row, alignment=ft.MainAxisAlignment.START))

    # Update the container to reflect changes
    matrix_container.update()
def set_mode(e , mode_container : ft.Column , dropdown : ft.dropdown):
    try : 
        retained_control = mode_container.controls[0]
        retained_control2 = mode_container.controls[1]
        mode_container.controls.clear()
        mode_container.controls.append(retained_control)
        mode_container.controls.append(retained_control2)
    except :
        pass
    mode = int(dropdown.value)
    label , text = None , None
    if mode == 1 :
        label = ft.Text("Number of iterations")
        text = ft.TextField(hint_text="Enter number of iterations" , width=500)
    elif mode == 2:
        label = ft.Text("Error Criteria")
        text = ft.TextField(hint_text="Enter Error Criteria" , width=500)
    mode_container.controls.append(label)
    mode_container.controls.append(text)
    mode_container.update()
def main(page: ft.Page):
    page.title = "System of Linear Equations"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.START

    # Dropdown to select the size of the matrix
    size_dropdown = ft.Dropdown(
        label="Select matrix size",
        options=[
            ft.dropdown.Option("2", 2),
            ft.dropdown.Option("3", 3),
            ft.dropdown.Option("4", 4),
            ft.dropdown.Option("5", 5),
            ft.dropdown.Option("6", 6),
        ],
        value="2",
        width=500,
    )

    matrix_container = ft.Column()

    panel = ft.Column(
        [size_dropdown],
        alignment=ft.MainAxisAlignment.START,
    )

    

    page.add(panel)
    page.add(matrix_container)

    # Operation Type and its subcategories
    sub_dropdown_container = ft.Column()
    size_dropdown.on_change = lambda e: update_matrix(e, panel, matrix_container, sub_dropdown_container)
    operation_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("0" ,"Alphabetic Solution"),
            ft.dropdown.Option("1", "Gauss Elimination"),
            ft.dropdown.Option("2", "Gauss-Jordan Elimination"),
            ft.dropdown.Option("5", "LU Decomposition"),
            ft.dropdown.Option("4" ,"Gauss-Seidel"),
            ft.dropdown.Option("3" ,"Jacobi")
        ],
        label="Select Operation Type",
        width=500,
        on_change=lambda e: set_subCategories(e, operation_dropdown, sub_dropdown_container, int(size_dropdown.value) , page),
    )

    page.add(ft.Row([operation_dropdown]))
    page.add(sub_dropdown_container)
    label  = ft.Text(value="Significant Digits")
    siginficantText = ft.TextField(hint_text="Enter Number of Significant digits" , width=500 , value="4")
    # if operation_dropdown.value is not None and int(operation_dropdown.value) != 0:
    page.add(label)
    page.add(siginficantText)
    button = ft.TextButton(
        text="Answer",
        on_click=lambda e: send_to_backend(page, siginficantText),
        style=ft.ButtonStyle(bgcolor="red"),
    )
    page.add(button)
    # Initialize matrix
    update_matrix(None, panel, matrix_container, sub_dropdown_container)

# Run the app
ft.app(main)