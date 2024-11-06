import flet as ft

def main(page: ft.Page):
    # Create a Text widget
    text = ft.Text(value="Hello, World!")

    # Create a Button widget
    def button_click(e):
        text.value = "Hello, Flet!"
        page.update()

    button = ft.ElevatedButton("Click Me", on_click=button_click)

    # Add widgets to the page
    page.add(text, button)

# Run the app
ft.app(target=main)
