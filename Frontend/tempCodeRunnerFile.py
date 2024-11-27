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
    print(f" send the data : {data_sent}")
    response = post("http://127.0.0.1:5000", json=data_sent)
    
    # Assuming the response.json() returns a dictionary with the result.
    response_data = response.json()

    result_message = response_data
    print(response_data)

    # Now handle the response depending on the operation type
    if operator in {1, 2, 5, 6, 7}:
        if 'result' in response_data:
            result_message = f"Result: {response_data['result']}"
            if 'L' in response_data:
                result_message += f"\nL Matrix: {response_data['L']}"
            elif 'x' in response_data:
                result_message += f"\nx: {response_data['x']}"
            result_message += f"\nTime Taken: {response_data['time_taken']}"
        
        digDialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Result"),
            content=ft.Text(result_message),
            actions=[
                ft.TextButton("Okay", on_click=lambda e: page.close(digDialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.open(digDialog)
        page.update()

    elif operator in {3, 4}:
        if 'x' in response_data:
            result_message = f"Solution: {response_data['x']}"
            result_message += f"\nTime Taken: {response_data['time_taken']}"
        
        digDialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Solution"),
            content=ft.Text(result_message),
            actions=[
                ft.TextButton("Okay", on_click=lambda e: page.close(digDialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.open(digDialog)
        page.update()

    else:
        # In case of an error
        error_message = response_data.get('error', 'Unknown error')
        digDialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Error"),
            content=ft.Text(f"An error occurred: {error_message}"),
            actions=[
                ft.TextButton("Okay", on_click=lambda e: page.close(digDialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.open(digDialog)
        page.update()