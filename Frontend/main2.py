import flet as ft
import numpy as np
from requests import post


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


# Tab 1: Matrix Solver
def matrix_solver_tab(page: ft.Page):
    # Update matrix when size changes
    def update_matrix(event, size_dropdown, matrix_container):
        selected_size = int(size_dropdown.value)
        matrix = create_matrix_with_labels(selected_size)
        # Clear the existing matrix controls
        matrix_container.controls.clear()

        # Add the new matrix to the matrix container
        for row in matrix:
            matrix_container.controls.append(ft.Row(row, alignment=ft.MainAxisAlignment.START))

        # Update the container to reflect changes
        matrix_container.update()

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
        on_change=lambda e: update_matrix(e, size_dropdown, matrix_container),
    )

    # Matrix container
    matrix_container = ft.Column()

    # Submit button
    submit_button = ft.ElevatedButton(
        text="Submit",
        # on_click=lambda e: send_to_backend(page, matrix_container),
    )

    # Return the complete layout
    layout = ft.Column(
        [
            size_dropdown,
            matrix_container,
            submit_button,
        ],
        spacing=20,
        expand=True,
    )

    # Populate the initial matrix once the container is part of the layout
    update_matrix(None, size_dropdown, matrix_container)

    return layout



# Tab 2: Linear Algebra Tools
def linear_algebra_tools_tab():
    return ft.Column(
        [
            ft.Text("Linear Algebra Tools", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("This tab will include various linear algebra operations."),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=20,
    )


# Tab 3: Settings
def settings_tab():
    return ft.Column(
        [
            ft.Text("Settings", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("This tab allows you to configure app settings."),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=20,
    )


# Main App
def main(page: ft.Page):
    page.title = "System of Linear Equations Solver"
    page.horizontal_alignment = ft.MainAxisAlignment.START
    page.vertical_alignment = ft.CrossAxisAlignment.START

    # Tabs
    tabs = ft.Tabs(
        [
            ft.Tab(
                text="Matrix Solver",
                content=matrix_solver_tab(page),
            ),
            ft.Tab(
                text="Linear Algebra Tools",
                content=linear_algebra_tools_tab(),
            ),
            ft.Tab(
                text="Settings",
                content=settings_tab(),
            ),
        ]
    )

    # Add tabs to page
    page.add(tabs)


ft.app(target=main)
