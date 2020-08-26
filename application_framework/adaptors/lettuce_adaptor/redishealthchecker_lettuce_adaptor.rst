.. _redishealthchecker_lettuce_adaptor:

Redisヘルスチェッカ(Lettuce)アダプタ
================================================================================================

.. contents:: 目次
  :depth: 3
  :local:

`Redis(外部サイト、英語) <https://redis.io/>`_ のヘルスチェックをできるようにするアダプタを提供する。
ヘルスチェックについては :ref:`health_check_endpoint_handler` を参照。

ヘルスチェックは、 :ref:`health_check_endpoint_handler-add_health_checker` で説明している
:java:extdoc:`HealthChecker <nablarch.fw.web.handler.health.HealthChecker>` を継承したクラスを作成して追加できる。
このアダプタでは、HealthCheckerを継承した :java:extdoc:`RedisHealthChecker <nablarch.integration.health.RedisHealthChecker>` を提供している。

.. _redishealthchecker_lettuce_adaptor_settings:

Redisのヘルスチェックを行う
-----------------------------------------------------------------------------------------------
HealthCheckEndpointHandlerのhealthCheckersプロパティにRedisHealthCheckerを指定することで、Redisのヘルスチェックを実現できる。

設定例を以下に示す。

.. code-block:: xml

    <!-- ヘルスチェックエンドポイントハンドラ -->
    <component class="nablarch.fw.web.handler.HealthCheckEndpointHandler">
      <!-- healthCheckersプロパティはリストで指定 -->
      <property name="healthCheckers">
        <list>
          <!-- Redisのヘルスチェック -->
          <component class="nablarch.integration.health.RedisHealthChecker">
            <!-- Redisのクライアント(LettuceRedisClient)を指定 -->
            <property name="client" ref="lettuceRedisClient" />
          </component>
        </list>
      </property>
    </component>

RedisHealthCheckerは :java:extdoc:`LettuceRedisClient<nablarch.integration.redisstore.lettuce.LettuceRedisClient>` を使って、
キーの存在確認を行い、例外が発生しなけければヘルスチェックが成功と判断する。キーは存在しなくてよい。
LettuceRedisClient については :ref:`redisstore_redis_client_config_client_classes` を参照。

キーを変更したい場合はRedisHealthCheckerのkeyプロパティに指定する。

.. code-block:: xml

    <!-- Redisのヘルスチェック -->
    <component class="nablarch.integration.health.RedisHealthChecker">
      <!-- Redisのクライアント(LettuceRedisClient)を指定 -->
      <property name="client" ref="lettuceRedisClient" />
      <!-- キーを指定 -->
      <property name="key" ref="pingtest" />
    </component>
