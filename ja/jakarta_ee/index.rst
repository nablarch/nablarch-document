=========================================================================
Jakarta EEの仕様名に関して
=========================================================================

.. contents:: 目次
  :depth: 3
  :local:

省略名の表記に関して
=========================================================================

Java EEで使われていた仕様の省略名について、Nablarch6では基本的にすべてJakarta EEでの仕様名に置き換えて表記している。

**例**

* JPA (Java Persistence API) → Jakarta Persistence
* JAX-RS (Java API for RESTful Web Services) → Jakarta RESTful Web Services

ただし、読みやすさが損なわれる場合は省略名を残している部分もある。
特に断りが無い限り、本解説書内で登場する省略名は以下のようにJakarta EEの仕様を指すものとする。


.. list-table:: 省略名とJakarta EEの仕様の対応表
   :widths: 1,3
   :header-rows: 1

   * - 省略名
     - Jakarta EE仕様
   * - JSF
     - `Jakarta Faces (外部サイト、英語) <https://jakarta.ee/specifications/faces/>`_
   * - JASPIC
     - `Jakarta Authentication (外部サイト、英語) <https://jakarta.ee/specifications/authentication/>`_
   * - JACC
     - `Jakarta Authorization (外部サイト、英語) <https://jakarta.ee/specifications/authorization/>`_
   * - JMS
     - `Jakarta Messaging (外部サイト、英語) <https://jakarta.ee/specifications/messaging/>`_
   * - JPA
     - `Jakarta Persistence (外部サイト、英語) <https://jakarta.ee/specifications/persistence/>`_
   * - JTA
     - `Jakarta Transactions (外部サイト、英語) <https://jakarta.ee/specifications/transactions/>`_
   * - jBatch
     - `Jakarta Batch (外部サイト、英語) <https://jakarta.ee/specifications/batch/>`_
   * - JCA
     - `Jakarta Connectors (外部サイト、英語) <https://jakarta.ee/specifications/connectors/>`_
   * - JAF
     - `Jakarta Activation (外部サイト、英語) <https://jakarta.ee/specifications/activation/>`_
   * - EL
     - `Jakarta Expression Language (外部サイト、英語) <https://jakarta.ee/specifications/expression-language/>`_
   * - EJB
     - `Jakarta Enterprise Beans (外部サイト、英語) <https://jakarta.ee/specifications/enterprise-beans/>`_
   * - JAXB
     - `Jakarta XML Binding (外部サイト、英語) <https://jakarta.ee/specifications/xml-binding/>`_
   * - JSON-B
     - `Jakarta JSON Binding (外部サイト、英語) <https://jakarta.ee/specifications/jsonb/>`_
   * - JSON-P
     - `Jakarta JSON Processing (外部サイト、英語) <https://jakarta.ee/specifications/jsonp/>`_
   * - JSP
     - `Jakarta Server Pages (外部サイト、英語) <https://jakarta.ee/specifications/pages/>`_
   * - JAX-WS
     - `Jakarta XML Web Services (外部サイト、英語) <https://jakarta.ee/specifications/xml-web-services/>`_
   * - JAX-RS
     - `Jakarta RESTful Web Services (外部サイト、英語) <https://jakarta.ee/specifications/restful-ws/>`_
   * - JSTL
     - `Jakarta Standard Tag Library (外部サイト、英語) <https://jakarta.ee/specifications/tags/>`_
   * - CDI
     - `Jakarta Contexts and Dependency Injection (外部サイト、英語) <https://jakarta.ee/specifications/cdi/>`_

.. _renamed_features_in_nablarch_6:

Nablarch5と6で名称が変更になった機能について
=========================================================================

Java EEがEclipse Foundationに移管され各仕様の名称が変更されたことに伴い、Nablarchが提供する機能でJava EEの仕様名を含んでいたものは名称の変更を行った。
以下に、変更前後の名称の対応表を記載する。


.. list-table:: Nablarch5,6で名称が変更になった機能の対応表
   :widths: 1,1
   :header-rows: 1

   * - Nablarch5までの名称
     - Nablarch6からの名称
   * - JAX-RS BeanValidationハンドラ
     - :doc:`../application_framework/application_framework/handlers/rest/jaxrs_bean_validation_handler` [#jaxr_rs_bean_validation_handler_footnote]_
   * - JAX-RSアダプタ
     - :doc:`../application_framework/adaptors/jaxrs_adaptor`
   * - JAX-RSサポート
     - :doc:`Jakarta RESTful Web Servicesサポート <../application_framework/application_framework/web_service/rest/architecture>`
   * - JAX-RSレスポンスハンドラ
     - :doc:`../application_framework/application_framework/handlers/rest/jaxrs_response_handler`
   * - JSPカスタムタグ
     - :doc:`../application_framework/application_framework/libraries/tag`
   * - JSP静的解析ツール
     - :doc:`../development_tools/toolbox/JspStaticAnalysis/index`
   * - JSR352に準拠したバッチアプリケーション
     - :doc:`../application_framework/application_framework/batch/jsr352/index`

.. [#jaxr_rs_bean_validation_handler_footnote]
  「BeanValidation」はNablarchが提供するバリデーション機能である :doc:`../application_framework/application_framework/libraries/validation/bean_validation` を指しているため、Jakarta Bean Validationには変更していない。

なお、変更されたのは名称のみで機能的な変更はない。
また、後方互換を維持するためにクラスやパッケージの名前などは変更されていない。
