import numpy as np
import numpy.linalg as LP
from . import Set2D

def isIntersect (triangle, line):
    ## triangleとlineが交差しているかの判定を行う関数.
    ## line: [重心, 頂点]
    origin = np.array(line[0]) ## 線分の開始点
    ray = np.array(line[1]) ## 線分の終点
    invRay = -1 * ray ## 終点ベクトルの反対
    v0 = np.array(triangle[0])
    v1 = np.array(triangle[1])
    v2 = np.array(triangle[2])
    
    if len(Set2D.set2D([v0, v1, v2]) & Set2D.set2D([origin, ray])) == 0:
        
        edge1 = v1 - v0
        edge2 = v2 - v0

        denominator = LP.det([edge1, edge2, invRay])

        if denominator > 0 :
            d = origin - v0
            u = LP.det([d, edge2, invRay]) / denominator
            if 0 <= u <= 2.5: ## note: ここをいくつの値に設定するかで全体の形状に影響を与えそう.
                v = LP.det([edge1, d, invRay]) / denominator
                if 0 <= v and u + v <= 2.5: ## note: ここをいくつの値に設定するかで全体の形状に影響を与えそう.
                    t = LP.det([edge1, edge2, d]) / denominator

                    ## 距離がマイナスの場合は交差していない
                    if t >= 0 :
                        return True

        origin = np.array(line[1]) ## 線分の開始点
        ray = np.array(line[0]) ## 線分の終点
        invRay = -1 * ray ## 終点ベクトルの反対

        denominator = LP.det([edge1, edge2, invRay])

        if denominator > 0 :
            d = origin - v0
            u = LP.det([d, edge2, invRay]) / denominator
            if 0 <= u <= 1.0: ## note: ここをいくつの値に設定するかで全体の形状に影響を与えそう.
                v = LP.det([edge1, d, invRay]) / denominator
                if 0 <= v and u + v <= 1.0: ## note: ここをいくつの値に設定するかで全体の形状に影響を与えそう.
                    t = LP.det([edge1, edge2, d]) / denominator

                    ## 距離がマイナスの場合は交差していない
                    if t >= 0 :
                        return True
    
    return False

def isCollide (candidate_tetra, tetra_set):
    
    ## 衝突判定
    for j in reversed(range(0, len(tetra_set))):
        target_tetra = tetra_set[j]
        ## 外接球を用いた大まかな衝突判定
        if LP.norm(candidate_tetra.circumcenter-target_tetra.circumcenter) <= target_tetra.circumradius + candidate_tetra.circumradius:
            c_p = candidate_tetra.point
            ## 新規に作成される辺候補のリスト
            candidate_edges = [[c_p[0] ,c_p[3]], [c_p[1] ,c_p[3]], [c_p[2] ,c_p[3]]]

            ## 新規に作成される面候補のリスト
            candidate_triangles = [
                [c_p[0], c_p[1], c_p[3]],
                [c_p[0], c_p[2], c_p[3]],
                [c_p[1], c_p[2], c_p[3]]
            ]

            for k in range(4):
                for l in range(3):
                    ## 新しく生成される辺と既存の面が交差するかどうかの判定
                    if isIntersect(target_tetra.triangle[k], candidate_edges[l]):
                        return True

            for m in range(6):
                for n in range(3):
                    ## 新しく生成される面と既存の辺が交差するかどうかの判定
                    if isIntersect(candidate_triangles[n], target_tetra.edge[m]): 
                        return True
    return False