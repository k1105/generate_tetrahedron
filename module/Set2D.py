def set2D(seq):
    # 2次元配列を集合に変換する関数.
    # ref: https://qiita.com/uuuno/items/b714d84ca2edbf16ea19
    return set(map(tuple, seq))
