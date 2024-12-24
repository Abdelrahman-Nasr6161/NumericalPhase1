import flet as ft
import dash
from dash import dcc, html
import plotly.graph_objects as go
import threading
import webview
import numpy as np

# Function to start the Dash app
def start_dash(custom_function):
    app = dash.Dash(__name__)

    # Generate x and y values based on the custom function
    x = np.linspace(-10, 10, 100)  # x values from -10 to 10
    y = custom_function(x)  # Apply the custom function

    # Create the Plotly chart
    fig = go.Figure(data=[
        go.Scatter(x=x, y=y, mode="lines", name="Custom Function")
    ])
    fig.update_layout(title="Custom Function Plot")

    # Layout of the Dash app
    app.layout = html.Div(children=[
        html.H1("Dynamic Function Plot", style={"text-align": "center"}),
        dcc.Graph(figure=fig)  # Interactive Plotly chart
    ])

    # Run the Dash app
    app.run_server(debug=False, port=8050, use_reloader=False)

# Function to start the WebView
def start_webview():
    threading.current_thread().name = "MainThread"
    webview.create_window("Plotly Chart", "http://localhost:8050", width=800, height=600)
    webview.start()

# Function to start the Flet app
def start_flet():
    def main(page: ft.Page):
        page.title = "Flet with Custom Plotly Chart"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER

        # Function to create the graph based on user input
        def create_graph(e):
            # Get the function string from the text field
            func_str = function_input.value

            try:
                # Convert the string to a Python function
                custom_function = eval(f"lambda x: {func_str}")

                # Start the Dash app with the custom function in a thread
                dash_thread = threading.Thread(target=start_dash, args=(custom_function,), daemon=True)
                dash_thread.start()

                # Start WebView
                threading.Thread(target=start_webview).start()

            except Exception as ex:
                result.value = f"Error in function: {str(ex)}"
                page.update()

        # Text field for function input
        function_input = ft.TextField(label="Enter a function (e.g., 'x**2', 'np.sin(x)')", expand=True)
        
        # Label to show errors or messages
        result = ft.Text()

        # Button to generate the graph
        generate_button = ft.ElevatedButton("Generate Graph", on_click=create_graph)

        # Add components to the Flet page
        page.add(
            function_input,
            generate_button,
            result
        )

    ft.app(target=main)

if __name__ == "__main__":
    start_flet()
