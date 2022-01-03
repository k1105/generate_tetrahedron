import numpy as np
import math
import numpy.linalg as LP


def GenerateVertex(tetra, tetras, k, random_list):

    pi = math.pi

    input = k * tetra.getNeighborInformationVector()+(1 - k) * \
        tetra.getPositionInformationVector(
            tetras)  # 入力ベクトル. 注目要素の近傍情報ベクトルと位置情報ベクトルのそれぞれにk, 1-k倍をして算出.

    input_norm = LP.norm(input)

    # 0 < theta < 2pi
    theta = (math.atan2(input[1], input[0]) + pi) % (pi / 2)
    # -pi/2 < phi < pi/2
    phi = (math.atan2(input[2], input[1]) + pi) % pi - pi / 2

    theta_num = int(theta / (math.pi/4)) + 1
    phi_num = int((phi + pi / 2) / (pi / 4)) + 1

    out_theta = theta + random_list["theta"][theta_num-1] * pi / 4
    out_phi = phi + random_list["phi"][phi_num-1] * pi / 8

    output = input_norm * np.array([math.cos(out_phi)*math.cos(out_theta),
                                    math.cos(out_phi)*math.sin(out_theta), math.sin(out_phi)])

    return list(output)
