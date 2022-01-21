import numpy as np
import math
import numpy.linalg as LP


def GenerateVertex(tetra, tetras, k, vert, gene):

    pi = math.pi

    input = k * tetra.getNeighborInformationVector()+(1 - k) * \
        tetra.getPositionInformationVector(
            vert, tetras)  # 入力ベクトル. 注目要素の近傍情報ベクトルと位置情報ベクトルのそれぞれにk, 1-k倍をして算出.

    input_norm = LP.norm(input)

    # 0 <= theta < 2pi
    theta = (math.atan2(input[1], input[0]) + 2 * pi) % (2 * pi)
    # -pi/2 <= phi < pi/2
    phi = math.atan2(input[2], abs(input[1]))

    if 0 <= theta < 2*pi:  # 定義域内であることの確認
        theta_num = int(theta / (pi / 4)) + 1
    else:
        print("theta error!")
        print(str(theta / pi) + "pi")

    if -pi/2 <= phi < pi/2:  # 定義域内であることの確認
        phi_num = int((phi + pi / 2) / (pi / 4)) + 1
    else:
        print("phi error!")

    if not 1 <= theta_num <= 8:
        print("theta_num error!")

    if not 1 <= phi_num <= 4:
        print("phi_num error!")

    state = theta_num + 8 * (phi_num - 1)  # 1 < state < 32

    out_theta = theta + gene["theta"][state-1] * pi / 4
    out_phi = phi + gene["phi"][state-1] * pi / 8

    output = input_norm * np.array([math.cos(out_phi)*math.cos(out_theta),
                                    math.cos(out_phi)*math.sin(out_theta), math.sin(out_phi)])

    return list(output)
