import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from func import mesh_to_figure
from obj_read import obj_file_to_mesh3d
from obj_read import obj_to_graph

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='basic-interactions'),
    html.Button('Bunny', id='btn1', n_clicks=0),
    html.Button('Cow', id='btn2', n_clicks=0),
    html.Button('Dragon', id='btn3', n_clicks=0),
    dcc.Slider(id='slider', min=10, max=40, step=1, value=20),
],
    style={'width': '50%'}
)

files = ["bunny.obj", "cow.obj", "dragon.obj"]
objs = [obj_file_to_mesh3d("objs/" + f) for f in files]
curr = 0
graphs = [obj_to_graph(data[1]) for data in objs]
heat_value = 20


@app.callback(
    Output('basic-interactions', 'figure'),
    Input('basic-interactions', 'clickData'),
    Input('btn1', 'n_clicks'),
    Input('btn2', 'n_clicks'),
    Input('btn3', 'n_clicks'))
def display_click_data(clickData, btn1, btn2, btn3):
    print(clickData)
    global objs, curr, graphs, heat_value
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn1' in changed_id:
        curr = 0
        fig = mesh_to_figure(objs[curr], graphs[curr], heat_value, None)
    elif 'btn2' in changed_id:
        curr = 1
        fig = mesh_to_figure(objs[curr], graphs[curr], heat_value, None)
    elif 'btn3' in changed_id:
        curr = 2
        fig = mesh_to_figure(objs[curr], graphs[curr], heat_value, None)
    else:
        fig = mesh_to_figure(objs[curr], graphs[curr], heat_value, clickData)
    return fig


@app.callback(Output('slider', 'value'),
              [Input('slider', 'value')])
def display_value(value):
    global heat_value
    heat_value = value
    return value


if __name__ == '__main__':
    app.run_server(debug=True)
