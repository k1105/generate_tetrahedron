import numpy as np
import numpy.linalg as LP
from module import Set2D


class Tetra():
    def __init__(self, p0, p1, p2, p3, index):
        p0 = list(p0)
        p1 = list(p1)
        p2 = list(p2)
        p3 = list(p3)

        self.point = [p0, p1, p2, p3]
        self.isCreated = [0, 0, 0, 0]
        self.triangle = [[p1, p2, p3], [
            p0, p2, p3], [p0, p1, p3], [p0, p1, p2]]
        self.edge = [
            [p0, p1],
            [p0, p2],
            [p0, p3],
            [p1, p2],
            [p1, p3],
            [p2, p3]
        ]
        self.circumcenter, self.circumradius = calcCircumsphere(
            [p0, p1, p2, p3])
        self.index = index
        self.childVertex = [None, None, None, None]
        self.centroid = (np.array(p0) + np.array(p1) +
                         np.array(p2) + np.array(p3)) / 4

    def findTriangleIndex(self, p0, p1, p2):
        # tetraが持つ三角形のうち、p0, p1, p2からなる三角形に一致するものを返す関数.
        for index in range(4):
            # print(self.triangle[index])
            if len(Set2D.set2D(self.triangle[index]) & Set2D.set2D([p0, p1, p2])) == 3:
                return index

        # 上のreturnが実行されなかった場合 = p0, p1, p2からなる三角形は存在しない
        print("error: there's no triangle in tetra: "+str([p0, p1, p2]))
        print("tetra's point: "+str(self.point))
        return -1

    def getNeighborInformationVector(self):
        sum = [0, 0, 0]
        for i in range(4):
            if self.childVertex[i] != None:  # 生成されていた場合
                s = self.triangle[i]
                c = (np.array(s[0]) + np.array(s[1]) + np.array(s[2])) / 3
                p = self.childVertex[i]
                vec = p - c
                sum += vec

        return np.array(sum)

    def getPositionInformationVector(self, vert, d_max):
        d = LP.norm(self.centroid - vert)
        if d == 0:  # NOTE: d == 0の場合のハンドリングについては要検討. 現在暫定的に３次の0ベクトルを返している.
            return np.array([0, 0, 0])
        e = (self.centroid - vert) / d

        return np.array((d_max - d) * e)

    def setChildVertex(self, index, vertex):
        # print(type(vertex))
        self.childVertex[index] = list(vertex)


def calcCircumsphere(point):
    # 外接球の半径と外点を求める関数
    p0 = np.array(point[0])
    p1 = np.array(point[1])
    p2 = np.array(point[2])
    p3 = np.array(point[3])
    matrix = [p0-p1, p0-p2, p2-p3]

    # 外接円の外点
    circumcenter = 0.5 * np.dot(LP.inv(matrix), [LP.norm(p0)**2-LP.norm(
        p1)**2, LP.norm(p0)**2-LP.norm(p2)**2, LP.norm(p2)**2-LP.norm(p3)**2])
    # 外接円の半径
    circumradius = LP.norm(p0 - circumcenter)

    return circumcenter, circumradius
