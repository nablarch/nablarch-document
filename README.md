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

## 図の作成方法
図はPlantUMLで作成します。原本（`.puml`）と生成物（`.png`）を、ページと同じ階層の`images/<ページ名>/`に同じ名前で置き、両方をコミットします。ドキュメントのビルドは図を生成しません。

### 前提
* Java 17
* plantuml.jar（`https://github.com/plantuml/plantuml/releases/download/v1.2025.4/plantuml-1.2025.4.jar`）
* 日本語フォント Noto Sans JP（`https://github.com/notofonts/noto-cjk/raw/main/Sans/Variable/TTF/Subset/NotoSansJP-VF.ttf`をフォントディレクトリに置き、`fc-cache -f`を実行する）

Graphvizは不要です。各`.puml`の先頭に`!pragma layout smetana`と`skinparam defaultFontName "Noto Sans JP"`を書きます。

### 生成
```bash
java -Djava.awt.headless=true -jar plantuml.jar -tpng -charset UTF-8 <ディレクトリ>/*.puml
```

### 規則
* ファイル名は`<見せるもの>_<種類>`。英小文字のsnake_case・ASCIIのみ。種類は`class`・`sequence`・`layout`・`components`・`flow`の5つ
* 同じ種類のページの同じ図は同じファイル名にする（例: `implementation/request_unit_test/images/{web,batch,mom}/execute_sequence.png`）
* 図は本文の可視化であり、本文に無い事実を入れない
* 用語は`.rn/20260724-ntf-yaml-support/mapping/glossary.md`の正表記に従う
* 画面キャプチャ（`.png`のみ）は本規則の対象外

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
