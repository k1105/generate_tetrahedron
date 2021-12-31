# 生成された四面体の頂点情報の出力(Processingで出力可能)
c = 5  # 出力時のスケール

for i in range(0, len(tetras)):
    tetra = tetras[i]
    for j in range(0, 4):
        print("beginShape();")
        s = tetra.triangle[j]
        for k in range(0, 3):
            print("vertex("+str(s[k][0]*c)+", " +
                  str(s[k][1]*c)+", "+str(s[k][2]*c)+");")
        print("endShape();")
        print("\n")
