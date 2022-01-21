import numpy as np
import math
import numpy.linalg as LP
from module import GetState as gs


def GenerateOutputVector(tetra, k, vert, d_max, gene):

    pi = math.pi

    input = k * tetra.getNeighborInformationVector()+(1 - k) * \
        tetra.getPositionInformationVector(
            vert, d_max)  # 入力ベクトル. 注目要素の近傍情報ベクトルと位置情報ベクトルのそれぞれにk, 1-k倍をして算出.

    input_norm = LP.norm(input)
    # 0 <= theta < 2pi
    theta = (math.atan2(input[1], input[0]) + 2 * pi) % (2 * pi)
    # -pi/2 <= phi < pi/2
    phi = math.atan2(input[2], abs(input[1]))

    state = gs.GetState(theta, phi)

    out_theta = theta + gene["theta"][state-1] * pi / 4
    out_phi = phi + gene["phi"][state-1] * pi / 8

    output = input_norm * np.array([math.cos(out_phi)*math.cos(out_theta),
                                    math.cos(out_phi)*math.sin(out_theta), math.sin(out_phi)])

    return list(output)
