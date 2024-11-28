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