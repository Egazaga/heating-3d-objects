from collections import defaultdict

import numpy as np


def obj_to_graph(faces):
    graph = defaultdict(set)
    for f in faces:
        graph[f[0]].add(f[1])
        graph[f[0]].add(f[2])
        graph[f[1]].add(f[0])
        graph[f[1]].add(f[1])
        graph[f[2]].add(f[0])
        graph[f[2]].add(f[1])
    return graph


def obj_file_to_mesh3d(path):
    with open(path, 'r') as file:
        obj_data = file.read()
    vertices = []
    faces = []
    lines = obj_data.splitlines()

    for line in lines:
        slist = line.split()
        if slist:
            if slist[0] == 'v':
                vertex = np.array(slist[1:], dtype=float)
                vertices.append(vertex)
            elif slist[0] == 'f':
                face = []
                for k in range(1, len(slist)):
                    face.append([int(s) for s in slist[k].replace('//', '/').split('/')])
                if len(face) > 3:  # triangulate the n-polyonal face, n>3
                    faces.extend(
                        [[face[0][0] - 1, face[k][0] - 1, face[k + 1][0] - 1] for k in range(1, len(face) - 1)])
                else:
                    faces.append([face[j][0] - 1 for j in range(len(face))])
            else:
                pass

    return np.array(vertices), np.array(faces)
