import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# This is a third-party library that makes it easy to write responsive, well-styled apps
# Documentation: https://dash-bootstrap-components.opensource.faculty.ai/docs/
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import chart_utils


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server


def layout():
    """
    Wrapping this in a function makes it easier to write the layout. All that's
    happening here is that a card is being defined. 
    So in the final product, you see a card with a header, some body text, and a graph.

    There is also a dropdown that controls the type of visual, and the options are 
    populated with a list comprehension.
    """
    chart_types = ["splom", "scatter", "density", "parallel"]

    card = dbc.Card(
        dbc.CardBody(
            [
                html.H4("This is an app", className="card-title"),
                html.P(
                    "Pick a chart type to display the data. Data is refreshed on page reload.",
                    className="card-text",
                ),
                dbc.Select(
                    id="selector",
                    options=[
                        {"label": chart_type, "value": i}
                        for i, chart_type in enumerate(chart_types)
                    ],
                    value=0,
                    placeholder="Select a chart type...",
                ),
                dcc.Graph(id="graph"),
            ]
        ),
    )

    items = dbc.Container(
        [card, dcc.Store(id="data-store"), dcc.Location(id="url"),], className="p-5",
    )

    return items


app.layout = layout()


@app.callback(
    Output("graph", "figure"),
    [Input("selector", "value"), Input("data-store", "data")],
)
def select_graph(graph_type, data):
    # This callback provides functionality to the dropdown.
    # When you select a chart type, the correct chart generation function is
    # used to build that chart.
    df = pd.DataFrame(data)

    chart_functions = [
        chart_utils.generate_splom,
        chart_utils.generate_scatter,
        chart_utils.generate_density,
        chart_utils.generate_parallel,
    ]

    f = chart_functions[int(graph_type)]

    return f(df)


@app.callback(Output("data-store", "data"), [Input("url", "pathname")])
def populate_data(pathname):
    # In this callback, you could hit an API endpoint where the data comes from.
    # If the data is coming from some API that refreshes daily, it would make sense to
    # pull from there. The data refresh could also be run as a script as part of the app.

    # This function is triggered on page load, and it would be wise to make this function
    # as lightweight as possible to make the page load faster.

    # You could also just write a pd.read_csv() function that reads in the CSV dynamically from your
    # file store.
    df = px.data.iris()
    return df.to_dict()


if __name__ == "__main__":
    app.run_server(debug=True)

