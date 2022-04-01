import numpy as np
import plotly.graph_objects as go


def get_shortest_path(graph, start, goal):
    explored = []
    queue = [[start]]

    if start == goal:
        print("Same Node")
        return None

    i = 0
    while queue:
        if i % 1000 == 0:
            print(i)
        i += 1
        path = queue.pop(0)
        node = path[-1]

        if node not in explored:
            neighbours = graph[node]

            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)

                if neighbour == goal:
                    print("Shortest path = ", *new_path)
                    return new_path
            explored.append(node)

    print("Path not found")
    return None


def mesh_to_figure(data, graph, last_click, curr_click):
    vertices, faces = data
    x, y, z = vertices[:, :3].T
    I, J, K = faces.T

    if last_click is not None:
        path = get_shortest_path(graph, last_click, curr_click)
        path = go.Scatter3d(x=x[path], y=z[path], z=y[path])
    else:
        path = go.Scatter3d()

    mesh = go.Mesh3d(
        x=x, y=z, z=y,
        vertexcolor=np.full((len(vertices), 3), fill_value=0.5),  # the color codes must be triplets of floats  in [0,1]
        i=I, j=J, k=K,
        name='',
        showscale=False)

    mesh.update(lighting=dict(ambient=0.18, diffuse=1, fresnel=.1, specular=.9, roughness=.1),
                lightposition=dict(x=100, y=200, z=150))

    layout = go.Layout(title='',
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

    fig = go.Figure(data=[mesh, path], layout=layout)
    return fig
