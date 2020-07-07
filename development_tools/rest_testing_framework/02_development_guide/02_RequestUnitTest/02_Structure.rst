----
構造
----

SimpleRestTestSupport
=========================================

リクエスト単体テスト用に用意されたスーパークラス。リクエスト単体テスト用のメソッドを用意している。
データベース関連機能が不要な場合は後述の ``RestTestSupport`` ではなくこちらのクラスを使用する。
:ref:`事前準備補助機能<rest_test_helper>` 、 :ref:`実行<rest_test_execute>` 、 :ref:`結果確認<rest_test_assert>` については以下の ``RestTestSupport`` と同じ機能を持つ。

.. tip::

  RestTestSupportを使用する場合、``dbInfo`` または ``testDataParser`` のコンポーネントを準備する必要がある。
  データベースへの依存が不要な場合は、``SimpleRestTestSupport`` を使用することでコンポーネント定義を簡略化できる。

RestTestSupport
=========================================

リクエスト単体テスト用に用意されたスーパークラス。リクエスト単体テスト用のメソッドを用意している。
``SimpleRestTestSupport`` を継承し、データベース関連機能を持つ。


データベース関連機能
--------------------

データベースに関する機能は、 ``RestTestSupport`` クラスから ``DbAccessTestSupport`` クラスに処理を委譲することで実現している。
``DbAccessTestSupport`` クラスの詳細は、\ :doc:`../../../testing_framework/guide/development_guide/06_TestFWGuide/02_DbAccessTest`\ を参照。

ただし、 ``DbAccessTestSupport`` のうち以下のメソッドは、\
リクエスト単体テスト(REST)では不要であり、アプリケーションプログラマに誤解を与えないよう、\
意図的に委譲を行っていない。

* ``public void beginTransactions()``
* ``public void commitTransactions()``
* ``public void endTransactions()``
* ``public void setThreadContextValues(String sheetName, String id)``
* ``public void assertSqlResultSetEquals(String message, String sheetName, String id, SqlResultSet actual)``
* ``public void assertSqlRowEquals(String message, String sheetName, String id, SqlRow actual)``

.. important::

  利用者の利便性を考慮し、データベース関連機能の委譲を行っている。\
  しかしRESTfulウェブサービスの単体テストにおいては、委譲された ``assertTableEquals`` などを使って
  データベースのテーブル内容を確認するテストより、サービスとして公開されたAPIに問い合わせることで
  データベースに依存することなくシステムが持つデータを確認するテストを推奨する。


.. _rest_test_helper:

事前準備補助機能
----------------

内蔵サーバへのリクエスト送信には、 ``HttpRequest`` のインスタンスが必要となる。\
``RestTestSupport`` クラスでは、 ``HttpRequest`` をリクエスト単体テスト用に拡張した\
``RestMockHttpRequest`` のオブジェクトを簡単に作成できるよう\
4つのメソッドを用意している。\

.. code-block:: java

  RestMockHttpRequest get(String uri)
  RestMockHttpRequest post(String uri)
  RestMockHttpRequest put(String uri)
  RestMockHttpRequest delete(String uri)


引数には、以下の値を引き渡す。

* テスト対象となるリクエストURI

これらのメソッドでは、受け取ったリクエストURIを元に ``RestMockHttpRequest`` インスタンスを生成し、\
メソッド名に応じたHTTPメソッドを設定した上で返却する。\
リクエストパラメータなどURI以外のデータを設定したい場合は、\
本メソッド呼び出しにより取得したインスタンスに対してデータの設定を行うとよい。

.. tip::

  ``RestMockHttpRequest`` は流れるようなインターフェイスでパラメータなどを設定できるよう
  メソッドをオーバーライドして自身のインスタンスを返すようにしてある。
  使用できるメソッドの詳細は :java:extdoc:`Javadoc <nablarch.fw.web.RestMockHttpRequest>` を参照

  リクエストを構築する例

  .. code-block:: java

    RestMockHttpRequest request = post("/projects")
                                      .setHeader("Authorization","Bearer token")
                                      .setCookie(cookie);

.. _rest_test_execute:

実行
====

``RestTestSupport``  にある下記のメソッドを呼び出すことで、\
内蔵サーバが起動されリクエストが送信される。

.. code-block:: java

 HttpResponse sendRequest(HttpRequest request)

.. _rest_test_assert:

結果確認
========


ステータスコード
-----------------

``RestTestSupport`` にある下記のメソッドを呼び出すことで、\
レスポンスのHTTPステータスコードが想定通りであることを確認する。

.. code-block:: java

   
  void assertStatusCode(String message, HttpResponse.Status expected, HttpResponse response);


引数には、以下の値を引き渡す。

* アサート失敗時のメッセージ
* 期待するステータス( ``HttpResponse.Status`` のEnum)
* 内蔵サーバから返却された ``HttpResponse`` インスタンス


期待するステータスコードとレスポンスのステータスコードが一致しなかった場合\
アサート失敗となる。


レスポンスボディ
----------------

レスポンスボディの検証についてはフレームワークでは仕組みを用意していない。
各プロジェクトの要件に合わせて `JSONAssert(外部サイト、英語) <http://jsonassert.skyscreamer.org/>`_ や
`json-path-assert(外部サイト、英語) <https://github.com/json-path/JsonPath/tree/master/json-path-assert>`_ 、
`XMLUnit(外部サイト、英語) <https://github.com/xmlunit/user-guide/wiki>`_ などのライブラリを使用すること。

.. tip::

  \ :doc:`RESTfulウェブサービスのブランクプロジェクト <../../../../application_framework/application_framework/blank_project/setup_blankProject/setup_WebService>`\ を作成した場合
  上記の `JSONAssert(外部サイト、英語) <http://jsonassert.skyscreamer.org/>`_ 、
  `json-path-assert(外部サイト、英語) <https://github.com/json-path/JsonPath/tree/master/json-path-assert>`_ 、
  `XMLUnit(外部サイト、英語) <https://github.com/xmlunit/user-guide/wiki>`_ がpom.xmlに記載されている。
  必要に応じてライブラリの削除や差し替えを行うこと。


レスポンスボディ検証の補助機能
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

レスポンスボディの検証をする際に、期待されるボディをJSONファイルやXMLファイルとして用意したい場合がある。
JSONAssertのように外部ライブラリが期待値として ``String`` しか引数に受け付けない場合に対応するため
``RestTestSupport`` にはファイルを読み込み ``String`` に変換するメソッドを用意している。

.. code-block:: java

  String readTextResource(String fileName)

このメソッドでは、以下のようにテストクラスと同じ名前のディレクトリにあるリソースから
引数で指定したファイル名でファイルを読み込み ``String`` に変換する。

+----------------------------------+------------------------------------------------------+-------------------------------------+
| ファイルの種類                   | 配置ディレクトリ                                     | ファイル名                          |
+==================================+======================================================+=====================================+
| テストクラスソースファイル       | <PROJECT_ROOT>/test/java/com/example/                | SampleTest.java                     |
+----------------------------------+------------------------------------------------------+-------------------------------------+
| レスポンスボディの期待値ファイル | <PROJECT_ROOT>/test/resources/com/example/SampleTest | response.json(引数のfileNameに指定) |
+----------------------------------+------------------------------------------------------+-------------------------------------+

