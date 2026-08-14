# page-entity_unit_test

対象: `ja/development_tools/testing_framework/implementation/class_unit_test/entity.rst`（第3部）
タスク: `#27-21`
個別指示: `.rn/20260724-ntf-yaml-support/ntf-doc-27-large-pages.md` §4
姉妹ページ: `implementation/class_unit_test/component.rst`（承認済み・373行）、`setup/class_unit_test.rst`（承認済み・第2部）

## 1. 参照リポジトリ

| リポジトリ | コミット |
| --- | --- |
| `nablarch-testing` | `e21bf67` |
| `nablarch-document`（旧解説書） | `2e501ad` |

`nablarch-testing` の HEAD は `fdf55d4` だが、本作業の参照コミットは `e21bf67` である。実装の事実はすべて `git show e21bf67:<path>` で読んだ。

## 2. 出典

`mapping.csv` を `csv.DictReader` で全行走査した実測。`dest_page='エンティティ単体テスト'` は **17件・1,344行**。`disposition` は MOVE 16／REFERENCE 1 で、DROP・MERGE は0件。`dest_section` は 使用方法 15／機能概要 2。

| `src_file` | 件数 | 行数 |
| --- | --- | --- |
| `05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst` | 8 | 681 |
| `05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/02_entityUnitTestWithNablarchValidation.rst` | 9 | 663 |

### 全17件の反映先（L1 ゲートの根拠）

| `mapping_id` | `disposition` | 出典 | 反映先 |
| --- | --- | --- | --- |
| `current-0002` | MOVE | BV `:6-12` | `:10` リード文・`:15` 機能概要 |
| `current-0012` | MOVE | NV `:6-12` | 同上（BV と統合） |
| `current-0003` | MOVE | BV `:16-21` | `:78` 使用方法の導入文 |
| `current-0013` | MOVE | NV `:16-21` | 同上（BV と統合） |
| `current-0004` | MOVE | BV `:24-34` | `:534-538` テストデータを作成する |
| `current-0014` | MOVE | NV `:24-35` | 同上（BV と統合） |
| `current-0005` | MOVE | BV `:37-65` | `:82-105` テストクラスを作成する |
| `current-0015` | MOVE | NV `:38-74` | 同上（BV と統合） |
| `current-0006` | MOVE | BV `:68-315` | `:113-283` 文字種と文字列長をテストする |
| `current-0016` | MOVE | NV `:77-285` | 同上（BV と統合。§5-3 を参照） |
| `current-0007` | MOVE | BV `:318-429` | `:287-336` その他の単項目バリデーションをテストする |
| `current-0017` | MOVE | NV `:288-380` | 同上（BV と統合） |
| `current-0008` | MOVE | BV `:432-569` | `:411-470` 相関バリデーションをテストする |
| `current-0009` | MOVE | BV `:572-701` | `:340-407` setterとgetterをテストする |
| `current-0018` | MOVE | NV `:383-553` | `:474-504` バリデーションメソッドをテストする |
| `current-0019` | MOVE | NV `:556-676` | `:508-530` コンストラクタをテストする |
| `current-0020` | REFERENCE | NV `:679-685` | 節にしていない。NV 側の setter・getter の記述は BV 側（`current-0009`）への1行参照であり、統合後は `:340` の節がそれにあたる |

**意図して落とした出典行は0件。** ただし画像14枚と `:download:` リンク6本は落とした（§3・§4）。

同じ2ファイルの残り4件（`current-0001`・`current-0011` は L1 タイトル行で DROP、`current-0010` BV `:704-770`・`current-0021` NV `:688-763` は「クラス単体テストの設定」＝第2部へ割当）は本ページに書いていない。本ページ17件と他ページ全行の `src_file` ＋行範囲の重なりを総当たりで判定し、重なりは0件（G12）。

## 3. 画像

**14枚すべて落とした。** 内訳は BV 側8枚・NV 側6枚で、いずれも Excel のテストデータのスクリーンショットである。`#27-19`（Excel 画像4枚を落とした）・`#27-20`（Excel 画像2枚を落とした）と同じ扱いで、S-10（Excel 形式に依存する記述を置かない）とも整合する。落とした情報は、カラム定義の `list-table`（`:123-162`・`:291-318`・`:344-355`）としてテキストで書き直した。

## 4. `:download:` リンク

**6本（BV `:18-20` の3本、NV `:18-20` の3本）すべて落とした。** → **`decide-3`**

リンク先の実ファイルは削除されていない。`git ls-files ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/01_ClassUnitTest/_download/` は10ファイルすべてを返す（`2e501ad` が削除したのは `.rst` だけ）。落とす理由は資産の不在ではなく、これらが本再構築で置き換える旧 `guide/` ツリー配下にあり、第3部の新ページからリンクを張ると旧ツリーを撤去した時点で参照が壊れることである。

**`reviews/page-component_unit_test.md:49` に「4ファイルは `2e501ad` で削除済み」と書いたのは誤りだった。同ファイルを訂正した。**

## 5. 判断

### 5-1. S-10 の書き分けの流儀は流用しない → **`decide-1`**

個別指示 `ntf-doc-27-large-pages.md:145` は、S-10 の Excel／YAML の書き分けの流儀をバリデーション方式の書き分けに流用してよいか確かめるよう求めている。**流用しないと判断した。** 理由は2つある。

1. `style.md:127-190`（S-03）の例外1 は、文字列 `Excel形式の場合`／`YAML形式の場合` の2つに限定して「〜する」形式と同一ページ内重複禁止を免除している。別の見出し対へ広げるには `style.md` の改訂が必要だが、作業指示 `ntf-doc-weekend-queue.md` §1 の禁止事項3が規約ファイルの書き換えを禁じている。
2. 確認する対象6種のうち3種（相関バリデーション＝Bean Validation のみ、バリデーションメソッド・コンストラクタ＝Nablarch Validation のみ）は片方の方式にしか存在せず、見出し対を立てると片側が空になる。

代わりに、素直に地の文で「Bean Validation の場合は…／Nablarch Validation の場合は…」と分け、表には「使用できる方式」「対象となるバリデーション方式」の列を設けた（`:129`・`:51`・`:188-191`・`:297`）。

### 5-2. 「共通 → 方式別」の構成を採った

個別指示 `ntf-doc-27-large-pages.md:137-147` の指示どおり、出典の「方式ごとに L2 を2本立てる構成」は採らなかった。両方式に共通する3種（文字種と文字列長・その他の単項目バリデーション・setter と getter）を先に1回だけ書き、片方の方式にしかない3種（相関バリデーション・バリデーションメソッド・コンストラクタ）を後に置いた。`#9` のコミット `51f8020` と同じ解である。片方だけの3節は、いずれも導入文の冒頭で「ここで示すのは、〜を使用する場合のテストである」と方式を明示した（`:411`・`:474`・`:508`）。

### 5-3. 457行を表に畳んだ

個別指示 `ntf-doc-27-large-pages.md:151` は、`current-0006` ＋ `current-0016` の457行（出典全体の34%）を表1つに畳めないか最初に検討するよう求めている。**5つの表に畳んだ結果、本文171行（`:113-283`）になった。**

| 統合したもの | 反映先 |
| --- | --- |
| カラム定義（BV 13列・NV 10列の2組） | `:123-162` の1表。「使用できる方式」列で BV 専用の3列（`group`・`interpolateKey_`*n*・`interpolateValue_`*n*）を区別 |
| `o`／`x` の記法 | `:174-186` の1表 |
| メッセージの記載形式（方式ごと） | `:188-206` の箇条書き1組＋記載例1表 |
| `messageIdWhenInvalidLength` 省略時のデフォルト値（BV 4行・NV 3行の2表） | `:210-233` の1表。NV は `max` を省略できないため NV の3行は BV の4行に包含される。差分は `minMessageId` の行に注記した |
| 実行される観点（方式ごとに同内容を2回） | `:241-265` の1表。「テストが実行されない条件」列を追加した |

## 6. 出典と実装の食い違い（実装を優先した箇所）

| 箇所 | 出典の記述 | 実装 | 本文 |
| --- | --- | --- | --- |
| 文字列長不足のテストが実行されない条件 | BV `:311`・NV `:279`「`min` 欄が省略された場合は実行されない」 | `CharsetTestVariation.java:275` `if (min <= 1) { return; }`（コメント: 最短0桁は負の桁でテストできない／1桁は未入力テストで代替） | `:262`「`min` が1以下の場合」。`min` を明示的に `1` と記入した場合も実行されない点は出典に無い |
| 指定できる文字種 | 11種のみ列挙 | `BasicJapaneseCharacterGenerator.java:41-56` は14種（中国語・サロゲートペア・改行が出典に無い） | `:170` に14種すべてを列挙 |
| 必須カラム | 記述なし | `CharsetTestVariation.java:107-145` は `allowEmpty`・`propertyName`・`messageIdWhenNotApplicable`・`max`・`min` を `rowData.get()` で読むため、**値が空欄でもカラム自体が無いと例外**になる | `:164-168` の `important` に追記 |
| 文字種のカラム名 | 記述なし | `CharacterGeneratorBase.java:53-59` は未知の名前に `IllegalArgumentException("unknown charsetName…")` | 同上 `important` に追記 |
| `Map` コンストラクタが無い場合 | 記述なし | `EntityTestSupport.java:535-550` `createEntityInstance` は `NoSuchMethodException` を捕捉してデフォルトコンストラクタにフォールバックする | `:73` の `important` に追記 |
| setter・getter・コンストラクタのテストデータのカラム | Excel 画像でのみ提示 | `EntityTestSupport.java:404-431`・`:487-525` が `name`・`set`・`get` を読む。`set` が空の行は setter を呼ばず、`get` が空の行は確認しない | `:344-355` の表に書き起こした |

## 7. ゲート

| ゲート | 結果 | 根拠 |
| --- | --- | --- |
| G1 `git status --porcelain` 全件 | PASS | `M entity.rst`・`M reviews/page-component_unit_test.md`・`?? reviews/page-entity_unit_test.md`・`M checks/task-27.md`・`M steering.md` のみ |
| G2 禁止ファイル差分0 | PASS | `design.md`・`mapping/style.md`・`mapping/glossary.md`・`mapping/vocabulary.md`・`mapping/mapping.csv`・`mapping/input/`・`ja/conf.py` を指定した `git status --porcelain` が0行 |
| G3 `sphinx.mo` 未コミット | PASS | `git status --porcelain` に出現なし |
| G4 `verify_mapping.py` | PASS | `OK: no errors`（exit 0） |
| G5 フルビルド | PASS | `-E` 付きフルビルドで `build succeeded.`、**`WARNING`・`ERROR` を含む行は0件**（全ログを保存して `grep -nE 'WARNING\|ERROR'` で実測） |
| G6 禁止語 | PASS | `不具合`・`バグ`・`将来`・`修正され` が0件 |
| G7 ラベル | PASS | `entity_unit_test` が `style.md:372` の確定表（および `ntf-doc-27-large-pages.md:116`）と文字列一致。`ja/`（`_build/` 除く）で重複定義0件 |
| G8 下線幅 | PASS | L1 `=` 50／L2 `-` 50 × 2／L3 `~` 49 × 5／L4 `^` 49 × 6。`awk` で実測し、`#27-19`・`#27-20` の 50/50/49/49 と一致 |
| G9 `:ref:` 飛び先とリンクテキスト | PASS（例外2件） | 14種・のべ24箇所すべて飛び先が実在。リンク文字列は飛び先の見出しと文字列一致。例外は `application_design` と `nablarch_batch-application_design` の2件で、**両者の見出しがともに「アプリケーションの責務配置」で同一のため、そのまま使うと1文中で区別できない**。`messaging/db/application_design.rst:4` が「Nablarchバッチアプリケーションの責務配置」という同じ文字列を使っている先例に合わせた |
| G10 出典の反映 | PASS | 17件すべてを反映（§2 の表）。意図的drop は0件 |
| G11 REFERENCE行を節にしない | PASS | `current-0020` は独立した節にしていない（§2 の表の最終行） |
| G12 二重掲載なし | PASS | 本ページ17件と他ページ全行の `src_file` ＋行範囲の重なりを総当たりで判定し0件 |
| G13 画像 `git mv` | PASS（該当なし） | `.. image::` 0件。14枚すべて落とした（§3） |
| L1 全 `mapping_id` の反映または意図的drop | PASS | §2 の17行の表が全件の反映先を示す |
| L2 他ページ割当の出典を書いていない | PASS | 第2部へ割当の `current-0010`（BV `:704-770`）・`current-0021`（NV `:688-763`）＝自動テストフレームワーク設定値の内容は書いていない。`:78` と `:208` から `class_unit_test_setting` へ送っている |
| L3 「〜したい」形式の見出し0件 | PASS | 見出し14件のうち「したい」で終わるものは0件 |
| L4 `拡張例` の見出しなし | PASS | `拡張例` が0件 |
| L5 L3見出しがすべて「〜する」形式 | PASS | L3 5件・L4 6件すべて動詞終止形の肯定形 |
| L6 フルビルドの警告 | PASS | G5 と同じ |
| L7 `implementation/index.rst` の toctree | PASS | 未変更（`git status` に出現しない）。`class_unit_test/entity` → `class_unit_test/component` の並びは `design.md:943-944` と一致 |
| S-01 である調 | PASS | です・ます・ください・下さい が0件（`:201`・`:203` の「です」はメッセージの記載例であり地の文ではない） |
| S-02 セクション構成 | PASS | リード文（目次直後・最初のL2より前）→ 機能概要 → 使用方法 |
| S-03 見出し | PASS | 「使用方法」配下の13見出しがすべて「〜する」で終わる。禁止語（概要・補足・注意事項・その他・準備する・設定する）0件。同一ページ内の重複0件 |
| S-04 下線記号 | PASS | L1 `=`／L2 `-`／L3 `~`／L4 `^` |
| S-05 code-block | PASS | 17件すべて言語指定あり（`java` 15／`text` 2）。内容はディレクティブ行から相対2字下げ |
| S-06 important / tip | PASS | `note::` 0件。`important` 5件はいずれも実行時エラーまたは必ずテストすべき対象、`tip` 8件は読まなくても作業できる補足 |
| S-07 表 | PASS | `list-table` 11件、すべて `:widths:` 指定あり。grid table・simple table は0件 |
| S-08 ラベル | PASS | ページ先頭ラベル1件のみ。節ラベルは定義していない |
| S-09 `.. contents::` | PASS | ラベル→タイトル→`.. contents:: 目次` / `:depth: 3` / `:local:` の順 |
| S-10 Excel／YAML書き分け | PASS | 形式に依存する記述を置いていない。読み込み単位は `:536` で「Excel 形式ではシート、YAML 形式ではファイル」と両方式を併記 |
| S-11 L4を持つL3の導入文 | PASS | L4を持つL3は「テストメソッドを作成する」1件で、`:109` に配下6件の内容と並び順の理由を述べた導入文がある |
| 用語置換 | PASS | `テストケース`・`精査`・`自動テストフレームワーク`・`想定結果`・`想定値`・`スーパークラス`・`テストソースコード`・`既定`・`Form単体テスト`・`Entity単体テスト` が0件 |

## 8. 4観点レビュー

QA / 設計 / クラフト / 検証 を別々のサブエージェントで実施。**必須指摘は4件で、すべて本文に反映した**（是正ラウンド1回）。

### 反映した必須指摘

| 観点 | 指摘 | 対応 |
| --- | --- | --- |
| 検証 | `:73` の「設定した方式に対応しないメソッドを呼び出すと `UnsupportedOperationException` が発生する」は全メソッドに成り立たない。例外を投げるのは `EntityTestSupport.java:145`（`testValidateAndConvert`）と `:173`（`testBeanValidation`）だけで、`testConstructorAndGetter`（`:440-445`）には検査が無い | `:73` を2メソッドに限定し、コンストラクタのテストがデフォルトコンストラクタにフォールバックする旨を追記 |
| 検証 | `:556-557` は「その他の単項目バリデーション」の失敗時にも観点が出力されるように読めるが、`EntityTestSupport.java:746-747` の `testSingleValidation` 呼び出しは `additionalMsgOnFail` を渡していない | 表の行を2つに分け、観点が出力されないことを明記（`:556-559`）。`:565` の `tip` にも `case` カラムが出力されない旨を追記 |
| クラフト | 文字種と文字列長・その他の単項目バリデーションの2節に、テストデータのデータタイプが書かれていない | `EntityTestSupport.java:687`・`:730` が `getListMapRequired` を使うことを確認し、両節に `LIST_MAP` を明記（`:121`・`:289`） |
| （自己検出） | `:ref:` 4種のリンク文字列が飛び先の見出しと一致していない（`特殊記法` × 3・`埋め込み文字`・`エンティティバリデーションのテストショット一覧を記述する`）。`testdata_notation.rst:356`・`testdata_examples.rst:1901`・`web.rst:322` はいずれも見出しをそのまま使っている | 3種を飛び先の見出しに合わせて書き換え（G9） |

### 反映した任意指摘

- `:340` に、setter・getter のテストには型の制限がある旨を追記（クラフト）。制限を見落として「全プロパティをテストした」と誤解するのを防ぐ。
- `:476` に、バリデーションメソッドのテストの記述例への `:ref:` を追加（クラフト）。相関バリデーションの節（`:413`）と対称にした。
- `:528-530` の `important` を圧縮（クラフト）。`:373-375` とほぼ同文だったため、「setter と getter のテストで述べたのと同じ理由から」に置き換えた。
- `:117` の `tip` を `important` に格上げ（クラフト）。「別の Form を保持する Form には使用できない」は無視すると誤ったテストデータを作る制約であるため。
- `:538` に「データベースに格納する」を補った（クラフト）。出典 BV `:32`・NV `:33` にこの語があり、落としたことで DB 前提が唐突に見えていた。
- 全角/半角境界の `\ ` エスケープ漏れ6箇所を修正（QA）。`:140`・`:233`・`:413`・`:445`・`:451`・`:476`。

### 根拠を確かめて反映しなかった指摘

| 観点 | 指摘 | 反映しない理由 |
| --- | --- | --- |
| QA | `:339` の見出し「setterとgetterをテストする」に `\ ` エスケープが無い | 承認済みページの見出しで `\ ` を使っている例は0件（`implementation/`・`setup/` 配下の全見出しを `awk` で走査）。`testdata_examples.rst:419`「テストショット一覧（testShots）を記述する」・`:44`「Excel形式の場合」も全角/半角が混在するがエスケープしていない |
| クラフト | 文字種と文字列長の節（171行）に小見出しを割る | この節は既に L4 であり、`style.md:185-215`（S-04）に L5 の記号定義が存在しない。規約の改訂が必要だが禁止事項3で禁じられている → **`decide-2`** |
| クラフト | `:174-186` の `o`／`x` の表は情報量が少ないので地の文にする | 記法の対応表であり、`testdata_notation.rst` の同種の表と粒度が揃っている |
| クラフト | `:267` の「`o` を設定した文字種が1つも無い行があるとエラーになる」を `important` にする | `o`／`x` の説明を読んだ直後でなければ意味が通らないため、地の文のまま位置を保った |
| 設計 | `:262` の「`min` が1以下の場合」は出典より広い一般化 | 実装（`CharsetTestVariation.java:275` `if (min <= 1) { return; }`）で裏付けた。§6 に記録 |

## 9. 判断待ち（週明けに判定してほしい項目）

- **`decide-1`（推奨）**: S-10 の Excel／YAML の書き分けの流儀を、バリデーション方式の書き分けへ流用しないと判断した（§5-1）。判断の分かれ目は `style.md:127-190`（S-03）の例外1 が文字列を2つに限定していることで、規約を改訂するなら流用もありうる。**この判断でよいか確認してほしい。**
- **`decide-2`（推奨）**: L4 見出しの下に小見出しが必要なページが出てきた。本ページの「文字種と文字列長をテストする」は171行あり、再訪時に特定の表へ辿り着きにくい。`style.md:185-215`（S-04）に L5 の記号定義が無いため対応できなかった。`#27-19` の `decide-1`・`#27-20` の①（L4 の使用量が `style.md:193`「用例が薄いページでのみ使う」と噛み合っていない）と同じ条文の問題である。**S-04 を判定可能な形に改める必要がある。**
- **`decide-3`（推奨）**: `_download/` 配下の10ファイルが `guide/` 旧ツリーに残っている（§4）。旧ツリーを撤去する際に、サンプルの成果物として第3部へ移設するか、あわせて削除するかを決める必要がある。
- **`decide-4`（参考）**: 個別指示 `ntf-doc-27-large-pages.md` §4 は本ページの出典を「457行（34%）」と述べており、`mapping.csv` の実測（`current-0006` 248行＋`current-0016` 209行＝457行／全体1,344行＝34.0%）と一致した。`#27-20` の⑥で報告した出典件数表のずれは、本ページには無かった。
- **`decide-5`（参考）**: `#27-20` からの申し送り（`checks/task-27.md:959`）は満たされている。`web.rst:399` は `entity_unit_test` へ「setter・getter のテストと同じ書式で期待値を記述する」として送っており、本ページ `:344-355` に `name`・`set`・`get` のカラム表がある。ただし飛び先はページ先頭のため、読者は目次から「setterとgetterをテストする」を辿る必要がある。節ラベルを振って `web.rst` の飛び先を変えることもできるが、承認済みページの `:ref:` を書き換えることになるため見送った。

## 10. `#27` 完了時の申し送り

作業指示 `ntf-doc-weekend-queue.md` §8 の申し送り（`nablarch-testing-yaml` が `1.0.0-SNAPSHOT` であり、BOM 収録をリリース時に確認する）は、**`reviews/page-common.md:170-174` に記録済みである**。作業指示は宛先を `reviews/page-testing_framework_common.md` と書いているが、`setup/common.rst` のレビュー記録は `reviews/page-common.md` であり、そちらに残した。

なお、作業指示 `ntf-doc-weekend-queue.md` の §8 はバージョンの出典を `pom.xml:17` としているが、実測は **16行目**（`grep -n '1.0.0-SNAPSHOT' /home/tie303177/work/nablarch/nablarch-testing-yaml/pom.xml` → `16:  <version>1.0.0-SNAPSHOT</version>`）。`page-common.md` の記載が正しい。
