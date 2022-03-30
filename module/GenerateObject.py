import random
import numpy as np
import numpy.linalg as LP
from module import TetraCollisionDetection as tcol
from module import SelectTarget as star
from module import GenerateOutuptVector as gout
from module import TetraClass as tc
from module import MergeTetra as mt
from module import InitializeGeneArray as iga


def GenerateObject(num, threshold, k, vert, d_max, gene_array, attempt):
    tetras = []
    edges = []

    # 最初の四面体を作成
    tetra = tc.Tetra([10, 10, 10], [-10, -10, 10],
                     [10, -10, -10], [-10, 10, -10], 0)

    # 配列に追加
    tetras.append(tetra)

    # 初期化処理終了

    # 各ループで生成される四面体の総数を記録
    diff = 1

    while diff != 0:
        diff = 0

        prev_tetras = tetras.copy()

        for tetra in prev_tetras:
            if LP.norm(tetra.centroid - vert) > d_max:
                continue

            # i 番目の四面体情報を取得
            # i 番目の四面体情報をもとに新しい四面体を作成
            # 原点を起点としたoutputの位置ベクトル.
            out = gout.GenerateOutputVector(
                tetra, k, vert, d_max, gene_array)
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
                diff += 1

                print("\r"+"processing...( number of tetras: " +
                      '{:.1f}'.format(len(tetras))+")", end="")

    if(len(tetras) >= num):
        return tetras, edges, gene_array, attempt
    else:
        print('\n failed to generate object. redo:('+str(attempt)+')')
        gene_array = iga.InitializeGeneArray()
        return GenerateObject(num, threshold, k, vert, d_max, gene_array, attempt+1)
