from module import PlaneCollisionDetection as pcol
import numpy as np
import json

# <sammary>
# plane_collision(ver0.0 2021.12.30)
# 入力された三角形, および線分の交差判定を行う.
# NOTE: 現在, 衝突しているにも拘らず正常に判定されないケースが確認されている.
# どのような場合にそうした誤った挙動をしてしまうのかについて, 様々な値を検討することで調査してほしい.
# </sammary>

triangle_open = open('triangle.json', 'r')
line_open = open('line.json', 'r')
triangle = json.load(triangle_open)
line = json.load(line_open)

p0 = triangle['tri1']['p0']
p1 = triangle['tri1']['p1']
p2 = triangle['tri1']['p2']

start = line['line1']['start']
end = line['line1']['end']

# if len(p0) != 3 and len(p1) != 3 and len(p2) != 3 and len(start) != 3 and len(end) != 3:
result = pcol.isIntersectToPlane([p0, p1, p2], [start, end])

if result:
    print('衝突しています')
else:
    print('衝突していません')

print('3角形の頂点：')
print(p0)
print(p1)
print(p2)
print('線分：')
print(start)
print(end)
# else:
#     print('入力された形式が正しくありません.')
