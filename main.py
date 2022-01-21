import random
import numpy as np
import time
import datetime
from module import Export as export
from module import GenerateObject as gobj
from module import InitializeGeneArray as iga

####### MAIN #######
start = time.time()
# 生成したい四面体の個数をここで指定:
num = int(input('生成する四面体の個数の下限 -> '))
threshold = int(input('くっつける頂点の距離の閾値-> '))  # 2つの頂点間の距離が, 閾値以下の場合に四面体同士がくっつく.
k = float(input('合成比率(0<k<1)-> '))
d_max = float(input('d_max(>=0) -> '))

vert = [0, 0, 0]
vert[0] = float(input('頂部のx座標 -> '))
vert[1] = float(input('頂部のy座標 -> '))
vert[2] = float(input('頂部のz座標 -> '))

print('generate '+str(num)+' tetrahedron.')

# random seedを現在時刻に指定
# pythonの場合, random seedは明示せずとも実行のたびに異なるseedを設定してくれるが, そのseedがいくつに設定されているのか, またどのタイミングで値が切り替わるのか把握できないので, 実行のたびに確実にseedが更新されるようマニュアルで指定している.
random.seed(datetime.datetime.now())

# 遺伝情報
# 頂部の計算

# 状態番号を保有する配列の生成

gene_array = iga.InitializeGeneArray()

# 形状生成
# gene_final: 最終的な形状を生成した際に使用された遺伝配列.
tetras, edges, gene_final = gobj.GenerateObject(
    num, threshold, k, vert, d_max, gene_array)

elapsed_time = time.time() - start
print("\n"+"completed. ({:.4g}".format(elapsed_time) + "s)")

# 書き出し処理
export.Export(tetras, edges, num, threshold, k, d_max, vert, gene_final)
