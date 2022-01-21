from . import TriangleIntersectionDetection as tint
import numpy.linalg as LP


def SelectTarget(c_p, tetra):
    # 四面体のうち, 生成面となる三角形の番号を返す関数.
    # 引数: なし
    # 戻り値: 0~3の整数

    vector = [tetra.centroid, tetra.centroid-c_p]

    target = -1

    for i in range(0, 4):
        if tint.isIntersectToTriangle(tetra.triangle[i], vector, "half-line"):
            target = i
            break

    if target == -1 and LP.norm(c_p) != 0:
        # どの平面とも交差せず, またベクトルの大きさが0でなかった場合
        print('error!')
        print("triangles: \n"
              + str(list(map(lambda val: '{:.2f}'.format(val),
                    tetra.triangle[0]))) + "\n"
              + str(list(map(lambda val: '{:.2f}'.format(val),
                    tetra.triangle[1]))) + "\n"
              + str(list(map(lambda val: '{:.2f}'.format(val),
                    tetra.triangle[2]))) + "\n"
              + str(list(map(lambda val: '{:.2f}'.format(val),
                    tetra.triangle[3])))
              )
        print("line: \n"
              + str(vector))

    # 以下を任意の処理に変更
    return target
