.. _request_unit_test_batch:

リクエスト単体テスト（Nablarchバッチアプリケーション）
======================================================

.. contents:: 目次
  :depth: 3
  :local:

Nablarch\ バッチアプリケーションのリクエスト単体テストでは、コマンドラインからバッチを起動したときの動作を擬似的に再現する。応答不要メッセージ送信のテストも、\ Nablarch\ バッチアプリケーションのテストとしてこのページの方法で行う。

機能概要
--------------------------------------------------

テスティングフレームワークは、テスト用のメインクラスからテスト対象のバッチを起動する。テストクラスにはテストを起動するコードだけを書き、実行するテストショット・準備データ・入力ファイル・期待値はテストデータに記述する。

.. TODO(NTF-FIG-04): 構成図 batch_request_test_class.png を削除した。
   本文と3点食い違い（MainForRequestTesting#handle の引数順が実装と逆・
   Excelファイル表記・FileSupport が固定長ファイル限定の記述）、
   Sphinx に作図系拡張が無く作り直せないため。
   この図の作図元ファイルは存在しない。作図できる環境で作り直したうえで戻すこと。

テストクラスは、\ ``StandaloneTestSupportTemplate``\ を継承した\ ``BatchRequestTestSupport``\ を継承して作成する。テストデータを読み取り、テストショット1件分の情報を保持する\ ``TestShot``\ を1件ずつ実行する。テスト用のメインクラス\ ``MainForRequestTesting``\ を通じて\ Nablarch Application Framework\ が起動され、テスト対象のアプリケーションが実行される。準備データの投入とテスト結果の確認は、テーブルについては\ ``DbAccessTestSupport``\ が、ファイルについては\ ``FileSupport``\ が行う。

応答不要メッセージ送信は、送信する電文のデータを保持するテーブル（以降、一時テーブルと呼ぶ）から送信対象のデータを取得して電文を送信する、\ Nablarch\ バッチアプリケーションである。この処理を行う\ Action\ クラスは\ Nablarch\ の一部として提供される（\ :ref:`応答不要でメッセージを送信する(応答不要メッセージ送信) <mom_system_messaging-async_message_send>`\ ）。このため、リクエスト単体テストではその\ Action\ クラスを使用して、次の成果物を確認する。

* 電文のレイアウトを定義したフォーマット定義ファイル
* 次の3種類のSQL文

  * 一時テーブルからステータスが未送信のデータを取得するためのSELECT文
  * 電文送信後に、該当データのステータスを処理済みに更新するためのUPDATE文
  * 電文送信に失敗した場合に、該当データのステータスを送信失敗に更新するためのUPDATE文

応答不要メッセージ送信では、他の処理のような\ Action\ クラスに対する条件網羅や限界値テストは実施しない。

このページで扱う主なクラスとリソースを次に示す。

.. list-table::
  :header-rows: 1
  :widths: 30,45,25

  * - 名称
    - 役割
    - 作成単位
  * - リクエスト単体テストクラス
    - テストロジックを実装する。
    - テスト対象クラス（Action）につき1つ作成する。
  * - テストデータ
    - テーブルに格納する準備データや期待値、入力ファイルなどを記載する。
    - テストクラスにつき1つ作成する。
  * - ``StandaloneTestSupportTemplate``
    - バッチやメッセージング処理などコンテナ外で動作する処理のテスト実行環境を提供する。テストデータを読み取り、テストショットを1件ずつ実行する。
    - －
  * - ``BatchRequestTestSupport``
    - Nablarch\ バッチアプリケーションのリクエスト単体テストで必要となるテスト準備機能、各種アサートを提供する。
    - －
  * - ``TestShot``
    - テストデータに定義されたテストショット1件分の情報を保持し、実行する。
    - －
  * - ``MainForRequestTesting``
    - テスト用のメインクラス。テスト用のコンポーネント設定ファイルからシステムリポジトリを初期化し、テスト対象の実行後に元のリポジトリへ戻す。
    - －
  * - ``DbAccessTestSupport``
    - 準備データの投入や更新内容の確認など、データベースを使用するテストに必要な機能を提供する。
    - －
  * - ``FileSupport``
    - 入力ファイルの作成や出力ファイルの内容確認など、ファイルを使用するテストに必要な機能を提供する。
    - －

``FileSupport``\ が提供するファイルの操作は、ファイルダウンロードのテストなど\ Nablarch\ バッチアプリケーション以外のテストでも必要になる。このため、独立したクラスとして提供されている。

使用方法
--------------------------------------------------

Nablarch\ バッチアプリケーションのリクエスト単体テストは、テストクラスとテストデータを作成し、\ JUnit\ でテストを実行するという流れで進める。コンポーネント設定は\ :ref:`リクエスト単体テストの設定（Nablarchバッチアプリケーション） <request_unit_test_setting_batch>`\ に従ってあらかじめ済ませておく。

テストクラスを作成する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
テストクラスは、次の条件を満たすように作成する。

* パッケージは、テスト対象の\ Action\ クラスと同じとする。
* クラス名は\ ``<Actionクラス名>RequestTest``\ とする。
* :java:extdoc:`BatchRequestTestSupport <nablarch.test.core.batch.BatchRequestTestSupport>`\ を継承する。

テスト対象の\ Action\ クラスが\ ``nablarch.sample.ss21AA.RM21AA001Action``\ の場合、テストクラスは次のようになる。

.. code-block:: java

  package nablarch.sample.ss21AA;

  import nablarch.test.core.batch.BatchRequestTestSupport;

  public class RM21AA001ActionRequestTest extends BatchRequestTestSupport {
      // 中略
  }

応答不要メッセージ送信のテストクラスは、次の条件を満たすように作成する。テスト対象の\ Action\ クラスが\ Nablarch\ から提供されるため、パッケージとクラス名の決め方だけが異なる。

* パッケージは、テスト対象機能のパッケージとする。
* クラス名は\ ``<電文のリクエストID>RequestTest``\ とする。
* :java:extdoc:`BatchRequestTestSupport <nablarch.test.core.batch.BatchRequestTestSupport>`\ を継承する。

テスト対象機能のパッケージが\ ``nablarch.sample.ss21AA``\ 、電文のリクエスト\ ID\ が\ ``RM11AC0301``\ の場合、テストクラスは次のようになる。

.. code-block:: java

  package nablarch.sample.ss21AA;

  import nablarch.test.core.batch.BatchRequestTestSupport;

  public class RM11AC0301RequestTest extends BatchRequestTestSupport {
      // 中略
  }

.. tip::

  JUnit 5\ でテストを書く場合は、継承ではなくインジェクションでテスティングフレームワークの機能を使用する（\ :ref:`JUnit 5用拡張機能 <junit5_extension>`\ ）。

テストメソッドを作成する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1つのテストショットにつき1つのテストメソッドを作成することを原則とする。\ Nablarch\ バッチアプリケーションでは複数のレコードを一度に扱うため、テストデータが比較的多くなる。1つのテストメソッドに複数のテストショットを記述すると、1つの読み込み単位に大量のテストデータを記述することになり、可読性・保守性が低下する。

ただし、次のいずれかに当てはまる場合は、複数のテストショットを1つのテストメソッドにまとめて記述することを検討する。

* テストショット間の関連が強く、読み込み単位を分けると可読性が下がる場合（例えば、入力ファイルのフォーマットチェックのテストショット）
* テストデータが少量であり、1つの読み込み単位に記述しても可読性・保守性に影響しない場合

テストメソッドでは、スーパクラスの\ ``execute``\ を呼び出す。

.. code-block:: java

  @Test
  public void testRegisterUser() {
      execute();
  }

引数なしの\ ``execute``\ は、テストメソッド名と同じ名前の読み込み単位を読み込む。読み込み単位の名前をテストメソッド名と別にする場合は、読み込み単位の名前を引数に渡した\ ``execute``\ を呼ぶ。

.. code-block:: java

  @Test
  public void testRegister() {
      execute("testRegisterUser");   // 引数なしの execute() は execute("testRegister") を読み込む
  }

テストデータを作成する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
テストデータの格納場所と記述方法は\ :ref:`テストデータの書き方 <testdata_notation>`\ に従う。実行するテストショットは\ :ref:`テストショット一覧（testShots）を記述する <testdata_notation-test_shots>`\ に、テストクラス全体で共通する準備データは\ :ref:`共通の準備データをまとめる <testdata_notation-setupdb>`\ に従って記述する。記述例は\ :ref:`テストデータの記載例 <testdata_examples>`\ を参照。

応答不要メッセージ送信のテストデータは、同期応答メッセージ送信と同じ書式で記述する（\ :ref:`メッセージングのデータを記述する <testdata_notation-messaging_data>`\ ）。ここでは、応答不要メッセージ送信で記述方法が異なる箇所を説明する。

応答不要メッセージ送信では応答電文が存在しないため、応答電文が期待値どおりであることを確認する必要がない。このため、次の記述は不要である。

* テストショット一覧の\ ``responseMessage``
* 応答電文のデータブロック（\ ``RESPONSE_HEADER_MESSAGES``\ ・\ ``RESPONSE_BODY_MESSAGES``\ ）

正常系のテストでは、電文が想定どおりに送信されることと、一時テーブルの該当データのステータスが処理済みに更新されることを確認する。応答不要メッセージ送信の\ Action\ クラスは、起動パラメータとして電文のリクエスト\ ID\ を要求する。このため、テストショット一覧に\ ``messageRequestId``\ カラムを追加し、電文のリクエスト\ ID\ を値に記述する。テストショット一覧に追加した独自のカラムがコマンドラインオプションとして渡される仕組みは、\ :ref:`コマンドライン引数を指定する <testdata_notation-command_line>`\ を参照。送信される要求電文の期待値は、テストショット一覧の\ ``expectedMessage``\ にグループIDを記述して対応付ける。

異常系のテストでは、電文の送信に失敗した場合に該当データのステータスを送信失敗に更新するUPDATE文を確認する。テストショット一覧に\ ``errorCase``\ カラムを追加し、\ ``true``\ を値に記述する。異常系では電文が送信されないため、要求電文の期待値を記述する必要はない。\ ``expectedStatusCode``\ には、異常終了したときの終了コードを記述する。

.. important::

  異常系のテストを行うには、応答不要メッセージ送信の共通\ Action\ クラスを、テスト用の\ Action\ クラスに切り替える。切り替えないまま\ ``errorCase``\ を記述しても、正常系として実行される。本番用のコンポーネント設定ファイルに、次のようなディスパッチハンドラの設定があるとする。

  .. code-block:: xml

    <!-- ディスパッチ用ハンドラ -->
    <component name="requestPathJavaPackageMapping" class="nablarch.fw.handler.RequestPathJavaPackageMapping">
      <!-- 応答不要メッセージ送信用の共通アクションを設定する -->
      <property name="basePackage" value="nablarch.fw.messaging.action.AsyncMessageSendAction" />
      <property name="immediate" value="false" />
    </component>

  テスト用のコンポーネント設定ファイルでは、本番用のコンポーネント設定ファイルを取り込んだうえで、同じコンポーネント名の定義を置いて上書きする。

  .. code-block:: xml

    <!-- ディスパッチ用ハンドラをテスト用のアクションに置き換える設定 -->
    <component name="requestPathJavaPackageMapping" class="nablarch.fw.handler.RequestPathJavaPackageMapping">
      <property name="basePackage" value="nablarch.test.core.messaging.AsyncMessageSendActionForUt" />
      <property name="immediate" value="false" />
    </component>

テストを実行する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
通常の\ JUnit\ テストと同じように実行する。テストを実行すると、読み込み単位のテストショット一覧が読み込まれ、テストショットが上から順に実行される。1件のテストショットは、次の順で処理される。

1. 入力データの準備（データベースへの準備データの投入、入力ファイルの作成、期待するログの登録、要求電文の期待値の登録）
2. メインクラスの起動
3. 出力結果の確認

メインクラスには、テスト用の\ ``MainForRequestTesting``\ を使用する。このクラスは、テスト用のコンポーネント設定ファイルからシステムリポジトリを初期化し、テスト対象の実行後に元のリポジトリへ戻す。このメインクラスは、テスト対象のハンドラ構成によらず使用する。テスト対象のハンドラ構成にリクエストスレッド内ループ制御ハンドラが含まれる場合は、これに加えて、そのハンドラをテスト用のハンドラに置き換える必要がある（\ :ref:`リクエスト単体テストの設定（Nablarchバッチアプリケーション） <request_unit_test_setting_batch>`\ ）。

テスト結果を確認する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
テストショットごとに、ステータスコードの確認が行われる。テストショット一覧の\ ``expectedStatusCode``\ と、バッチの終了コードを照合する。\ ``expectedStatusCode``\ は必須カラムである。カラムを定義したうえで、期待する終了コードを必ず記述する。値を空にすると終了コードと一致せず、テストが失敗する。

このほか、次の確認が行われる。いずれも、テストショット一覧の該当するカラムが空欄の場合は行われない。

* データベースの更新内容の確認。テストショット一覧の\ ``expectedTable``\ に記述したグループIDの期待値と、テーブルの状態を照合する。
* 出力ファイルの内容の確認。テストショット一覧の\ ``expectedFile``\ に記述したグループIDの期待値と、出力されたファイルの内容を照合する。
* 要求電文の内容の確認。テストショット一覧の\ ``expectedMessage``\ に記述したグループIDの期待値と、送信された電文を照合する。
* ログの出力内容の確認。テストショット一覧の\ ``expectedLog``\ に記述したグループIDの期待値と、出力されたログを照合する。

各カラムの記述方法は\ :ref:`テストショット一覧（testShots）を記述する <testdata_notation-test_shots>`\ を、期待値のデータブロックの記述方法は\ :ref:`テストデータの書き方 <testdata_notation>`\ を参照。
