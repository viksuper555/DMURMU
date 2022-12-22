
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
import dash_table
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output
from dash_table.Format import Format, Scheme
import tree
elements = []
# elements = tree.get_nodes() + tree.get_edges()
params = [
    ('v1', ['V', 'v1']),
    ('v2', ['V', 'v2']),
    ('pti', ['', 'P(ϑ)']),
    ('ε1', ['p(ε|ϑ)', 'ε1']),
    ('ε2', ['p(ε|ϑ)', 'ε2']),
    ('ε3', ['p(ε|ϑ)', 'ε3']),
]

def description_card():
    """
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Risk Analysis"),
            html.H3("Welcome to the decision making under risk and uncertainty."),
            html.Div(
                id="intro",
                children="Insert input data to visualize calculation values and propose a decision path.",
            ),
        ],
    )


def generate_control_card():
    """
    :return: A Div containing controls for input data.
    """

    return html.Div(
        id="control-card",
        children=[
            dbc.Label("Input data"),
            dash_table.DataTable(
                id='table-input',
                columns=(
                    [{'id': 'ti', 'name': ['', 'ϑ'], 'editable':False}] +
                    [{'id': p[0], 'name': p[1], 'type': 'numeric'} for p in params]
                ),
                data=[
                    {'ti': 'ϑ1', 'v1': -100000, 'v2': 0, 'pti': 0.16, 'ε1': 1, 'ε2': 0, 'ε3': 0}, 
                    {'ti': 'ϑ2', 'v1': 50000, 'v2': 0, 'pti': 0.32, 'ε1': 0.1, 'ε2': 0.9, 'ε3': 0}, 
                    {'ti': 'ϑ3', 'v1': 100000, 'v2': 0, 'pti': 0.36, 'ε1': 0, 'ε2': 1, 'ε3': 0}, 
                    {'ti': 'ϑ4', 'v1': 200000, 'v2': 0, 'pti': 0.16, 'ε1': 0, 'ε2': 0, 'ε3': 1}
                ],
                # data=[
                #     dict(ti=f'ϑ{i}', **{param[0]: 0 for param in params})
                #     for i in range(1, 5)
                # ],
                css=[
                {"selector": ".column-header--delete svg", "rule": 'display: "none"'},
                {"selector": ".column-header--delete::before", "rule": 'content: "X"'}
                ],
                style_cell={'textAlign': 'center', 'padding': '5px'},
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'
                },
                editable=True,
                merge_duplicate_headers=True
            ),
            html.Br(),
            dbc.Label('Concession value (in cash):'),
            dcc.Input(
                id="value_input",
                type='number',
                placeholder="Please enter value.",
                value=23000
            ),
            html.Br(),
            dbc.Label('Cost of experiment:'),
            dcc.Input(
                id="cost_input",
                type='number',
                placeholder="Please enter cost.",
                value=5000
            ),
            html.Br(),
            html.Div(
                dbc.Button("Generate", id="generate-btn", size="lg", color="success", n_clicks=0),
                id="generate-btn-outer"
            ),
        ],
    )


def generate_table():
    return html.Div(
    dash_table.DataTable(
        id='table-results'
    ))

def generate_graph():
    return html.Div([
        cyto.Cytoscape(
            id='cytoscape',
            layout={'name': 'preset'},
            style={'width': '100%', 'height': '600px'},
            elements=elements,
            stylesheet=[
            # Group selectors
            {
                'selector': 'node',
                'style': {
                    'content': 'data(label)'
                }
            },
            # Class selectors
            {
                'selector': '.blue',
                'style': {
                    'background-color': 'blue',
                    'line-color': 'blue'
                }
            },
            {
                'selector': '.green',
                'style': {
                    'background-color': 'green',
                    'line-color': 'green'
                }
            },
            {
                'selector': '.red',
                'style': {
                    'background-color': 'red',
                    'line-color': 'red'
                }
            },
            {
                'selector': '.gold',
                'style': {
                    'background-color': 'gold',
                    'line-color': 'gold'
                }
            },
            {
                'selector': '.transparent',
                'style': {
                    'background-color': 'transparent',
                    'line-color': 'transparent'
                }
            },
            {
                'selector': '.whiteSmoke',
                'style': {
                    'background-color': 'WhiteSmoke',
                    'line-color': 'WhiteSmoke'
                }
            },
        ]
        ),
        dbc.Label(id='result_label')])
