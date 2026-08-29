# Step 4 指示書（第2回）— nablarch-testing-yaml

宛先: `nablarch-testing-yaml` モジュール担当CC

**第1回（`ntf-step4-02-nablarch-testing-yaml.md`、`#34` 承認済み）の後に、解説書側で形式間の意味集合を揃える是正が入った**
（`nablarch-document` の `6bfc058`・`04b9405`・`6ba3c83`。台帳 `#42`）。本指示書はその追随である。
**第1回の 2-1（`isBlankRow`）の決定を 2-4 で上書きする。**

---

## 0. 渡すときの文面

**担当CCには次をそのまま貼る。**

```
Step 4 の第2回の作業を依頼します。指示書に是正7件が確定済みで載っています。
探索は不要です。解説書を読み比べて不一致を探す作業ではありません。

解説書側で「Excel 形式と YAML 形式は同じ意味集合を別の記法で表す」という軸に沿った是正が
入ったので（6bfc058・04b9405・6ba3c83）、本モジュールをそれに追随させます。
第1回の 2-1（isBlankRow）の決定は今回の 2-4 で上書きします。

作業場:
  /home/tie303177/work/nablarch/nablarch-testing-yaml
  ブランチ feature/ntf-yaml（3ee39c9）

指示書:
  /home/tie303177/work/nablarch/nablarch-document/.rn/20260724-ntf-yaml-support/ntf-step4-06-nablarch-testing-yaml-2.md
  nablarch-document の origin/ntf-yaml-support に入っています。
  作業ツリーが古い場合は
  git show origin/ntf-yaml-support:.rn/20260724-ntf-yaml-support/ntf-step4-06-nablarch-testing-yaml-2.md
  で読んでください。

解説書は afa4f9e を参照点にしてください（ja/ 配下は 05e57a1 と同一です）。
必ず git show afa4f9e:<path> で読み、作業ツリーの HEAD を読まないでください。

指示書の「1. やること」「2. 是正」「3. テストの作り方」「4. 完了条件」「6. 報告」に
従ってください。特に次の5つを落とさないでください。

- 2-1・2-2・2-3・2-4・2-5 には「着手前に特定すること」があります。実装に入る前に、その結果だけを
  先に報告してください
- 第2節の7件は直してください。ここは判断済みです。範囲の判断を持たないでください
- Excel 形式に同じ意味がある項目（2-1・2-4）は、本体 nablarch-testing を正解（oracle）にした
  テストを書いてください。YAML 側の実装の結果どうしを比べるテストでは、規則の写し間違いを検知できません
- 足したテスト・直したテストそれぞれについて、期待値をわざと崩すと落ちることを1度確認し、
  確認したことを報告に書く
- nablarch-testing-converter のテストが落ちるのは想定内です。converter は直さず、落ちたテストと
  理由を報告してください

ビルド: mvn install を実行する場合は JAVA_HOME を設定してください。未設定だと javadoc プラグインが
「Unable to find javadoc command」で落ちます（実測）。
  JAVA_HOME=/usr/lib/jvm/temurin-21-jdk-amd64

後始末: git status --short が空になること。tmp/ はテストスイート自身が作る空ディレクトリなので
そのままでよい。一時ファイル・作業用スクリプト・ログを残さないでください。
```

---

## 1. やること

**解説書に書いてあることを、実装とテストで押さえる。** 読み比べて不一致を洗い出す作業ではない。

**本モジュールは `src/main` を変更してよい**（タグ0件・未リリース）。**依存先の `nablarch-testing` は変更しない。**

### 参照点（ピン）

| 対象 | ピン | 読み方 |
|---|---|---|
| 解説書 `nablarch-document` | **`afa4f9e`**（ブランチ `ntf-yaml-support`。`ja/` は `05e57a1` と同一） | `git show afa4f9e:<path>` |
| 本モジュール | **`3ee39c9`**（ブランチ `feature/ntf-yaml`。`@Test` 268件・`@Ignore` 1件） | 作業ツリーで作業してよい |
| `nablarch-testing` | `3c4bd2a` | `git show 3c4bd2a:<path>`。**変更しない** |
| `nablarch-testing-converter` | `d611bec` | `git show d611bec:<path>`。**変更しない**。落ちるテストは報告するだけ |

**解説書は必ずピンで読む。** 作業ツリーの HEAD はピンとは別物である。

### 判断の軸（2026-08-28 ユーザー確定。すべての是正はこれで決まっている）

**中間モデル＝NTF 仕様＝現行 Excel 実装が定める意味。「YAML で表せて Excel で表せない意味」は存在しない。**
YAML の記法がこの意味集合からはみ出す場合、**対応する意味があれば写す（末尾 `null` → `""`）、無ければ弾く（エラー）**。
静的に決まるものはスキーマで、設定に依存するもの（`fw_header:` のキー）は実装で検査する。

### 落ちたときの扱い

- **第2節の7件は直す。** 解説書が正であり、実装が追いついていない
- **既存テストが落ちたら、期待値を解説書に合わせて直す。** 「変えた／変えなかった」を件数つきで報告する（完了条件4）

---

## 2. 是正（7件）

### 2-1. ファイル・電文の末尾フィールドの `null` が `null` のまま残る

**解説書**（`afa4f9e` の `implementation/testdata_notation.rst`）:

- `:889`（ファイルデータの `important`）: 「末尾のフィールドに ``null``\ と記述した場合は、形式によらず\ ``""``\ になる。後ろに値のあるフィールドがあれば\ null\ のまま保持される」
- `:1155`（電文）: 「末尾のフィールドの値を書かなければ、そのフィールドは\ ``""``\ として扱われる（末尾に ``null``\ と記述した場合の扱いも、ファイルデータと同じである）」

**Excel の仕組み**（`nablarch-testing@3c4bd2a`。変更しない）: `DataFileParser.java:68` が値行に
`NablarchTestUtils.trimTailCopy`（`src/main/java/nablarch/test/NablarchTestUtils.java:273`。末尾から `null`・空文字を**連続して**取り除く。
実体は同 `:251`-`:263` の `trimTail`）を掛けてから `DataFileFragment.addValue`（`DataFileFragment.java:102`-`:115`）に渡し、
`addValue` が名前の数まで `""` で埋める。解釈（`interpret`）は `TestDataParsingTemplate.java:183` で**この前**に済んでいる。

**現行**（`3ee39c9`）: `YamlFileBuilder.java:243`-`:249` が各セルを `interpret` した `rowValues` をそのまま
`addValueWithId`（`:247`）／`addValue`（`:249`）に渡す。`trimTail` に相当する処理が無い。

**実測**（ディレクター。`~/work/cowork/nablarch/ntf-doc-renewal/probe/Probe.java`。本体・yaml に同じ意味の入力を読ませた）:

| 入力（データ行の値） | 本体（NTF 意味） | yaml `3ee39c9` |
|---|---|---|
| F1 `x`,`null`,`null` | `x`,`""`,`""` | **`x`,null,null** |
| F2 `x`,`null`,`y` | `x`,null,`y` | 同 |
| F3 `""`,空,空 | `""`,`""`,`""` | 同 |
| F4 `null`,`null`,`null` | `""`,`""`,`""` | **null,null,null** |
| F5 `x` のみ | `x`,`""`,`""` | 同 |
| F6 `x`,`""`,`null` | `x`,`""`,`""` | **`x`,`""`,null** |
| M1 電文 `x`,`null`,`null` | `x`,`""`,`""` | **`x`,null,null** |
| S2 送信同期 `x`,`null`,`null` | `x`,`""`,`""` | **`x`,null,null** |

**やること**: `rowValues` を `addValueWithId`／`addValue` に渡す直前で `NablarchTestUtils.trimTailCopy` に通す。
**規則を手写ししない**（本体の実装をそのまま使う。本体が変われば追随する）。`interpret` → `trimTail` → `addValue` の順は本体と同じ。

**着手前に特定すること**: 既存テストのうち、レコードの末尾に `null`（クォートなし・値省略）を置いて `null` を期待しているもの。
テストクラス・フィクスチャ（`src/test/java/**/*.yaml`）を全走査し、**件数と一覧を報告してから**実装に入る。

### 2-2. 電文の `records:` に2つ以上のレコードレイアウトを書ける

**解説書**（`afa4f9e` の `implementation/testdata_notation.rst`）:

- `:1153`: 「電文のレコードレイアウトは1つであり、ファイルデータのように複数のレコードレイアウトを持たない」
- `:1299`: 「``records:``\ に記述するレコードレイアウトは1つである。2つ以上記述するとエラーになる」

**Excel の仕組み**（`3c4bd2a`）: `MessageParser.java:70`-`:76` の `onReadingValues` は名前行への切り替えを持たず、
2つ目の名前行以降は**データ行として読まれる**。複数レイアウトを表す記法が無い。

**現行**（`3ee39c9`）: スキーマ `src/main/resources/nablarch/test/ntf-testdata-yaml-schema.json` の `records` は
`message_data`（`:205`-`:208`）・`expected_request_message_data`（`:238`-`:240`）・`group_message_data`（`:269`-`:271`）の3箇所とも
`minItems: 1` だけで上限が無く、`YamlFileBuilder.buildFragmentsInternal`（`:188` から）はレコードごとにフラグメントを作る。

**やること**: 3箇所の `records` に `maxItems: 1` を加える。`description` も「レコードレイアウトは1つ」に改める（2-7）。
検証はスキーマ検証（`YamlLoader`）で落ちる形でよい（静的に決まるため）。

**着手前に特定すること**: 既存フィクスチャで電文セクション（`messages`・`expected_request_header_messages`・
`expected_request_body_messages`・`response_header_messages`・`response_body_messages`）の1エントリに `records` を2つ以上書いているもの。
`src/test/java/**/*.yaml` を全走査し、**件数と一覧を報告してから**実装に入る（`YamlTestDataParserTest/schemaFullCoverage.yaml` を含めて確かめること）。

### 2-3. `fw_header:` に `reader.fwHeaderfields` に無いキーを書いても通る

**解説書**（`afa4f9e` の `implementation/testdata_notation.rst:1295`）:

> ``fw_header:``\ に記載できるキーは、\ ``reader.fwHeaderfields``\ の名前（省略時は ``requestId``\ ・\ ``userId``\ ・\ ``resendFlag``\ ・\ ``resultCode``\ ）だけである。それ以外のキーがあるとエラーになる。フレームワーク制御ヘッダとして扱う名前が ``reader.fwHeaderfields``\ で決まる点は、\ Excel\ 形式と同じである。

**Excel の仕組み**（`3c4bd2a` の `MessageParser.java`）: `:33` `FW_HEADER_KEY = "reader.fwHeaderfields"`、`:107`-`:110` が
`SystemRepository.getString(FW_HEADER_KEY)` が空なら `requestId`・`userId`・`resendFlag`・`resultCode` の4つ、あれば
`NablarchTestUtils.makeArray`（カンマ分割。**前後の空白は取り除かない**）で集合を作り、`:102`-`:104` の `isFrameworkHeader` で判定する。
無い名前の行は制御ヘッダではなくフィールド名称行として読まれる（`:1264`）。

**現行**（`3ee39c9`）: `YamlMessageBuilder.java:233`-`:246` の `convertFwHeader` が、マップの全キーをそのまま制御ヘッダに入れる。

**やること**: `convertFwHeader` で、キーが上の集合に無ければ例外にする。集合の作り方は本体と同じ（同じキー・同じ既定4つ・同じ `makeArray`）。
例外には電文の `id` と不正なキー名を含める（同メソッドの既存の `IllegalStateException` と同じ形でよい）。

**着手前に特定すること**: 既存フィクスチャの `fw_header:` のキーのうち既定4つ以外のもの（`3ee39c9` の実測では
`customProjectKey`・`customField`・`boolFlag` の3つがある。`YamlMessageBuilderTest/customFwHeaderData.yaml`・`fwHeaderMapData.yaml` 付近）と、
それを使うテストが `reader.fwHeaderfields` を設定しているか。**設定していないテストは是正後に落ちる**。件数と一覧を報告してから実装に入る。

### 2-4. 空エントリの判定が「すべての値が空文字」を含む（第1回 2-1 の上書き）

**解説書**（`afa4f9e` の `implementation/testdata_notation.rst:1502`。**`6bfc058` で改訂済み**）:

> 記法として空のエントリは読み飛ばされる。\ Excel\ 形式では行の全セルが空セルの場合、\ YAML\ 形式では ``rows:``\ 内の要素が空マッピング（\ ``{}``\ ）の場合である。\ ``""``\ と書いた空文字は値であり、すべての値が ``""``\ のエントリは読み飛ばされず、全カラムが空文字のエントリとして読み込まれる。

**第1回の指示書 2-1 は「空文字だけを空と見なす」としていた。これを上書きする。** 理由: Excel では `""` と書いたセルは空セルではなく
（本体 `PoiXlsReader.java:140`-`:147` の `isBlankLine` は生セルの `isEmpty()` だけを見る）、全セルに `""` と書いたエントリは残る。
YAML で全値 `""` を落とすと「Excel で表せて YAML で表せない意味」ができる（判断の軸に反する）。

**現行**（`3ee39c9`）: `YamlSection.java:202`-`:209` の `isBlankRow` が「全ての値が空文字」で真を返す。
Javadoc（`:169`-`:181`・`:193`-`:201`・`:219`-`:221`）と `YamlTableDataBuilder.java:169`-`:171` のコメントも同じ前提で書かれている。

**やること**: `isBlankRow` を「空マッピング `{}`（値を1つも持たない行）」だけ真にする。Java null・`""` はどちらも非空。Javadoc・コメントも合わせる。

**着手前に特定すること**: `isBlankRow`／`dropBlankRows` の挙動を期待値に書いた既存テストの全件。`3ee39c9` の実測では
`YamlSectionTest.java:473`-`:595` の6件、`YamlTableDataBuilderTest.java:1292`-`:1687` の12件、`YamlColumnOmissionTest.java:174`、
`YamlFileBuilderTest.java:531` が「blank」を名に持つ。**これ以外にも `""` だけの行を書いたフィクスチャがありうる**ので全走査し、
どれを変えどれを変えないかを件数つきで報告してから実装に入る。

### 2-5. 2文字の `\` ＋ `r` を含む値が読める

**解説書**（`afa4f9e` の `implementation/testdata_notation.rst:1445`。**`04b9405` で改訂済み**）:

> バックスラッシュと ``r``\ の2文字（\ ``"\\r"``\ ）を含む値は書けない。\ Excel\ 形式ではこの2文字が必ず\ CR\ に変換されるため、この2文字を含む値はテスティングフレームワークの仕様上存在せず、\ YAML\ 形式ではエラーになる。\ ``"\\n"``\ は\ Excel\ 形式と同じく2文字のまま残る

`setup/common.rst:77` は YAML 形式に `LineSeparatorInterpreter` を指定しないと定めているため、「CR として解釈する」は採れない。

**Excel の仕組み**（`3c4bd2a`）: `LineSeparatorInterpreter.java:31`・`:34` が既定で `\\r` を CR に置換する。`\\n` は対象外。
本体は全セル（データ行・ディレクティブ行・制御ヘッダ行）に掛ける。

**現行**（`3ee39c9`）: 値は `YamlSection.interpret:248`-`:257` を通る（`YamlFileBuilder.java:243`（データ行）・`:265`（ディレクティブ）、
`YamlTableDataBuilder.java:154`（テーブル）・`:202`（`LIST_MAP`））。制御ヘッダの値は `YamlMessageBuilder.convertFwHeader:244` の
`objectToString` だけを通る。いずれも2文字の `\` ＋ `r` をそのまま値にする。

**やること**: 値（データ行・ディレクティブ・制御ヘッダ）に2文字の `\` ＋ `r` が含まれていればエラーにする。
検査は1箇所（`YamlSection`）に置き、`interpret` と `convertFwHeader` の両方から通す。
例外には値と、分かる範囲で出所（セクション・`id`／`path`）を含める。**`"\\n"` は対象外**（2文字のまま残す）。**実際の CR（`"\r"`）は対象外**。

**着手前に特定すること**: 既存フィクスチャ・テストで2文字の `\` ＋ `r` を値に置いているもの（`3ee39c9` の `git grep` では
`src/test` に0件だが、Java 文字列リテラルの中に `"\\\\r"` として書かれている可能性がある。テストの Java ソースも走査する）。

### 2-6. `@Ignore` 1件の削除（Step 4 の `@Ignore` の判断。2026-08-28）

`YamlTableDataBuilderTest.java:751` `buildListMapRows_unknownCharacterTypeIsNotConverted` は
「列挙外の文字種名は変換されず `${存在しない文字種,3}` のまま」を期待しているが、**解説書はそう書いていない**。
`implementation/testdata_notation.rst:1315`（`afa4f9e`）は「``${文字種,文字数}``\ で使用できる文字種は、以下の14種類に限定される」とだけ書く。
列挙外の名前は本体 `CharacterGeneratorBase.java:53`-`:56`（`3c4bd2a`）が `IllegalArgumentException` を投げ、**Excel でも YAML でも同じ**である。
「間違えたときにどうなるか」は解説書に書かない基準（2026-08-25 ユーザー確定）どおりであり、テストは解説書に無い「あるべき姿」を追っている。

**やること**: このテストメソッドを削除する。フィクスチャ `charTypeUnknownTest`（`YamlTableDataBuilderTest/nativeTypes.yaml`）が
他から参照されていなければ併せて削除する。**他に `@Ignore` を足さない。**

### 2-7. スキーマ `description` の追随

`src/main/resources/nablarch/test/ntf-testdata-yaml-schema.json`（`3ee39c9`）。**スキーマの `description` も SSoT の適用範囲である**（2026-08-25 ユーザー確定）。

| 行 | 何が食い違うか | 合わせる先 |
|---|---|---|
| `:108`（`table_data.rows`）・`:136`（`list_map_data.rows`） | 「全ての値が空文字 `""` の行は、行が無いものとして取り除かれる」 | `notation.rst:1502`（`{}` だけ。2-4） |
| `:213`-`:215`（`message_data.fw_header`）・`:424`-`:430`（`$defs.fw_header`） | 「記述したキーはすべて FW 制御ヘッダとして NTF に渡される」「任意のヘッダ名を許容する」 | `notation.rst:1295`（`reader.fwHeaderfields` の名前だけ。他はエラー。2-3） |
| `:208`・`:241`・`:272`（3つの `records`） | 上限に触れていない | `notation.rst:1153`・`:1299`（レコードレイアウトは1つ。2-2） |
| `:377`（`record_fragment.rows`） | 「不足した末尾のフィールドは `""` として扱われる」だけで、末尾の `null` に触れていない | `notation.rst:889`・`:1155`（末尾の `null` も `""`。2-1） |

**`description` の文言は解説書に合わせる。実装の挙動を写さない。**

---

## 3. テストの作り方

**Excel に同じ意味がある項目（2-1・2-4）は、本体 `nablarch-testing` を正解にする。**
YAML 側の実装の結果どうし（例: `YamlFileBuilder` の出力と自分で書いた期待値）を比べるだけでは、規則の写し間違いを検知できない
（converter の第1回で、正解値を converter 自身の reader にしたため末尾 `null` の欠陥を80経路すべて素通りした実例がある）。

作り方: POI で同じ意味の `.xlsx` を組み（`YamlSectionTest` が既に POI を使っている）、本体の公開 API
`BasicTestDataParser`（`PoiXlsReader` ＋ 本体 `src/test/resources/unit-test.xml:29`-`:40` と同じ順のインタープリタ
`NullInterpreter` → `QuotationTrimmer` → `LineSeparatorInterpreter`。`DateTimeInterpreter`・`${...}` 系は掛けない）で読んだ結果と、
`YamlTestDataParser` で同じ意味の `.yaml` を読んだ結果を比べる。比較はファイル・電文なら `DataFile#toDataRecords()`
（`DataFile.java:155`）の値、テーブル・`LIST_MAP` なら行の値。

**2-1 で必ず入れる入力**: 上の実測表の F1〜F6・M1・S2（送信同期は4種のうち1つ以上）。
**2-4 で必ず入れる入力**: `{}` の行／全値 `""` の行／`null` だけの行／マーカーカラムだけに値がある行、をテーブルと `LIST_MAP` の両方で。

**エラーにする項目（2-2・2-3・2-5）は YAML だけのテストでよい**（Excel に対応する意味が無い）。例外の型と、メッセージに出所が入ることを assert する。
2-3 は `reader.fwHeaderfields` を設定した場合・しない場合の両方、2-5 は `"\\n"` と実際の CR が通ることも入れる。

**足したテスト・直したテストそれぞれについて、期待値をわざと崩すと落ちることを1度確認する**（完了条件3）。

---

## 4. 完了条件

1. **第2節の7件がすべて是正されている。** 是正ごとに、直す前は落ちて直したあとは通るテストがあること（2-6・2-7 は除く）
2. **2-1〜2-5 の「着手前に特定すること」の結果が、実装に入る前に報告されている**
3. **足したテスト・直したテストそれぞれについて、期待値をわざと崩すと落ちることを1度確認している。** 確認したことを報告に書く
4. **既存テストの期待値を変えた箇所が全件挙がっている。** どれを変えどれを変えなかったかを、件数を数えたうえで報告する
5. **`@Ignore` が0件**（2-6 で削除し、新たに足していない）
6. **カバレッジ C0/C1 を計測し、結果を報告する。** `src/main` の是正で下がった箇所があれば挙げる
7. `mvn -o clean test` が緑。着手前は **267件成功・`@Ignore` 1件**（2026-08-27 ディレクター実測）
8. `git status --short` が空。`tmp/` はテストスイート自身が作る空ディレクトリなので残ってよい
9. 変更を push する
10. **converter で落ちるテストを報告する**（直さない）。少なくとも `YamlFormatReaderScalarTest#skipsRowWhoseValuesAreAllEmpty`（`d611bec`。全値 `""` の行が読み飛ばされることを期待）は 2-4 で落ちる見込み。
    `mvn install` した本モジュールで `nablarch-testing-converter@d611bec` の `mvn -o clean test` を実行し、着手前（`Tests run: 656, Failures: 0, Errors: 0, Skipped: 0`）からの差分を全件挙げる

---

## 5. やらないこと

- **解説書を直さない。** 「解説書が誤っている」と判断した項目は、根拠（`file:line` と参照コミット）を添えて報告して止める
- **`nablarch-testing` を直さない。** リリース済みであり `src/main` は変更禁止
- **`nablarch-testing-converter` を直さない。** 落ちるテストは報告するだけ
- **解説書に無い書き方を追いかけない**
- **Excel の実装に合わせない。** 合わせる先は解説書である。本体を oracle に使うのは、解説書が「形式によらず同じ」と定めた意味を確かめるためであり、本体の挙動を仕様にするためではない
- **`YamlFileBuilder` に Excel の行走査（`DataFileParser`）を通さない**（2026-08-28 ユーザー判断。構造は YAML が明示するので判定するものが無く、足りないのは値の規則だけ）

---

## 6. 報告

次の6つを、この順で1つのファイルにまとめる。

1. **2-1〜2-5 の「着手前に特定すること」の結果**（実装前に一度報告する）
2. **第2節7件の是正結果。** 是正ごとに、変更したファイルと `file:line`、直す前に落ちたテストの名前
3. **本体を oracle にしたテストの一覧**（2-1・2-4）。入力ごとに本体の値と YAML の値
4. **期待値をわざと崩す確認の結果。** 対象テスト名と、崩した内容
5. **既存テストの期待値を変えた箇所の全件**
6. **カバレッジ C0/C1** と、**converter で落ちたテストの全件**（完了条件10）

---

## 7. レビュー

**4観点レビューは回さない。** 作業が7件に確定していて探索を含まないため。ディレクターが差分を全量読み直して独立に検証する。

観点D（検証の妥当性）は、次の2つで代替する。

1. 完了条件3「期待値をわざと崩すと落ちること」
2. **第3節の oracle。** 2-1・2-4 は本体を正解にするため、YAML 側の規則の写し間違いは本体との不一致として落ちる


## 8. #44 承認後の追加タスク #45（2026-08-29）

#44 は承認済み（`/rn:ty`。yaml `ef1fc63` の steering に記録済み）。以下は承認文面の全文と、CC の確認2件への回答。
**この節に書いていないことで判断に迷ったら、止まらずに steering へ前提を書いて進め、完了報告で挙げる。** 確認のために止まるのは、進めると取り消しが効かない場合だけ。

### 8.1 承認文面（送付済みの全文。貼り付けで欠けた箇所はこちらが正）

#44 承認（/rn:ty）。ディレクターの独立検証は合格: scratchpad の clone で `mvn -o clean test` 318件緑・`@Ignore` 0件、`src/main` の差分5ファイルを全量読み、ミューテーション7件（2-1 `trimTailCopy` 無効／2-3 未知キー素通し／2-3 設定値無視／2-4 旧判定／2-5 検査無効／2-5 `fw_header` 経路だけ未検査／2-5 判定を過剰に）がすべて検知されること、converter `d611bec` で同じ4件（`656 / Failures: 3, Errors: 1`）が落ちることを再現した。

完了条件 #2 は満たすと判定する。特定結果は `7480453` で最初の実装 `ce81530` に先行して記録されており、タスクごとの停止は #38 以降こちらが免除した。#42 の出典訂正18箇所（§8.6）は受け入れる。

**先に渡した #45 の文面は取り消す。** その作業でローカルに残っている未コミットの変更はすべて捨て、`git status --short` が空・HEAD が `f2891b7` であることを確かめてから、下の #45 に着手する。

§8 の判断:
- §8.1 **仕様差ではない。** 解説書は「後続の行がキーの一部を持たない場合、そのカラムは null を明示的に指定したのと同じ扱い」と既に定めている。T5/L5 は入力が非等価（Excel の空セル＝`""`、YAML のキー省略＝null）なだけ。矛盾していた解説書側の一文（マーカーカラムだけのエントリの他カラムの値）は `nablarch-document@a6da1f6` で「他のカラムの値は通常どおり読み込まれる（Excel の空セルは `""`、YAML のキー省略は null）」に改訂した
- §8.2 converter 側で直す。ディレクターが作成済みの converter 第2回の指示書で扱う。yaml では何もしない
- §8.3 起票不要。解説書の該当文を `a6da1f6` で「後ろに空文字でも null でもないフィールドがあれば null のまま保持される（末尾側に並んだ `""` と `null` は、まとめて `""` になる）」に改訂した
- §8.4 追随する（下の #45 の 2）
- §8.5 **user 判断: ソースコメントから解説書への参照をすべて取り除く**（下の #45 の 1）。リリース済みの `nablarch-testing`・`nablarch-testing-rest`・`nablarch-testing-junit5` の `src/` には解説書への参照が1件も無い（ディレクター実測）。解説書を指す行番号も節見出しも逐語引用も、ソースには書かない。根拠の追跡は `.rn/` の報告書・台帳で行う。機械検証（§8.5 の案1）も作らない

次のタスク **#45**（1タスク。終わったら報告して止まる）:

1. **`src/main`・`src/test`（フィクスチャの YAML・コメントを含む）から、解説書への参照をすべて取り除く。** 対象は `.rst` のパス（行番号の有無を問わない）、`nablarch-document`、「解説書」「出典」「根拠:」として解説書を指す記述、解説書の節見出し・逐語引用（`aac55ad` の実測: `.rst` を含む行 77行・26ファイル、「解説書／出典／根拠:」を含む行 108行）。Javadoc・テストの説明は、**何を確かめるかを自分の言葉で書く**（既存の Given/When/Then と本体クラス名への言及は残してよい）。他リポジトリのソースを `path:line` で指す7箇所（`../nablarch-testing/.../LineSeparatorInterpreter.java:31` など）は行番号とパスを落とし、クラス名だけ残す。**着手前に、取り除く行の全件（`file:line`）を機械抽出して件数を報告してから始める。** 終わったら `git grep -nE '\.rst|nablarch-document|解説書|出典' -- src/` が0件であることを報告に書く
2. 2-5 の規則（バックスラッシュと `r` の2文字を含む値はエラー）を、スキーマ `description` の `table_data.rows`・`list_map_data.rows`・`record_fragment.rows`・`message_data.fw_header`・`$defs.fw_header` に1文ずつ追記する。文言は `record-separator` の既存文（#42）と揃える。実装の挙動を写さない
3. `YamlBlankEntryOracleTest` の T5/L5 の Javadoc から「仕様差」の枠組みを外し、「キーを省略したカラムは null を明示したのと同じ。Excel の空セルは `""` なので入力が非等価」と自分の言葉で書く（1 のとおり解説書は引かない）。あわせて、等価な入力（Excel 側は他のセルに `null` と記述、YAML 側はキー省略）で本体と YAML が一致することを oracle で示すケースを T6/L6 として足す。足したテストは期待値を崩すと落ちることを1度確認する
4. `checks/task-31.md` の3箇所（`:8`・`:9`・`:23`）に「#41 で削除」の注記を入れる（付録 A の未決）

完了条件: `mvn -o clean test` 緑（318件＋T6/L6）・`@Ignore` 0件・1 の grep が0件・`git status --short` 空・push。報告は `report-step4-2.md` に §9 として追記する（1 の件数と抽出方法、2〜4 の変更箇所の `file:line`、T6/L6 の本体の値と YAML の値、崩す確認の結果）。

やらないこと: 解説書・`nablarch-testing`・`nablarch-testing-converter` を直さない。テストの動作・期待値を変えない（1 はコメントとフィクスチャのコメントだけ。変えたら報告に挙げる）。解説書に無い書き方を追いかけない。

---

### 8.2 確認2件への回答と登録内容の訂正

#45 の確認2件への回答と、登録内容（`4688307`）の訂正3件。

1. **スキーマの追記先は5箇所で正しい。** `table_data.rows`（`:108`）／`list_map_data.rows`（`:136`）／`message_data.fw_header`（`:216`）／`record_fragment.rows`（`:380`）／`$defs.fw_header`（`:433`）。行番号は `ef1fc63` のスキーマ。文言を揃える既存文は `:293`（`record-separator`）
2. **Rules の参照点は #45 に含める。** Rules の「参照点（ピン）」1行で解説書だけを `afa4f9e` → `a6da1f6` に取り直す（本モジュール・`nablarch-testing`・converter のピンは変えない）。理由: `afa4f9e` の `testdata_notation.rst:1502` は「他のカラムがすべて空文字のエントリとして読み込まれる」のままで、3（T5/L5 の Javadoc と T6/L6）の前提と矛盾する。`a6da1f6` との差は `testdata_notation.rst:889`・`:1502` と `testdata_converter.rst:63` の3行で、行番号は変わらない。#45 の Steps に「Rules のピン取り直し」を1項目足す

登録内容の訂正:

- **Step A の「ソースを `path:line` で指す7箇所は行番号とパスをそのまま残す」は指示と逆。** 正しくは**行番号とパスを落とし、クラス名だけ残す**（例: `../nablarch-testing/.../LineSeparatorInterpreter.java:31` → `LineSeparatorInterpreter`）。フルパスの7箇所に加え、パス無しで他リポジトリの行番号を指す3箇所（`YamlTestDataParserTest.java:1857` の `SendSyncSupport.java:347`、`YamlTrailingNullOracleTest.java:317` の `MockMessages.java:64`、`YamlMessageBuilderTest.java:1155` の `MessageParser.java:108`）も同じ扱いにする。本モジュール自身を指す `YamlLoader.java:151`（`YamlMessageBuilderTest.java:1385`）は対象外で残す
- **#44 の記録「§8.5 user 判断待ち（継続）。方式は変えない。行番号を書くなら現行どおりでよい」は判定前の記述。** 承認文面のとおり「§8.5 ソースコメントから解説書への参照をすべて取り除く（#45 の 1）。機械検証も作らない」に書き換える
- HEAD が `f2891b7` でなく `ef1fc63` だった件は了解。`ef1fc63` は steering.md のみで push 済みなので、そのままでよい

上の訂正を steering に反映してから #45 に着手する。完了条件・報告の形は送付済みの文面のとおり（終わったら報告して止まる）。
