# 作業指示: `ntf-doc-09-pre.md` / `ntf-doc-09-pre-rev1.md` の全面撤回

配置先: `.rn/20260724-ntf-yaml-support/ntf-doc-09-pre-withdrawn.md`

対象ブランチ: `lovaizu/nablarch-document` の `work`

**この指示が、先行する2つの指示書（`ntf-doc-09-pre.md` および `ntf-doc-09-pre-rev1.md`）に優先する。**

---

## 撤回する

`verify_pages.py` の作成を**全面的に撤回する。作らない。** 着手済みの場合は中断し、下記の手順で元に戻す。

## 撤回の理由

`steering.md`（334行）と `design.md`（796行）を全量読んだ結果、提案した3つの検査がいずれも**既存の仕組みと重複している**か、**確定済みの設計と衝突する**ことが判明した。指示を出した側が両文書を部分的にしか読んでいなかったことが原因である。

### 検査1（セクション構成の一致）— 設計と衝突する

- `steering.md` Rules L42「各ページのセクション・小見出しの並び順は…そのページに来た読者が最初に欲しい答えは何かを起点に組み立て直す」— 構成はページごとに組み直す前提であり、固定的な一致検査は設計と逆行する
- `design.md` L94 — `対象範囲` は意図的に独立見出しを持たない
- `design.md` L191 — 第2部の `機能概要`・`拡張例` は任意で、0件は既に `verify_mapping.py` の advisory として監視されている
- `design.md` L450 — 「ページ作成時点」の網羅性担保は**観点A（網羅性）のサブエージェントレビュー**が担うと既に定義済み
- `steering.md` L257 — 前方参照によるスタブページ運用があるため、見出しのみのページが常に存在する。検査1はスタブページ全件を ERROR にする

### 検査3（外部被参照ラベルの保全）— `#last` で捕捉される

ラベルが定義されなければ `db_double_submit.rst:106` の `:ref:` が `undefined label` 警告になる。`steering.md` `#last` Steps（`undefined label` 0件の確認）で確実に検出される。専用検査は不要。

### 検査2（孤立ラベル）— `#last` の grep で足りる

`#last` の「リンク切れになる参照3件の解消確認」で棚卸しする際、`grep` で確認できる。恒久ツールを持つ必要がない。

---

## 実施手順

### 未着手の場合

破棄するだけでよい。`ntf-doc-09-pre.md` / `ntf-doc-09-pre-rev1.md` を `.rn/20260724-ntf-yaml-support/` から削除し、本書に撤回の記録を残す。そのまま `#9` に進む。

### 着手済み・未コミットの場合

作業ツリーの変更を破棄する。`git status` がクリーンであることを確認する。

### 着手済み・コミット済みの場合

次をすべて元に戻す。**`git revert` でも手動の打ち消しでもよいが、履歴に撤回の記録が残る形にすること。**

- `mapping/tools/verify_pages.py` の削除
- `steering.md` の `#9〜` Steps に追加した `verify_pages.py` 実行の行を削除
- `steering.md` の `#last` Completion criteria に追加した `verify_pages.py` の行を削除
- `design.md` §11 観点A に追加した「ページのセクション構成が `mapping.csv` の `dest_section` と一致しているか」の行を削除
- `checks/task-09-pre.md` は削除する（作成済みの場合）

### 元に戻さないもの

`about/index.rst` / `mapping.csv` / `_batch/*.csv` / `vocabulary.md` / `glossary.md` は、両指示書とも変更を禁止していたため差分が無いはずである。**差分がある場合は元に戻す前に報告すること。**

---

## ゲート

- `mapping/tools/verify_pages.py` が存在しない
- `steering.md` / `design.md` が `ntf-doc-09-pre.md` 適用前の状態に戻っている（`git diff` で確認）
- `about/index.rst` / `mapping.csv` / `_batch/` / `vocabulary.md` / `glossary.md` に差分がない
- `python3 mapping/tools/verify_mapping.py` が `exit 0`、594行 / 12,986 / 11,983 が不変
- 撤回の経緯が `checks/task-09-pre-withdrawn.md`（またはそれに代わる記録）に1〜2行で残っている。詳細は本書を参照する形でよい

## 次のアクション

撤回が済んだら、**追加の指示なしで `#9`（テストデータの書き方、`implementation/testdata_notation.rst`、対象140行）に着手する。** `steering.md` `#9〜` の共通 Steps に従う。撤回作業の user review は不要とし、`#9` の user review にまとめる。

## 禁止事項

- `verify_pages.py` を「せっかく作ったから」という理由で残さない
- 撤回の範囲を独自に狭めない。3つの検査すべてを撤回する
- 差分が本書の想定と食い違う場合、元に戻す前に報告する
