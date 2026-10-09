# nablarch-document
OSS版Nablarchドキュメントです。

## 前提
本ドキュメントはSphinx（9系）でビルドします。
Javadocリンク用のSphinx拡張javasphinxは、リポジトリに同梱したものを使用します（`_extensions/javasphinx/README.md`参照）。

ドキュメントビルド（HTML生成・linkcheck）環境とtextlint実行環境は、要求するPython・docutilsのバージョンが両立しないため分離しています。

| 環境 | Python | 依存定義 |
|------|--------|----------|
| ドキュメントビルド・linkcheck | 3.12以上 | requirements.txt（requirements.inから生成したlockファイル） |
| textlint | 3.10系（3.11以降は不可） | requirements-lint.txt |

## 環境構築
WindowsまたはDockerを想定しています。
### Windows
#### ドキュメントビルド環境
Python 3.12以上および依存ライブラリをインストールします。
```sh
pip install -r requirements.txt
```
#### textlint実行環境
Python 3.10系をインストールします（依存ライブラリの一部（docutils-ast-writer）がPython 3.11以降では動作しないため、ドキュメントビルド環境とは別のPython環境（venv等）を使用してください）。

docutils-ast-writerはsetuptools 58以降ではインストールできないため、先にsetuptoolsを固定してからインストールします。
```sh
pip install setuptools==57.5.0 wheel
pip install --no-build-isolation -r requirements-lint.txt
```
さらに、以下をインストールします。
* Node.js（v22系LTS。v22.23.1で動作確認済み）
* npmで依存ライブラリをインストールします。
  ```sh
  npm install
  ```
#### linkcheck実行環境
* ドキュメントビルド環境と同一

### Docker
#### ドキュメントビルド環境及びlinkcheck実行環境
* 以下のコマンドでビルドしたイメージを使用してください。
  ```
  docker build -t nablarch-document-build .
  ```
#### textlint実行環境
* 以下のコマンドでビルドしたイメージを使用してください。
  ```
  docker build --target lint -t nablarch-document-lint .
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
  docker run --rm -v <リポジトリをクローンしたディレクトリ(フルパス)>:/root/document nablarch-document-lint /bin/bash -c "cd /root/document; ../node_modules/.bin/textlint .textlint/test/test.rst"
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
  docker run --rm -v <リポジトリをクローンしたディレクトリ(フルパス)>:/root/document nablarch-document-lint /bin/bash -c "cd /root/document; ../node_modules/.bin/textlint ja/development_tools"
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
