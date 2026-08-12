# レビュー記録: `setup/class_unit_test.rst`（第2部「クラス単体テストの設定」）

対象タスク: `#14`。**個別の作業指示を出さず、`steering.md`「#9〜: ページの作成」の共通 Steps のみで進めた初のページ**（`#13` で定着させた運用）。ベースコミット `dacd7af`、初版コミット `8285125`。

対象ページ: `ja/development_tools/testing_framework/setup/class_unit_test.rst`（新規作成）
出典: 削除済みの現行解説書（`origin/develop` で参照）
マッピング行: `dest_page=クラス単体テストの設定` の3行（`current-0010` / `current-0021` / `current-0191`）。193 lines、すべて `dest_section=使用方法`・`disposition=MOVE`・`audience=user`。

実装での事実確認: `nablarch/nablarch-testing` の `main`、**参照コミット `e21bf67`**。`file:line` は本ファイル各項に記載する。

## 作成時の判断（レビュー前に確定したもの）

### D-1 出典2件の設定項目一覧を1つの表に統合した

`current-0010`（Bean Validation 版、8項目）と `current-0021`（Nablarch Validation 版、6項目）は**同一クラス `EntityTestConfiguration` の設定項目一覧**であり、別々に載せると同じクラスの設定が2箇所に分かれる。`EntityTestConfiguration` の公開セッターは8件で、これは `current-0010` の8項目と一致する（`EntityTestConfiguration.java` のセッター全件を確認）。よって8項目の表1つに統合し、方式による差は表のセルと `.. important::` で表した。

### D-2 メッセージIDの意味を実装の分岐で組み直した

出典2件は同じ設定項目に異なる説明を与えている（下表）。`design.md` §8「出典どうしが食い違う場合は実装を優先する」に従い、`EntityTestConfiguration.getOverLimitMessageId`（`EntityTestConfiguration.java:100-111`）と `getUnderLimitMessageId`（同 `:76-91`）の分岐で意味を確定した。

| 設定項目 | `current-0010` | `current-0021` | 実装での確定 | 採用 |
|---|---|---|---|---|
| `maxMessageId` | 最大文字列長超過時 | 最大文字列長超過時 | `:100-103` `min==null`（最大のみ指定）の超過時 | 実装 |
| `maxAndMinMessageId` | 可変長・超過時 | 可変長（超過/不足の別なし） | `:106-107` `max>min` の超過時 | 実装（`current-0010` 側と一致） |
| `underLimitMessageId` | 可変長・不足時 | 文字列長不足時（一般） | `:86-87` `max>min` の不足時 | 実装（`current-0010` 側と一致） |
| `fixLengthMessageId` | 固定長 | 固定長 | `:84-85` と `:104-105` の双方で返る＝**超過・不足の両方**で使う | 実装（出典2件のどちらも明示していない事実を補った） |
| `minMessageId` | あり（不足時） | 記載なし | `:82-83` `max==null`（最小のみ指定）の不足時 | 実装 |
| `emptyInputMessageId` | 未入力時 | 未入力時 | `:65-67` | 一致 |

### D-3 メッセージIDは「デフォルト値」であることを明記した

`current-0010` は「デフォルト値」と書き、`current-0021` は単に「メッセージID」と書いている。実装では、テストデータに `messageIdWhenInvalidLength` / `messageIdWhenEmptyInput` が指定されていればそちらが優先され、未指定のときだけ `EntityTestConfiguration` の値が使われる（`CharsetTestVariation.java:265-267`・`:279-281`・`:287-289`）。`current-0010` 側の「デフォルト値」が実装と整合するため採用した。

### D-4 第2部の記載範囲を守り、テストデータの記述例は置かなかった

出典 `current-0191` の直前（`current-0190`、`02_DbAccessTest.rst:429-443`）にあたる「カラムを省略したときの扱い」は `dest_page=テストデータの書き方` に割当済みである。本ページは設定の説明に徹し、省略時の扱いは `` :ref:`カラムを省略する <testdata_notation-column_omission>` `` で第3部へ導線を張った（`design.md` §3）。

### D-5 `validationTestStrategy` を掲載した（`decide` 判定）

事前調査（`ntf-doc-13-standing-rules.md:79` の付録）は「`validationTestStrategy` はどちらの出典にも無い」「`minMessageId` は出典どうしの食い違いで実装が正」としていたが、**いずれも指示側の誤りとして取り消された**（ユーザー判定、2026-08-12）。

- `validationTestStrategy` は `current-0010` の表（`:731`）・脚注（`:744`）・記述例（`:767`）に**実在する**。落とすと「マッピングにある内容を落とさない」に抵触するため掲載した。
- `minMessageId` が `current-0021` に無いのは欠落ではなく正しい。Nablarch Validation では最大文字列長の省略が実行時に例外となり（`CharsetTestVariation.java:126-130`）、`minMessageId` に到達しないためである。

詳細は `checks/task-14.md` §2。

## ラウンド1 — 4観点レビュー（A:網羅性 / B:トンマナ / C:用語 / D:整合性）

`steering.md` Rules に従い、**4観点をそれぞれ別のサブエージェント**で実施した。各観点には成果物・目的・完了条件・チェックリストのみを渡し、self-check ファイルも他観点の判定も渡していない。プロンプトには Rules が要求する3点（実測コマンドで裏付けよ／付属の検証スクリプトを正解として使わず独立に組め／敵対的にレビューせよ）を全観点に入れた。

**指摘件数**: must 4件（A:1 / D:3）、should 8件（A:2 / B:3 / C:3）、note 12件（A:5 / B:5 / C:2 相当・重複含む）。4観点とも overall: fail。

### 有効と判定し是正した指摘

| # | 観点 | severity | 指摘 | 実装・出典での裏付け | 対応 |
|---|---|---|---|---|---|
| R1-1 | D | must | 「文字列長に関する**4つ**のメッセージID」は誤り。文字列長関連は5つ | `EntityTestConfiguration.java:76-111` の2メソッドが `max`/`maxAndMin`/`min`/`underLimit`/`fixLength` の5つを返し分ける | 「5つ」に是正 |
| R1-2 | D | must | 文字種・文字列長テストのデータ行を「**テストショット**」と呼んでいるが別物 | `EntityTestSupport.java:684-697` は**任意IDの `LIST_MAP`** を読む。`testShots`（`:239`）は項目間バリデーション用で必須カラムも別（`testdata_notation.rst:561-578`）。カラム体系は `CharsetTestVariation.java:107-146` の `allowEmpty`/`propertyName`/`max`/`min`/`messageIdWhen*` | 文字種・文字列長のテストデータを指す表現に置換 |
| R1-3 | D | must | `.. important::` 後半（`minMessageId` 必須の条件）が過剰一般化 | 例外は `EntityTestConfiguration.java:78-80` のみ。唯一の呼び出し元 `CharsetTestVariation.java:272-283` は `:275` `min<=1` で早期 return、`:279-281` で `messageIdWhenInvalidLength` 指定時は呼ばない | 「最大を省略し、かつ最小に2以上を指定し、かつ `messageIdWhenInvalidLength` 未指定」に限定 |
| R1-4 | A | must | `current-0021:696`「（全項目必須）」が本文にも記録にも無い | 実装に一律の必須検査は無く（`validationTestStrategy` は `EntityTestConfiguration.java:41` に既定値）、8項目必須とは書けない。実効的に必須なのは `characterGenerator`（未設定で `CharsetTestVariation.java:320` が NPE） | `characterGenerator` 未設定で例外になる旨を明記。一律必須でない根拠は `checks/task-14.md` に記録 |
| R1-5 | A | should | 「メッセージのキーを指定する」は不正確 | `BeanValidationTestStrategy.java:135-150` が `MessageInterpolator` で補間する＝`{}` で囲んだメッセージテンプレート。記述例（`:53-58`）も `{}` 付き | テンプレートである旨に是正 |
| R1-6 | C | must | 散文中の完全修飾クラス名リテラル4件は先行4ページに前例0件。同ページ内でも `:java:extdoc:` と混在 | 承認済み `common.rst:40` は `nablarch.test.*` を `:java:extdoc:` で記述。`ja/conf.py:305` の `javadoc_url_map` が `nablarch` を解決 | 4件を `:java:extdoc:` に統一 |
| R1-7 | C | should | 「データベースを使用するテスト」はテスト種別名の欠落形 | `glossary.md` §5.5 の正表記は `データベースを使用するクラスのテスト` | 正表記側に是正 |
| R1-8 | C | should | XMLコメント「エンティティテスト設定」が地の文の `エンティティ単体テスト` と不一致 | 出典からの逐語引き継ぎ。`glossary.md` §1 の適用対象は本文であり、コード内の**日本語コメント**は識別子ではない | 用語に揃えた |
| R1-9 | C | should | 「設定値」がページ内で二義（総称／各項目に指定する値） | `:12`・`:14` は総称、`:113` は列見出し | 総称側を「設定項目」に、列見出しを「指定できる値」に |
| R1-10 | C | note | 同一文内で「メッセージのID」と「メッセージID」が揺れ | — | 「メッセージID」に統一 |
| R1-11 | C | should | 「実行時エラー」は先例が無い | FW解説書は「実行時エラー」1件（`SQL実行時エラー`）に対し「実行時例外」27件・「例外が発生する」13件。現行解説書0件、NTF既存ページ0件 | FW多数派の例外表現に是正 |
| R1-12 | C | note | 「バリデーションの方式」は FW 0件・現行 0件の造語 | FWは「バリデーション機能」13件 | 先例のある言い方に是正 |
| R1-13 | D | should | 「省略したカラムはデフォルト値として扱われる」が参照先と食い違う | `BasicTestDataParser.java:171-180` は `fillDefaultValues()` を `EXPECTED_COMPLETED` にのみ適用。参照先 `testdata_notation.rst:697` は「`EXPECTED_TABLE` では比較対象外」と明記 | 適用範囲を限定した表現に是正 |
| R1-14 | B | should | L3見出しが `style.md` S-03 の内容条件（組だけで中身が分かる）に抵触 | `common.rst` の L3 3件はいずれも対象語が見出し内で完結 | 対象を見出しに含めた |
| R1-15 | B・D | should | 参照が一方向で切れている | `testdata_notation.rst:700` は `BasicDefaultValues` に言及しながら設定方法のページを指していない。`design.md` §D観点が「参照が一方向で切れていないか」を挙げる | `testdata_notation.rst:700` に `class_unit_test_setting` への `:ref:` を1箇所追加 |
| R1-16 | A | note | `maxAndMinMessageId` の説明が `max>min` の条件を落としている | `EntityTestConfiguration.java:104-108` は `max.equals(min)` を先に `fixLengthMessageId` へ振る | 「異なる値を指定した場合」と分かる形に |
| R1-17 | A・D | note | 導入文が実際の挙動と設定項目を取りこぼす | `CharsetTestVariation.java:235-241` の `testAll` は文字種のテスト（`:296-320`）と適正長のテストも実行。導入文は `validationTestStrategy` を受けられない | 表の8項目を受けられる導入文に |
| R1-18 | B | note | 「上の記述例」は少数派 | FW「上記」32件 対「上の記述例／上の例」4件。NTF既存ページは「上記」2件・「上の〜」0件 | 「上記」側に |
| R1-19 | B | note | `minMessageId` のセル単独では Bean Validation 専用と分からない | 条件は `important` にしかない | セルに一言追加 |
| R1-20 | C | note | 「コンポーネント設定」は正表記の短縮形 | `glossary.md` §5.12。`common.rst` は4箇所すべて正表記、短縮形0件 | 正表記に |

### 有効でないと判定した指摘（是正しない）

| # | 観点 | 指摘 | 却下の根拠 |
|---|---|---|---|
| R1-X1 | B | 2つ目の表を simple table にする（S-07 規約本体は短い2〜3列表を simple table と定める） | **`style.md` S-07:241「本例外の適用はページ単位で判断する（同一ページ内で表ごとに記法を使い分けない）」に抵触する。** 1つ目の表は `:java:extdoc:` と長文説明を含むため `list-table` が正であり、ページ単位の判断は `list-table` に決まる。指摘が挙げる `about/index.rst` の混在例は、S-07 の当該条項が確定した `#9`・`#10` より前の成果物である |
| R1-X2 | B | 「使われる」を「使用される」に統一する（FW 0件 / 17件） | 承認済み `testdata_notation.rst` 2件・`testdata_examples.rst` 3件に先例があり、NTF解説書内の一貫性を優先する |
| R1-X3 | B | XML の `value=` の桁揃えを外す（FW・NTF既存ページとも0件） | 出典（`current-0010`・`current-0021` の記述例）からの原形保存であり、コード例の忠実性を優先する |
| R1-X4 | A・D | `charValue`「1文字のASCII文字」・`numberValue`「0または正の整数」を実装に合わせて緩める（`BasicDefaultValues.java:102-108` は長さ1のみ検証、`:125-127` は無検証） | 出典 `current-0191:457,459` どおりの**推奨値**として維持する。実装が検査しないことは、利用者が任意の値を入れてよいことを意味しない。R1-9 の列見出し変更（「設定値」→「指定できる値」）により推奨値として読める形になる |
| R1-X5 | D | `LengthValidator` に不足時専用のメッセージIDが無い理由を補足する | バリデータ側（Nablarch Validation 本体）の仕様であり、本ページの記載範囲（NTF のコンポーネント設定）外。出典にも無い |
| R1-X6 | D | `emptyInputMessageId` が `allowEmpty` の値によって使われない旨を補足する | `allowEmpty` はテストデータ側のカラムであり、その記法は第3部「テストデータの書き方」の範囲。第2部に持ち込まない（`design.md` §3） |

### 未対応として残す判断（保留）

| # | 観点 | 内容 | 残す理由 |
|---|---|---|---|
| R1-P1 | A | 出典2件が持っていた第3部エンティティ単体テストへの `:ref:` 導線（`current-0010:705`・`current-0021:689`）が本ページに無い | 参照先ページが**未作成**（`implementation/` 配下は `index.rst`・`testdata_notation.rst`・`testdata_examples.rst` のみ）。第3部エンティティ単体テストのページ作成タスクで `:ref:` を追加する（下記 申し送り1） |

ラウンド1の是正はコミット `ca699c5`（`class_unit_test.rst` 18行 / `testdata_notation.rst` 1行）。

## ラウンド2 — 是正差分限定の検証

`#10b` の申し送り「是正ラウンド2以降は、是正差分に限定した検証観点のみを回す」に従い、ラウンド1の差分（`ca699c5`）だけを対象に、**「是正が指示範囲に収まっているか」「是正が新しい欠陥を生んでいないか」の2点**をレビューした。ページ全体の再レビューはしていない。

**判定: pass（`must` 0件）。指摘は should 3件・note 5件。**

| # | severity | 指摘 | 判断 | 対応 |
|---|---|---|---|---|
| R2-1 | should | L3見出しから「省略した」が落ち、「テストデータのカラム」は `ファイルデータ` の項目も含む語で範囲が過広。直下の本文（実装どおりデータベースに限定）と食い違う | 有効 | 「**省略したテーブルのカラムのデフォルト値を変更する**」に。表示幅48で L3 下線49文字に収まる |
| R2-2 | should | 「テストデータに指定された最大文字列長・最小文字列長」がカラム名を示さず、読者が引ける先が無い（当該カラムは第3部にも未記載） | 有効 | `` ``max`` ``・`` ``min`` `` のカラム名を明示（`CharsetTestVariation.java:124-137`） |
| R2-3 | should | `important` の「文字列長が不正な場合に期待するメッセージIDを明示的に指定していないとき」が、直前の表の設定項目を指すとも読め、「設定項目を指定しないと設定項目が必須」という循環に読める | 有効 | テストデータのカラム `` ``messageIdWhenInvalidLength`` `` を名指し（`CharsetTestVariation.java:279-281`） |
| R2-4 | note | 「`max`・`min` の組み合わせで決まる」だけでは一意に決まらない（`max > min` では超過時 `maxAndMinMessageId` / 不足時 `underLimitMessageId` に分かれる） | 有効 | 超過・不足の軸を追加（`EntityTestConfiguration.java:76-91` と `:100-111` が別メソッド） |
| R2-5 | note | 導入文の拡張により、文字種不適合時のメッセージIDにも `EntityTestConfiguration` のデフォルト値があるように読める。実際は必須カラム `messageIdWhenNotApplicable` で行ごとに指定する | 有効 | デフォルト値を持つのは文字列長と未入力に関するメッセージIDだけであることを明記（`CharsetTestVariation.java:41-47`・`:296-320`） |
| R2-6 | note | 「メッセージテンプレート」は `ja/` 全体で当該1件のみの語。FW解説書は同じ対象を別表現で書いている | 有効 | FW解説書 `bean_validation.rst:114,139` の先例に寄せた |
| R2-7 | note | ラウンド1で追加した逆方向 `:ref:` がページ先頭に飛び、`BasicDefaultValues` がクラス単体テスト限定の設定に見える。実際は `testDataParser` の共有プロパティ（`BasicTestDataParser.java:44,239`） | 有効 | 該当 L3 に `class_unit_test_setting-column_default_values` を定義し、そこへ飛ばした（`style.md` S-08 の `<ページ先頭ラベル>-<内容>` 形式。`ja/` 全体で衝突0件） |
| R2-8 | note | ラウンド1で指示範囲外の変更が1行（`underLimitMessageId` の説明も「異なる値を指定した」に変更） | **受け入れ（記録のみ）** | 実装（`getUnderLimitMessageId` は `max > min` のときのみ）と一致し、片方だけ直すと `fixLengthMessageId` 行の「同じ値」と噛み合わなくなる。整合上必要な変更として承認した |

ラウンド2の是正はコミット `5a55ada`。ラウンド2の検証で**新たな事実誤りは検出されなかった**（`important` の条件は実装と過不足なく一致、段落内改行0件、下線幅・`:java:extdoc:` のエスケープ・リンク解決〈HTTP 200〉・ビルド出力とも問題なし）。

## `#15` 以降への申し送り

1. **第3部エンティティ単体テストのページを作成したら、本ページから `:ref:` を張る。** 出典 `current-0010:705`・`current-0021:689` が持っていた導線であり、`design.md` §3 の「第2部からは `:ref:` で参照する」に対応する。R1-P1 の保留分。
2. **`#10a` の用語統一（`テストケース` → `テストショット`）を機械的に適用すると事実誤りになる箇所がある。** 本ページの R1-2 がその実例で、出典が「テストケース」と呼んでいた文字種・文字列長テストのデータ行は `testShots` のエントリではない（`EntityTestSupport.java:684-697` は任意IDの `LIST_MAP` を読む）。**置換先は referent を実装で確かめてから決める**こと。`glossary.md` §8 の対応表自身も、`@Test` メソッドなら `テストメソッド`、何を検証するかを述べる文脈なら普通名詞の `テスト` と、referent 依存の置換を認めている。
3. **散文中のクラス名は `:java:extdoc:`単純名 <完全修飾名>`` で書く。** 完全修飾名のリテラル（`` `` `` 囲み）は先行4ページに前例が0件（R1-6）。完全修飾名を書くのはコードブロック内の `class=` 属性のみ。
4. **`style.md` S-07 の表記法はページ単位で決まる（S-07:241）。** 1つでも `list-table` が必要な表があるページは、短い表も `list-table` に揃える（R1-X1）。
5. **`.. important::` などで「〜すると実行時エラーになる」と書くときは、例外を投げる行だけでなく、その呼び出し元の早期 return 条件まで辿る。** R1-3 は、例外を投げる行（`EntityTestConfiguration.java:78-80`）だけを見て条件を一般化したことによる誤りだった。
