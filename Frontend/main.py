import flet as ft
import numpy as np

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
    if oper == "3":
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

    # Update the container to reflect changes
    sub_dropdown_container.update()

# Function to collect matrix and dropdown data
def send_to_backend(page: ft.Page):
    error_message = None
    matrix_data = []
    operator = page.controls[2].controls[0].value  # Operation Type
    sub_operator = None
    x0 : int
    try:
        x0 = int(page.controls[4].value)
    except:
        x0 = 4
    try:
        operator = int(operator)
    except ValueError:
        error_message = "Please Select a Valid Operation Type"
    
    if operator == 3:  # Check for LU Decomposition subcategory
        sub_dropdown_container = page.controls[3]
        if sub_dropdown_container.controls:
            sub_operator = sub_dropdown_container.controls[0].value
            if not sub_operator:
                error_message = "Please Select an LU Decomposition Method"
    
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
    
    print(matrix_data)
    print(f"Selected Operation: {operator}")
    if operator == 3:
        print(f"Selected LU Sub-Method: {sub_operator}")
    print(f"Number of significant digits: {x0}")

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
            ft.dropdown.Option("3", "LU Decomposition")
        ],
        label="Select Operation Type",
        width=500,
        on_change=lambda e: set_subCategories(e, operation_dropdown, sub_dropdown_container),
    )

    page.add(ft.Row([operation_dropdown]))
    page.add(sub_dropdown_container)
    text = ft.TextField(hint_text="Enter Number of Significant digits" , width=500 , value="4")
    page.add(text)
    button = ft.TextButton(
        text="Answer",
        on_click=lambda e: send_to_backend(page),
        style=ft.ButtonStyle(bgcolor="red"),
    )

    page.add(button)
    print(page.controls)
    # Initialize matrix
    update_matrix(None, panel, matrix_container)

# Run the app
ft.app(main)
