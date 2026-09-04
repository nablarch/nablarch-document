# NTF 解説書 刷新版 レビューガイド

チームメンバー・TL が刷新版をレビューするための申し送りです。読むのは刷新版の HTML で、本書は v6 から判断で変えたことと、その理由だけを伝えます。

## 進め方

- 読むものは刷新版の HTML 38 ページです（部の目次 3 ページを除く。配布方法は別途連絡）。比較する相手は [v6 の公開解説書](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/index.html) で、各ページに元の v6 ページを書いてあります
- まず「全体で判断してほしいこと」に答え、次に担当ページの申し送りを読み、変えた箇所を刷新版で開いて判断してください
- 分担は、TL が「全体で判断してほしいこと」と入口・第1部です。メンバーは処理方式ごとに、第2部の設定ページと第3部の実装ページを対で担当します。第4部はツールを使う人が担当します
- コメントは [PR #728](https://github.com/nablarch/nablarch-document/pull/728) のレビューコメントに、該当行へ付けてください。ページ全体への意見は「Files changed」のファイル先頭行へ
- 用語の統一・JUnit 5 化・表の折り返しなどの横断的な変更はページ別には書いていません。下の「全体で変えたこと」で 1 回だけ判断してください

## 全体で変えたことと理由

- 47 ページを 4 部構成 38 ページに組み直した（とは／導入と設定／テスト実装／ツール）
  - v6 は設定と実装手順が同じページに混在していたため
- JUnit 5 を標準にし、JUnit 4 は「JUnit 4での使用」1 ページに集約した
  - ブランクプロジェクトが JUnit 5 構成のため
- 横断の設定を「導入」「テストデータの設定」「システム日時と採番の固定」の 3 ページに集めた
  - v6 は方式別ページに散っていたため
- 実装と食い違う記述は実装に合わせ、陳腐化した例示は落とした
- 「間違えたときにどうなるか」の注意は、正しく書こうとしても踏むものだけに絞った
- 用語を統一した
  - 自動テストフレームワーク → テスティングフレームワーク
  - テストケース → テストショット
  - スーパークラス → スーパクラス
- 内部構造のクラス図と Excel のスクリーンショットを落とし、構成図・シーケンス図 21 枚を新しく描いた
- テストデータの YAML 形式を Excel 形式と対で併記した
  - AI エージェントが生成・解析できるようにするため
- 表を折り返しにした
  - Excel シートを再現した 10 表は、折り返しても識別子の幅で横スクロールが残る（折り返しの指定は全表に付けてある）
- `:download:` のサンプルファイル 10 本を落とし、代わりに Example アプリケーション 3 本の `src/test` を第3部の部トビラで案内した
  - 実ファイルが失われていたため。Example アプリケーションは JUnit 5 で書かれ、保守されているため

## 全体で判断してほしいこと

初めてテスティングフレームワークを使う人になったつもりで刷新版を読み、次を判断してください。

1. アーキテクトが第2部を辿って、自分のプロジェクトに要る設定と、その設定方法が分かるか
2. アプリケーションプログラマが第3部だけでテストを書き始められるか。v6 にあって、無いと困る説明や例はないか
3. JUnit 4 のまま続けるプロジェクトが「JUnit 4での使用」1 ページで困らないか
4. Excel 形式だけを使う人が「テストデータの書き方」「テストデータの記載例」で迷わないか（YAML 形式と対で並べています）
5. 構成図・シーケンス図で、テストの仕組みが文章より分かりやすくなっているか
6. 「間違えたときにどうなるか」の注意は、正しく書こうとしても踏むものだけに絞りました。通常の使い方で踏むのに、落ちているものはないか

# ページ別の申し送り

各ページは「元の v6 ページ」「v6 に無い部分」「変えたことと理由」だけを書いています。「v6 に無い部分」は、比較する相手が無い箇所があるページにだけあります。書いていないページ・節は、横断的な変更と、実装に合わせた記述の訂正を除いて、v6 の内容を引き継いでいます。

## 入口

### テスティングフレームワーク（`index.rst`）

**元の v6 ページ**
- [テスティングフレームワーク](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/index.html)

**変えたことと理由**
- toctree 3本を4部（とは／導入と設定／テスト実装／ツール）に再構成し、対象読者と読む順序を示した
  - 入口で各ガイドの中身が分からなかったため
- important 2件（Jakarta Batch・マルチスレッド非対応）を〈テスティングフレームワークとは〉の「テストの種類」節末へ移した
  - 対応範囲の説明と同じ場所で読めるため

## 第1部 テスティングフレームワークとは

### テスティングフレームワークとは（`about/index.rst`）

**元の v6 ページ**
- [自動テストフレームワーク](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/01_Abstract.html)
- [テスティングフレームワーク](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/index.html)

**変えたことと理由**
- アーキテクチャの構成物表（6行）を落とした
  - 図から読み取れる内容の再掲だったため
- テストの種類の表と、リクエスト単体テスト6種の表を箇条書きにした（テスト範囲→実行方法の順。6種の名前は各ページへのリンク）
- サポートクラスの継承図を、テストの種類ごとに3枚に分けた
  - 1枚では拡大しないと読めない幅だったため

## 第2部 導入と設定

### テスティングフレームワークの導入（`setup/introduction.rst`）

**元の v6 ページ**
- [同期応答メッセージ送信処理を伴う取引単体テストの実施方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/send_sync.html) の依存関係

**v6 に無い部分**
依存関係以外は刷新で書き起こした。

**変えたことと理由**
- MOM の取引単体テストのページにしか無かった導入手順を、テストの種類によらず行う3つとしてこのページに集めた
- 依存関係を `test` スコープにし、v6 の `<exclusions>`（jetty・findbugs）を落とした
  - 現在の `nablarch-testing` に当該依存が無いため

### JUnit 5での使用（`setup/standard_usage.rst`）

**元の v6 ページ**
- [JUnit 5用拡張機能](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/JUnit5_Extension.html)
- [自動テストフレームワーク](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/01_Abstract.html) の前提事項（surefire の条件）

**変えたことと理由**
- `resolveTestRules()` の説明を未リリースの修正版前提で書いた
  - リリース済みの 2.1.0 では、本文どおりに書くと内部ルールが落ちる
- `TestRule` の例を `Timeout` からプロジェクト独自のものに差し替え、JUnit 5 の同等機能への対応表と warning 5件を足した

### JUnit 4での使用（`setup/junit4.rst`）

**元の v6 ページ**
- [自動テストフレームワーク](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/01_Abstract.html)
- [目的別API使用方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.html)

**v6 に無い部分**
機能概要とテストクラスの例は刷新で書き起こした。

**変えたことと理由**
- 第3部の JUnit 5 の例を継承方式に読み替える規則を置いた
  - JUnit 4 の既存資産があるプロジェクトが書き続けられるようにするため

### テストデータの設定（形式・配置・記述の省略）（`setup/testdata.rst`）

**元の v6 ページ**
- [目的別API使用方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.html)
- [データベースを使用するクラスのテスト](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/02_DbAccessTest.html)
- [リクエスト単体テスト（バッチ処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_batch.html)
- [リクエスト単体テストの実施方法(バッチ)](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/batch.html)
- [リクエスト単体テスト（メッセージ受信処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_real.html)
- [リクエスト単体テスト（同期応答メッセージ送信処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_send_sync.html)

**v6 に無い部分**
上のページに散らばっていた、テストの種類によらず効く設定を 1 ページに集めた。

**変えたことと理由**
- YAML の `interpreters` を、Excel 用の5つのうち日時・文字種の2つに絞った
  - 残る3つは Excel のセル値を読むためのものだったため
- 読み込み先を VM 引数 `-D` で一時的に上書きする案内（v6 の脚注）を落とした
  - 設定ファイルに書く手順に一本化したため

### システム日時と採番の固定（`setup/fixed_time_and_id.rst`）

**元の v6 ページ**
- [目的別API使用方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.html) の 2 節「システム日時を任意の値に固定したい」「シーケンスオブジェクトを使った採番のテストをしたい」

**変えたことと理由**
- `fixedDate` を実装が受け付ける 14桁・17桁と書いた
  - `FixedSystemTimeProvider` の javadoc（12桁・15桁）とは食い違ったままになる
- `SystemRepository` からシステム日時を取得する Java コード例を落とし、1文に置き換えた
  - 第2部は設定を書くページのため

### エンティティ単体テストの設定（`setup/entity_unit_test.rst`）

**元の v6 ページ**
- [Bean Validationに対応したForm/Entityのクラス単体テスト](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.html)
- [Nablarch Validationに対応したForm/Entityのクラス単体テスト](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/02_entityUnitTestWithNablarchValidation.html)

**変えたことと理由**
- Bean Validation 版8項目・Nablarch Validation 版6項目に分かれていた設定項目表を、8項目の表1つに統合した
  - ページによって理解が変わるため
- 「クラス単体テストの設定」1ページだったものを、エンティティとコンポーネントの2ページに分けた
  - 目次から内容に気づけるようにするため（第3部の実装ページと同じ分け方）

### コンポーネント単体テストの設定（デフォルト以外のトランザクション）（`setup/component_unit_test.rst`）

**元の v6 ページ**
- [目的別API使用方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.html) の「デフォルト以外のトランザクションを使用したい」

**変えたことと理由**
- 「クラス単体テストの設定」から分けて、題に内容（デフォルト以外のトランザクション）を出した
  - 目次から内容に気づけるようにするため

### リクエスト単体テストの設定（ウェブアプリケーション）（`setup/request_unit_test/web.rst`）

**元の v6 ページ**
- [リクエスト単体テスト（ウェブアプリケーション）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/02_RequestUnitTest.html) の「各種設定値」「その他の設定」と構造の説明

**変えたことと理由**
- 設定値の表のデフォルト値欄を、デフォルト設定を読み込んだ後の実効値に統一した
  - 上書きの要否が変わるため
- v6 の「実行速度を上げる」の枠組みと、`-Xverify:none` などの JVM オプションの小節を落とした
  - フレームワークの設定ではないため
- Eclipse の実行構成で VM 引数を指定する手順と画面を落とした
  - IDE 固有の操作であり、テスティングフレームワークの設定ではないため
- 拡張例「テストデータの書き方を拡張する」を落とした
  - v6 の記述は「継承する」だけで、どういう場合に行うかが無く、利用者が動ける内容にならないため。拡張点の説明は `AbstractHttpRequestTestTemplate` の Javadoc にある

### リクエスト単体テストの設定（RESTfulウェブサービス）（`setup/request_unit_test/rest.rst`）

**元の v6 ページ**
- [リクエスト単体テスト（RESTfulウェブサービス）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_rest.html) の「モジュール一覧」「設定」「各種設定値」

**変えたことと理由**
- 設定先を `src/test/resources/unit-test.xml` と具体パスで書いた記述を落とした
  - 構成に依らないため
- `webFrontControllerKey` の指定条件を「`webFrontController` 以外の名前で登録している場合」に一般化した
- tip の「Nablarch5u18 以降」の条件を外し、対象を依存関係3件にも広げた

### リクエスト単体テストの設定（HTTPメッセージング）（`setup/request_unit_test/http_messaging.rst`）

**元の v6 ページ**
- [リクエスト単体テストの実施方法(HTTP同期応答メッセージ送信処理)](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/http_send_sync.html)
- [リクエスト単体テストの実施方法（HTTP同期応答メッセージ受信処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/http_real.html)

**変えたことと理由**
- v6 が HTTP 受信と MOM 受信に二重に持っていたフレームワーク制御ヘッダの important を、本ページに集約した
- v6 の「これらの設定はアーキテクトが行うもの」という断りを落とした

### リクエスト単体テストの設定（Nablarchバッチアプリケーション）（`setup/request_unit_test/batch.rst`）

**元の v6 ページ**
- [リクエスト単体テスト（バッチ処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_batch.html) の「各種設定値」

**変えたことと理由**
- 置き換えの適用条件を、常駐バッチかどうかからリクエストスレッド内ループ制御ハンドラを含む構成かに改めた
- ディレクティブのデフォルト値とテスト用データ型の登録を「テストデータの設定」へ移し、導線を置いていない

### リクエスト単体テストの設定（MOMによるメッセージング）（`setup/request_unit_test/mom.rst`）

**元の v6 ページ**
- [リクエスト単体テストの実施方法(同期応答メッセージ受信処理)](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/real.html) の important 1 件

**v6 に無い部分**
上の important 以外は刷新で書き起こした。

**変えたことと理由**
- フレームワーク制御ヘッダのフィールド名は HTTP メッセージングのページに集約し、本ページは参照だけにした

### リクエスト単体テストの設定（テーブルをキューとして使ったメッセージング）（`setup/request_unit_test/db_queue.rst`）

**元の v6 ページ**
- なし（v6 に対応する記述は無い）

**変えたことと理由**
- 他の方式と並ぶ位置にページを新設し、本文はバッチのページへの導線 1 文だけにした
  - 設定の実体が同じため
- 目次・機能概要・使用方法を置いておらず、設定章の他のページと形が揃っていない

### 取引単体テストの設定（RESTfulウェブサービス）（`setup/deal_unit_test/rest.rst`）

**元の v6 ページ**
- [取引単体テストの実施方法（RESTfulウェブサービス）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/rest.html) の「Cookieなど前のレスポンスの情報を引き継ぐ方法」

**変えたことと理由**
- 提供済みの実装2クラスを「使用方法」、独自実装の手順を「拡張例」に分けた
  - 登録だけの読者が拡張を読まずに済むため

### 取引単体テストの設定（HTTPメッセージング）（`setup/deal_unit_test/http_messaging.rst`）

**元の v6 ページ**
- [HTTP同期応答メッセージ送信処理を伴う取引単体テストの実施方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/http_send_sync.html)
- [同期応答メッセージ送信処理を伴う取引単体テストの実施方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/send_sync.html)

**変えたことと理由**
- MOM のページにしかなかった応答電文の読み込み設定を本ページに本文として置き、MOM からはリンクにした
- Interpreter をインライン定義から `nablarch/test/test-data.xml` の `component-ref` 参照に揃えた

### 取引単体テストの設定（MOMによるメッセージング）（`setup/deal_unit_test/mom.rst`）

**元の v6 ページ**
- [同期応答メッセージ送信処理を伴う取引単体テストの実施方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/send_sync.html) の「フレームワークで使用するクラスの設定」

**変えたことと理由**
- 応答電文の読み込み設定は HTTP メッセージングのページに集約し、本ページは同名の節で参照だけにした

### マスタデータ復旧機能（`setup/master_data_restore.rst`）

**元の v6 ページ**
- [マスタデータ復旧機能](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/04_MasterDataRestore.html)

**変えたことと理由**
- 環境構築の4節を必須3件と任意1件に分け、テーブルの依存関係の解析の抑止を使用方法の末尾に移した

## 第3部 テストの実装

### テストデータの書き方（`implementation/testdata_notation.rst`）

**元の v6 ページ**
- [自動テストフレームワーク](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/01_Abstract.html)
- [データベースを使用するクラスのテスト](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/02_DbAccessTest.html)
- [目的別API使用方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.html)
- [リクエスト単体テストの実施方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/index.html)

**v6 に無い部分**
上のページに分散していた記法の説明を 1 ページに集めた。

**変えたことと理由**
- テストデータの階層を「データコンテナ／データセクション／データブロック」と名付け、冒頭の表で定義した
  - v6 は「ブック」「シート」という Excel の物理名で説明していたが、YAML 形式ではディレクトリとファイルになる。形式に依らない名前は変換ツールの中間モデル（`TestDataContainer`／`TestDataSection`／`TestDataBlock`）から採った
  - API の引数名 `sheetName` には、データセクション名を渡す
- 0件のテーブルデータを記述する節を新設した
  - 準備データを空にする・期待値で空を検証する方法が v6 のどこにも無かった
- カラム省略の制約を「`LIST_MAP` は Map 完全一致のため全カラム必須／登録系は推奨」に分けた
  - v6 は一律に省略不可としていた

### テストデータの記載例（`implementation/testdata_examples.rst`）

**元の v6 ページ**
- [目的別API使用方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.html) の「Excelファイル記述例」（採番処理の例のみ）

**v6 に無い部分**
採番処理の例以外は、v6 に対応する記述が無い。

**変えたことと理由**
- Tips集・DBアクセステスト・各テスト種別ページに散っていた記述例を用途別に1ページへ集約した
  - 読者が記法の節から該当する用途の例へ直接たどれるようにするため
- v6 に例が無い用途は記法の下書き資料から新規に書き起こし、題材はテスティングフレームワーク本体のテストリソースに合わせた
- 36 組の例をすべて Excel・YAML の両形式でテスティングフレームワークに読み込ませ、エラーなく読めて両形式が同じ値になることを確かめた
  - 読み込みで見つかった 3 件（`quoting-delimiter` セルの記法、`expectedMessages` の `file-type`、DB のバイナリ値の `0x`）は直した

### エンティティ単体テスト（`implementation/class_unit_test/entity.rst`）

**元の v6 ページ**
- [Bean Validationに対応したForm/Entityのクラス単体テスト](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.html)
- [Nablarch Validationに対応したForm/Entityのクラス単体テスト](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/02_entityUnitTestWithNablarchValidation.html)

**変えたことと理由**
- テストクラス・テストデータ・テスト対象クラスのダウンロードリンク6本を落とした
  - 撤去する旧ページ配下にあるため
  - 代わりに第3部の部トビラで Example アプリケーションの `src/test` を案内した
- コンストラクタをテストする節の個別コード例を落とし、「型の制限は setter と getter のテストと同じ」の1文にした
- 「テスト結果を確認する」を新設した
  - テストが失敗したときに何が出力されるかが v6 に無かった

### コンポーネント単体テスト（`implementation/class_unit_test/component.rst`）

**元の v6 ページ**
- [Action/Componentのクラス単体テスト](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.html)
- [データベースを使用するクラスのテスト](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/02_DbAccessTest.html) の DB テスト関連の節
- [目的別API使用方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.html) の DB テスト関連の節

**変えたことと理由**
- サンプルアプリ固有のコード・Excel 画像・ダウンロードリンク4本を落とし、参照系・更新系の汎用手順に置き換えた
- ページ内に持っていたテストデータの記述例を記載例ページへ移し、本ページはテストコード側の書き方に絞った
- 「確認する対象 → 使用するメソッド」の一覧表を新設した（`assertSqlRowEquals` を含む）
  - v6 は使い分けを示していなかった

### リクエスト単体テスト（ウェブアプリケーション）（`implementation/request_unit_test/web.rst`）

**元の v6 ページ**
- [リクエスト単体テスト（ウェブアプリケーション）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/02_RequestUnitTest.html)
- [リクエスト単体テストの実施方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/index.html)
- [リクエスト単体テストの実施方法(ファイルアップロード)](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/fileupload.html)
- [二重サブミット防止機能のテスト実施方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/double_transmission.html)
- [リクエスト単体テストの実施方法(メール送信)](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/mail.html)
- [目的別API使用方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.html) の該当節

**変えたことと理由**
- 内部構造（`HttpServer`・`HttpRequestTestSupport`・`DbAccessTestSupport` の行）を落とし、利用者が名前を書くクラスだけを表に残した
- リクエストスコープの値の確認から Form 取得と `SqlRow` のコード例を落とし、型ごとの使用メソッド表と tip に置き換えた
- アップロードファイルの具体例2組を落とし、2方法の説明と記法ページへの参照だけにした
  - 記載例ページに画像ファイルの例はある

### リクエスト単体テスト（RESTfulウェブサービス）（`implementation/request_unit_test/rest.rst`）

**元の v6 ページ**
- [リクエスト単体テスト（RESTfulウェブサービス）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_rest.html)
- [リクエスト単体テストの実施方法（RESTfulウェブサービス）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/rest.html)

**変えたことと理由**
- v6 の「`SimpleRestTestSupport` ならテストデータの書き方は読み飛ばしてよい」の案内を落とした

### リクエスト単体テスト（HTTPメッセージング）（`implementation/request_unit_test/http_messaging.rst`）

**元の v6 ページ**
- [リクエスト単体テストの実施方法（HTTP同期応答メッセージ受信処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/http_real.html) の導入部
- [リクエスト単体テストの実施方法(HTTP同期応答メッセージ送信処理)](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/http_send_sync.html) の導入部
- [リクエスト単体テスト（HTTP同期応答メッセージ送信処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_http_send_sync.html) の読み替え表

**変えたことと理由**
- 読み替え表から `MockMessagingContext → MockMessagingClient` の行を落とした
  - 読み替え先の MOM のページに出てこないため
- 「送信キュー・受信キューを通信先と読み替える」の適用範囲を同期応答メッセージ送信の説明に限定した
  - 受信側は実際にキューを使うため

### リクエスト単体テスト（Nablarchバッチアプリケーション）（`implementation/request_unit_test/batch.rst`）

**元の v6 ページ**
- [リクエスト単体テスト（バッチ処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_batch.html)
- [リクエスト単体テストの実施方法(バッチ)](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/batch.html)
- [リクエスト単体テストの実施方法（応答不要メッセージ送信処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/delayed_send.html)

**変えたことと理由**
- 応答不要メッセージ送信をページとして立てず、記述方法が異なる箇所を各節に差し込んだ
  - 実体が Nablarch バッチのテストであるため
- ファイル期待値の記法表とログ検証のカラム表を本ページから落とした
  - 記法は「テストデータの書き方」にまとめたため

### リクエスト単体テスト（MOMによるメッセージング）（`implementation/request_unit_test/mom.rst`）

**元の v6 ページ**
- [リクエスト単体テスト（メッセージ受信処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_real.html)
- [リクエスト単体テスト（同期応答メッセージ送信処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_send_sync.html)
- [リクエスト単体テストの実施方法(同期応答メッセージ受信処理)](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/real.html)
- [リクエスト単体テストの実施方法(同期応答メッセージ送信処理)](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/send_sync.html)
- [リクエスト単体テストの実施方法（応答不要メッセージ受信処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/delayed_receive.html)

**変えたことと理由**
- 同期応答メッセージ送信は、テスト対象の処理方式のテストを踏襲する形にし、MOM に固有の点だけを本ページに置いた

### リクエスト単体テスト（テーブルをキューとして使ったメッセージング）（`implementation/request_unit_test/db_queue.rst`）

**元の v6 ページ**
- なし（v6 に「テーブルをキューとして使ったメッセージング」の記述は無い）

**変えたことと理由**
- 章から辿れるよう独立したページを立て、本文はバッチのページへの参照1文だけにした
  - コード例とテストデータの例は置かない

### 取引単体テスト（ウェブアプリケーション）（`implementation/deal_unit_test/web.rst`）

**元の v6 ページ**
- [取引単体テストの実施方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/index.html)
- [二重サブミット防止機能のテスト実施方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/double_transmission.html) の取引単体テスト側

**変えたことと理由**
- v6 の「画面ハードコピー取得ツール、DBダンプ取得ツール等は現在検討中」の tip を落とした
  - 取得するエビデンスは変わらないため
- 二重サブミット防止機能の確認手順を本ページの節に畳んだ
  - v6 はリクエスト単体テストのページ配下で、取引単体テストの読者が辿り着きにくかったため

### 取引単体テスト（RESTfulウェブサービス）（`implementation/deal_unit_test/rest.rst`）

**元の v6 ページ**
- [取引単体テストの実施方法（RESTfulウェブサービス）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/rest.html)

**変えたことと理由**
- なし（横断的な変更のみ）

### 取引単体テスト（HTTPメッセージング）（`implementation/deal_unit_test/http_messaging.rst`）

**元の v6 ページ**
- [HTTP同期応答メッセージ送信処理を伴う取引単体テストの実施方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/http_send_sync.html) の実施方法部分

**変えたことと理由**
- なし（横断的な変更のみ）

### 取引単体テスト（Nablarchバッチアプリケーション）（`implementation/deal_unit_test/batch.rst`）

**元の v6 ページ**
- [取引単体テストの実施方法（バッチ）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/batch.html)

**変えたことと理由**
- なし（横断的な変更のみ）

### 取引単体テスト（MOMによるメッセージング）（`implementation/deal_unit_test/mom.rst`）

**元の v6 ページ**
- [同期応答メッセージ送信処理を伴う取引単体テストの実施方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/send_sync.html)
- [取引単体テストの実施方法（同期応答メッセージ受信処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/real.html)
- [取引単体テストの実施方法（応答不要メッセージ受信処理）](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/delayed_receive.html)

**変えたことと理由**
- テスト対象を受信側と同期応答送信を伴うウェブ側の2通りに分け、進め方はバッチ版・ウェブ版の取引単体テストへ委ねた

### 取引単体テスト（テーブルをキューとして使ったメッセージング）（`implementation/deal_unit_test/db_queue.rst`）

**元の v6 ページ**
- なし（v6 の[取引単体テストの実施方法](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/index.html)配下にこの処理方式のページは無い）

**変えたことと理由**
- 他の処理方式と同じく独立したページを立て、本文はバッチ版への参照1文だけにした
  - コード例とテストデータの例は置かない

## 第4部 ツール

### リクエスト単体データ作成ツール（`tools/request_data_tool.rst`）

**元の v6 ページ**
- [リクエスト単体データ作成ツール](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/08_TestTools/01_HttpDumpTool/01_HttpDumpTool.html)
- [リクエスト単体データ作成ツール インストールガイド](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/08_TestTools/01_HttpDumpTool/02_SetUpHttpDumpTool.html)

**変えたことと理由**
- Linux 向けの `httpDump.sh` の案内を落とし、`httpDump.bat` だけを案内した
  - 配布物に `.sh` が無い
- 前提から「開発環境構築ガイドに従って構築済み」を落とした
  - 参照先のページが存在しない

### マスタデータ投入ツール（`tools/master_data_tool.rst`）

**元の v6 ページ**
- [マスタデータ投入ツール](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/08_TestTools/02_MasterDataSetup/01_MasterDataSetupTool.html)
- [マスタデータ投入ツール インストールガイド](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/08_TestTools/02_MasterDataSetup/02_ConfigMasterDataSetupTool.html)

**変えたことと理由**
- 前提を「アーキタイプから生成したプロジェクト」から「Maven の標準ディレクトリ構成」に広げた
  - ビルドファイルが依存するのはディレクトリ構成だけ
- 配布物にサンプルアプリケーションのデータが入っており、そのまま実行すると記述テーブルが置き換わることを警告した
- ターゲット表に動作（main は test へフォールバック、バックアップへコピーする範囲、失敗しても `BUILD SUCCESSFUL`）を書き足した
  - v6 では投入できたかを判断できなかったため

### HTMLチェックツール（`tools/html_check_tool.rst`）

**元の v6 ページ**
- [HTMLチェックツール](https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/08_TestTools/03_HtmlCheckTool/index.html)

**変えたことと理由**
- 画面を HTML5 で記述しているプロジェクトでは使用できないことを明示し、無効化・差し替えの節へ誘導した
  - v6 は触れていない
- 設定ファイルの書き損じで黙って壊れる事象と `htmlCheckerConfig` の副作用を実装から足し、指摘メッセージの形式を表にした

### テストデータ変換ツール（`tools/testdata_converter.rst`）

**元の v6 ページ**
- なし（`nablarch-testing-converter` の実装と設計資料から書き起こした）

**変えたことと理由**
- 変換で何が保たれ何が変わるかを機能概要に置いた
  - Excel 形式から移す読者には可否の判断が先に要る
- 設計資料に無い Maven プラグイン（`convert` ゴール）と Java から呼ぶ方法を実装から書き起こした
  - そのままでは使い始められない
- 変換結果を確かめる手段として、同じ形式への往復と `YamlTestDataValidator` を示した
  - 変換の経路には検証が組み込まれていないため
