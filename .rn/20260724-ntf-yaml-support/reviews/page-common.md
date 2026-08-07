# レビュー記録: `setup/common.rst`（第2部「共通設定」）

対象タスク: `#11`（作業指示 `ntf-doc-11-common.md`）。ベースコミット `f4e4de8`。

対象ページ: `ja/development_tools/testing_framework/setup/common.rst`（新規作成）
出典: 削除済みの `ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.rst`（削除前コミット `2e501ad`）
マッピング行: `dest_page=共通設定` の5行（`current-0225` / `current-0226` / `current-0227` / `current-0228` / `current-0246`）。129 lines、すべて `dest_section=使用方法`・`disposition=MERGE`・`audience=user`。

## 作成時の判断（レビュー前に確定したもの）

作業指示 `ntf-doc-11-common.md` が「`reviews/page-common.md` に記録すること」と明示している3件を含め、
本ページ作成時に行った判断を記録する。

### D-1 `FixedSystemTimeProvider` の桁数は実装を優先し「14桁 / 17桁」とした（作業指示 STEP 2-1）

| 項目 | 内容 |
|---|---|
| 出典の記述 | `03_Tips.rst:330-331` 「`yyyyMMddHHmmss` (12桁)」「`yyyyMMddHHmmssSSS` (15桁)」 |
| 実装での確認結果 | `yyyyMMddHHmmss` は14桁、`yyyyMMddHHmmssSSS` は17桁 |
| 実装の `file:line` | `nablarch-testing` の `src/main/java/nablarch/test/FixedSystemTimeProvider.java:23,26`（フォーマット文字列の定義）、`:46,48`（`len == LONGEST_FORMAT.length()` / `len == SHORTEST_FORMAT.length()` による桁数判定）、`:51`（形式外は `IllegalArgumentException`） |
| 参照コミット | `nablarch/nablarch-testing` の `main`、`e21bf67` |
| 判断 | `design.md` §8「出典と実装が食い違う場合は実装を優先する」に従い、**14桁 / 17桁**と記載した。出典の「12桁 / 15桁」は本ページに写していない（ゲート6で0件を確認） |
| 補足 | 実装側の Javadoc（`FixedSystemTimeProvider.java:35-36`）にも同じ「12桁 / 15桁」という誤りがある。判定の根拠は Javadoc ではなくコード（`:46,48`）である。出典自身が挙げる設定例 `20100914123456`（`03_Tips.rst:321`）も14桁であり、出典内部でも整合していない |
| 実装確認の実施者 | `#11` 作業指示 STEP 2 のとおり、レビュー役が `e21bf67` を clone して実コードで確認した結果を根拠として採用した。本タスクでは `nablarch-testing` を再取得していない（起動ディレクトリ外のため） |

### D-2 `current-0226` の Java コード例はコードブロックとして載せない（作業指示 STEP 3-1）

| 項目 | 内容 |
|---|---|
| 対象 | `03_Tips.rst:334-338` の `code-block:: java`（`SystemRepository.getObject("systemTimeProvider")` で `SystemTimeProvider` を取得し `getDate()` を呼ぶ2行） |
| 判断 | コードブロックを置かない |
| 理由 | `design.md` §3「記載範囲」は、第2部に置くものをコンポーネント設定ファイルの設定項目・記述例・拡張方法に限り、**テストソースコードの実装例は置かない**と定めている。当該コード例は設定ではなく API の使用例であり、第2部の記載範囲外である |
| 内容の引き継ぎ | 内容は落とさず、地の文として残した（`setup/common.rst:45` 「この設定を行うと、テスト対象のアプリケーションが ``SystemTimeProvider`` を通じて取得するシステム日時は、指定した日時に固定される。」）。「固定した日時は `SystemTimeProvider` を通じて取得される」という事実が保持されている |

### D-3 採番の記述例は `testdata_examples-table_data` へ `:ref:` で導線を張った（作業指示 STEP 3-2）

| 項目 | 内容 |
|---|---|
| 参照元 | `setup/common.rst:83`（`シーケンス採番をテーブル採番に置き換える` の末尾） |
| 参照先 | `` :ref:`テーブルのデータを記述する <testdata_examples-table_data>` `` |
| 理由 | 出典の「Excelファイル記述例」（`03_Tips.rst:389` 以降）は `current-0229` として `dest_page=テストデータの記載例` に割当済みであり、本ページには割り当てられていない。`design.md` §3「『使い方』に該当するものは第3部に置き、第2部からは `:ref:` で参照する」に従い、第2部から第3部へ導線だけを張った |
| ラベル選定の理由 | 採番の記述例そのもの（`testdata_examples.rst:951` の L3 `採番処理のテストデータを記述する`）にはラベルが無い。承認済みの `#10` の成果物である `testdata_examples.rst` にラベルを足さない（作業指示 禁止事項）ため、その親にあたる L2 セクションの既存ラベル `testdata_examples-table_data`（`testdata_examples.rst:776`）を指した |
| 表示テキストの扱い | 作業指示は表示テキストを「テーブルデータを記述する」と記していたが、参照先の実際の見出しは `testdata_examples.rst:778` 「**テーブルのデータを記述する**」である。参照先の見出し文言と表示テキストを一致させる（`testdata_examples.rst:780` 自身が `` :ref:`テーブルのデータを記述する <testdata_notation-table_data>` `` と実見出しに揃えている前例に合わせる）ため、実見出しの表記を採用した |
| **申し送り** | 本参照は L2 セクションを指しており、読者は着地後にページ内で L3 `採番処理のテストデータを記述する` を探す必要がある。**採番の記述例をピンポイントで参照する必要が生じた場合は、`testdata_examples.rst` の当該 L3 に `testdata_examples-id_generation` 相当のセクションラベルを追加し、本ページの `:ref:` をそちらに差し替える。** `#10` 成果物への追記になるため、実施は `#10` の凍結解除またはユーザー判断を伴うタスクで行うこと |

### D-4 出典の2つの単一行の表を、表にせず地の文にした

| 項目 | 内容 |
|---|---|
| 対象 | `03_Tips.rst:326-332`（`fixedDate` の property名／設定内容、grid table・データ行1件）、`03_Tips.rst:740-745`（`nablarch.test.resource-root` のキー／値、simple table・データ行1件） |
| 判断 | いずれも表を作らず、地の文と `code-block` で記述した |
| 理由 | 両表ともデータ行が1件しかなく、表にしても列見出し（`property名`／`設定内容`、`キー`／`値`）が情報を増やさない。`style.md` S-07 は「表を作る場合にどの記法を使うか」を定める規約であり、表を作ること自体を要求していない。内容（キー名・プロパティ名・値の意味・受け付ける形式）はすべて地の文に保持している（本ファイル「出典と本文の対応」参照）。なお本ページは表を1件も持たないため、S-07 の例外（表が多いページは `list-table` に揃える）の適用対象にもならない |
| 落とした情報 | なし。出典の grid table（`+---+` 形式）は `style.md` S-07 が使用を禁じているため、いずれにせよそのままの形では持ち込めない |

### D-5 コードブロックの言語指定を出典から変更した

出典は `nablarch.test.resource-root` の設定例に `bash`（`03_Tips.rst:753`）と `text`（`:763`）を使い分けているが、内容は同一形式の `キー=値` である。`style.md` S-05「言語指定は実際の内容に応じて個別に付ける」に従い、両方とも `properties` に統一した（FW解説書のライブラリでも `properties` は24件使われている）。

### D-6 「機能概要」「拡張例」の見出しとトランザクションの節を置かなかった

`design.md` §3 は第2部のページを「機能概要（任意）→ 使用方法（必須）→ 拡張例（任意）」とし、「出典が無い場合は見出し自体を置かない」と定めている。`verify_mapping.py` の出力でも `[第2部 導入と設定 > 共通設定 > 機能概要]` と `[同 > 拡張例]` はいずれも 0 row である。トランザクションについては、`design.md` §3 の記載内容欄に語としては挙がっているが、本ページに割り当てられたマッピング行が無く（トランザクション関連の `current-0237`・`current-0195` はいずれも `dest_page=コンポーネント単体テスト`）、節を作らなかった。

## レビュー記録

`#11` のレビュー（`design.md` §11.6 の4観点 A:網羅性 / B:トンマナ / C:用語 / D:整合性）は、
コーディネーターが別のサブエージェントで実施する（作業指示 STEP 5）。本節はその結果を記録する欄である。

### ラウンド1

| 指摘ID | ラウンド | 観点 | 区分 | 指摘内容 | 対応要否 | 不要の理由 | 対応内容 |
|---|---|---|---|---|---|---|---|
| （未実施） | | | | | | | |

## 出典と本文の対応

`dest_page=共通設定` の5行の全件対応は `checks/task-11.md` のゲート1に記載する。
