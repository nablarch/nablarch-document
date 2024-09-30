.. _micrometer_adaptor:

Micrometerアダプタ
==================================================

.. contents:: 目次
  :depth: 3
  :local:

`Micrometer(外部サイト、英語) <https://micrometer.io/>`_ を使用したメトリクス収集を行うためのアダプタを提供する。

本アダプタを使うことで、次のようなことができるようになり、アプリケーションの運用監視がしやすくなるというメリットが得られる。

* JVM のメモリ使用量や CPU 使用率など、アプリケーションのメトリクスを収集できる
* 収集したメトリクスを `Datadog(外部サイト) <https://www.datadoghq.com/ja/>`_ や `CloudWatch(外部サイト) <https://aws.amazon.com/jp/cloudwatch/>`_ などの監視サービスに連携できる


モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <!-- Micrometerアダプタ -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-micrometer-adaptor</artifactId>
  </dependency>
  
.. tip::

  Micrometerのバージョン1.13.0を使用してテストを行っている。
  バージョンを変更する場合は、プロジェクト側でテストを行い問題ないことを確認すること。

Micrometerアダプタを使用するための設定を行う
--------------------------------------------------
Micrometerでメトリクスを収集するためには、 `レジストリ(外部サイト、英語) <https://docs.micrometer.io/micrometer/reference/concepts/registry.html>`_ と呼ばれるクラスを作成する必要がある。
本アダプタでは、このレジストリを :ref:`repository` に登録するための :java:extdoc:`ComponentFactory<nablarch.core.repository.di.ComponentFactory>` を提供している。

ここでは、 `LoggingMeterRegistry(外部サイト、英語)`_ をコンポーネントとして登録する :java:extdoc:`LoggingMeterRegistryFactory<nablarch.integration.micrometer.logging.LoggingMeterRegistryFactory>` を例にして設定方法について説明する。

.. tip::

  `LoggingMeterRegistry(外部サイト、英語)`_ は、 SLF4J または Java Util Logging を使ってメトリクスをログに出力する機能を提供する。
  特に設定をしていない場合は、 Java Util Logging を使って標準出力にメトリクスが出力されるため、簡単な動作確認をするのに適している。

  他のレジストリは連携先のサービスの準備や、収集したメトリクスを出力する実装を作りこむなどの手間がかかる。
  このため、この説明では最も簡単に動作を確認できる `LoggingMeterRegistry(外部サイト、英語)`_ を使用している。

なお、ベースとなるアプリケーションには `ウェブアプリケーションのExample(外部サイト) <https://github.com/nablarch/nablarch-example-web>`_ を使用する。

.. _micrometer_adaptor_declare_default_meter_binder_list_provider_as_component:

DefaultMeterBinderListProviderをコンポーネントとして宣言する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Micrometerには、 `MeterBinder(外部サイト、英語)`_ というインタフェースが存在する。

JVMのメモリ使用量やCPU使用率など、よく使用するメトリクスの収集は、このインタフェースを実装したクラスとしてあらかじめ用意されている。
（例：JVMのメモリ使用量は `JvmMemoryMetrics(外部サイト、英語)`_ 、CPU使用率は `ProcessorMetrics(外部サイト、英語)`_ ）

:java:extdoc:`DefaultMeterBinderListProvider <nablarch.integration.micrometer.DefaultMeterBinderListProvider>` は、この `MeterBinder(外部サイト、英語)`_ のリストを提供するクラスで、本クラスを使用することでJVMのメモリ使用量やCPU使用率などのメトリクスを収集できるようになる。

まず ``src/main/resources/web-component-configuration.xml`` に、この :java:extdoc:`DefaultMeterBinderListProvider <nablarch.integration.micrometer.DefaultMeterBinderListProvider>` の宣言を追加する。

.. code-block:: xml

  <component name="meterBinderListProvider"
             class="nablarch.integration.micrometer.DefaultMeterBinderListProvider" />


収集されるメトリクスの具体的な説明については、 :ref:`micrometer_default_metrics` を参照。

DefaultMeterBinderListProviderを廃棄処理対象にする
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:java:extdoc:`DefaultMeterBinderListProvider <nablarch.integration.micrometer.DefaultMeterBinderListProvider>` は廃棄処理が必要なコンポーネントなので、下記のように廃棄処理対象として宣言する。

.. code-block:: xml
  
  <component name="disposer"
      class="nablarch.core.repository.disposal.BasicApplicationDisposer">

    <property name="disposableList">
      <list>
        <component-ref name="meterBinderListProvider"/>
      </list>
    </property>

  </component>

オブジェクトの廃棄処理については、 :ref:`repository-dispose_object` を参照

レジストリのファクトリクラスをコンポーネントとして宣言する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: xml

  <component class="nablarch.integration.micrometer.logging.LoggingMeterRegistryFactory">
    <property name="meterBinderListProvider" ref="meterBinderListProvider" />
    <property name="applicationDisposer" ref="disposer" />
  </component>

次に、使用するレジストリごとに用意されているファクトリクラスをコンポーネントとして宣言する。

このとき、 ``meterBinderListProvider`` と ``applicationDisposer`` の２つのプロパティを設定する。
それぞれのプロパティには、上で宣言した :java:extdoc:`DefaultMeterBinderListProvider <nablarch.integration.micrometer.DefaultMeterBinderListProvider>` と :java:extdoc:`BasicApplicationDisposer <nablarch.core.repository.disposal.BasicApplicationDisposer>` を設定する。

なお、本アダプタが提供しているファクトリクラスについては :ref:`micrometer_registry_factory` に一覧を記載している。


設定ファイルを作成する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

最後に、 ``src/main/resources`` の下に ``micrometer.properties`` という名前のテキストファイルを作成する。

ここでは、中身を次のように記述する。

.. code-block:: properties

  # 確認を楽にするため、5秒ごとにメトリクスを出力する（デフォルトは1分）
  nablarch.micrometer.logging.step=5s
  # step で指定した時間よりも早くアプリケーションが終了した場合でも廃棄処理でログが出力されるよう設定
  nablarch.micrometer.logging.logInactive=true

.. important::

  ``micrometer.properties`` は内容が空であっても必ず配置しなければならない。


.. _micrometer_metrics_output_example:

実行結果
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
以上で、 ``LoggingMeterRegistry`` を用いたメトリクスの収集ができるようになる。

アプリケーションを起動すると、以下のように収集されたメトリクスが標準出力に出力されていることを確認できる。

.. code-block:: text

  2020-09-04 15:33:40.689 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.gc.count{memory.manager.name=PS Scavenge} throughput=2.6/s
  2020-09-04 15:33:40.690 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.gc.count{memory.manager.name=PS MarkSweep} throughput=0.4/s
  2020-09-04 15:33:40.691 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.buffer.count{id=mapped} value=0 buffers
  2020-09-04 15:33:40.691 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.buffer.count{id=direct} value=2 buffers
  2020-09-04 15:33:40.692 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.buffer.memory.used{id=direct} value=124 KiB
  2020-09-04 15:33:40.692 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.buffer.memory.used{id=mapped} value=0 B
  2020-09-04 15:33:40.692 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.buffer.total.capacity{id=mapped} value=0 B
  2020-09-04 15:33:40.692 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.buffer.total.capacity{id=direct} value=124 KiB
  2020-09-04 15:33:40.693 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.classes.loaded{} value=9932 classes
  2020-09-04 15:33:40.693 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.gc.live.data.size{} value=0 B
  2020-09-04 15:33:40.693 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.gc.max.data.size{} value=2.65918 GiB
  2020-09-04 15:33:40.694 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.committed{area=heap,id=PS Old Gen} value=182.5 MiB
  2020-09-04 15:33:40.694 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.committed{area=heap,id=PS Survivor Space} value=44 MiB
  2020-09-04 15:33:40.694 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.committed{area=heap,id=PS Eden Space} value=197 MiB
  2020-09-04 15:33:40.694 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.committed{area=nonheap,id=Code Cache} value=29.125 MiB
  2020-09-04 15:33:40.694 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.committed{area=nonheap,id=Compressed Class Space} value=6.796875 MiB
  2020-09-04 15:33:40.695 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.committed{area=nonheap,id=Metaspace} value=55.789062 MiB
  2020-09-04 15:33:40.695 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.max{area=heap,id=PS Old Gen} value=2.65918 GiB
  2020-09-04 15:33:40.695 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.max{area=heap,id=PS Survivor Space} value=44 MiB
  2020-09-04 15:33:40.696 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.max{area=nonheap,id=Code Cache} value=240 MiB
  2020-09-04 15:33:40.696 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.max{area=nonheap,id=Metaspace} value=-1 B
  2020-09-04 15:33:40.696 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.max{area=heap,id=PS Eden Space} value=1.243652 GiB
  2020-09-04 15:33:40.696 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.max{area=nonheap,id=Compressed Class Space} value=1 GiB
  2020-09-04 15:33:40.697 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.used{area=nonheap,id=Code Cache} value=28.618713 MiB
  2020-09-04 15:33:40.697 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.used{area=nonheap,id=Compressed Class Space} value=6.270714 MiB
  2020-09-04 15:33:40.697 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.used{area=nonheap,id=Metaspace} value=54.118324 MiB
  2020-09-04 15:33:40.698 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.used{area=heap,id=PS Old Gen} value=69.320663 MiB
  2020-09-04 15:33:40.698 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.used{area=heap,id=PS Survivor Space} value=7.926674 MiB
  2020-09-04 15:33:40.698 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.memory.used{area=heap,id=PS Eden Space} value=171.750542 MiB
  2020-09-04 15:33:40.698 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.daemon{} value=28 threads
  2020-09-04 15:33:40.698 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.live{} value=29 threads
  2020-09-04 15:33:40.699 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.peak{} value=31 threads
  2020-09-04 15:33:40.702 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.states{state=blocked} value=0 threads
  2020-09-04 15:33:40.703 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.states{state=runnable} value=9 threads
  2020-09-04 15:33:40.703 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.states{state=new} value=0 threads
  2020-09-04 15:33:40.703 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.states{state=timed-waiting} value=3 threads
  2020-09-04 15:33:40.703 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.states{state=terminated} value=0 threads
  2020-09-04 15:33:40.704 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: jvm.threads.states{state=waiting} value=17 threads
  2020-09-04 15:33:41.199 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: process.cpu.usage{} value=0.111672
  2020-09-04 15:33:41.199 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: process.start.time{} value=444222h 33m 14.544s
  2020-09-04 15:33:41.199 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: process.uptime{} value=26.729s
  2020-09-04 15:33:41.200 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: system.cpu.count{} value=8
  2020-09-04 15:33:41.200 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: system.cpu.usage{} value=0.394545



.. _micrometer_registry_factory:

レジストリファクトリ
--------------------------------------------------
本アダプタでは、以下のレジストリのファクトリクラスを提供している。

.. list-table::

  * - レジストリ
    - ファクトリクラス
    - 提供しているアダプタのバージョン
  * - `SimpleMeterRegistry(外部サイト、英語)`_
    - :java:extdoc:`SimpleMeterRegistryFactory <nablarch.integration.micrometer.simple.SimpleMeterRegistryFactory>`
    - ``1.0.0`` 以上
  * - `LoggingMeterRegistry(外部サイト、英語)`_
    - :java:extdoc:`LoggingMeterRegistryFactory <nablarch.integration.micrometer.logging.LoggingMeterRegistryFactory>`
    - ``1.0.0`` 以上
  * - `CloudWatchMeterRegistry(外部サイト、英語)`_
    - :java:extdoc:`CloudWatchMeterRegistryFactory <nablarch.integration.micrometer.cloudwatch.CloudWatchMeterRegistryFactory>`
    - ``1.0.0`` 以上
  * - `DatadogMeterRegistry(外部サイト、英語)`_
    - :java:extdoc:`DatadogMeterRegistryFactory <nablarch.integration.micrometer.datadog.DatadogMeterRegistryFactory>`
    - ``1.0.0`` 以上
  * - `StatsdMeterRegistry(外部サイト、英語)`_
    - :java:extdoc:`StatsdMeterRegistryFactory <nablarch.integration.micrometer.statsd.StatsdMeterRegistryFactory>`
    - ``1.0.0`` 以上
  * - `OtlpMeterRegistry(外部サイト、英語)`_
    - :java:extdoc:`OtlpMeterRegistryFactory <nablarch.integration.micrometer.otlp.OtlpMeterRegistryFactory>`
    - ``1.3.0`` 以上


.. _micrometer_configuration:

設定ファイル
--------------------------------------------------

配置場所
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
本アダプタの設定ファイルは、クラスパス直下に ``micrometer.properties`` という名前で配置されるように作成する。

フォーマット
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
このファイルに記載する設定は、以下のフォーマットで記述する。

.. code-block:: text

  nablarch.micrometer.<subPrefix>.<key>=設定する値

ここで、 ``<subPrefix>`` に設定する値は、使用するレジストリファクトリごとに異なる値を指定する。

レジストリファクトリごとに、 ``<subPrefix>`` で指定する値を下記表に記載する。

=================================== ================
レジストリファクトリ                  subPrefix
=================================== ================
``SimpleMeterRegistryFactory``      ``simple``
``LoggingMeterRegistryFactory``     ``logging``
``CloudWatchMeterRegistryFactory``  ``cloudwatch``
``DatadogMeterRegistryFactory``     ``datadog``
``StatsdMeterRegistryFactory``      ``statsd``
``OtlpMeterRegistryFactory``        ``otlp``
=================================== ================

また、 ``<key>`` には Micrometer がレジストリごとに提供している `設定クラス(外部サイト、英語) <https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/config/MeterRegistryConfig.html>`_ で定義されたメソッドと同じ名前を指定する。

例えば、 `DatadogMeterRegistry(外部サイト、英語)`_ に対しては `DatadogConfig(外部サイト、英語)`_ という設定クラスが用意されている。
そして、この設定クラスには `apiKey(外部サイト、英語) <https://javadoc.io/doc/io.micrometer/micrometer-registry-datadog/1.13.0/io/micrometer/datadog/DatadogConfig.html#apiKey()>`_ というメソッドが定義されている。




したがって、 ``micrometer.properties`` に次のように記述することで、 ``apiKey`` を設定できる。

.. code-block:: text

  nablarch.micrometer.datadog.apiKey=XXXXXXXXXXXXXXXXXXXX

OS環境変数・システムプロパティで上書きする
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``micrometer.properties`` に記述した設定の値は、OS環境変数およびシステムプロパティで上書きできる。

設定値は、優先度の高い順に次の順番で採用される。

#. システムプロパティで指定した値
#. OS環境変数で指定した値
#. ``micrometer.properties`` の設定値

例えば、次のような条件で設定したとする。

micrometer.properties

  .. code-block:: text

    nablarch.micrometer.example.one=PROPERTIES
    nablarch.micrometer.example.two=PROPERTIES
    nablarch.micrometer.example.three=PROPERTIES

OS環境変数

  .. code-block:: text

    $ export NABLARCH_MICROMETER_EXAMPLE_TWO=OS_ENV

    $ export NABLARCH_MICROMETER_EXAMPLE_THREE=OS_ENV

システムプロパティ

  .. code-block:: text

    -Dnablarch.micrometer.example.three=SYSTEM_PROP

この場合、それぞれの設定値は最終的に次の値が採用される。

========== ================
key        採用される値
========== ================
``one``    ``PROPERTIES``
``two``    ``OS_ENV``
``three``  ``SYSTEM_PROP``
========== ================

OS環境変数で上書きするときの名前のルールについては、 :ref:`OS環境変数の名前について <repository-overwrite_environment_configuration_by_os_env_var_naming_rule>` を参照。

設定のプレフィックスを変更する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

設定のプレフィックス (``nablarch.micrometer.<subPrefix>``) は、各レジストリファクトリごとに :java:extdoc:`prefix <nablarch.integration.micrometer.MeterRegistryFactory.setPrefix(java.lang.String)>` プロパティを指定することで変更できる。

以下に、プレフィックスを変更する例を記載する。

.. code-block:: xml

  <component name="meterRegistry" class="nablarch.integration.micrometer.logging.LoggingMeterRegistryFactory">
    <property name="meterBinderListProvider" ref="meterBinderListProvider" />
    <property name="applicationDisposer" ref="disposer" />

    <!-- prefix プロパティに任意のプレフィックスを設定する -->
    <property name="prefix" value="sample.prefix" />
  </component>

この場合、 ``micrometer.properties`` は次のように設定できるようになる。

.. code-block:: text

  sample.prefix.step=10s

設定ファイルの場所を変更する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

設定ファイル（``micrometer.properties``）の場所は、以下の方法で変更できる。

まず、レジストリファクトリの :java:extdoc:`xmlConfigPath <nablarch.integration.micrometer.MeterRegistryFactory.setXmlConfigPath(java.lang.String)>` プロパティに、設定ファイルを読み込むXMLファイルのパスを指定する。

.. code-block:: xml

  <component name="meterRegistry" class="nablarch.integration.micrometer.logging.LoggingMeterRegistryFactory">
    <property name="meterBinderListProvider" ref="meterBinderListProvider" />
    <property name="applicationDisposer" ref="disposer" />

    <!-- 設定ファイルを読み込むXMLファイルのパスを指定 -->
    <property name="xmlConfigPath" value="config/metrics.xml" />
  </component>

そして、 ``xmlConfigPath`` プロパティで指定した場所に、設定ファイルを読み込むXMLファイルを配置する。
下記設定では、クラスパス内の ``config/metrics.properties`` が設定ファイルとして読み込まれるようになる。

.. code-block:: xml

  <?xml version="1.0" encoding="UTF-8"?>
  <component-configuration
          xmlns="http://tis.co.jp/nablarch/component-configuration"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://tis.co.jp/nablarch/component-configuration https://nablarch.github.io/schema/component-configuration.xsd">

    <!-- Micrometerアダプタの設定を読み込む -->
    <config-file file="config/metrics.properties" />

  </component-configuration>

.. tip::

  このXMLファイルはコンポーネント設定ファイルと同じ書式で記述できる。

  ただし、このファイルでコンポーネントを定義しても、システムリポジトリから参照を取得できない。


.. _micrometer_default_metrics:

DefaultMeterBinderListProviderで収集されるメトリクス
-----------------------------------------------------

:java:extdoc:`DefaultMeterBinderListProvider <nablarch.integration.micrometer.DefaultMeterBinderListProvider>` が生成する `MeterBinder(外部サイト、英語)`_ のリストには、以下のクラスが含まれている。


* `JvmMemoryMetrics(外部サイト、英語)`_
* `JvmGcMetrics(外部サイト、英語)`_
* `JvmThreadMetrics(外部サイト、英語)`_
* `ClassLoaderMetrics(外部サイト、英語)`_
* `ProcessorMetrics(外部サイト、英語)`_
* `FileDescriptorMetrics(外部サイト、英語)`_
* `UptimeMetrics(外部サイト、英語)`_
* :java:extdoc:`NablarchGcCountMetrics <nablarch.integration.micrometer.instrument.binder.jvm.NablarchGcCountMetrics>`



これにより、下記メトリクスが収集されるようになる。

.. list-table::

  * - メトリクス名
    - 説明
  * - ``jvm.buffer.count``
    - バッファプール内のバッファの数
  * - ``jvm.buffer.memory.used``
    - バッファプールの使用量
  * - ``jvm.buffer.total.capacity``
    - バッファプールの合計容量
  * - ``jvm.memory.used``
    - メモリプールのメモリ使用量
  * - ``jvm.memory.committed``
    - メモリプールのコミットされたメモリ量
  * - ``jvm.memory.max``
    - メモリプールの最大メモリ量
  * - ``jvm.gc.max.data.size``
    - OLD領域の最大メモリ量
  * - ``jvm.gc.live.data.size``
    - Full GC 後の OLD 領域のメモリ使用量
  * - ``jvm.gc.memory.promoted``
    - GC 前後で増加した、 OLD 領域のメモリ使用量の増分
  * - ``jvm.gc.memory.allocated``
    - 前回の GC 後から今回の GC までの、 Young 領域のメモリ使用量の増分
  * - ``jvm.gc.concurrent.phase.time``
    - コンカレントフェーズの処理時間
  * - ``jvm.gc.pause``
    - GC の一時停止に費やされた時間
  * - ``jvm.threads.peak``
    - スレッド数のピーク数
  * - ``jvm.threads.daemon``
    - 現在のデーモンスレッドの数
  * - ``jvm.threads.live``
    - 現在の非デーモンスレッドの数
  * - ``jvm.threads.states``
    - 現在のスレッドの状態ごとの数
  * - ``jvm.classes.loaded``
    - 現在ロードされているクラスの数
  * - ``jvm.classes.unloaded``
    - JVM が起動してから今までにアンロードされたクラスの数
  * - ``system.cpu.count``
    - JVM で使用できるプロセッサーの数
  * - ``system.load.average.1m``
    - 最後の1分のシステム負荷平均 （参考： `OperatingSystemMXBean(外部サイト) <https://docs.oracle.com/javase/jp/11/docs/api/java.management/java/lang/management/OperatingSystemMXBean.html#getSystemLoadAverage()>`_ ）
  * - ``system.cpu.usage``
    - システム全体の直近の CPU 使用率
  * - ``process.cpu.usage``
    - JVM の直近のCPU使用率
  * - ``process.files.open``
    - 開いているファイルディスクリプタの数
  * - ``process.files.max``
    - ファイルディスクリプタの最大数
  * - ``process.uptime``
    - JVM の稼働時間
  * - ``process.start.time``
    - JVM の起動時刻（UNIX 時間）
  * - ``jvm.gc.count``
    - GC の回数
  * - ``jvm.threads.started``
    - JVMで起動したスレッド数
  * - ``process.cpu.time``
    - Java仮想マシン・プロセスによって使用されるCPU時間

実際に収集されるメトリクスのイメージは :ref:`micrometer_metrics_output_example` を参照。

共通のタグを設定する
--------------------------------------------------

レジストリファクトリの :java:extdoc:`tags <nablarch.integration.micrometer.MeterRegistryFactory.setTags(java.util.Map)>` プロパティで、すべてのメトリクスに共通するタグを設定できる。

この機能は、アプリケーションが稼働しているホスト、インスタンス、リージョンなどを識別できる情報を設定するといった用途として使用できる。

以下に設定方法を記載する。

.. code-block:: xml

  <component name="meterRegistry" class="nablarch.integration.micrometer.logging.LoggingMeterRegistryFactory">
    <property name="meterBinderListProvider" ref="meterBinderListProvider" />
    <property name="applicationDisposer" ref="disposer" />

    <!-- tags プロパティで共通のタグを設定 -->
    <property name="tags">
      <map>
        <entry key="foo" value="FOO" />
        <entry key="bar" value="BAR" />
      </map>
    </property>
  </component>

``tags`` プロパティの型は ``Map<String, String>`` となっており、 ``<map>`` タグを使って設定できる。
このとき、マップのキーがタグの名前、マップの値がタグの値に対応付けられる。

上記設定の場合、収集されるメトリクスは次のようになる。

.. code-block:: text

  （省略）
  2020-09-04 17:30:06.656 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: process.start.time{bar=BAR,foo=FOO} value=444224h 29m 38.875000064s
  2020-09-04 17:30:06.656 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: process.uptime{bar=BAR,foo=FOO} value=27.849s
  2020-09-04 17:30:06.656 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: system.cpu.count{bar=BAR,foo=FOO} value=8
  2020-09-04 17:30:06.657 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: system.cpu.usage{bar=BAR,foo=FOO} value=0.475654

全てのメトリクスに、 ``foo=FOO``, ``bar=BAR`` のタグが設定されていることが確認できる。

監視サービスと連携する
--------------------------------------------------

監視サービスと連携するためには、大きく次のとおり設定する必要がある。

#. 監視サービスや連携方法ごとに用意された Micrometer のモジュールを依存関係に追加する
#. 使用するレジストリファクトリをコンポーネントとして定義する
#. その他、監視サービスごとに独自に設定する

ここでは、それぞれの監視サービスと連携する方法について説明する。


Datadog と連携する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

依存関係を追加する
  .. code-block:: xml

    <dependency>
      <groupId>io.micrometer</groupId>
      <artifactId>micrometer-registry-datadog</artifactId>
      <version>1.13.0</version>
    </dependency>

レジストリファクトリを宣言する
  .. code-block:: xml
  
    <component name="meterRegistry" class="nablarch.integration.micrometer.datadog.DatadogMeterRegistryFactory">
      <property name="meterBinderListProvider" ref="meterBinderListProvider" />
      <property name="applicationDisposer" ref="disposer" />
    </component>

APIキーを設定する
  .. code-block:: text

    nablarch.micrometer.datadog.apiKey=XXXXXXXXXXXXXXXX

  APIキーは ``nablarch.micrometer.datadog.apiKey`` で設定できる。

サイトURLを設定する
  .. code-block:: text

    nablarch.micrometer.datadog.uri=<サイトURL>

  サイトURLは ``nablarch.micrometer.datadog.uri`` で設定できる。

  その他の設定については `DatadogConfig(外部サイト、英語)`_ を参照。

連携を無効にする
  .. code-block:: text

    nablarch.micrometer.datadog.enabled=false
    nablarch.micrometer.datadog.apiKey=XXXXXXXXXXXXXXXX

  ``micrometer.properties`` で ``nablarch.micrometer.datadog.enabled`` に ``false`` を設定することで、メトリクスの連携を無効にできる。
  この設定は環境変数で上書きできるので、本番環境のみ環境変数で ``true`` に上書きして連携を有効にできる。

  .. important::
    連携を無効にした場合も、 ``nablarch.micrometer.datadog.apiKey`` には何らかの値を設定しておく必要がある。
    値はダミーで問題ない。

CloudWatch と連携する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

依存関係を追加する
  .. code-block:: xml

    <dependency>
      <groupId>io.micrometer</groupId>
      <artifactId>micrometer-registry-cloudwatch2</artifactId>
      <version>1.13.0</version>
    </dependency>

レジストリファクトリを宣言する
  .. code-block:: xml
  
    <component name="meterRegistry" class="nablarch.integration.micrometer.cloudwatch.CloudWatchMeterRegistryFactory">
      <property name="meterBinderListProvider" ref="meterBinderListProvider" />
      <property name="applicationDisposer" ref="disposer" />
    </component>

リージョンやアクセスキーを設定する
  .. code-block:: bash
    
    $ export AWS_REGION=ap-northeast-1

    $ export AWS_ACCESS_KEY_ID=XXXXXXXXXXXXXXXXXXXXX

    $ export AWS_SECRET_ACCESS_KEY=YYYYYYYYYYYYYYYYYYYYY

  ``micrometer-registry-cloudwatch2`` モジュールは AWS SDK を使用している。
  したがって、リージョンやアクセスキーなどの設定は AWS SDK の方法に準拠する。

  上記は、LinuxでOS環境変数を使って設定する場合の例を記載している。
  より詳細な情報は、 `AWSのドキュメント(外部サイト) <https://docs.aws.amazon.com/ja_jp/sdk-for-java/v1/developer-guide/setup-credentials.html>`_ を参照。

名前空間を設定する
  .. code-block:: text

    nablarch.micrometer.cloudwatch.namespace=test

  メトリクスのカスタム名前空間は ``nablarch.micrometer.cloudwatch.namespace`` で設定できる。

  その他の設定については `CloudWatchConfig(外部サイト、英語)`_ を参照。

より詳細な設定
  OS環境変数や設定ファイルでは指定できない、より詳細に設定したい場合は、 :java:extdoc:`CloudWatchAsyncClientProvider <nablarch.integration.micrometer.cloudwatch.CloudWatchAsyncClientProvider>` を実装したカスタムプロバイダを作ることで対応できる。

  .. code-block:: java

      package example.micrometer.cloudwatch;

      import nablarch.integration.micrometer.cloudwatch.CloudWatchAsyncClientProvider;
      import software.amazon.awssdk.services.cloudwatch.CloudWatchAsyncClient;

      public class CustomCloudWatchAsyncClientProvider implements CloudWatchAsyncClientProvider {
          @Override
          public CloudWatchAsyncClient provide() {
              return CloudWatchAsyncClient
                      .builder()
                      .asyncConfiguration(...) // 任意の設定を行う
                      .build();
          }
      }

  :java:extdoc:`CloudWatchAsyncClientProvider <nablarch.integration.micrometer.cloudwatch.CloudWatchAsyncClientProvider>` は ``CloudWatchAsyncClient`` を提供する ``provide()`` メソッドを持つ。
  カスタムプロバイダでは、任意の設定を行った ``CloudWatchAsyncClient`` を構築して返すように ``provide()`` メソッドを実装する。

  .. code-block:: xml

    <component name="meterRegistry" class="nablarch.integration.micrometer.cloudwatch.CloudWatchMeterRegistryFactory">
      <property name="meterBinderListProvider" ref="meterBinderListProvider" />
      <property name="applicationDisposer" ref="disposer" />

      <!-- cloudWatchAsyncClientProvider プロパティにカスタムプロバイダを設定する -->
      <property name="cloudWatchAsyncClientProvider">
        <component class="example.micrometer.cloudwatch.CustomCloudWatchAsyncClientProvider" />
      </property>
    </component>

  作成したカスタムプロバイダは、 ``CloudWatchMeterRegistryFactory`` の :java:extdoc:`cloudWatchAsyncClientProvider <nablarch.integration.micrometer.cloudwatch.CloudWatchMeterRegistryFactory.setCloudWatchAsyncClientProvider(nablarch.integration.micrometer.cloudwatch.CloudWatchAsyncClientProvider)>` プロパティに設定する。

  これにより、カスタムプロバイダが生成した ``CloudWatchAsyncClient`` がメトリクスの連携で使用されるようになる。

  .. tip::

    デフォルトでは、 `CloudWatchAsyncClient.create() (外部サイト、英語) <https://javadoc.io/static/software.amazon.awssdk/cloudwatch/2.13.4/software/amazon/awssdk/services/cloudwatch/CloudWatchAsyncClient.html#create-->`_ で作成されたインスタンスが使用される。

連携を無効にする
  .. code-block:: text

    nablarch.micrometer.cloudwatch.enabled=false
    nablarch.micrometer.cloudwatch.namespace=test

  ``micrometer.properties`` で ``nablarch.micrometer.cloudwatch.enabled`` に ``false`` を設定することで、メトリクスの連携を無効にできる。
  この設定は環境変数で上書きできるので、本番環境のみ環境変数で ``true`` に上書きして連携を有効にできる。

  .. important::
    連携を無効にした場合も、 ``nablarch.micrometer.cloudwatch.namespace`` には何らかの値を設定しておく必要がある。
    また、環境変数 ``AWS_REGION`` を設定しておく必要がある。

    いずれも、値はダミーで問題ない。

Azure と連携する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MicrometerでメトリクスをAzureに連携する方法
  Azureは、JavaアプリケーションからAzureにメトリクスを連携するための仕組みとして、Javaエージェントを用いた方法(**Java 3.0 エージェント**)を提供している。

  * `Azure Monitor Application Insights を監視する Java のコード不要のアプリケーション(外部サイト) <https://learn.microsoft.com/ja-jp/azure/azure-monitor/app/opentelemetry-enable?tabs=java>`_

  このJava 3.0 エージェントは、Micrometerの `グローバルレジストリ(外部サイト、英語) <https://docs.micrometer.io/micrometer/reference/concepts/registry.html#_global_registry>`_ に出力したメトリクスを自動的に収集し、Azureに連携する仕組みを提供している。

  * `アプリケーションからカスタム テレメトリを送信する(外部サイト) <https://learn.microsoft.com/ja-jp/azure/azure-monitor/app/opentelemetry-enable?tabs=java>`_

  .. important::
    Java 3.0 エージェントは、初期化処理中に大量のjarファイルをロードする。
    これにより、Java 3.0 エージェントの初期化処理中はGCが頻発することがある。

    このため、アプリケーション起動後しばらくは、GCの影響により性能が一時的に劣化する可能性がある点に注意すること。

    また、高負荷時は Java 3.0 エージェントの処理によるオーバーヘッドが性能に影響を与える可能性がある。
    したがって、性能試験では本番同様に Java 3.0 エージェントを導入し、想定内の性能になることを確認すること。


  Java 3.0 エージェントの設定方法は :ref:`Azureにおける分散トレーシング <azure_distributed_tracing>` 参照。

MicrometerアダプタでメトリクスをAzureに連携するための設定
  MicrometerアダプタでメトリクスをAzureに連携するためには、以下のとおり設定する必要がある。

  * アプリケーションの起動オプションに、Java 3.0 エージェントを追加する
  * ``MeterRegistry`` にグローバルレジストリを使うようにコンポーネントを定義する

  1つ目の起動オプションの設定方法については、 `Azureのドキュメント <https://learn.microsoft.com/ja-jp/azure/azure-monitor/app/opentelemetry-enable?tabs=java#modify-your-application>`_ を参照のこと。

  2つ目のグローバルレジストリを使う方法について、本アダプタではグローバルレジストリのファクトリクラスとして :java:extdoc:`GlobalMeterRegistryFactory <nablarch.integration.micrometer.GlobalMeterRegistryFactory>` を用意している。
  以下に、このファクトリクラスのコンポーネント定義の例を示す。

  .. code-block:: xml

    <component name="meterRegistry" class="nablarch.integration.micrometer.GlobalMeterRegistryFactory">
      <property name="meterBinderListProvider" ref="meterBinderListProvider" />
      <property name="applicationDisposer" ref="disposer" />
    </component>

  この設定により、メトリクスの収集はグローバルレジストリによって行われるようになる。
  そして、グローバルレジストリで収集されたメトリクスは、Java 3.0 エージェントによってAzureに連携されるようになる。

  .. tip::
    Java 3.0 エージェントを使うこの方法では、Azure用の ``MeterRegistry`` は使用しない。
    したがって、Azure用のモジュールを依存関係に追加しなくてもメトリクスを連携できる。


詳細設定について
  メトリクスの連携は、Azureが提供するJava 3.0 エージェントによって行われる。
  このため、メトリクスの連携に関する設定は全てJava 3.0 エージェントが提供する方法で行う必要がある。

  Java 3.0 エージェントの設定の詳細については、 `構成オプション(外部サイト) <https://learn.microsoft.com/ja-jp/azure/azure-monitor/app/java-standalone-config>`_ を参照のこと。

  .. important::
    本アダプタ用の設定ファイルである ``micrometer.properties`` は使用できないが、ファイルは配置しておく必要がある（内容は空で構わない）。

連携を無効にする
  Java 3.0 エージェントを使用せずにアプリケーションを起動することで、メトリクスの連携を無効にできる。

StatsD で連携する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Datadog は `DogStatsD(外部サイト) <https://docs.datadoghq.com/ja/developers/dogstatsd/?tab=hostagent>`_ という `StatsD(外部サイト、英語) <https://github.com/statsd/statsd>`_ プロトコルを使った連携をサポートしている。
したがって、 ``micrometer-registry-statsd`` モジュールを用いることで、 StatsD で Datadog と連携することもできる。

ここでは、 Datadog に StatsD プロトコルで連携する場合を例にして説明する。
なお、DogStatsD のインストール方法などについては `Datadogのサイト(外部サイト) <https://docs.datadoghq.com/ja/agent/>`_ を参照。

依存関係を追加する
  .. code-block:: xml

    <dependency>
      <groupId>io.micrometer</groupId>
      <artifactId>micrometer-registry-statsd</artifactId>
      <version>1.13.0</version>
    </dependency>

レジストリファクトリを宣言する
  .. code-block:: xml
  
    <component name="meterRegistry" class="nablarch.integration.micrometer.statsd.StatsdMeterRegistryFactory">
      <property name="meterBinderListProvider" ref="meterBinderListProvider" />
      <property name="applicationDisposer" ref="disposer" />
    </component>

必要に応じて設定ファイルを記述する
  StatsD デーモンと連携するための設定は、デフォルト値が DogStatsD をデフォルト構成でインストールした場合と一致するように調整されている。
  
  したがって、 DogStatsD をデフォルトの構成でインストールしている場合は、特に設定を明示しなくても DogStatsD による連携が動作する。

  もしデフォルト構成以外でインストールしている場合は、 `StatsdConfig(外部サイト、英語)`_ を参照して、実際の環境に合わせた設定を行うこと。

  .. code-block:: text

    # ポートを変更
    nablarch.micrometer.statsd.port=9999

連携を無効にする
  .. code-block:: text

    nablarch.micrometer.statsd.enabled=false

  ``micrometer.properties`` で ``nablarch.micrometer.statsd.enabled`` に ``false`` を設定することで、メトリクスの連携を無効にできる。
  この設定は環境変数で上書きできるので、本番環境のみ環境変数で ``true`` に上書きして連携を有効にできる。

OpenTelemetry Protocol (OTLP) で連携する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

多くの監視サービスでは `OpenTelemetry(外部サイト) <https://opentelemetry.io/ja>`_ をサポートしており、通信プロトコルに OpenTelemetry Protocol (以下、OTLP) を使用してメトリクスを収集できる。
``micrometer-registry-otlp`` モジュールを用いることで、 OTLP で様々な監視サービスと連携できる。

  .. important::
     OpenTelemetry によるメトリクスの収集では、どういった連携方法が適しているか（利用可能か）は監視サービスによって異なるため、使用する監視サービスの情報を確認すること。
     例として、いくつかの監視サービスの情報を以下に示す。

     * `Datadog の OpenTelemetry(外部サイト) <https://docs.datadoghq.com/ja/opentelemetry/>`_
     * `New RelicによるOpenTelemetryの紹介(外部サイト) <https://docs.newrelic.com/jp/docs/opentelemetry/opentelemetry-introduction>`_
     * `Prometheus | HTTP API | OTLP Receiver(外部サイト、英語) <https://prometheus.io/docs/prometheus/latest/querying/api/#otlp-receiver>`_

ここでは、localhost の 9090 ポートで起動している Prometheus に OTLP で連携する場合を例にして説明する。

依存関係を追加する
  .. code-block:: xml

    <dependency>
      <groupId>io.micrometer</groupId>
      <artifactId>micrometer-registry-otlp</artifactId>
      <version>1.13.0</version>
    </dependency>

レジストリファクトリを宣言する
  .. code-block:: xml
  
    <component name="meterRegistry" class="nablarch.integration.micrometer.otlp.OtlpMeterRegistryFactory">
      <property name="meterBinderListProvider" ref="meterBinderListProvider" />
      <property name="applicationDisposer" ref="disposer" />
    </component>

設定ファイルを記述する
  .. code-block:: text

    # 送信先を変更
    nablarch.micrometer.otlp.url=http://localhost:9090/api/v1/otlp/v1/metrics

ヘッダ情報を設定する
  .. code-block:: text

    nablarch.micrometer.otlp.headers=key1=value1,key2=value2

  認証で使用するAPIキー等のヘッダ情報が必要な場合、 ``nablarch.micrometer.otlp.headers`` で設定できる。

連携を無効にする
  .. code-block:: text

    nablarch.micrometer.otlp.enabled=false

  ``micrometer.properties`` で ``nablarch.micrometer.otlp.enabled`` に ``false`` を設定することで、メトリクスの連携を無効にできる。
  この設定は環境変数で上書きできるので、本番環境のみ環境変数で ``true`` に上書きして連携を有効にできる。

アプリケーションの形式ごとに収集するメトリクスの例
---------------------------------------------------------

ここでは、アプリケーションの形式（ウェブ・バッチ）ごとに、どのようなメトリクスを収集すると良いか説明する。

ウェブアプリケーションで収集するメトリクスの例
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

HTTPリクエストの処理時間
  HTTPリクエストごとの処理時間を計測することで、以下のようなことができるようになる。

  * 各URLごとにどの程度アクセスがあるか確認する
  * リクエストの処理にどれくらい時間がかかっているか確認する

  また、パーセンタイルを計測することで、大部分のリクエストがどれくらいの時間で処理できているかを確認できるようにもなる。

  これらのメトリクスを収集する方法については、以下のガイドを参照のこと。

  * :ref:`micrometer_timer_metrics_handler`
  * :ref:`micrometer_timer_metrics_handler_percentiles`

SQLの処理時間
  SQLの処理時間を計測することで、以下のようなことができるようになる。

  * それぞれのSQLがどの程度の時間で処理されているか確認する
  * 想定よりも時間がかかっているSQLが無いか確認する

  SQLの処理時間を計測する方法については、以下のガイドを参照のこと。

  * :ref:`micrometer_sql_time`

ログレベルごとの出力回数
  ログレベルごとの出力回数を計測することで、以下のようなことができるようになる。

  * 警告ログが異常な回数出力されていないか確認する（攻撃の検知）
  * エラーログを検知する

  ログレベルごとの出力回数については、以下のガイドを参照のこと。

  * :ref:`micrometer_log_count`

アプリケーションサーバやライブラリが提供するリソースの情報
  アプリケーションサーバやライブラリが提供するリソース（スレッドプールやDBのコネクションプールなど）の状態を
  メトリクスとして収集しておくことで、障害発生時に原因箇所を特定するための情報源として活用できるようになる。

  多くのアプリケーションサーバは、リソースの状態をJMXのMBeanを通じて公開している。
  MBeanの情報を収集する方法については、以下のガイドを参照のこと。

  * :ref:`micrometer_mbean_metrics`

バッチアプリケーションで収集するメトリクスの例
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

バッチの処理時間
  普段からバッチの処理時間を計測しておくことで、平常時の処理時間を知ることができる。
  これにより、処理時間が平常時とは異なる値になったときに、異常を迅速に検知できるようになる。

  バッチの処理時間は、 :ref:`micrometer_default_metrics` で収集される ``process.uptime`` で計測できる。

トランザクション単位の処理時間
  トランザクション単位の処理時間を計測することで、マルチスレッドのバッチが均等に処理を分散できているかなどを確認できるようになる。

  また、バッチの処理時間と同様に、処理時間が平常時から逸脱したときにも異常を迅速に検知できる。

  バッチのトランザクション単位の処理時間の計測については、以下のガイドを参照のこと。

  * :ref:`micrometer_adaptor_batch_transaction_time`

バッチの処理件数
  バッチの処理件数を計測することで、以下のようなことができるようになる。

  * バッチの進捗状況を確認する
  * 想定通りの速度で処理が進んでいるか確認する
  * 想定通りの件数が処理できているか確認する

  バッチの処理件数の計測については、以下のガイドを参照のこと。

  * :ref:`micrometer_batch_processed_count`

SQLの処理時間
  SQLの処理時間を計測することで、以下のようなことができるようになる。

  * それぞれのSQLがどの程度の時間で処理されているか確認する
  * 想定よりも時間がかかっているSQLが無いか確認する

  SQLの処理時間を計測する方法については、以下のガイドを参照のこと。

  * :ref:`micrometer_sql_time`

ログレベルごとの出力回数
  ログレベルごとの出力回数を計測することで、警告ログやエラーログの検知ができるようになる。

  ログレベルごとの出力回数については、以下のガイドを参照のこと。

  * :ref:`micrometer_log_count`

ライブラリが提供するリソースの情報
  ライブラリが提供するリソース（DBのコネクションプールなど）の状態をメトリクスとして収集しておくことで、
  障害発生時に原因箇所を特定するための情報源として活用できるようになる。

  ライブラリによっては、リソースの状態をJMXのMBeanで公開していることがある。
  MBeanの情報を収集する方法については、以下のガイドを参照のこと。

  * :ref:`micrometer_mbean_metrics`


.. _micrometer_timer_metrics_handler:

処理時間を計測するハンドラ
--------------------------------------------------

:java:extdoc:`TimerMetricsHandler <nablarch.integration.micrometer.instrument.handler.TimerMetricsHandler>` をハンドラキューに設定すると、後続ハンドラの処理時間を計測しメトリクスとして収集できるようになる。
これにより、ハンドラキュー内の処理の平均処理時間や最大処理時間をモニタできるようになる。

``TimerMetricsHandler`` には、 :java:extdoc:`HandlerMetricsMetaDataBuilder <nablarch.integration.micrometer.instrument.handler.HandlerMetricsMetaDataBuilder>` インタフェースを実装したクラスのインスタンスを設定する必要がある。
``HandlerMetricsMetaDataBuilder`` は、収集したメトリクスに設定する以下のメタ情報を構築する機能を提供する。

* メトリクスの名前
* メトリクスの説明
* メトリクスに設定するタグの一覧

``HandlerMetricsMetaDataBuilder`` の実装例を以下に示す。

.. code-block:: java

  import io.micrometer.core.instrument.Tag;
  import nablarch.fw.ExecutionContext;
  import nablarch.integration.micrometer.instrument.handler.HandlerMetricsMetaDataBuilder;

  import java.util.Arrays;
  import java.util.List;

  public class CustomHandlerMetricsMetaDataBuilder<TData, TResult>
      implements HandlerMetricsMetaDataBuilder<TData, TResult> {
    
      @Override
      public String getMetricsName() {
          return "metrics.name";
      }

      @Override
      public String getMetricsDescription() {
          return "Description of this metrics.";
      }

      @Override
      public List<Tag> buildTagList(TData param, ExecutionContext executionContext, TResult tResult, Throwable thrownThrowable) {
          return Arrays.asList(Tag.of("foo", "FOO"), Tag.of("bar", "BAR"));
      }
  }

``getMetricsName()`` と ``getMetricsDescription()`` は、それぞれメトリクスの名前と説明を返すように実装する。

``buildTagList()`` には、ハンドラに渡されたパラメータと後続ハンドラの実行結果、そして後続ハンドラがスローした例外が渡される（例外がスローされていない場合は ``null``）。
本メソッドは必要に応じてこれらの情報を参照し、メトリクスに設定するタグの一覧を ``List<io.micrometer.core.instrument.Tag>`` で返すように実装する。

次に、 ``TimerMetricsHandler`` をハンドラキューに設定する例を以下に示す。

.. code-block:: xml

  <!-- ハンドラキュー構成 -->
  <component name="webFrontController"
             class="nablarch.fw.web.servlet.WebFrontController">
    <property name="handlerQueue">
      <list>
        <!-- 省略 -->

        <component class="nablarch.integration.micrometer.instrument.handler.TimerMetricsHandler">
          <property name="meterRegistry" ref="meterRegistry" />

          <property name="handlerMetricsMetaDataBuilder">
            <component class="xxx.CustomHandlerMetricsMetaDataBuilder" />
          </property>
        </component>

        <!-- 省略 -->
      </list>
    </property>
  </component>

ハンドラキューに ``TimerMetricsHandler`` を追加し、 ``handlerMetricsMetaDataBuilder`` プロパティに作成した ``HandlerMetricsMetaDataBuilder`` のコンポーネントを設定する。

また ``meterRegistry`` プロパティには、使用しているレジストリファクトリが生成した `MeterRegistry(外部サイト、英語)`_ を渡すように設定する。

これにより、ここより後ろのハンドラの処理時間をメトリクスとして収集できるようになる。

なお、Nablarchでは ``HandlerMetricsMetaDataBuilder`` の実装として以下の機能を提供するクラスを用意している。
詳細は、リンク先の説明を参照のこと。

* :ref:`micrometer_adaptor_http_request_process_time_metrics`

.. _micrometer_timer_metrics_handler_percentiles:

パーセンタイルを収集する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``TimerMetricsHandler`` には、パーセンタイル値を監視サービスに連携するために以下のプロパティが用意されている。

.. list-table::

  * - プロパティ
    - 説明
  * - ``percentiles``
    - 収集するパーセンタイル値のリスト。
      95パーセンタイルを収集する場合、 ``0.95`` と指定する。
  * - ``enablePercentileHistogram``
    - 収集したヒストグラムのバケットを監視サービスに連携するかどうかのフラグ。
      連携先の監視サービスがヒストグラムからパーセンタイル値を計算する仕組みをサポートしていない場合、この設定は無視される。
  * - ``serviceLevelObjectives``
    - 収集するヒストグラムに追加するバケットの値のリスト。
      単位はミリ秒。
      この値は、SLO(Service Level Objective)に基づいて設定する。
  * - ``minimumExpectedValue``
    - 収集するヒストグラムバケットの最小値を設定する。
      単位はミリ秒。
  * - ``maximumExpectedValue``
    - 収集するヒストグラムバケットの最大値を設定する。
      単位はミリ秒。

これらのプロパティは、Micrometerが提供する `Timer(外部サイト、英語)`_ に設定する値として使用される。
より詳細な説明は、 `Micrometerのドキュメント <https://docs.micrometer.io/micrometer/reference/concepts/histogram-quantiles.html>`_ を参照のこと。

なお、これらのプロパティはデフォルトでは全て未設定のため、パーセンタイルの情報は収集されない。
パーセンタイルの情報を収集する必要がある場合は、これらのプロパティを明示的に設定すること。
以下に、設定例を示す。

.. code-block:: xml

  <component class="nablarch.integration.micrometer.instrument.handler.TimerMetricsHandler">
    <property name="meterRegistry" ref="meterRegistry" />
    <property name="handlerMetricsMetaDataBuilder">
      <component class="nablarch.integration.micrometer.instrument.http.HttpRequestTimeMetricsMetaDataBuilder" />
    </property>

    <!-- 98, 90, 50 パーセンタイルを収集する -->
    <property name="percentiles">
      <list>
        <value>0.98</value>
        <value>0.90</value>
        <value>0.50</value>
      </list>
    </property>

    <!-- ヒストグラムバケットを監視サービスに連携する -->
    <property name="enablePercentileHistogram" value="true" />

    <!-- SLO として 1000ms, 1500ms を設定 -->
    <property name="serviceLevelObjectives">
      <list>
        <value>1000</value>
        <value>1500</value>
      </list>
    </property>
    
    <!-- バケットの最小値に 500 ms を設定 -->
    <property name="minimumExpectedValue" value="500" />
    <!-- バケットの最大値に 3000 ms を設定 -->
    <property name="maximumExpectedValue" value="3000" />
  </component>

ヒストグラムバケットをサポートする ``MeterRegistry`` を使用した場合、上記設定により次のようなメトリクスが収集できるようになる。

.. code-block:: text

  http_server_requests_seconds{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",quantile="0.98",} 1.475346432
  http_server_requests_seconds{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",quantile="0.9",} 1.408237568
  http_server_requests_seconds{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",quantile="0.5",} 0.737148928
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="0.5",} 9.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="0.536870911",} 9.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="0.626349396",} 12.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="0.715827881",} 16.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="0.805306366",} 16.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="0.894784851",} 17.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="0.984263336",} 17.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="1.0",} 18.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="1.073741824",} 20.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="1.431655765",} 29.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="1.5",} 32.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="1.789569706",} 32.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="2.147483647",} 32.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="2.505397588",} 32.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="2.863311529",} 32.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="3.0",} 32.0
  http_server_requests_seconds_bucket{class="com.nablarch.example.app.web.action.MetricsAction",exception="None",httpMethod="GET",method="index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext",outcome="SUCCESS",status="200",le="+Inf",} 32.0

.. tip::
  本アダプタで提供している ``MeterRegistry`` では ``OtlpMeterRegistry`` のみがヒストグラムバケットをサポートする。

  例では、ヒストグラムバケットの具体例（``http_server_requests_seconds_bucket``）を示すため `PrometheusMeterRegistry(外部サイト、英語)`_ を使用している（`Prometheus(外部サイト、英語) <https://prometheus.io/>`_ は、ヒストグラムによるパーセンタイルの計算をサポートしている）。
  ただし、 ``PrometheusMeterRegistry`` の ``MeterRegistryFactory`` は、本アダプタでは提供していない。
  実際に ``PrometheusMeterRegistry`` を試したい場合は、以下のようなクラスを自前で用意すること。

  .. code-block:: java

    package example.micrometer.prometheus;

    import io.micrometer.prometheusmetrics.PrometheusConfig;
    import io.micrometer.prometheusmetrics.PrometheusMeterRegistry;
    import nablarch.core.repository.di.DiContainer;
    import nablarch.integration.micrometer.MeterRegistryFactory;
    import nablarch.integration.micrometer.MicrometerConfiguration;
    import nablarch.integration.micrometer.NablarchMeterRegistryConfig;

    public class PrometheusMeterRegistryFactory extends MeterRegistryFactory<PrometheusMeterRegistry> {

        @Override
        protected PrometheusMeterRegistry createMeterRegistry(MicrometerConfiguration micrometerConfiguration) {
            return new PrometheusMeterRegistry(new Config(prefix, micrometerConfiguration));
        }

        @Override
        public PrometheusMeterRegistry createObject() {
            return doCreateObject();
        }

        static class Config extends NablarchMeterRegistryConfig implements PrometheusConfig {

            public Config(String prefix, DiContainer diContainer) {
                super(prefix, diContainer);
            }

            @Override
            protected String subPrefix() {
                return "prometheus";
            }
        }
    }

あらかじめ用意されているHandlerMetricsMetaDataBuilderの実装
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ここでは、Nablarchによってあらかじめ用意されている ``HandlerMetricsMetaDataBuilder`` の実装クラスについて紹介する。

.. _micrometer_adaptor_http_request_process_time_metrics:

HTTPリクエストの処理時間を収集する
*********************************************************************

:java:extdoc:`HttpRequestTimeMetricsMetaDataBuilder <nablarch.integration.micrometer.instrument.http.HttpRequestTimeMetricsMetaDataBuilder>` は、HTTPリクエストの処理時間計測のためのメトリクスのメタ情報を構築する。

本クラスは、メトリクスの名前に ``http.server.requests`` を使用する。

また、本クラスは以下のタグを生成する。

.. list-table::

  * - タグ名
    - 説明
  * - ``class``
    - リクエストを処理したアクションクラスの名前(``Class.getName()``)。
      取得できない場合は ``UNKNOWN``。
  * - ``method``
    - リクエストを処理したアクションクラスのメソッド名と、引数の型名(``Class.getCanonicalName()``)をアンダースコア(``_``)で繋げた文字列。
      取得できない場合は ``UNKNOWN``。
  * - ``httpMethod``
    - HTTPメソッド
  * - ``status``
    - HTTPステータスコード
  * - ``outcome``
    - ステータスコードの種類を表す文字列（1XX: ``INFORMATION``, 2XX: ``SUCCESS``, 3XX: ``REDIRECTION``, 4XX: ``CLIENT_ERROR``, 5XX: ``SERVER_ERROR``, その他: ``UNKNOWN``）
  * - ``exception``
    - リクエスト処理中のスローされた例外の単純名（例外スローされていない場合は ``None``）

本クラスを使った場合の設定例を以下に示す。

.. code-block:: xml

  <!-- ハンドラキュー構成 -->
  <component name="webFrontController"
             class="nablarch.fw.web.servlet.WebFrontController">
    <property name="handlerQueue">
      <list>
        <!-- HTTPリクエストの処理時間のメトリクス収集ハンドラ -->
        <component class="nablarch.integration.micrometer.instrument.handler.TimerMetricsHandler">
          <!-- レジストリファクトリが生成する MeterRegistry を meterRegistry プロパティに設定する -->
          <property name="meterRegistry" ref="meterRegistry" />

          <!-- HttpRequestTimeMetricsMetaDataBuilder を handlerMetricsMetaDataBuilder に設定する -->
          <property name="handlerMetricsMetaDataBuilder">
            <component class="nablarch.integration.micrometer.instrument.http.HttpRequestTimeMetricsMetaDataBuilder" />
          </property>
        </component>

        <component class="nablarch.fw.web.handler.HttpCharacterEncodingHandler"/>

        <!-- 省略 -->
     </list>
    </property>
  </component>

リクエスト全体の処理時間を計測するため、 ``TimerMetricsHandler`` はハンドラキューの先頭に設定する。

以上の設定で、 ``LoggingMeterRegistry`` を使っていた場合は次のようなメトリクスが収集されるようになる。

.. code-block:: text

  2020-10-06 13:52:10.309 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: http.server.requests{class=com.nablarch.example.app.web.action.AuthenticationAction,exception=None,httpMethod=POST,method=login_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext,outcome=REDIRECTION,status=303} throughput=0.2/s mean=0.4617585s max=0.4617585s
  2020-10-06 13:52:10.309 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: http.server.requests{class=com.nablarch.example.app.web.action.IndustryAction,exception=None,httpMethod=GET,method=find,outcome=SUCCESS,status=200} throughput=0.2/s mean=0.103277s max=0.103277s
  2020-10-06 13:52:10.310 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: http.server.requests{class=com.nablarch.example.app.web.action.AuthenticationAction,exception=None,httpMethod=GET,method=index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext,outcome=SUCCESS,status=200} throughput=0.2/s mean=4.7409146s max=4.7409146s
  2020-10-06 13:52:10.310 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: http.server.requests{class=com.nablarch.example.app.web.action.ProjectAction,exception=None,httpMethod=GET,method=index_nablarch.fw.web.HttpRequest_nablarch.fw.ExecutionContext,outcome=SUCCESS,status=200} throughput=0.2/s mean=0.5329547s max=0.5329547s

.. _micrometer_adaptor_batch_transaction_time:

バッチのトランザクション単位の処理時間を計測する
--------------------------------------------------

:java:extdoc:`BatchTransactionTimeMetricsLogger <nablarch.integration.micrometer.instrument.batch.BatchTransactionTimeMetricsLogger>` を使用することで、 :ref:`nablarch_batch` のトランザクション単位の処理時間をメトリクスとして計測できるようになる。
これにより、トランザクション単位の平均処理時間や最大処理時間をモニタできるようになる。

``BatchTransactionTimeMetricsLogger`` は `Timer(外部サイト、英語)`_ を使って ``batch.transaction.time`` という名前でメトリクスを収集する。
この名前は、 :java:extdoc:`setMetricsName(String) <nablarch.integration.micrometer.instrument.batch.BatchTransactionTimeMetricsLogger.setMetricsName(java.lang.String)>` で変更できる。

また、メトリクスには以下のタグが付与される。

.. list-table::

  * - タグ名
    - 説明
  * - ``class``
    - アクションのクラス名（ :ref:`-requestPath <nablarch_batch-resolve_action>` から取得した値）

以下に ``BatchTransactionTimeMetricsLogger`` を使うための設定例を示す。

.. code-block:: xml

  <!-- CommitLogger を複数組み合わせる -->
  <component name="commitLogger"
             class="nablarch.core.log.app.CompositeCommitLogger">
    <property name="commitLoggerList">
      <list>
        <!-- デフォルトの CommitLogger を設定 -->
        <component class="nablarch.core.log.app.BasicCommitLogger">
          <property name="interval" value="${nablarch.commitLogger.interval}" />
        </component>

        <!-- トランザクション単位の処理時間の計測 -->
        <component class="nablarch.integration.micrometer.instrument.batch.BatchTransactionTimeMetricsLogger">
          <property name="meterRegistry" ref="meterRegistry" />
        </component>
      </list>
    </property>
  </component>

まず、 :java:extdoc:`CompositeCommitLogger <nablarch.core.log.app.CompositeCommitLogger>` を ``commitLogger`` という名前でコンポーネントとして定義する。
そして、 ``commitLoggerList`` プロパティに :java:extdoc:`BasicCommitLogger <nablarch.core.log.app.BasicCommitLogger>` と ``BatchTransactionTimeMetricsLogger`` のコンポーネントを設定する。

以上の設定により、トランザクション単位の時間計測が可能となる。
以下で、その仕組みを説明する。

Nablarchバッチは、 :ref:`loop_handler` によってトランザクションのコミット間隔を制御している。
このトランザクションループ制御ハンドラは、トランザクションがコミットされるときに :java:extdoc:`CommitLogger <nablarch.core.log.app.CommitLogger>` の ``increment(long)`` メソッドをコールする仕組みを提供している。
この ``CommitLogger`` の実体は、 ``commitLogger`` という名前でコンポーネントを定義することで上書きできる。

``BatchTransactionTimeMetricsLogger`` は ``CommitLogger`` インタフェースを実装している。
そして、 ``increment(long)`` の呼び出し間隔を計測することでトランザクション単位の時間を計測している。
このため、 ``BatchTransactionTimeMetricsLogger`` を ``commitLogger`` という名前でコンポーネント定義すると、トランザクション単位の時間計測ができる仕組みとなっている。

しかし、 ``BatchTransactionTimeMetricsLogger`` をそのまま ``commitLogger`` という名前で定義した場合、デフォルトで定義されている ``CommitLogger`` のコンポーネントである ``BasicCommitLogger`` が動作しなくなる。
そこで上記設定例では、複数の ``CommitLogger`` を組み合わせることができる ``CompositeCommitLogger`` を使用して、 ``BasicCommitLogger`` と ``BatchTransactionTimeMetricsLogger`` を併用するようにしている。

``LoggingMeterRegistry`` を使用している場合、 ``BatchTransactionTimeMetricsLogger`` の計測結果は以下のように出力される。

.. code-block:: text

  12 17, 2020 1:50:33 午後 io.micrometer.core.instrument.logging.LoggingMeterRegistry lambda$publish$5
  情報: batch.transaction.time{class=MetricsTestAction} throughput=1/s mean=2.61463556s max=3.0790852s

.. _micrometer_batch_processed_count:

バッチの処理件数を計測する
--------------------------------------------------

:java:extdoc:`BatchProcessedRecordCountMetricsLogger <nablarch.integration.micrometer.instrument.batch.BatchProcessedRecordCountMetricsLogger>` を使用すると、 :ref:`nablarch_batch` が処理した入力データの件数を計測できるようになる。
これにより、バッチの進捗状況や処理速度の変化をモニタできるようになる。

``BatchProcessedRecordCountMetricsLogger`` は `Counter(外部サイト、英語)`_ を使って ``batch.processed.record.count`` という名前でメトリクスを収集する。
この名前は、 :java:extdoc:`setMetricsName(String) <nablarch.integration.micrometer.instrument.batch.BatchProcessedRecordCountMetricsLogger.setMetricsName(java.lang.String)>` で変更できる。

また、メトリクスには以下のタグが付与される。

.. list-table::

  * - タグ名
    - 説明
  * - ``class``
    - アクションのクラス名（ :ref:`-requestPath <nablarch_batch-resolve_action>` から取得した値）

以下に ``BatchProcessedRecordCountMetricsLogger`` を使うための設定例を示す。

.. code-block:: xml

  <!-- CommitLogger を複数組み合わせる -->
  <component name="commitLogger"
             class="nablarch.core.log.app.CompositeCommitLogger">
    <property name="commitLoggerList">
      <list>
        <!-- デフォルトの CommitLogger を設定 -->
        <component class="nablarch.core.log.app.BasicCommitLogger">
          <property name="interval" value="${nablarch.commitLogger.interval}" />
        </component>

        <!-- 処理件数を計測する -->
        <component class="nablarch.integration.micrometer.instrument.batch.BatchProcessedRecordCountMetricsLogger">
          <property name="meterRegistry" ref="meterRegistry" />
        </component>
      </list>
    </property>
  </component>

``BatchProcessedRecordCountMetricsLogger`` は、「バッチのトランザクション単位の処理時間の計測」と同じく、 :java:extdoc:`CommitLogger <nablarch.core.log.app.CommitLogger>` の仕組みを利用して処理件数を計測している。
``CommitLogger`` の仕組みや、その利用の仕方については :ref:`micrometer_adaptor_batch_transaction_time` を参照のこと。

以上の設定で、 ``BatchProcessedRecordCountMetricsLogger`` を使用できるようになる。

``LoggingMeterRegistry`` を使用している場合、以下のようにメトリクスが出力されることを確認できる。

.. code-block:: text

  12 23, 2020 3:23:24 午後 io.micrometer.core.instrument.logging.LoggingMeterRegistry lambda$publish$4
  情報: batch.processed.record.count{class=MetricsTestAction} throughput=10/s
  12 23, 2020 3:23:34 午後 io.micrometer.core.instrument.logging.LoggingMeterRegistry lambda$publish$4
  情報: batch.processed.record.count{class=MetricsTestAction} throughput=13/s
  12 23, 2020 3:23:39 午後 io.micrometer.core.instrument.logging.LoggingMeterRegistry lambda$publish$4
  情報: batch.processed.record.count{class=MetricsTestAction} throughput=13/s

.. _micrometer_log_count:

ログレベルごとの出力回数を計測する
--------------------------------------------------

:java:extdoc:`LogCountMetrics <nablarch.integration.micrometer.instrument.binder.logging.LogCountMetrics>` を使用すると、ログレベルごとの出力回数を計測できるようになる。
これにより、特定レベルのログ出力頻度をモニタしたり、エラーログの監視などができるようになる。

``LogCountMetrics`` は `Counter(外部サイト、英語)`_ を使って ``log.count`` という名前でメトリクスを収集する。
この名前は、 :java:extdoc:`MetricsMetaData <nablarch.integration.micrometer.instrument.binder.MetricsMetaData>` を受け取る :java:extdoc:`コンストラクタ <nablarch.integration.micrometer.instrument.binder.logging.LogCountMetrics.LogCountMetrics(nablarch.integration.micrometer.instrument.binder.MetricsMetaData)>` で変更できる。

また、メトリクスには以下のタグが付与される。

.. list-table::

  * - タグ名
    - 説明
  * - ``level``
    - ログレベル。
  * - ``logger``
    - :java:extdoc:`LoggerManager <nablarch.core.log.LoggerManager>` からロガーを取得するときに使用した名前。

LogPublisher を設定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``LogCountMetrics`` は、ログ出力イベントを検知するために :java:extdoc:`LogPublisher <nablarch.core.log.basic.LogPublisher>` の仕組みを使用している。

したがって ``LogCountMetrics`` を使い始めるためには、まず ``LogPublisher`` の設定をする必要がある。
``LogPublisher`` の設定については、 :ref:`log-publisher_usage` を参照のこと。

カスタムのDefaultMeterBinderListProviderを作成する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``LogCountMetrics`` は `MeterBinder(外部サイト、英語)`_ の実装クラスとして提供されている。
したがって、 :java:extdoc:`DefaultMeterBinderListProvider <nablarch.integration.micrometer.DefaultMeterBinderListProvider>` を継承したクラスを作り、 ``LogCountMetrics`` を含んだ ``MeterBinder`` のリストを返すように実装する必要がある。

.. tip::

  ``DefaultMeterBinderListProvider`` の説明については、 :ref:`micrometer_adaptor_declare_default_meter_binder_list_provider_as_component` を参照。

以下に、その実装例を示す。

.. code-block:: java

  package example.micrometer.log;

  import io.micrometer.core.instrument.binder.MeterBinder;
  import nablarch.integration.micrometer.DefaultMeterBinderListProvider;
  import nablarch.integration.micrometer.instrument.binder.logging.LogCountMetrics;

  import java.util.ArrayList;
  import java.util.List;

  public class CustomMeterBinderListProvider extends DefaultMeterBinderListProvider {

      @Override
      protected List<MeterBinder> createMeterBinderList() {
          // デフォルトの MeterBinder リストに LogCountMetrics を追加
          List<MeterBinder> meterBinderList = new ArrayList<>(super.createMeterBinderList());
          meterBinderList.add(new LogCountMetrics());
          return meterBinderList;
      }
  }

最後に、 ``MeterRegistryFactory`` コンポーネントの ``meterBinderListProvider`` プロパティに、作成したカスタムの ``DefaultMeterBinderListProvider`` を設定する。
以上で、 ``LogCountMetrics`` が使用できるようになる。

``LoggingMeterRegistry`` を使用した場合、以下のようにメトリクスが出力されることが確認できる。

.. code-block:: text

  2020-12-22 14:25:36.978 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: log.count{level=WARN,logger=com.nablarch.example.app.web.action.MetricsAction} throughput=0.4/s
  2020-12-22 14:25:41.978 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: log.count{level=ERROR,logger=com.nablarch.example.app.web.action.MetricsAction} throughput=1.4/s

集計対象のログレベル
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

デフォルトでは、 ``WARN`` 以上のログ出力回数のみが集計の対象となる。

集計対象のログレベルのしきい値は、 ``LogCountMetrics`` のコンストラクタに :java:extdoc:`LogLevel <nablarch.core.log.basic.LogLevel>` を渡すことで変更できる。
以下の実装例では、しきい値を ``INFO`` に変更している。

.. code-block:: java

  // （省略）
  import nablarch.core.log.basic.LogLevel;

  public class CustomMeterBinderListProvider extends DefaultMeterBinderListProvider {

      @Override
      protected List<MeterBinder> createMeterBinderList() {
          List<MeterBinder> meterBinderList = new ArrayList<>(super.createMeterBinderList());
          meterBinderList.add(new LogCountMetrics(LogLevel.INFO)); // LogLevel のしきい値を指定
          return meterBinderList;
      }
  }

.. important::

  ログレベルのしきい値を下げすぎると、アプリケーションによっては大量のメトリクスが収集される可能性がある。
  使用する監視サービスの料金体系によっては使用料金が増大する可能性があるため、注意して設定すること。

.. _micrometer_sql_time:

SQLの処理時間を計測する
--------------------------------------------------

:java:extdoc:`SqlTimeMetricsDaoContext <nablarch.integration.micrometer.instrument.dao.SqlTimeMetricsDaoContext>` を使用することで、 :ref:`universal_dao` を通じて実行したSQLの処理時間を計測できるようになる。
これにより、SQLごとの平均処理時間や最大処理時間をモニタできるようになる。

``SqlTimeMetricsDaoContext`` は `Timer(外部サイト、英語)`_ を使って ``sql.process.time`` という名前でメトリクスを収集する。
この名前は、 ``SqlTimeMetricsDaoContext`` のファクトリクラスである :java:extdoc:`SqlTimeMetricsDaoContextFactory <nablarch.integration.micrometer.instrument.dao.SqlTimeMetricsDaoContextFactory>` の :java:extdoc:`setMetricsName(String) <nablarch.integration.micrometer.instrument.dao.SqlTimeMetricsDaoContextFactory.setMetricsName(java.lang.String)>` で変更できる。

また、メトリクスには以下のタグが付与される。

.. list-table::

  * - タグ名
    - 説明
  * - ``sql.id``
    - ``DaoContext`` のメソッド引数に渡されたSQLID（SQLIDが無い場合は ``"None"``）
  * - ``entity``
    - エンティティクラスの名前（``Class.getName()``）
  * - ``method``
    - 実行された ``DaoContext`` のメソッド名

以下に ``SqlTimeMetricsDaoContext`` を使うための設定例を示す。

.. code-block:: xml

  <!-- SqlTimeMetricsDaoContextFactory を daoContextFactory という名前で定義 -->
  <component name="daoContextFactory"
             class="nablarch.integration.micrometer.instrument.dao.SqlTimeMetricsDaoContextFactory">
    <!-- delegate に、委譲先となる DaoContext のファクトリを設定する -->
    <property name="delegate">
      <component class="nablarch.common.dao.BasicDaoContextFactory">
        <property name="sequenceIdGenerator">
          <component class="nablarch.common.idgenerator.SequenceIdGenerator" />
        </property>
      </component>
    </property>

    <!-- レジストリファクトリが生成する MeterRegistry を meterRegistry プロパティに設定する -->
    <property name="meterRegistry" ref="meterRegistry" />
  </component>

``SqlTimeMetricsDaoContext`` は、 :java:extdoc:`DaoContext <nablarch.common.dao.DaoContext>` をラップすることで各データベースアクセスメソッドの処理時間を計測する仕組みになっている。
そして、 :java:extdoc:`SqlTimeMetricsDaoContextFactory <nablarch.integration.micrometer.instrument.dao.SqlTimeMetricsDaoContextFactory>` は、 ``DaoContext`` をラップした ``SqlTimeMetricsDaoContext`` を生成するファクトリクラスとなる。

この ``SqlTimeMetricsDaoContextFactory`` を ``daoContextFactory`` という名前でコンポーネントとして定義する。
これにより、 :ref:`universal_dao` が使用する ``DaoContext`` が ``SqlTimeMetricsDaoContext`` に置き換わる。

以上で、 ``SqlTimeMetricsDaoContext`` が使用できるようになる。

``LoggingMeterRegistry`` を使用した場合、以下のようにメトリクスが出力されることが確認できる。

.. code-block:: text

  2020-12-23 15:00:25.161 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: sql.process.time{entity=com.nablarch.example.app.entity.Project,method=delete,sql.id=None} throughput=0.2/s mean=0.0005717s max=0.0005717s
  2020-12-23 15:00:25.161 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: sql.process.time{entity=com.nablarch.example.app.entity.Project,method=findAllBySqlFile,sql.id=SEARCH_PROJECT} throughput=0.6/s mean=0.003364233s max=0.0043483s
  2020-12-23 15:00:25.161 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: sql.process.time{entity=com.nablarch.example.app.web.dto.ProjectDto,method=findBySqlFile,sql.id=FIND_BY_PROJECT} throughput=0.2/s mean=0.000475s max=0.0060838s
  2020-12-23 15:00:25.162 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: sql.process.time{entity=com.nablarch.example.app.entity.Industry,method=findAll,sql.id=None} throughput=0.8/s mean=0.00058155s max=0.0013081s

.. _micrometer_mbean_metrics:

任意のMBeanから取得した値をメトリクスとして計測する
-------------------------------------------------------------

:java:extdoc:`JmxGaugeMetrics <nablarch.integration.micrometer.instrument.binder.jmx.JmxGaugeMetrics>` を使用すると、任意のMBeanから取得した値をメトリクスとして計測できるようになる。
これにより、使用しているアプリケーションサーバやライブラリがMBeanで提供している様々な情報を計測し、モニタできるようになる。

.. tip::

  MBeanとは、Java Management Extensions(JMX)で定義されたJavaオブジェクトで、管理対象リソースの情報へアクセスするためのAPIなどを提供する。
  Tomcatなどのアプリケーションサーバの多くは、サーバの状態（スレッドプールの状態など）をMBeanで公開している。
  アプリケーションからこれらのMBeanにアクセスすることで、サーバの状態を取得できるようになっている。

  JMXについての詳細は、 `Java Management Extensions Guide(外部サイト、英語) <https://docs.oracle.com/en/java/javase/11/jmx/java-management-extensions-jmx-user-guide.html>`_ を参照。

``JmxGaugeMetrics`` は、 `Gauge(外部サイト、英語)`_ を使用して、MBeanから取得した値を計測する。

以下で、 ``JmxGaugeMetrics`` の設定例を説明する。

まず、アプリケーションサーバが提供するMBeanを参照する例として、Tomcatのスレッドプールの状態を取得する例を示す。
次にアプリケーションに組み込んだライブラリが提供するMBeanを参照する例として、HikariCPのコネクションプールの状態を取得する例を示す。

Tomcatのスレッドプールの状態を取得する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``JmxGaugeMetrics`` は `MeterBinder(外部サイト、英語)`_ の実装クラスとして提供されている。
したがって、 :java:extdoc:`DefaultMeterBinderListProvider <nablarch.integration.micrometer.DefaultMeterBinderListProvider>` を継承したクラスを作り、 ``JmxGaugeMetrics`` を含んだ ``MeterBinder`` のリストを返すように実装する必要がある。

.. tip::

  ``DefaultMeterBinderListProvider`` の説明については、 :ref:`micrometer_adaptor_declare_default_meter_binder_list_provider_as_component` を参照。

以下に、実装例を示す。

.. code-block:: java

  package example.micrometer;

  import io.micrometer.core.instrument.binder.MeterBinder;
  import nablarch.integration.micrometer.DefaultMeterBinderListProvider;
  import nablarch.integration.micrometer.instrument.binder.MetricsMetaData;
  import nablarch.integration.micrometer.instrument.binder.jmx.JmxGaugeMetrics;
  import nablarch.integration.micrometer.instrument.binder.jmx.MBeanAttributeCondition;

  import java.util.ArrayList;
  import java.util.List;

  public class CustomMeterBinderListProvider extends DefaultMeterBinderListProvider {

      @Override
      protected List<MeterBinder> createMeterBinderList() {
          List<MeterBinder> meterBinderList = new ArrayList<>(super.createMeterBinderList());
          meterBinderList.add(new JmxGaugeMetrics(
              // メトリクスの名前と説明
              new MetricsMetaData("thread.count.current", "Current thread count."),
              // 収集する MBean の属性を特定する情報
              new MBeanAttributeCondition("Catalina:type=ThreadPool,name=\"http-nio-8080\"", "currentThreadCount")
          ));
          return meterBinderList;
      }
  }

``JmxGaugeMetrics`` のコンストラクタには、次の２つのクラスを渡す必要がある。

* :java:extdoc:`MetricsMetaData <nablarch.integration.micrometer.instrument.binder.MetricsMetaData>`
    * メトリクスの名前や説明、タグなどのメタ情報を指定する
* :java:extdoc:`MBeanAttributeCondition <nablarch.integration.micrometer.instrument.binder.jmx.MBeanAttributeCondition>`
    * 収集するMbeanを特定するための、オブジェクト名と属性名を指定する

``JmxGaugeMetrics`` は、 ``MBeanAttributeCondition`` で指定された情報に基づいてMBeanの情報を取得する。
そして、 ``MetricsMetaData`` で指定された情報でメトリクスを構築する。

.. tip::

  Tomcatが作成するMBeanのオブジェクト名・属性名は、JDKに付属しているJConsoleというツールを使って確認できる。
  JConsoleでTomcatを実行しているJVMに接続し「MBeans」タブを開くと、接続しているJVMで取得可能なMBeanの一覧が表示される。

  JConsoleについての詳細は、 `Monitoring and Management Guide(外部サイト、英語) <https://docs.oracle.com/en/java/javase/15/management/using-jconsole.html#GUID-77416B38-7F15-4E35-B3D1-34BFD88350B5>`_ を参照。

以上の設定で ``LoggingMeterRegistry`` を使用した場合、以下のようにメトリクスが出力されることが確認できる。

.. code-block:: text

  24-Dec-2020 16:20:24.467 情報 [logging-metrics-publisher] io.micrometer.core.instrument.logging.LoggingMeterRegistry.lambda$publish$3 thread.count.current{} value=10

HikariCPのコネクションプールの状態を取得する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`HikariCP(外部サイト、英語) <https://github.com/brettwooldridge/HikariCP>`_ には、コネクションプールの情報をMBeanで参照できるようにする機能が用意されている。

* `MBean (JMX) Monitoring and Management(外部サイト、英語) <https://github.com/brettwooldridge/HikariCP/wiki/MBean-(JMX)-Monitoring-and-Management>`_

この機能を使用することで、 ``JmxGaugeMetrics`` でコネクションプールの情報を収集できるようになる。

まず、HikariCPのMBeanで情報を公開する機能を有効にする。
MBeanによる情報公開を有効にするには、 ``com.zaxxer.hikari.HikariDataSource`` の ``registerMbeans`` プロパティに ``true`` を設定する。

.. code-block:: xml

  <?xml version="1.0" encoding="UTF-8"?>
  <component-configuration
          xmlns="http://tis.co.jp/nablarch/component-configuration"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://tis.co.jp/nablarch/component-configuration https://nablarch.github.io/schema/component-configuration.xsd">
    <!-- 省略 -->

    <!-- データソース設定 -->
    <component name="dataSource"
              class="com.zaxxer.hikari.HikariDataSource" autowireType="None">
      <property name="driverClassName" value="${nablarch.db.jdbcDriver}"/>
      <property name="jdbcUrl"         value="${nablarch.db.url}"/>
      <property name="username"        value="${nablarch.db.user}"/>
      <property name="password"        value="${nablarch.db.password}"/>
      <property name="maximumPoolSize" value="${nablarch.db.maxPoolSize}"/>
      <!-- MBeanによる情報公開を有効にする -->
      <property name="registerMbeans"  value="true"/>
    </component>

  </component-configuration>

上記設定では、 ``HikariDataSource`` のコンポーネント定義で ``registerMbeans`` プロパティに ``true`` を設定している。

次に、HikariCPが公開するMBeanのオブジェクト名と、計測したい属性名を指定した形で ``JmxGaugeMetrics`` を設定する。
なお、オブジェクト名や属性名の仕様は、 `前述のHikariCPのドキュメント(外部サイト、英語) <https://github.com/brettwooldridge/HikariCP/wiki/MBean-(JMX)-Monitoring-and-Management#programmatic-access>`_ に記載されている。

以下は、コネクションプールの最大数とアクティブ数を計測する場合の ``JmxGaugeMetrics`` の実装例になる。

.. code-block:: java

  package com.nablarch.example.app.metrics;

  import io.micrometer.core.instrument.binder.MeterBinder;
  import nablarch.integration.micrometer.DefaultMeterBinderListProvider;
  import nablarch.integration.micrometer.instrument.binder.MetricsMetaData;
  import nablarch.integration.micrometer.instrument.binder.jmx.JmxGaugeMetrics;
  import nablarch.integration.micrometer.instrument.binder.jmx.MBeanAttributeCondition;

  import java.util.ArrayList;
  import java.util.List;

  public class CustomMeterBinderListProvider extends DefaultMeterBinderListProvider {

      @Override
      protected List<MeterBinder> createMeterBinderList() {
          List<MeterBinder> meterBinderList = new ArrayList<>(super.createMeterBinderList());
          // 最大数
          meterBinderList.add(new JmxGaugeMetrics(
              new MetricsMetaData("db.pool.total", "Total DB pool count."),
              new MBeanAttributeCondition("com.zaxxer.hikari:type=Pool (HikariPool-1)", "TotalConnections")
          ));
          // アクティブ数
          meterBinderList.add(new JmxGaugeMetrics(
              new MetricsMetaData("db.pool.active", "Active DB pool count."),
              new MBeanAttributeCondition("com.zaxxer.hikari:type=Pool (HikariPool-1)", "ActiveConnections")
          ));
          return meterBinderList;
      }
  }

以上の設定で ``LoggingMeterRegistry`` を使用した場合、以下のようにメトリクスが出力されることが確認できる。

.. code-block:: text

  2020-12-24 16:37:57.143 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: db.pool.active{} value=0
  2020-12-24 16:37:57.143 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: db.pool.total{} value=5

サーバ起動時に出力される警告ログについて
*********************************************************************

Micrometerが監視サービスにメトリクスを連携する方法には、大きく次の２つの方法が存在する。

* 一定間隔でアプリケーションが監視サービスにメトリクスを送信する (Client pushes)
    * Datadog, CloudWatch など
* 一定間隔で監視サービスがアプリケーションにメトリクスを問い合わせに来る (Server polls)
    * Prometheus など

前者(Client pushes)の場合、 ``MeterRegistry`` はコンポーネント生成後に一定間隔でメトリクスの送信を開始する。
一方で、HikariCPのコネクションプールは、一番最初にデータベースアクセスが行われたときに初めて作成される仕様となっている。

このため、最初のデータベースアクセスが発生する前にメトリクスの送信が実行されると、 ``JmxGaugeMetrics`` は存在しないコネクションプールの情報を参照することになる。
このとき、Micrometerは以下のような警告ログを出力する。

.. code-block:: text

  24-Dec-2020 16:57:16.729 警告 [logging-metrics-publisher] io.micrometer.core.util.internal.logging.WarnThenDebugLogger.log Failed to apply the value function for the gauge 'db.pool.active'. Note that subsequent logs will be logged at debug level.
          java.lang.RuntimeException: javax.management.InstanceNotFoundException: com.zaxxer.hikari:type=Pool (HikariPool-1)
                  at nablarch.integration.micrometer.instrument.binder.jmx.JmxGaugeMetrics.obtainGaugeValue(JmxGaugeMetrics.java:59)
                  at io.micrometer.core.instrument.Gauge.lambda$builder$0(Gauge.java:58)
                  at io.micrometer.core.instrument.StrongReferenceGaugeFunction.applyAsDouble(StrongReferenceGaugeFunction.java:47)
                  at io.micrometer.core.instrument.internal.DefaultGauge.value(DefaultGauge.java:54)
                  at io.micrometer.core.instrument.logging.LoggingMeterRegistry.lambda$publish$3(LoggingMeterRegistry.java:98)
                  at io.micrometer.core.instrument.Meter.use(Meter.java:158)
                  at io.micrometer.core.instrument.logging.LoggingMeterRegistry.lambda$publish$12(LoggingMeterRegistry.java:97)
                  at java.util.stream.ForEachOps$ForEachOp$OfRef.accept(ForEachOps.java:183)
                  at java.util.stream.SortedOps$SizedRefSortingSink.end(SortedOps.java:357)
                  at java.util.stream.AbstractPipeline.copyInto(AbstractPipeline.java:483)
                  at java.util.stream.AbstractPipeline.wrapAndCopyInto(AbstractPipeline.java:472)
                  at java.util.stream.ForEachOps$ForEachOp.evaluateSequential(ForEachOps.java:150)
                  at java.util.stream.ForEachOps$ForEachOp$OfRef.evaluateSequential(ForEachOps.java:173)
                  at java.util.stream.AbstractPipeline.evaluate(AbstractPipeline.java:234)
                  at java.util.stream.ReferencePipeline.forEach(ReferencePipeline.java:485)
                  at io.micrometer.core.instrument.logging.LoggingMeterRegistry.publish(LoggingMeterRegistry.java:95)
                  at io.micrometer.core.instrument.push.PushMeterRegistry.publishSafely(PushMeterRegistry.java:52)
                  at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
                  at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308)
                  at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180)
                  at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294)
                  at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
                  at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
                  at java.lang.Thread.run(Thread.java:748)
          Caused by: javax.management.InstanceNotFoundException: com.zaxxer.hikari:type=Pool (HikariPool-1)
                  at com.sun.jmx.interceptor.DefaultMBeanServerInterceptor.getMBean(DefaultMBeanServerInterceptor.java:1095)
                  at com.sun.jmx.interceptor.DefaultMBeanServerInterceptor.getAttribute(DefaultMBeanServerInterceptor.java:643)
                  at com.sun.jmx.mbeanserver.JmxMBeanServer.getAttribute(JmxMBeanServer.java:678)
                  at nablarch.integration.micrometer.instrument.binder.jmx.JmxGaugeMetrics.obtainGaugeValue(JmxGaugeMetrics.java:52)
                  ... 23 more

なお、コネクションプールが生成されていない間、メトリクスの値は ``NaN`` となる。

.. code-block:: text

  24-Dec-2020 17:01:31.443 情報 [logging-metrics-publisher] io.micrometer.core.instrument.logging.LoggingMeterRegistry.lambda$publish$3 db.pool.active{} value=NaN
  24-Dec-2020 17:01:31.443 情報 [logging-metrics-publisher] io.micrometer.core.instrument.logging.LoggingMeterRegistry.lambda$publish$3 db.pool.total{} value=NaN

この警告ログは最初の一度だけ出力され、2回目以降は抑制されるようになっている。
また、データベースアクセスが実行されコネクションプールが生成されると、そのあとは正常にコネクションプールの値が収集されるようになる。

つまり、この警告ログはアプリケーションが正常な場合であってもタイミング次第で出力される可能性があるということになる。
しかし、実害は無いので無視しても問題はない。

ただし、どうしても警告ログを抑制したい場合は、以下のように実装することである程度回避できるようになる。

.. code-block:: java

  package example.micrometer;

  // 省略
  import nablarch.core.log.Logger;
  import nablarch.core.log.LoggerManager;
  import nablarch.core.repository.initialization.Initializable;
  import java.sql.SQLException;
  import javax.sql.DataSource;
  import java.sql.Connection;

  public class CustomMeterBinderListProvider extends DefaultMeterBinderListProvider implements Initializable {
      private static final Logger LOGGER = LoggerManager.get(CustomMeterBinderListProvider.class);

      private DataSource dataSource;

      @Override
      protected List<MeterBinder> createMeterBinderList() {
          // 省略
      }

      public void setDataSource(DataSource dataSource) {
          this.dataSource = dataSource;
      }

      @Override
      public void initialize() {
          try (Connection con = dataSource.getConnection()) {
              // 初期化時にコネクションを確立することで、MBeanが取れないことによる警告ログの出力を抑制する
          } catch (SQLException e) {
              LOGGER.logWarn("Failed initial connection.", e);
          }
      }
  }

カスタムの ``DefaultMeterBinderListProvider`` で :java:extdoc:`Initializable <nablarch.core.repository.initialization.Initializable>` を実装する。
また、 ``java.sql.DataSource`` をプロパティとして受け取れるように実装を修正する。
そして、 ``initialize()`` メソッドの中でデータベースに接続するように実装する。

コンポーネント定義では、 ``DataSource`` をプロパティで渡すように変更する。
そして、初期化対象のコンポーネント一覧に、このクラスを追加する。

.. code-block:: xml

  <component name="meterBinderListProvider"
             class="example.micrometer.CustomMeterBinderListProvider">
    <!-- DataSource を設定する -->
    <property name="dataSource" ref="dataSource" />
  </component>

  <!-- 初期化が必要なコンポーネント -->
  <component name="initializer"
             class="nablarch.core.repository.initialization.BasicApplicationInitializer">
    <property name="initializeList">
      <list>
        <!-- 省略 -->

        <!-- 初期化対象のコンポーネントとして追加 -->
        <component-ref name="meterBinderListProvider" />
      </list>
    </property>
  </component>

以上の修正により、システムリポジトリが初期化されたときにデータベース接続が行われるようになる。
メトリクスの送信間隔はデフォルトで１分なので、たいていの場合メトリクス送信よりも前にコネクションプールが作成されるようになる。
これにより、警告ログは出力されなくなる。

ただし、メトリクスの送信間隔を非常に短い時間に設定している場合、システムリポジトリが初期化される前にメトリクスが送信されて警告ログが出力される可能性がある点に注意すること。



.. _MeterBinder(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/binder/MeterBinder.html
.. _Counter(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/Counter.html
.. _Gauge(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/Gauge.html
.. _DatadogConfig(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-registry-datadog/1.13.0/io/micrometer/datadog/DatadogConfig.html
.. _CloudWatchConfig(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-registry-cloudwatch2/1.13.0/io/micrometer/cloudwatch2/CloudWatchConfig.html
.. _StatsdConfig(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-registry-statsd/1.13.0/io/micrometer/statsd/StatsdConfig.html
.. _OtlpConfig(外部サイト、英語): https://javadoc.io/static/io.micrometer/micrometer-registry-otlp/1.13.0/io/micrometer/registry/otlp/OtlpConfig.html
.. _MeterRegistry(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/MeterRegistry.html
.. _DatadogMeterRegistry(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-registry-datadog/1.13.0/io/micrometer/datadog/DatadogMeterRegistry.html
.. _StatsdMeterRegistry(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-registry-statsd/1.13.0/io/micrometer/statsd/StatsdMeterRegistry.html
.. _OtlpMeterRegistry(外部サイト、英語): https://javadoc.io/static/io.micrometer/micrometer-registry-otlp/1.13.0/io/micrometer/registry/otlp/OtlpMeterRegistry.html
.. _DatadogMeterRegistry(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-registry-datadog/1.13.0/io/micrometer/datadog/DatadogMeterRegistry.html
.. _CloudWatchMeterRegistry(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-registry-cloudwatch2/1.13.0/io/micrometer/cloudwatch2/CloudWatchMeterRegistry.html
.. _LoggingMeterRegistry(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/logging/LoggingMeterRegistry.html
.. _SimpleMeterRegistry(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/simple/SimpleMeterRegistry.html
.. _JvmMemoryMetrics(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/binder/jvm/JvmMemoryMetrics.html
.. _ProcessorMetrics(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/binder/system/ProcessorMetrics.html
.. _JvmGcMetrics(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/binder/jvm/JvmGcMetrics.html
.. _JvmThreadMetrics(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/binder/jvm/JvmThreadMetrics.html
.. _ClassLoaderMetrics(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/binder/jvm/ClassLoaderMetrics.html
.. _FileDescriptorMetrics(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/binder/system/FileDescriptorMetrics.html
.. _UptimeMetrics(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/binder/system/UptimeMetrics.html
.. _Timer(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-core/1.13.0/io/micrometer/core/instrument/Timer.html
.. _PrometheusMeterRegistry(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-registry-prometheus/1.13.0/io/micrometer/prometheusmetrics/PrometheusMeterRegistry.html
