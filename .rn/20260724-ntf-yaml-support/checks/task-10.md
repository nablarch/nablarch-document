# self-check: #10 テストデータの記載例

対象: `ja/development_tools/testing_framework/implementation/testdata_examples.rst`
実施日: 2026-08-07

## 1. マッピングの反映

```
$ python3 -c "import csv; rows=list(csv.DictReader(open('.rn/20260724-ntf-yaml-support/mapping/mapping.csv',encoding='utf-8'))); \
print(len(rows), len([r for r in rows if r['dest_page']=='テストデータの記載例']))"
594 65
```

`dest_page=テストデータの記載例` は65行（`csv.DictReader` でカウント。`wc -l` は不使用）。全65行の反映先は観点Aのレビューで1行ずつ突き合わせ済みで、落丁0件・創作0件（`reviews/page-testdata_examples.md` 参照）。出典の内訳と反映先の対応は次のとおり。

| 出典 | 行数 | 反映先（L2） |
|---|---|---|
| `input/ntf-testdata-doc-examples-overview.md` | 6 | データブロックとデータタイプ / グループIDによる使い分け |
| `input/ntf-testdata-doc-examples-table.md` | 4 | テーブルのデータを記述する / LIST_MAPのデータを記述する |
| `input/ntf-testdata-doc-examples-testshots.md` | 4 | テストケース一覧（testShots）を記述する |
| `input/ntf-testdata-doc-examples-file.md` | 22 | ファイルのデータを記述する |
| `input/ntf-testdata-doc-examples-messaging.md` | 17 | メッセージングのデータを記述する |
| `input/ntf-testdata-doc-examples-special.md` | 11 | 値を特殊記法で記述する / ファイルのデータを記述する / コメント・マーカーカラム・空エントリを扱う / テーブルのデータを記述する |
| `06_TestFWGuide/03_Tips.rst`（削除済み、`git show 6bf8cfb^:` で参照） | 1 | テーブルのデータを記述する（採番処理） |

姉妹ページ `testdata_notation.rst` に既にある制約・仕様は本ページで再掲せず、各節の導入文から `:ref:` で参照して解決した。

出典の `[要確認]` 2件はいずれも解消した。

- `ntf-testdata-doc-examples-overview.md:87`（Excel 例と YAML 例で `description` が食い違う）→ 「注文カウンタが正しくインクリメントされます」に統一
- `ntf-testdata-doc-examples-special.md:53`（`${updateTime}`・`${setUpTime}` の定義が無い）→ `testdata_notation.rst:1294` の定義に従って記述

## 2. 構成と規約

```
$ python3 -c "...見出し集計..."
{'L2': 9, 'L3': 28, 'L4': 56}  lines: 1883
```

- L2 9個は `design.md`「テストデータの2ページ」節の規定どおり、`testdata_notation.rst` の対応する見出しと文言・順序が一致（観点Bで 9/9 を実測）。「テストクラスとテストデータの対応」は規定どおり不在
- 「機能概要」「使用方法」を持たない構成（`design.md` §4 の例外規定、`style.md` S-02）
- 全 L3（28個）が末尾2つに `Excel形式の場合` / `YAML形式の場合` の L4 対を持つ
- L3 導入文の形式別 L4 予告（S-11）: 未充足0件

```
L3 intros without format preview: 0
```

- admonition の配置（S-10 規約1・3）: L4 配下に残るのは1件のみで、これは Excel 固有の内容（シート内の記述順）であり正しい配置

```
admonitions inside L4: 1
  (286, 'Excel形式の場合', '同じグループIDのデータブロックは、シート内で連続させて記述する。…')
```

- 表記法: `list-table` 49件、simple table 0件、grid table 0件（`style.md` S-07 のページ単位例外を適用。`#10` で例外の発動条件を追記）
- 識別子行は全件が表外の地の文に「」付きの普通の文字（S-10 規約2・規約4）

## 3. 機械検証

```
yaml blocks ok: 28, errors: 0
tables: 49, issues: 0          # :widths: の要素数=列数、合計=100
short underlines: 0            # 東アジア文字幅換算でアンダーライン不足なし
```

観点Dのレビューでは、28個の YAML ブロックを `ntf-testdata-yaml-schema.json`（Draft 2020-12）で検証し、必須キー欠落・未定義キー・型不正・enum 違反いずれも0件であることを確認した。

## 4. ビルド

Docker でクリーンフルビルド（`rm -rf _build` 後に再実行）。

```
$ docker run --rm -v "$(pwd)":/root/document nablarch-document-build-sandboxed /bin/bash -c \
  "cd /root/document; rm -rf _build; sphinx-build -d _build/.doctrees/ja -b html ja _build/html"
…
/root/document/ja/application_framework/application_framework/libraries/db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test (…)
build succeeded, 1 warning.
```

警告は既知の1件（`#last` で解消予定の外部被参照ラベル）のみ。本ページ起因の警告・エラーは0件。

## 5. toctree

`ja/development_tools/testing_framework/implementation/index.rst:10` に `testdata_examples` を登録済み（`#9` の前方参照スタブ作成時に追記済み）。`testdata_notation.rst` からの被参照ラベル9件はすべて解決（未定義ラベル警告なし）。

## 6. 実装で裏付けた是正

観点Dの指摘に伴い、`/home/tie303177/work/nablarch/` 配下の実ソースで次を確認したうえで是正した。

| 事実 | 裏付け |
|---|---|
| 固定長ファイルの全レコード定義は同一レコード長でなければならない | `FixedLengthFile.java:96-113`（`getRecordLength` が不一致時に `IllegalStateException`） |
| `sendSyncTestData` はベースパスキーであり識別子ではない | `SendSyncSupport.java:46`（`RESPONSE_MESSAGES_SHEET_NAME = "message"`）、`:49`（`SEND_SYNC_TEST_DATA_BASE_PATH`）、`:346-348`。`DataType.MESSAGE` はこの経路に渡らない（`:67,82` は `EXPECTED_REQUEST_*`、`MockMessagingClient.java:57,70` は `RESPONSE_*`） |
| デフォルト値の補完対象はカラム名自体を書かなかったカラム | `TableData.java:706-722`（`allColumns` から `columnNames` を除いた集合が対象） |
| Excel の宣言済みカラムの欠落セルは空文字になる | `HeaderLine.java`（`String val = (i >= line.size()) ? "" : line.get(i);`） |
| YAML 経路に `QuotationTrimmer` は入らない | `YamlFileBuilder.java:246-252`、`nablarch-testing-yaml/src/test/resources/unit-test.xml:53-58` |
| `HTTP_METHOD` は `context` の `LIST_MAP` から取得される | `TestCaseInfo.java:28,40,306-308` |

## 7. 判断を仰ぐ事項

`reviews/page-testdata_examples.md`「判断・申し送り」に記載。user review で確認いただきたいのは次の2件。

- **判断1**: コメント行（`// この行もスキップされます`）を表内に残した。`style.md` S-10 規約2 の「1セルしか値がない行を表に残さない」は識別子行を対象とした規定と解したが、記載例としての価値と規約の文言のどちらを優先するか
- **判断2**: 承認済みの `#9`（`testdata_notation.rst`）に3件の是正を入れた。いずれも実装で裏付けた事実誤りで、放置すると本ページと矛盾する（`sendSyncTestData` の説明、YAML 例の旧識別子、`HTTP_METHOD` の所在）

## 8. 禁止事項の遵守

| 禁止事項 | 遵守状況 |
|---|---|
| `mapping.csv` を変更しない | 遵守（`git status` に現れない） |
| `glossary.md` / `vocabulary.md` / `design.md` を変更しない | 遵守（同上） |
| 実装ソースを変更しない | 遵守（`/home/tie303177/work/nablarch/` は読み取りのみ） |
| `_build/` を削除したまま残さない | 遵守（クリーンビルドで再生成済み） |

`style.md` は2箇所追記した（判断4）。`#9` でも同ページを改訂しており、変更禁止対象ではない。
