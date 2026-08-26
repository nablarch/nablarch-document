.. _deal_unit_test_setting_rest:

取引単体テストの設定（RESTfulウェブサービス）
==================================================

.. contents:: 目次
  :depth: 3
  :local:

機能概要
--------------------------------------------------

RESTfulウェブサービスの取引単体テストでは、実装クラスをコンポーネント設定ファイルに登録することで、サーバが発行したセッションIDやCSRFトークンを後続のリクエストへ引き継げる。引き継ぐ処理はテスティングフレームワークが提供する実装から選べるほか、独自に作成したクラスに差し替えることもできる。テストの実装方法は\ :ref:`取引単体テスト（RESTfulウェブサービス） <deal_unit_test_rest>`\ を参照。

使用方法
--------------------------------------------------

前のレスポンスの値を次のリクエストに引き継ぐ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1つの取引を複数のリクエストで構成する場合、先行するリクエストのレスポンスに現れた値を、次に送るリクエストへ持ち越したいことがある。この持ち越しは、リクエストとレスポンスを操作する\ :java:extdoc:`RequestResponseProcessor <nablarch.test.core.http.RequestResponseProcessor>`\ の実装クラスが担う。

実装クラスは、テスト用のコンポーネント設定ファイルに\ ``defaultProcessor``\ という名前で登録する。登録すると、内蔵サーバへリクエストを送る直前に\ :java:extdoc:`processRequest <nablarch.test.core.http.RequestResponseProcessor.processRequest(nablarch.fw.web.HttpRequest)>`\ が、レスポンスを受け取った直後に\ :java:extdoc:`processResponse <nablarch.test.core.http.RequestResponseProcessor.processResponse(nablarch.fw.web.HttpRequest,nablarch.fw.web.HttpResponse)>`\ が呼び出される。

テスティングフレームワークは、クッキーを引き継ぐ実装として\ :java:extdoc:`RequestResponseCookieManager <nablarch.test.core.http.RequestResponseCookieManager>`\ を用意している。この実装クラスは、レスポンスの\ ``Set-Cookie``\ ヘッダに現れるクッキーのうち、\ ``cookieName``\ プロパティに指定した名前のものを取り出し、次のリクエストの\ ``Cookie``\ ヘッダに設定する。

.. important::

  ``cookieName``\ は必須のプロパティである。指定していないと、レスポンスの処理時に例外が発生する。

.. code-block:: xml

  <component name="defaultProcessor" class="nablarch.test.core.http.RequestResponseCookieManager">
    <property name="cookieName" value="JSESSIONID"/>
  </component>

クッキーのうち\ :ref:`セッションストア <session_store>`\ のセッションIDに特化した実装として、\ :java:extdoc:`NablarchSIDManager <nablarch.test.core.http.NablarchSIDManager>`\ も提供している。この実装クラスは、\ :ref:`セッション変数保存ハンドラ <session_store_handler>`\ がセッションIDを保持する際のデフォルトのクッキー名\ ``NABLARCH_SID``\ をクッキー名の初期値に持つ。そのため\ ``cookieName``\ を指定しなくてよい。

セッションIDのクッキー名をデフォルトから変更している場合は、\ ``RequestResponseCookieManager``\ を使用してクッキー名を明示する。

複数の値をまとめて引き継ぐ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
引き継ぐ値が複数あり、\ :java:extdoc:`RequestResponseProcessor <nablarch.test.core.http.RequestResponseProcessor>`\ の実装クラスを複数使用したい場合がある。このときは\ :java:extdoc:`ComplexRequestResponseProcessor <nablarch.test.core.http.ComplexRequestResponseProcessor>`\ を\ ``defaultProcessor``\ という名前で登録し、使用する実装クラスを\ ``processors``\ プロパティに列挙する。

列挙した実装クラスは、リクエストの操作・レスポンスの操作のいずれも、記述した順に実行される。

.. code-block:: xml

  <component name="defaultProcessor" class="nablarch.test.core.http.ComplexRequestResponseProcessor">
    <property name="processors">
      <list>
        <component class="nablarch.test.core.http.RequestResponseCookieManager">
          <property name="cookieName" value="JSESSIONID"/>
        </component>
        <component class="nablarch.test.core.http.NablarchSIDManager"/>
        <component class="com.example.test.CSRFTokenManager"/>
      </list>
    </property>
  </component>

拡張例
--------------------------------------------------

リクエストとレスポンスの操作を実装する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
テスティングフレームワークが提供する実装クラスで要件を満たせない場合は、独自の実装クラスを作成する。拡張するには\ :java:extdoc:`RequestResponseProcessor <nablarch.test.core.http.RequestResponseProcessor>`\ を実装し、提供されている実装クラスと同じく\ ``defaultProcessor``\ という名前で登録する。

実装クラスは、先に受信したレスポンスから取り出した値を次のリクエストへ受け渡すために、その値を内部状態として保持することになる。\ ``defaultProcessor``\ として登録したインスタンスは\ :ref:`システムリポジトリ <repository>`\ 上でシングルトンとなるため、明示的に初期化しないと、複数のテストメソッドの間で内部状態が引き継がれてしまう。

これを防ぐため、テスティングフレームワークは各テストメソッドの開始時に\ :java:extdoc:`RequestResponseProcessor#reset <nablarch.test.core.http.RequestResponseProcessor.reset()>`\ を呼び出す。内部状態をテストメソッドごとに切り離したい場合は、\ ``reset()``\ に初期化する処理を書く。内部状態を持たない場合や、複数のテストメソッドの間で内部状態を共有したい場合は、\ ``reset()``\ を何もしないメソッドとしてよい。
