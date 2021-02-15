.. _redisstore_lettuce_adaptor:

Redisストア(Lettuce)アダプタ
================================================================================================

.. contents:: 目次
  :depth: 3
  :local:

セッションストアに `Redis(外部サイト、英語) <https://redis.io/>`_ を使用できるようにするアダプタを提供する。

セッションストアにRedisを使用すると、DBストアを選択した場合と比較して次のようなメリットが得られる。

* セッション情報を保存するためのテーブルを事前に用意する必要がない
* 有効期限が切れたセッション情報を削除するためのバッチを作る必要がない

.. _redisstore_minimum_settings:

最小構成で動かす
-----------------------------------------------------------------------------------------------
ここでは、 ``localhost`` の ``6379`` ポートで起動している単一のRedisインスタンスに対して接続する場合を例に、設定方法を説明する。

.. tip::
  ローカルで試す場合、Dockerを使えば次のようにコマンドを実行することでRedisインスタンスを構築できる。
  
  .. code-block:: shell

    > docker run --name redis -d -p 6379:6379 redis:5.0.9
  
  停止する場合は次のようにコマンドを実行する。

  .. code-block:: shell

    > docker stop redis



.. _redisstore_minimum_settings_content:

設定内容
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

最小構成でRedisストアを使い始めるには、アプリケーションのコンポーネント定義と環境設定値を修正する必要がある。

.. _redisstore_minimum_settings_how_modify_component_definition:

コンポーネント定義ファイルを修正する
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
最初に、コンポーネントの定義ファイルを修正する方法について説明する。

.. code-block:: xml

  <!-- 省略 -->
  <config-file file="nablarch/webui/redisstore-lettuce.config" />
  <config-file file="common.properties" />
  <config-file file="env.properties" />
  
  <!-- 省略 -->
  <import file="nablarch/webui/redisstore-lettuce.xml" />

まず、デフォルトコンフィグレーションが提供している次の２つの設定ファイルを読み込む。

* ``nablarch/webui/redisstore-lettuce.config``
* ``nablarch/webui/redisstore-lettuce.xml``

``redisstore-lettuce.config`` には、 ``redisstore-lettuce.xml`` で使用しているプレースホルダのデフォルト値が宣言されている。

アプリケーションで用意している環境設定ファイル（``env.properties`` など）がある場合、 ``redisstore-lettuce.config`` はそれよりも前に読み込むようにする。
こうすることで、必要に応じてデフォルトのプレースホルダの値をアプリケーションの環境設定ファイルで上書きできるようになる。

さらに、 :ref:`repository-overwrite_environment_configuration_by_os_env_var` で説明している方法を用いることで、実行環境ごとに接続先のRedisを切り替えることができるようになる。

.. tip::

  デフォルトでは、 ``localhost`` の ``6379`` ポートで起動している単一のRedisインスタンスに接続するように設定されている。


``redisstore-lettuce.xml`` には、Redisストアを使用するために必要となるコンポーネントが定義されている。

``redisstore-lettuce.xml`` を使用すると、 ``nablarch/webui/session-store.xml`` は不要になる。
:ref:`ウェブのアーキタイプ <firstStepGenerateWebBlankProject>` でプロジェクトを生成している場合、デフォルトで ``session-store.xml`` を使用するように設定されているので、 ``session-store.xml`` のインポートを削除し、代わりに ``redisstore-lettuce.xml`` をインポートするように修正する。


.. code-block:: xml

  <!-- 初期化が必要なコンポーネント -->
  <component name="initializer"
             class="nablarch.core.repository.initialization.BasicApplicationInitializer">
    <property name="initializeList">
      <list>
        <!-- 省略 -->
        <component-ref name="lettuceRedisClientProvider"/>
      </list>
    </property>
  </component>

次に、 :java:extdoc:`LettuceRedisClientProvider<nablarch.integration.redisstore.lettuce.LettuceRedisClientProvider>` のコンポーネントを :java:extdoc:`BasicApplicationInitializer<nablarch.core.repository.initialization.BasicApplicationInitializer>` の ``initializeList`` に追加する。

``LettuceRedisClientProvider`` のコンポーネントは ``redisstore-lettuce.xml`` に ``lettuceRedisClientProvider`` という名前で定義されているので、名前参照を使って設定できるようになっている。

この設定の説明については、 :ref:`redisstore_initialize_client` を参照。


.. code-block:: xml

  <!-- 廃棄が必要なコンポーネント -->
  <component name="disposer"
             class="nablarch.core.repository.disposal.BasicApplicationDisposer">
    <property name="disposableList">
      <list>
        <!-- 省略 -->
        <component-ref name="lettuceRedisClientProvider"/>
      </list>
    </property>
  </component>

さらに、 :java:extdoc:`LettuceRedisClientProvider<nablarch.integration.redisstore.lettuce.LettuceRedisClientProvider>` のコンポーネントを :java:extdoc:`BasicApplicationDisposer<nablarch.core.repository.disposal.BasicApplicationDisposer>` の ``disposableList`` に追加する。

この設定の説明については、 :ref:`repository-dispose_object` を参照。


.. _redisstore_minimum_settings_how_modify_env_config:

環境設定値を修正する
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
次に、環境設定値の修正方法を説明する。

.. code-block:: properties

  # デフォルトのセッションストア名
  nablarch.sessionManager.defaultStoreName=redis

プロジェクトの環境設定ファイルで、 ``nablarch.sessionManager.defaultStoreName`` という設定項目を定義し、値に ``redis`` と設定する。

.. tip::

  :ref:`ウェブのアーキタイプ <firstStepGenerateWebBlankProject>` でプロジェクトを生成している場合は、 ``src/main/resources/common.properties`` に ``nablarch.sessionManager.defaultStoreName`` が宣言されている。


以上で、 ``localhost`` の ``6379`` ポートで起動しているRedisをセッションストアとして使用できるようになる。

.. _redisstore_redis_client_config:

Redis の構成に合わせて設定する
-----------------------------------------------------------------------------------------------
:ref:`redisstore_minimum_settings` では、ローカルで起動する単一のRedisインスタンスに接続する例を示した。

しかし、実際に本番などでRedisを使用する場合は次のような構成のRedisに接続できる必要がある。

* Sentinelを使用したMaster-Replica構成
* Cluster構成

ここでは、接続先のRedisの構成に合わせて、どのように設定を変更すればいいのかについて説明する。

.. _redisstore_redis_client_config_client_classes:

構成ごとに用意されたクライアントクラス
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

本アダプタでは、接続先のRedisの構成ごとに専用のクライアントクラス（:java:extdoc:`LettuceRedisClient<nablarch.integration.redisstore.lettuce.LettuceRedisClient>` を実装したクラス）を用意している。

:java:extdoc:`LettuceSimpleRedisClient<nablarch.integration.redisstore.lettuce.LettuceSimpleRedisClient>`
  単一のRedisインスタンスに直接接続する場合に使用するクラス。

:java:extdoc:`LettuceMasterReplicaRedisClient<nablarch.integration.redisstore.lettuce.LettuceMasterReplicaRedisClient>`
  Master-Replica構成のRedisインスタンスに接続する場合に使用するクラス。
  Sentinelを介して接続する場合も、このクラスを使用する。

:java:extdoc:`LettuceClusterRedisClient<nablarch.integration.redisstore.lettuce.LettuceClusterRedisClient>`
  Cluster構成のRedisインスタンスに接続する場合に使用するクラス。

アプリケーションで使用するRedisの構成に合わせて、これらの中から使用するクライアントクラスを設定する必要がある。

.. tip::

  これらのクライアントクラスのコンポーネントは ``redisstore-lettuce.xml`` で定義されているので、利用者側で定義する必要はない。

.. _redisstore_redis_client_config_how_select_client:

使用するクライアントクラスを設定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
どのクライアントクラスを使用するかは、環境設定値 ``nablarch.lettuce.clientType`` で設定できるようになっている。

設定値と採用されるクライアントクラスの関係を、以下に表で示す。

================= ======================================
設定値             クライアントクラス
================= ======================================
``simple``        ``LettuceSimpleRedisClient``
``masterReplica`` ``LettuceMasterReplicaRedisClient``
``cluster``       ``LettuceClusterRedisClient``
================= ======================================

したがって、アプリケーションの環境設定ファイルで次のように設定することで、Cluster構成のRedisに接続できるようになる。

.. code-block:: properties

  nablarch.lettuce.clientType=cluster

.. tip::

  ``nablarch.lettuce.clientType`` のデフォルト値は、 ``redisstore-lettuce.config`` で ``simple`` が設定されている。

.. _redisstore_redis_client_config_uri:

接続URIを設定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
接続先のRedisの情報は、URIで指定する。

URIは、Redisの構成ごとに次の環境設定値で設定できるようになっている。

=============== ====================================== =============
Redisの構成     環境設定値                               デフォルト値(redisstore-lettuce.configで設定されている値)
=============== ====================================== =============
単一            ``nablarch.lettuce.simple.uri``         ``redis://localhost:6379``
Master-Replica  ``nablarch.lettuce.masterReplica.uri`` ``redis-sentinel://localhost:26379,localhost:26380,localhost:26381?sentinelMasterId=masterGroupName``
Cluster         ``nablarch.lettuce.cluster.uriList``   ``redis://localhost:6379,redis://localhost:6380,redis://localhost:6381``
=============== ====================================== =============

Clusterの設定値は、各ノードに接続するためのURIを半角カンマで列挙した値を設定する。
個々のURIのフォーマットの詳細については、 `Lettuceのドキュメント(外部サイト、英語) <https://lettuce.io/core/5.3.0.RELEASE/reference/index.html#redisuri.uri-syntax>`_ を参照。

.. _redisstore_redis_client_config_advanced:

より高度な設定を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
環境設定値で指定できるのは、クライアントクラスの種類とURIのみとなっている。
より細かい設定を行いたい場合は、各クライアントクラスを継承したカスタムクライアントクラスを作成する必要がある。

各クライアントクラスには、Lettuceのインスタンスを生成するメソッドが ``protected`` で定義されている。
各クライアントクラスに用意されている、 ``protected`` メソッドを以下に表で示す。

=================================== ======================================== =============
クライアントクラス                    メソッド                                  戻り値の型
=================================== ======================================== =============
``LettuceSimpleRedisClient``        ``createClient()``                       `RedisClient(外部サイト、英語) <https://lettuce.io/core/5.3.0.RELEASE/api/io/lettuce/core/RedisClient.html>`_
\                                   ``createConnection(RedisClient)``        `StatefulRedisConnection<byte[], byte[]>(外部サイト、英語) <https://lettuce.io/core/5.3.0.RELEASE/api/io/lettuce/core/api/StatefulRedisConnection.html>`_
``LettuceMasterReplicaRedisClient`` ``createClient()``                       `RedisClient(外部サイト、英語) <https://lettuce.io/core/5.3.0.RELEASE/api/io/lettuce/core/RedisClient.html>`_
\                                   ``createConnection(RedisClient)``        `StatefulRedisMasterReplicaConnection<byte[], byte[]>(外部サイト、英語) <https://lettuce.io/core/5.3.0.RELEASE/api/io/lettuce/core/masterreplica/StatefulRedisMasterReplicaConnection.html>`_
``LettuceClusterRedisClient``       ``createClient()``                       `RedisClusterClient(外部サイト、英語) <https://lettuce.io/core/5.3.0.RELEASE/api/io/lettuce/core/cluster/RedisClusterClient.html>`_
\                                   ``createConnection(RedisClusterClient)`` `StatefulRedisClusterConnection<byte[], byte[]>(外部サイト、英語) <https://lettuce.io/core/5.3.0.RELEASE/api/io/lettuce/core/cluster/api/StatefulRedisClusterConnection.html>`_
=================================== ======================================== =============

これらのメソッドをカスタムクライアントクラスでオーバーライドし、独自の設定を行ったLettuceのインスタンスを返すように実装することで、任意の設定ができるようになる。

そして、元となったコンポーネントと同じ名前でカスタムクライアントクラスのコンポーネントを定義することで、クライアントクラスのコンポーネントを差し替えることができる。

各クライアントクラスのコンポーネント名を、以下に表で示す。

=================================== ====================================
クライアントクラス                    コンポーネント名
=================================== ====================================
``LettuceSimpleRedisClient``        ``lettuceSimpleRedisClient``
``LettuceMasterReplicaRedisClient`` ``lettuceMasterReplicaRedisClient``
``LettuceClusterRedisClient``       ``lettuceClusterRedisClient``
=================================== ====================================

.. _redisstore_redis_client_config_advanced_topology_refresh_example:

例：Clusterのトポロジ更新の監視を有効にする
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Clusterのトポロジ更新の監視を有効にする設定を例に、カスタムクライアントクラスの実装と設定方法を説明する。

まず、Cluster構成用のクライアントクラスである ``LettuceClusterRedisClient`` を継承して、カスタムクライアントクラス（``CustomClusterRedisClient``）を作成する。

.. code-block:: java
  
  package com.nablarch.example.redisstore;
  
  import io.lettuce.core.RedisURI;
  import io.lettuce.core.cluster.ClusterClientOptions;
  import io.lettuce.core.cluster.ClusterTopologyRefreshOptions;
  import io.lettuce.core.cluster.RedisClusterClient;
  import nablarch.integration.redisstore.lettuce.LettuceClusterRedisClient;
  
  import java.time.Duration;
  import java.util.List;
  import java.util.stream.Collectors;
  
  public class CustomClusterRedisClient extends LettuceClusterRedisClient {
  
      @Override
      protected RedisClusterClient createClient() {
          List<RedisURI> redisUriList = uriList.stream().map(RedisURI::create).collect(Collectors.toList());
          RedisClusterClient client = RedisClusterClient.create(redisUriList);
  
          ClusterTopologyRefreshOptions clusterTopologyRefreshOptions = ClusterTopologyRefreshOptions.builder()
                  .enableAllAdaptiveRefreshTriggers()
                  .enablePeriodicRefresh(Duration.ofSeconds(10))
                  .build();
  
          ClusterClientOptions clusterClientOptions = ClusterClientOptions.builder()
                  .topologyRefreshOptions(clusterTopologyRefreshOptions)
                  .build();
  
          client.setOptions(clusterClientOptions);
  
          return client;
      }
  }

LettuceでClusterのトポロジ更新を監視できるようにするには、必要な設定を行った `ClusterTopologyRefreshOptions（外部サイト、英語） <https://lettuce.io/core/5.3.0.RELEASE/api/io/lettuce/core/cluster/ClusterTopologyRefreshOptions.html>`_ を `RedisClusterClient（外部サイト、英語） <https://lettuce.io/core/5.3.0.RELEASE/api/io/lettuce/core/cluster/RedisClusterClient.html>`_ に設定する必要がある。

したがって、 ``CustomClusterRedisClient`` では ``RedisClusterClient`` を生成する ``createClient()`` をオーバーライドして、必要な設定を行った ``RedisClusterClient`` のインスタンスを返すように実装する。

.. tip::

  Lettuceの設定の詳細については、 `Lettuceのドキュメント（外部サイト、英語） <https://lettuce.io/core/5.3.0.RELEASE/reference/index.html#clientoptions.cluster-specific-options>`_ を参照。

次に、このカスタムクライアントクラスをコンポーネント定義する。

.. code-block:: xml

  <import file="nablarch/webui/redisstore-lettuce.xml" />

  <component name="lettuceClusterRedisClient" class="com.nablarch.example.redisstore.CustomClusterRedisClient">
    <property name="uriList" ref="redisClusterUriListFactory" />
  </component>

``CustomClusterRedisClient`` の元となったクライアントクラスは ``LettuceClusterRedisClient`` なので、 ``lettuceClusterRedisClient`` という名前で定義することでコンポーネントを上書きできる。

``uriList`` プロパティの設定は、元となった ``redisstore-lettuce.xml`` での設定をそのまま流用している。
他のクライアントクラスを拡張したクラスを作る場合も、プロパティの設定は ``redisstore-lettuce.xml`` の設定をそのまま流用すること。

以上で、トポロジ更新の監視が可能となる。

.. _redisstore_mechanism_to_decide_client:

使用するクライアントクラスの決定の仕組み
-----------------------------------------------------------------------------------------------
:ref:`redisstore_redis_client_config_how_select_client` で、使用するクライアントクラスは環境設定値 ``nablarch.lettuce.clientType`` で設定できることを説明した。
ここでは、具体的にどのようにしてクライアントクラスが決定されているのか、仕組みを説明する。

３つのクライアントクラスのコンポーネントのうち、実際にどのコンポーネントを使用するかは :java:extdoc:`LettuceRedisClientProvider<nablarch.integration.redisstore.lettuce.LettuceRedisClientProvider>` によって決定される。

``LettuceRedisClientProvider`` は、 ``redisstore-lettuce.xml`` で次のように定義されている。

.. code-block:: xml

  <component name="lettuceRedisClientProvider" class="nablarch.integration.redisstore.lettuce.LettuceRedisClientProvider">
      <property name="clientType" value="${nablarch.lettuce.clientType}" />
      <property name="clientList">
          <list>
              <component-ref name="lettuceSimpleRedisClient" />
              <component-ref name="lettuceMasterReplicaRedisClient" />
              <component-ref name="lettuceClusterRedisClient" />
          </list>
      </property>
  </component>

このクラスは、 ``clientList`` と ``clientType`` という２つのプロパティを持っている。

``clientList`` には、候補となるクライアントクラスのコンポーネントがリストで設定されている。
そして ``clientType`` には、使用するクライアントクラスの識別子を設定する。

各クライアントクラスは ``getType()`` という自身の識別子を返すメソッドを持っている。
``LettuceRedisClientProvider`` は ``clientType`` プロパティに設定された値と ``clientList`` プロパティに設定された各コンポーネントが返す ``getType()`` の値を比較する。
そして、値が一致したものを、実際に使用するコンポーネントとして決定している。

``LettuceRedisClientProvider`` は :java:extdoc:`ComponentFactory<nablarch.core.repository.di.ComponentFactory>` を実装しており、 ``createObject()`` メソッドは、決定されたクライアントクラス（:java:extdoc:`LettuceRedisClient<nablarch.integration.redisstore.lettuce.LettuceRedisClient>`）のコンポーネントを返すように実装されている。

.. _redisstore_initialize_client:

クライアントクラスの初期化
-----------------------------------------------------------------------------------------------
本アダプタが提供している３つのクライアントクラスは、いずれもRedisへの接続を確立するために初期化が必要となっている。

各クライアントクラスは :java:extdoc:`Initializable<nablarch.core.repository.initialization.Initializable>` を実装しており、 ``initialize()`` メソッドを実行することでRedisへの接続が確立される。
したがって、使用するクライアントクラスのコンポーネントは、 :java:extdoc:`BasicApplicationInitializer<nablarch.core.repository.initialization.BasicApplicationInitializer>` の ``initializeList`` プロパティに設定しなければならない。

実際の ``initializeList`` への設定は、以下のように :ref:`redisstore_mechanism_to_decide_client` で説明した ``LettuceRedisClientProvider`` のコンポーネントを使用する。

.. code-block:: xml

  <!-- 初期化が必要なコンポーネント -->
  <component name="initializer"
             class="nablarch.core.repository.initialization.BasicApplicationInitializer">
    <property name="initializeList">
      <list>
        <!-- 省略 -->
        <component-ref name="lettuceRedisClientProvider"/>
      </list>
    </property>
  </component>

こうすることで、コンポーネント定義の記述を変更することなく、決定されたクライアントクラスのコンポーネントを初期化できる。

クライアントクラスの廃棄処理
-----------------------------------------------------------------------------------------------

各クライアントクラスは :java:extdoc:`Disposable<nablarch.core.repository.disposal.Disposable>` を実装しており、 ``dispose()`` メソッドを実行することでRedisへの接続が閉じられる。
したがって、使用するクライアントクラスのコンポーネントを :java:extdoc:`BasicApplicationDisposer<nablarch.core.repository.disposal.BasicApplicationDisposer>` の ``disposableList`` プロパティに設定することで、アプリケーション終了時にRedisとの接続を閉じることができる。

.. code-block:: xml

  <!-- 廃棄が必要なコンポーネント -->
  <component name="disposer"
             class="nablarch.core.repository.disposal.BasicApplicationDisposer">
    <property name="disposableList">
      <list>
        <!-- 省略 -->
        <component-ref name="lettuceRedisClientProvider"/>
      </list>
    </property>
  </component>

``BasicApplicationInitializer`` の ``initializeList`` と同様で、 ``disposableList`` プロパティに ``LettuceRedisClientProvider`` コンポーネントを指定することで、実際に使用されるクライアントクラスの廃棄処理が実行されるようになる。


.. _redisstore_session_persistence:

セッション情報の保存方法
-----------------------------------------------------------------------------------------------
Redisに保存されたセッション情報は、 ``nablarch.session.<セッションID>`` というキーで保存されている。

以下は、 ``redis-cli`` で保存されているキーを表示した様子を記載している。

.. code-block:: shell

  127.0.0.1:6379> keys *
  1) "nablarch.session.8b00bce5-d19f-4f63-b1fe-d14ecca9a4f6"

また、セッション情報（:java:extdoc:`SessionEntry<nablarch.common.web.session.SessionEntry>` のリスト）は、デフォルトでは :java:extdoc:`JavaSerializeStateEncoder<nablarch.common.web.session.encoder.JavaSerializeStateEncoder>` でエンコードされたバイナリ形式で保存されている。

使用するエンコーダーは、 ``serializeEncoder`` という名前で別のエンコーダーのコンポーネントを定義することで変更できる。

.. _redisstore_expiration:

有効期限の管理方法
-----------------------------------------------------------------------------------------------
Redisには、保存したキーに対して有効期限を設定する仕組みが用意されている。
有効期限が切れたキーは自動的に削除される。

本アダプタは、セッションの有効期限の管理にこのRedisの有効期限の仕組みを使用している。
したがって、有効期限が切れたセッション情報は自動的に削除されるため、ゴミとして残ったセッション情報を削除するためのバッチを用意する必要はない。

以下は、セッション情報の有効期限を `pttl コマンド（外部サイト、英語） <https://redis.io/commands/pttl>`_ で確認している様子を記載している。

.. code-block:: shell

  127.0.0.1:6379> pttl "nablarch.session.8b00bce5-d19f-4f63-b1fe-d14ecca9a4f6"
  (integer) 879774

