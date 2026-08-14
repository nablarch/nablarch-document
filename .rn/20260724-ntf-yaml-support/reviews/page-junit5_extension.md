# `setup/junit5_extension.rst`（JUnit 5用拡張機能）

`#27-02` のレビュー記録。対象は `mapping.csv` の `dest_page=JUnit 5用拡張機能` の17行（`MOVE` 16件・`MERGE` 1件、合計475行）。`REFERENCE`・`DROP` の行は無いため G11・G12 は該当なし。出典は `origin/develop` の `ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/JUnit5_Extension.rst` と同 `01_Abstract.rst` で、いずれも `#7` で削除済み。`git show 2e501ad:<path>` で読む。

## 出典行の消化

| `mapping_id` | 出典 | `lines` | `dest_section` | 反映先 |
|---|---|---:|---|---|
| `current-0178` | `01_Abstract.rst:671-688` | 18 | 機能概要 | 使用方法 > JUnit 4で書いたテストをJUnit 5上で実行する（`:182`・`:221-223`）。**節の割り当てを変えた**（下記「判断待ち」1） |
| `current-0179` | `01_Abstract.rst:691-695` | 5 | 機能概要 | 機能概要 > 前提事項（`:73`） |
| `current-0180` | `01_Abstract.rst:698-739` | 42 | 使用方法 | 使用方法 > JUnit 4で書いたテストをJUnit 5上で実行する（`:184-219`） |
| `current-0265` | `JUnit5_Extension.rst:14-22` | 9 | 機能概要 | リード文（`:10`）と 機能概要 の第1・第2段落（`:16`・`:18`） |
| `current-0266` | `:26-33` | 8 | 機能概要（`MERGE`） | 機能概要 の第3段落（`:20`）と tip（`:22-24`） |
| `current-0267` | `:37-47` | 11 | 使用方法 | 使用方法 > 依存関係を追加する（`:80-94`） |
| `current-0268` | `:51-97` | 47 | 使用方法 | 使用方法 > テストクラスに合成アノテーションを設定する（`:98-127`） |
| `current-0269` | `:101-144` | 44 | 使用方法 | 機能概要 > Extensionクラスと合成アノテーションの一覧（`:26-69`）。**節の割り当てを変えた**（下記「判断待ち」2） |
| `current-0270` | `:147-168` | 22 | 使用方法 | 使用方法 > BasicHttpRequestTestTemplateを使用する（`:129-147`） |
| `current-0271` | `:172-183` | 12 | 拡張例 | 拡張例 の導入文と3項リスト（`:227-233`） |
| `current-0272` | `:186-207` | 22 | 拡張例 | 拡張例 > 独自拡張クラスを作成する（`:235-254`） |
| `current-0273` | `:210-234` | 25 | 拡張例 | 拡張例 > 独自拡張用のExtensionクラスを作成する（`:256-275`） |
| `current-0274` | `:237-258` | 22 | 拡張例 | 拡張例 > ExtendWithでテストクラスに適用する（`:277-297`） |
| `current-0275` | `:261-342` | 82 | 拡張例 | 拡張例 > baseUriを渡す合成アノテーションを作成する（`:299-374`） |
| `current-0276` | `:345-369` | 25 | 拡張例 | 拡張例 > 事前処理・事後処理を実装する（`:376-393`） |
| `current-0277` | `:372-423` | 52 | 拡張例 | 拡張例 > JUnit 4のTestRuleを再現する（`:395-440`） |
| `current-0278` | `:427-455` | 29 | 使用方法 | 使用方法 > RegisterExtensionでExtensionクラスを適用する（`:149-176`） |

`mapping.csv` は無変更（作業指示 §1-4）。`verify_mapping.py` は `OK: no errors`（exit 0）。

## 実装で確認した事実

参照コミット: `nablarch/nablarch-testing` = `e21bf67`。`nablarch-testing-junit5` はローカルリポジトリが無いため、`~/.m2/repository/com/nablarch/framework/nablarch-testing-junit5/2.1.0/nablarch-testing-junit5-2.1.0-sources.jar` を展開して読んだ。以下の行番号はその展開結果のもの。

| 本文の記述 | 実装上の根拠 |
|---|---|
| インジェクションの対象は、生成したインスタンスを代入できる型で宣言されたフィールドすべてであり、可視性を問わず、スーパクラスで宣言されたフィールドも含む（`:121`） | `TestEventDispatcherExtension.java:61-82` の `postProcessTestInstance` が `ReflectionUtils.findFields(testInstance.getClass(), isInjectionTarget, HierarchyTraversalMode.BOTTOM_UP)` で候補を集め、各フィールドに `setAccessible(true)` してから代入する。判定条件は `:98-100` の `field -> field.getType().isAssignableFrom(supportClass)` |
| 該当するフィールドが複数ある場合はそのすべてに同じインスタンスが代入され、1つもない場合は何も起きない（`:121`） | 同 `:61-82`。`findFields` が返したリストを走査して代入するだけで、件数の検査は無い |
| 値が設定済みだと `IllegalStateException` が送出される（`:125`） | 同 `:64-81`。`field.get(testInstance) != null` のとき `throw new IllegalStateException(String.format("The %s field of %s is already set some value.", ...))` |
| `Object` 型のフィールドも対象に該当する（`:125`） | `:98-100` の判定は `isAssignableFrom` である。`Object.class.isAssignableFrom(TestSupport.class)` は `true` になる |
| `BasicHttpRequestTestExtension` は `RegisterExtension` では適用できない（`:151`） | `BasicHttpRequestTestExtension.java:16-23`。`createSupport` が `@BasicHttpRequestTest` を読み、無い場合は `IllegalStateException("%s is not annotated by %s.")` を送出する。`:25-30` で `annotation.baseUri()` を `getBaseUri()` の戻り値にする |
| `createSupport()` が返したインスタンスは `TestEventDispatcherExtension` の `protected` な `support` フィールドに保存され、サブクラスから参照できる（`:271`） | `TestEventDispatcherExtension.java:58` の `protected TestEventDispatcher support;` と `:61-82` の `support = createSupport(...)` |
| `TestEventDispatcherExtension` は「すべてのExtensionクラスのスーパクラス」である（`:271`） | 展開結果に対する `grep -rn 'class.*Extension extends'` のヒットは11件。うち9件が `extends TestEventDispatcherExtension`、`RestTestExtension` が `extends SimpleRestTestExtension`、`MessagingReceiveTestExtension` が `extends MessagingRequestTestExtension` で、いずれも1段挟んで `TestEventDispatcherExtension` に到達する |
| `findAnnotation` が取得できるのはテストクラスに直接設定されたアノテーションだけである（`:357`） | `TestEventDispatcherExtension.java:195-197`。実体は `testInstance.getClass().getAnnotation(annotationClass)` のみで、スーパクラスの探索も合成アノテーションの再帰探索も行わない |
| `nablarch-testing-rest` は推移的に解決されない（`:94`） | `nablarch-testing-junit5-2.1.0.pom:43-49`。`<scope>compile</scope>` かつ `<optional>true</optional>` で、`<!-- RestTestExtension, SimpleRestTestExtension を使う場合のみ必要 -->` のコメントが付く |
| `beforeAll` はテストクラス全体、`beforeEach` はテストメソッドごとに実行される（`:378`） | `TestEventDispatcherExtension.java:102-105` の `beforeAll` が `TestEventDispatcher.dispatchEventOfBeforeTestClassAndBeforeSuit()` を、`:112-116` の `beforeEach` が `support.dispatchEventOfBeforeTestMethod()` を呼ぶ |

## 出典から変えた点

| 出典 | 変更 | 理由 |
|---|---|---|
| `JUnit5_Extension.rst:101-144` の一覧が「使用方法」側の節にある | 「機能概要 > Extensionクラスと合成アノテーションの一覧」に置いた（`:26`） | `design.md:220-222` の第2部アウトラインが「主なクラスとリソース」の表を機能概要に置くと定めている。`mapping.csv` の `dest_section` と割れる点は下記「判断待ち」2 |
| `01_Abstract.rst:671-688`（JUnit Vintage の導入）が `dest_section=機能概要` | 「使用方法 > JUnit 4で書いたテストをJUnit 5上で実行する」に置いた（`:180`） | `design.md:150-180` が `current-0180`（Vintage の pom 記述）を第2部の使用方法に戻すと記録している。同じ話題の前半（`current-0178`）だけを機能概要に割ると節がまたがる。下記「判断待ち」1 |
| `:56` 「JUnit 5の `Extension` を利用している」／`:346` 「これを利用して」 | 「使用している」に改めた（`:18`・`:357`） | `.textlint/conf/prh.yml:16-22` が `利用` → `使用` を定める（`者`・`ケース` を除く） |
| `01_Abstract.rst:693-695` の見出し「前提条件」 | 「前提事項」にした（`:71`） | `glossary.md:309` の 正表記。同行が `前提条件` を揺れ表記として挙げている |
| `01_Abstract.rst:685` の 「移行の手順については `公式のガイド`」 | 「公式の移行ガイド」にした（`:223`） | 「公式のユーザガイド」（`:12`）と表示名が重なると Sphinx が `Duplicate explicit target name` の警告を出す。実測で確認した（是正前のビルドで 2 warnings、是正後 1 warning） |
| `JUnit5_Extension.rst:32` の「JUnit 5 自体についての情報は…参照のこと」が「機能概要」相当の位置にある | ページのリード文の直後（`:12`）に移した | `glossary.md:309` は 前提事項 を「適用できないケースを示す枠」と定めている。ページの記載範囲の宣言は前提事項ではない |
| `:436` 「必ず親クラスの…」ほか（`親クラス` 5箇所） | すべて「スーパクラス」にした（`:271`・`:386`・`:392`・`:425`・`:439`） | `glossary.md:321` が `スーパクラス` を 正表記、`スーパークラス` を揺れ表記と定める。出典の `親クラス` は同表の対象外だが、同じ概念に2語を使わないため揃えた |
| `JUnit5_Extension.rst:432-434` 「Extensionが正常に動作しなくなる」 | 「Extensionクラスが正しく動作しない」（`:172`）。同様に本文中の裸の「Extension」を「Extensionクラス」に統一した | ページ内で JUnit 5 の `Extension` インタフェース（`:18` の外部リンク）と本拡張機能の実装クラスの両方を指す語になっており、区別が付かない |
| `01_Abstract.rst:700-703` の「以下２つのアーティファクト」 | アーティファクト名の箇条書き（`:186-187`）を残し、地の文に `junit-bom` の役割を書いた（`:184`） | 出典は箇条書きでアーティファクト名を挙げていたが、コードブロックには `junit-bom` も含まれる。名前を挙げずに「次の2つ」とだけ書くと、コードブロックの3ブロックと数が合わない |
| — | `:184` に「JUnit VintageはJUnit 5が提供するプロジェクトであり、本拡張機能の一部ではない」を書き足した | この節だけが `01_Abstract.rst` 由来で、本拡張機能の使用手順ではない。節が「使用方法」の下にあるため、本拡張機能の一手順と読まれる |
| — | `:94` に `nablarch-testing-rest` が `optional` である旨と `:ref:`リクエスト単体テストの設定（RESTfulウェブサービス） <request_unit_test_setting_rest>`` を書き足した | 出典に記述が無いが、実装上必須の設定である（上表）。作業指示 §2「出典が欠いている、実装上必須の設定は書き足してよい」に従い、`file:line` を上表に記録した |
| — | `:121` にインジェクション対象の判定条件を、`:125` に `IllegalStateException` と `Object` 型フィールドの落とし穴を書き足した | 出典（`:80-83`）は「値を設定してはならない」とだけ述べ、対象の決まり方と例外の型を書いていない。上表の実装で裏付けた |
| — | `:151` に `BasicHttpRequestTestExtension` が `RegisterExtension` では適用できない旨を書き足した | 出典（`:429-430`）は「本拡張機能が提供するExtensionは RegisterExtension を使っても利用できる」と例外なしで述べるが、実装は例外を送出する（上表） |
| — | `:127` に `:ref:`テストクラスとテストデータの対応 <testdata_notation-file_structure>`` を張った | `support.getMap(sheetName, id)` の実装例（`:114`）にシート名とIDが現れるが、その対応規則は第3部の該当ページにある。`design.md:239-248`（「使い方」は第3部に置き第2部からは `:ref:` で参照する）に従った |
| `:390-402` のコード内コメント「4. 生成したリストを返却する」 | 「返す」にした（`:424`） | ページ内の他の記述（`:415` ほか）が「返す」で、同一ページ内で割れていた |
| `:272` のコードブロック冒頭の `..` | `...` にした（`:283`） | 同ページ内の他の省略記号（`:110`・`:112` ほか）が `...` で、2文字は誤記である |
| `:246` 「インスタンス変数」 | 「インスタンスフィールド」にした（`:289`） | ページ内の他の記述（`:100`・`:121`・`:271`）が「フィールド」で統一されている |
| `:186-207` の地の文「テスティングフレームワークが提供するクラスは、インスタンスの生成時にテストクラスの `Class` オブジェクトを渡す必要がある」 | 「基本的にインスタンスの生成時に…受け取る」にした（`:250`） | 直後の tip（`:254`）が `SimpleRestTestSupport` は不要と述べており、「必要がある」と断ずると矛盾する。出典（`:203`）も「基本的に」を含む |

## 4観点レビュー ラウンド1

QA（網羅性）／設計（構成）／クラフト（文章）／検証（実装との一致）を、それぞれ別のサブエージェントで実施した（`steering.md` `Rules`）。依頼プロンプトには3点（実測コマンドで裏付ける／付属の検証スクリプトを正解にしない／敵対的にレビューする）を入れた。

判定: **4観点とも FAIL**。重複を除いた `must` は4件。指摘の事実関係は、採用したものすべてについて実装・規約ファイル・ビルド出力を自分で開いて確認した（上の2表が確認結果）。

### 是正した指摘

| # | 観点 | 指摘 | 是正 |
|---|---|---|---|
| R1-1（`must`） | 検証 | `:145`（当時）の「本拡張機能が提供するExtensionクラスは `RegisterExtension` で適用することもできる」が例外なしで書かれている。`BasicHttpRequestTestExtension` は合成アノテーションが無いと例外を送出する | `:151` に例外を書き足した（上表） |
| R1-2（`must`） | 検証 | `nablarch-testing-rest` が `optional` で推移的に解決されないのに、tip が `nablarch-testing` への依存だけを述べている | `:94` に段落を足し、RESTful の設定ページへ導線を張った（上表） |
| R1-3（`must`） | 検証・QA | `:117`（当時）の「代入可能なフィールドを見つけてインジェクションする」が、対象の決まり方・複数該当時の挙動・0件時の挙動を述べていない | `:121` を書き直した（上表） |
| R1-4（`must`） | 検証・クラフト | `:121`（当時）の「拡張機能は例外を送出してテストを終了させる」が、例外の型を伏せ、かつ「終了させる」が実際の結果（テストの失敗）とずれる | `:125` を「Extensionクラスは `IllegalStateException` を送出し、そのテストは失敗する」に改め、`Object` 型フィールドの落とし穴を足した |
| R1-5（`should`） | クラフト | L3見出しの下線が13本とも50文字で、既存の承認済みページ（`setup/master_data_restore.rst` の6本、`setup/request_unit_test/rest.rst` の3本ほか）の49文字と割れている | 13本とも49にした。`git ls-files '*.rst'` 配下の `^~~~~` を実測すると、このページを除いて 49 が41本・50 が37本で、50側の内訳は `implementation/testdata_examples.rst` の24本が大半を占める。`#27` で作った `master_data_restore.rst` に合わせて49を採った |
| R1-6（`should`） | クラフト | `:18`（当時）の `**Extensionクラス**`・`**合成アノテーション**` が太字になっている | 落とした（`:20`）。`style.md:483-505` は太字ラベルを Excel/YAML の形式別ラベルに限る旨を定めており、用語の強調に使う先例が無い |
| R1-7（`should`） | 設計 | `:73`（当時）のページ記載範囲の宣言が「前提事項」の節にある | リード文の直後（`:12`）に移した（上表） |
| R1-8（`should`） | クラフト | `:125`（当時）の「それ以外は…と同じである」の「それ以外」が何を指すか読めない | 「`baseUri` の指定以外の手順は」にした（`:131`） |
| R1-9（`should`） | クラフト | `:131`（当時）のクラス名だけ `YourTestClass` で、他の実装例（`:104`・`:149`・`:277`・`:354`）は `YourTest` | `YourTest` に揃えた（`:139`） |
| R1-10（`should`） | 設計・QA | `:218-222`（当時）の導入文が3項リストで閉じており、その後に続く3つのL3（`baseUri` の合成アノテーション・事前処理と事後処理・`TestRule`）を予告していない | `:233` に1文を足した |
| R1-11（`should`） | 検証 | `:176`（当時）が JUnit Vintage を本拡張機能の機能のように読ませる | `:184` に「JUnit 5が提供するプロジェクトであり、本拡張機能の一部ではない」を足した |
| R1-12（`should`） | クラフト | `:239`（当時）の「`Class` オブジェクトを渡す必要がある」と直後の tip が矛盾する | 「基本的に…受け取る」にした（`:250`）。出典にも「基本的に」がある |
| R1-13（`should`） | 検証 | `:346`（当時）の `findAnnotation` の説明が、直接設定されたアノテーションしか取れないことに触れていない | `:357` に書き足した（上表） |
| R1-14（`info`） | クラフト | `利用` が2箇所ある | `使用` にした（`:18`・`:357`） |
| R1-15（`info`） | クラフト | `親クラス` が5箇所ある | `スーパクラス` にした（上表） |
| R1-16（`info`） | クラフト | `:367`（当時）のメソッド列挙が `beforeAll`・`beforeEach`・`afterAll`・`afterEach` の順で、直後の説明文の並び（クラス全体→メソッドごと）と合わない | `beforeAll`・`afterAll`・`beforeEach`・`afterEach` にした（`:378`） |
| R1-17（`info`） | クラフト | 外部リンクの表示名が「公式のユーザガイド」「公式ガイドの…」「公式のガイド」で割れている | 「公式のユーザガイド」を基準に揃えた（`:12`・`:24`・`:176`）。移行ガイド（`:223`）だけは同名になるとビルド警告が出るため「公式の移行ガイド」とした |
| R1-18（`info`） | クラフト | コードブロック内の `..`、「Extension」の裸使い、「インスタンス変数」、「返却する」 | いずれも上表のとおり直した |
| R1-19（`info`） | QA | `:271`（当時）が `support` フィールドの型・可視性を書いていない | `TestEventDispatcher` 型・`protected` を明記した（`:271`） |

### 対応せず記録に留めた指摘

| # | 観点 | 指摘 | 対応しない理由 |
|---|---|---|---|
| R1-20 | QA | 依存関係の節に `junit-jupiter`（JUnit 5本体のエンジン）の追加手順が無く、`nablarch-testing-junit5` だけでは JUnit 5 のテストが実行されない。指摘には `mvn dependency:tree` の実測が添えられていた | ページの記載範囲外である。`:12` が「JUnit 5そのものの導入方法…は、このページでは説明しない」と宣言しており、その宣言は出典（`JUnit5_Extension.rst:32`）に由来する |
| R1-21 | 検証 | `resolveTestRules()` で再現される `TestRule` は `Description` から情報を受け取るものに限られる。`TestEventDispatcherExtension.java:44-49` の `NOOP_STATEMENT` に各ルールを適用し、`:122-136` の `emulateTestRules` がそれを `beforeEach`（`:112-116`）で評価するだけで、テスト本体はルールを通らない。出典（`JUnit5_Extension.rst:376-390`）が例に挙げる `Timeout` は機能しない | **本文に書いていない。** 下記「判断待ち」3に回す。作業指示 §2 の「本体の不具合が疑われる場合は書かずに `decide` に上げる」に該当する |
| R1-22 | 検証 | `RegisterExtension` をインスタンスフィールドで宣言した場合、`beforeAll`・`afterAll` に加えて `postProcessTestInstance` も呼ばれず、`support` が未設定のまま `NullPointerException` になる | JUnit 5 側の仕様であり、一次情報（ユーザガイドの本文）を自分で確認できていないため **未確認**。出典（`JUnit5_Extension.rst:433`）の範囲に留め、「`beforeAll` や `afterAll` などの処理が実行されず、Extensionクラスが正しく動作しない」（`:172`）とした |
| R1-23 | 設計 | 節順が「BasicHttpRequestTestTemplateを使用する」→「RegisterExtensionでExtensionクラスを適用する」で、汎用の話が個別の話の後に来る | 出典（`JUnit5_Extension.rst:147` と `:427`）の順を保った。`RegisterExtension` は出典でも最後に置かれた補足である |
| R1-24 | クラフト | `style.md:343` のページ一覧が「JUnit 5用拡張機能（スタブ）」のままである | 規約ファイルは変更しない（作業指示 §1-3）。下記「判断待ち」4に回す |
| R1-25 | QA | `maven-surefire-plugin` 2.22.0 という閾値の一次情報（surefire 側のリリースノート等）を確認できない | 出典（`01_Abstract.rst:695`）にそのまま書かれている記述であり、出典を示せる。surefire 側の一次情報は **未確認** |

## ゲート

`checks/task-27.md` の `#27-02` の節に記録した。

## 判断待ち（`decide`）

1. **`current-0178` の `dest_section` と実際の配置が割れている。** CSV は `機能概要`、ページ上は 使用方法 > JUnit 4で書いたテストをJUnit 5上で実行する（`:180`）。同じ話題の後半 `current-0180` が `使用方法` で、`design.md:150-180` もそれを 第2部 使用方法 に戻すと記録している。前半だけを機能概要に割ると節が2つにまたがる。`mapping.csv` は変更していない（§1-4）。CSV 側を `使用方法` に直すか、ページを分けるかの判断が要る。
2. **`current-0269` の `dest_section` と実際の配置が割れている。** CSV は `使用方法`、ページ上は 機能概要 > Extensionクラスと合成アノテーションの一覧（`:26`）。`design.md:220-222` が「主なクラスとリソース」の表を機能概要に置くと定めており、この表はそれに当たる。`mapping.csv` は変更していない。
3. **`resolveTestRules()` で再現できる `TestRule` に制約がある。** R1-21 のとおり、テスト本体はルールを通らないため、`Timeout` のようにテスト本体の実行を制御するルールは機能しない。出典（`JUnit5_Extension.rst:376-390`）はその `Timeout` を例に挙げており、`TestEventDispatcherExtension` の Javadoc（`:149-168`）も制約に触れていない。本体の不具合か、出典の実装例の誤りかの判断が要る。判断が付くまで、ページは出典どおり `Timeout` の例を載せ、制約には触れていない（`:395-440`）。
4. **`style.md:343` が「JUnit 5用拡張機能（スタブ）」のままである。** `#27-02` でスタブを外したので、規約側の表記を更新する必要がある。§1-3 により本作業では変更していない。
5. **`maven-surefire-plugin` 2.22.0 の閾値は出典由来で、surefire 側の一次情報を確認していない。** ページ（`:73`）は出典（`01_Abstract.rst:695`）に忠実。
