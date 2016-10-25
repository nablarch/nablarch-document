.. _http_response_handler:

HTTPレスポンスハンドラ
==================================================
.. contents:: 目次
  :depth: 3
  :local:

本ハンドラは、後続ハンドラが返す :java:extdoc:`HttpResponse <nablarch.fw.web.HttpResponse>` に従い、サーブレットAPIを
呼び出しクライアントへのレスポンスを行う。
応答の方法には、下記3通りが存在する。

サーブレットフォワード
  サーブレットにフォワードを行い、レスポンスを描画する。主にJSPを使ったレスポンス時に使用する。

リダイレクト
  クライアントにリダイレクトを行う応答を返す。

直接レスポンス
   :java:extdoc:`ServletResponse <javax.servlet.ServletResponse>` の `getOutputStream` メソッドを使用して直接
   レスポンスを行う。

処理の流れは以下のとおり。

.. image:: ../images/HttpResponseHandler/flow.png

ハンドラクラス名
--------------------------------------------------
* :java:extdoc:`nablarch.fw.web.handler.HttpResponseHandler`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

制約
------------------------------

なし。



応答の変換方法
------------------------------------------------------

本ハンドラでは、後続のハンドラから返されるスキーマ [#scheme]_ と、ステータスコード  [#statusCode]_ によりクライアントに返すレスポンスの方法を変更する。

変換条件と応答方法は下記表の通り。


.. list-table::
  :header-rows: 1
  :widths: 5,5
  :class: white-space-normal

  * -   変換条件
    -   応答の方法
  * -   スキーマが
        ``servlet`` の場合
    -   別サーブレットへ処理をフォワードする
  * -   スキーマが
        ``redirect`` の場合
    -   指定したURLへのリダイレクトを行う
  * -   スキーマが
        ``http`` または ``https`` の場合
    -   指定したURLへのリダイレクトを行う
  * -   スキーマが上記以外で、
        ステータスコードが200～399以外の場合
    -   ステータスコードに合うエラー画面の表示をおこなう。
  * -   上記以外の場合
    -   HttpResponse#getBodyStream()の結果を応答する。




.. [#scheme]
      ここで言う「スキーマ」とは、後続ハンドラが返した
      :java:extdoc:`HttpResponse#getContentPath() <nablarch.fw.web.HttpResponse.getContentPath()>`
      で取得した  :java:extdoc:`ResourceLocator <nablarch.fw.web.ResourceLocator>` の
      :java:extdoc:`getScheme() メソッド <nablarch.fw.web.ResourceLocator.getScheme()>` の戻り値のことを指す。

.. [#statusCode]
      ここで言う「ステータスコード」とは、後続ハンドラが返す
      :java:extdoc:`HttpResponse <nablarch.fw.web.HttpResponse>` クラスの
      :java:extdoc:`getStatusCode() <nablarch.fw.web.HttpResponse.getStatusCode()>` メソッドの戻り値のことを示す。

.. _http_response_handler-convert_status_code:

HTTPステータスコードの変更
------------------------------------------------------

本ハンドラでは、ステータスコードを一部変更してクライアントへのレスポンスに設定する。

HTTPステータスコードを決定する変換条件と、応答のエラーコードは下記表のとおり。

.. list-table::
  :header-rows: 1
  :widths: 3,7
  :class: white-space-normal

  * -   変換条件
    -   エラーコード
  * -   Ajaxのリクエストの場合
    -   元のステータスコードそのままを返す
  * -   元のステータスコードが400の場合
    -   ステータスコード200を返す
  * -   上記以外の場合
    -   ステータスコード の結果そのままを返す


.. _http_response_handler-change_content_path:

言語毎のコンテンツパスの切り替え
------------------------------------------------------

本ハンドラは、HTTPリクエストに含まれる言語設定をもとにして、フォワード先を動的に切り替える機能を持つ。
この機能を利用することで、利用者が選んだ言語に合わせてフォワードするJSPを切り替える機能が実現できる。

この機能を使用する際は、本ハンドラの ``contentPathRule`` プロパティに下記いずれかのクラスを設定する。


============================================================================================================================= ============================================================================================
クラス名                                                                                                                      説明
============================================================================================================================= ============================================================================================
:java:extdoc:`DirectoryBasedResourcePathRule <nablarch.fw.web.i18n.DirectoryBasedResourcePathRule>`                           コンテキストルート直下のディレクトリを言語の切り替えに
                                                                                                                              |br|
                                                                                                                              使用するクラス。

                                                                                                                               .. code-block:: bash

                                                                                                                                # /management/user/search.jspを日本語(ja)と
                                                                                                                                # 英語(en)に対応する場合の配置例
                                                                                                                                # コンテキストルート直下に言語ごとにディレクトリを作成する。
                                                                                                                                # ディレクトリ名は言語名とする。
                                                                                                                                コンテキストルート
                                                                                                                                ├─en
                                                                                                                                │  └─management
                                                                                                                                │      └─user
                                                                                                                                │           search.jsp
                                                                                                                                └─ja
                                                                                                                                    └─management
                                                                                                                                        └─user
                                                                                                                                             search.jsp

:java:extdoc:`FilenameBasedResourcePathRule <nablarch.fw.web.i18n.FilenameBasedResourcePathRule>`                             ファイル名を言語の切り替えに使用するクラス。

                                                                                                                                .. code-block:: bash

                                                                                                                                 # /management/user/search.jspを日本語(ja)と
                                                                                                                                 # 英語(en)に対応する場合の配置例
                                                                                                                                 # 言語毎にファイルを作成する。
                                                                                                                                 # ファイル名にはサフィックス「"_"＋言語名」を付ける。
                                                                                                                                 コンテキストルート
                                                                                                                                 └─management
                                                                                                                                         └─user
                                                                                                                                              search_en.jsp
                                                                                                                                              search_ja.jsp
============================================================================================================================= ============================================================================================

この際の設定例は下記の通り。

.. code-block:: xml

  <!-- リソースパスルール -->
  <component name="resourcePathRule" class="nablarch.fw.web.i18n.DirectoryBasedResourcePathRule" />

  <!-- HTTPレスポンスハンドラ -->
  <component class="nablarch.fw.web.handler.HttpResponseHandler">
    <property name="contentPathRule" ref="resourcePathRule" />
  </component>


上記以外の方法でコンテンツの切り替えを行いたい場合は、 :java:extdoc:`ResourcePathRule <nablarch.fw.web.i18n.ResourcePathRule>`
クラスを継承したクラスを作成し、作成したクラスを上記同様に ``resourcePathRule`` プロパティに設定すること。


本ハンドラ内で発生した致命的エラーの対応
------------------------------------------------------

本ハンドラ内の処理で、下記事象が発生した場合、正常な応答が返せないと判断して、クライアントに対しては
ステータスコード500で固定的なレスポンスを返す。

* サーブレットフォワード時に ServletException が発生した場合
* RuntimeException およびそのサブクラスの例外が発生した場合
* Error およびそのサブクラスの例外が発生した場合

この際のレスポンスは下記HTMLとなる。

.. code-block:: html

  <html>
    <head>
      <title>A system error occurred.</title>
    </head>
    <body>
      <p>
        We are sorry not to be able to proceed your request.<br/>
        Please contact the system administrator of our system.
      </p>
    </body>
  </html>

.. important::

    上記HTMLのレスポンスは固定的になっており、設定による変更などはできない。

    このレスポンスは、本ハンドラ内で例外が発生するレアケースのみでしか使われることはない。
    このため、通常この仕様が問題になることはないが、どんなことがあってもこのレスポンスを
    出してはいけないシステムにおいては、本ハンドラを参考にハンドラの自作を検討すること。



.. |br| raw:: html

  <br />
