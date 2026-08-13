# `#11` 作業指示 — 共通設定（`setup/common.rst`）

対象ブランチ: `lovaizu/nablarch-document` の `work`（`f4e4de8` の続き）

`#10b` は user review 承認済みで完全に閉じている。本書から第2部に入る。

本ページは**第2部の1ページ目**である。`steering.md` の作成順「第3部のテストデータ2ページ → 第2部 → 第3部の残り → 第4部」に従う。第2部の他ページが本ページを前提に「共通設定を参照」と書けるようにするため、第2部の中でも先頭に置く。

## 対象

| 項目 | 値 |
|---|---|
| `dest_page` | `共通設定` |
| ファイル | `ja/development_tools/testing_framework/setup/common.rst`（新規作成。スタブは存在しない） |
| `dest_part` | 第2部 導入と設定 |
| マッピング行 | 5行 / 129 lines（すべて `dest_section=使用方法`・`disposition=MERGE`・`audience=user`） |

### マッピング5行（全件）

出典はすべて削除済みの `ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.rst` である。削除前コミット `2e501ad` から読むこと（`git show 2e501ad:<path>`）。

| `mapping_id` | 行範囲 | lines | `heading_path` 末尾 | 主題 |
|---|---|---|---|---|
| `current-0225` | 304-309 | 6 | システム日時を任意の値に固定したい > (L2直下) | 日時固定の課題と機能 |
| `current-0226` | 312-342 | 31 | 同 > 設定ファイル例 | `FixedSystemTimeProvider` の設定 |
| `current-0227` | 346-356 | 11 | シーケンスオブジェクトを使った採番のテストをしたい > (L2直下) | 採番の課題と機能・手順 |
| `current-0228` | 359-388 | 30 | 同 > 設定ファイルの例 | 本番設定をテーブル採番設定で上書き |
| `current-0246` | 734-784 | 51 | テストデータ読み込みディレクトリを変更したい | `nablarch.test.resource-root` |

`design.md` §3 は「共通設定」の記載内容に『トランザクション』も挙げているが、**本ページに割り当てられたマッピング行は無い。** トランザクション関連の出典（`current-0237`・`current-0195`）はいずれも `dest_page=コンポーネント単体テスト`（第3部）に割り当て済みである。本ページにトランザクションの節を作らない。

## STEP 1 — ページの構成

### セクション構成

`design.md` §3 の第2部アウトラインに従う。`機能概要` と `拡張例` は出典が0行のため、**見出しごと置かない**（`design.md` §3「使用方法のみ必須」）。

```
共通設定
├── .. contents:: 目次
└── 使用方法（L2）
      ├── テストデータの読み込み先を変更する（L3）
      ├── システム日時を固定する（L3）
      └── シーケンス採番をテーブル採番に置き換える（L3）
```

**L3の並びはこの順とする。** 読み込み先の設定は他の2つを含むすべてのテストの前提であり、`#10a` で確定した「全体から個別へ」に一致する。出典（`03_Tips.rst`）の登場順は日時固定→採番→読み込み先だが、`steering.md` Rules「並び順は元資料の構成ではなく読者の問いを起点に組み立て直す」に従い、出典順を踏襲しない。

**セクションタイトルは `style.md` S-03 の「〜する」形式とする。** ページタイトルが `共通設定` と汎用的であるため、セクションタイトル側で対象を明示すること（`共通設定 > システム日時を固定する` の組で中身が分かる状態にする）。

### ページ先頭のラベル

`.. _testing_framework_common:` とする。`style.md` S-08 は「ページ先頭のラベルはページIDそのもの」と定めているが、ファイル名の語幹 `common` は `ja/` 全体で一意性を保てない汎用語であり、Sphinx のラベルはプロジェクト大域である。同ディレクトリの `setup/index.rst` が `testing_framework_setup` を採っている前例に沿う。

セクションラベルは、他ページから参照する必要が生じた時点で `testing_framework_common-<英語スネークケース>` の形式で足す。本タスクでは先頭ラベルのみとし、セクションラベルは置かない（現時点で本ページを参照する既存ページが無いため）。

### 目次

L2セクションを1つ持つため `.. contents::` を置く（`style.md` S-09 の「適用しないページ」＝`toctree` のみでL2を1つも持たないページ、に該当しない）。ラベル→タイトル→目次の順とする。

## STEP 2 — 実装で確認済みの事実

以下はレビュー役が `nablarch/nablarch-testing` の `main`（コミット `e21bf67`）を clone して実コードで確認した。同じ調査をやり直す必要はないが、CC 側で再確認して構わない。

### 2-1. `FixedSystemTimeProvider`

| 事項 | 実装での確認結果 | `file:line` |
|---|---|---|
| 完全修飾名 | `nablarch.test.FixedSystemTimeProvider` | `src/main/java/nablarch/test/FixedSystemTimeProvider.java:1,20` |
| プロパティ | `fixedDate`（setter は `setFixedDate(String)`） | 同 `:42` |
| 受け付ける形式 | `yyyyMMddHHmmss` または `yyyyMMddHHmmssSSS` | 同 `:23,26` |
| 形式外の値 | `IllegalArgumentException` | 同 `:51` |
| 短い方を指定した場合 | 右0詰めでミリ秒に `000` が入る | 同 `:50` |

**桁数の記載は出典が誤っている。** 出典（`03_Tips.rst:329-330`）は「`yyyyMMddHHmmss` (12桁)」「`yyyyMMddHHmmssSSS` (15桁)」と書いているが、実測すると `yyyyMMddHHmmss` は**14桁**、`yyyyMMddHHmmssSSS` は**17桁**である。出典自身が挙げる例 `20100914123456` も14桁である。実装は `len == SHORTEST_FORMAT.length()`（`:48`）／`LONGEST_FORMAT.length()`（`:46`）で判定しており、14桁・17桁以外は例外になる。

なお、実装側の Javadoc（`:35-36`）にも同じ「12桁 / 15桁」という誤りがある。判定の根拠は Javadoc ではなくコードである。

**実施すること**: `design.md` §8「出典と実装が食い違う場合は実装が優先」に従い、桁数を書くなら **14桁 / 17桁** とする。出典の「12桁 / 15桁」をそのまま写さない。判断の根拠（`file:line` と参照コミット `e21bf67`）を `reviews/page-common.md` に記録すること。

### 2-2. `nablarch.test.resource-root`

| 事項 | 実装での確認結果 | `file:line` |
|---|---|---|
| キー名 | `nablarch.test.resource-root` | `src/main/java/nablarch/test/TestSupport.java:33` |
| 既定値 | `test/java/` | 同 `:30` |
| 未設定時 | 既定値を使う | 同 `:356-361` |
| 区切り文字 | `;`（セミコロン） | 同 `:42,329` |
| 複数指定時の探索 | 最初にリソースが見つかったパスを使う | 同 `:285,291-298` |
| どこにも無い場合 | `IllegalArgumentException`（探索したディレクトリを列挙） | 同 `:294-297` |

出典が述べている「セミコロン区切りで複数指定可」「同名のテストデータが存在した場合、最初に発見されたテストデータが読み込まれる」は、いずれも実装と一致する。そのまま書いてよい。

VM引数による一時的な変更（`-Dnablarch.test.resource-root=...`）は出典の脚注にあり、内容として引き継ぐ。**脚注（`.. [#]`）の形をそのまま持ち込まず、本文または `tip` に組み込むこと**（`design.md` §8「出典の文面をそのまま流用しない」、`style.md` S-06）。

### 2-3. 採番のクラスは未確認である

`nablarch.common.idgenerator.OracleSequenceIdGenerator` と `nablarch.common.idgenerator.FastTableIdGenerator` は `nablarch-testing` に存在しない（grep 0件、`e21bf67`）。Nablarch 本体側のクラスであり、レビュー役は実装を確認していない。

**実施すること**: 出典（`03_Tips.rst:359-388`）に書かれている以上のことを書かない。プロパティの一覧表を新たに作らない。設定例のXMLは出典の内容を引き継ぐが、各プロパティの意味を推測で補わない。出典末尾の `IdGenerator` の Javadoc への `tip`（`:java:extdoc:`）は引き継ぐこと。

## STEP 3 — 記載範囲の線引き

`design.md` §3「記載範囲」により、第2部に置くのはコンポーネント設定ファイルの設定項目・記述例・拡張方法である。**テストソースコードの実装例とテストデータの記述例は第2部に置かない。**

これに関係する判断が2件ある。

### 3-1. `current-0226` の Java コード例は載せない

出典 `03_Tips.rst:339-342` に、`SystemRepository` から `SystemTimeProvider` を取得して `getDate()` を呼ぶ2行のコード例がある。これは設定ではなく API の使用例であり、第2部の記載範囲外である。

**コードブロックは置かない。ただし内容は落とさない。**「固定した日時は `SystemTimeProvider` を通じて取得される」という事実を地の文として残す。判断とその理由を `reviews/page-common.md` に記録すること。

### 3-2. 採番のテストデータ記述例は第3部へ導線を張る

出典の「Excelファイル記述例」（`03_Tips.rst:389` 以降）は本ページに割り当てられていない（`current-0229` として `dest_page=テストデータの記載例` に割り当て済み・作成済み）。

**採番のセクションから、記載例ページへ `:ref:` で導線を張ること。** `design.md` §3「『使い方』に該当するものは第3部に置き、第2部からは `:ref:` で参照する」に従う。

参照先は ``:ref:`テーブルデータを記述する <testdata_examples-table_data>` `` とする。採番の記述例そのもの（`testdata_examples.rst` の `採番処理のテストデータを記述する`）にはラベルが無いが、**承認済みの `#10` のページにラベルを足さない。** 現状で最も近い既存ラベルを指す。より細かい参照が必要になった場合に備え、`reviews/page-common.md` に申し送りとして記録すること。

## STEP 4 — `setup/index.rst` の toctree に追記

現状の `setup/index.rst` は `junit5_extension`・`master_data_restore` の2件を持つ。`common` を先頭に追加する。

```
.. toctree::
   :maxdepth: 1

   common
   junit5_extension
   master_data_restore
```

並びは `design.md` §3 の第2部の構成（共通設定 → クラス単体テストの設定 → リクエスト単体テストの設定 → 取引単体テストの設定 → JUnit 5用拡張機能 → マスタデータ復旧機能）に従う。既存2件の順序は変えない。

## STEP 5 — レビュー

`steering.md`「`#9`〜: ページの作成」の Steps に従う。

- 4観点（A:網羅性 / B:トンマナ / C:用語 / D:整合性）を、それぞれ**別のサブエージェント**で実施する
- プロンプトには Rules の3点（実測で裏付ける／付属の検証スクリプトを正解として使わず独立に組む／敵対的に見る）を必ず含める
- 指摘への対応は最大3ラウンド。`must` を残したまま user review に上げない

**`#10a`・`#10b` の申し送りを本タスクから適用する。**

- 完了条件が「全件表」を求める項目は、**母集合をホワイトリストで切り出さない。** 全走査したうえで、非該当と判定したものも判定理由を添えて表に載せる（`page-testdata_examples.md` 23 / `page-testdata_notation.md` 32）
- 完了条件が「全件表」を求める項目は、ゲートの実行順の先頭に置く
- 概観表・定義セルに具体的なカラム名を列挙しない
- 地の文に書く語は、表・出典・実装に実在することを `grep` で確認してから書く
- **是正ラウンド2以降は、是正差分に限定した検証観点のみを回す。** ラウンド1で4観点を回し、ラウンド2以降は「是正が指示範囲に収まっているか」「是正が新しい欠陥を生んでいないか」だけを見る。全観点の再走査を繰り返すと、新しい観点の指摘がラウンドを伸ばす。**各ラウンドの指摘件数と観点を記録すること**（レビューサイクル改善の効果測定のため）

## STEP 6 — 記録

- `reviews/page-common.md` を新規作成し、`design.md` §11.7 の形式（指摘ID / ラウンド / 観点 / 区分 / 指摘内容 / 対応要否 / 不要の理由 / 対応内容）で全件記録する
- `checks/task-11.md` を新規作成し、ゲートの実行出力を記録する
- `steering.md` に `#11` のエントリを追加し、Steps・Completion criteria を記載する

## ゲート

すべて実行結果で確認し、`checks/task-11.md` に記録すること。**ゲート1（全件表）を実行順の先頭に置く。**

1. `dest_page=共通設定` の5行が全件、ページのどこに反映されたかの対応表（`mapping_id` ごとに反映先のセクションと行番号を記載）。5行すべてが表に現れること
2. `python3 mapping/tools/verify_mapping.py` が exit 0、594行 / 12,986 / 11,983 が不変
3. `git diff f4e4de8 HEAD -- .rn/20260724-ntf-yaml-support/mapping/ ja/conf.py` が空
4. `ja/development_tools/testing_framework/` 配下の全 `.rst` に `テストケース` が0件
5. `setup/common.rst` に `機能概要`・`拡張例` の見出しが0件、`使用方法` が1件
6. `setup/common.rst` に `12桁`・`15桁` が0件
7. `setup/common.rst` の `:ref:` がすべて解決すること。`testdata_examples-table_data` への参照が1件以上あること
8. `setup/index.rst` の toctree に `common` が含まれ、既存2件の順序が変わっていないこと
9. 段落内改行が0件
10. Docker でフルビルド（`-a`）し、`build succeeded` かつ警告が既知の `db_double_submit.rst` 1件のみ（新規0件）
11. `f4e4de8` との差分で、`ja/` 配下の変更が `setup/common.rst`（新規）と `setup/index.rst`（toctree 1行追加）だけであること

## 禁止事項

- `mapping.csv` / `_batch/` / `vocabulary.md` / `style.md` / `glossary.md` / `design.md` / `ja/conf.py` を変更しない
- 承認済みの `#8`・`#9`・`#10`・`#10a`・`#10b` の成果を変更しない。`testdata_examples.rst` にラベルを足さない
- `機能概要`・`拡張例` の見出しを置かない。出典が0行である
- トランザクションの節を作らない。本ページに割り当てられた行が無い
- 出典の「12桁 / 15桁」をそのまま書かない。実装と食い違う
- 採番のクラス（`OracleSequenceIdGenerator` / `FastTableIdGenerator`）について、出典に無い説明を補わない。プロパティ一覧表を作らない
- 出典の脚注（`.. [#]`）・見出し構造・「〜したい」形式の見出しをそのまま持ち込まない
- テストソースコードの実装例・テストデータの記述例を本ページに置かない（`design.md` §3 記載範囲）
- 段落内で改行しない（1段落1行）
- **user review の承認を受けるまで次ページに着手しない**
