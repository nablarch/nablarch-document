.. _deal_unit_test_setting_rest:

取引単体テストの設定（RESTfulウェブサービス）
==================================================

.. contents:: 目次
  :depth: 3
  :local:

RESTfulウェブサービスの取引単体テストでは、先行するリクエストのレスポンスとしてサーバから受け取った値を、次のリクエストへ引き継ぐ設定を行う。引き継ぐ処理はテスティングフレームワークが提供する実装から選べるほか、独自に作成した実装クラスに差し替えることもできる。

使用方法
--------------------------------------------------

前のレスポンスの値を次のリクエストに引き継ぐ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
取引単体テストでは、セッションIDやCSRFトークンなど、先行するリクエストのレスポンスとしてサーバから受け取った値を、次のリクエストに含めたい場合がある。この受け渡しは、リクエストとレスポンスを操作する\ :java:extdoc:`RequestResponseProcessor <nablarch.test.core.http.RequestResponseProcessor>`\ の実装クラスを、テスト用のコンポーネント設定ファイルに\ ``defaultProcessor``\ という名前で登録すると実現できる。登録した実装クラスは、内蔵サーバへのリクエスト送信前に\ :java:extdoc:`processRequest <nablarch.test.core.http.RequestResponseProcessor.processRequest(nablarch.fw.web.HttpRequest)>`\ が、レスポンス受信後に\ :java:extdoc:`processResponse <nablarch.test.core.http.RequestResponseProcessor.processResponse(nablarch.fw.web.HttpRequest,nablarch.fw.web.HttpResponse)>`\ が実行される。

テスティングフレームワークは、よく使われる実装として\ :java:extdoc:`RequestResponseCookieManager <nablarch.test.core.http.RequestResponseCookieManager>`\ を提供している。この実装クラスは、レスポンスに設定されたクッキーから\ ``cookieName``\ プロパティに指定した名前のものを取り出し、次のリクエストのクッキーに設定する。\ ``cookieName``\ は必須のプロパティであり、指定していないとレスポンスの処理時に例外が発生する。

.. code-block:: xml

  <component name="defaultProcessor" class="nablarch.test.core.http.RequestResponseCookieManager">
    <property name="cookieName" value="JSESSIONID"/>
  </component>

クッキーのうち\ :ref:`セッションストア <session_store>`\ のセッションIDに特化した実装として、\ :java:extdoc:`NablarchSIDManager <nablarch.test.core.http.NablarchSIDManager>`\ も提供している。この実装クラスは、\ :ref:`セッション変数保存ハンドラ <session_store_handler>`\ がセッションIDを保持する際のデフォルトのクッキー名\ ``NABLARCH_SID``\ をクッキー名の初期値に持つため、\ ``cookieName``\ を指定しなくてよい。セッションIDのクッキー名をデフォルトから変更している場合は、\ ``RequestResponseCookieManager``\ を使用してクッキー名を明示する。

複数の値をまとめて引き継ぐ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
引き継ぐ値が複数あり、\ :java:extdoc:`RequestResponseProcessor <nablarch.test.core.http.RequestResponseProcessor>`\ の実装クラスを複数使用したい場合は、\ :java:extdoc:`ComplexRequestResponseProcessor <nablarch.test.core.http.ComplexRequestResponseProcessor>`\ を\ ``defaultProcessor``\ という名前で登録し、\ ``processors``\ プロパティに使用する実装クラスを列挙する。列挙した実装クラスは、リクエストの操作・レスポンスの操作のいずれも、記述した順に実行される。

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
テスティングフレームワークが提供する実装クラスで要件を満たせない場合は、リクエストとレスポンスを操作するためのインタフェースである\ :java:extdoc:`RequestResponseProcessor <nablarch.test.core.http.RequestResponseProcessor>`\ を、各アプリケーションの要件に合わせて実装する。実装したクラスは、提供されている実装クラスと同じく\ ``defaultProcessor``\ という名前で登録する。

実装クラスは、先に受信したレスポンスから取り出した値を次のリクエストへ受け渡すために、その値を内部状態として保持することになる。\ ``defaultProcessor``\ として登録したインスタンスは\ :ref:`システムリポジトリ <repository>`\ 上でシングルトンとなるため、明示的に初期化しないと、複数のテストメソッドの間で内部状態が引き継がれてしまう。これを防ぐため、テスティングフレームワークは各テストメソッドの開始時に\ :java:extdoc:`RequestResponseProcessor#reset <nablarch.test.core.http.RequestResponseProcessor.reset()>`\ を呼び出す。テストメソッドの間で内部状態を引き継ぎたくない場合は、\ ``reset()``\ に初期化する処理を実装する。内部状態を持たない場合や、複数のテストメソッドの間で内部状態を共有したい場合は、\ ``reset()``\ を何もしないメソッドとしてよい。
