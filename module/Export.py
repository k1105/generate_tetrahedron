import numpy as np
import os
import datetime
from stl import mesh
from graphviz import Digraph


def Export(tetras, edges):
    vertices = []
    faces = []

    # stl生成
    print('generating stl file...')
    for tetra in tetras:
        for i in range(4):
            if tetra.isCreated[i] == 0:
                face = []
                for point in tetra.triangle[i]:
                    if not point in vertices:
                        vertices.append(point)
                    face.append(vertices.index(point))
                faces.append(face)

    # メッシュ（物体）作成
    vertices = np.array(vertices)
    faces = np.array(faces)
    obj = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            obj.vectors[i][j] = vertices[f[j], :]

    # 保存
    now = datetime.datetime.now()
    dir_path = 'out/'+now.strftime('%Y%m%d_%H%M%S')
    os.makedirs(dir_path)
    obj.save(dir_path+'/'+now.strftime('%Y%m%d_%H%M%S')+'.stl')

    print('completed.')

    # グラフ生成
    print('generating graph...')
    G = Digraph(format="png")
    G.attr("node", shape="circle")

    for tetra in tetras:
        if tetra.isCreated == [1, 1, 1, 1]:
            G.node(str(tetra.index), fillcolor="#ccddff", style="filled")

    for i, j in edges:
        G.edge(str(i), str(j))

    print('completed.')
    G.render(dir_path+'/'+now.strftime('%Y%m%d_%H%M%S'))
