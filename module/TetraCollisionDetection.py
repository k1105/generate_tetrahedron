import numpy.linalg as LP
from . import TriangleIntersectionDetection as tint


def isCollide(candidate_tetra, tetra_set):

    # 衝突判定
    for j in reversed(range(len(tetra_set))):
        target_tetra = tetra_set[j]
        # 外接球を用いた大まかな衝突判定
        if LP.norm(candidate_tetra.circumcenter-target_tetra.circumcenter) <= target_tetra.circumradius + candidate_tetra.circumradius:
            c_p = candidate_tetra.point
            # 新規に作成される辺候補のリスト
            candidate_edges = [[c_p[0], c_p[3]], [
                c_p[1], c_p[3]], [c_p[2], c_p[3]]]

            # 新規に作成される面候補のリスト
            candidate_triangles = [
                [c_p[0], c_p[1], c_p[3]],
                [c_p[0], c_p[2], c_p[3]],
                [c_p[1], c_p[2], c_p[3]]
            ]

            for k in range(4):
                for l in range(3):
                    # 新しく生成される辺と既存の面が交差するかどうかの判定
                    if tint.isIntersectToTriangle(target_tetra.triangle[k], candidate_edges[l]):
                        return True

            for m in range(6):
                for n in range(3):
                    # 新しく生成される面と既存の辺が交差するかどうかの判定
                    if tint.isIntersectToTriangle(candidate_triangles[n], target_tetra.edge[m]):
                        return True
    return False
