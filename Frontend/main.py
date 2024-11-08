import flet as ft
import numpy as np

# Function to create matrix text boxes with variable labels
def create_matrix_with_labels(size: int):
    size = int(size)
    matrix = []
    variable_count = 1  # To generate labels like x1, x2, ...
    
    for i in range(size):
        row = []
        variable_count = 1
        for j in range(size + 1):  # To include the equal sign column
            # Create a text field
            cell = ft.TextField(width=40, text_align=ft.TextAlign.RIGHT, focused_border_color="red"  )
            
            # Add label (except for the last cell in each row)
            if j < size:
                label = ft.Text(f"x{variable_count}", size=12, color="red")
                row.append(ft.Row([cell, label], alignment=ft.MainAxisAlignment.START))
                variable_count += 1
            else:
                label = ft.Text("=", color="white", size=12)
                row.append(ft.Row([label, cell], alignment=ft.MainAxisAlignment.START))  # Last cell in the row (equal sign)

        matrix.append(row)
    return matrix

def main(page: ft.Page):
    page.title = "System of Linear Equations"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.START

    # Panel at top-left with a dropdown to select the size of the matrix
    panel = ft.Column(
        [
            # Dropdown to select the size of the matrix
            ft.Dropdown(
                label="Select matrix size",
                options=[
                    ft.dropdown.Option("3", 3),
                    ft.dropdown.Option("4", 4),
                    ft.dropdown.Option("5", 5),
                    ft.dropdown.Option("6", 6),
                ],
                value="3",  # Default value set to 3
                on_change=lambda e: update_matrix(e, page, panel),
                width=500
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
    )

    # Add the panel to the page
    page.add(panel)

    # IconButton to collect matrix data
    button = ft.TextButton(text="Answer",on_click=lambda e: send_to_backend(page) , style=ft.ButtonStyle(bgcolor="red"))
    page.add(button)
    
    # Example TextField and Dropdown below the matrix
    text = ft.Row(
        [ft.Text(value="Significant digits" , italic=True , size=32),
         
        ft.TextField(text_style=ft.TextStyle.italic, hint_text="Please Pick a Significant digit Count", width=500)]
    )
    page.add(text)
    
    dropdown = ft.Row(
        [
            ft.Text(value="Select Operation Type" , size=32 , italic= True),
            ft.Dropdown(
        options=[
            ft.dropdown.Option("1", "Gauss Elimination"),
            ft.dropdown.Option("2","Gauss-Jordan Elimination")
            ] 
            , width=500 , value="1")
        ]
    )
    page.add(dropdown)

    # Initialize the matrix with the default 3x3 size and add it to the panel
    update_matrix(None, page, panel)

def send_to_backend(page: ft.Page):
    matrix_data = []
    size = int(page.controls[0].controls[0].value)  # Get selected matrix size from dropdown
    error_message = None  # Variable to store error message if any

    for row in page.controls[0].controls[1:]:  # Skip the first control (dropdown)
        for col in row.controls:
            if isinstance(col, ft.Row):
                for cell in col.controls:
                    if isinstance(cell, ft.TextField):
                        try:
                            # Try to convert the value to float
                            value = float(cell.value)
                            matrix_data.append(value)
                        except ValueError:
                            # If conversion fails, set the error message
                            error_message = "Please enter valid numbers in all matrix cells."
                            matrix_data.append(0.0)  # Optionally append 0.0 as a fallback

    if error_message:
        # Show an error message using a Snackbar
        page.snack_bar = ft.SnackBar(content=ft.Text(error_message, color="black"))
        page.snack_bar.open = True
        page.update()  # Refresh the page to display the snackbar
        return  # Exit the function if there is an error

# Function to update the matrix dynamically when dropdown value changes
def update_matrix(event, page, panel):
    # Get the selected size (as an integer)
    selected_size = int(page.controls[0].controls[0].value)  # Convert to integer

    # Create matrix with labels based on selected size
    matrix = create_matrix_with_labels(selected_size)

    # Clear the existing matrix controls and keep only the dropdown
    panel.controls = [panel.controls[0]]  # Keep only the dropdown (first control)

    # Add the new matrix to the panel
    for row in matrix:
        panel.controls.append(ft.Row(row, alignment=ft.MainAxisAlignment.START))

    # Update the page to reflect changes
    page.update()

# Run the app
ft.app(main)
