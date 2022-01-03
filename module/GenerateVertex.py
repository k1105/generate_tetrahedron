import numpy as np
import random
import math
import numpy.linalg as LP
from . import TriangleIntersectionDetection as tint


def GenerateVertex(tetra, tetras, target, k, random_list):

    pi = math.pi

    triangle = tetra.triangle[target]
    left_point = np.array(tetra.point[target])

    input = k * tetra.getNeighborInformationVector()+(1 - k) * \
        tetra.getPositionInformationVector(
            tetras)  # 入力ベクトル. 注目要素の近傍情報ベクトルと位置情報ベクトルのそれぞれにk, 1-k倍をして算出.

    input_norm = LP.norm(input)

    # 0 < theta < 2pi
    theta = math.atan2(input[1], input[0]) + pi
    # -pi/2 < phi < pi/2
    phi = (math.atan2(input[2], input[1]) + pi) % pi - pi / 2

    theta_num = int(theta / (math.pi/4)) + 1
    phi_num = int((phi + pi / 2) / (pi / 4)) + 1

    out_theta = theta + random_list["theta"][theta_num-1] * pi / 4
    out_phi = phi + random_list["phi"][phi_num-1] * pi / 8

    output = [tetra.centroid, input_norm * np.array([math.cos(out_phi)*math.cos(out_theta),
                                                     math.cos(out_phi)*math.sin(out_theta), math.sin(out_phi)]) + tetra.centroid]

    intersectionPlane = -1

    for i in range(0, 4):
        if tint.isIntersectToTriangle(tetra.triangle[i], output, "half-line"):
            intersectionPlane = i
            break

    if intersectionPlane == -1 and input_norm != 0:
        ## どの平面とも交差せず, またベクトルの大きさが0でなかった場合
        print('error!')
        print("triangles: \n"
              + str(tetra.triangle[0]) + "\n"
              + str(tetra.triangle[1]) + "\n"
              + str(tetra.triangle[2]) + "\n"
              + str(tetra.triangle[3]))
        print("line: \n"
              + str(output))
        print("output_theta: \n"
              + str(out_theta))
        print("output_phi: \n"
              + str(out_phi))
        print("norm: \n"
              + str(input_norm))

    # ベクトルを作る
    center = (np.array(triangle[0])+np.array(triangle[1]) +
              np.array(triangle[2])) / 3  # 三角形の重心
    vector = np.array(left_point - center)  # 頂点-重心

    # 頂点を作る
    c = random.uniform(0.7, 1.5)  # ベクトルに掛け合わされる定数
    # candidate_point. 頂点候補（衝突判定によって棄却される可能性あり）
    return list(map(int, -1 * c * vector + center))
