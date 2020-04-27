.. _jaxrs_adaptor:

JAX-RSアダプタ
============================

.. contents:: 目次
  :depth: 3
  :local:

:ref:`RESTfulウェブサービス <restful_web_service>` で使用するための以下のアダプタを提供する。

* JSONを `Jackson(外部サイト、英語) <https://github.com/FasterXML/jackson>`_ を使って変換するアダプタ
* `Jersey(外部サイト、英語) <https://jersey.java.net/>`_  で :ref:`RESTfulウェブサービス <restful_web_service>` を使用するためのアダプタ
* `RESTEasy(外部サイト、英語) <http://resteasy.jboss.org/>`_ で :ref:`RESTfulウェブサービス <restful_web_service>` を使用するためのアダプタ

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <!-- jacksonアダプタを使う場合 -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-jackson-adaptor</artifactId>
  </dependency>

  <!-- Jersey用アダプタを使う場合 -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-jersey-adaptor</artifactId>
  </dependency>

  <!-- RESTEasy用アダプタを使う場合 -->  
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-resteasy-adaptor</artifactId>
  </dependency>
  
.. tip::

  Jacksonのバージョン2.10.3を使用してテストを行っている。
  バージョンを変更する場合は、プロジェクト側でテストを行い問題ないことを確認すること。
  

.. tip::

  Jackson1系ライブラリの脆弱性対応が行われなくなったため、Nablarch5u16よりJackson1系のサポートを廃止した。
  Jackson1系を使用していた場合はJackson2系へ移行すること。

  【参考情報】

  * https://jvndb.jvn.jp/ja/contents/2019/JVNDB-2019-012258.html
  * https://github.com/advisories/GHSA-r6j9-8759-g62w
  
   
Jersey環境下でRESTfulウェブサービスを利用する
--------------------------------------------------
ウェブアプリケーションサーバにバンドルされている `JAX-RS(外部サイト、英語) <https://jcp.org/en/jsr/detail?id=339>`_ の実装が、
`Jersey(外部サイト、英語) <https://jersey.java.net/>`_ の場合には、Jersey用のアダプタを使用する。

以下にJersey用アダプタの適用方法を示す。

:java:extdoc:`JaxRsMethodBinderFactory#handlerList <nablarch.fw.jaxrs.JaxRsMethodBinderFactory.setHandlerList(java.util.List)>`
に対して、Jersey用のハンドラを構築するファクトリクラス(:java:extdoc:`JerseyJaxRsHandlerListFactory <nablarch.integration.jaxrs.jersey.JerseyJaxRsHandlerListFactory>`)
をファクトリインジェクションする。これにより、Jersey用の以下のハンドラ構成が自動的に設定される。

* :ref:`body_convert_handler` の設定(以下のコンバータが設定される)

  * JSONのコンバータには :java:extdoc:`Jackson2BodyConverter <nablarch.integration.jaxrs.jackson.Jackson2BodyConverter>` が設定される。
  * XMLのコンバータには :java:extdoc:`JaxbBodyConverter <nablarch.fw.jaxrs.JaxbBodyConverter>` が設定される。
  * application/x-www-form-urlencodedのコンバータには :java:extdoc:`FormUrlEncodedConverter <nablarch.fw.jaxrs.FormUrlEncodedConverter>` が設定される。

* :ref:`jaxrs_bean_validation_handler`

.. code-block:: xml

  <component name="packageMapping" class="nablarch.integration.router.RoutesMapping">
    <property name="methodBinderFactory">
      <component class="nablarch.fw.jaxrs.JaxRsMethodBinderFactory">
        <property name="handlerList">
          <!-- handlerListプロパティにJerseyのハンドラキューをファクトリインジェクションする -->
          <component class="nablarch.integration.jaxrs.jersey.JerseyJaxRsHandlerListFactory"/>
        </property>
      </component>
    </property>

    <!-- 上記以外のプロパティは省略 -->
  </component>

.. tip::
  使用するウェブアプリケーションサーバに `Jackson(外部サイト、英語) <https://github.com/FasterXML/jackson>`_ が
  バンドルされていない場合は、Jacksonのモジュールをアプリケーションモジュールとセットでデプロイすること。
  
RESTEasy環境下でRESTfulウェブサービスを利用する
--------------------------------------------------
ウェブアプリケーションサーバにバンドルされている `JAX-RS(外部サイト、英語) <https://jcp.org/en/jsr/detail?id=339>`_ の実装が、
`RESTEasy(外部サイト、英語) <http://resteasy.jboss.org/>`_ の場合には、RESTEasy用のアダプタを使用する。

以下にRESTEasy用アダプタの適用方法を示す。

:java:extdoc:`JaxRsMethodBinderFactory#handlerList <nablarch.fw.jaxrs.JaxRsMethodBinderFactory.setHandlerList(java.util.List)>`
に対して、RESTEasy用のハンドラを構築するファクトリクラス(:java:extdoc:`ResteasyJaxRsHandlerListFactory <nablarch.integration.jaxrs.resteasy.ResteasyJaxRsHandlerListFactory>`)
をファクトリインジェクションする。これにより、RESTEasy用の以下のハンドラ構成が自動的に設定される。

* :ref:`body_convert_handler` の設定(以下のコンバータが設定される)

  * JSONのコンバータには :java:extdoc:`Jackson2BodyConverter <nablarch.integration.jaxrs.jackson.Jackson2BodyConverter>` が設定される。
  * XMLのコンバータには :java:extdoc:`JaxbBodyConverter <nablarch.fw.jaxrs.JaxbBodyConverter>` が設定される。
  * application/x-www-form-urlencodedのコンバータには :java:extdoc:`FormUrlEncodedConverter <nablarch.fw.jaxrs.FormUrlEncodedConverter>` が設定される。

* :ref:`jaxrs_bean_validation_handler`

.. code-block:: xml

  <component name="packageMapping" class="nablarch.integration.router.RoutesMapping">
    <property name="methodBinderFactory">
      <component class="nablarch.fw.jaxrs.JaxRsMethodBinderFactory">
        <property name="handlerList">
          <!-- handlerListプロパティにRESTEasyのハンドラキューをファクトリインジェクションする -->
          <component class="nablarch.integration.jaxrs.resteasy.ResteasyJaxRsHandlerListFactory"/>
        </property>
      </component>
    </property>

    <!-- 上記以外のプロパティは省略 -->
  </component>

.. tip::
  使用するウェブアプリケーションサーバに `Jackson(外部サイト、英語) <https://github.com/FasterXML/jackson>`_ が
  バンドルされていない場合は、Jacksonのモジュールをアプリケーションモジュールとセットでデプロイすること。

各環境下で利用するボディコンバータを変更（追加）したい
----------------------------------------------------------------------
プロジェクトで対応すべきMIMEが増えた場合には、 :java:extdoc:`JaxRsHandlerListFactory <nablarch.fw.jaxrs.JaxRsHandlerListFactory>` を実装し対応する。

実装方法は、本アダプタ
(:java:extdoc:`JerseyJaxRsHandlerListFactory <nablarch.integration.jaxrs.jersey.JerseyJaxRsHandlerListFactory>` 、 :java:extdoc:`ResteasyJaxRsHandlerListFactory <nablarch.integration.jaxrs.resteasy.ResteasyJaxRsHandlerListFactory>`)
を参考にすると良い。




