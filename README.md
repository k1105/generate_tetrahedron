## システム概要

Boxcel の考え方を拡張させ, 四面体を一つの単位として形状生成を行うプログラム.既に生成された四面体の面から新しい四面体をランダムで生成する操作を繰り返すことで, 総体としてもランダムな形状を作る.

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

1.  github からこのリポジトリをローカルに clone し, clone したディレクトリに移動.

```bash
$ git clone git@github.com:k1105/generate_tetrahedron.git
$ cd generate_tetrahedron
```

1. システムを実行するのに必要なライブラリをまとめてインストールするため, 以下を実行.

```bash
$ pip install -r requirements.txt
```

### 2 回目移行

1. github 上でシステムの更新が行われている可能性があるので, 毎回初めに pull してくる.

```bash
$ git pull origin master
```

1. システムを実行するのに必要なライブラリも増えている可能性があるので, 以下を実行.

```bash
$ pip install -r requirements.txt
```

### システムの実行

実行したいファイル名を指定して, 次のように実行.

```bash
$ python {filename}.py
```

## ファイル構成

- generate_tetrahedron.py
  = ランダムな四面体生成を行い, 生成された形状(stl 形式), processing で出力する用のコード(txt 形式)及び, 各四面体の関係をネットワーク図で表現したグラフ(png 形式)を出力する.
