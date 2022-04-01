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
    html.Button('Cow', id='btn1', n_clicks=0),
    html.Button('Bunny', id='btn2', n_clicks=0),
    html.Button('Cat', id='btn3', n_clicks=0),
],
    style={'width': '50%'}
)

files = ["cow.obj", "bunny.obj", "cat.obj"]
objs = [obj_file_to_mesh3d("objs/" + f) for f in files]
curr = 0
graphs = [obj_to_graph(data[1]) for data in objs]
last_click = None


@app.callback(
    Output('basic-interactions', 'figure'),
    Input('basic-interactions', 'clickData'),
    Input('btn1', 'n_clicks'),
    Input('btn2', 'n_clicks'),
    Input('btn3', 'n_clicks'))
def display_click_data(clickData, btn1, btn2, btn3):
    global objs, curr, graphs, last_click
    print(clickData)
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split(".")[0]

    if 'btn1' in changed_id or 'btn2' in changed_id or 'btn3' in changed_id:  # button clicked
        if 'btn1' in changed_id:
            curr = 0
        if 'btn2' in changed_id:
            curr = 1
        if 'btn3' in changed_id:
            curr = 2
        last_click = None
        fig = mesh_to_figure(objs[curr], graphs[curr], None, None)
    elif clickData is None:  # init
        fig = mesh_to_figure(objs[curr], graphs[curr], None, None)
    else:  # click on graph
        if last_click is None:
            fig = mesh_to_figure(objs[curr], graphs[curr], None, None)
            last_click = clickData["points"][0]["pointNumber"]
        else:
            curr_click = clickData["points"][0]["pointNumber"]
            fig = mesh_to_figure(objs[curr], graphs[curr], last_click, curr_click)
            last_click = curr_click

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
