.. _body_convert_handler:

リクエストボディ変換ハンドラ
==================================================
.. contents:: 目次
  :depth: 3
  :local:

本ハンドラでは、リクエストボディとレスポンスボディの変換処理を行う。

変換時に使用するフォーマットは、リクエストを処理するリソース(アクション)クラスのメソッドに設定された
:java:extdoc:`Consumes <javax.ws.rs.Consumes>` 及び :java:extdoc:`Produces <javax.ws.rs.Produces>` アノテーションで指定する。

本ハンドラでは、以下の処理を行う。

* リクエストボディをリソース(アクション)クラスで受け付けるFormに変換する。
  詳細は、:ref:`body_convert_handler-convert_request` を参照。

* リソース(アクション)クラスの処理結果をレスポンスボディに変換する。
  詳細は、:ref:`body_convert_handler-convert_response` を参照。

処理の流れは以下のとおり。

.. image:: ../images/BodyConvertHandler/flow.png
  :scale: 75
  
ハンドラクラス名
--------------------------------------------------
* :java:extdoc:`nablarch.fw.jaxrs.BodyConvertHandler`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-jaxrs</artifactId>
  </dependency>

制約
------------------------------
本ハンドラは :ref:`router_adaptor` よりも後ろに設定すること
  このハンドラは、リソース(アクション)クラスのメソッドに設定された、アノテーションの情報を元に
  リクエスト及びレスポンスの変換処理を行う。
  このため、ディスパッチ先を特定する :ref:`router_adaptor` よりも後ろに設定する必要がある。

変換処理を行うコンバータを設定する
--------------------------------------------------
このハンドラでは、 :java:extdoc:`bodyConverters <nablarch.fw.jaxrs.BodyConvertHandler.setBodyConverters(java.util.List)>` プロパティに設定された、
:java:extdoc:`BodyConverter <nablarch.fw.jaxrs.BodyConverter>` の実装クラスを使用してリクエスト及びレスポンスの変換処理を行う。
:java:extdoc:`bodyConverters <nablarch.fw.jaxrs.BodyConvertHandler.setBodyConverters(java.util.List)>` プロパティには、
プロジェクトで使用するMIMEに対応した、 :java:extdoc:`BodyConverter <nablarch.fw.jaxrs.BodyConverter>` を設定すること。

以下に例を示す。

.. code-block:: xml

  <component class="nablarch.fw.jaxrs.BodyConvertHandler">
    <property name="bodyConverters">
      <list>
        <!-- application/xmlに対応したリクエス・レスポンスのコンバータ -->
        <component class="nablarch.fw.jaxrs.JaxbBodyConverter" />
        <!-- application/x-www-form-urlencodedに対応したリクエスト・レスポンスのコンバータ -->
        <component class="nablarch.fw.jaxrs.FormUrlEncodedConverter" />
      </list>
    </property>
  </component>

.. tip::
  :java:extdoc:`bodyConverters <nablarch.fw.jaxrs.BodyConvertHandler.setBodyConverters(java.util.List)>` プロパティに設定されたコンバータで、
  変換出来ないMIMEが使用された場合、サポートしていないメディアタイプであることを示すステータスコード(``415``)を返却する。

.. _body_convert_handler-convert_request:

リクエストボディをFormに変換する
--------------------------------------------------
リクエストボディの変換処理で使用するフォーマットは、リクエストを処理するメソッドに設定された :java:extdoc:`Consumes <javax.ws.rs.Consumes>` により決まる。
もし、 :java:extdoc:`Consumes <javax.ws.rs.Consumes>` に設定されたMIMEと異なるMIMEがリクエストヘッダーのContent-Typeに設定されていた場合は、
サポートしていないメディアタイプであることを示すステータスコード(``415``)を返却する。

リソース(アクション)のメソッドの実装例を以下に示す。

この例では、 ``MediaType.APPLICATION_JSON`` が示す ``application/json`` に対応した
:java:extdoc:`BodyConverter <nablarch.fw.jaxrs.BodyConverter>` でリクエストボディが ``Person`` に変換される。

.. code-block:: java

  @Consumes(MediaType.APPLICATION_JSON)
  @Valid
  public HttpResponse saveJson(Person person) {
      UniversalDao.insert(person);
      return new HttpResponse();
  }

.. _body_convert_handler-convert_response:

リソース(アクション)の処理結果をレスポンスボディに変換する
----------------------------------------------------------------------
レスポンスボディへの変換処理で使用するフォーマットは、リクエストを処理したメソッドに設定された :java:extdoc:`Produces <javax.ws.rs.Produces>` により決まる。

リソース(アクション)のメソッドの実装例を以下に示す。

この例では、 ``MediaType.APPLICATION_JSON`` が示す ``application/json`` に対応した
:java:extdoc:`BodyConverter <nablarch.fw.jaxrs.BodyConverter>` でリクエストボディが ``Person`` に変換される。

.. code-block:: java

  GET
  @Produces(MediaType.APPLICATION_JSON)
  public List<Person> findJson() {
      return UniversalDao.findAll(Person.class);
  }

