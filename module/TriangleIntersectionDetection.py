import numpy as np
from . import Set2D


def det3x3(a, b, c):
    return a[0]*b[1]*c[2]+a[1]*b[2]*c[0]+a[2]*b[0]*c[1]-a[2]*b[1]*c[0]-a[1]*b[0]*c[2]-a[0]*b[2]*c[1]


def isIntersectToTriangle(triangle, line):
    # triangleとlineが交差しているかの判定を行う関数.
    # line: [重心, 頂点]

    v0 = np.array(triangle[0])
    v1 = np.array(triangle[1])
    v2 = np.array(triangle[2])

    # v0, v1, v2, およびline[0], line[1]に重複した要素が存在していないか検証. もし重複した要素が存在していない場合は以下を実行
    dup = len(Set2D.set2D([v0, v1, v2]) & Set2D.set2D([line[0], line[1]]))
    if dup == 0:
        origin = np.array(line[0])  # 線分の開始点
        ray = np.array(line[1]) - origin  # 線分の終点
        invRay = -1 * ray  # 終点ベクトルの反対
        edge1 = v1 - v0
        edge2 = v2 - v0

        denominator = det3x3(edge1, edge2, invRay)

        if denominator > 0:
            d = origin - v0
            u = det3x3(d, edge2, invRay) / denominator
            if 0 <= u <= 1:
                v = det3x3(edge1, d, invRay) / denominator

                if 0 <= v and u + v <= 1:
                    t = det3x3(edge1, edge2, d) / denominator

                    # 距離がマイナスの場合は交差していない
                    if t >= 0:
                        return True

        origin = np.array(line[1])  # 線分の開始点
        ray = np.array(line[0]) - origin  # 線分の終点
        invRay = -1 * ray  # 終点ベクトルの反対

        denominator = det3x3(edge1, edge2, invRay)

        if denominator > 0:
            d = origin - v0
            u = det3x3(d, edge2, invRay) / denominator
            if 0 <= u <= 1:
                v = det3x3(edge1, d, invRay) / denominator
                if 0 <= v and u + v <= 1:
                    t = det3x3(edge1, edge2, d) / denominator

                    # 距離がマイナスの場合は交差していない
                    if t >= 0:
                        return True

    return False
