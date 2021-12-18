import numpy as np
import random


def GenerateVertex(triangle, left_point):

    # ベクトルを作る
    center = (np.array(triangle[0])+np.array(triangle[1]) +
              np.array(triangle[2])) / 3  # 三角形の重心
    vector = np.array(left_point - center)  # 頂点-重心

    # 頂点を作る
    k = random.uniform(0.7, 1.5)  # ベクトルに掛け合わされる定数
    # candidate_point. 頂点候補（衝突判定によって棄却される可能性あり）
    return list(map(int, -1 * k * vector + center))
