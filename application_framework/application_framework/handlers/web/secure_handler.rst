.. _secure_handler:

セキュアハンドラ
==================================================
.. contents:: 目次
  :depth: 3
  :local:

本ハンドラでは、セキュリティ関連のヘッダを、レスポンスオブジェクト(:java:extdoc:`HttpResponse <nablarch.fw.web.HttpResponse>`)に対して設定する。

デフォルトでは、以下のレスポンスヘッダを設定する。

* X-Frame-Options: SAMEORIGIN
* X-XSS-Protection: 1; mode=block
* X-Content-Type-Options: nosniff


本ハンドラでは、以下の処理を行う。

* セキュリティ関連のレスポンスヘッダの設定処理

処理の流れは以下のとおり。

.. image:: ../images/SecureHandler/flow.png
  :scale: 85
  
ハンドラクラス名
--------------------------------------------------
* :java:extdoc:`nablarch.fw.web.handler.SecureHandler`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

制約
------------------------------
:ref:`http_response_handler` よりも後ろに設定すること
  本ハンドラで設定したレスポンスヘッダを、 :ref:`http_response_handler` がServlet APIのレスポンスオブジェクトに設定するため。

デフォルトで適用されるヘッダの値を変更したい
--------------------------------------------------
要件により、デフォルトで適用されるセキュリティ関連のヘッダの値を変更したい場合がある。

例えば、フレーム内の表示を全て許可しない場合には、 ``X-Frame-Options`` ヘッダの値を ``DENY`` に変更する必要がある。
このような場合は、コンポーネント設定ファイルに明示的に設定を行うことで対応する。

以下に例を示す。

.. code-block:: xml

  <component class="nablarch.fw.web.handler.SecureHandler">
    <property name="secureResponseHeaderList">
      <list>
        <!-- X-Frame-Optionsの値を明示的に指定 -->
        <component class="nablarch.fw.web.handler.secure.FrameOptionsHeader">
          <property name="option" value="DENY" />
        </component>

        <!-- 上記以外のヘッダはデフォルトのまま -->
        <component class="nablarch.fw.web.handler.secure.XssProtectionHeader" />
        <component class="nablarch.fw.web.handler.secure.ContentTypeOptionsHeader" />
      </list>
    </property>
  </component>

.. tip::

  値を変更するためのプロパティの詳細は、以下のクラスを参照。

  * :java:extdoc:`FrameOptionsHeader <nablarch.fw.web.handler.secure.FrameOptionsHeader>`
  * :java:extdoc:`ContentTypeOptionsHeader <nablarch.fw.web.handler.secure.ContentTypeOptionsHeader>`
  * :java:extdoc:`XssProtectionHeader <nablarch.fw.web.handler.secure.XssProtectionHeader>`


デフォルト以外のレスポンスヘッダを設定する
-------------------------------------------------------
デフォルト以外のセキュリティ関連のレスポンスヘッダを設定する手順を以下に示す。

1. :java:extdoc:`SecureResponseHeader <nablarch.fw.web.handler.secure.SecureResponseHeader>` インタフェースの実装クラスで、
   レスポンスヘッダに設定するフィールド名と値を指定する。

2. 本ハンドラ(:java:extdoc:`SecureHandler <nablarch.fw.web.handler.SecureHandler>`)に、``No1`` で作成したクラスを設定する。

.. important::

  :java:extdoc:`SecureResponseHeader <nablarch.fw.web.handler.secure.SecureResponseHeader>` 実装クラスを設定する際は、
  デフォルトで適用されていたコンポーネントも設定すること。

  以下に設定ファイルの例を示す。

  .. code-block:: xml

    <component class="nablarch.fw.web.handler.SecureHandler">
      <property name="secureResponseHeaderList">
        <list>
          <component class="nablarch.fw.web.handler.secure.FrameOptionsHeader" />
          <component class="nablarch.fw.web.handler.secure.XssProtectionHeader" />
          <component class="nablarch.fw.web.handler.secure.ContentTypeOptionsHeader" />

          <!-- 追加で作成したコンポーネント -->
          <component class="nablarch.fw.web.handler.secure.SampleSecurityHeader" />
        </list>
      </property>
    </component>
    
