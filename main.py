import random
import numpy as np
import numpy.linalg as LP
import time
import os
import datetime
from stl import mesh
from module import TetraCollisionDetection as tcol
from module import PlaneIntersectionDetection as pint
from module import Set2D
from graphviz import Digraph


class Tetra():
    def __init__(self, p0, p1, p2, p3, index):
        self.point = [p0, p1, p2, p3]
        self.isCreated = [0, 0, 0, 0]
        self.triangle = [[p1, p2, p3], [
            p0, p2, p3], [p0, p1, p3], [p0, p1, p2]]
        self.edge = [
            [p0, p1],
            [p0, p2],
            [p0, p3],
            [p1, p2],
            [p1, p3],
            [p2, p3]
        ]
        self.circumcenter, self.circumradius = calcCircumsphere(
            [p0, p1, p2, p3])
        self.index = index

    def findTriangleIndex(self, p0, p1, p2):
        # tetraが持つ三角形のうち、p0, p1, p2からなる三角形に一致するものを返す関数.
        for index in range(0, 4):
            # print(self.triangle[index])
            if len(Set2D.set2D(self.triangle[index]) & Set2D.set2D([p0, p1, p2])) == 3:
                return index

        ## 上のreturnが実行されなかった場合 = p0, p1, p2からなる三角形は存在しない
        print("error: there's no triangle in tetra: "+str([p0, p1, p2]))
        print("tetra's point: "+str(self.point))
        return -1


def calcCircumsphere(point):
    # 外接球の半径と外点を求める関数
    p0 = np.array(point[0])
    p1 = np.array(point[1])
    p2 = np.array(point[2])
    p3 = np.array(point[3])
    matrix = [p0-p1, p0-p2, p2-p3]

    # 外接円の外点
    circumcenter = 0.5 * np.dot(LP.inv(matrix), [LP.norm(p0)**2-LP.norm(
        p1)**2, LP.norm(p0)**2-LP.norm(p2)**2, LP.norm(p2)**2-LP.norm(p3)**2])
    # 外接円の半径
    circumradius = LP.norm(p0 - circumcenter)

    return circumcenter, circumradius


####### MAIN #######
start = time.time()
edges = []
# 生成したい四面体の個数をここで指定:
num = int(input('生成する四面体の個数-> '))
threshold = int(input('くっつける頂点の距離の閾値->'))  # 2つの頂点間の距離が, 閾値以下の場合に四面体同士がくっつく.

print('generate '+str(num)+' tetrahedron.')

# 最初の四面体を作成
tetra = Tetra([10, 10, 10], [-10, -10, 10], [10, -10, -10], [-10, 10, -10], 0)

tetra_set = []

# 配列に追加
tetra_set.append(tetra)

while len(tetra_set) < num:
    for i in range(0, len(tetra_set)):
        # i 番目の四面体情報を取得
        tetra_i = tetra_set[i]

        # i 番目の四面体情報をもとに新しい四面体を作成
        # 面を選ぶ
        target = random.randint(0, 3)

        if tetra_i.isCreated[target] == 0:
            s = tetra_i.triangle[target]  # tetra_i上のtarget番目の三角形.

            # ベクトルを作る
            center = (np.array(s[0])+np.array(s[1]) +
                      np.array(s[2])) / 3  # 三角形の重心
            # 三角形sに含まれないtetra_iの頂点
            left_point = np.array(tetra_i.point[target])
            vector = np.array(left_point - center)  # 頂点-重心

            # 頂点を作る
            k = random.uniform(0.7, 1.5)  # ベクトルに掛け合わされる定数
            # candidate_point. 頂点候補（衝突判定によって棄却される可能性あり）
            c_p = list(map(int, -1 * k * vector + center))
            # print(c_p)

            candidate_tetra = Tetra(s[0], s[1], s[2], c_p, len(tetra_set))
            connected_tetra = None

            # merge処理 開始
           # print("check close tetra (from: "+str(target_tetra.index)+")")
            merged = False

            for target_tetra in tetra_set:
                if merged:
                    break

                # 共有する頂点の数を検出.
                # 0 ... 四面体は接していない
                # 1 ... 四面体は一点でのみ接する
                # 2 ... 四面体は1辺を共有する
                # 3 ... 四面体は1面を共有する
                if len(Set2D.set2D(candidate_tetra.point) & Set2D.set2D(target_tetra.point)) == 2:  # 1つの辺を共有する場合
                    candidate_point = candidate_tetra.point[3]  # 末尾の頂点.
                    # くっつく可能性のある頂点 = 共有している辺以外の頂点２つ.　= 「candidate_tetraとtarget_tetraに共通しない要素」とtarget_tetraに共通する要素
                    target_points = list(map(list, (Set2D.set2D(candidate_tetra.point) ^ Set2D.set2D(
                        target_tetra.point)) & Set2D.set2D(target_tetra.point)))

                    # 2つの四面体が共有する辺.
                    shared_edge = list(map(list, Set2D.set2D(
                        candidate_tetra.point) & Set2D.set2D(target_tetra.point)))

                    ## 発生率はかなり低いが, 稀にcandidate_pointがshared_edgeに含まれる
                    # =新規で作成された頂点が既存の他の頂点にたまたま一致することがある.
                    # この場合は何もしないので、 それをハンドリング.
                    if not candidate_point in shared_edge:

                        for target_point in target_points:
                            # print("target")
                            target_triangle_index = target_tetra.findTriangleIndex(
                                shared_edge[0], shared_edge[1], target_point)
                            # merge先になる可能性のある四面体におけるisCreatedのチェック.
                            if target_tetra.isCreated[target_triangle_index] == 0 and not pint.isIntersectToPlane(candidate_tetra.triangle[3], candidate_point, target_point):
                                # 閾値以下、かつマージ後の頂点が四面体の裏側に回ってないか判定.
                                if LP.norm(np.array(target_point)-np.array(candidate_point)) < threshold:
                                    candidate_triangle_index = candidate_tetra.findTriangleIndex(
                                        shared_edge[0], shared_edge[1], candidate_point)
                                    candidate_tetra.point[3] = target_point
                                    connected_tetra = target_tetra
                                    merged = True
                                    break

            # merge処理 終了

           # print("\r"+"processing...("+'{:.1f}'.format(len(tetra_set)/num*100)+"%) | check collision of tetra (from: "+str(target_tetra.index)+")" ,end="")

            if not tcol.isCollide(candidate_tetra, tetra_set):
                # 判定をPassした場合 :
                candidate_tetra.isCreated[3] = 1  # 生成した時点で接してる四面体
                tetra_set[i].isCreated[target] = 1

                edges.append((tetra_i.index, candidate_tetra.index))

                if connected_tetra is not None:
                    if candidate_triangle_index != -1 and target_triangle_index != -1:
                        candidate_tetra.isCreated[candidate_triangle_index] = 1
                        tetra_set[connected_tetra.index].isCreated[target_triangle_index] = 1
                        edges.append(
                            (connected_tetra.index, candidate_tetra.index))

                # 一覧に追加
                new_tetra = Tetra(candidate_tetra.point[0], candidate_tetra.point[1],
                                  candidate_tetra.point[2], candidate_tetra.point[3], candidate_tetra.index)
                new_tetra.isCreated = candidate_tetra.isCreated
                tetra_set.append(new_tetra)

                print("\r"+"processing...(" +
                      '{:.1f}'.format(len(tetra_set)/num*100)+"%)", end="")

            if(len(tetra_set) == num):
                break

elapsed_time = time.time() - start
print("\n"+"completed. ({:.4g}".format(elapsed_time) + "s)")

vertices = []
faces = []

# stl生成
print('generating stl file...')
for tetra in tetra_set:
    for i in range(0, 4):
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


# Y軸方向に90度回転
#obj.rotate([0.0, 1.0, 0.0], math.radians(90))

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

for tetra in tetra_set:
    if tetra.isCreated == [1, 1, 1, 1]:
        G.node(str(tetra.index), fillcolor="#ccddff", style="filled")

for i, j in edges:
    G.edge(str(i), str(j))
G.render(dir_path+'/'+now.strftime('%Y%m%d_%H%M%S'))