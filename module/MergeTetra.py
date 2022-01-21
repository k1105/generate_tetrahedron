from module import Set2D
from module import TriangleIntersectionDetection as tint
import numpy.linalg as LP
import numpy as np


def Merge(candidate_tetra, tetras, threshold):
    candidate_triangle_index = -1
    target_triangle_index = -1

    for target_tetra in tetras:
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

            # 発生率はかなり低いが, 稀にcandidate_pointがshared_edgeに含まれる
            # =新規で作成された頂点が既存の他の頂点にたまたま一致することがある.
            # この場合は何もしないので、 それをハンドリング.
            if candidate_point in shared_edge:
                continue

            for target_point in target_points:
                # print("target")
                target_triangle_index = target_tetra.findTriangleIndex(
                    shared_edge[0], shared_edge[1], target_point)
                # merge先になる可能性のある四面体におけるisCreatedのチェック.
                if target_tetra.isCreated[target_triangle_index] == 0 and not tint.isIntersectToTriangle(candidate_tetra.triangle[3], [candidate_point, target_point]):
                    # 閾値以下、かつマージ後の頂点が四面体の裏側に回ってないか判定.
                    if LP.norm(np.array(target_point)-np.array(candidate_point)) < threshold:
                        candidate_triangle_index = candidate_tetra.findTriangleIndex(
                            shared_edge[0], shared_edge[1], candidate_point)
                        candidate_tetra.point[3] = target_point
                        connected_tetra = target_tetra
                        return candidate_tetra, connected_tetra, candidate_triangle_index, target_triangle_index

        return candidate_tetra, None, candidate_triangle_index, target_triangle_index
