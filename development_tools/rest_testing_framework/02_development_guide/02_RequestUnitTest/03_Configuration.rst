.. _rest-test-configuration:

----------
各種設定値
----------

環境設定に依存する設定値については、コンポーネント設定ファイルで変更できる。\
設定可能な項目を以下に示す。

コンポーネント設定ファイル設定項目一覧
===============================================

+----------------------------+-------------------------------------------------------------------------+-------------------------------------------------------+
| 設定項目名                 | 説明                                                                    | デフォルト値                                          |
+============================+=========================================================================+=======================================================+
| webBaseDir                 | ウェブアプリケーションのルートディレクトリ\ [#]_\                       | src/main/webapp                                       |
+----------------------------+-------------------------------------------------------------------------+-------------------------------------------------------+
| webFrontControllerKey      | Webフロントコントローラーのリポジトリキー\ [#]_\                        | webFrontController                                    |
+----------------------------+-------------------------------------------------------------------------+-------------------------------------------------------+ 

.. [#] 
  PJ共通のwebモジュールが存在する場合、このプロパティにカンマ区切りでディレクトリを設定する。
  複数指定された場合、先頭から順にリソースが読み込まれる。
  
  以下に例を示す。

  .. code-block:: xml

    <component name="restTestConfiguration" class="nablarch.test.core.http.RestTestConfiguration">
      <property name="webBaseDir" value="/path/to/web-a/,/path/to/web-common"/>

  この場合、web-a、web-commonの順にリソースが探索される。
       
.. [#]
  ウェブアプリケーション実行基盤とウェブサービス実行基盤をひとつのWarで実行する場合など
  :ref:`Webフロントコントローラー <web_front_controller>` をデフォルトの"webFrontController"以外の名前で
  コンポーネント登録する場合がある。
  そのような場合は、このプロパティにウェブサービスで使用するWebフロントコントローラーのリポジトリキーを設定することで
  内蔵サーバで実行されるハンドラを制御することができる。

  以下に例を示す。

  ウェブアプリケーション実行基盤用のWebフロントコントローラー( ``webFrontController`` )と
  ウェブサービス実行基盤用のWebフロントコントローラー( ``jaxrsController`` )が登録されているコンポーネント定義。

  .. code-block:: xml

    <!-- ハンドラキュー構成 -->
    <component name="webFrontController" class="nablarch.fw.web.servlet.WebFrontController">
      <property name="handlerQueue">
        <list>
          <component class="nablarch.fw.web.handler.HttpCharacterEncodingHandler"/>
          <component class="nablarch.fw.handler.GlobalErrorHandler"/>
          <component class="nablarch.common.handler.threadcontext.ThreadContextClearHandler"/>
          <component class="nablarch.fw.web.handler.HttpResponseHandler"/>
          ・
          ・
          ・
          (略)
        </list>
      </property>
    </component>

    <component name="jaxrsController" class="nablarch.fw.web.servlet.WebFrontController">
      <property name="handlerQueue">
        <list>
          <component class="nablarch.fw.web.handler.HttpCharacterEncodingHandler"/>
          <component class="nablarch.fw.handler.GlobalErrorHandler"/>
          <component class="nablarch.fw.jaxrs.JaxRsResponseHandler"/>
          ・
          ・
          ・
          (略)
        </list>
      </property>
    </component>


  デフォルト設定でRESTfulウェブサービス実行基盤向けテスティングフレームワークを使用すると
  "webFrontController"が使用されるため、ウェブアプリケーション向けのWebフロントコントローラーが実行される。
  以下のように設定を上書きすることでウェブサービス向けのWebフロントコントローラーを使用できる。

  .. code-block:: xml

    <import file="nablarch/test/rest-request-test.xml"/>
    <!--  デフォルトのコンポーネント定義をimport後に上書きする。-->
    <component name="restTestConfiguration" class="nablarch.test.core.http.RestTestConfiguration">
      <property name="webFrontControllerKey" value="jaxrsController"/>
