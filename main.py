import random
import numpy as np
import time
import datetime
from module import Export as export
from module import GenerateObject as gobj

####### MAIN #######
start = time.time()
# 生成したい四面体の個数をここで指定:
num = int(input('生成する四面体の個数(>2) -> '))
threshold = int(input('くっつける頂点の距離の閾値-> '))  # 2つの頂点間の距離が, 閾値以下の場合に四面体同士がくっつく.
k = float(input('合成比率(0<k<1)-> '))

print('generate '+str(num)+' tetrahedron.')

# random seedを現在時刻に指定
# pythonの場合, random seedは明示せずとも実行のたびに異なるseedを設定してくれるが, そのseedがいくつに設定されているのか, またどのタイミングで値が切り替わるのか把握できないので, 実行のたびに確実にseedが更新されるようマニュアルで指定している.
random.seed(datetime.datetime.now())

# 遺伝情報
# 頂部の計算
vert = np.array([random.uniform(-100, 100),
                 random.uniform(-100, 100), random.uniform(-100, 100)])

# 状態番号を保有する配列の生成
weight_list = [random.uniform(0.8, 1.2) for i in range(32)]
theta_list = [random.randint(1, 8) for i in range(32)]
phi_list = [random.randint(1, 8) for i in range(32)]

gene_array = {"weight": weight_list, "theta": theta_list, "phi": phi_list}

# 形状生成処理　開始
tetras, edges = gobj.GenerateObject(num, threshold, k, vert, gene_array)

# 形状生成処理　終了

elapsed_time = time.time() - start
print("\n"+"completed. ({:.4g}".format(elapsed_time) + "s)")

export.Export(tetras, edges)
