# Step 4 指示書 — nablarch-testing-yaml

宛先: `nablarch-testing-yaml` モジュール担当CC

---

## 0. 渡すときの文面

**担当CCには次をそのまま貼る。**

```
Step 4 の作業を依頼します。指示書に18件（実装の是正5件・テスト追加13件）が確定済みで
載っています。探索は不要です。解説書を読み比べて不一致を探す作業ではありません。

作業場:
  /home/tie303177/work/nablarch/nablarch-testing-yaml
  ブランチ feature/ntf-yaml（0db2221）

指示書:
  /home/tie303177/work/nablarch/nablarch-document/.rn/20260724-ntf-yaml-support/ntf-step4-02-nablarch-testing-yaml.md
  nablarch-document の origin/ntf-yaml-support に入っています。
  作業ツリーが古い場合は
  git show origin/ntf-yaml-support:.rn/20260724-ntf-yaml-support/ntf-step4-02-nablarch-testing-yaml.md
  で読んでください。

解説書は 5b5c91e を参照点にしてください。直前の2コミット（bb08f04・5b5c91e）で
setup/common.rst と implementation/testdata_notation.rst が変わっています。必ず
git show 5b5c91e:<path> で読み、作業ツリーの HEAD を読まないでください。

指示書の「1. やること」「2. 実装の是正」「3. テスト追加」「4. 完了条件」「6. 報告」に
従ってください。特に次の3つを落とさないでください。

- 足したテスト・直したテストそれぞれについて、期待値をわざと崩すと落ちることを1度確認し、
  確認したことを報告に書く（「テストが通る」だけでは何かを押さえた証拠になりません）
- 2-2（isResourceExisting）は nablarch-testing-converter のテストを落とします。
  落ちること自体は想定内です。converter は直さず、落ちたテストと理由を報告してください
- 解説書は直さないでください。「解説書が誤っている」と判断した項目は、根拠を添えて
  報告して止めてください

後始末: git status --short が空になること。tmp/ と javac.*.args を残さないこと。
一時ファイル・作業用スクリプト・ログを消すこと。
```

---

## 1. やること

**解説書に書いてあることを、テストで押さえる。** 読み比べて不一致を洗い出す作業ではない。

本指示書には、ディレクターが解説書を全量分解し、既存テスト226件と突き合わせて確定した作業だけが
載っている。**範囲を広げないこと。** 解説書に無い書き方は直さないしテストもしない。

**本モジュールは `src/main` を変更してよい。** タグが0件で未リリースであり、後方互換の対象になる
利用者が存在しないため（2026-08-26 実測）。**依存先の `nablarch-testing` は変更しない。**
リリース済みであり、Step 4 の対象外である。

### 参照点（ピン）

| 対象 | ピン | 読み方 |
|---|---|---|
| 解説書 `nablarch-document` | **`5b5c91e`**（ブランチ `ntf-yaml-support`） | `git show 5b5c91e:<path>` |
| 本モジュール | **`0db2221`**（ブランチ `feature/ntf-yaml`） | 作業ツリーで作業してよい |
| `nablarch-testing` | `3c4bd2a` | `git show 3c4bd2a:<path>`。**変更しない** |
| `nablarch-testing-converter` | `60d9a2d` | `git show 60d9a2d:<path>`。**変更しない** |

**解説書は必ずピンで読む。** 作業ツリーの HEAD はピンとは別物である。

### 落ちたときの扱い

- **実装の是正5件（第2節）は直す。** 解説書が正であり、実装が追いついていない
- **テスト追加13件（第3節）で落ちたものは、直さず `@Ignore` にして記録する。**
  理由に機械的に集められる印を付ける。例:
  `@Ignore("NTF-DOC: implementation/testdata_notation.rst:1322 — 期待 X / 実際 Y")`
  何を直すかはディレクターが全モジュール分を集めてから判断する。範囲の判断を持たないこと

---

## 2. 実装の是正（5件）

### 2-1. 空行判定が Java null を空扱いしている

**解説書**（`5b5c91e` の `implementation/testdata_notation.rst:1500`）:

> 全要素が空のエントリは読み飛ばされる。Excel\ では行の全セルが空の場合、YAML\ では ``rows:``\ 内の要素が空マッピング（\ ``{}``\ ）またはすべての値が空文字の場合にスキップされる。

**スキップの条件は「空マッピング `{}`」と「すべての値が空文字」の2つだけである。** null に触れていない。

**現行**: `src/main/java/nablarch/test/core/reader/yaml/YamlSection.java:201`-`:208`（`0db2221`）の
`isBlankRow` が `str != null && !str.isEmpty()` で判定するため、Java null も空として扱う。
YAML ではクォートなしの `null` とキーだけ書いた `COL:` がロード時点で Java null になるため
（同 `notation.rst:1399`）、それだけの行が消える。

**Excel の対応箇所**（`3c4bd2a`。参考。変更しない）: `PoiXlsReader.java:123` が空セルを `""`、
テキスト `null` を `"null"` にし、`:140`-`:147` の `isBlankLine` が `isEmpty()` だけで判定する。
判定は解釈前の生文字列に掛かるため、`null` だけの行は残る。

**やること**: `isBlankRow` を解説書に合わせる。空文字だけを空と見なし、Java null は非空として扱う。

**波及先（同時に直す）**:

- `src/main/resources/nablarch/test/ntf-testdata-yaml-schema.json:108` と `:136` の `description` が
  「全ての値が null または空文字 `""` の行は、行が無いものとして取り除かれる」と現行挙動を仕様として
  書いている。解説書に合わせる（`:108` は 2-5 でも触る）
- 既存テストのうち期待値の見直しが要るもの: `YamlSectionTest.java` の `dropBlankRows_*` 5件、
  `YamlTableDataBuilderTest.java` の `buildTableDataList_blankValueRow*` 5件・`buildListMapRows_blankValueRow*` 2件。
  **全件を数え直して、どれを変えどれを変えなかったかを報告に書くこと**

### 2-2. `isResourceExisting` の判定単位が Excel と違う

**現行**: `src/main/java/nablarch/test/core/reader/yaml/YamlLoader.java:142`-`:143`（`0db2221`）が
`basePath + "/" + resourceName + ".yaml"` の存在を見る。`resourceName` は `<クラス名>/<読み込み単位名>` の
形で渡るため、**読み込み単位（Excel のシート相当）の存在**を答えている。

**Excel**（`3c4bd2a`。変更しない）: `TestDataReader` は2つを持つ。

| メソッド | 実装 | 単位 |
|---|---|---|
| `isResourceExisting` | `PoiXlsReader.java:232`-`:252` | **入れ物**（`basePath/<クラス名>.xls` または `.xlsx` の存在。シート名を見ない） |
| `isDataExisting` | `PoiXlsReader.java:255`-`:274` | シート（`getSheetNames().contains(sheetName)`） |

`TestDataParser` インタフェースが公開しているのは `isResourceExisting` だけである
（`TestDataParser.java:115`）。呼ぶ側の `TestSupport.java:308`-`:315`（`getPathResourceExisting`）と
`nablarch-testing-rest@ec718a2` の `RestTestSupport.java:235`-`:240` は、**入れ物単位**の意味で使っている。
YAML を挿すと、`setUpDb.yaml` を置いていないテストクラスで `getPathOf` が解決に失敗する。

**やること**: `isResourceExisting` を Excel と同じ入れ物単位に揃える。YAML の入れ物は
`basePath/<クラス名>` ディレクトリである（`implementation/class_unit_test/component.rst:313` が
`<ディレクトリ>/<ファイル名>/<読み込み単位の名前>.yaml` と定めている）。

**呼び出し元は3箇所である**（`0db2221`・`60d9a2d` 実測。全走査済み）:

| # | 箇所 | いまの用途 | 是正後 |
|---|---|---|---|
| 1 | `YamlTestDataParser.java:103` | `TestDataParser` の公開実装 | **入れ物単位に変える** |
| 2 | `YamlTestDataParser.java:109`（`getSetupTableData` の内部ガード） | 事前データが無ければ空リストを返す | **別の判定に置き換える。** Excel は同じ位置で `isDataExisting`（シート単位）を使う（`BasicTestDataParser.java:52`） |
| 3 | `nablarch-testing-converter@60d9a2d` `YamlTestCoreAdapter.java:102` | 本番の呼び出し元は0件。テストのみ | **converter は直さない。** 落ちたテストと理由を報告する |

**#2 を落とすと、`tools/master_data_tool.rst:28` が述べる挙動（Excel 形式のファイルに YAML 用パーサを
設定すると投入0件になり、例外も警告も出ない）が壊れる。** 同時に確かめること。

**converter で落ちるテスト**: `YamlTestCoreAdapterTest.java:365`-`:370`（`isResourceExisting_reflectsFileExistence`）。
**直さずに報告する。**

### 2-3. 送信同期4キーでレコード種別が潰れる

**解説書**（`5b5c91e` の `implementation/testdata_notation.rst:1163`。**直前のコミット `5b5c91e` で改訂済み**）:

> 電文のレコード種別の扱いは、データタイプによって異なる。\ ``MESSAGE``\ （\ ``setUpMessages``\ ・\ ``expectedMessages``\ ）では、記載した値は使われず、デフォルトのレコード種別（\ ``"default"``\ ）になる。同期応答メッセージ送信で使う4つのデータタイプ（\ ``EXPECTED_REQUEST_HEADER_MESSAGES``\ ・\ ``EXPECTED_REQUEST_BODY_MESSAGES``\ ・\ ``RESPONSE_HEADER_MESSAGES``\ ・\ ``RESPONSE_BODY_MESSAGES``\ ）と取引単体テストのモックアップクラスの電文では、記載した値がそのままレコード種別になる。

**現行**: `src/main/java/nablarch/test/core/reader/yaml/YamlFileBuilder.java:187`-`:189`（`0db2221`）が
`messaging` 経路のすべてで `"default"` に固定する。`buildFragmentsForMessage`（`:139`-`:141`）と
`buildFragmentsForSendSync`（`:162`-`:164`）の両方が `messaging=true` を渡すため、送信同期4キーでも
記載値が捨てられる。

**やること**: 送信同期4キーでは `record_type` の記載値を保持する。`messages` は `"default"` のまま
変えない（Excel も `"default"` にするため、既に一致している）。

`getMessage` と `getMessageWithoutCache` はどちらも `YamlMessageBuilder#buildMessagePool` を通るため、
セクションキーで区別する必要がある。`YamlTestDataParser.java:157`・`:164`-`:166` を参照。

**既存テストのうち期待値の見直しが要るもの**: `record_type: HEADER` を書いたフィクスチャ7件、
`record_type: FW_HEADER` を書いたフィクスチャ16件（`0db2221` 実測）。**どれを変えどれを変えなかったかを
報告に書くこと。** 特に次の4件は名前どおりの意味が変わる:
`YamlFileBuilderTest#buildFragmentsForSendSync_fwHeaderRecordTypeIsNotSkipped`、
`YamlMessageBuilderTest#buildMessagePool_fwHeaderRecordTypeIsNotSkipped`、
`YamlTestDataParserTest#getSendSyncMessage_fwHeaderRecordTypeIsNotSkipped`、
`YamlTestDataParserTest#getMessage_fwHeaderRecordTypeIsNotSkipped`。

`implementation/testdata_notation.rst:1299`-`:1301` の「`record_type` に特別な予約値はない」は変わらない。
`record_type: FW_HEADER` は予約値ではなく、送信同期4キーでは単に `FW_HEADER` というレコード種別になる。

### 2-4. テスト用の `yamlInterpreters` が解説書の禁止に反する

**解説書**（`5b5c91e` の `setup/common.rst`）:

- `:77` 「``yamlInterpreters``\ に指定するのは、この2つだけでよい。…\ Excel\ 形式で必要な\ ``NullInterpreter``\ ・\ ``QuotationTrimmer``\ ・\ ``LineSeparatorInterpreter``\ は指定しない。」（2つ＝`DateTimeInterpreter` と `CompositeInterpreter`→`BasicJapaneseCharacterInterpreter`。`:57`-`:68`）
- `:81`（important）「``NullInterpreter``\ を指定してはならない。指定すると、文字列として記述した ``"null"``\ も\ Java\ の\ null\ になり、両者を区別できなくなる。」

**現行**: `src/test/resources/unit-test.xml:56`-`:76`（`0db2221`）の `yamlInterpreters` が
`NullInterpreter` と `LineSeparatorInterpreter` を含む。

**やること**: テスト用の設定を解説書に合わせる。

**あわせて確認すること**: 解説書は直前のコミット `bb08f04` で、YAML 形式の電文用に
`yamlMessagingInterpreters`（`CompositeInterpreter`→`BasicJapaneseCharacterInterpreter` のみ）を
新設した（`setup/common.rst:244`-`:257`）。本モジュールのテストが電文用パーサを別に組んでいる場合は、
そちらも合わせること。

### 2-5. スキーマの `description` 3件が解説書と食い違う

`src/main/resources/nablarch/test/ntf-testdata-yaml-schema.json`（`0db2221`）。

| 行 | 何が食い違うか | 合わせる先 |
|---|---|---|
| `:410`（`length`） | 「`"-"` フィールドの値は NTF が格納時に改行コードおよび前後空白を除去する」が不正確。除去されるのは**改行と、その前後の空白**であって、改行を含まない値の前後空白は残る | `implementation/testdata_notation.rst:1059` |
| `:108`（`rows`。テーブル系） | 空行除去の条件に null を含めている（2-1）。あわせて FK 制約の文言が BOOLEAN 型カラムで矛盾する | `implementation/testdata_notation.rst:1500`・`:820`-`:833` |
| `:136`（`rows`。`list_map`） | 同上（空行除去の条件に null を含めている） | `implementation/testdata_notation.rst:1500` |

**スキーマの `description` も SSoT の適用範囲である**（2026-08-25 ユーザー確定）。利用者が読む仕様文であり、
解説書と食い違えば同じ問題が再発する。

---

## 3. テスト追加（13件）

いずれも**解説書に記述があり、既存テスト226件が押さえていないもの**である（`0db2221` 実測）。
既に押さえているものを二重に書かないこと。

| # | 解説書（`5b5c91e`） | 押さえるもの | 既存の状況（実測） |
|---|---|---|---|
| 3-1 | `notation.rst:92`・`:1399`、`implementation/deal_unit_test/batch.rst:352` | YAML 1.2 Core Schema で解釈されるため、クォートなしの `no`・`yes`・`on`・`off` がキーでも値でも文字列のままになる。とくに `batch.rst:352` の実例 `- no: "1"` はキー `no` を引用符なしで書いており、YAML 1.1 なら真偽値 `false` になる | `yes`・`on:`・`off` の出現0件。`yamlNativeBooleanIsStringified` は値の `true`/`false` のみ（`YamlTestDataParserTest.java:198`-`:208`） |
| 3-2 | `notation.rst:1313`-`:1320` | `${<文字種>,3}` が14文字種それぞれで該当文字種3文字になる（サロゲートペアは3コードポイント）。列挙外の文字種名は変換されない | 半角英字・半角数字の2種のみ（`YamlTableDataBuilderTest.java:616`-`:640`） |
| 3-3 | `notation.rst:1322` | `"${半角数字,2}-${半角数字,4}"` が7文字になり、3文字目が `-` のまま残る（組み合わせ記法） | 0件 |
| 3-4 | `notation.rst:1441`-`:1443` | `"\n"` が LF 1文字（`U+000A`）になる | `\r` のみ（`buildListMapRows_escapedCrIsCarriageReturn`）。`\n` は0件 |
| 3-5 | `notation.rst:1326`-`:1331` | `"20210123123456"` が `2021-01-23 12:34:56.000`、`"20210123"` が `2021-01-23 00:00:00.000` に評価される（時刻の後置0埋め省略） | 0件 |
| 3-6 | `notation.rst:1337` | `"${attach:ファイルパス}"` がアップロードファイルの指定として読める | 0件 |
| 3-7 | `notation.rst:255`-`:269` | グループIDは完全一致で突合される。`case01` を指定したとき `case010` を持つエントリは収集されない | 0件（`case010` の出現0件） |
| 3-8 | `notation.rst:205` | `setup_tables_extra` のような前方一致するトップレベルキーは `setup_tables` として読まれず、スキーマ違反になる | 0件 |
| 3-9 | `notation.rst:339` | `expected_tables` に group_id `a`・`b`・`a` の順でエントリを並べても、group_id `a` の収集結果は2件になる（Excel のように1件で打ち切られない） | 0件 |
| 3-10 | `notation.rst:1149` | `messages` の `id` に予約値 `setUpMessages`・`expectedMessages` を書いて取得できる | 0件（両文字列の出現0件） |
| 3-11 | `implementation/deal_unit_test/mom.rst:72` | モックアップクラスの電文は、リクエストIDと同じ名前のディレクトリ配下の固定名 `message.yaml` が読み込み単位になる。`<リクエストID>.yaml` のような配置では読まれない | 0件（`message.yaml` の出現0件） |
| 3-12 | `implementation/class_unit_test/component.rst:313` | `TestDataParser` を直接使うとき、第2引数 `<ファイル名>/<読み込み単位の名前>` が `<ディレクトリ>/<ファイル名>/<読み込み単位の名前>.yaml` に解決される | 0件（`CommonTestData` の出現0件） |
| 3-13 | `notation.rst:503`-`:507` | `rows:` に `args[0]: "x"` と書くと、返る Map のキーが文字列 `"args[0]"` になる（`[` `]` を含むキーがマーカーカラムとして除外されない） | `buildListMapRows_partialBracketKeyIsNotExcluded` は片側だけの `[` を見るもので、`args[0]` 形式は0件 |

**3-2 の「列挙外の文字種名は変換されない」は負のテストである。必ず書くこと。**

`notation.rst:1059` の `fields[].length: "-"`（全レコードの最大バイト長への自動拡張と、値中の改行と
その前後の空白の除去）は、`schemaFullCoverage.yaml:87` にデータはあるが挙動を押さえるテストが無い。
**2-5 で `description` を直すため、その根拠として同時に押さえること。**

---

## 4. 完了条件

1. **第2節の5件がすべて是正されている。** 是正ごとに、直す前は落ちて直したあとは通るテストがあること
2. **第3節の13件について、テストが存在する。** 落ちたものは `@Ignore` ＋ 印つきの理由で記録されている
3. **足したテスト・直したテストそれぞれについて、期待値をわざと崩すと落ちることを1度確認している。**
   確認したことを報告に書く。「テストが通る」だけでは、そのテストが何かを押さえた証拠にならない
4. **既存テストの期待値を変えた箇所が全件挙がっている。** 2-1・2-3 は既存テストの期待値に触れる。
   どれを変えどれを変えなかったかを、件数を数えたうえで報告する
5. **カバレッジ C0/C1 を計測し、結果を報告する。** `src/main` の是正で下がった箇所があれば挙げる
6. `mvn test` が緑であること。converter で落ちるテスト（2-2）は本モジュールの外なので対象外
7. `git status --short` が空。`tmp/` と `javac.*.args` を残さない
8. 変更を push する

---

## 5. やらないこと

- **解説書を直さない。** 「解説書が誤っている」と判断した項目は、根拠（`file:line` と参照コミット）を
  添えて報告して止める
- **`nablarch-testing` を直さない。** リリース済みであり `src/main` は変更禁止
- **`nablarch-testing-converter` を直さない。** 2-2 で落ちるテストは報告するだけ
- **解説書に無い書き方を追いかけない。** 誤った書き方は無限にあり、追い始めると完了条件が動く
- **Excel の実装に合わせない。** 合わせる先は解説書である

---

## 6. 報告

次の5つを、この順で1つのファイルにまとめる。

1. **第2節5件の是正結果。** 是正ごとに、変更したファイルと `file:line`、直す前に落ちたテストの名前
2. **第3節13件の結果。** 通ったもの・`@Ignore` にしたものの内訳。`@Ignore` は理由の文言をそのまま載せる
3. **期待値をわざと崩す確認の結果。** 対象テスト名と、崩した内容
4. **既存テストの期待値を変えた箇所の全件。** 2-1・2-3 それぞれについて件数を数えたうえで
5. **カバレッジ C0/C1 の計測結果**と、converter で落ちたテスト（2-2）

---

## 7. レビュー

**4観点レビューは回さない。** 作業が18件に確定していて探索を含まないこと、成果物が確定済みの作業だけに
なることによる。ディレクターが担当範囲を全量読み直して独立に検証する。

観点D（検証の妥当性）は、完了条件3「期待値をわざと崩すと落ちること」で代替する。
