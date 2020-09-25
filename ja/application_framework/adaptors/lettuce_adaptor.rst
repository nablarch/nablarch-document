.. _lettuce_adaptor:

Lettuceアダプタ
================================================================================================

.. contents:: 目次
  :depth: 3
  :local:

Nablarchが提供する下記の機能で `Redis(外部サイト、英語) <https://redis.io/>`_ を使用できるようにするアダプタを提供する。

- :ref:`session_store`
- :ref:`health_check_endpoint_handler`

本アダプタでは、Redisのクライアントライブラリとして `Lettuce(外部サイト、英語) <https://lettuce.io/>`_ を使用している。

.. _lettuce_adaptor_module_list:

モジュール一覧
-----------------------------------------------------------------------------------------------

.. code-block:: xml

  <!-- RedisStore Lettuceアダプタ -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-lettuce-adaptor</artifactId>
  </dependency>

  <!-- デフォルトコンフィグレーション -->
  <dependency>
    <groupId>com.nablarch.configuration</groupId>
    <artifactId>nablarch-main-default-configuration</artifactId>
  </dependency>

.. tip::

  Redisは5.0.9、Lettuceは5.3.0.RELEASEのバージョンを使用してテストを行っている。
  バージョンを変更する場合は、プロジェクト側でテストを行い問題ないことを確認すること。

各機能に対応したアダプタの説明は下記を参照。

.. toctree::
  :maxdepth: 1

  lettuce_adaptor/redisstore_lettuce_adaptor
  lettuce_adaptor/redishealthchecker_lettuce_adaptor
