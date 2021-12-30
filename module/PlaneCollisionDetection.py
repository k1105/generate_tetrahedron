import numpy as np
import numpy.linalg as LP
from . import Set2D


def isIntersectToPlane(triangle, line):
    # triangleとlineが交差しているかの判定を行う関数.
    ## line: [重心, 頂点]
    origin = np.array(line[0])  # 線分の開始点
    ray = np.array(line[1])  # 線分の終点
    invRay = -1 * ray  # 終点ベクトルの反対
    v0 = np.array(triangle[0])
    v1 = np.array(triangle[1])
    v2 = np.array(triangle[2])

    if len(Set2D.set2D([v0, v1, v2]) & Set2D.set2D([origin, ray])) == 0:

        edge1 = v1 - v0
        edge2 = v2 - v0

        denominator = LP.det([edge1, edge2, invRay])

        if denominator > 0:
            d = origin - v0
            u = LP.det([d, edge2, invRay]) / denominator
            if 0 <= u <= 1:  # note: ここをいくつの値に設定するかで全体の形状に影響を与えそう.
                v = LP.det([edge1, d, invRay]) / denominator
                # note: ここをいくつの値に設定するかで全体の形状に影響を与えそう.
                if 0 <= v and u + v <= 1:
                    t = LP.det([edge1, edge2, d]) / denominator

                    # 距離がマイナスの場合は交差していない
                    if t >= 0:
                        return True

        origin = np.array(line[1])  # 線分の開始点
        ray = np.array(line[0])  # 線分の終点
        invRay = -1 * ray  # 終点ベクトルの反対

        denominator = LP.det([edge1, edge2, invRay])

        if denominator > 0:
            d = origin - v0
            u = LP.det([d, edge2, invRay]) / denominator
            if 0 <= u <= 1:  # note: ここをいくつの値に設定するかで全体の形状に影響を与えそう.
                v = LP.det([edge1, d, invRay]) / denominator
                # note: ここをいくつの値に設定するかで全体の形状に影響を与えそう.
                if 0 <= v and u + v <= 1:
                    t = LP.det([edge1, edge2, d]) / denominator

                    # 距離がマイナスの場合は交差していない
                    if t >= 0:
                        return True

    return False
