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

### main.py
遺伝情報に基づく四面体生成を行い, 生成された形状(stl 形式), 各四面体の関係をネットワーク図で表現したグラフ(png 形式)を出力する. また, csv形式で以下のファイルが生成される:
- 最終的な形状生成に使用した遺伝配列 : gene_array.csv
- 出力された形状における各四面体の情報 : object_information.csv
- 形状生成に使用したパラメータ（最低要素数, 合成比率, マージ処理の閾値, d_max, 頂部の座標） : params.csv
  
![image](https://user-images.githubusercontent.com/47634358/143669189-2bb7d877-f817-4e0e-9b90-51475638ef2a.png)

main.pyの実行時, ``--file``オプションを指定すると, 遺伝配列についてcsvファイルから読み込ませることができる. 
```
python main.py --file <file_path>
```
例えば, 2022/1/22 3時46分50秒に実行した実行結果``out/20220122_034650``にある``gene_array.csv``を使用する場合は(もちろん, この名前の場所にファイルがあることが前提), 
```
python main.py --file out/20220122_034650/gene_array.csv
```
と実行.
