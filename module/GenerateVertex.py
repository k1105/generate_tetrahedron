import numpy as np
import random
import math


def GenerateVertex(tetra, tetras, target, k, random_list):

    triangle = tetra.triangle[target]
    left_point = np.array(tetra.point[target])

    input = k * tetra.getNeighborInformationVector()+(1 - k) * \
        tetra.getPositionInformationVector(
            tetras)  # 入力ベクトル. 注目要素の近傍情報ベクトルと位置情報ベクトルのそれぞれにk, 1-k倍をして算出.

    # 0 < theta < 2pi
    theta = math.atan2(input[1], input[0]) + math.pi
    # -pi/2 < phi < pi/2
    phi = (math.atan2(input[2], input[1]) + math.pi) % math.pi - math.pi / 2

    theta_num = int(theta / (math.pi/4)) + 1
    phi_num = int((phi + math.pi / 2) / (math.pi / 4)) + 1

    print(str(theta_num) + ' -> ' + str(random_list["theta"][theta_num-1]))
    print(str(phi_num) + ' -> ' + str(random_list["phi"][phi_num-1]))

    # ベクトルを作る
    center = (np.array(triangle[0])+np.array(triangle[1]) +
              np.array(triangle[2])) / 3  # 三角形の重心
    vector = np.array(left_point - center)  # 頂点-重心

    # 頂点を作る
    c = random.uniform(0.7, 1.5)  # ベクトルに掛け合わされる定数
    # candidate_point. 頂点候補（衝突判定によって棄却される可能性あり）
    return list(map(int, -1 * c * vector + center))
