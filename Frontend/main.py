from ast import mod
import ast
from os import error
from turtle import width
import flet as ft
import numpy as np
from requests import post
from sklearn import model_selection
from torch import mode

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
def set_subCategories(e, operation_dropdown, sub_dropdown_container):
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
        
        
    
    # Update the container to reflect changes
    sub_dropdown_container.update()
# Function to collect matrix and dropdown data
def send_to_backend(page: ft.Page, significant: ft.TextField):
    error_message = None
    mode_selection = None
    matrix_data = []
    operator = page.controls[2].controls[0].value  # Operation Type
    x0: int
    value_of_mode = None
    mode = None

    try:
        x0 = int(significant.value)
        x0 = int(np.clip(x0, 1, 15))
    except:
        x0 = 4

    try:
        operator = int(operator)
    except:
        error_message = "Please Select a Valid Operation Type"

    if operator == 1:
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
            mode_selection = page.controls[3].controls
            mode = int(mode_selection[0].value)
            value_of_mode = float(mode_selection[2].value)
        except:
            error_message = "Please select Iteration method"

    # Get the matrix size
    dropdown = page.controls[0].controls[0]
    size = int(dropdown.value)

    # Access the matrix rows
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
        # Show an error message using a Snackbar
        page.snack_bar = ft.SnackBar(content=ft.Text(error_message, color="black"))
        page.snack_bar.open = True
        page.update()
        return

    # Convert matrix data to numpy array and reshape
    matrix_data = np.array(matrix_data, dtype=float)
    matrix_data = np.reshape(matrix_data, (size, size + 1))
    data_sent = {
        "matrix": matrix_data.tolist(),
        "x0": x0,
        "epsilon": value_of_mode,
        "its": value_of_mode,
        "mode": mode,
        "operation": operator
    }
    # print(f" send the data : {data_sent}")
    response = post("http://127.0.0.1:5000", json=data_sent)
    
    # Assuming the response.json() returns a dictionary with the result.
    response_data = response.json()
    print(response_data)

    # Now handle the response depending on the operation type
    if operator in {1, 2, 5, 6, 7}:
        result_message = None
        if 'x' in response_data:
            np.set_printoptions(precision=x0 , suppress= True)
            x = response_data.get('x')
            x = np.array(x)
            if (np.any(np.isnan(x))):
                result_message = f"Error was found during solution"
            else: 
                result_message = "x:\n" + str(x)  # Add "x" before the result matrix
        else :
            result_message = f"Error was found during solution"

        if 'result' in response_data:
            result_message += f"\n\nResult Matrix:\n{np.array2string(np.array(response_data['result']))}"
            if 'L' in response_data:
                result_message += f"\n\nL Matrix: {np.array2string(np.array(response_data['L']))}"
            result_message += f"\n\nTime Taken: {response_data['time_taken']}"
        
        digDialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Result", size=20, color="blue"),  # Larger font for headline
            content=ft.Text(result_message, size=16),  # Larger font for content
            actions=[
                ft.TextButton("Okay", on_click=lambda e: page.close(digDialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.open(digDialog)
        page.update()

    elif operator in {3, 4}:
        result_message = "x:\n" + str(response_data.get('x', ''))  # Add "x" before the result matrix

        if 'x' in response_data:
            result_message += f"\n\nSolution Matrix: {np.array2string(np.array(response_data['x']))}"
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
            title=ft.Text("Error", size=20, color="red"),  # Larger font for error headline
            content=ft.Text(f"An error occurred: {error_message}", size=16),  # Larger font for error content
            actions=[
                ft.TextButton("Okay", on_click=lambda e: page.close(digDialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.open(digDialog)
        page.update()


def update_matrix(event, panel, matrix_container):
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
        mode_container.controls.clear()
        mode_container.controls.append(retained_control)
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
            ft.dropdown.Option("3", 3),
            ft.dropdown.Option("4", 4),
            ft.dropdown.Option("5", 5),
            ft.dropdown.Option("6", 6),
        ],
        value="3",
        width=500,
    )

    matrix_container = ft.Column()

    panel = ft.Column(
        [size_dropdown],
        alignment=ft.MainAxisAlignment.START,
    )

    size_dropdown.on_change = lambda e: update_matrix(e, panel, matrix_container)

    page.add(panel)
    page.add(matrix_container)

    # Operation Type and its subcategories
    sub_dropdown_container = ft.Column()
    operation_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("1", "Gauss Elimination"),
            ft.dropdown.Option("2", "Gauss-Jordan Elimination"),
            ft.dropdown.Option("5", "LU Decomposition"),
            ft.dropdown.Option("4" ,"Gauss-Seidel"),
            ft.dropdown.Option("3" ,"Jacobi")
        ],
        label="Select Operation Type",
        width=500,
        on_change=lambda e: set_subCategories(e, operation_dropdown, sub_dropdown_container),
    )

    page.add(ft.Row([operation_dropdown]))
    page.add(sub_dropdown_container)
    label  = ft.Text(value="Significant Digits")
    page.add(label)
    siginficantText = ft.TextField(hint_text="Enter Number of Significant digits" , width=500 , value="4")
    page.add(siginficantText)
    button = ft.TextButton(
        text="Answer",
        on_click=lambda e: send_to_backend(page, siginficantText),
        style=ft.ButtonStyle(bgcolor="red"),
    )
    page.add(button)
    # Initialize matrix
    update_matrix(None, panel, matrix_container)

# Run the app
ft.app(main)
