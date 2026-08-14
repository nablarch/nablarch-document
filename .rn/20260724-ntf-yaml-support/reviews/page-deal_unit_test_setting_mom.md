# `setup/deal_unit_test/mom.rst`（取引単体テストの設定（MOMによるメッセージング））

`#26` のレビュー記録。対象は `mapping.csv` の `dest_page=取引単体テストの設定（MOMによるメッセージング）` の行（元は `current-0158` の1行、出典 `origin/develop` の `ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/send_sync.rst:280-383`）。`#25` の user review の回答1 に従って出典を3分割したため、本タスクの成果物は `setup/deal_unit_test/mom.rst` と `setup/common.rst` の追加分の2つにまたがる。

## 出典の分割（`current-0158` → `-a`／`-b`／`-c`）

| `mapping_id` | 出典の範囲 | `lines` | `dest_page` | 内容 |
|---|---|---:|---|---|
| `current-0158-a` | `:280-297` | 18 | 取引単体テストの設定（MOMによるメッセージング） | 導入文（テスト用のプロファイルに設定する／環境ごとの切り替え／アーキテクトが行う）とモックアップクラスの設定 |
| `current-0158-b` | `:298-360` | 63 | 共通設定 | Excelファイルの配置場所の設定（`sendSyncTestData`・配置イメージ画像・`file:` スキーム推奨の tip）とテストデータ解析クラスの設定（`messagingTestDataParser`） |
| `current-0158-c` | `:361-383` | 23 | 共通設定 | 必要な単体テストライブラリの `pom.xml` への追加 |

行範囲の和集合は `:280-383` で隙間・重複なし（18 + 63 + 23 = 104）。`verify_mapping.py` は 597行 / 12,986 / 11,983 で `exit 0`。

**`-b` を `共通設定` に置いた根拠**（`#25` の回答1）。この2つの設定を必要とするのは取引単体テストのうち `HTTPメッセージング` と `MOMによるメッセージング` の2処理方式である。`SendSyncSupport` を生成するのは `MockMessagingClient.java:54`（HTTPメッセージング）と `MockMessagingContext.java:52`・`:93`（MOM）の2クラスだけで、リクエスト単体テスト側は `RequestTestingSendSyncSupport` を通る別経路である（`nablarch/nablarch-testing` = `e21bf67` を `git grep 'new SendSyncSupport' -- src/main` で実測）。`design.md:192` が共通設定の範囲に「テストデータの配置」を挙げていることが直接の根拠であり、節の見出しで適用条件（同期応答メッセージ送信）を名乗ることで、全処理方式に必要だと読ませないようにした。

**`-c` を `共通設定` に置いた判断**（本タスクで確定）。`nablarch-testing` はテスト種別・処理方式によらず必要であり、MOMの取引単体テストのページにだけ置くと、他のページの読者が依存関係の追加手順に到達できない。第2部の表題は「テスティングフレームワークの導入と設定」であり、依存関係の追加は「導入」に当たる。処理方式固有のモジュール（`nablarch-testing-rest` 等）は従来どおり該当ページに置く（`setup/request_unit_test/rest.rst:15-42`）。

## 実装で確認した事実

参照コミット: `nablarch/nablarch-testing` = `e21bf67`（読み方は `git -C /home/tie303177/work/nablarch/nablarch-testing show e21bf67:<path>`）。`nablarch/nablarch-testing-yaml` はブランチ `feature/ntf-yaml` の作業ツリー。

| 本文の記述 | 実装上の根拠 |
|---|---|
| `MockMessagingProvider` はテスティングフレームワークが提供するモックアップクラスである | `src/main/java/nablarch/test/core/messaging/MockMessagingProvider.java:14`・`:20-22`（`implements MessagingProvider`、`createContext()` が `MockMessagingContext` を返す） |
| キューへのアクセスは行われず、テストデータに記述した内容から応答電文が生成されて返される | `MockMessagingContext.java:20-22`（クラスJavadoc「本クラスを使用する場合、キューへのアクセスは行われない」）、`:41-80`（`sendSync` に送信処理が無く、`:91-114` の `createReceivedMessage` がテストデータのバイナリから応答電文を組み立てて返す） |
| コンポーネント名は `messageSender.<リクエストID>.messagingProviderName` に指定した名前で解決される | `nablarch-fw-messaging` の `MessageSenderSettings.java:239`（`messagingProvider = getComponent("messagingProviderName", SettingType.BOTH, required=true)`）、`:104`・`:113`（Javadoc「MessagingProviderをリポジトリから取得する際に使用するコンポーネント名」）。`MessageSender.java:134` の `settings.getMessagingProvider().createContext()` がその値を使う（`~/.m2/repository/com/nablarch/framework/nablarch-fw-messaging/2.1.0/nablarch-fw-messaging-2.1.0-sources.jar` を展開して確認） |
| テストデータの配置場所を `sendSyncTestData` というキーに設定する | `SendSyncSupport.java:49`（`SEND_SYNC_TEST_DATA_BASE_PATH = "sendSyncTestData"`）、`:346`・`:348`（`FilePathSetting#getBaseDirectory`／`#getFileIfExists` に渡す） |
| 設定していない場合はテストの実行時に例外が発生する | `SendSyncSupport.java:350-353`（テストデータが見つからないと `IllegalStateException`）、`:416-419`（`SystemRepository.get("messagingTestDataParser")` が `null` なら `IllegalStateException`）。ベースパス未設定は `FilePathSetting.java:144-149` の `getBasePathUrl` が `IllegalArgumentException`（`nablarch-core-2.2.1-sources.jar`） |
| どちらもテスティングフレームワークのデフォルト設定には含まれない | `nablarch-testing-default-configuration-6u3.jar` を展開し全ファイルを走査。`sendSyncTestData`・`messagingTestDataParser`・`filePathSetting` のいずれも**0件**（`grep -ral`） |
| Excel形式では、テストデータの拡張子を `fileExtensions` に設定する | `FilePathSetting.java:111-136` の `resolvePath` が、論理名に対応する拡張子が設定されている場合にファイル名へ結合する。`PoiXlsReader.java:55-65` は読み込み単位の名前を「ファイル名/シート名」に分け、`<ベースパス>/<リクエストID>.xls` または `.xlsx` を開く |
| YAML形式では `fileExtensions` に `sendSyncTestData` を設定しない。設定するとテストデータが見つからず例外になる | `YamlLoader.java:81-85` がファイルパスを `<ベースパス>/<リソース名>.yaml` として組み立てる（リソース名は `SendSyncSupport.java:347` の `<リクエストID>/message`）ため、実体はリクエストIDと同じ名前の**ディレクトリ**である。`resolvePath` が拡張子を結合すると `<ベースパス>/<リクエストID>.yaml` を探して存在せず、`SendSyncSupport.java:350` の `IllegalStateException` になる。**実際に動かして確認した**（下記「実行して確認した結果」） |
| YAML形式では `messagingTestDataParser` に `YamlTestDataParser` を登録し、`testDataReader` は指定しない | `YamlTestDataParser.java:43`（`extends BasicTestDataParser`。`SendSyncSupport.java:416` の受け型と一致）、`:71-74`（`setTestDataReader` は何もしない）、`:161-167`（`getMessageWithoutCache` のオーバーライド）、`YamlSection.java:214-223`（同期応答メッセージ送信で使う4つのデータタイプをすべて YAML のキーに対応づける） |

### 実行して確認した結果（YAML形式の `fileExtensions`）

`nablarch-testing` と `nablarch-testing-yaml` の `target/classes` と Maven のクラスパスを使い、`filePathSetting`（`sendSyncTestData` のベースパスのみ）と `messagingTestDataParser`（`YamlTestDataParser`）を登録したコンポーネント設定を読み込んで、`new SendSyncSupport().getResponseMessageBinaryByRequestId(DataType.RESPONSE_BODY_MESSAGES, "REQ001")` を実行した。テストデータは `<ベースパス>/REQ001/message.yaml` に `response_header_messages:`／`response_body_messages:` を置いた。

| `fileExtensions` の `sendSyncTestData` | 結果 |
|---|---|
| `yaml` を設定 | `IllegalStateException: test data file was not found. request id=[REQ001], ...` |
| 設定しない | 成功（14バイト・`0000RESULT_DAT` を取得） |

## 出典から変えた点

| 出典 | 変更 | 理由 |
|---|---|---|
| `:313` の配置場所の値 `file:///C:/nablarch/workspace/Nablarch_sample/test/message` | `file:/path/to/test/message` に置き換えた | Windows の絶対パスは環境依存で、そのまま使えない。FW解説書の記述例も `file:/var/nablarch/input` の形である（`libraries/file_path_management.rst:73`） |
| `:370-382` の `<exclusions>`（`org.mortbay.jetty`・`com.google.code.findbugs`） | 落とした | `nablarch-testing` 2.2.0（`e21bf67` の `pom.xml`）に両者の依存がいずれも無く、除外設定が陳腐化している（`grep -i 'mortbay\|jetty\|findbugs'` のヒットは `:200` のテスト除外設定のみ）。`design.md` §8「陳腐化した例示は落としてよい」を適用した。`<scope>test</scope>` は実プロジェクトの記述に合わせて足した（`nablarch-example-batch/pom.xml:124-128`） |
| `:308-324` の `filePathSetting` の `format` エントリ | コードブロックには残し、地の文で「同じコンポーネントに、電文のフォーマット定義ファイルの配置場所（`format`）も設定する」と述べた | 同期応答メッセージ送信では `MessageSenderSettings.java:258-273` が `formatDir`（デフォルトの論理名は `format`）のベースディレクトリを引くため、実際に必要な設定である |
| `:345` の `<component name="xlsReaderForPoi" ...>` | `name` 属性を落とした | 入れ子のコンポーネントに名前を付けてもこの設定では参照しない。既存の承認済みページ（`setup/class_unit_test.rst:132-143`）も同じ形である |
| `:286` `モックアップクラスの設定`／`:301` `Excelファイルの配置場所の設定`／`:336` `テストデータ解析クラスの設定`／`:364` `必要な単体テストライブラリのpom.xmlへの追加` の見出し | 「〜する」形式に改め、`:301` と `:336` は `共通設定` の1セクション（`同期応答メッセージ送信のテストデータの読み込みを設定する`）にまとめた | `style.md` S-03（セクションタイトルは「〜する」形式）。2つの設定はどちらも欠けるとテストが動かず、常にセットで行うため、1つのL3にまとめて `style.md` S-10 規約3 の形式別L4対を1組だけ置く形にした |
| `:299` のラベル `send_sync_test_data_path` | 引き継がず、`testing_framework_common-send_sync_test_data` を新設した | 削除済みの現行解説書の外部被参照ラベルではない（`ja/` 配下に参照0件。`checks/task-07.md`「リンク切れになる参照」の3件にも含まれない）。`style.md` S-08 の命名規則に従った |

## 4観点レビュー ラウンド1

観点A（網羅性）／B（トンマナ）／C（用語）／D（整合性）を、それぞれ別のサブエージェントで実施した。依頼プロンプトには Rules の3点（実測で裏付ける／付属の検証スクリプトを正解にしない／敵対的にレビューする）を入れた。

判定: **A FAIL（`must` 1）／B FAIL（`must` 2）／C FAIL（`must` 1）／D FAIL（`must` 2）**。重複除去後の `must` は5件、`should` は9件、`info` は8件。

### 是正した指摘

| # | 観点 | 指摘 | 是正 |
|---|---|---|---|
| R1-1（`must`） | A-1・D-1 | `YamlTestDataParser` は `nablarch-testing` に無く、別モジュール `nablarch-testing-yaml` が提供する。依存関係を書いたページが解説書に存在せず、`common.rst` の tip の「必要なモジュールは該当するページに記載している」も事実に反する | `common.rst:28-37` に `nablarch-testing-yaml` の追加手順を書いた。`design.md` §8「出典が欠いている、実装上必須の設定の追記」および `design.md:176`（YAML形式の `nablarch-testing-yaml` は当該ページに記載する）に従う。座標は `nablarch-testing-yaml/pom.xml:14-16` で確認 |
| R1-2（`must`） | B-2 | 両形式で共通の `messagingTestInterpreters` の定義が「Excel形式の場合」の中だけにあり、YAML形式のコードブロックがそれを `ref` で参照していた。YAML形式しか読まない読者が自分の側だけを写すと、未定義のコンポーネントを参照する設定になる | 定義をL4対より前の共通部（`common.rst:126-141`）へ移した。各L4は `filePathSetting` と `messagingTestDataParser` の差分だけを示す形にした |
| R1-3（`must`） | B-1・D-3 | `style.md` S-11 に反し、L4見出しを持つL3の導入文が、配下にどのL4があるかを示していない | `common.rst:143` に「ベースディレクトリの指定と、テストデータを解析するコンポーネントの設定は、テストデータの形式によって異なる。Excel形式とYAML形式のそれぞれについて後述する。」を追加 |
| R1-4（`must`） | C-1 | `同期応答メッセージ送信`（MOM側の正表記）を HTTPメッセージングにも掛けていた。`glossary.md:158` は HTTP 側の正表記を `HTTPメッセージ送信` と定め、§8（`glossary.md:532`）は混ぜた表記を無条件で置換すると定めている | 節見出し・リード文・本文・両ページの `:ref:` のリンク文字列を「同期応答メッセージ送信・HTTPメッセージ送信」に改めた。この併記形は承認済みの `implementation/testdata_notation.rst:497` に実在する |
| R1-5（`must`） | A-3・B-3・D-2 | リード文が「テストの種類によらず共通に行う設定」と述べたうえで、適用範囲が2処理方式に限られる節を並べており、同一ページ内で矛盾していた。あわせて内部設計文書の語 `テスト種別` を持ち込んでいた（`ja/` 配下で本行のみ） | `common.rst:10` を書き直し、条件付きの節を「あわせて、同期応答メッセージ送信・HTTPメッセージ送信を伴う取引単体テストだけが必要とする」と分けて述べた。`テスト種別` は `テストの種類`（`about/index.rst:52` の節題）に改めた |
| R1-6（`should`） | D-4 | `fileExtensions` に `xlsx` だけを示していたが、承認済みの `implementation/testdata_examples.rst:1810` は同じ配置場所のファイルを `REQ001.xls` として示す。`FilePathSetting` は1キー1拡張子で解決するため、両ページどおりに作ると読み込みに失敗する | `common.rst:179` を「テストデータのファイルの拡張子（`xlsx` または `xls`）を指定する」に改めた |
| R1-7（`should`） | A-2 | `messagingProviderName` は `SettingType.BOTH` で参照され、リクエストID別の設定が無ければ `messageSender.DEFAULT.messagingProviderName` にフォールバックする（`MessageSenderSettings.java:239`・`:104`・`:113`） | `mom.rst:29` に DEFAULT の1文を追加した |
| R1-8（`should`） | A-4 | 出典 `:281-282` の「テスト用のプロファイルに設定する／環境ごとの切り替え」は4つの設定すべてを覆う導入文だったが、分割後は `mom.rst` にしか導線が無く、`common.rst` の節と HTTPメッセージングのページには届いていなかった | `common.rst:122` の末尾に切り替え方法への `:ref:` を追加した |
| R1-9（`should`） | D-5 | 依存関係の tip が「これに加えて専用のモジュールが必要」と書いていたが、RESTページは「3つを追加すれば `nablarch-testing` の API も使える」と述べており、`nablarch-testing` を直接宣言しない構成である。読者が4つ書くのか3つでよいのか判断できない | tip（`common.rst:41`）を「専用のモジュールが `nablarch-testing` に依存する場合は、`nablarch-testing` を個別に追加しなくてよい」に書き直した |
| R1-10（`should`） | C-2 | `messagingTestDataParser` の呼び方が「テストデータを解析するコンポーネント」「解析クラス」「テストデータ解析クラス」の3通りに割れていた。承認済みは `setup/class_unit_test.rst:108` の「テストデータを解析するコンポーネント」 | 本文・XMLコメント・両ページの参照文を「テストデータを解析するコンポーネント」に統一した |
| R1-11（`should`） | C-4 | `sendSyncTestData` に設定する値を、承認済みページは `ベースディレクトリ`（`testdata_notation.rst:1154`・`testdata_examples.rst:1802`）と呼ぶのに対し、本文は `配置場所` と呼んでいた | 全件を `ベースディレクトリ` に改めた |
| R1-12（`info`） | C-6・B-7 | 図の導入が「配置イメージを次に示す」で、`ja/` 配下に用例が無い。また図が示す「リクエストIDごとに1ファイル」が本文から読み取れない | 「ベースディレクトリの配下は次の図のとおりで、リクエストIDごとに1つのファイルを置く。」に改めた（`about/index.rst:106` の「次の図のとおり」に合わせた） |
| R1-13（`info`） | C-7 | 地の文の `Excel形式` が素の表記で、`ja/` 配下の多数派（`\ Excel\ 形式`、61件対4件）と異なる | 地の文をエスケープ形に統一した（見出し `Excel形式の場合` は `testdata_examples.rst` の反復見出しと同じく素のまま） |
| R1-14（`should`） | D-6 | `volume.md` の傾向記述が本タスクの変更で陳腐化した（最小ページが入れ替わった） | `volume.md:91` に1文を追記した |

### 対応せず記録に留めた指摘

| # | 観点 | 指摘 | 対応しない理由 |
|---|---|---|---|
| R1-15 | C-5（`should`） | `mom.rst:21` の「キューへのアクセスは行われず」が、対の `http_messaging.rst:21`「メッセージの送信は行われず」と揃っていない | 実装に忠実な記述である（`MockMessagingContext.java:21`「本クラスを使用する場合、キューへのアクセスは行われない」）。MOM はプロバイダ層で差し替わるため、置き換わる対象が両ページで異なる。語を揃えると実装と離れる |
| R1-16 | B-5（`should`） | YAML形式の「リクエストIDと同じ名前のディレクトリを参照する」の説明先が無い | 参照先の共通部（`testdata_notation.rst:1154`）が「Excel形式ではリクエストIDと同じ名前のファイルの `message` シート、YAML形式ではリクエストIDと同じ名前のディレクトリ配下の `message.yaml`」と両形式を書いている。指摘が見ていたのは同ページのYAML形式のL4であり、導線は成立している |
| R1-17 | B-6（`info`） | L4のアンダーラインが49で、`testdata_examples.rst`（50）と異なる | `style.md` S-04 は表示幅以上を求めるのみで、いずれも適合。`testdata_notation.rst` の `^` 31件はすべて49であり、ページをまたぐ統一は既存資産にも無い |
| R1-18 | A-8（`info`） | `YamlTestDataParser` の `:java:extdoc:` はリリースまでリンク切れになる | `nablarch-testing-yaml` 自体が未リリースであり、本解説書はリリース後の状態を書いている。承認済みページも `@Published` でないクラスに `:java:extdoc:` を張っている（`http_messaging.rst:21` の `MockMessagingClient`） |
| R1-19 | D-8・D-9（`info`） | `common.rst` と2つのモックアップページが相互参照になっている／`sendSyncTestData` の前提が3ページに現れる | 各方向に固有の情報があり、行き来するだけのリンクではない。第3部の2件はファイル名規則を説明するための最小限の再掲である |

### 是正後の確認

- Docker フルビルド（`-a`）は `build succeeded, 1 warning.`。警告は既知の `db_double_submit.rst:108` のみで新規0件、`duplicate label` 0件
- 生成HTMLで、`common.html` の目次に新しいL3とL4対が並び、`mom.html`・`http_messaging.html` からの `:ref:` が `common.html#testing-framework-common-send-sync-test-data` に解決することを確認した
- 見出し下線（表示幅以上）・段落内の改行0件・用語の走査（`テスト種別`・`解析クラス`・`配置場所`・`配置イメージ` の各0件）を再実行して確認した

## 検証ラウンド（是正差分のみ）

是正差分に限定した検証観点を別のサブエージェントで1回実施した（`steering.md` `#10` の共通 Steps「是正ラウンド2以降は、是正差分に限定した検証観点のみを回す」に従う）。依頼プロンプトには Rules の3点を入れた。

判定: **PASS（`must` 0件・`should` 2件・`info` 5件）**。是正の範囲は逸脱なし（`git status --porcelain -uall` の全件が本作業の9エントリ、`ja/` 配下の削除行は `common.rst` のリード文1行のみで R1-5 の意図どおり）。`mapping.csv`・`_batch/batch-25.csv` は difflib で照合し、`current-0158` の1行が3行に置き換わっただけで他行は完全一致であることを確認した。

| # | 種別 | 指摘 | 対応 |
|---|---|---|---|
| V-1 | `should` | R1-2 の是正が防ごうとした失敗モードが残っている。目次（`:depth: 3`）からL4へ直接飛べるため、`YAML形式の場合` だけを見た読者には `ref="messagingTestInterpreters"` の定義が見えない | 両方のL4に「``interpreters`` には、前掲の ``messagingTestInterpreters`` の定義とあわせて記述する。」を追加した（`common.rst:179`・`:211`） |
| V-2 | `should` | 拡張子の不整合が閉じ切っていない。承認済みの `implementation/testdata_examples.rst:1810` は同じ配置場所のファイルを `REQ001.xls` と示すため、両ページを字義どおりに写すと読み込みに失敗する | `common.rst:181` を「実際に配置するテストデータのファイルの拡張子（``xlsx`` または ``xls``）を指定する。指定した拡張子と一致しないファイルは読み込まれない。」に改めた |
| V-3 | `info` | `common.rst:122` の `:ref:` 2件のリンク文字列が飛び先の見出しと不一致（`HTTPメッセージング` / `MOMによるメッセージング`） | 承認済みページに同型の先例が5件あり規約違反ではない（`request_unit_test/rest.rst:42` ほか）。処理方式名で読ませる方が文が短く読みやすいため現状維持 |
| V-4 | `info` | `style.md` S-10 規約1 の2類型に「両形式で同一の設定」が入っていない | 規約3の太字ラベル例外の第2項が「形式別のL4対を持つL3の共通部」を前提にしており、共通部を持つこと自体は想定されている。規約の類型追加は `#pre-last` の候補として記録に留める |
| V-5 | `info` | S-11 の「後述する」文の直後に `tip` が挟まる | `tip` は両形式に共通する推奨事項であり、L4より前に置くのが正しい。順序は変更しない |
| V-6 | `info` | `volume.md:91` の「最小はこのページ」は、0行のページ（EXPECTED_ZERO 3件）を除いた非0行中の最小 | 数値は全件正確であることを検証側も確認済み。文意が通るため現状維持 |
| V-7 | `info` | 依存関係の節が `nablarch-testing-default-configuration` に触れていない | 出典に無く、必要なページ（`setup/request_unit_test/rest.rst:27-32`）が挙げている。tip が各ページへ誘導する |

### 検証ラウンドが独立に確認した事実（いずれも本文と一致）

- `nablarch-testing-yaml` の座標（`nablarch-testing-yaml/pom.xml:14-15`）と、`YamlTestDataParser` が `nablarch-testing` 側に存在しないこと
- tip の書き直しが `setup/request_unit_test/rest.rst:15-42` と矛盾しないこと（`nablarch-testing-rest` は `nablarch-testing` へ compile 依存）
- `messageSender.DEFAULT.messagingProviderName` のフォールバック（`MessageSenderSettings.java:239`・`:304`・`:675-680`）
- デフォルト設定（`nablarch-testing-default-configuration-6u3.jar` の33ファイル）に `sendSyncTestData`・`messagingTestDataParser`・`filePathSetting` が0件で、デフォルト設定が持つ `interpreters`・`testDataParser` とも名前が衝突しないこと
- 画像の配置が `design.md:897` の規約に適合し、`en/` 側が無傷であること
- 3ページとも docutils の `system-message`／`problematic` が0件で、見出し下線が全件表示幅以上であること

### 検証ラウンド後の再ビルド

V-1・V-2 の是正後に Docker フルビルド（`-a`）を再実行し、`build succeeded, 1 warning.`（既知の `db_double_submit.rst:108` のみ・新規0件）。ビルド直後に `sphinx.mo` を復元した。
