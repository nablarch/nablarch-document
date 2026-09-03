# NTF 解説書 刷新版 レビューガイド

チームメンバー・TL が刷新版をレビューするための申し送りです。読むのは刷新版の HTML で、本書は v6 から判断で変えたことと、その理由だけを伝えます。

## 進め方

- 読むものは刷新版の HTML 38 ページです（配布方法は別途連絡）。比較する相手は [v6 の公開解説書](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/index.html) で、各ページに元の v6 ページを書いてあります
- まず「全体で判断してほしいこと」に答え、次に担当ページの申し送りを読み、変えた箇所を刷新版で開いて判断してください
- 分担は、TL が全体と第1部、メンバーが担当領域です。第2部の設定と第3部の実装は処理方式ごとに対になっています
- コメントは [PR #728](https://github.com/nablarch/nablarch-document/pull/728) のレビューコメントに、該当行へ付けてください。ページ全体への意見は「Files changed」のファイル先頭行へ
- 用語の統一・JUnit 5 化・図の差し替え・表の折り返しなどの横断的な変更はページ別には書いていません。下の「全体で変えたこと」で 1 回だけ判断してください

## 全体で変えたことと理由

- 47 ページを 4 部構成 38 ページに組み直した（とは／導入と設定／テスト実装／ツール）
  - v6 は設定と実装手順が同じページに混在していたため
- JUnit 5 を標準にし、JUnit 4 は「JUnit 4での使用」1 ページに集約した
  - ブランクプロジェクトが JUnit 5 構成のため
- 横断の設定を「導入」「テストデータの設定」「システム日時と採番の固定」の 3 ページに集めた
  - v6 は方式別ページに散っていたため
- 実装と食い違う記述は実装に合わせ、陳腐化した例示は落とした
- 「間違えたときにどうなるか」の注意は書かない基準にした
- 用語を統一した
  - 自動テストフレームワーク → テスティングフレームワーク
  - テストケース → テストショット
  - スーパークラス → スーパクラス
- 内部構造のクラス図と Excel のスクリーンショットを落とし、構成図・シーケンス図 21 枚を新しく描いた
- テストデータの YAML 形式を Excel 形式と対で併記した
  - AI エージェントが生成・解析できるようにするため
- 表を折り返しにした
  - Excel シートを再現した 10 表は横スクロールのまま
- `:download:` のサンプルファイル 10 本を落とした
  - 実ファイルが失われていたため

## 全体で判断してほしいこと

1. JUnit 5 を標準にし JUnit 4 を 1 ページに寄せた位置づけでよいか。JUnit 4 で書き続けるプロジェクトが、第3部の例を継承方式に読み替えられるか
2. 横断の設定を 3 ページに集めた構成で、アーキテクトが設定漏れなく辿れるか
3. 実装を優先して v6 の記述を変えた方針でよいか。実装側の不具合であれば、解説書ではなく実装を直す判断になる
4. 「間違えたときにどうなるか」を書かない基準で、利用者が実際に困る注意まで落としていないか
5. YAML を併記したことで、Excel だけを使う読者にとって「テストデータの書き方」「テストデータの記載例」が読みにくくなっていないか
6. 内部構造のクラス図を利用者向けの構成図・シーケンス図に置き換えた判断でよいか。図が示す関係が実装と合っているか
7. サンプルファイル 10 本を落とし、記載例ページの例で代替した判断でよいか

# ページ別の申し送り

各ページは「由来」「判断で変えたことと理由」「実装との食い違いを直した箇所」だけを書いています。書いていないページ・節は、横断的な変更を除いて v6 の内容をそのまま引き継いでいます。
## 入口

### テスティングフレームワーク（`index.rst`）

既存。v6 の[テスティングフレームワーク](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/index.html)から。

- toctree 3本を4部（とは／導入と設定／テスト実装／ツール）に再構成し、対象読者と読む順序を示した
  - 入口で各ガイドの中身が分からなかったため
- important 2件（Jakarta Batch・マルチスレッド非対応）を〈テスティングフレームワークとは〉の「テストの種類」節末へ移した
  - 対応範囲の説明と同じ場所で読めるため

## 第1部 テスティングフレームワークとは

### テスティングフレームワークとは（`about/index.rst`）

混在。v6 の[自動テストフレームワーク](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/01_Abstract.html)と v6 の[テスティングフレームワーク](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/index.html)から。

- 取引単体テストの実行方法は、v6 が明言する3処理方式（ウェブ＝手動、REST・バッチ＝自動）だけを名指しし、残る3方式は述べていない
- アーキテクチャの構成物表（6行）を落とした
  - 図から読み取れる内容の再掲だったため

## 第2部 導入と設定

### テスティングフレームワークの導入（`setup/introduction.rst`）

混在。v6 の[同期応答メッセージ送信処理を伴う取引単体テストの実施方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/send_sync.html)の依存関係だけが対応し、残りは刷新で書き起こした。

- MOM の取引単体テストのページにしか無かった導入手順を、テストの種類によらず行う3つとしてこのページに集めた
- 依存関係を `test` スコープにし、v6 の `<exclusions>`（jetty・findbugs）を落とした
  - 現在の `nablarch-testing` に当該依存が無いため
- 実装との食い違いを直した: テスト用のコンポーネント設定ファイルの用意、テストデータの投入に使用するトランザクション（`testTran`）

### JUnit 5での使用（`setup/standard_usage.rst`）

既存。v6 の[JUnit 5用拡張機能](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/JUnit5_Extension.html)から。前提事項の surefire 条件だけは v6 の[自動テストフレームワーク](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/01_Abstract.html)から。

- `resolveTestRules()` の説明を未リリースの修正版前提で書いた
  - リリース済みの 2.1.0 では、本文どおりに書くと内部ルールが落ちる
- `TestRule` の例を `Timeout` からプロジェクト独自のものに差し替え、JUnit 5 の同等機能への対応表と warning 5件を足した
- 実装との食い違いを直した: JUnit 5 本体の依存関係、インジェクション対象の条件、`RegisterExtension` で適用できない Extension、実装と合わない tip 2件

### JUnit 4での使用（`setup/junit4.rst`）

混在。v6 の[自動テストフレームワーク](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/01_Abstract.html)と v6 の[目的別API使用方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.html)から。機能概要とテストクラスの例は刷新で書き起こした。

- 第3部の JUnit 5 の例を継承方式に読み替える規則を置いた
  - JUnit 4 の既存資産があるプロジェクトが書き続けられるようにするため
- 実装との食い違いを直した: JUnit 4 の依存関係（`junit-vintage-engine`）、委譲の例の `assertSqlResultSetEquals`

### テストデータの設定（`setup/testdata.rst`）

混在。v6 の[目的別API使用方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.html)、v6 の[データベースを使用するクラスのテスト](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/02_DbAccessTest.html)、v6 の[リクエスト単体テスト（バッチ処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_batch.html)、v6 の[リクエスト単体テストの実施方法(バッチ)](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/batch.html)、v6 の[リクエスト単体テスト（メッセージ受信処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_real.html)・v6 の[リクエスト単体テスト（同期応答メッセージ送信処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_send_sync.html)の5ページに散らばっていた、テストの種類によらず効く設定を集めた。

- YAML の `interpreters` を、Excel 用の5つのうち日時・文字種の2つに絞った
  - 残る3つは Excel のセル値を読むためのものだったため
- 読み込み先を VM 引数 `-D` で一時的に上書きする案内（v6 の脚注）を落とした
  - 設定ファイルに書く手順に一本化したため
- 実装との食い違いを直した: テストデータの読み込み先の記述先とデフォルト値、ディレクティブのデフォルト値の記述例、データ型の対応表

### システム日時と採番の固定（`setup/fixed_time_and_id.rst`）

混在。v6 の[目的別API使用方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.html)の2節「システム日時を任意の値に固定したい」「シーケンスオブジェクトを使った採番のテストをしたい」から。

- `fixedDate` を実装が受け付ける 14桁・17桁と書いた
  - `FixedSystemTimeProvider` の javadoc（12桁・15桁）とは食い違ったままになる
- `SystemRepository` からシステム日時を取得する Java コード例を落とし、1文に置き換えた
  - 第2部は設定を書くページのため
- 実装との食い違いを直した: 本番側のシーケンス採番クラスの FQCN、テーブル採番の設定値の参照先

### クラス単体テストの設定（`setup/class_unit_test.rst`）

混在。v6 の[Bean Validationに対応したForm/Entityのクラス単体テスト](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.html)、v6 の[Nablarch Validationに対応したForm/Entityのクラス単体テスト](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/02_entityUnitTestWithNablarchValidation.html)、v6 の[目的別API使用方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.html)から。

- Bean Validation 版8項目・Nablarch Validation 版6項目に分かれていた設定項目表を、8項目の表1つに統合した
  - ページによって理解が変わるため
- 実装との食い違いを直した: Nablarch Validation 版の「（全項目必須）」、デフォルト以外のトランザクションの設定キー
### リクエスト単体テストの設定（ウェブアプリケーション）（`setup/request_unit_test/web.rst`）

既存。v6 の[リクエスト単体テスト（ウェブ）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/02_RequestUnitTest.html)の「各種設定値」「その他の設定」と構造の説明から。

- 設定値の表のデフォルト値欄を、デフォルト設定を読み込んだ後の実効値に統一した
  - 上書きの要否が変わるため
- v6 の「実行速度を上げる」の枠組みと JVM オプション・Eclipse の手順を落とした
  - フレームワークの設定ではないため
- 実装との食い違いを直した: dumpVariableItem、jsTestResourceDir、htmlResourcesCharset、htmlCheckerConfig、httpServerFactory の登録

### リクエスト単体テストの設定（RESTfulウェブサービス）（`setup/request_unit_test/rest.rst`）

既存。v6 の[リクエスト単体テスト（RESTfulウェブサービス）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_rest.html)の「モジュール一覧」「設定」「各種設定値」から。

- 設定先を `src/test/resources/unit-test.xml` と具体パスで書いた記述を落とした
  - 構成に依らないため
- `webFrontControllerKey` の指定条件を「`webFrontController` 以外の名前で登録している場合」に一般化した
- tip の「Nablarch5u18 以降」の条件を外し、対象を依存関係3件にも広げた
- 実装との食い違いを直した: httpServerFactory の登録

### リクエスト単体テストの設定（HTTPメッセージング）（`setup/request_unit_test/http_messaging.rst`）

混在。v6 の[リクエスト単体テストの実施方法(HTTP同期応答メッセージ送信処理)](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/http_send_sync.html)と[同(HTTP同期応答メッセージ受信処理)](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/http_real.html)から。

- v6 が HTTP 受信と MOM 受信に二重に持っていたフレームワーク制御ヘッダの important を、本ページに集約した
- v6 の「これらの設定はアーキテクトが行うもの」という断りを落とした
- 実装との食い違いを直した: モックアップのコンポーネント名の決まり方、charset の説明、制御ヘッダの全列挙と空白の扱い

### リクエスト単体テストの設定（Nablarchバッチアプリケーション）（`setup/request_unit_test/batch.rst`）

混在。v6 の[リクエスト単体テスト（バッチ処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_batch.html)の「各種設定値」から。

- 置き換えの適用条件を、常駐バッチかどうかからリクエストスレッド内ループ制御ハンドラを含む構成かに改めた
- ディレクティブのデフォルト値とテスト用データ型の登録を「テストデータの設定」へ移し、導線を置いていない
- 実装との食い違いを直した: 応答不要メッセージ送信用プロバイダの差し替え、上書き時のプロパティ値の非継承

### リクエスト単体テストの設定（MOMによるメッセージング）（`setup/request_unit_test/mom.rst`）

混在。v6 に対応するのは[リクエスト単体テストの実施方法(同期応答メッセージ受信処理)](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/real.html)の important 1件のみ。

- フレームワーク制御ヘッダのフィールド名は HTTP メッセージングのページに集約し、本ページは参照だけにした
- リクエストスレッド内ループ制御ハンドラの置き換えは本ページに書かず、バッチのページへの導線も置いていない
- 実装との食い違いを直した: メッセージ受信用プロバイダの登録、同期応答メッセージ送信用プロバイダの差し替え

### リクエスト単体テストの設定（テーブルをキューとして使ったメッセージング）（`setup/request_unit_test/db_queue.rst`）

新規。v6 の NTF 解説書に対応する記述は無い。

- 他の方式と並ぶ位置にページを新設し、本文はバッチのページへの導線 1 文だけにした
  - 設定の実体が同じため
- 目次・機能概要・使用方法を置いておらず、設定章の他のページと形が揃っていない

### 取引単体テストの設定（RESTfulウェブサービス）（`setup/deal_unit_test/rest.rst`）

既存。v6 の[取引単体テスト（RESTfulウェブサービス）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/rest.html)の「Cookieなど前のレスポンスの情報を引き継ぐ方法」から。

- 提供済みの実装2クラスを「使用方法」、独自実装の手順を「拡張例」に分けた
  - 登録だけの読者が拡張を読まずに済むため
- 実装との食い違いを直した: XML 記述例の構文、cookieName の必須、ComplexRequestResponseProcessor の実行順

### 取引単体テストの設定（HTTPメッセージング）（`setup/deal_unit_test/http_messaging.rst`）

混在。v6 の[取引単体テスト（HTTPメッセージング）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/http_send_sync.html)と[取引単体テスト（MOMによるメッセージング）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/send_sync.html)から。

- MOM のページにしかなかった応答電文の読み込み設定を本ページに本文として置き、MOM からはリンクにした
- Interpreter をインライン定義から `nablarch/test/test-data.xml` の `component-ref` 参照に揃えた
- 実装との食い違いを直した: 記述例のコンポーネント名、charset の適用範囲、YAML の fileExtensions、読み込み設定

### 取引単体テストの設定（MOMによるメッセージング）（`setup/deal_unit_test/mom.rst`）

混在。v6 の[取引単体テスト（MOMによるメッセージング）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/send_sync.html)の「フレームワークで使用するクラスの設定」から。

- 応答電文の読み込み設定は HTTP メッセージングのページに集約し、本ページは同名の節で参照だけにした
- 実装との食い違いを直した: モックアップのコンポーネント名の決まり方

### マスタデータ復旧機能（`setup/master_data_restore.rst`）

既存。v6 の[マスタデータ復旧機能](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/04_MasterDataRestore.html)から。

- 環境構築の4節を必須3件と任意1件に分け、テーブルの依存関係の解析の抑止を使用方法の末尾に移した
- 実装との食い違いを直した: testEventListeners の登録、抑止設定の列挙順と適用範囲、復旧時の削除・挿入の単位、バックアップ用スキーマの tip
## 第3部 テストの実装

### テストデータの書き方（`implementation/testdata_notation.rst`）

混在。v6 で[テスティングフレームワークの概要](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/01_Abstract.html)・[データベースアクセスのテスト](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/02_DbAccessTest.html)・[Tips集](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.html)と[リクエスト単体テストの各処理方式のページ](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/index.html)に分散していた記法の説明を1ページに集めた。

- 0件のテーブルデータを記述する節を新設した
  - 準備データを空にする・期待値で空を検証する方法が v6 のどこにも無かった
- カラム省略の制約を「`LIST_MAP` は Map 完全一致のため全カラム必須／登録系は推奨」に分けた
  - v6 は一律に省略不可としていた
- 実装との食い違いを直した: 改行記法、可変長の `""` 行、電文の対応付け順、マーカーカラム・`default` グループの適用範囲、省略カラムの既定値、`testShots` の必須カラム

### テストデータの記載例（`implementation/testdata_examples.rst`）

混在。v6 に対応するページは無く、採番処理の例だけが「Tips集」の[Excelファイル記述例](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.html)から来ている。

- Tips集・DBアクセステスト・各テスト種別ページに散っていた記述例を用途別に1ページへ集約した
  - 読者が記法の節から該当する用途の例へ直接たどれるようにするため
- v6 に例が無い用途は記法の下書き資料から新規に書き起こし、題材はテスティングフレームワーク本体のテストリソースに合わせた
- Excel 形式の例は実際に読み込ませて確かめていない
  - 実物との突き合わせはレビューに委ねる
- 実装との食い違いを直した: レコード長の不一致、`sendSyncTestData`、`EXPECTED_COMPLETE_TABLE` の補完条件、`quoting-delimiter` の例

### エンティティ単体テスト（`implementation/class_unit_test/entity.rst`）

既存。v6 の[Bean Validationに対応したForm/Entityのクラス単体テスト](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.html)と[Nablarch Validationに対応したForm/Entityのクラス単体テスト](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/02_entityUnitTestWithNablarchValidation.html)を1ページに統合した。

- テストクラス・テストデータ・テスト対象クラスのダウンロードリンク6本を落とした
  - 撤去する旧ページ配下にあるため
  - 読者はサンプルを入手できなくなる
- コンストラクタをテストする節の個別コード例を落とし、「型の制限は setter と getter のテストと同じ」の1文にした
- 「テスト結果を確認する」を新設した
  - テストが失敗したときに何が出力されるかが v6 に無かった
- 実装との食い違いを直した: 必須カラム5件、文字種14種、`min` が1以下のときの文字列長不足テスト、方式に対応しないメソッドの挙動

### コンポーネント単体テスト（`implementation/class_unit_test/component.rst`）

既存。v6 の[Action/Componentのクラス単体テスト](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.html)を軸に、[データベースを使用するクラスのテスト](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/02_DbAccessTest.html)と[Tips集](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.html)の DB テスト関連の節を統合した。

- サンプルアプリ固有のコード・Excel 画像・ダウンロードリンク4本を落とし、参照系・更新系の汎用手順に置き換えた
- ページ内に持っていたテストデータの記述例を記載例ページへ移し、本ページはテストコード側の書き方に絞った
- 「確認する対象 → 使用するメソッド」の一覧表を新設した（`assertSqlRowEquals` を含む）
  - v6 は使い分けを示していなかった
- 実装との食い違いを直した: `assertSqlResultSetEquals`・`assertTableEquals`・`getListMap` の引数、別ディレクトリのテストデータの解決先

### リクエスト単体テスト（ウェブアプリケーション）（`implementation/request_unit_test/web.rst`）

混在。v6 の[リクエスト単体テスト（ウェブアプリケーション）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/02_RequestUnitTest.html)と[リクエスト単体テストの実施方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/index.html)を1ページに統合し、[ファイルアップロード](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/fileupload.html)・[二重サブミット防止](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/double_transmission.html)・[メール送信](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/mail.html)・「Tips集」の該当節を取り込んだ。

- 内部構造（`HttpServer`・`HttpRequestTestSupport`・`DbAccessTestSupport` の行）を落とし、利用者が名前を書くクラスだけを表に残した
- リクエストスコープの値の確認から Form 取得と `SqlRow` のコード例を落とし、型ごとの使用メソッド表と tip に置き換えた
- アップロードファイルの具体例2組を落とし、2方法の説明と記法ページへの参照だけにした
  - 記載例ページに画像ファイルの例はある
- 実装との食い違いを直した: `getParam` の戻り値、`assertObjectPropertyEquals` の例、送信メソッドと実行手順の順序、出力ファイルの名前、自動確認の項目
### リクエスト単体テスト（RESTfulウェブサービス）（`implementation/request_unit_test/rest.rst`）

既存。v6 の[リクエスト単体テスト（RESTfulウェブサービス）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_rest.html)と[リクエスト単体テストの実施方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/rest.html)を1ページに統合した。

- v6 の「`SimpleRestTestSupport` ならテストデータの書き方は読み飛ばしてよい」の案内を落とした
- 実装との食い違いを直した: `readTextResource` の引数、期待値ファイルの配置、内蔵サーバの起動タイミング、`setBody`、`testDataParser` の準備

### リクエスト単体テスト（HTTPメッセージング）（`implementation/request_unit_test/http_messaging.rst`）

既存。v6 の[リクエスト単体テストの実施方法（HTTP同期応答メッセージ受信処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/http_real.html)と[リクエスト単体テストの実施方法(HTTP同期応答メッセージ送信処理)](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/http_send_sync.html)の導入部、[リクエスト単体テスト（HTTP同期応答メッセージ送信処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_http_send_sync.html)の読み替え表から。

- 読み替え表から `MockMessagingContext → MockMessagingClient` の行を落とした
  - 読み替え先の MOM のページに出てこないため
- 「送信キュー・受信キューを通信先と読み替える」の適用範囲を同期応答メッセージ送信の説明に限定した
  - 受信側は実際にキューを使うため
- 実装との食い違いを直した: `RequestTestingMessagingClient` が内部クラスを持たないこと

### リクエスト単体テスト（Nablarchバッチアプリケーション）（`implementation/request_unit_test/batch.rst`）

混在。v6 の[リクエスト単体テスト（バッチ処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_batch.html)と[リクエスト単体テストの実施方法(バッチ)](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/batch.html)を1ページに統合し、[リクエスト単体テストの実施方法（応答不要メッセージ送信処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/delayed_send.html)を取り込んだ。

- 応答不要メッセージ送信をページとして立てず、記述方法が異なる箇所を各節に差し込んだ
  - 実体が Nablarch バッチのテストであるため
- ファイル期待値の記法表とログ検証のカラム表を本ページから落とした
  - 記法は「テストデータの書き方」にまとめたため
- 実装との食い違いを直した: `execute()` の引数、ループ制御ハンドラ、応答不要送信の `errorCase`・`expectedMessage`・`expectedStatusCode`

### リクエスト単体テスト（MOMによるメッセージング）（`implementation/request_unit_test/mom.rst`）

既存。v6 の5ページを1ページに統合した。[リクエスト単体テスト（メッセージ受信処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_real.html)、[リクエスト単体テスト（同期応答メッセージ送信処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_send_sync.html)、[リクエスト単体テストの実施方法(同期応答メッセージ受信処理)](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/real.html)、[リクエスト単体テストの実施方法(同期応答メッセージ送信処理)](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/send_sync.html)、[リクエスト単体テストの実施方法（応答不要メッセージ受信処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/delayed_receive.html)。

- 同期応答メッセージ送信は、テスト対象の処理方式のテストを踏襲する形にし、MOM に固有の点だけを本ページに置いた
- 実装との食い違いを直した: サポートクラス名・パッケージ、要求電文のアサート主体、`execute()` の引数、`expectedStatusCode` の照合

### リクエスト単体テスト（テーブルをキューとして使ったメッセージング）（`implementation/request_unit_test/db_queue.rst`）

新規。v6 に「テーブルをキューとして使ったメッセージング」の記述は無い。

- 章から辿れるよう独立したページを立て、本文はバッチのページへの参照1文だけにした
  - コード例とテストデータの例は置かない

### 取引単体テスト（ウェブアプリケーション）（`implementation/deal_unit_test/web.rst`）

既存。v6 の[取引単体テストの実施方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/index.html)と[二重サブミット防止機能のテスト実施方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/double_transmission.html)の取引単体テスト側を1ページにした。

- v6 の「画面ハードコピー取得ツール、DBダンプ取得ツール等は現在検討中」の tip を落とした
  - 取得するエビデンスは変わらないため
- 二重サブミット防止機能の確認手順を本ページの節に畳んだ
  - v6 はリクエスト単体テストのページ配下で、取引単体テストの読者が辿り着きにくかったため

### 取引単体テスト（RESTfulウェブサービス）（`implementation/deal_unit_test/rest.rst`）

混在。v6 の[取引単体テストの実施方法（RESTfulウェブサービス）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/rest.html)から。

- 実装との食い違いを直した: 1つの取引を構成する複数リクエストの送信方法

### 取引単体テスト（HTTPメッセージング）（`implementation/deal_unit_test/http_messaging.rst`）

既存。v6 の[HTTP同期応答メッセージ送信処理を伴う取引単体テストの実施方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/http_send_sync.html)の実施方法部分。

- 実装との食い違いを直した: 出力されるログの形式とロガー、応答電文のヘッダ、要求電文のデータブロック

### 取引単体テスト（Nablarchバッチアプリケーション）（`implementation/deal_unit_test/batch.rst`）

混在。v6 の[取引単体テストの実施方法（バッチ）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/batch.html)。

- 実装との食い違いを直した: テストショット一覧の必須カラムとカラム名、import のパッケージ、正常系の `expectedStatusCode`、`expectedTable` の値

### 取引単体テスト（MOMによるメッセージング）（`implementation/deal_unit_test/mom.rst`）

混在。v6 の3ページを1ページにした。[同期応答メッセージ送信処理を伴う取引単体テストの実施方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/send_sync.html)、[取引単体テストの実施方法（同期応答メッセージ受信処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/real.html)、[取引単体テストの実施方法（応答不要メッセージ受信処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/delayed_receive.html)。

- テスト対象を受信側と同期応答送信を伴うウェブ側の2通りに分け、進め方はバッチ版・ウェブ版の取引単体テストへ委ねた
- 実装との食い違いを直した: モックアップクラスが担う範囲、応答電文を返す順序、ログのロガー名とレベル、要求電文の `requestId` フィールド

### 取引単体テスト（テーブルをキューとして使ったメッセージング）（`implementation/deal_unit_test/db_queue.rst`）

新規。v6 の[取引単体テストの実施方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/index.html)配下にこの処理方式のページは無い。

- 他の処理方式と同じく独立したページを立て、本文はバッチ版への参照1文だけにした
  - コード例とテストデータの例は置かない
## 第4部 ツール

### リクエスト単体データ作成ツール（`tools/request_data_tool.rst`）

既存。v6 の[リクエスト単体データ作成ツール](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/08_TestTools/01_HttpDumpTool/01_HttpDumpTool.html)と[リクエスト単体データ作成ツール インストールガイド](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/08_TestTools/01_HttpDumpTool/02_SetUpHttpDumpTool.html)を1ページにした。

- Linux 向けの `httpDump.sh` の案内を落とし、`httpDump.bat` だけを案内した
  - 配布物に `.sh` が無い
- 前提から「開発環境構築ガイドに従って構築済み」を落とした
  - 参照先のページが存在しない
- 実装との食い違いを直した: 前提事項の `JAVA_HOME`、初期画面表示のテストデータ、HTMLダンプの出力先、Eclipse の操作項目名

### マスタデータ投入ツール（`tools/master_data_tool.rst`）

既存。v6 の[マスタデータ投入ツール](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/08_TestTools/02_MasterDataSetup/01_MasterDataSetupTool.html)と[マスタデータ投入ツール インストールガイド](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/08_TestTools/02_MasterDataSetup/02_ConfigMasterDataSetupTool.html)を1ページにした。

- 前提を「アーキタイプから生成したプロジェクト」から「Maven の標準ディレクトリ構成」に広げた
  - ビルドファイルが依存するのはディレクトリ構成だけ
- 配布物にサンプルアプリケーションのデータが入っており、そのまま実行すると記述テーブルが置き換わることを警告した
- ターゲット表に動作（main は test へフォールバック、バックアップへコピーする範囲、失敗しても `BUILD SUCCESSFUL`）を書き足した
  - v6 では投入できたかを判断できなかったため
- 実装との食い違いを直した: 配布物のファイル構成、バックアップ用スキーマに必要なテーブルの範囲

### HTMLチェックツール（`tools/html_check_tool.rst`）

既存。v6 の[HTMLチェックツール](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/08_TestTools/03_HtmlCheckTool/index.html)。

- 画面を HTML5 で記述しているプロジェクトでは使用できないことを明示し、無効化・差し替えの節へ誘導した
  - v6 は触れていない
- 設定ファイルの書き損じで黙って壊れる事象と `htmlCheckerConfig` の副作用を実装から足し、指摘メッセージの形式を表にした
- 実装との食い違いを直した: 構文チェックの仕様（タグの省略可否、文書型宣言、クォートの例）、JavaScript の `--` の条件

### テストデータ変換ツール（`tools/testdata_converter.rst`）

新規。v6 に対応するページは無い。`nablarch-testing-converter` の実装と設計資料から書き起こした。

- 変換で何が保たれ何が変わるかを機能概要に置いた
  - Excel 形式から移す読者には可否の判断が先に要る
- 設計資料に無い Maven プラグイン（`convert` ゴール）と Java から呼ぶ方法を実装から書き起こした
  - そのままでは使い始められない
- 変換結果を確かめる手段として、同じ形式への往復と `YamlTestDataValidator` を示した
  - 変換の経路には検証が組み込まれていないため
