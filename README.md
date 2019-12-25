# nablarch-document
OSS版Nablarchドキュメントです。

## 前提
本ドキュメントはSphinxでビルドすることを前提としています。
また、幾つかのプラグインを使用しているため事前にインストールする必要があります。

以下が必要なものとなります。
* Sphinx(1.6.3)
* javasphinx(0.9.15)
* sphinx-rtd-theme(0.2.4)

## ドキュメントのビルド方法
```bash
make html
```

## textlintの実行方法


### 環境構築

#### Node.js

Node.jsをインストールします。
（v8.9.3で動作確認済み）

#### npm install

npmで依存ライブラリをインストールします。

```sh
npm install
```

#### docutils-ast-writer

[textlint-plugin-rst](https://github.com/jimo1001/textlint-plugin-rst)の依存ライブラリである
docutils-ast-writerをインストールします。

```sh
pip install docutils-ast-writer
```

### 疎通確認

```sh
./node_modules/.bin/textlint .textlint/test/test.rst
```

`./node_modules/.bin`をPATHに設定しておくと、以下のように実行できる。

```sh
textlint .textlint/test/test.rst
```

### 実行

対象ディレクトリを指定してtextlintを起動します。

```sh
./node_modules/.bin/textlint development_tools
```

### 設定ファイル

| ファイル               | 説明           |
|------------------------|----------------|
| .textlintrc            | textlintの設定 |
| .textlint/conf/prh.yml | 辞書的なやつ   |

