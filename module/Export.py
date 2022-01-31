import numpy as np
import os
import datetime
import csv
from stl import mesh
from graphviz import Digraph


def Export(tetras, edges, num, threshold, k, d_max, vert, gene_final, time, attempt):
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

    G.render(dir_path+'/'+now.strftime('%Y%m%d_%H%M%S'))

    with open(dir_path+'/params.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["生成要素の下限", "結合の閾値", "合成比率", "d_max"])
        writer.writerow([num, threshold, k, d_max])
        writer.writerow(['頂部のx座標', '頂部のy座標', '頂部のz座標'])
        writer.writerow(vert)

    with open(dir_path+'/gene_array.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["state", "weight", "theta", "phi"])
        for i in range(32):
            writer.writerow([i+1, gene_final["weight"][i],
                            gene_final["theta"][i], gene_final["phi"][i]])

    with open(dir_path+'/object_information.csv', 'w') as f:
        writer = csv.writer(f)
        sum = [0, 0, 0, 0, 0]
        for tetra in tetras:
            isCreated = int(tetra.isCreated[0]+tetra.isCreated[1] +
                            tetra.isCreated[2]+tetra.isCreated[3])
            sum[isCreated] += 1

        writer.writerow(["実行時間", "総試行回数", "isCreated==0の要素数",
                        "isCreated==1の要素数", "isCreated==2の要素数", "isCreated==3の要素数", "isCreated==4の要素数"])
        writer.writerow(
            [time, attempt, sum[0], sum[1], sum[2], sum[3], sum[4]])
        writer.writerow(["index", "pos0.x", "pos0.y",
                         "pos0.z", "pos1.x", "pos1.y", "pos1.z", "pos2.x", "pos2.y", "pos2.z", "pos03.x", "pos3.y", "pos3.z", "centroid.x", "centroid.y", "centroid.z", "isCreated", '体積'])
        for tetra in tetras:
            # 体積の計算
            p0 = tetra.point[0]
            p1 = tetra.point[1]
            p2 = tetra.point[2]
            p3 = tetra.point[3]

            volume = ((p3[0]-p0[0])*((p1[1]-p0[1])*(p2[2]-p0[2])-(p1[2]-p0[2])*(p2[1]-p0[1])) +
                      (p3[1]-p0[1])*((p1[2]-p0[2])*(p2[0]-p0[0])-(p1[0]-p0[0])*(p2[2]-p0[2])) +
                      (p3[2]-p0[2])*((p1[0]-p0[0])*(p2[1]-p0[1])-(p1[1]-p0[1])*(p2[0]-p0[0]))) / 6

            data = [tetra.index]+p0+p1+p2+p3 + \
                list(tetra.centroid) + \
                [int(tetra.isCreated[0]+tetra.isCreated[1] +
                     tetra.isCreated[2]+tetra.isCreated[3])] + [volume]
            writer.writerow(data)

    print('completed.')
