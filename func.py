import numpy as np
import plotly.graph_objects as go
from matplotlib.cm import get_cmap
from matplotlib.colors import Normalize
from numba import njit


@njit
def set_heatmap(id, graph, step, heatmap):
    neighbors = {id}
    next_neighbors = {id}
    next_neighbors.clear()  # jit needs to know the type
    seen = set()
    for s in range(step, 0, -1):
        print(s)
        for neighbor in neighbors:
            if neighbor not in seen:
                heatmap[neighbor] = s
                seen.add(neighbor)
                next_neighbors.update(graph[graph[:, 0] == neighbor][:, 1])
        neighbors = next_neighbors
        next_neighbors = {id}
        next_neighbors.clear()


def mesh_to_figure(data, graph, heat_value, clickData):
    vertices, faces = data
    x, y, z = vertices[:, :3].T
    I, J, K = faces.T

    if clickData is not None:
        norm = Normalize()
        id = clickData["points"][0]["pointNumber"]
        values = [0] * len(vertices)
        set_heatmap(id, graph, heat_value, values)
        color = get_cmap('magma')(norm(values))
    else:
        color = np.zeros((len(vertices), 3))

    mesh = go.Mesh3d(
        x=x, y=z, z=y,
        vertexcolor=color,  # the color codes must be triplets of floats  in [0,1]!!
        i=I, j=J, k=K,
        name='',
        showscale=False)

    mesh.update(lighting=dict(ambient=0.18, diffuse=1, fresnel=.1, specular=.9, roughness=.1),
                lightposition=dict(x=100, y=200, z=150))

    layout = go.Layout(title='Mesh3d from a Wavefront obj file',
                       autosize=False,
                       font=dict(size=14, color='black'),
                       width=900,
                       height=800,
                       scene=dict(xaxis=dict(visible=False),
                                  yaxis=dict(visible=False),
                                  zaxis=dict(visible=False),
                                  aspectmode='data',
                                  camera=dict(eye=dict(x=0, y=2, z=0)),
                                  ),
                       paper_bgcolor='rgb(235,235,235)',
                       margin=dict(t=175),
                       uirevision=True)

    fig = go.Figure(data=[mesh], layout=layout)
    return fig

# def recurs(id, graph, step, heatmap):
#     # slower?
#     if step == 0:
#         return
#     if step <= heatmap[id]:
#         return
#     heatmap[id] = step
#
#     neighbors = graph[graph[:, 0] == id][:, 1]
#     for neighbor in neighbors:
#         if neighbor != -1:
#             recurs(neighbor, graph, step - 1, heatmap)
#
#     # faster?
#     if step == 0:
#         return
#     heatmap[id] = step
#
#     neighbors = graph[graph[:, 0] == id][:, 1]
#     for neighbor in neighbors:
#         if neighbor != -1 and heatmap[neighbor] < step - 1:
#             recurs(neighbor, graph, step - 1, heatmap)
