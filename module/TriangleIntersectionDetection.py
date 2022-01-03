import numpy as np
from . import Set2D


def det3x3(a, b, c):
    return a[0]*b[1]*c[2]+a[1]*b[2]*c[0]+a[2]*b[0]*c[1]-a[2]*b[1]*c[0]-a[1]*b[0]*c[2]-a[0]*b[2]*c[1]


def isIntersectToTriangle(triangle, segment, option=""):
    # triangleと線分segmentが交差しているかの判定を行う関数.
    # option: line -> 線分ではなく, 始点から伸びる半直線と平面が交差するかを判定.
    # segment: [始点, 終点]

    v0 = np.array(triangle[0])
    v1 = np.array(triangle[1])
    v2 = np.array(triangle[2])

    # v0, v1, v2, およびsegment[0], segment[1]に重複した要素が存在していないか検証. もし重複した要素が存在していない場合は以下を実行
    dup = len(Set2D.set2D([v0, v1, v2]) &
              Set2D.set2D([segment[0], segment[1]]))
    if dup == 0:
        origin = np.array(segment[0])  # 線分の開始点
        ray = np.array(segment[1]) - origin  # 線分の終点
        invRay = -1 * ray  # 終点ベクトルの反対
        edge1 = v1 - v0
        edge2 = v2 - v0

        denominator = det3x3(edge1, edge2, invRay)

        if denominator > 0:
            d = origin - v0
            u = det3x3(d, edge2, invRay) / denominator
            v = det3x3(edge1, d, invRay) / denominator
            # 表面からの交差判定なのでtの符号は逆向きにする.
            t = -det3x3(edge1, edge2, d) / denominator

            # Debug
            # print("u: " + str(u))
            # print("v: " + str(v))
            # print("t: " + str(t))

            if 0 <= u <= 1:
                if 0 <= v and u + v <= 1:
                    # 距離がマイナスの場合は交差していない
                    if option == "half-line":
                        if t >= 0:
                            return True
                    else:
                        if 1 >= t >= 0:
                            return True

        origin = np.array(segment[1])  # 線分の開始点
        ray = np.array(segment[0]) - origin  # 線分の終点
        invRay = -1 * ray  # 終点ベクトルの反対

        denominator = det3x3(edge1, edge2, invRay)

        if denominator > 0:
            d = origin - v0
            u = det3x3(d, edge2, invRay) / denominator
            v = det3x3(edge1, d, invRay) / denominator
            t = det3x3(edge1, edge2, d) / denominator

            # Debug
            # print("u: " + str(u))
            # print("v: " + str(v))
            # print("t: " + str(t))

            if 0 <= u <= 1:
                if 0 <= v and u + v <= 1:
                    if option == "half-line":
                        if t >= 0:
                            return True
                    else:
                        if 1 >= t >= 0:
                            return True

                    # 距離がマイナスの場合は交差していない

    return False
