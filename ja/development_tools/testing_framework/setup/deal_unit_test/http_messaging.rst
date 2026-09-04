.. _deal_unit_test_setting_http_messaging:

取引単体テストの設定（HTTPメッセージング）
==================================================

.. contents:: 目次
  :depth: 3
  :local:

機能概要
--------------------------------------------------
HTTPメッセージ送信を伴う取引単体テストは、通信先を用意せずに実施する。電文を実際に送る代わりに、テストデータに記述した内容から応答電文を生成して返すモックアップクラスを登録する。テストの実装方法は\ :ref:`取引単体テスト（HTTPメッセージング） <deal_unit_test_http_messaging>`\ を参照。

使用方法
--------------------------------------------------

モックアップクラスを登録する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
HTTPメッセージ送信を伴う取引単体テストでは、テスティングフレームワークが提供するモックアップクラス\ :java:extdoc:`MockMessagingClient <nablarch.test.core.messaging.MockMessagingClient>`\ を使用する。このクラスを使用すると、電文の送信は行われず、テストデータに記述した内容から応答電文が生成されて返される。コンポーネント設定ファイルに、次のとおり登録する。

.. code-block:: xml

  <!-- HTTP通信用クライアント -->
  <component name="defaultRealTimeMessagingClient"
             class="nablarch.test.core.messaging.MockMessagingClient">
    <property name="charset" value="Shift-JIS"/>
  </component>

コンポーネント名の指定方法は\ :ref:`リクエスト単体テストの設定（HTTPメッセージング） <request_unit_test_setting_http_messaging>`\ と同じである。

``charset``\ には、\ :ref:`メッセージングログ <messaging_log>`\ に出力する電文の文字コード名を指定する。この項目は省略でき、省略した場合は\ ``UTF-8``\ が使用される。

応答電文のテストデータは、ベースディレクトリとテストデータを解析するコンポーネントをあわせて設定しないと読み込まれない。\ :ref:`同期応答メッセージ送信・HTTPメッセージ送信のテストデータの読み込みを設定する <deal_unit_test_setting_http_messaging-send_sync_test_data>`\ で設定する。

電文のフォーマットとデータの記述方法は\ :ref:`メッセージングのデータを記述する <testdata_notation-messaging_data>`\ を参照。

.. _deal_unit_test_setting_http_messaging-send_sync_test_data:

同期応答メッセージ送信・HTTPメッセージ送信のテストデータの読み込みを設定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
同期応答メッセージ送信・HTTPメッセージ送信を伴う取引単体テストでは、モックアップクラスが応答電文をテストデータから読み込む。この設定は、HTTPメッセージングと\ :ref:`MOMによるメッセージング <deal_unit_test_setting_mom>`\ で共通である。読み込みには、テストデータのベースディレクトリと、テストデータを解析するコンポーネントの設定が必要である。どちらもテスティングフレームワークのデフォルト設定には含まれないため、テスト用のコンポーネント設定ファイルに記述する。設定していない場合は、テストの実行時に例外が発生する。設定ファイルを環境ごとに切り替える方法は\ :ref:`環境ごとにコンポーネントを切り替える方法(モックに切り替える方法) <how_to_change_componet_define>`\ を参照。

テストデータのベースディレクトリは、\ :ref:`ファイルパス管理 <file_path_management>`\ の\ ``sendSyncTestData``\ というキーに設定する。同じコンポーネントに、電文のフォーマット定義ファイルのベースディレクトリ（\ ``format``\ ）も設定する。テストデータを解析するコンポーネントは、\ ``messagingTestDataParser``\ という名前で登録する。ベースディレクトリの配下でのファイル名の決まりは\ :ref:`メッセージングのデータを記述する <testdata_notation-messaging_data>`\ を参照。

ベースディレクトリの指定と、テストデータを解析するコンポーネント、テストデータの記法を解釈するクラス群の設定は、テストデータの形式によって異なる。\ Excel\ 形式と\ YAML\ 形式のそれぞれについて後述する。

ベースディレクトリ配下のテストデータの配置とデータセクションの対応を次に示す。

.. image:: ../images/http_messaging/send_sync_testdata_layout.png
  :scale: 100

.. tip::

  ベースディレクトリは、クラスパス（\ ``classpath:``\ ）ではなくファイルシステムのパス（\ ``file:``\ ）で指定することを推奨する。ファイルシステムのパスを指定すると、アプリケーションサーバの起動中にテストデータを編集して、そのままテストを続けられる。

Excel形式の場合
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: xml

  <!-- テストデータとフォーマット定義ファイルのベースディレクトリ -->
  <component name="filePathSetting"
             class="nablarch.core.util.FilePathSetting" autowireType="None">
    <property name="basePathSettings">
      <map>
        <entry key="sendSyncTestData" value="file:/path/to/test/message"/>
        <entry key="format" value="classpath:web/format"/>
      </map>
    </property>
    <property name="fileExtensions">
      <map>
        <entry key="sendSyncTestData" value="xlsx"/>
        <entry key="format" value="fmt"/>
      </map>
    </property>
  </component>

  <!-- テストデータを解析するコンポーネント -->
  <component name="messagingTestDataParser"
             class="nablarch.test.core.reader.BasicTestDataParser">
    <property name="testDataReader">
      <component class="nablarch.test.core.reader.PoiXlsReader"/>
    </property>
    <property name="interpreters">
      <list>
        <component-ref name="nullInterpreter"/>
        <component-ref name="quotationTrimmer"/>
        <component-ref name="compositeInterpreter"/>
      </list>
    </property>
  </component>

\ :ref:`特殊記法 <testdata_notation-special_notation>`\ を解釈するクラス（Interpreter）は、\ :ref:`テスト用のコンポーネント設定ファイル <testing_framework_introduction-test_component_config>`\ がimportしているデフォルト設定\ ``nablarch/test/test-data.xml``\ に定義されているもののうち、次の3つを指定する。

* ``nullInterpreter``

  * ``null``\ と書いたセルを\ Java\ の\ null\ に変換する

* ``quotationTrimmer``

  * ダブルクォートで囲んだセルから、前後のダブルクォートを外す

* ``compositeInterpreter``

  * ``${文字種,文字数}``\ を、その文字種の文字列に変換する

``fileExtensions``\ の\ ``sendSyncTestData``\ には、実際に配置するテストデータのファイルの拡張子（\ ``xlsx``\ または\ ``xls``\ ）を指定する。指定した拡張子と一致しないファイルは読み込まれない。ベースディレクトリの配下には、リクエストIDごとに1つのファイルを置く。

YAML形式の場合
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: xml

  <!-- テストデータとフォーマット定義ファイルのベースディレクトリ -->
  <component name="filePathSetting"
             class="nablarch.core.util.FilePathSetting" autowireType="None">
    <property name="basePathSettings">
      <map>
        <entry key="sendSyncTestData" value="file:/path/to/test/message"/>
        <entry key="format" value="classpath:web/format"/>
      </map>
    </property>
    <property name="fileExtensions">
      <map>
        <entry key="format" value="fmt"/>
      </map>
    </property>
  </component>

  <!-- テストデータを解析するコンポーネント -->
  <component name="messagingTestDataParser"
             class="nablarch.test.core.reader.YamlTestDataParser">
    <property name="interpreters">
      <list>
        <component-ref name="compositeInterpreter"/>
      </list>
    </property>
  </component>

``interpreters``\ に指定するのは、\ ``${文字種,文字数}``\ をその文字種の文字列に変換する\ ``compositeInterpreter``\ だけでよい。null・空文字・ダブルクォートは\ YAML\ の構文が担うため、\ Excel\ 形式で指定する\ ``nullInterpreter``\ ・\ ``quotationTrimmer``\ は指定しない。\ ``testDataReader``\ は指定しない。\ :java:extdoc:`YamlTestDataParser <nablarch.test.core.reader.YamlTestDataParser>`\ は\ YAML\ ファイルを直接読み込むため、この設定を使用しない。

.. important::

  ``fileExtensions``\ には\ ``sendSyncTestData``\ を設定しない。\ YAML\ 形式ではリクエストIDと同じ名前のディレクトリを参照するため、拡張子を設定するとテストデータが見つからず、テストの実行時に例外が発生する。
