## 生成された四面体の頂点情報の出力(Processingで出力可能)
c = 5 ## 出力時のスケール

for i in range(0, len(tetra_set)):
    tetra = tetra_set[i]
    for j in range(0, 4):
        print("beginShape();")
        s = getTriangle(tetra, j)
        for k in range(0, 3):
            print("vertex("+str(s[k].x*c)+", "+str(s[k].y*c)+", "+str(s[k].z*c)+");")
        print("endShape();")
        print("\n")