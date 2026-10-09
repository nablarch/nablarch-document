# javasphinx (vendored)

本ディレクトリは、Sphinx拡張 [javasphinx](https://github.com/bronto/javasphinx) 0.9.15
（Copyright 2012-2015 Bronto Software, Inc. and contributors / Apache License 2.0）のうち、
本ドキュメントのビルドに必要な部分を同梱（vendoring）したものです。
ライセンス条文は同梱の [LICENSE](./LICENSE) を参照してください。

## 同梱の経緯

- 原本の javasphinx は2019年にアーカイブされ保守終了しており、現行のSphinx
  （4.0以降）では起動できない（`sphinx.locale.l_` の削除による ImportError）。
- 保守されたフォーク・後継パッケージは存在しないため、外部パッケージへの依存を
  やめ、必要最小部分をリポジトリ内で管理する。

## 同梱対象と原本からの変更点

同梱対象: `__init__.py` / `domain.py` / `extdoc.py` / `formatter.py` / `util.py`
（`apidoc.py` / `compiler.py` / `htmlrst.py` はビルドで未使用のため同梱しない。
これにより lxml / beautifulsoup4 / future への依存が不要になる）

原本からの変更点は次の2点のみ:

1. `domain.py`: `from sphinx.locale import l_` → `from sphinx.locale import _`
   （`l_` はSphinx 4.0で削除された。PyPIの javasphinx-workaround 0.9.15 と同一の修正）
2. `extdoc.py`: `sphinx.util.nodes.split_explicit_title` の利用をやめ、旧来の
   明示タイトル解釈（`<(.*?)>$` 相当）をロール内に実装。Sphinx 4以降は正規表現が
   `<([^<]*?)>$` に変更され、ターゲットに `<` を含む記法
   （コンストラクタ参照 `Class.<init>(...)`）を解釈できないため。
   この解釈は `:java:extdoc:` ロール内に閉じており、他のロールには影響しない。

## 利用箇所

- `:java:extdoc:` ロール（既存Javadoc URLへのリンク生成）: 日英計約3,900箇所
- `.. java:method::` ディレクティブ（メソッドシグネチャの整形表示）: 日英各1箇所
  （シグネチャ解析のため `javalang` に依存する。requirements.txt で管理）
