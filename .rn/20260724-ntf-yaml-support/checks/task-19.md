# `#19` self-check — リクエスト単体テストの設定（HTTPメッセージング）

対象ページ: `ja/development_tools/testing_framework/setup/request_unit_test/http_messaging.rst`（新規作成）

## ゲート0 — 個別の作業指示を出す条件の判定

`steering.md`「#9〜」の「個別の作業指示を出す条件」3件について、いずれにも当たらないことを確認した。

| 条件 | 判定 | 根拠 |
|---|---|---|
| (1) 出典が500 lines を超える | 該当なし | `mapping.csv` の当該3行の `lines` 合計は **30**（10 + 4 + 16） |
| (2) `design.md` の確定事項どうし、または `design.md` と `mapping.csv` が食い違う | 該当なし | `design.md:862`（`setup/request_unit_test/http_messaging.rst`）・`style.md:351`（S-08。同パスと `request_unit_test_setting_http_messaging`）・`mapping.csv` の `dest_page` の3者が一致する |
| (3) 出典が0行 | 該当なし | 3行・30 lines |

したがって共通 Steps のみで進めた。

## ゲート1 — マッピング全件（母集合を先に固定）

`csv.DictReader` で `dest_page=リクエスト単体テストの設定（HTTPメッセージング）` を抽出。**3行**。

| `mapping_id` | 出典 | 範囲 | `lines` | `disposition` | 反映先 |
|---|---|---|---|---|---|
| `current-0066-b` | `.../02_RequestUnitTest/http_real.rst` | `120`〜`129` | 10 | SPLIT | 「フレームワーク制御ヘッダの項目名を指定する」 |
| `current-0074` | `.../02_RequestUnitTest/http_send_sync.rst` | `143`〜`146` | 4 | MOVE | 「モックアップクラスを登録する」の `tip` |
| `current-0075` | `.../02_RequestUnitTest/http_send_sync.rst` | `149`〜`164` | 16 | MOVE | 「モックアップクラスを登録する」の本文・XML例・`charset` の説明 |

反映漏れ0件。

## ゲート2 — ページ先頭ラベル

`style.md` S-08 の表から引用した。新規考案なし。

- ページ: `リクエスト単体テストの設定（HTTPメッセージング）`
- ファイル: `setup/request_unit_test/http_messaging.rst`（S-08 の表と一致）
- ラベル: `request_unit_test_setting_http_messaging`（S-08 の表と一致）

## ゲート3 — Docker フルビルド

```
docker run --rm -v /home/tie303177/work/nablarch/nablarch-document:/root/document \
  nablarch-document-build /bin/bash -c \
  "cd /root/document; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"
```

結果: `build succeeded, 1 warning.`（是正後の最終ビルドも同じ。計3回実行し、いずれも同じ結果）

警告の全件は次の1件のみ。既知の `#7` 検出分（`#last` で解消予定）であり、**新規0件**。

```
/root/document/ja/application_framework/application_framework/libraries/db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test
```

（`:108` は Sphinx 警告が出力した行番号であり、実ファイルで `:ref:` が書かれているのは `:106` である。）

ビルド直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行して副産物を戻すこと
（`steering.md` の Rules に追記済み）。

## ゲート4 — 4観点レビュー

ラウンド1は4観点（A:網羅性 / B:トンマナ / C:用語 / D:整合性）を**それぞれ別のサブエージェント**で実施した。
プロンプトには Rules の3点（実測で裏付ける／付属の検証スクリプトを正解にしない／敵対的にレビューする）を
必ず入れた。

| ラウンド | 観点 | 判定 | `must` | `should` | `note` |
|---|---|---|---|---|---|
| 1 | A 網羅性 | FAIL | 3 | 1 | 3 |
| 1 | B トンマナ | FAIL | 1 | 4 | 3 |
| 1 | C 用語 | FAIL | 1 | 2 | 2 |
| 1 | D 整合性 | FAIL | 3 | 2 | 5 |
| 2 | 是正差分限定の検証 | **PASS** | 0 | 3 | 3 |

ラウンド1の `must` は8件（重複除去後7件）で、すべて対応した。ラウンド2は `must` 0で pass。
指摘と対応の対応表、採らなかった指摘とその理由、ユーザー判断を仰ぐ `decide` 3件は
`reviews/page-request_unit_test_setting_http_messaging.md` に記載した。

ラウンド2の `note` 1（記録の理由づけが逆である、という指摘）は**採らなかった。** 実物を確認した結果、
指摘のほうが誤りであることを確認している（`SendSyncMessageParser.java:109-141` が
`createFixedLengthFileParser` を override し、`MessageParser` の無名サブクラスではなく
`FixedLengthFileParser` の無名サブクラスを返している。根拠は同レビュー記録）。

## ゲート5 — 差分の範囲（`#19` からの新ゲート）

### 着手時の HEAD

**`85b64e2`**。当初は `71334aa` を基準にしていたが、2026-08-13 の作業指示により、ビルド副産物の混入を
止めるゲート是正（`steering.md`）と到達不能なハッシュの訂正（`checks/task-18.md`）を `#19` とは別の
単独コミットに切り出したため、その `85b64e2` を `#19` の着手時の HEAD として置き直した。
`#19` の差分範囲は以降このハッシュを基準に判定する。

### 母集合

`git status --porcelain` の全件とする。`git diff` は**未追跡ファイルを出さない**ため、新規に置かれた
予定外のファイルを取りこぼす（2026-08-13 の作業指示による是正。`steering.md` の共通 Steps も同時に改めた）。

### 全件（`git status --porcelain`）

| 状態 | ファイル | 予定していた変更か |
|---|---|---|
| `M` | `ja/development_tools/testing_framework/setup/index.rst` | 予定どおり（`toctree` 追記1行） |
| `??` | `ja/development_tools/testing_framework/setup/request_unit_test/http_messaging.rst` | 予定どおり（本ページ） |
| `??` | `.rn/20260724-ntf-yaml-support/checks/task-19.md` | 予定どおり（self-check） |
| `??` | `.rn/20260724-ntf-yaml-support/reviews/page-request_unit_test_setting_http_messaging.md` | 予定どおり（レビュー記録） |

予定外0件。

### このゲートが検出した1件

初回の全件確認で `locales/ja/LC_MESSAGES/sphinx.mo`（`Bin 23235 -> 23237 bytes`）が現れた。
Docker フルビルドが再生成した副産物で、`#18` の `/rn:gm` で差し戻された1件と同一である（混入は通算4回目）。
`git checkout 2993496 -- locales/ja/LC_MESSAGES/sphinx.mo` で戻し、上表のとおり0件にした。
`ja/` に絞っていたら検出できなかった。

**ゲートの位置も是正した。** `#18` で追加した時点では `commit & push` の**後ろ**にあり、
`git diff --stat <着手時の HEAD> HEAD` はコミット済みの差分しか見ないため、混入を検出できるのは
コミットしてしまった後だった。`commit & push` の直前へ移し、母集合を `git status --porcelain` に変えた。
あわせて共通 Steps の Docker ビルドの Rule に、**ビルド直後に
`git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行する**ことを書き足した。

### `checks/task-18.md` の到達不能なハッシュの訂正

`checks/task-18.md:377` が記録していたハッシュは `ntf-yaml-support` の祖先ではなく、どのブランチにも
含まれていなかった（`git merge-base --is-ancestor` が偽、`git branch -a --contains` が0件）。
ブランチ上の実物は `c0381ed`（親 `ae56ff2`）である。`c0381ed` に訂正し、訂正後に
`grep -rn "<旧ハッシュ>" .rn/` が**0件**であることを確認した。

## ゲート6 — user review（`/rn:ty`、2026-08-13）

**承認された。** レビュー役が独立検証を行い、`must` の残存は0件、本文に事実誤りは無いことを確認した。
あわせて `decide` 3件の回答と `should` 1件の訂正指示を受けた。**回答の全文と根拠は
`reviews/page-request_unit_test_setting_http_messaging.md` §4・§5 に記載した。** 本節には是正の実行結果のみ記す。

| 事項 | 回答 | 本文（`http_messaging.rst`）への影響 |
|---|---|---|
| `decide` 1（`glossary.md:160` の意味列） | **是正する** | 無し（正表記が変わらないため波及しない） |
| `decide` 2（出典外の追記） | **残す。ただし追記は2件ではなく3件** | 無し |
| `decide` 3（FW解説書 `http_system_messaging.rst:85`） | **対象外として記録に留める。別タスク化もしない** | 無し |
| `should` 1（追記の件数を3件に訂正） | 記録のみ訂正 | 無し |

### `decide` 1 の是正で通したゲート（4件ともパス）

是正内容は `mapping/glossary.md:160` の意味列のセル1つの書き換え。

| # | ゲート | 実行 | 結果 |
|---|---|---|---|
| 1 | 差分が `:160` の意味列のセル1つに収まる（正表記・揺れ・採用根拠が不変） | `git diff --stat -- mapping/glossary.md` ＋ 是正前後の全行突き合わせ | **パス**。`1 file changed, 1 insertion(+), 1 deletion(-)`。差分行は `:160` のみ。同行を `|` で5列に分割して突き合わせ、変更は列2（意味）のみ。列1（正表記）・列3（揺れ）・列4・列5（採用根拠）は同一 |
| 2 | `mapping/mapping.csv`・`mapping/_batch/` の差分が空 | `git status --porcelain -- mapping/mapping.csv mapping/_batch/` | **パス**。0行 |
| 3 | `verify_mapping.py` が `exit 0`、594行 / 12,986 / 11,983 が不変 | `python3 mapping/tools/verify_mapping.py` を是正の前後で実行し出力を `diff` | **パス**。`exit=0`。`Loaded 594 rows from mapping.csv` / `lines total (all rows): 12986` / `lines total (excluding DROP): 11983`。前後の出力の `diff` は差分0 |
| 4 | `ja/` 配下に差分が出ない | `git status --porcelain -- ja/` | **パス**。0行 |

### 書き換えを禁じている対象に触れていないことの確認

`glossary.md` で書き換えを禁じているのは、削除前の現行解説書に実在した見出し文字列の一覧
（`:403`〜`:449` 相当の候補表）である。是正した `:160` はこの範囲外であり、採用根拠の列（実測値の記録）も
不変である（ゲート1）。

### `#20` 以降への申し送り（1件追加）

`reviews/page-request_unit_test_setting_http_messaging.md` §5 に申し送り7（`YAML` 形式だけを使う読者が
`fw_header:` のキー名を何に合わせればよいか、どちらのページからも読み取れない件）を追記した。
**`#19` では是正しない。**
