from turtle import onclick
import flet as ft
from functions import send_to_backend , get_child

def addCells(size, matrix):
    for i in range(size):
        row = ft.Row()
        for j in range(size+1):
            cell = ft.TextField(width=50 , height=50)
            row.controls.append(cell)
            if(j<size-1):
                text = ft.Text(value=f"x{j+1}")
                row.controls.append(text)
            elif(j==size-1):
                text1 = ft.Text(value=f"x{j+1}")
                text2 = ft.Text(value="=")
                row.controls.append(text1)
                row.controls.append(text2)
        matrix.controls.append(row)
def resize(event , page : ft.Column):
    update_suboptions(None , page)
    size_dropdown : ft.Dropdown = get_child(page , "size_dropdown")
    size = int(size_dropdown.value)
    matrix_container : ft.Column = get_child(page , "matrix_container")
    matrix_container.controls.clear()

    addCells(size , matrix_container)

    page.update()
def initialize_matrix(page : ft.Column):
    update_suboptions(None,page)
    matrix = get_child(page , "matrix_container")
    size = 2

    addCells(size , matrix)

    page.update()
def update_suboptions(event ,page :ft.Page ):
    operation = get_child(page , "operation_dropdown")
    suboptions = get_child(page , "suboptions")
    oper_type = int(operation.value)
    suboptions.controls.clear()
    significant_digits = ft.TextField(hint_text="Enter number of significant digits" , width=500 , key="significant_digits", value=4)
    if oper_type in {1,2}:
        suboptions.controls.append(significant_digits)
    elif oper_type in {3 , 4}:
        mode_select = ft.Dropdown(
            options=[
                ft.dropdown.Option("1" , "Iterative"),
                ft.dropdown.Option("2" , "Relative Error"),
            ],
            value="1",
            key="mode_select",width=500
        )
        criteria = ft.TextField(hint_text="Select Criteria" , key="criteria_text_field" , width=500)
        initial_guess_row = ft.Row(key="initial_guess_row")
        initial_guess_label = ft.Text(value="Initial Guess" , key="initial_guess_label")
        initial_guess_row.controls.append(initial_guess_label)
        size_dropdown : ft.Dropdown = get_child(page , "size_dropdown")
        size = int(size_dropdown.value)
        for i in range(size):
            field = ft.TextField(width=50, height=50)
            initial_guess_row.controls.append(field)
        suboptions.controls.append(initial_guess_row)
        suboptions.controls.append(mode_select)
        suboptions.controls.append(criteria)
        suboptions.controls.append(significant_digits)
    elif oper_type == 5:
        LU_sub_operations = ft.Dropdown(
            options=[
                ft.dropdown.Option("1" , "Doolittle Decomposition"),
                ft.dropdown.Option("2" , "Crout Decomposition"),
                ft.dropdown.Option("3" , "Cholesky Decomposition"),
            ],
            width= 500,value="1",key="LU_sub"
        )
        suboptions.controls.append(LU_sub_operations)
        suboptions.controls.append(significant_digits)
    suboptions.update()

def tab1():
    tab1 = ft.Column(key="Tab1")
    matrix_panel = ft.Column(key="matrix_container")
    size_dropdown = ft.Dropdown(
        options=
        [
            ft.dropdown.Option("2",2),
            ft.dropdown.Option("3",3),
            ft.dropdown.Option("4",4),
            ft.dropdown.Option("5",5),
            ft.dropdown.Option("6",6),
        ],
        key="size_dropdown",
        value="2",
        width=500,
        on_change= lambda e : resize(e , tab1)
    )
    tab1.controls.append(size_dropdown)
    tab1.controls.append(matrix_panel)
    
    operation = ft.Dropdown(
        options=[
            ft.dropdown.Option("1" , "Gauss Elimination"),
            ft.dropdown.Option("2" , "Gauss-Jordan Elimination"),
            ft.dropdown.Option("3" , "Jacobi"),
            ft.dropdown.Option("4" , "Gauss-Seidel"),
            ft.dropdown.Option("5" , "LU Decomposition"),
        ],
        value="1",
        width=500,
        key="operation_dropdown",
        on_change= lambda e : update_suboptions(e , tab1)
    )
    tab1.controls.append(operation)
    suboptions = ft.Column(key="suboptions")
    tab1.controls.append(suboptions)
    submit_button = ft.TextButton(
    text="Answer",
    key="submit_button",
    style=ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=4),
        side=ft.BorderSide(color="blue", width=2),
        ),
        on_click = lambda e : send_to_backend(e , tab1)
    )
    tab1.controls.append(submit_button)
    return tab1

def main(page : ft.Page):
    tabs = ft.Tabs(
        tabs=
        [
            ft.Tab(content=tab1(), text="Matrix Solver")
        ]
    )
    page.add(tabs)
    matrixTab = page.controls[0].tabs[0].content
    initialize_matrix(matrixTab)
    
ft.app(target=main)