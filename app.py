import plotly.graph_objects as go
import tree
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
import dash_table
# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

app = dash.Dash(__name__)

elements = tree.get_nodes() + tree.get_edges()
params = [
    ('v1', ['V', 'v1']),
    ('v2', ['V', 'v2']),
    ('pti', ['', 'P(ϑ)']),
    ('eps1', ['p(ε|ϑ)', 'ε1']),
    ('eps2', ['p(ε|ϑ)', 'ε2']),
    ('eps3', ['p(ε|ϑ)', 'ε3']),
]
app.layout = html.Div([
    dash_table.DataTable(
        id='table-editing-simple',
        columns=(
            [{'id': 'ti', 'name': ['', 'ϑ']}] +
            [{'id': p[0], 'name': p[1]} for p in params]
        ),
        data=[
            dict(ti=f'ϑ{i}', **{param[0]: 0 for param in params})
            for i in range(1, 4)
        ],
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
    html.Button('Generate', id='submit-val', n_clicks=0),
    cyto.Cytoscape(
        id='cytoscape-layout',
        layout={'name': 'grid'},
        style={'width': '100%', 'height': '450px'},
        elements=elements
    )
])

    
if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)