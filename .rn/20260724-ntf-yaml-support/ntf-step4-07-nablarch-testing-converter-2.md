# Step 4 指示書（第2回）— nablarch-testing-converter

宛先: `nablarch-testing-converter` モジュール担当CC

**第1回（`ntf-step4-05-nablarch-testing-converter.md`、`#33`〜`#39` 完了・ディレクター検証済み・合格）の後に、
解説書側で形式間の意味集合を揃える是正が入り（`nablarch-document` の `6bfc058`・`04b9405`・`6ba3c83`。台帳 `#42`）、
あわせてディレクターの調査で converter の Excel 読みが本体と値処理の順序が逆であることが分かった。** 本指示書はその追随と是正である。

---

## 渡す前にやること（ディレクター向け。CC には渡さない）

**完了（2026-08-29。ディレクター実測）。** 本指示書は `nablarch-testing-yaml` の第2回（`ntf-step4-06-nablarch-testing-yaml-2.md`）の完了に依存する。

| # | やること | 結果 |
|---|---|---|
| 1 | yaml 第2回の完了報告をディレクターが独立に検証する（`mvn -o clean test`・本体 oracle テストの中身・ミューテーション） | 済（yaml `#45`＝`3fecc4e` まで合格。yaml 指示書 §9） |
| 2 | yaml のピンを取り直し、本指示書の参照点の表と 2-4 を更新する（`3ee39c9` → 新しい先端） | 済（`3fecc4e`。解説書も `afa4f9e` → `a6da1f6`） |
| 3 | yaml を `mvn install` する（`JAVA_HOME=/usr/lib/jvm/temurin-17-jdk-amd64`） | 済（`3fecc4e` を install。生成物は親 POM `nablarch-parent:6-NEXT-SNAPSHOT` の `maven.compiler.target=17` で major 61＝Java 17。`~/.m2/.../nablarch-testing-yaml-1.0.0-SNAPSHOT.jar` 2026-08-29 14:28） |
| 4 | その状態で converter `d611bec` の `mvn -o clean test` を実測し、赤の全件を 2-4 の表に書く（第1回の着手時と同じ形） | 済（`656 / F3 E1`。2-4 に全件） |
| 5 | 「渡すときの文面」の着手時の実測値を 4 の結果に差し替える | 済。あわせて「ソースから解説書参照を全撤去」を 2-6 として追加（user 判断 2026-08-29） |

---

## 0. 渡すときの文面

**担当CCには次をそのまま貼る。**（着手時の実測値は「渡す前にやること」4 の結果で差し替える）

```
Step 4 の第2回の作業を依頼します。指示書に是正6件が確定済みで載っています。
探索は不要です。解説書を読み比べて不一致を探す作業ではありません。

着手前に、いまの状態を1度実測してください。mvn -o clean test は
Tests run: 656, Failures: 3, Errors: 1, Skipped: 0 になります（こちらでも実測済み）。
この赤4件は依存先 nablarch-testing-yaml の第2回の是正に converter のテストが追随していないもので、
指示書 2-4 に全件載せてあり、2-4 で直す対象です。それ以外の赤が出たら、着手せず報告してください。

作業場:
  /home/tie303177/work/nablarch/nablarch-testing-converter
  ブランチ ntf-test-data-converter（d611bec）

指示書:
  /home/tie303177/work/nablarch/nablarch-document/.rn/20260724-ntf-yaml-support/ntf-step4-07-nablarch-testing-converter-2.md
  nablarch-document の origin/ntf-yaml-support に入っています。
  作業ツリーが古い場合は
  git show origin/ntf-yaml-support:.rn/20260724-ntf-yaml-support/ntf-step4-07-nablarch-testing-converter-2.md
  で読んでください。

解説書は a6da1f6 を参照点にしてください。
必ず git show a6da1f6:<path> で読み、作業ツリーの HEAD を読まないでください。

依存先 nablarch-testing-yaml は 3fecc4e を参照点にしてください（第2回 #36〜#45 の是正が入った版で、
~/.m2 にも install 済みです）。変更しないでください。

指示書の「1. やること」「2. 是正」「3. テストの作り方」「4. 完了条件」「6. 報告」に
従ってください。特に次の6つを落とさないでください。

- 2-1・2-3 には「着手前に特定すること」があります。実装に入る前に、その結果だけを先に報告してください。
  2-1 は波及先が広いので、表が揃うまで実装に入らないでください
- 第2節の6件は直してください。ここは判断済みです。範囲の判断を持たないでください
- 2-5 の4経路テストは、正解を本体 nablarch-testing にしてください。converter 自身の reader を正解にした
  第1回のテストは、末尾の null が Excel と YAML で違う値になっていても80経路すべて緑でした
- 足したテスト・直したテストそれぞれについて、期待値をわざと崩すと落ちることを1度確認し、
  確認したことを報告に書く
- 解説書は直さないでください。「解説書が誤っている」と判断した項目は、根拠を添えて
  報告して止めてください
- ソース（src/main・src/test・フィクスチャ）に解説書への参照を書かないでください。.rst のパス・
  行番号・節見出し・逐語引用・「解説書」「出典」のいずれも不可です。既存のものは 2-6 で全部取り除きます。
  2-6 は単独のコミットにしてください

ビルドの注意: target/classes が jacoco 計装済みのまま残っていることがあり、その状態の
mvn test は「Cannot process instrumented class」で失敗します。mvn clean test を使ってください。
mvn install を実行する場合は JAVA_HOME を設定してください（Nablarch 6 の基準は Java SE 17）。
  JAVA_HOME=/usr/lib/jvm/temurin-17-jdk-amd64

後始末: git status --short が空になること。一時ファイル・作業用スクリプト・ログを
残さないでください（jacoco.exec と target/ は .gitignore に入っているので消さなくてよい）。
```

---

## 1. やること

**解説書に書いてあることを、実装とテストで押さえる。** 読み比べて不一致を洗い出す作業ではない。

**本モジュールは `src/main` を変更してよい**（タグ0件・未リリース）。**依存先の `nablarch-testing`・`nablarch-testing-yaml` は変更しない。**

### 参照点（ピン）

| 対象 | ピン | 読み方 |
|---|---|---|
| 解説書 `nablarch-document` | **`a6da1f6`**（ブランチ `ntf-yaml-support`） | `git show a6da1f6:<path>` |
| 本モジュール | **`d611bec`**（ブランチ `ntf-test-data-converter`。`@Test` 656件・`@Ignore` 0件） | 作業ツリーで作業してよい |
| `nablarch-testing` | `3c4bd2a` | `git show 3c4bd2a:<path>`。**変更しない** |
| `nablarch-testing-yaml` | **`3fecc4e`**（ブランチ `feature/ntf-yaml`。第2回 `#36`〜`#45` の是正が入った版） | `git show 3fecc4e:<path>`。**変更しない**。`~/.m2` にはこの版が install 済み |

**解説書は必ずピンで読む。** 作業ツリーの HEAD はピンとは別物である。

### 判断の軸（2026-08-28 ユーザー確定。すべての是正はこれで決まっている）

**中間モデル＝NTF 仕様＝現行 Excel 実装が定める意味**（`tools/testdata_converter.rst:14`「テスティングフレームワークの仕様上の意味だけを持つ中間モデル」、
`:22`「意味を変えずに往復できる」）。**converter の Excel 読みは、本体が読むのと同じ意味を中間モデルに入れる。** 自分で解釈しない。

### 落ちたときの扱い

- **第2節の6件は直す。** 解説書が正であり、実装が追いついていない
- **既存テストが落ちたら、期待値を解説書に合わせて直す。** 「変えた／変えなかった」を件数つきで報告する（完了条件5）

---

## 2. 是正（6件）

### 2-1. Excel 読みの値処理が本体と順序が逆で、末尾の `null` が `""` にならない

**解説書**（`a6da1f6`）: `implementation/testdata_notation.rst:889`「末尾のフィールドに ``null``\ と記述した場合は、形式によらず\ ``""``\ になる」、
`:1155`（電文も同じ）。`tools/testdata_converter.rst:14`（中間モデルは仕様上の意味だけを持つ）。

**本体の仕組み**（`nablarch-testing@3c4bd2a`。変更しない）: `TestDataParsingTemplate.java:183` で全セルを**先に解釈**（インタープリタ列）し、
そのあと構造解析する。ファイル・電文の値行は `DataFileParser.java:68` が `NablarchTestUtils.trimTailCopy`
（`src/main/java/nablarch/test/NablarchTestUtils.java:273`。末尾から `null`・空文字を連続して取り除く）を掛け、
`DataFileFragment.addValue`（`DataFileFragment.java:102`-`:115`）が名前の数まで `""` で埋める。
解釈後の Java null は「空」なので末尾から落ちて `""` になる。

**現行**（`d611bec`）: `TestCoreReaderAdapter.java:40` の `EMPTY_INTERPRETERS` で本体パーサを回す
（`:86` `TableDataParser`・`:101` `ListMapParser`・`:151`/`:155` `FixedLengthFileParser`/`VariableLengthFileParser`・`:183` `MessageParser`・
`:333`-`:334` `SendSyncBodyCollector`/`SendSyncMessageParser`・`:374` `HeaderCollector`・`:461` `BodyLineCollector`）。
構造解析が先に走り、**そのあと** `XlsFormatReader` が自分で解釈する（`readDataRows:420`-`:434` の `:429` `interpretValue`、
`readTableBlocks:150`-`:168` の `:167` `interpretRows`、`readListMapBlock:180`-`:198` の `:197`。実体は `interpretValue:570`・`interpretRows:678`）。
生セル `null` は空でないため `trimTail` に落ちず、解釈後に Java null として末尾に残る。

**実測**（ディレクター。`~/work/cowork/nablarch/ntf-doc-renewal/probe/Probe.java`。本体と converter に同じ `.xlsx` を読ませた）:

| 入力（データ行のセル） | 本体（NTF 意味） | converter `d611bec` |
|---|---|---|
| F1 `x`,`null`,`null` | `x`,`""`,`""` | **`x`,null,null** |
| F2 `x`,`null`,`y` | `x`,null,`y` | 同 |
| F3 `""`,空,空 | `""`,`""`,`""` | 同 |
| F4 `null`,`null`,`null` | `""`,`""`,`""` | **null,null,null** |
| F5 `x` のみ | `x`,`""`,`""` | 同 |
| F6 `x`,`""`,`null`／F7 `x`,空,`null` | `x`,`""`,`""` | **`x`,`""`,null** |
| M1 電文 `1`,`x`,`null`,`null` | `x`,`""`,`""` | **`x`,null,null** |
| S2 送信同期 `2`,`x`,`null`,`null` | `x`,`""`,`""` | **`x`,null,null** |

仕様内の入力で意味が変わるのは末尾に連続する `null` だけである（他の順序依存は仕様外の入力に対する差で、
`~/work/cowork/nablarch/ntf-doc-renewal/01-現在地.md`「A・B の調査結果」(2) の表）。

**やること**（2026-08-28 ユーザー了解の方針）: **converter が自分で解釈するのをやめ、本体パーサにインタープリタ列を渡して本体に解釈させる。値は器から取る。**

1. `TestCoreReaderAdapter` の本体パーサ（`TableDataParser`・`ListMapParser`・`FixedLengthFileParser`・`VariableLengthFileParser`・`MessageParser`・
   `SendSyncMessageParser`）に、本体 `src/test/resources/unit-test.xml:29`-`:40` と同じ順の `NullInterpreter` → `QuotationTrimmer` → `LineSeparatorInterpreter` を渡す
   （`XlsFormatReader.java:530`・`:533`・`:536` の3インスタンスを移す）。**`DateTimeInterpreter`・`${...}` 系は渡さない**（`tools/testdata_converter.rst:61`。記法のまま運ぶ）
2. **`HeaderCollector`（`:374`）・`BodyLineCollector`（`:461`）は空のまま。** 生行は型行・長さ行・名前行の原文復元にだけ使い、**データ行の値には使わない**
3. データ行の値は器から取る。ファイル・電文は `FragmentView.getValues`（`src/main/java/nablarch/test/core/file/FragmentView.java:60`。
   `trimTail`・`addValue` を通ったあとの値）、テーブルは `TableData.getValue`、`LIST_MAP` は `readListMap` の結果。
   `readDataRows:429` の `interpretValue` と `readTableBlocks:167`・`readListMapBlock:197` の `interpretRows` を消す
4. 書き（`XlsFormatWriter.toCellNotation:685`）は変えない。解釈後の値から記法へ戻す逆写像は第1回で確定している

**着手前に特定すること**（`nablarch/CLAUDE.md` 2-2。**表が揃うまで実装に入らない**）。本体が全セルを解釈するようになると、
データ行以外の値も解釈後になる。次の (a)〜(e) それぞれについて「何が変わるか／どう対処するか」を1行ずつ表にして報告する。

- (a) **ディレクティブ値**。`normalizeDirectiveValue:486`-`:500` が `QuotationTrimmer` 相当を自前で掛けている（二重適用になる）。
  `record-separator`・`field-separator` の値に `LineSeparatorInterpreter` が掛かる。書き戻し（`XlsFormatWriter.java:469`）は記法へ戻すか
- (b) **FW 制御ヘッダ値**。`readMessageBlock:246`-`:248` は「本体が生文字列として返すため `stripQuotes` は適用しない」と書いている。解釈後になったときの読みと書き戻し
- (c) **空エントリ判定**。`dropEmptyEntries:622`・`isEmptyEntry:639`・`isEmptyCell:668` は生セルで判定している。本体は `PoiXlsReader.java:93` で
  `isBlankLine`（`:140`-`:147`。生セルの `isEmpty()`）により**全セルが空の行を先に落とす**ので、converter 側の判定が要るのはマーカーカラムだけに値がある行だけになる。2-2 と合わせて決める
- (d) **生行と器の行数の対応**。`requireLine:448` が生行を器の断片構造で数えている。値を器から取ったあとも型行・長さ行・名前行の位置決めに生行を使うため、対応が崩れないか
- (e) **既存テストで生値（解釈前）を期待しているもの**の全件。`TestCoreReaderAdapterTest`・`XlsFormatReaderTest`・`XlsFormatReaderCellTypeTest`・
  `XlsFormatReaderRealFileTest`・`XlsNotationSymmetryTest`・`XlsEmptyEntryTest`・`RoundTripTest` を全走査し、変える／変えないを件数つきで

### 2-2. マーカーカラムだけに値があるエントリが消える

**解説書**（`a6da1f6` の `tools/testdata_converter.rst:63`。**`6bfc058`・`a6da1f6` で改訂済み**）:

> マーカーカラムだけに値があるエントリは、テスティングフレームワークが読み飛ばさない（\ :ref:`コメント・マーカーカラム・空エントリを扱う <testdata_notation-comment_and_marker>`\ 参照）ため、本ツールもマーカーカラムの値だけを除いたエントリとして中間モデルに残す。消えるのはマーカーカラムの値だけである。

`implementation/testdata_notation.rst:1502`「この判定はマーカーカラムを除外する前に行われる。そのため、マーカーカラムだけに値があるエントリは読み飛ばされない。他のカラムの値は通常どおり読み込まれる（Excel 形式の空セルは ``""``、YAML 形式でキーを省略した場合は前述のとおり null）」（`#43` で改訂。上の `:63` も同時に改訂した）。

**現行**（`d611bec`）: `readTableBlocks:167`・`readListMapBlock:197` の `dropEmptyEntries` が、本体からマーカーカラム除外後の行を受け取ってから空判定するため、
マーカーカラムだけに値がある行が落ちる。**実測**（2026-08-27。`SETUP_TABLE=T`／カラム行 `[no]`,`id`,`name`／データ行 `1,U0001,yamada`・`(空),"",""`・`3,(空),(空)`）:
本体 `PoiXlsReader#readLine` は3件、converter は `#33` 後も2件（3件目が消える）。

**やること**: マーカーカラムだけに値があるエントリを、全カラムが `""` のエントリとして中間モデルに残す。本体が全セル空の行を先に落とす（2-1 (c)）ので、
`dropEmptyEntries` を消してよいかを 2-1 (c) の表で決める。**Excel 形式へ書くときは第1回 2-2 の `entryCells:627`（全要素が空文字のエントリは各セルへ `""`）がそのまま効く。**
YAML へ書くときは全値 `""` のエントリになり、yaml 第2回 2-4 の是正後は読み戻しても消えない。

### 2-3. 交互記述のシートを変換しても警告が出ない

**解説書**（`a6da1f6` の `tools/testdata_converter.rst:69`。**`6ba3c83` で「警告して変換」に確定**）:

> 収集方式が「グループ」のデータタイプ（テーブル・ファイル・グループID付きの電文）について、同じデータタイプと同じグループIDのデータブロックの間に別のデータブロックを挟んだシートでは、テスティングフレームワークは\ Excel\ 形式では収集を途中で終え、後ろのデータブロックを読まない（\ :ref:`グループIDによる使い分け <testdata_notation-group_id>`\ 参照）。\ YAML\ 形式にはこれに相当する記法が無く、そのまま変換すると読まれなかったデータブロックが有効になって意味が変わる。本ツールはこのシートを検出すると、テスティングフレームワークが読まなかったデータブロックを出力せずに変換を続け、警告を出す。変換後の\ YAML\ 形式でテスティングフレームワークが読む内容は、\ Excel\ 形式で読んでいた内容と同じである。

`implementation/testdata_notation.rst:281`（データタイプが交互）・`:305`（グループIDが交互）が Excel の挙動、`:339` が YAML では起きないことを述べる。

**本体の仕組み**（`3c4bd2a`）: `TestDataParsingTemplate.doParse:284`-`:310`。対象ブロックを読み始めたあと（`nowReading`）、
別のデータタイプのマーカー行に当たると `:303`-`:307` で `break` する。`GroupDataParsingTemplate.java:36`-`:43` の `isTargetType` は
`データタイプ名 + [グループID] + '='` の前方一致、`:51`-`:53` の `shouldStopOnNextOne` は偽（同じキーのブロックは続けて集める）。

**現行**（`d611bec`）: `XlsFormatReader.read:106`-`:137` は `readHeaders`（`TestCoreReaderAdapter.java:244`-`:248`。全マーカー行を記述順に返す）で
(データタイプ, グループID) ごとに1回だけ本体パーサを呼ぶ。本体が途中で `break` するため、**読まれなかったブロックは既に出力されない見込み**だが、
**警告は出ない**（`LOGGER`（`:77`）に警告を出しているのは `deduplicateColumnNames:702` の `:716` だけ）。

**やること**:

1. **先に落ちるテストを書く。** 交互記述のシート（例: `SETUP_TABLE=A`／`SETUP_TABLE[g1]=B`／`SETUP_TABLE=C` の順。または `EXPECTED_TABLE`／`EXPECTED_COMPLETE_TABLE`／`EXPECTED_TABLE`）を
   実 `.xlsx` で組み、(i) 警告が1件出ること（ブック名・シート名・データタイプ・グループID・読まれなかったブロックの識別子を含む）、
   (ii) 出力に読まれなかったブロックが無いこと、(iii) 出力を本体が読んだ結果が、元の `.xlsx` を本体が読んだ結果と一致すること、を assert する。
   警告の捕捉は `XlsFormatReaderTest.java:861`-`:895` の `CapturingHandler` の形でよい。**このテストが (i) で落ちることを確認してから**実装に入る
2. `readHeaders` の並びから、グループ収集のデータタイプについて同じ (データタイプ, グループID) が別のキーを挟んで再び現れることを検出し、`LOGGER.warning` で出す。
   出力から外すのは本体の `break` に任せる（converter が自前で選別しない）
3. **`LIST_MAP`・`MESSAGE`（識別子で1件を引くデータタイプ）は対象外**（解説書 `:69` は「収集方式が「グループ」のデータタイプ」に限っている）

**着手前に特定すること**: 交互記述のシートを converter で読んだとき、(ii) が現状で成り立つか（本体の `break` がそのまま効いているか）を実測して報告する。
成り立たなければ、その理由（どこで後ろのブロックが拾われるか）を `file:line` で示す。

### 2-4. `nablarch-testing-yaml` 第2回の是正への追随

**依存先の第2回**（`ntf-step4-06-nablarch-testing-yaml-2.md`）で、YAML の読みが次のように変わる。converter の YAML 読み（`YamlFormatReader` → `YamlTestCoreAdapter` → yaml のビルダ）は
yaml のビルダ経由なので**実装は自動で追随する**。追随を**テストで押さえ**、落ちる既存テストの期待値を解説書に合わせる。

| yaml 第2回 | 解説書 | converter で押さえること |
|---|---|---|
| 2-1 末尾 null → `""` | `notation.rst:889`・`:1155` | ファイル・電文の末尾 `null` を YAML から読むと `""`（2-5 の母集合に入れる） |
| 2-2 電文 `records:` は1つ | `notation.rst:1153`・`:1299` | 2つ以上の YAML を読むと yaml のスキーマ検証で落ちる（`YamlSchemaValidationException`）。Excel へは書けない形なので converter 側の検査は不要 |
| 2-3 `fw_header:` のキー | `notation.rst:1295` | `reader.fwHeaderfields` に無いキーの YAML を読むとエラー |
| 2-4 空エントリは `{}` だけ | `notation.rst:1502` | 全値 `""` のエントリが残る。**`YamlFormatReaderScalarTest#skipsRowWhoseValuesAreAllEmpty`（`d611bec`）は全値 `""` の行が読み飛ばされることを期待しているため落ちる** → 解説書どおりに直す |
| 2-5 2文字 `\` ＋ `r` はエラー | `notation.rst:1445` | 2文字の `\` ＋ `r` を含む YAML を読むとエラー。第1回 §1-1 で「YAML→XLS→読み戻しで CR に変わる（追わない）」とした観測は、この是正で入力自体が弾かれるため消える |

**着手時に赤いテストの全件**（ディレクター実測 2026-08-29。yaml `3fecc4e` を install した状態で converter `d611bec` の `mvn -o clean test`）:

```
Tests run: 656, Failures: 3, Errors: 1, Skipped: 0
  YamlFormatReaderInvalidInputTest.fillsMissingRecordFragmentValuesWithEmptyStringInsteadOfNull:763 → yaml 2-1（末尾 null → ""）。期待 [a, null, ""] に対し実際 [a, "", ""]
  YamlFormatReaderScalarTest.readsUnquotedNullAsJavaNullInRecordFragmentPath:650                    → yaml 2-1（末尾 null → ""）。期待 null に対し実際 ""
  YamlFormatReaderScalarTest.skipsRowWhoseValuesAreAllEmpty:596                                     → yaml 2-4（空エントリは {} だけ）。全値 "" の行が残る
  YamlFormatReaderRealFileTest.keepsFwHeaderNamedRecordInSendSyncFromRealYaml:640                   → yaml 2-2（電文 records: は1つ）。YamlSchemaValidationException「$.response_body_messages[0].records: アイテムは最大でも 1 個必要ですが、2 が見つかりました」
```

4件とも「converter 側のテストが yaml 第2回より前の挙動を期待値に書いている」もので、`src/main` の欠陥ではない。4件とも 2-4 で解説書どおりに直す。

### 2-5. 4経路テストの正解が converter 自身の reader になっている

**第1回の完了条件3**（`SpecialNotationRoundTripTest`。20件×4経路）は起点が実ファイルで比較が解釈後の値だが、**正解値が本体ではなく converter 自身の reader**
（`readXls:154`・`readYaml:164`。`assertFourRoutes:203`・`assertExampleFourRoutes:538`）である。「Excel 記法の解釈後の値＝YAML 記法の解釈後の値」を
converter の2つの reader の間で比べているため、2-1 の末尾 `null` のように**両 reader が同じ誤りを持つ欠陥は検知できない**（実際、80経路すべて緑のまま起きていた）。

**やること**:

1. **正解を本体にする。** 各経路で生成した `.xlsx` を本体（`PoiXlsReader` ＋ 本体 `unit-test.xml:29`-`:40` と同じ順のインタープリタ3本）で読んだ値、
   生成した `.yaml` を `nablarch-testing-yaml` の `YamlTestDataParser` で読んだ値を、起点の `.xlsx`／`.yaml` を同じ読み手で読んだ値と比べる。
   本体の呼び方は `~/work/cowork/nablarch/ntf-doc-renewal/probe/Probe.java:26`-`:39`（`nablarch.test.core.reader` パッケージのパッケージ private な
   `parse(dir, resource, id, false)` を使う。`TestCoreReaderAdapter` と同じパッケージなので converter のテストからも呼べる）。
   ファイル・電文は `DataFile#toDataRecords()`（`DataFile.java:155`）の値で比べてもよい
2. **母集合に足す**（第1回の20件は残す）:
   - ファイル・電文の末尾 `null`（2-1 の実測表 F1・F4・F6・M1・S2。**このうち1つ以上は着手前に落ちることを確認する**）
   - 全値 `""` のテーブル・`LIST_MAP` エントリ（第1回はガード列 `K` を置いていたため母集合に無い）
   - マーカーカラムだけに値があるエントリ（2-2）
   - `implementation/testdata_examples.rst:2423`-`:2461`「アップロードファイルを指定する」（`LIST_MAP`＋`[no]`＋`${attach:...}`）。第1回は母集合の節（`:2133`-`:2461`）に含まれていたが外していた
3. 交互記述（2-3）は4経路ではなく 2-3 のテストで押さえる（YAML には表せない）

---

### 2-6. ソースから解説書への参照をすべて取り除く

**user 判断（2026-08-29）: モジュールのソースコメントから解説書への参照をすべて取り除く。** リリース済みの `nablarch-testing`・`nablarch-testing-rest`・`nablarch-testing-junit5` の `src/` には
解説書への参照が1件も無い（ディレクター実測）。根拠の追跡は `.rn/` の報告書・台帳で行う。yaml は `#45`（`3fecc4e`）で同じ作業を済ませている。

**現行**（`d611bec`。ディレクター実測 `git grep -nE '\.rst|nablarch-document|解説書|出典|根拠:' -- src/`）: **167行・43ファイル**
（`src/main` 71行・19ファイル、`src/test` 96行・24ファイル）。パターン別（重複あり）は `.rst` 152行・41ファイル／`nablarch-document` 2行／「解説書」20行／「出典」1行／「根拠:」0行。
`.java` 以外（フィクスチャ・リソース）には無い。

**やること**:

1. **着手前に、取り除く行の全件（`file:line`）を上の式で機械抽出し、件数を報告してから始める**
2. `src/main`・`src/test` から、`.rst` のパス（行番号の有無を問わない）、`nablarch-document`、「解説書」「出典」として解説書を指す記述、解説書の節見出し・逐語引用をすべて取り除く。
   Javadoc・テストの説明は、**何を確かめるかを自分の言葉で書く**（既存の Given/When/Then と本体クラス名への言及は残してよい）
3. 他リポジトリのソースを `path:line` で指す箇所（`git grep -nE '\.\./nablarch-|[A-Za-z]+\.java:[0-9]+' -- src` で **11行**: `GroupIdNotation.java:16`・`YamlTestCoreAdapter.java:101`・
   `ConverterFileFilter.java:159`・`XlsFormatReader.java:655`-`:656`・`XlsFormatWriter.java:701`・`YamlTestCoreAdapterTest.java:371`・`ConverterFileFilterTest.java:145`・
   `XlsEmptyEntryTest.java:44`-`:45`・`YamlFormatReaderInvalidInputTest.java:1284`）は、行番号とパスを落としてクラス名だけ残す（例: `PoiXlsReader.java:93` → `PoiXlsReader`）。
   `nablarch-testing@3c4bd2a` のようなコミット指定も落とす
4. **テストの動作・期待値は変えない**（変えるのはコメント・Javadoc・assert メッセージの文字列だけ）。**2-6 は単独のコミットにする**
   （コメントと文字列だけの変更であることを、ディレクターがコメント行を落とした差分で機械的に確かめるため）
5. 終わったら `git grep -nE '\.rst|nablarch-document|解説書|出典|根拠:' -- src/` と `git grep -nE '[A-Za-z]+\.java:[0-9]+' -- src` がともに **0件**であることを報告に書く

---

## 3. テストの作り方

**Excel に同じ意味がある項目（2-1・2-2・2-5）は、本体 `nablarch-testing` を正解にする。** converter 自身の reader どうし、
または自分で書いた期待値との比較だけでは、規則の写し間違いを検知できない（2-5 の経緯）。

**エラー・警告になる項目（2-3・2-4 の一部）は、例外の型・警告の件数と文言を assert する。**

**足したテスト・直したテストそれぞれについて、期待値をわざと崩すと落ちることを1度確認する**（完了条件4）。

---

## 4. 完了条件

1. **第2節の6件がすべて是正されている。** 是正ごとに、直す前は落ちて直したあとは通るテストがあること（2-3 は先に書いた落ちるテスト、2-5 は母集合に足した末尾 `null` の1件以上）
2. **2-1・2-3 の「着手前に特定すること」の結果が、実装に入る前に報告されている**
3. **2-5 の4経路テストが本体を正解にしており、母集合に 2-5 の4種が入っている**
4. **足したテスト・直したテストそれぞれについて、期待値をわざと崩すと落ちることを1度確認している。** 確認したことを報告に書く
5. **既存テストの期待値を変えた箇所が全件挙がっている。** どれを変えどれを変えなかったかを、件数を数えたうえで報告する
6. **`@Ignore` が0件**
7. **カバレッジ C0/C1 を計測し、結果を報告する。** `src/main` の是正で下がった箇所があれば挙げる
8. `mvn -o clean test` が緑。着手時点では4件が赤い（`Tests run: 656, Failures: 3, Errors: 1, Skipped: 0`。2026-08-29 実測。2-4 で解消する）。`clean` を付ける
9. `git status --short` が空。一時ファイル・作業用スクリプト・ログを残さない
10. 変更を push する
11. **`git grep -nE '\.rst|nablarch-document|解説書|出典|根拠:' -- src/` と `git grep -nE '[A-Za-z]+\.java:[0-9]+' -- src` が0件**（2-6）。2-6 が単独のコミットになっている

---

## 5. やらないこと

- **解説書を直さない。** 「解説書が誤っている」と判断した項目は、根拠（`file:line` と参照コミット）を添えて報告して止める
- **`nablarch-testing`・`nablarch-testing-yaml` を直さない**
- **解説書に無い書き方を追いかけない。** `TABLE[]=x`・`SETUP_TABLEX=T`（角括弧の無いグループID）・`TABLE[=x`（閉じていない角括弧）・全角ダブルクォートは解説書に無く、対象外
- **仕様外の入力に対する本体との差（先頭列の `null`・ディレクティブ値の `null`・マーカーを引用符で囲む等）を揃えに行かない。** 2-1 で本体に解釈させれば結果的に揃うものはそれでよいが、揃えるためのコードを足さない
- **converter が自前で「読まれなかったブロック」を選別しない**（2-3）。本体の挙動に任せ、警告だけを足す
- **ソース（`src/main`・`src/test`・フィクスチャ）に解説書への参照を書かない。** `.rst` のパス・行番号・節見出し・逐語引用・「解説書」「出典」のいずれも不可。2-1〜2-5 で足すコメントも同じ

---

## 6. 報告

次の6つを、この順で1つのファイルにまとめる。

1. **2-1・2-3 の「着手前に特定すること」の結果**（実装前に一度報告する）
2. **第2節5件の是正結果。** 是正ごとに、変更したファイルと `file:line`、直す前に落ちたテストの名前
3. **2-5 の結果。** 母集合（第1回の20件＋足した分）ごとに、4経路それぞれの合否。正解が本体であることが分かる形で
4. **期待値をわざと崩す確認の結果。** 対象テスト名と、崩した内容
5. **既存テストの期待値を変えた箇所の全件**
6. **カバレッジ C0/C1 の計測結果**
7. **2-6 の件数と抽出方法**（着手前の全件 `file:line`、作業後の grep が0件であること、2-6 のコミットハッシュ）

---

## 7. レビュー

**4観点レビューは回さない。** 作業が6件に確定していて探索を含まないため。ディレクターが差分を全量読み直して独立に検証する
（第1回と同じく、自分で `mvn -o clean test`・ミューテーション・実ファイル起点のプローブを行う）。

観点D（検証の妥当性）は、次の2つで代替する。

1. 完了条件4「期待値をわざと崩すと落ちること」
2. **2-5 の正解を本体にすること。** converter の読み書きの写像が本体と食い違えば、本体との不一致として落ちる
