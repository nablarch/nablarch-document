# nablarch-document
OSS版Nablarchドキュメントです。

## 前提
本ドキュメントはSphinxでビルドします。  

## 環境構築
WindowsまたはDockerを想定しています。
### Windows
#### ドキュメントビルド環境
Python 3.8.x〜3.10.x（3.11以降は不可）および依存ライブラリをインストールします。

依存ライブラリの一部（docutils-ast-writer）はsetuptools 58以降ではインストールできないため、先にsetuptoolsを固定してからインストールします。
```sh
pip install setuptools==57.5.0 wheel
pip install --no-build-isolation -r requirements.txt
```
※ Python 3.10を使用する場合、標準ライブラリparserモジュール削除の影響でコードブロックのハイライト判定が変わります。Dockerイメージには互換シムを組み込み済みです（詳細はDockerfileのコメントを参照）。Windowsでビルド成果物の完全一致が必要な場合はPython 3.8.x/3.9.xを使用するか、同様のシムを導入してください。
#### textlint実行環境
上記に加えて、以下をインストールします。
* Node.js（v22系LTS。v22.23.1で動作確認済み）
* npmで依存ライブラリをインストールします。
  ```sh
  npm install
  ```
#### linkcheck実行環境
* ドキュメントビルド環境と同一

### Docker
#### ドキュメントビルド環境及びtextlint実行環境及びlinkcheck実行環境
* 以下のコマンドでビルドしたイメージを使用してください。
  ```
  docker build -t nablarch-document-build .
  ```

## ドキュメントのビルド方法
### Windows
* 日本語ドキュメント
  ```bash
  make html ja
  ```
* 英語ドキュメント
  ```bash
  make html en
  ```

### Docker
* 日本語ドキュメント
  ```bash
  docker run --rm -v <リポジトリをクローンしたディレクトリ(フルパス)>:/root/document nablarch-document-build /bin/bash -c "cd /root/document; sphinx-build -d _build/.doctrees/ja -b html ja _build/html"
  ```
* 英語ドキュメント
  ```bash
  docker run --rm -v <リポジトリをクローンしたディレクトリ(フルパス)>:/root/document nablarch-document-build /bin/bash -c "cd /root/document; sphinx-build -d _build/.doctrees/en -b html en _build/html/en"
  ```


## textlintの実行方法
### textlintの設定ファイル
* 以下の設定ファイルを使用します。編集する必要はありません。

  | ファイル               | 説明           |
  |------------------------|----------------|
  | .textlintrc            | textlintの設定 |
  | .textlint/conf/prh.yml | 辞書           |

### 疎通確認
#### Windows
* 日本語ドキュメント
  ```sh
  ./node_modules/.bin/textlint .textlint/test/test.rst
  ```
  `./node_modules/.bin`をPATHに設定しておくと、以下のように実行できます。
  ```sh
  textlint .textlint/test/test.rst
  ```

#### Docker
* 日本語ドキュメント
  ```sh
  docker run --rm -v <リポジトリをクローンしたディレクトリ(フルパス)>:/root/document nablarch-document-build /bin/bash -c "cd /root/document; ../node_modules/.bin/textlint .textlint/test/test.rst"
  ```

### 実行
#### Windows
* 対象ディレクトリを指定してtextlintを起動します。
  ```sh
  ./node_modules/.bin/textlint ja/development_tools
  ```

#### Docker
* 対象ディレクトリを指定してtextlintを起動します。
  ```sh
  docker run --rm -v <リポジトリをクローンしたディレクトリ(フルパス)>:/root/document nablarch-document-build /bin/bash -c "cd /root/document; ../node_modules/.bin/textlint ja/development_tools"
  ```

## linkcheckの実行方法
### 実行
#### Docker
* 日本語ドキュメント
  ```bash
  docker run --rm -v <リポジトリをクローンしたディレクトリ(フルパス)>:/root/document nablarch-document-build /bin/bash -c "cd /root/document; sphinx-build -d _build/.doctrees/ja -b linkcheck ja _build/linkcheck/ja"
  ```

* 英語ドキュメント
  ```bash
  docker run --rm -v <リポジトリをクローンしたディレクトリ(フルパス)>:/root/document nablarch-document-build /bin/bash -c "cd /root/document; sphinx-build -d _build/.doctrees/en -b linkcheck en _build/linkcheck/en"
  ```
