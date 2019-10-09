import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from glob import glob
import os
import numpy as np
#import subprocess

#subprocess.call(["taskkill","/K","/IM","PyMOL.exe"])

pseFiles = glob("*.pse")

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
externalStylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, externalStylesheets=externalStylesheets)

df = pd.read_csv('dataSetA.csv',float_precision='round_trip')

app.layout = html.Div([
    html.Div([
    dcc.Dropdown(
        id='my-dropdown',
        placeholder='Select PyMOL Session',
        options=[
            {'label': f, 'value': f} for f in pseFiles
        ],
        value="None"
    ),
    html.Div(id='output-container')
]),

html.Div([
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": False} for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=True,
        filtering=True,
        sorting=True,
        sorting_type="single",
        row_selectable="multi",
        row_deletable=False,
        style_table={'overflowX': 'scroll'},
        style_cell={'whiteSpace': 'no-wrap',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'minWidth': '50px', 'width': '180px', 'maxWidth': '180px',},
        css=[{
        'selector': '.dash-cell div.dash-cell-value',
        'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
        }],
        style_cell_conditional=[
        {'if': {'column_id': 'QED'},
         'width': '80px'},
         ],
        selected_rows=[],
        pagination_mode="fe",
            pagination_settings={
                "displayed_pages": 1,
                "current_page": 0,
                "page_size": 20,
            },
            navigation="page",
    ),
    html.Div(id='datatable-interactivity-container')
]) 
    ])
@app.callback(
    dash.dependencies.Output('output-container', 'children'),
    [dash.dependencies.Input('my-dropdown', 'value')])
def update_output(value):
    os.startfile(value)
    return 'Opening PyMol Session: "{}"'.format(value)


@app.callback(
    Output('datatable-interactivity-container', "children"),
    [Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows")])
def update_graph(rows, derived_virtual_selected_rows):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncracy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    if rows is None:
        dff = df
    else:
        dff = pd.DataFrame(rows)

    color_rows = []
    for i in range(len(dff)):
        if i in derived_virtual_selected_rows:
            color_rows.append("#7FDBFF")
        else:
            color_rows.append("#0074D9")

    return html.Div([
           html.Div([
           html.H5('QED Scores By Data Set'),
                dcc.Graph(
                    id='PDBs',
                    figure={
                        'data': [
                            go.Scatter(
                                x=df[df['Data_Set'] == i]['QED'],
                                y=df[df['Data_Set'] == i]['QED'],
                                text=df[df['Data_Set'] == i]['PDB'],
                                mode='markers',
                                opacity=0.7,
                                marker={
                                    'size': 15,
                                    'line': {'width': 0.5, 'color': 'black'}
                                },
                                name=i
                            ) for i in df.Data_Set.unique()
                        ],
                        'layout': go.Layout(
                            xaxis={'type': 'log', 'title': 'Data Set A'},
                            yaxis={'title': 'QED'},
                            #margin={'l': 40, 'b': 40, 't': 20, 'r': 10},
                            legend={'x': 0, 'y': 1},
                            hovermode='closest'
                        
                        )
                    }
                )
           ])
        ]
    )



if __name__ == '__main__':
    app.run_server(debug=False)
