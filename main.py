import random
import numpy as np
import numpy.linalg as LP
import time
import datetime
from module import TetraCollisionDetection as tcol
from module import TriangleIntersectionDetection as tint
from module import Set2D
from module import SelectTarget as star
from module import GenerateVertex as gver
from module import TetraClass as tc
from module import Export as export
from module import MergeTetra as mt


####### MAIN #######
start = time.time()
# 生成したい四面体の個数をここで指定:
num = int(input('生成する四面体の個数(>2) -> '))
threshold = int(input('くっつける頂点の距離の閾値-> '))  # 2つの頂点間の距離が, 閾値以下の場合に四面体同士がくっつく.
k = float(input('合成比率(0<k<1)-> '))

print('generate '+str(num)+' tetrahedron.')

# random seedを現在時刻に指定
# pythonの場合, random seedは明示せずとも実行のたびに異なるseedを設定してくれるが, そのseedがいくつに設定されているのか, またどのタイミングで値が切り替わるのか把握できないので, 実行のたびに確実にseedが更新されるようマニュアルで指定している.
random.seed(datetime.datetime.now())

# 四面体リストの初期化処理
tetras = []
edges = []

# 最初の四面体を作成
tetra = tc.Tetra([10, 10, 10], [-10, -10, 10],
                 [10, -10, -10], [-10, 10, -10], 0)

# 配列に追加
tetras.append(tetra)

target = random.randint(0, 3)

triangle = tetra.triangle[target]
left_point = tetra.point[target]

# 2つ目の四面体生成
# ベクトルを作る
center = (np.array(triangle[0])+np.array(triangle[1]) +
          np.array(triangle[2])) / 3  # 三角形の重心
vector = np.array(left_point - center)  # 頂点-重心

# 頂点を作る
c = random.uniform(0.7, 1.5)  # ベクトルに掛け合わされる定数
# candidate_point. 頂点候補（衝突判定によって棄却される可能性あり）
point = -1 * c * vector + center

second_tetra = tc.Tetra(triangle[0], triangle[1], triangle[2], point, 1)

tetras.append(second_tetra)

tetras[1].isCreated[3] = 1  # 生成した時点で接してる四面体
tetras[1].setChildVertex(3, tetras[0].point[target])
tetras[0].isCreated[target] = 1
tetras[0].setChildVertex(target, tetras[1].point[3])

edges.append((0, 1))

# 初期化処理終了

# 位置情報ベクトルを計算するための前処理
# 頂部の計算
vert = np.array([random.uniform(-100, 100),
                 random.uniform(-100, 100), random.uniform(-100, 100)])

# 状態番号を保有する配列の生成
theta_list = list(range(1, 9))
random.shuffle(theta_list)
phi_list = list(range(1, 9))
random.shuffle(phi_list)

random_list = {"theta": theta_list, "phi": phi_list}

while len(tetras) < num:
    for tetra in tetras:
        # i 番目の四面体情報を取得
        # i 番目の四面体情報をもとに新しい四面体を作成
        # 原点を起点としたoutputの位置ベクトル.
        out = gver.GenerateVertex(tetra, tetras, k, vert, random_list)
        # 面を選ぶ
        target = star.SelectTarget(out, tetra)

        if target == -1:
            ## print('output vector == 0: '+str(tetra.index))
            continue

        if tetra.isCreated[target] != 0:
            ## print('selected plane already has an element.: '+str(tetra.index))
            continue

        s = tetra.triangle[target]  # tetra上のtarget番目の三角形.
        # ベクトルを作る
        center = (np.array(s[0])+np.array(s[1]) +
                  np.array(s[2])) / 3  # 三角形の重心
        left_point = tetra.point[target]

        vector = np.array(left_point - center)  # 頂点-重心
        e = vector / LP.norm(vector)  # 単位ベクトル
        # 頂点を作る
        point = -1 * (LP.norm(out)) * e + center
        # candidate_tetra : マージ処理を実施する前の四面体.
        raw_tetra = tc.Tetra(s[0], s[1], s[2], point, len(tetras))

        # merge処理
        # connected_tetra : マージ処理によってraw_tetraと結合した四面体.
        processed_tetra, connected_tetra, candidate_triangle_index, target_triangle_index = mt.Merge(
            raw_tetra, tetras, threshold)

        # print("\r"+"processing...("+'{:.1f}'.format(len(tetras)/num*100)+"%) | check collision of tetra (from: "+str(target_tetra.index)+")" ,end="")

        if not tcol.isCollide(processed_tetra, tetras):
            # 判定をPassした場合 :
            validated_tetra = processed_tetra
            validated_tetra.isCreated[3] = 1  # 生成した時点で接してる四面体
            validated_tetra.setChildVertex(3, tetra.point[target])
            tetra.isCreated[target] = 1
            tetra.setChildVertex(target, validated_tetra.point[3])

            edges.append((tetra.index, validated_tetra.index))

            if connected_tetra is not None:
                if candidate_triangle_index != -1 and target_triangle_index != -1:
                    validated_tetra.isCreated[candidate_triangle_index] = 1
                    validated_tetra.setChildVertex(
                        candidate_triangle_index, tetras[connected_tetra.index].point[target_triangle_index])
                    tetras[connected_tetra.index].isCreated[target_triangle_index] = 1
                    tetras[connected_tetra.index].setChildVertex(
                        target_triangle_index, validated_tetra.point[candidate_triangle_index])
                    edges.append(
                        (connected_tetra.index, validated_tetra.index))

            # 一覧に追加
            tetras.append(validated_tetra)

            print("\r"+"processing...(" +
                  '{:.1f}'.format(len(tetras)/num*100)+"%)", end="")

        if(len(tetras) == num):
            break

elapsed_time = time.time() - start
print("\n"+"completed. ({:.4g}".format(elapsed_time) + "s)")

export.Export(tetras, edges)
