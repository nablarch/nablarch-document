.. _request_unit_test_setting_web:

リクエスト単体テストの設定（ウェブアプリケーション）
====================================================

.. contents:: 目次
  :depth: 3
  :local:

機能概要
--------------------------------------------------
ウェブアプリケーションのリクエスト単体テストは、デフォルト設定\ ``nablarch/test/http-request-test.xml``\ を読み込むと必要なコンポーネントが登録され、実行できる状態になる。このページの設定は、HTMLダンプの出力先やHTMLチェックの有無など、実行環境やプロジェクトの規約に合わせて変えたい項目を上書きするためのものである。HTMLダンプのために行うHTMLリソースのコピーを抑止して、テストの実行時間を短くする方法もここで示す。テストの実装方法は\ :ref:`リクエスト単体テスト（ウェブアプリケーション） <request_unit_test_web>`\ を参照。

使用方法
--------------------------------------------------

コンポーネント設定ファイルに設定項目を登録する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
デフォルト設定（\ ``nablarch/test/http-request-test.xml``\ ）を読み込むと、\ :java:extdoc:`HttpTestConfiguration <nablarch.test.core.http.HttpTestConfiguration>`\ が\ ``httpTestConfiguration``\ というコンポーネント名で登録される。実行環境に依存する設定値は、このコンポーネントを同じ名前で上書きして変更する。上書きの記述は、デフォルト設定の読み込みより後に置く。主な設定項目は次のとおりである。デフォルト値の欄には、デフォルト設定を読み込んだ状態で有効になる値を示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 1
  :widths: 22,48,30

  * - 設定項目名
    - 説明
    - デフォルト値
  * - ``htmlDumpDir``
    - HTMLダンプを出力するディレクトリ（以下、ダンプディレクトリ）
    - ``./tmp/html_dump``
  * - ``webBaseDir``
    - ウェブアプリケーションのルートディレクトリ
    - ``src/main/webapp``
  * - ``xmlComponentFile``
    - リクエスト単体テストの実行時に使用するコンポーネント設定ファイル
    - 該当なし
  * - ``userIdSessionKey``
    - ログイン中のユーザIDを格納するセッションスコープのキー
    - ``user.id``
  * - ``exceptionRequestVarKey``
    - \ :java:extdoc:`ApplicationException <nablarch.core.message.ApplicationException>`\ が格納されるリクエストスコープのキー
    - ``nablarch_application_error``
  * - ``dumpFileExtension``
    - HTMLダンプの拡張子
    - ``html``
  * - ``httpHeader``
    - HTTPリクエストヘッダとして送信する値
    - ``Content-Type``\ が\ ``application/x-www-form-urlencoded``\ 、\ ``Accept-Language``\ が\ ``ja JP``
  * - ``sessionInfo``
    - セッションスコープに格納する値
    - ``commonHeaderLoginUserName``\ が\ ``リクエスト単体テストユーザ``\ 、\ ``commonHeaderLoginDate``\ が\ ``20100914``
  * - ``htmlResourcesExtensionList``
    - ダンプディレクトリへコピーするHTMLリソースの拡張子
    - ``css``\ ・\ ``jpg``\ ・\ ``js``\ ・\ ``less``\ ・\ ``png``\ ・\ ``template``\ ・\ ``woff``\ ・\ ``eot``\ ・\ ``svg``\ ・\ ``ttf``
  * - ``jsTestResourceDir``
    - JavaScriptの自動テストで使用するリソースを配置したディレクトリ
    - ``src/test/webapp``
  * - ``backup``
    - ダンプディレクトリをバックアップするかどうか
    - ``true``
  * - ``htmlResourcesCharset``
    - パスの書き換え対象となるHTMLリソースの文字コード。\ ``css``\ ・\ ``js``\ ・\ ``template``\ は、\ ``htmlResourcesExtensionList``\ の指定によらず書き換えの対象になる
    - ``UTF-8``
  * - ``checkHtml``
    - HTMLチェックを実施するかどうか
    - ``true``
  * - ``htmlChecker``
    - HTMLチェックを行うオブジェクト。\ :java:extdoc:`HtmlChecker <nablarch.test.tool.htmlcheck.HtmlChecker>`\ を実装したクラスのインスタンスを指定する。詳細は\ :ref:`HTMLチェックツール <html_check_tool>`\ を参照
    - ``htmlCheckerConfig``\ の設定に伴って設定される\ :java:extdoc:`Html4HtmlChecker <nablarch.test.tool.htmlcheck.Html4HtmlChecker>`
  * - ``htmlCheckerConfig``
    - HTMLチェックツールの設定ファイルのパス。この項目を設定すると、指定した設定ファイルを適用した\ :java:extdoc:`Html4HtmlChecker <nablarch.test.tool.htmlcheck.Html4HtmlChecker>`\ が\ ``htmlChecker``\ に設定される
    - ``src/test/resources/nablarch/test/http-request-test/html-check-config.csv``
  * - ``ignoreHtmlResourceDirectory``
    - HTMLリソースのうちコピー対象外とするディレクトリ名のリスト
    - ``.svn``
  * - ``tempDirectory``
    - JSPのコンパイル先ディレクトリ
    - ``target/tmp``
  * - ``uploadTmpDirectory``
    - アップロードファイルを一時的に格納するディレクトリ。テストで準備したアップロード対象のファイルは、このディレクトリにコピーしてから処理される。アップロード対象のファイルそのものが移動されることを防ぐためである
    - ``./tmp``
  * - ``dumpVariableItem``
    - HTMLダンプから可変項目を除去するかどうか。可変項目とは、JSESSIONIDと二重サブミット防止用のトークンを指す。いずれもテストの実行ごとに異なる値になるため、HTMLダンプを毎回同じ内容にしたい場合は\ ``true``\ を指定する。プロパティ名から受ける印象とは逆の意味である点に注意する
    - ``false``

.. important::

  ``checkHtml``\ を\ ``true``\ のままにする場合は、\ ``htmlChecker``\ と\ ``htmlCheckerConfig``\ のどちらか一方が設定されている必要がある。どちらも設定されていないと、ステータスコードが500未満のHTMLレスポンスに対するHTMLチェックの実行時に例外が発生する。デフォルト設定では\ ``htmlCheckerConfig``\ が設定されるため、デフォルト設定を読み込んでいる場合にこの状態は生じない。デフォルト設定を読み込まずにコンポーネント設定ファイルを組み立てる場合に注意する。

``webBaseDir``\ には、カンマ区切りで複数のディレクトリを指定できる。プロジェクト共通のウェブモジュールがある場合など、ルートディレクトリが複数に分かれているときに使用する。指定した順にリソースが探索される。

.. code-block:: xml

  <property name="webBaseDir" value="/path/to/web-a/,/path/to/web-common"/>

``xmlComponentFile``\ を設定すると、リクエストの送信直前に、指定したコンポーネント設定ファイルでシステムリポジトリが再初期化される。通常は設定する必要はない。クラス単体テストとリクエスト単体テストとで設定を変える必要がある場合にのみ設定する。

.. tip::

  ``ignoreHtmlResourceDirectory``\ にバージョン管理用のディレクトリ（\ ``.svn``\ や\ ``.git``\ ）を指定すると、HTMLリソースをコピーする際のパフォーマンスが向上する。

.. tip::

  デフォルト設定を読み込まず、\ ``tempDirectory``\ も指定しない場合は、内蔵サーバ（Jetty）のデフォルト動作により\ ``./work``\ がコンパイル先ディレクトリになる。\ ``./work``\ が存在しない場合は、OSの一時ディレクトリが出力先になる。

記述例を示す。\ ``sessionInfo``\ には次の値を設定している。デフォルト値と同じ値を明示的に記述している項目もある。

.. list-table::
  :class: white-space-normal
  :header-rows: 1
  :widths: 30,25,45

  * - キー
    - 値
    - 説明
  * - ``commonHeaderLoginUserName``
    - ``リクエスト単体テストユーザ``
    - 共通ヘッダ領域に表示するログインユーザ名
  * - ``commonHeaderLoginDate``
    - ``20100914``
    - 共通ヘッダ領域に表示するログイン日時

.. code-block:: xml

  <component name="httpTestConfiguration" class="nablarch.test.core.http.HttpTestConfiguration">
    <property name="htmlDumpDir" value="./tmp/html_dump"/>
    <property name="webBaseDir" value="src/main/webapp"/>
    <property name="xmlComponentFile" value="http-request-test.xml"/>
    <property name="userIdSessionKey" value="user.id"/>
    <property name="httpHeader">
      <map>
        <entry key="Content-Type" value="application/x-www-form-urlencoded"/>
        <entry key="Accept-Language" value="ja JP"/>
      </map>
    </property>
    <property name="sessionInfo">
      <map>
        <entry key="commonHeaderLoginUserName" value="リクエスト単体テストユーザ"/>
        <entry key="commonHeaderLoginDate" value="20100914"/>
      </map>
    </property>
    <property name="htmlResourcesExtensionList">
      <list>
        <value>css</value>
        <value>js</value>
        <value>jpg</value>
      </list>
    </property>
    <property name="backup" value="true"/>
    <property name="htmlResourcesCharset" value="UTF-8"/>
    <property name="ignoreHtmlResourceDirectory">
      <list>
        <value>.svn</value>
      </list>
    </property>
    <property name="tempDirectory" value="webTemp"/>
    <property name="htmlCheckerConfig"
      value="src/test/resources/nablarch/test/http-request-test/html-check-config.csv"/>
  </component>

HTMLリソースのコピーを抑止する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
テストの実行時に次のシステムプロパティを指定すると、\ :ref:`リクエスト単体テスト（ウェブアプリケーション） <request_unit_test_web>`\ のHTMLダンプの出力時に、HTMLリソースをコピーしなくなる。CSSや画像ファイルなどの静的なHTMLリソースを頻繁に編集しない場合は、テストを実行するたびにHTMLリソースをコピーする必要はないため、このシステムプロパティを設定してもよい。

.. code-block:: bash

  -Dnablarch.test.skip-resource-copy=true

.. important::

  このシステムプロパティを指定するとHTMLリソースがコピーされなくなるため、CSSなどのHTMLリソースを編集してもHTMLダンプに反映されない。

.. tip::

  ダンプディレクトリ配下のHTMLリソースのコピー先ディレクトリ（デフォルトは\ ``../htmlResources``\ ）が存在しない場合は、このシステムプロパティの指定の有無にかかわらず、HTMLリソースのコピーが実行される。

Eclipseで指定する場合は、実行構成の「引数(Arguments)」タブの「VM 引数(VM Arguments)」欄に記述する。

.. image:: images/web/skip_resource_copy.png
  :scale: 100

拡張例
--------------------------------------------------

テストデータの書き方を拡張する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
テストデータの書き方を変える場合は、\ :java:extdoc:`AbstractHttpRequestTestTemplate <nablarch.test.core.http.AbstractHttpRequestTestTemplate>`\ と\ :java:extdoc:`TestCaseInfo <nablarch.test.core.http.TestCaseInfo>`\ を継承する。

``AbstractHttpRequestTestTemplate``\ は、リクエスト単体テストのサポートクラスである\ ``BasicHttpRequestTestTemplate``\ のスーパクラスである。アプリケーションプログラマが直接使用することはなく、テスティングフレームワークを拡張する際に用いる。\ ``TestCaseInfo``\ はテストデータに定義されたテストショットの情報を格納するクラスで、\ ``AbstractHttpRequestTestTemplate``\ の型引数に指定する。
