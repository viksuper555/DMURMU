import dash_html_components as html
from layout import description_card, generate_control_card, generate_graph, generate_table
import dash_bootstrap_components as dbc
from dash import Dash, Input, State, Output, no_update
import pandas as pd
import tree
from dash.exceptions import PreventUpdate
# app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

app = Dash(__name__, external_stylesheets=[dbc.themes.LITERA])
app.title = "Decision making under risk and uncertainty"

@app.callback(
    [
        Output('table-results','data'),
        Output('table-results','columns'),
        Output('cytoscape','elements'),
    ],
    [Input('generate-btn','n_clicks')],
    [
        State('table-input','data'),
        State('cost_input', 'value')
    ])

def update_datatable(n_clicks, df, cost):            
    if not n_clicks:
        raise PreventUpdate
    df = pd.DataFrame(df)
    calc = calculate_result(df)
    columns = [{'name': col, 'id': col} for col in calc.columns]
    elements = tree.build_tree_analysis(df, calc, cost)
    # elements = tree.build_tree_no_analysis(df)
    return calc.to_dict(orient='records'), columns, elements

def calculate_result(df):
    ti_len = len(df['ti'])
    prods = {"ε1":[tree.sum_product(df, 'pti', 'ε1')], 
             "ε2":[tree.sum_product(df, 'pti', 'ε2')],
             "ε3":[tree.sum_product(df, 'pti', 'ε3')]}
    for eps in range(1, len(prods)+1):
        for ti in range(0, ti_len):
            prods[f"ε{eps}"].append(df['pti'][ti]*df[f'ε{eps}'][ti]/prods[f"ε{eps}"][0])
    
    df = pd.DataFrame(prods).T.round(4).reset_index()
    df.columns = ['ε', 'p(ε)'] + [f'ϑ{x+1}' for x in range(ti_len)]
    return df


app.layout = html.Div(
    id="app-container",
    children=[
        # Banner
        html.Div(
            id="banner",
            className="banner",
            children=[html.Img(src=app.get_asset_url("plotly_logo.png"))],
        ),
        # Left column
        html.Div(
            id="left-column",
            className="four columns",
            children=[description_card(), generate_control_card()]
            + [
                html.Div(
                    ["initial child"], id="output-clientside", style={"display": "none"}
                )
            ],
        ),
        # Right column
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                html.Div(
                    id="wait_time_card",
                    children=[
                        html.B("Results"),
                        html.Hr(),
                        html.Div(id="wait_time_table", children=generate_table(), style={"width":"50%"}),
                        html.Hr(),
                        html.Div(id="wait_time_table", children=generate_graph()),
                    ],
                ),
            ],
        ),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)