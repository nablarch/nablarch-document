# `#22` 作業指示 — 取引単体テストの設定（RESTfulウェブサービス）

宛先: CC（`nablarch/nablarch-document` の `ntf-yaml-support`）
発行: レビュー役、2026-08-13

参照点

- `nablarch-document` = `41909d4`（本書の `file:line` はこのコミットで開いて確かめたもの）
- 出典の基準コミット = `c241906`。レビュー役の手元 `2e501ad` と、参照する出典ファイルの blob が一致することを実測済み
- `nablarch-testing` = `e21bf67`

---

## 1. `#21` 承認反映の検証結果 — 受理

ゲート1〜10 をレビュー役が独立に実行し、**全件 PASS を確認した。** 追加の是正は求めない。確認した内容は次のとおり。

| ゲート | 実測結果 |
|---|---|
| `ja/` の差分 | 4ファイルのみ（`testdata_notation.rst`・`batch.rst`・`http_messaging.rst`・`mom.rst`）。他ファイルへの波及なし |
| `既定` 残存 | `about`／`setup`／`implementation`／`tools` 配下で**0件**（`grep -o`） |
| `デフォルト設定` の新規発生 | 反映前16件・反映後16件で**増減なし** |
| `glossary.md` の差分 | §5.12 に1行・§5.14 に1行・§8 に3行の追加のみ |
| 証拠一覧（§5.15） | **反映前後で1バイトも変わっていない**（節全体126行を内容比較。行番号は後述） |
| `design.md` の差分 | 類型1件の追加のみ（26行・1ハンク） |
| `mapping.csv`／`mapping/_batch`／`volume.md` | **差分なし** |
| `verify_mapping.py` | 595行 / 12,986 / 11,983、exit 0 |
| 見出し下線 | 4ファイルの全見出しを再走査し、規則（L1 `max(50,表示幅)`／L2 50固定／L3 `max(49,表示幅)`）からの逸脱**0件** |
| `design.md` §8 の新類型が引く `file:line` | `GroupMessageParser.java:58`・`SendSyncMessageParser.java:42-43`・`MessagePool.java:54`・`:155-163`・`NablarchTestUtils.java:36`・`:45-49`・`MessageParser.java:102-103`・`batch.rst:78` を実物で確認、全件一致 |

Docker フルビルドの `build succeeded, 1 warning.` は再実行していない。**CC の報告として受け取る。**

### 1.1 指示と実測が食い違った3件 — すべて CC が正しい

3件とも**レビュー役の指示の側が誤っていた。** 実測を採った CC の判断は正しい。

1. **`既定` の内訳** — 再実測すると `testdata_notation.rst` 6・`batch.rst` 13・`http_messaging.rst` 2・`mom.rst` 5 で、CC の報告と一致する。指示の「batch 12・testdata_notation 7」は誤り。なお `grep -c`（該当行数）で数えると 6/10/2/3 = 21件になる。**指示の 12/7 はどちらの数え方でも再現しない、単純な誤記である。**
2. **`batch.rst:39` の表示幅** — `ディレクティブのデフォルト値を設定する` の表示幅は38で、是正前の32から+6。指示の「+2」は誤り。`max(49, 38) = 49` で下線の変更が不要という結論は変わらない。
3. **`S:design.md:443`** — 正しい。`verify_glossary.py` の `[ref]` 検証を通っている。

### 1.2 CC 側の作業が不要な訂正1件

`02-進め方.md` とレビュー役の前指示は、証拠一覧の位置を「`glossary.md:403`〜`:449`」と書いていた。実測すると、反映前は `:401`〜`:449`、反映後は `:403`〜`:451` である。**指示に書いた行番号が最初から実物と2行ずれていた。** 内容は §5.15 全体が反映前後で完全一致しており、CC は禁止領域に一切触れていない。レビュー役が自分の記録を直す。**CC 側の作業は無い。**

---

## 2. `#22` の対象ページ

**`ja/development_tools/testing_framework/setup/deal_unit_test/rest.rst`（新規）**

`setup/deal_unit_test/` ディレクトリは存在しない。**このタスクで新設する。**

### 2.1 3条件の判定 — 個別の作業指示は不要

レビュー役が実測した。**3条件のいずれにも当たらない。** 共通 Steps で進めてよい。本書は禁止事項ではなく、着手前に知っておくと手戻りが減る事実を渡すものである。

| 条件 | 判定 |
|---|---|
| 出典が500行超 | 非該当。`DROP` を除いて52行（3行、すべて `MERGE`・`audience=user`） |
| 出典0行 | 非該当 |
| `design.md` と `mapping.csv` の食い違い | 非該当。`機能概要` が0行だが、`verify_mapping.py` が `optional since #6, not an error` と宣言済みであり、食い違いではない |

### 2.2 マッピング行（全3行）

| `mapping_id` | disposition | lines | 出典 | `dest_section` |
|---|---|---:|---|---|
| `current-0150` | MERGE | 4 | `05_UnitTestGuide/03_DealUnitTest/rest.rst:40-43` | 使用方法 |
| `current-0151` | MERGE | 20 | 同 `:46-65` | 拡張例 |
| `current-0152` | MERGE | 28 | 同 `:68-95` | 使用方法 |

出典ファイル `03_DealUnitTest/rest.rst` は全95行である。`:1-37`（表題・リード文・「取引単体テストのテストクラス例」）は本ページの範囲外で、別のマッピング行が持つ。**`:68-95` は出典の末尾まで**である。

---

## 3. 着手前に渡しておく事実

### 3.1 セクション構成 — `機能概要` は置かない

作成済みの第2部7ページはいずれも `機能概要` の見出しを持たず、リード文＋`使用方法`（L2、12行目）＋必要に応じて `拡張例` の形である（`setup/common.rst:12`・`class_unit_test.rst:12`・`request_unit_test/web.rst:12`・`:222`・`rest.rst:12`・`http_messaging.rst:12`・`batch.rst:12`・`mom.rst:12`・`:28`）。**本ページも同じ形にする。** `使用方法` と `拡張例` の両方を持つ。

ページ先頭ラベルは `style.md` S-08 の一覧から引く。**`deal_unit_test_setting_rest`。** 現ツリーに同名ラベルは無い（実測）。

### 3.2 `使用方法` と `拡張例` が出典の中で入れ子になっている

`dest_section` の割り当てが出典の行順と一致しない。**使用方法 = `:40-43` + `:68-95`、拡張例 = その間の `:46-65`** である。出典を上から順に写すと `拡張例` の内容が `使用方法` に混ざる。

そのうえで、`:46-65` の中身は一様ではない。

- `:46-49`・`:58-64` — `RequestResponseProcessor` を自分で実装する話。`拡張例` に当たる
- `:51-56` — フレームワークが提供する `RequestResponseCookieManager`・`NablarchSIDManager` の説明。**自分で実装せずに使える話であり、`使用方法` の側の内容である**

**どちらに置くかは CC が判断し、根拠を `reviews/page-*.md` に記録すること。** レビュー役はどちらでもよいとは考えていないが、出典の切れ目とセクションの切れ目が一致しないこと自体は `MERGE` 行が想定している事象であり、`mapping.csv` を変える必要はない。**`mapping.csv` は変更しない。**

### 3.3 出典のXMLが構文として壊れている（2箇所）

出典 `:70-72` と `:83-85` は、開始タグを `/>` で自己閉じしたうえで子要素と閉じタグを書いている。XMLとして不正であり、そのまま貼るとコピーした読者の設定ファイルが読み込めない。

```
（出典 :70-72、そのままでは不正）
<component name="defaultProcessor" class="nablarch.test.core.http.RequestResponseCookieManager"/>
  <property name="cookieName" value="JSESSIONID"/>
</component>
```

**開始タグの `/` を落として是正する。** `:83-85` の `RequestResponseCookieManager` も同型で、同じ是正が要る。`:86` の `NablarchSIDManager`・`:87` の `CSRFTokenManager` は子要素を持たない自己閉じタグであり、正しい。

`design.md` §8「出典と実装が食い違う場合は実装を優先する」の適用として扱い、`reviews/page-*.md` の「出典と実装が食い違った点」に記録すること。

### 3.4 用語

- **`インターフェース`（出典 `:47`）は `インタフェース` に直す**（`glossary.md` §8 の置換規則）。同じ出典の `:49` は `インタフェース` と書いており、出典の中で割れている
- **`デフォルト`**（出典 `:55`・`:56`）はそのままでよい。`#21` で正表記に確定した。**`既定` を新たに書かないこと**
- **`デフォルト設定`** の語は `nablarch-testing-default-configuration` が提供する設定を指す固有の語である（`design.md:443`）。一般語として使わないこと

### 3.5 `:ref:` の扱い

出典が持つ `:ref:session_store`・`:ref:session_store_handler` は、**そのまま持ってくる。** 参照先はFW解説書側にあり削除の対象外である。解決できているかは Sphinx ビルドの警告で確認する（既知の1件以外が増えないこと）。

`:java:extdoc:` の記述もそのまま持ってくる。

### 3.6 `setup/index.rst` の `toctree`

現在の `toctree` は `request_unit_test/mom` の次が `junit5_extension`・`master_data_restore` である。`design.md:153-162` の構成は **リクエスト単体6ページ → 取引単体3ページ → JUnit 5用拡張機能 → マスタデータ復旧機能** の順であり、`deal_unit_test/*` は `junit5_extension` より前に入る。

本タスクでは `deal_unit_test/rest` の1行を `request_unit_test/mom` と `junit5_extension` の間に追加する。**`request_unit_test/db_queue` の行はまだ入れない**（ページが無い）。

---

## 4. ゲート

**実行順は上から。** `git status --porcelain` の全件確認を `commit & push` の直前に必ず通す。

1. `git status --porcelain` の**全件**を目視し、意図した差分だけであることを確認する。`git diff` は未追跡ファイルを出さないため母集合に使わない
2. `ja/` の差分は `setup/deal_unit_test/rest.rst`（新規）と `setup/index.rst`（1行追加）の2ファイルに限る
3. `mapping.csv`・`mapping/_batch`・`volume.md`・`glossary.md`・`design.md` に差分が無いこと
4. `verify_mapping.py` が 595行 / 12,986 / 11,983 で exit 0
5. `既定` が `about`／`setup`／`implementation`／`tools` 配下に0件のままであること（`grep -o`）
6. 新ページが `デフォルト設定` の語を作っていないこと
7. 見出し下線を実測則で再計算する（L1 `max(50,表示幅)`／L2 50固定／L3 `max(49,表示幅)`）
8. Docker フルビルド（`-a`）で新規警告0件。**直後に `git checkout -- ja/locales/ja/LC_MESSAGES/sphinx.mo` で再生成物を戻す**（通算8回目になる）
9. 貼り付けたXMLが構文として妥当であること（3.3）

---

## 5. `verify_glossary.py` の申し送りへの回答 — **今回は触らない。`#last` の直前に1タスクでまとめる**

CC が挙げた障壁「登録すれば解消するが、既存の全件数主張を再計算する作業になる」は、**実測すると成立しない。** レビュー役が `term_candidates.tsv` に5表記（`環境設定ファイル`／`propertiesファイル`／`プロパティファイル`／`デフォルト`／`既定`）を追加して `detect_term_variants.py scan` を再実行し、追加前の再生成結果と突き合わせた。

**既存の表記で出現数が変わったものは0件である。** 増えたのは追加した5表記×4コーパスの20行だけだった。追加した5表記は既存の登録表記と部分文字列の関係を持たないため、最長一致・非重複の影響を受けない。

それでも今回触らない理由は別にある。**`scan-terms.tsv` は `#10a`（`6ce81b5`、`テストケース`→`テストショット` の正表記変更）以降ずっと再生成されておらず、既に実物とずれている。** 同じ `term_candidates.tsv` で作業ツリーを再走査すると、コミット済み `scan-terms.tsv` と比べて**55件の出現数が食い違い、12表記×4コーパスの行が増減する。** 食い違う55件は**すべて `design` コーパス**である。`design.md` は毎タスク書き換わるため、いま緑にしても次のタスクで再び赤くなる。

`[ref]` 13件も同じ根であり、いずれも `glossary.md` が `S:design.md:27`〜`:151` を行番号で指しているものである。`#21` の追記は `design.md:476` 以降なのでこの13件を増やしていない。

したがって、次のようにする。

- **`#22`〜 では `verify_glossary.py` をゲートに入れない。** 現在の25件は既知として扱う
- **`#last` の直前に1タスクを置き、そこで一括是正する。** 内容は (a) 未登録9表記の `term_candidates.tsv` への登録、(b) `scan-terms.tsv` の再生成、(c) `[section]` 1件（§5.7 の揺れ表記 `テストソースコード` が §8 対応表に無い）の是正、(d) `[ref]` 13件の行番号是正
- そのタスクで、**`design.md` を `scan` のコーパスから外すか、`glossary.md` から `S:design.md:NN` の行番号指定を無くすかを決める。** `design.md` は生きている文書であり、行番号で指す限り再発する

**用語の実効性は保たれている。** 揺れ表記→正表記の対応そのものは `[applies] 94件 / 不一致0件` で今も検証できており、残り24ページの品質に効くのはこちらである。25件が赤いことで失われているのは、9表記の出現数の裏取りと `design.md` への13件の行番号だけである。

---

## 6. その次

`#23` 以降の順序は `design.md:153-162` に従う。第2部の残りは**6ページ**である（`style.md` S-08 の第2部14行から、表題ページ1件と作成済み7件を引いた数。CC の報告にある「残り9ページ」は実測と合わない）。

| 順 | ページ | 出典 lines | 個別指示 |
|---|---|---:|---|
| — | `setup/request_unit_test/db_queue.rst` | 0 | **要。レビュー役が作成中。指示が届くまで着手しない** |
| 1 | `setup/deal_unit_test/rest.rst` | 52 | 不要（本タスク） |
| 2 | `setup/deal_unit_test/http_messaging.rst` | 20 | 不要 |
| 3 | `setup/deal_unit_test/mom.rst` | 104 | 不要 |
| 4 | `setup/junit5_extension.rst` | 475 | 不要。ただし4行のスタブが既にあり、**新規作成ではなく追記**として扱う |
| 5 | `setup/master_data_restore.rst` | 193 | 同上（スタブへの追記） |

`db_queue.rst` は `mapping.csv` に該当行が0件である（`dest_page = リクエスト単体テストの設定（テーブルをキューとして使ったメッセージング）` の行が存在しないことを実測）。**出典が無いページを推測で書かせない。** レビュー役が指示を出すまで着手しないこと。

`junit5_extension.rst` は出典475行で、17行のマッピングのうち3行（`current-0178`〜`0180`）が第1部の出典ファイル `06_TestFWGuide/01_Abstract.rst` から来ている。**これは食い違いではなく、意図された割当である。** `design.md:118-136` が `#6` の「依存関係を第1部に集約する」方針を取り消し、`current-0180`（JUnit Vintage有効化の依存関係）と `current-0267`（JUnit 5用拡張機能の依存関係）を第2部「JUnit 5用拡張機能」の使用方法へ差し戻したと明記している。第1部 `about/index.rst:117` の「稼動環境」も1文＋`:ref:` だけで、依存関係を持っていない（実測）。**3条件の3つめには当たらない。**
