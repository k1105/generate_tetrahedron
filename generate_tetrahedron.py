import random
import numpy as np
import numpy.linalg as LP
import itertools
import time


class Tetra():
    def __init__(self, p0, p1, p2, p3):
        self.point = [p0, p1, p2, p3]
        self.isCreated = [0, 0, 0, 0]
        self.triangle = [[p1, p2, p3], [p0, p2, p3], [p0, p1, p3], [p0, p1, p2]]
        self.edge = [
                        [p0, p1],
                        [p0, p2],
                        [p0, p3],
                        [p1, p2],
                        [p1, p3],
                        [p2, p3]
                    ]
        self.circumcenter, self.circumradius = calcCircumsphere([p0, p1, p2, p3])
        

def set2D(seq):
    ## 2次元配列を集合に変換する関数.
    ## ref: https://qiita.com/uuuno/items/b714d84ca2edbf16ea19
    return set(map(tuple, seq))

def isIntersect (triangle, line):
    ## triangleとlineが交差しているかの判定を行う関数.
    ## line: [重心, 頂点]
    origin = np.array(line[0]) ## 線分の開始点
    ray = np.array(line[1]) ## 線分の終点
    invRay = -1 * ray ## 終点ベクトルの反対
    v0 = np.array(triangle[0])
    v1 = np.array(triangle[1])
    v2 = np.array(triangle[2])
    
    if len(set2D([v0, v1, v2]) & set2D([origin, ray])) == 0:
        
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

def isCollide (candidate_tetra, tetra_set):
    
    ## 衝突判定
    for j in reversed(range(0, len(tetra_set))):
        target_tetra = tetra_set[j]
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

def calcCircumsphere(point):
    ### 外接球の半径と外点を求める関数
    p0 = np.array(point[0])
    p1 = np.array(point[1])
    p2 = np.array(point[2])
    p3 = np.array(point[3])
    matrix = [p0-p1, p0-p2, p2-p3]

    ### 外接円の外点
    circumcenter = 0.5 * np.dot(LP.inv(matrix) , [LP.norm(p0)**2-LP.norm(p1)**2, LP.norm(p0)**2-LP.norm(p2)**2, LP.norm(p2)**2-LP.norm(p3)**2])
    ### 外接円の半径
    circumradius = LP.norm(p0 - circumcenter)
    
    return circumcenter, circumradius

####### MAIN #######
start = time.time()

## 生成したい四面体の個数をここで指定:
num = 2000
threshold = 20 ##くっつける頂点の距離の閾値. 2つの頂点間の距離が, 閾値以下の場合に四面体同士がくっつく.

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
            s = tetra_i.triangle[target] ##tetra_i上のtarget番目の三角形.
            
            ## ベクトルを作る
            center = (np.array(s[0])+np.array(s[1])+np.array(s[2])) / 3 ## 三角形の重心
            left_point = np.array(tetra_i.point[target]) ## 三角形sに含まれないtetra_iの頂点
            vector = np.array(left_point - center) ##頂点-重心

            ## 頂点を作る
            k = random.uniform(0.7, 1.5) ##ベクトルに掛け合わされる定数
            c_p = list(map(int, -1 * k * vector + center)) ## candidate_point. 頂点候補（衝突判定によって棄却される可能性あり）
            ## print(c_p)
            
            candidate_tetra = Tetra(s[0], s[1], s[2], c_p)
            
            if not isCollide(candidate_tetra, tetra_set):
                ## 判定をPassした場合 :
                candidate_tetra.isCreated[3] = 1 ##生成した時点で接してる四面体
                
                ## merge処理
                merged = False
                
                for target_tetra in tetra_set:
                    if merged:
                        break

                    ## edgeは元々のままだと３次元配列. 重複するedgeを検出する処理のために2次元配列に平坦化.
                    candidate_edges = tuple(map(list, (map(itertools.chain.from_iterable, candidate_tetra.edge))))
                    target_edges = tuple(map(list, (map(itertools.chain.from_iterable, target_tetra.edge))))

                    ## 共有する頂点の数を検出.
                    ## 0 ... 四面体は接していない
                    ## 1 ... 四面体は一点でのみ接する
                    ## 2 ... 四面体は1辺を共有する
                    ## 3 ... 四面体は1面を共有する
                    if len(set2D(candidate_tetra.point) & set2D(target_tetra.point)) == 2: ## 1つの辺を共有する場合
                        candidate_point = candidate_tetra.point[3] ## 末尾の頂点.
                        ## くっつく可能性のある頂点 = 共有している辺以外の頂点２つ.　= 「candidate_tetraとtarget_tetraに共通しない要素」とtarget_tetraに共通する要素
                        target_points = list(map(list, (set2D(candidate_tetra.point) ^ set2D(target_tetra.point)) & set2D(target_tetra.point)))
                        
                        ## 2つの四面体が共有する辺.
                        shared_edge = list(map(list, set2D(candidate_tetra.point) & set2D(target_tetra.point)))
                        
                        ## 発生率はかなり低いが, 稀にcandidate_pointがshared_edgeに含まれる
                        ## =新規で作成された頂点が既存の他の頂点にたまたま一致することがある.
                        ## この場合は何もしないので、 それをハンドリング.
                        if not candidate_point in shared_edge:

                            for target_point in target_points:                            
                                if LP.norm(np.array(target_point)-np.array(candidate_point)) < threshold: ##閾値以下の場合

                                    ##isCreatedの更新
                                    ## candidate_tetraにおける, candidate_point, 共通する辺の頂点から成る三角形の番号を取得
                                    candidate_updated = False
                                    target_updated = False

                                    for k in range(0, 4):
                                        if len(set2D(candidate_tetra.triangle[k]) & set2D([shared_edge[0], shared_edge[1], candidate_point])) == 3:
                                            candidate_tetra.isCreated[k] = 1
                                            ## print("candidateのisCreated更新")
                                            candidate_updated = True
                                            break

                                    if not candidate_updated: ## debug
                                        print("error: Candidate's isCreated Not Updated.")
                                        
                                    ## 既存の四面体における, target_point, 共通する辺の頂点から成る三角形の番号を取得
                                    for k in range(0, 4):
                                        if len(set2D(target_tetra.triangle[k]) & set2D([shared_edge[0], shared_edge[1], target_point])) == 3: 
                                            target_tetra.isCreated[k] = 1
                                            ## print("targetのisCreated更新")
                                            target_updated = True
                                            break

                                    if not target_updated: ## debug
                                        print("error: Target's isCreated Not Updated.")
                                        
                                    if candidate_updated == False or target_updated == False:
                                        print("candidate_tetra.point: ")
                                        print([candidate_tetra.point[0], candidate_tetra.point[1], candidate_tetra.point[2], candidate_tetra.point[3]])
                                        print("target_tetra.point: ")
                                        print([target_tetra.point[0], target_tetra.point[1], target_tetra.point[2], target_tetra.point[3]])
                                        print("candidate_point: ")
                                        print(candidate_point)
                                        print("target_point: ")
                                        print(target_point)
                                        print("target_points: ")
                                        print(target_points)
                                        print("shared_edge: ")
                                        print(shared_edge)
                                        print("target_triangles: ")
                                        print(target_tetra.triangle)

                                    candidate_tetra.point[3] = target_point
                                    ## print("merge")
                                    merged = True
                                    break

                
                ## 一覧に追加
                new_tetra = Tetra(candidate_tetra.point[0], candidate_tetra.point[1], candidate_tetra.point[2], candidate_tetra.point[3])
                
                tetra_set.append(new_tetra)
                ## isCreatedを更新
                tetra_set[i].isCreated[target] = 1
                
                print("\r"+"processing...("+'{:.1f}'.format((len(tetra_set)-1)/num*100)+"%)",end="")
                if(len(tetra_set)-1 == num): break

elapsed_time = time.time() - start
print("\n"+"completed. ({:.4g}".format(elapsed_time) + "s)")
