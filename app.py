import dash_html_components as html
from layout import description_card, generate_control_card, generate_graph, generate_table
import dash_bootstrap_components as dbc
from dash import Dash, Input, State, Output
import pandas as pd
import tree
from dash.exceptions import PreventUpdate
import helpers

dash_app = Dash(__name__, external_stylesheets=[dbc.themes.LITERA])
dash_app.title = "Decision making under risk and uncertainty"

@dash_app.callback(
    [
        Output('table-results','data'),
        Output('table-results','columns'),
        Output('cytoscape','elements'),
        Output('result_label','children'),
    ],
    [Input('generate-btn','n_clicks')],
    [
        State('table-input','data'),
        State('value_input', 'value'),
        State('cost_input', 'value'),
    ])
def update_datatable(n_clicks, df, value, cost):            
    if not n_clicks or not df or len(df) < 1:
        raise PreventUpdate
    if not value:
        value = 0
    if not cost:
        cost = 0
    df = pd.DataFrame(df)
    calc = helpers.calculate_result(df)
    columns = [{'name': col, 'id': col} for col in calc.columns]
    elements = tree.add_basic_calcs(value, cost) + tree.build_tree_no_analysis(df) + tree.build_tree_analysis(df, calc, cost, glob_offset=350)    
    best = None 
    for el in elements:
        id = el.get('data').get('id')
        if id and id.startswith("total"):
            if not best or helpers.parse(el) > helpers.parse(best):
                best = el
        
    id = best.get('data').get('id')
    text = 'The best option is to do '
    if id == 'total1':
        text += f'experiment only, '
    elif id == 'total2':
        text += f'analysis and experiment, '
    elif id == 'total3':
        text += f'no analysis and no experiment, '
    else:
        text += f'analysis without experiment, '

    text += f'you can earn up to {helpers.parse(best)}.'

    return calc.to_dict(orient='records'), columns, elements, text


dash_app.layout = html.Div(
    id="app-container",
    children=[
        # Banner
        html.Div(
            id="banner",
            className="banner",
            children=[html.Img(src=dash_app.get_asset_url("super5_logo.png"))],
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
                        html.Div(id="wait_time_table2", children=generate_graph()),
                    ],
                ),
            ],
        ),
        html.Footer('Free open-source project by Viktor Kolev. All rights reserved.')
    ],
)

app = dash_app.server

if __name__ == "__main__":
    app.run(debug=False)