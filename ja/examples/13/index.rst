
=====================================================
Logbookを用いたリクエスト/レスポンスログ出力サンプル
=====================================================

--------------
提供パッケージ
--------------

`ソースコード <https://github.com/nablarch/nablarch-biz-sample-all>`_

本サンプルは、以下のパッケージで提供される。

  *please.change.me.*\ **common.log.logbook**

--------------
概要
--------------

本サンプルは、 `Logbook <https://github.com/zalando/logbook>`_ を用いてHTTPリクエストおよびレスポンスのログ出力を行うサンプルである。

.. important::

  Logbook を使用するためには、Javaのバージョンを 11 以上にする必要がある。
  そのため、本サンプルでは Java 11を使用する。

~~~~~~~~~~~~~~~~~~~~~~~~~
本サンプルで取り扱う範囲
~~~~~~~~~~~~~~~~~~~~~~~~~

Logbookは様々なメッセージ形式や出力方法に対応しているが、本サンプルでは以下の実装を取り扱う。

* Logbookのログ出力には、Nablarchのログ出力機能を使用する

  * Nablarchとの連携は :ref:`SLF4Jアダプタ <slf4j_adaptor>` を使用して実現する
  * ログは標準出力に出力する

* リクエスト送信にはJAX-RSクライアントを使用し、メッセージの形式にはJSONを使用する

  * JAX-RSクライアントの実装として Jersey を使用する

* `JsonPath <https://github.com/json-path/JsonPath>`_ を使用して、JSON形式の特定項目に対してマスク処理を行う

--------------
使用方法
--------------

~~~~~~~~~~~~~~~~~~~~~~~~~
依存ライブラリの追加
~~~~~~~~~~~~~~~~~~~~~~~~~

Logbook、Jersey、SLF4Jアダプタを使用可能にするため、プロジェクトの依存関係設定に以下の依存関係を追加する。
Logbookでは使用環境に応じたモジュールがいくつか公開されているため、それらも合わせて追加する。

.. code-block:: xml

  <dependencies>
    ...
    <!-- SLF4Jアダプタ -->
    <dependency>
      <groupId>com.nablarch.integration</groupId>
      <artifactId>slf4j-nablarch-adaptor</artifactId>
      <scope>runtime</scope>
    </dependency>

    <!-- Logbook -->
    <dependency>
      <groupId>org.zalando</groupId>
      <artifactId>logbook-core</artifactId>
      <version>2.16.0</version>
    </dependency>
    <dependency>
      <groupId>org.zalando</groupId>
      <artifactId>logbook-jaxrs</artifactId>
      <version>2.16.0</version>
    </dependency>
    <dependency>
      <groupId>org.zalando</groupId>
      <artifactId>logbook-json</artifactId>
      <version>2.16.0</version>
    </dependency>

    <!-- Jersey -->
    <dependency>
      <groupId>org.glassfish.jersey.core</groupId>
      <artifactId>jersey-client</artifactId>
      <version>2.35</version>
    </dependency>
    <dependency>
      <groupId>org.glassfish.jersey.media</groupId>
      <artifactId>jersey-media-json-jackson</artifactId>
      <version>2.35</version>
    </dependency>
    <dependency>
      <groupId>org.glassfish.jersey.inject</groupId>
      <artifactId>jersey-hk2</artifactId>
      <version>2.35</version>
    </dependency>
    ...
  </dependencies>

.. tip::

  本サンプルでは、Jerseyは :ref:`JAX-RSアダプタ <jaxrs_adaptor>` が使用しているJacksonのバージョンを考慮したバージョンを使用している。
  依存関係に指定するバージョンについては、実行環境に合わせて適切なバージョンを設定すること。


~~~~~~~~~~~~~~~~~~~~~~~~~
log.propertiesの設定
~~~~~~~~~~~~~~~~~~~~~~~~~

Nablarchのログ出力機能でLogbookのログを出力するため、 **log.properties** に以下の設定を行う。
なお、LogbookはログレベルをTRACEに設定する必要があるため、Logbook用のロガーを定義することを推奨する。

* LogbookはTRACEレベルでログ出力を行うため、ログレベルをTRACEに設定する
* ログの出力先を設定する

本サンプルでは、出力先に :java:extdoc:`StandardOutputLogWriter (標準出力へ出力) <nablarch.core.log.basic.StandardOutputLogWriter>` を設定する。

.. code-block:: properties

  ...
  # 標準出力
  writer.stdout.className=nablarch.core.log.basic.StandardOutputLogWriter
  writer.stdout.formatter.className=nablarch.core.log.basic.BasicLogFormatter
  writer.stdout.formatter.format=$date$ -$logLevel$- $runtimeLoggerName$ [$executionId$] boot_proc = [$bootProcess$] proc_sys = [$processingSystem$] req_id = [$requestId$] usr_id = [$userId$] $message$$information$$stackTrace$
  ...
  # 利用可能なロガー名順序
  availableLoggersNamesOrder=DEV,PER,SQL,MON,ACC,LOGBOOK,ROO
  ...
  # Logbookの設定
  loggers.LOGBOOK.nameRegex=org\\.zalando\\.logbook\\..*
  loggers.LOGBOOK.level=TRACE
  loggers.LOGBOOK.writerNames=stdout
  ...


Nablarchのログ出力設定については、 :ref:`log-basic_setting` を参照。

.. _logbook_settings:

~~~~~~~~~~~~~~~~~~~~~~~~~~~
Logbookの構成
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Logbookを使用するには、必要な設定を行った Logbook クラスのインスタンスを生成する。

デフォルト設定では、すべてのリクエストおよびレスポンスのボディを含む情報が出力される。

.. code-block:: java

  // Logbookを生成（デフォルト設定）
  Logbook logbook = Logbook.builder().build();

Logbookには様々な設定があり、出力条件を設定する condition やマスク処理を設定する Filtering 等を設定できる。
例えばボディのマスク処理を行う場合は、BodyFilterメソッドで値を置換するFilterを設定することで実現できる。

.. code-block:: java

  // Logbookを生成（ボディの id 項目をマスクする設定）
  Logbook logbook = Logbook.builder()
          .bodyFilter(jsonPath("$.id").replace("*****"))
          .build();

.. code-block:: java

  // Logbookを生成（ボディにある配列内の id と username 項目をマスクする設定）
  Logbook logbook = Logbook.builder()
          .bodyFilter(JsonPathBodyFilters.jsonPath("$[*].id").replace("*****"))
          .bodyFilter(JsonPathBodyFilters.jsonPath("$[*].username").replace("*****"))
          .build();

各種設定の詳細については、 `LogbookのREADME <https://github.com/zalando/logbook/blob/main/README.md>`_ を参照。

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
JAX-RSクライアントにLogbookを登録
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

生成した Logbook インスタンスは使用するクライアントに登録することで使用できる。

Logbookでは様々なクライアントに登録するためのクラスが提供されており、
本サンプルではJAX-RSクライアントを使用するため、 LogbookClientFilter クラスを使用する。

.. code-block:: java

  // JAX-RSクライアントにLogbookを登録
  Client client = ClientBuilder.newClient()
                    .register(new LogbookClientFilter(logbook));

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
リクエスト/レスポンスのログを出力
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Logbookを登録したJAX-RSクライアントでリクエストを送信、およびレスポンスを受信すると、ログが出力される。

.. code-block:: java

  Response response = client.target("http://localhost:3000")
                        .path("/users")
                        .request()
                        .get();

本サンプルでは出力先を標準出力に設定しているため、標準出力に以下のようなログが出力される。
Nablarchのログ出力機能に設定しているフォーマットで出力され、メッセージ部分だけが Logbook で設定しているフォーマットで出力される。
Logbookの デフォルトフォーマットでは、メッセージの種類（リクエスト送信かレスポンス受信か）、ヘッダ、ボディが出力される。

* リクエストのログ

.. code-block:: text

  2023-05-11 09:38:06.438 -TRACE- org.zalando.logbook.Logbook [202305110938060580001] boot_proc = [] proc_sys = [jaxrs] req_id = [/logbook/get] usr_id = [guest] Outgoing Request: bb068bcf35bc5226
  Remote: localhost
  GET http://localhost:3000/users HTTP/1.1

* レスポンスのログ

.. code-block:: text

  2023-05-11 09:38:06.496 -TRACE- org.zalando.logbook.Logbook [202305110938060580001] boot_proc = [] proc_sys = [jaxrs] req_id = [/logbook/get] usr_id = [guest] Incoming Response: bb068bcf35bc5226
  Duration: 57 ms
  HTTP/1.1 200 OK
  Connection: keep-alive
  Content-Length: 213
  Content-Type: application/json; charset=utf-8
  Date: Thu, 11 May 2023 00:38:06 GMT
  Keep-Alive: timeout=5

  [{"id":"81b8b153-5ed5-4d42-be13-346f257b368d","username":"Chasity91"},{"id":"6b1e7b91-6a1f-4424-be3c-4e3d28dd59c0","username":"Felton_Rohan"},{"id":"622677a4-04e3-4b70-85dd-a0b7f7161678","username":"Bella_Purdy"}]

前述の :ref:`Logbookの構成 <logbook_settings>` で説明したマスク処理を設定している場合は、上記のログにあるボディが変換され、以下のように出力される。
（ここでは、ボディにある配列内の id と username 項目をマスクする設定にしている）

.. code-block:: text

  2023-05-11 09:48:37.513 -TRACE- org.zalando.logbook.Logbook [202305110948374650002] boot_proc = [] proc_sys = [jaxrs] req_id = [/logbook/get/mask] usr_id = [guest] Incoming Response: e1ba3d95197a4539
  Duration: 9 ms
  HTTP/1.1 200 OK
  Connection: keep-alive
  Content-Length: 213
  Content-Type: application/json; charset=utf-8
  Date: Thu, 11 May 2023 00:48:37 GMT
  Keep-Alive: timeout=5

  [{"id":"*****","username":"*****"},{"id":"*****","username":"*****"},{"id":"*****","username":"*****"}]
