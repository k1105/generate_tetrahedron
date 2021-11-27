## システム概要

Boxcel の考え方を拡張させ, 四面体を一つの単位として形状生成を行うプログラム.既に生成された四面体の面から新しい四面体をランダムで生成する操作を繰り返すことで, 総体としてもランダムな形状を作る.

<img width="1440" alt="スクリーンショット 2021-11-19 11 25 27" src="https://user-images.githubusercontent.com/47634358/143669165-e5aff56c-34bd-4b53-a717-212d1de08c02.png">

## 使用方法

### 初期設定

以下の設定は初回のみ実行する.

1. homebrew, python がインストールされているか確認.

```bash
$ brew --version
$ python --version
```

いずれかで`command not found.`が表示された場合,

```bash
### homebrewのインストール
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

python は,[progate のサイト](https://prog-8.com/docs/python-env)を参考にインストール.

2.  github からこのリポジトリをローカルに clone し, clone したディレクトリに移動.

```bash
$ git clone git@github.com:k1105/generate_tetrahedron.git
$ cd generate_tetrahedron
```

3. システムを実行するのに必要なライブラリをまとめてインストールするため, 以下を実行.

```bash
$ pip install -r requirements.txt
```

### 2 回目以降

1. github 上でシステムの更新が行われている可能性があるので, 毎回初めに pull してくる.

```bash
$ git pull origin master
```

2. システムを実行するのに必要なライブラリも増えている可能性があるので, 以下を実行.

```bash
$ pip install -r requirements.txt
```

### システムの実行

実行したいファイル名を指定して, 次のように実行.

```bash
$ python {filename}.py
```

## ファイル構成

- main.py
  = ランダムな四面体生成を行い, 生成された形状(stl 形式), processing で出力する用のコード(txt 形式: comming soon..)及び, 各四面体の関係をネットワーク図で表現したグラフ(png 形式)を出力する.
  
![image](https://user-images.githubusercontent.com/47634358/143669189-2bb7d877-f817-4e0e-9b90-51475638ef2a.png)


- module/Set2D.py
  = 2 次元配列を集合に変換する関数.

- module/TetraCollisionDetection.py
  = 四面体の衝突判定に必要な関数を持つモジュール.
