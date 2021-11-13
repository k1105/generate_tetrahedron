import random
import copy
import numpy as np
import numpy.linalg as LP


class Tetra():
    def __init__(self, p0, p1, p2, p3):
        self.point = [p0, p1, p2, p3]
        self.isCreated = [0, 0, 0, 0]
        self.triangle = [[p0, p1, p2], [p0, p1, p3], [p0, p2, p3], [p1, p2, p3]]
        self.edge = [
                        [p0, p1],
                        [p0, p2],
                        [p0, p3],
                        [p1, p2],
                        [p1, p3],
                        [p2, p3]
                    ]

def getTriangle(tetra, num):
    ## 四面体tetraに含まれる面numの情報を返す関数.
    point_list = copy.copy(tetra.point) ##point_list=四面体tetraの持つ4つの頂点.
    del point_list[num] ##point_listからnum番目の頂点を削除.→point_listは3つの頂点情報を持つ事になる=三角形の頂点.
    return point_list

def isIntersect (triangle, line):
    ## triangleとlineが交差しているかの判定を行う関数.
    ## line: [重心, 頂点]
    origin = np.array(line[0]) ## 線分の開始点
    ray = np.array(line[1]) ## 線分の終点
    invRay = -1 * ray ## 終点ベクトルの反対
    v0 = np.array(triangle[0])
    v1 = np.array(triangle[1])
    v2 = np.array(triangle[2])
    
    if not(all(v0==origin) or all(v1==origin) or all(v2==origin) or all(v0==ray) or all(v1==ray) or all(v2==ray)):
        
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
            if 0 <= u <= 2.5: ## note: ここをいくつの値に設定するかで全体の形状に影響を与えそう.
                v = LP.det([edge1, d, invRay]) / denominator
                if 0 <= v and u + v <= 2.5: ## note: ここをいくつの値に設定するかで全体の形状に影響を与えそう.
                    t = LP.det([edge1, edge2, d]) / denominator

                    ## 距離がマイナスの場合は交差していない
                    if t >= 0 :
                        return True
    
    return False

def isCollide (candidate_edges, candidate_triangles, tetra_set):
    ## 衝突判定
    for j in reversed(range(0, len(tetra_set))):
        target_tetra = tetra_set[j]
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

## 生成したい四面体の個数をここで指定:
num = 100

print('generate '+str(num)+' tetrahedron.')

##最初の四面体を作成
tetra = Tetra([10 ,10 ,10], [-10,-10,10], [10,-10,-10], [-10, 10, -10])

tetra_set = []

## 配列に追加
tetra_set.append(tetra)

while len(tetra_set) < num:
    for i in range(0, len(tetra_set)):
        ## i 番目の四面体情報を取得
        tetra_i = tetra_set[i]
        
        ## i 番目の四面体情報をもとに新しい四面体を作成
        ## 面を選ぶ
        target = random.randint(0, 3)
        
        if tetra_i.isCreated[target] == 0:
            s = getTriangle(tetra_i, target) ##tetra_i上のtarget番目の三角形.
            
            ## ベクトルを作る
            center = (np.array(s[0])+np.array(s[1])+np.array(s[2])) / 3 ## 三角形の重心
            left_point = np.array(tetra_i.point[target]) ## 三角形sに含まれないtetra_iの頂点
            vector = np.array(left_point - center) ##頂点-重心

            ## 頂点を作る
            k = random.uniform(0.7, 1.5) ##ベクトルに掛け合わされる定数
            c_p = list(map(int, -1 * k * vector + center)) ## candidate_point. 頂点候補（衝突判定によって棄却される可能性あり）
            ## print(c_p)
            ## 新規に作成される辺候補のリスト
            candidate_edges = [[s[0] ,c_p], [s[1] ,c_p], [s[2] ,c_p]]
            
            ## 新規に作成される面候補のリスト
            candidate_triangles = [
                [s[0], s[1], c_p],
                [s[0], s[2], c_p],
                [s[1], s[2], c_p]
            ]
            
            if not isCollide(candidate_edges, candidate_triangles, tetra_set):
                ## 判定をPassした場合 :
                ## 四面体を生成 
                new_point = c_p
                new_tetra = Tetra(s[0], s[1], s[2], new_point)
                new_tetra.isCreated[3] = 1 ##生成した時点で接してる四面体
                ## 一覧に追加
                tetra_set.append(new_tetra)
                ## isCreatedを更新
                tetra_set[i].isCreated[target] = 1
                
                print("processing...("+'{:.1f}'.format((len(tetra_set)-1)/num*100)+"%)")

print("completed.")
