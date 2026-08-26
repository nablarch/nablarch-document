# Step 4 指示書 — nablarch-testing-converter

宛先: `nablarch-testing-converter` モジュール担当CC

---

## 渡す前にやること（ディレクター向け。CC には渡さない）

**`nablarch-testing-yaml` の Step 4 が完了するまで、本指示書を渡さない**（2026-08-26 user 了承）。

本モジュールは `nablarch-testing-yaml` に依存する（`pom.xml:40`-`:44`。`1.0.0-SNAPSHOT`）。
yaml 側の是正 2-2（`isResourceExisting` の判定単位を入れ物に揃える）は、**本モジュールのテストを
意図的に落とす**。この状態で渡すと、CC は落ちたテストが自分の変更のせいか yaml のせいかを
切り分けられない。

**2026-08-26 20:58 の実測**（`mvn -o clean test -Dtest=YamlTestCoreAdapterTest`）:

```
Tests run: 18, Failures: 1
YamlTestCoreAdapterTest.isResourceExisting_reflectsFileExistence:370
```

同時点で yaml リポジトリは作業中だった。HEAD がピン `0db2221` から `e9bee93` へ進み、
`src/main` が7ファイル・+187/-65。指示書18件のうち 2-1・2-2・2-3 が済み、2-4・2-5 と
テスト追加13件が残っていた。`~/.m2` の yaml jar は 20:31 に install された**作業途中の版**である。

**渡す前の手順**

1. yaml CC の完了報告を受け、ディレクターが `0db2221` からの差分を全量読み直して独立に検証する
2. **yaml のピンを取り直す**。本指示書の参照点の表と 2-2・「5. やらないこと」を更新する
3. yaml を `mvn install` する
4. **「5. やらないこと」の `YamlTestCoreAdapterTest.java:365`-`:370` の扱いを書き換える。**
   yaml が直ったあとは「落ちるのが想定内」ではなく「**期待値を yaml の新しい仕様に合わせて直す**」に変わる。
   これは第2節の是正に足す（件数も更新する）
5. `nablarch-testing` は**取り直し不要**。`~/.m2` の `nablarch-testing-6-NEXT-SNAPSHOT.jar`
   （2026-08-21 18:28 install）は PR ブランチ由来であることを実測で確認した
   （`javap` で `TestDataParsingTemplate` にブランチだけが持つ `cachedParse`・`tryLoadFromCache`・
   `storeToCache`・`saveCache` があること）。さらにピン `3c4bd2a` とブランチ先端 `44b9cc9` は
   `src/main` がバイト同一である

---

## 0. 渡すときの文面

**担当CCには次をそのまま貼る。**

```
Step 4 の作業を依頼します。指示書に15件（実装の是正4件・テスト追加11件）が確定済みで
載っています。探索は不要です。解説書を読み比べて不一致を探す作業ではありません。

作業場:
  /home/tie303177/work/nablarch/nablarch-testing-converter
  ブランチ ntf-test-data-converter（60d9a2d）

指示書:
  /home/tie303177/work/nablarch/nablarch-document/.rn/20260724-ntf-yaml-support/ntf-step4-05-nablarch-testing-converter.md
  nablarch-document の origin/ntf-yaml-support に入っています。
  作業ツリーが古い場合は
  git show origin/ntf-yaml-support:.rn/20260724-ntf-yaml-support/ntf-step4-05-nablarch-testing-converter.md
  で読んでください。

解説書は 5783b35 を参照点にしてください。直前の3コミット（7f194a7・45c3852・5783b35）で
tools/testdata_converter.rst が変わっています。必ず git show 5783b35:<path> で読み、
作業ツリーの HEAD を読まないでください。

指示書の「1. やること」「2. 実装の是正」「3. テスト追加」「4. 完了条件」「6. 報告」に
従ってください。特に次の5つを落とさないでください。

- 2-1 と 2-3 には「着手前に検証すること」があります。実装に入る前に、その結果だけを
  先に報告してください。反例が見つかったら実装せずに止めてください
- 第2節の4件は直してください。ここは判断済みです。
  第3節のテスト追加11件で落ちたものは、直さず @Ignore にして記録してください。
  理由に機械的に集められる印を付けます。例:
  @Ignore("NTF-DOC: tools/testdata_converter.rst:287 — 期待 X / 実際 Y")
  何を直すかは全モジュール分を集めてからディレクターが判断します。範囲の判断を持たないでください
- 完了条件3（母集合の4経路）を落とさないでください。RoundTripTest は中間モデルを起点に
  するので、この確認の代わりになりません。実ファイルを起点にし、テスティングフレームワークが
  解釈したあとの値で比べてください
- 足したテスト・直したテストそれぞれについて、期待値をわざと崩すと落ちることを1度確認し、
  確認したことを報告に書く（「テストが通る」だけでは何かを押さえた証拠になりません）
- 解説書は直さないでください。「解説書が誤っている」と判断した項目は、根拠を添えて
  報告して止めてください

ビルドの注意: target/classes が jacoco 計装済みのまま残っていることがあり、その状態の
mvn test は「Cannot process instrumented class」で失敗します。mvn clean test を使ってください。

後始末: git status --short が空になること。一時ファイル・作業用スクリプト・ログを
残さないでください（jacoco.exec と target/ は .gitignore に入っているので消さなくてよい）。
```

---

## 1. やること

**解説書に書いてあることを、テストで押さえる。** 読み比べて不一致を洗い出す作業ではない。

本指示書には、ディレクターが解説書を全量分解し、既存テストと突き合わせて確定した作業だけが載っている。
**範囲を広げないこと。** 解説書に無い書き方は直さないしテストもしない。

**本モジュールは `src/main` を変更してよい。** タグが0件で未リリースであり、後方互換の対象になる
利用者が存在しないため（2026-08-26 実測）。**依存先の `nablarch-testing`・`nablarch-testing-yaml` は
変更しない。**

### 参照点（ピン）

| 対象 | ピン | 読み方 |
|---|---|---|
| 解説書 `nablarch-document` | **`5783b35`**（ブランチ `ntf-yaml-support`） | `git show 5783b35:<path>` |
| 本モジュール | **`60d9a2d`**（ブランチ `ntf-test-data-converter`） | 作業ツリーで作業してよい |
| `nablarch-testing` | `3c4bd2a` | `git show 3c4bd2a:<path>`。**変更しない** |
| `nablarch-testing-yaml` | **渡す前に取り直す**（`0db2221` は古い。Step 4 で `src/main` が動いている） | `git show <取り直したピン>:<path>`。**変更しない** |

**解説書は必ずピンで読む。** 作業ツリーの HEAD はピンとは別物である。

### 担当ページ

`ja/development_tools/testing_framework/tools/testdata_converter.rst`（`5783b35` で329行）を軸にする。
**あわせて、第2節の完了条件の母集合として次の2箇所を使う。**

| 用途 | ページ | 範囲 |
|---|---|---|
| 担当ページ（全量） | `tools/testdata_converter.rst` | 329行すべて |
| 完了条件の母集合 | `implementation/testdata_notation.rst` | 「null・空文字・改行など特殊な値を記述する」の特殊記法の表2つ（Excel 形式・YAML 形式） |
| 完了条件の母集合 | `implementation/testdata_examples.rst` | 「null・空文字・改行など特殊な値を記述する」の節 |

**完了条件の基準は「書き方（`testdata_notation.rst`）と記載例（`testdata_examples.rst`）に載っている状態が、
変換後も同じ意味で読めること」である**（2026-08-26 ユーザー確定）。「同じ意味」とは、
**テスティングフレームワークが解釈したあとの値が一致すること**を指す。セルの見た目ではない。

### 落ちたときの扱い

- **実装の是正（第2節）は直す。** 解説書が正であり、実装が追いついていない
- **テスト追加（第3節）で落ちたものは、直さず `@Ignore` にして記録する。**
  理由に機械的に集められる印を付ける。例:
  `@Ignore("NTF-DOC: implementation/testdata_notation.rst:1363 — 期待 X / 実際 Y")`
  何を直すかはディレクターが全モジュール分を集めてから判断する。範囲の判断を持たないこと

---

## 2. 実装の是正（4件）

### 2-1. Excel 形式の読み書きが記法⇄値の対称な写像になっていない

**これが第2節の根本で、以下の4つの症状はすべてこの1つの原因から出る。**

**解説書**（`5783b35` の `tools/testdata_converter.rst:14`）:

> 本ツールは、\ Excel\ 形式と\ YAML\ 形式のどちらか一方を正とするのではなく、両者の間に、テスティングフレームワークの仕様上の意味だけを持つ中間モデルを置く。

**同 `:22`**（節見出し）: 「意味を変えずに往復できる」。
**同 `:34`-`:35`**（表）: 「値 / 未変換のまま保持する。``${systemTime}``\ などの特殊記法は解決せず、文字列として持つ」。

**中間モデルが持つべきは「テスティングフレームワークが解釈したあとの値」である。**
すなわち Java null（値なし）か `String`（実際の文字列）であり、`null` リテラル・クォート記法・
`\r` といった **Excel 形式固有の記法そのものではない**。`${systemTime}` などは
テスティングフレームワークが**テスト実行時に**解釈するものなので（`:61`）、記法のまま持つ。
両者は別の話である。

**現行**: Excel の読み込みは `QuotationTrimmer` だけを掛け（`XlsFormatReader.java:526`・`:539`-`:545`。
`60d9a2d`。以下同じ）、`NullInterpreter`・`LineSeparatorInterpreter` を掛けない。
書き出しは中間モデルの Java null だけを `null` リテラルにする（`XlsFormatWriter.java:581`）。
**読みで外した記法を書きで戻さないため、写像が非対称になっている。**

Excel 形式で必要なインタープリタが `NullInterpreter`・`QuotationTrimmer`・`LineSeparatorInterpreter` の
3つであることは解説書 `setup/common.rst:77` が述べている。

**実測した症状（4件。すべて `60d9a2d` × `3c4bd2a` で計測。読み取り専用のプローブで、どのリポジトリも変更していない）**

テスティングフレームワークが解釈したあとの値を、往復の前後で比べたもの。

| # | 記法（解説書） | 原本 | XLS→XLS 後 | XLS→YAML 後 |
|---|---|---|---|---|
| a | `null`（`notation.rst:1360` DBに null を格納） | Java null | Java null | **文字列 `null`** |
| b | `"null"`（`notation.rst:1363` 文字列の null） | 文字列 `null` | **Java null** | 文字列 `null` |
| c | `"""`（`notation.rst:1378` ダブルクォート1文字） | `"` | **再読込で例外** | `"` |
| d | `\r`（`notation.rst:1390` CR） | CR（`U+000D`） | CR | **2文字の `\` ＋ `r`** |

- a・b は、読みで `NullInterpreter` を掛けないため `null` と `"null"` が中間モデルで同じ文字列
  `null` に潰れることによる
- c は、書き戻しでクォートを付け直さないため `"` 1文字のセルになり、再読込で
  `QuotationTrimmer.java:25`-`:27`（`3c4bd2a`）が `substring(1, 0)` を実行して落ちることによる
- d は、読みで `LineSeparatorInterpreter` を掛けないため2文字の `\r` が中間モデルへ入り、
  YAML 側でエスケープされた `"1\\r2"` として書き出されることによる。YAML 形式の
  インタープリタには `LineSeparatorInterpreter` を指定しない（`setup/common.rst:77`）ため、
  読み戻すと2文字のままになる

**やること**

1. **Excel の読み込みで、`NullInterpreter` → `QuotationTrimmer` → `LineSeparatorInterpreter` を
   この順に掛ける。** 中間モデルには解釈後の値（Java null または `String`）を入れる。
   `${...}` 系のインタープリタは**掛けない**（`:61`。テスト実行時に解釈されるべきもの）
2. **Excel の書き出しで、その逆写像を行う。** Java null は `null` リテラル。`String` は、
   そのまま書くと別の意味に読まれる場合だけ記法へ戻す。**戻す条件は、掛けるインタープリタの
   実装から一意に決まる**（`3c4bd2a` 実測）:

   | # | 条件 | 戻し方 | 根拠 |
   |---|---|---|---|
   | i | CR（`U+000D`）を含む | その文字を2文字の `\` ＋ `r` へ戻す | `LineSeparatorInterpreter.java:31`・`:34` が既定で `\\r` を CR に置換する（`notation.rst:1390`-`:1391`） |
   | ii | `"null"` に `equalsIgnoreCase` する | 前後を半角ダブルクォートで囲む | `NullInterpreter.java:11`・`:15` が `equalsIgnoreCase("null")` で Java null に置き換える（`notation.rst:1360`） |
   | iii | 半角 `"` で始まり半角 `"` で終わる、または全角 `”` で始まり全角 `”` で終わる | 前後を半角ダブルクォートで囲む | `QuotationTrimmer.java:25`-`:27` が `startsWith` ＋ `endsWith` で判定して外側1層を外す（`notation.rst:1363`・`:1379`） |

   **iii は1文字の `"`（および1文字の `”`）を含む。** `QuotationTrimmer.java:25`-`:26` の
   `startsWith("\"") && endsWith("\"")` は1文字の `"` に対して真になり、`:27` の
   `substring(1, str.length() - 1)` が `substring(1, 0)` になって落ちる。囲まないと
   再読込で例外になる（上表 c）。

   **適用順は i → ii → iii である。** i で増える `\` ＋ `r` は ii・iii の判定に影響しない。
   **ii と iii は排他である**（`"null"` は ii に該当せず iii に該当する）。

   **戻さないもの**: 値の途中のダブルクォート（`ab"c` は `notation.rst:1379` のとおり
   そのまま書けばよい。`QuotationTrimmer` は前後が揃っていなければ何もしない）、
   2文字の `\` ＋ `n`（`notation.rst:1391` のとおり変換されない）、LF（`U+000A`。
   `notation.rst:1393` のとおりセル内の改行としてそのまま書く）
3. **YAML 側は変更しない。** YAML はもともと解釈後の値を扱う（`notation.rst:1399`）ため、
   中間モデルを解釈後の値にすれば写像はそのまま合う

**波及先（同時に直す）**

- **`RoundTripTest.java:652`-`:665` `nullCell_xlsConvertsToLiteralString_yamlPreservesNull` は、
  この非可逆を「既知の非可逆挙動を固定するテスト」として期待値に書いている**（`:643` の見出し、
  `:660` の `assertThat(xlsBack.getRows().get(0).get(0), is("null"))`）。是正後は XLS 経路でも
  null が保持されるため、期待値を `nullValue()` に変え、メソッド名と Javadoc も直す
- **`RoundTripTest` のクラス Javadoc `:47`-`:53`「可逆性の対象外」から、null の非対称の記述
  （`:50`-`:52`）を落とす**
- **`XlsFormatWriter` のクラス Javadoc `:56`-`:58`「読み戻しでは文字列 `null` として戻るため、
  `null`↔`null` は Excel 経路では復元されない」を落とす**
- **`XlsFormatReader.java:528`-`:538` の `stripQuotes` の Javadoc は、`QuotationTrimmer` だけを
  掛ける前提で書かれている。**掛けるインタープリタが3つになるので書き直す

**`RoundTripTest` は完了条件3の代わりにならない。** 同テストは**中間モデルを起点にして
中間モデルへ戻す**（クラス Javadoc `:43`）ため、記法⇄値の写像が非対称でも、書きと読みが
同じ非対称であれば緑になる。実際、上表の4件はいずれも同テストが緑のまま起きている。
完了条件3は**実ファイルを起点にし、テスティングフレームワークが解釈したあとの値で比べること。**

**着手前に検証すること**: 上の「戻す条件」に反例がないかを、`notation.rst` の Excel 形式の表
（13行）と YAML 形式の表（13行）の全行で確かめ、結果を報告してから実装に入る。
**反例が見つかったら、実装せずに報告して止める。**

### 2-2. 全フィールドが空文字のレコードが Excel 形式へ書き戻せない

**解説書**（`5783b35` の `implementation/testdata_examples.rst:2231`）:

> 全フィールドが空文字のレコードは、いずれか1つのフィールドに ``""``\ と記述する。全セルを空にした行は読み飛ばされ、レコードにならないためである。

**現行**: この記載例（同 `:2237`-`:2260`）の Excel 形式を往復させると、**レコードが1件消える**。
実測では、テスティングフレームワークが読むレコードが原本3件・XLS→XLS 後2件・XLS→YAML→XLS 後2件だった。

原因は 2-1 と同じで、`""` が読みで空文字になり（`XlsFormatReader.java:425`）、
書き戻しで全セルが空の行になり、再読込のときテスティングフレームワークに読み飛ばされることによる。
**YAML 形式では `rows:` に `["", "", ""]` として正しく残っている**（同 `:2291`「Excel 形式と違い、
行が読み飛ばされることはない」）ので、壊れるのは Excel 形式へ書き出す側だけである。

**やること**: ファイル・メッセージのデータ行を Excel 形式へ書き出すとき、
**全要素が空文字になる行は、先頭要素を `""` と書く。** 記載例 `:2231` が定める書き方に合わせる。

**テーブルと `LIST_MAP` は対象外である。** 全要素が空のエントリは読み飛ばすのが記法であり
（`notation.rst:1500`）、全要素が空のエントリを記述する記法が無いため、変換先の形式で表せない。
この点は解説書 `tools/testdata_converter.rst:63` に明記済みである。

### 2-3. 中間モデルが Excel 形式の書式（`[ ]`）を持っている

**解説書**（`5783b35` の `tools/testdata_converter.rst:14`）: 中間モデルが持つのは
「テスティングフレームワークの仕様上の意味だけ」である。**グループIDを囲む半角角括弧 `[ ]` は
Excel 形式の書式であって値ではない。**

**現行**: `TestDataBlock.groupId` が整形済み（`[case1]`）で保持されている。
`YamlFormatReader.java:485`-`:488`（`formatGroup`）が YAML の生値を読んだ直後に `"[" + groupId + "]"` で
囲み、`YamlFormatWriter.java:479`-`:488`（`rawGroup`）が書き出しで剥がしている。

**現状は壊れていない。** 4種のグループIDで往復を実測した（2026-08-26）。壊れていないのは
両リーダーが同じ形に揃えているためで、モデルの持ち方が正しいからではない。

**やること**: 中間モデルは**生値**で持つ。`[ ]` の付け外しは Excel 形式の中だけで行う。

- `YamlFormatReader.formatGroup` の `[ ]` 付与をやめる
- `YamlFormatWriter.rawGroup` の推測剥がしをやめる（生値をそのまま書く）
- `[ ]` を付けるのは `XlsFormatWriter.java:529`-`:531`（`marker`）の中だけにする
- `[ ]` を外すのは `TestCoreReaderAdapter.java:282`-`:286`（`markerGroupId`）の中だけにする

**着手前に検証すること**: `groupId` の読み書きに関わる箇所を全走査し、`[ ]` に依存している箇所を
全件挙げてから実装に入る。既存テストの期待値に `[case1]` 形式が現れる箇所も全件挙げる。

### 2-4. 既存の `@Ignore` 2件は、解説書に記述の無い「あるべき姿」を追っている

**どちらも削除する。** `解説書に無い書き方は直さない・テストしない` に反する。
他責先がリリース済みの `nablarch-testing` であり、直す予定も無いため、置いておくと
永久に赤いままの宿題になる。

| # | テスト（`60d9a2d`） | `@Ignore` の主張 | 実測 |
|---|---|---|---|
| 1 | `YamlFormatReaderInvalidInputTest.java:740` `failsToReadRecordFragmentRowWithMoreValuesThanFields` | 「反映されない値がある入力はエラーになるべき（`testdata_notation.rst:891`）」。他責先は `DataFileFragment#addValue` | **`5783b35` の `:891` はパディングとバイナリデータの記述で、この主張は無い。** 超過値を黙って捨てる挙動は論点4 として **user 判断済み（現行どおりで仕様。解説書影響なし）** |
| 2 | `YamlFormatReaderInvalidInputTest.java:1280` `keepsOriginalColumnCaseInTable` | 「カラム名の大小を保つあるべき姿」。他責先は `TableData` | **解説書にテーブルのカラム名の大小についての記述は0件**（`5783b35` の `ja/development_tools/testing_framework` 全走査） |

**やること**: 2件のテストメソッドを削除する。あわせて、同ファイルの Javadoc や他のテストから
この2件を `{@link}` で参照している箇所を全走査して、参照ごと外す。

**削除するのはこの2件だけである。** 他に `@Ignore` を足す必要が出た場合（第3節・完了条件3）は、
印つきの理由を付けて残すこと。


---

## 3. テスト追加（11件）

いずれも**解説書に記述があり、既存テスト605メソッドが押さえていないもの**である（`60d9a2d` 実測）。
既に押さえているものを二重に書かないこと。

| # | 解説書（`5783b35`） | 押さえるもの | 既存が0件であることの実測 |
|---|---|---|---|
| 3-1 | `:53`-`:55` | 上の 3-2〜3-5 で `YamlTestDataValidator` が報告する種類の不正な YAML を変換元にしても、`TestDataConverter.convert` が検証を理由に失敗しない（変換自体は完走する） | `YamlTestDataValidator` を `src/main` から参照している箇所は自ファイル以外0件。テスト側の参照も `YamlTestDataValidatorTest` と `YamlFormatReaderInvalidInputTest` の2ファイルだけで、**入口を `TestDataConverter`／`ConverterMojo` にしたものは0件** |
| 3-2 | `:59` | セルの背景色・書式・結合セルを設定した Excel を xls→xls で往復させると、往復後のセルにその色・書式・結合が無い | `addMergedRegion`・`MergedRegion`・`createComment` の出現0件。既存の色・罫線テスト（`XlsFormatWriterTest.java:553`・`:578`・`:597`・`:616`・`:635`・`:657`・`:678`・`:701`・`:752`・`:849`・`:870`）は**書き出したブックを見るだけで往復させていない** |
| 3-3 | `:59` | コメント行を含む YAML を yaml→yaml で往復させると、往復後にコメントが無い | コメントを入力に置いた YAML のテストは0件 |
| 3-4 | `:176` | 変換元が YAML 形式のとき `excludeSheets` を指定しても、変換件数と出力内容が指定しないときと一致する（エラーにもならない） | `excludeSheet`／`excludeSheets` の呼び出しは `TestDataConverterTest.java:517` と `ConverterMojoTest.java:194` の2箇所だけで、**どちらも `from=xls`** |
| 3-5 | `:233` | 直下に不正な YAML、サブディレクトリにも不正な YAML を置いて `validate` を実行すると、返る `ValidationError` は直下のぶんだけになる。直下に `.yaml` を持たない上位ディレクトリ（配下には不正な YAML がある）を指定すると空リストが返る | `YamlTestDataValidatorTest` で `.yaml` をサブディレクトリに置くテストは0件（`mkdir` の呼び出しは `:737` の1件で、これは `broken.yaml` という名前の**ディレクトリ**を直下に作るもの） |
| 3-6 | `:251`-`:254` | `withTestShotsHeaderColor(x)` を渡すと、識別子 `testShots` の `LIST_MAP` のヘッダ行の背景色が `x` になる | `withTestShotsHeaderColor` の出現0件 |
| 3-7 | `:259`-`:262` | `withExpectedHeaderColor(x)` を渡すと、`EXPECTED_` で始まるブロックと `RESPONSE_` で始まるブロックのヘッダ行の背景色が**どちらも** `x` になる | `withExpectedHeaderColor` の出現0件 |
| 3-8 | `:263`-`:266` | `withOtherHeaderColor(x)` を渡すと、`MESSAGE` と識別子が `testShots` 以外の `LIST_MAP` のヘッダ行の背景色が `x` になり、`testShots` の `LIST_MAP` は変わらない | `withOtherHeaderColor` の出現0件 |
| 3-9 | `:275`-`:278` | `withMaxColumnWidthChars(n)` が効く。**上限文字数が実際に列幅を打ち切ること**（既定20に対し30文字の値を持つ列が20文字相当で頭打ちになること）も押さえる | `withMaxColumnWidthChars` の出現0件。上限が列幅を打ち切ることを assert したテストも0件（既定値の一致だけを見る `XlsOutputConfigTest.java:25` はある） |
| 3-10 | `:287`-`:290` | `withDisplayGridlines(true)` を渡すと、**出力したシートのグリッド線表示がオンになる**。既定（`false`）ではオフになる | `withDisplayGridlines` の出現0件。`setDisplayGridlines` のテスト側出現も0件（`src/main` 側は `XlsFormatWriter.java:131` が呼んでいる）。既存は `XlsOutputConfigTest.java:25` が設定値の一致を見るだけで、**シートへの反映を見ていない** |
| 3-11 | `:239` | `ExcelFormatConfig` を設定した `ConversionRequest` で `to=yaml` の変換を実行しても、出力 YAML の中身が設定なしの場合と一致する | 出力 YAML の中身を2通りの設定で比較したテストは0件（`ConverterMojoTest.java:298`・`:323` は変換が完走することだけを見ている） |

**3-2・3-3・3-4・3-11 は負のテストである**（「無いこと」「変わらないこと」を押さえる）。
**期待値をわざと崩したときに落ちることを、この4件については特に念入りに確認すること。**
「何も起きないこと」を assert するテストは、対象を素通りしていても緑になる。

**既存が押さえていた項目は書き直さない。** 解説書の81項目のうち、上の11件を除く残りは
既存605メソッドが押さえていることをディレクターが実測で確認した。

---

## 4. 完了条件

1. **第2節の4件（2-1〜2-4）がすべて是正されている。** 是正ごとに、直す前は落ちて直したあとは通るテストがあること
2. **2-1・2-3 の「着手前に検証すること」の結果が、実装に入る前に報告されている**
3. **完了条件の母集合が往復で保たれることを、テストで押さえている。**
   `notation.rst` の特殊記法の表（Excel 形式13行・YAML 形式13行）と `testdata_examples.rst` の
   「null・空文字・改行など特殊な値を記述する」の各記載例について、
   **XLS→XLS・XLS→YAML→XLS・YAML→YAML・YAML→XLS→YAML の4経路**で、
   テスティングフレームワークが解釈したあとの値が往復前と一致すること。
   **一致しないものは `@Ignore` ＋ 印つきの理由で記録する**
4. **第3節の11件について、テストが存在する。** 落ちたものは `@Ignore` ＋ 印つきの理由で記録されている
5. **足したテスト・直したテストそれぞれについて、期待値をわざと崩すと落ちることを1度確認している。**
   確認したことを報告に書く。「テストが通る」だけでは、そのテストが何かを押さえた証拠にならない
6. **既存テストの期待値を変えた箇所が全件挙がっている。** 2-1・2-3 は既存テストの期待値に触れる。
   どれを変えどれを変えなかったかを、件数を数えたうえで報告する
7. **カバレッジ C0/C1 を計測し、結果を報告する。** `src/main` の是正で下がった箇所があれば挙げる
8. **`mvn clean test` が緑であること。** `target/classes` が jacoco 計装済みのまま残っていると
   `mvn test` は `Cannot process instrumented class` で失敗する（2026-08-26 実測）。`clean` を付ける
9. `git status --short` が空。一時ファイル・作業用スクリプト・ログを残さない
   （`jacoco.exec` と `target/` は `.gitignore:1`・`:3` に入っているので消さなくてよい）
10. 変更を push する

---

## 5. やらないこと

- **解説書を直さない。** 「解説書が誤っている」と判断した項目は、根拠（`file:line` と参照コミット）を
  添えて報告して止める
- **`nablarch-testing` を直さない。** リリース済みであり `src/main` は変更禁止
- **`nablarch-testing-yaml` を直さない。** 同モジュールには別の指示書が出ている
- **解説書に無い書き方を追いかけない。** 誤った書き方は無限にあり、追い始めると完了条件が動く
- **形式間の対応表を作らない。** 合わせる先は各形式と解説書であって、形式どうしではない
- **`YamlTestCoreAdapterTest.java:365`-`:370` の扱いは、渡す前にディレクターが確定する。**
  `nablarch-testing-yaml` 側の是正（`isResourceExisting` の判定単位を入れ物に揃える）が入ると
  このテストは落ちる（2026-08-26 実測。`isResourceExisting_reflectsFileExistence:370`）。
  **yaml の是正が入った版で渡すので、期待値を新しい仕様に合わせて直すことになる。**
  渡す時点でこの行が書き換わっていなければ、指示書が更新されていない。着手せず報告すること

---

## 6. 報告

次の6つを、この順で1つのファイルにまとめる。

1. **2-1・2-3 の「着手前に検証すること」の結果**（実装前に一度報告する）
2. **第2節4件の是正結果。** 是正ごとに、変更したファイルと `file:line`、直す前に落ちたテストの名前
3. **完了条件3（母集合の4経路）の結果。** 表の行ごと・記載例ごとに、4経路それぞれの合否
4. **第3節11件の結果。** 通ったもの・`@Ignore` にしたものの内訳。`@Ignore` は理由の文言をそのまま載せる
5. **期待値をわざと崩す確認の結果。** 対象テスト名と、崩した内容
6. **既存テストの期待値を変えた箇所の全件**と、**カバレッジ C0/C1 の計測結果**

---

## 7. レビュー

**4観点レビューは回さない。** 作業が15件に確定していて探索を含まないこと、成果物が確定済みの
作業だけになることによる。ディレクターが担当範囲を全量読み直して独立に検証する。

観点D（検証の妥当性）は、次の2つで代替する。

1. 完了条件5「期待値をわざと崩すと落ちること」
2. **完了条件3の測り方そのもの。** 既存の `RoundTripTest` は中間モデルを起点にするため、
   記法⇄値の写像が非対称でも書きと読みが同じ非対称なら緑になる。実際、第2節の4つの症状は
   いずれも同テストが緑のまま起きていた。完了条件3は実ファイルを起点にし、
   テスティングフレームワークが解釈したあとの値で比べるので、この盲点をふさぐ
