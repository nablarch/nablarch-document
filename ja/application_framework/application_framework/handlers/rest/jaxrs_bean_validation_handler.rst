.. _jaxrs_bean_validation_handler:

Jakarta RESTful Web Servcies Bean Validationハンドラ
======================================================
.. contents:: 目次
  :depth: 3
  :local:

.. tip::
  本機能は、Nablarch5までは「JAX-RS BeanValidationハンドラ」という名称だった。
  しかし、Java EEがEclipse Foundationに移管され仕様名が変わったことに伴い「Jakarta RESTful Web Servcies Bean Validationハンドラ」という名称に変更された。

  変更されたのは名称のみで、機能的な差は無い。

  その他、Nablarch6で名称が変更された機能については :ref:`renamed_features_in_nablarch_6` を参照のこと。


本ハンドラは、リソース(アクション)クラスが受け取るForm(Bean)に対して、:ref:`bean_validation` を実行する。
バリデーションでバリデーションエラーが発生した場合には、後続のハンドラに処理は委譲せずに、
:java:extdoc:`ApplicationException <nablarch.core.message.ApplicationException>` を送出して処理を終了する。

本ハンドラでは、以下の処理を行う。

* リソース(アクション)クラスのメソッドが受け取るFormに対する :ref:`bean_validation` を行う。

処理の流れは以下のとおり。

.. image:: ../images/JaxRsBeanValidationHandler/flow.png
  :scale: 75
  
ハンドラクラス名
--------------------------------------------------
* :java:extdoc:`nablarch.fw.jaxrs.JaxRsBeanValidationHandler`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-jaxrs</artifactId>
  </dependency>

  <!-- Bean Validationのモジュール -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core-validation-ee</artifactId>
  </dependency>

制約
------------------------------
:ref:`body_convert_handler` よりも後ろに設定すること
  このハンドラは、 :ref:`body_convert_handler` がリクエストボディから変換したForm(Bean)に対してバリデーションを行うため。

リソース(アクション)で受け取るForm(Bean)に対してバリデーションを実行する
----------------------------------------------------------------------------------------------------
リソース(アクション)のメソッドで受け取るForm(Bean)に対して、バリデーションを実行したい場合は、
そのメソッドに対して :java:extdoc:`Valid <jakarta.validation.Valid>` アノテーションを設定する。

以下に例を示す。

.. code-block:: java

  // Personオブジェクトに対してバリデーションを実行したいので、
  // Validアノテーションを設定する。
  @POST
  @Consumes(MediaType.APPLICATION_JSON)
  @Valid
  public HttpResponse save(Person person) {
      UniversalDao.insert(person);
      return new HttpResponse();
  }
