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

  Micrometerのバージョン1.5.4を使用してテストを行っている。
  バージョンを変更する場合は、プロジェクト側でテストを行い問題ないことを確認すること。

Micrometerアダプタを使用するための設定を行う
--------------------------------------------------
| Micrometerでメトリクスを収集するためには、 `レジストリ(外部サイト、英語) <https://micrometer.io/docs/concepts#_registry>`_ と呼ばれるクラスを作成する必要がある。
| 本アダプタでは、このレジストリを :ref:`repository` に登録するための :java:extdoc:`ComponentFactory<nablarch.core.repository.di.ComponentFactory>` を提供している。

ここでは、 `LoggingMeterRegistry(外部サイト、英語)`_ をコンポーネントとして登録する :java:extdoc:`LoggingMeterRegistryFactory<nablarch.integration.micrometer.logging.LoggingMeterRegistryFactory>` を例にして設定方法について説明する。

なお、ベースとなるアプリケーションには `ウェブアプリケーションのExample(外部サイト) <https://github.com/nablarch/nablarch-example-web>`_ を使用する。

DefaultMeterBinderListProviderをコンポーネントとして宣言する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| Micrometerには、 `MeterBinder(外部サイト、英語)`_ というインタフェースが存在する。
| JVMのメモリ使用量やCPU使用率など、よく利用するメトリクスの収集は、このインタフェースを実装したクラスとしてあらかじめ用意されている。
| （例：JVMのメモリ使用量は `JvmMemoryMetrics(外部サイト、英語)`_ 、CPU使用率は `ProcessorMetrics(外部サイト、英語)`_ ）

:java:extdoc:`DefaultMeterBinderListProvider <nablarch.integration.micrometer.DefaultMeterBinderListProvider>` は、この `MeterBinder(外部サイト、英語)`_ のリストを提供するクラスで、本クラスを使用することでJVMのメモリ使用量やCPU使用率などのメトリクスを収集できるようになる。

まず ``src/main/resources/web-component-configuration.xml`` に、この :java:extdoc:`DefaultMeterBinderListProvider <nablarch.integration.micrometer.DefaultMeterBinderListProvider>` の宣言を追加する。

.. code-block:: xml

  <component name="meterBinderListProvider"
             class="nablarch.integration.micrometer.DefaultMeterBinderListProvider" />


収集されるメトリクスの具体的な説明については、 :ref:`micrometer_default_metrics` を参照。

DefaultMeterBinderListProviderを廃棄処理対象にする
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| :java:extdoc:`DefaultMeterBinderListProvider <nablarch.integration.micrometer.DefaultMeterBinderListProvider>` は廃棄処理が必要なコンポーネントなので、下記のように廃棄処理対象として宣言する。

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

| このとき、 ``meterBinderListProvider`` と ``applicationDisposer`` の２つのプロパティを設定する。
| それぞれのプロパティには、上で宣言した :java:extdoc:`DefaultMeterBinderListProvider <nablarch.integration.micrometer.DefaultMeterBinderListProvider>` と :java:extdoc:`BasicApplicationDisposer <nablarch.core.repository.disposal.BasicApplicationDisposer>` を設定する。

なお、本アダプタが提供しているファクトリクラスについては :ref:`micrometer_registry_factory` に一覧を記載している。


設定ファイルを作成する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

最後に、 ``src/main/resources`` の下に ``micrometer.properties`` という名前のテキストファイルを作成する。

ここでは、中身を次のように記述する。

.. code-block:: properties

  # 5秒ごとにメトリクスを出力する
  nablarch.micrometer.logging.step=5s

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

  nablarch.micrometer.<subPrefix>.<key>

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
=================================== ================

また、 ``<key>`` には Micrometer がレジストリごとに提供している `設定クラス(外部サイト、英語) <https://javadoc.io/doc/io.micrometer/micrometer-core/1.5.4/io/micrometer/core/instrument/config/MeterRegistryConfig.html>`_ で定義されたメソッドと同じ名前を指定する。

| 例えば、 `DatadogMeterRegistry(外部サイト、英語)`_ に対しては `DatadogConfig(外部サイト、英語)`_ という設定クラスが用意されている。
| そして、この設定クラスには `apyKey(外部サイト、英語) <https://javadoc.io/doc/io.micrometer/micrometer-registry-datadog/1.5.4/io/micrometer/datadog/DatadogConfig.html#apiKey()>`_ というメソッドが定義されている。




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

    $ export NABLARCH_MICROMETER_EXAMPLE_ONE=OS_ENV

    $ export NABLARCH_MICROMETER_EXAMPLE_TWO=OS_ENV

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

設定のプレフィックス (``nablarch.micrometer.<subPrefix>``) は、各レジストリファクトリごとに :java:extdoc:`prefix <nablarch.integration.micrometer.MeterRegistryFactory.setPrefix(String)>` プロパティを指定することで変更できる。

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

まず、レジストリファクトリの :java:extdoc:`xmlConfigPath <nablarch.integration.micrometer.MeterRegistryFactory.xmlConfigPath(String)>` プロパティに、設定ファイルを読み込むXMLファイルのパスを指定する。

.. code-block:: xml

  <component name="meterRegistry" class="nablarch.integration.micrometer.logging.LoggingMeterRegistryFactory">
    <property name="meterBinderListProvider" ref="meterBinderListProvider" />
    <property name="applicationDisposer" ref="disposer" />

    <!-- 設定ファイルを読み込むXMLファイルのパスを指定 -->
    <property name="xmlConfigPath" value="config/metrics.xml" />
  </component>

| そして、 ``xmlConfigPath`` プロパティで指定した場所に、設定ファイルを読み込むXMLファイルを配置する。
| 下記設定では、クラスパス内の ``config/metrics.properties`` が設定ファイルとして読み込まれるようになる。

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

  ただし、このファイルでコンポーネントを定義しても、システムリポジトリから参照を取得することはできない。


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
    - メモリープールのメモリー使用量
  * - ``jvm.memory.committed``
    - メモリープールのコミットされたメモリー量
  * - ``jvm.memory.max``
    - メモリープールの最大メモリー量
  * - ``jvm.gc.max.data.size``
    - OLD領域の最大メモリー量
  * - ``jvm.gc.live.data.size``
    - Full GC 後の OLD 領域のメモリー使用量
  * - ``jvm.gc.memory.promoted``
    - GC 前後で増加した、 OLD 領域のメモリー使用量の増分
  * - ``jvm.gc.memory.allocated``
    - 前回の GC 後から今回の GC までの、 Young 領域のメモリー使用量の増分
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

実際に収集されるメトリクスのイメージは :ref:`micrometer_metrics_output_example` を参照。

共通のタグを設定する
--------------------------------------------------

レジストリファクトリの :java:extdoc:`tags <nablarch.integration.micrometer.MeterRegistryFactory.setTags(Map)>` プロパティで、すべてのメトリクスに共通するタグを設定できる。

この機能は、アプリケーションが稼働しているホスト、インスタンス、リージョンなどを識別できる情報を設定するといった用途として利用できる。

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

| ``tags`` プロパティの型は ``Map<String, String>`` となっており、 ``<map>`` タグを使って設定できる。
| このとき、マップのキーがタグの名前、マップの値がタグの値に対応付けられる。

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

監視サービスと連携するためには、大きく次の設定を行う必要がある。

#. 監視サービスごとに用意された Micrometer のモジュールを依存関係に追加する
#. 監視サービス用のレジストリファクトリをコンポーネントとして定義する
#. その他、監視サービスごとに独自の設定を行う

ここでは、それぞれの監視サービスと連携する方法について説明する。


Datadog と連携する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

依存関係を追加する
  .. code-block:: xml

    <dependency>
      <groupId>io.micrometer</groupId>
      <artifactId>micrometer-registry-datadog</artifactId>
      <version>1.5.4</version>
    </dependency>

レジストファクトリを宣言する
  .. code-block:: xml
  
    <component name="meterRegistry" class="nablarch.integration.micrometer.datadog.DatadogMeterRegistryFactory">
      <property name="meterBinderListProvider" ref="meterBinderListProvider" />
      <property name="applicationDisposer" ref="disposer" />
    </component>

APIキーを設定する
  .. code-block:: text

    nablarch.micrometer.datadog.apiKey=XXXXXXXXXXXXXXXX

  API キーは ``nablarch.micrometer.datadog.apyKey`` で設定できる。

  その他の設定については `DatadogConfig(外部サイト、英語)`_ を参照。


CloudWatch と連携する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

依存関係を追加する
  .. code-block:: xml

    <dependency>
      <groupId>io.micrometer</groupId>
      <artifactId>micrometer-registry-cloudwatch2</artifactId>
      <version>1.5.4</version>
    </dependency>

レジストファクトリを宣言する
  .. code-block:: xml
  
    <component name="meterRegistry" class="nablarch.integration.micrometer.statsd.StatsdMeterRegistryFactory">
      <property name="meterBinderListProvider" ref="meterBinderListProvider" />
      <property name="applicationDisposer" ref="disposer" />
    </component>

リージョンやアクセスキーを設定する
  .. code-block:: bash
    
    $ export AWS_REGION=ap-northeast-1

    $ export AWS_ACCESS_KEY_ID=XXXXXXXXXXXXXXXXXXXXX

    $ export AWS_SECRET_ACCESS_KEY=YYYYYYYYYYYYYYYYYYYYY

  | ``micrometer-registry-cloudwatch2`` モジュールは AWS SDK を利用している。
  | したがって、リージョンやアクセスキーなどの設定は AWS SDK の方法に準拠する。

  | 上記は、LinuxでOS環境変数を使って設定する場合の例を記載している。
  | より詳細な情報は、 `AWSのドキュメント(外部サイト) <https://docs.aws.amazon.com/ja_jp/sdk-for-java/v1/developer-guide/setup-credentials.html>`_ を参照。

名前空間を設定する
  .. code-block:: text

    nablarch.micrometer.cloudwatch.namespace=test

  メトリクスのカスタム名前空間は ``nablarch.micrometer.cloudwatch.namespace`` で設定できる。

  その他の設定については `CloudWatchConfig(外部サイト、英語)`_ を参照。

より詳細な設定
  OS環境変数や設定ファイルでは指定できない、より詳細な設定を行いたい場合は、 :java:extdoc:`CloudWatchAsyncClientProvider <nablarch.integration.micrometer.cloudwatch.CloudWatchAsyncClientProvider>` を実装したカスタムプロバイダを作ることで対応できる。

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

  | :java:extdoc:`CloudWatchAsyncClientProvider <nablarch.integration.micrometer.cloudwatch.CloudWatchAsyncClientProvider>` は ``CloudWatchAsyncClient`` を提供する ``provide()`` メソッドを持つ。
  | カスタムプロバイダでは、任意の設定を行った ``CloudWatchAsyncClient`` を構築して返すように ``provide()`` メソッドを実装する。

  .. code-block:: xml

    <component name="meterRegistry" class="nablarch.integration.micrometer.cloudwatch.CloudWatchMeterRegistryFactory">
      <property name="meterBinderListProvider" ref="meterBinderListProvider" />
      <property name="applicationDisposer" ref="disposer" />

      <!-- cloudWatchAsyncClientProvider プロパティにカスタムプロバイダを設定する -->
      <property name="cloudWatchAsyncClientProvider">
        <component class="example.micrometer.cloudwatch.CustomCloudWatchAsyncClientProvider" />
      </property>
    </component>

  作成したカスタムプロバイダは、 ``CloudWatchMeterRegistryFactory`` の :java:extdoc:`cloudWatchAsyncClientProvider <nablarch.integration.micrometer.cloudwatch.CloudWatchMeterRegistryFactory.setCloudWatchAsyncClientProvider(CloudWatchAsyncClientProvider)>` プロパティに設定する。

  これにより、カスタムプロバイダが生成した ``CloudWatchAsyncClient`` がメトリクスの連携で使用されるようになる。

  .. tip::

    デフォルトでは、 `CloudWatchAsyncClient.create() (外部サイト、英語) <https://javadoc.io/static/software.amazon.awssdk/cloudwatch/2.13.4/software/amazon/awssdk/services/cloudwatch/CloudWatchAsyncClient.html#create-->`_ で作成されたインスタンスが使用される。

StatsD で連携する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| Datadog は `DogStatsD(外部サイト) <https://docs.datadoghq.com/ja/developers/dogstatsd/?tab=hostagent>`_ という `StatsD(外部サイト、英語) <https://github.com/statsd/statsd>`_ プロトコルを使った連携をサポートしている。
| したがって、 ``micrometer-registry-statsd`` モジュールを用いることで、 StatsD で Datadog と連携することもできる。

| ここでは、 Datadog に StatsD プロトコルで連携する場合を例にして説明する。
| なお、DogStatsD のインストール方法などについては `Datadogのサイト(外部サイト) <https://docs.datadoghq.com/ja/agent/>`_ を参照。

依存関係を追加する
  .. code-block:: xml

    <dependency>
      <groupId>io.micrometer</groupId>
      <artifactId>micrometer-registry-statsd</artifactId>
      <version>1.5.4</version>
    </dependency>

レジストファクトリを宣言する
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

HTTPリクエストの処理時間を収集する
--------------------------------------------------

:java:extdoc:`HttpRequestMetricsHandler <nablarch.integration.micrometer.instrument.handler.http.HttpRequestMetricsHandler>` を使用することで、 HTTP リクエストの処理時間をメトリクスとして収集できる。

このハンドラを使用する場合は、次のようにハンドラキューを構成する。

.. code-block:: xml

  <component name="meterRegistry" class="nablarch.integration.micrometer.logging.LoggingMeterRegistryFactory">
    <property name="meterBinderListProvider" ref="meterBinderListProvider" />
    <property name="applicationDisposer" ref="disposer" />
  </component>

  <component name="webFrontController"
             class="nablarch.fw.web.servlet.WebFrontController">
    <property name="handlerQueue">
      <list>
        <!-- HTTPリクエストのメトリクス収集ハンドラ -->
        <component class="nablarch.integration.micrometer.instrument.handler.http.HttpRequestMetricsHandler">
          <!-- レジストリファクトリが生成する MeterRegistry を meterRegistry プロパティに設定する -->
          <property name="meterRegistry" ref="meterRegistry" />
        </component>

        <component class="nablarch.fw.web.handler.HttpCharacterEncodingHandler"/>

        <!-- 省略 -->
     </list>
    </property>
  </component>

本ハンドラはリクエストの処理時間を計測するため、ハンドラキューの先頭に設定する。

また ``meterRegistry`` プロパティには、使用しているレジストリファクトリが生成した `MeterRegistry(外部サイト、英語)`_ を渡すように設定する。

以上の設定で、次のようなメトリクスが収集されるようになる。

.. code-block:: text

  2020-09-04 19:16:29.085 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: http.server.requests{exception=None,method=GET,outcome=SUCCESS,path=/action/projectBulk/index,status=200} throughput=0.4/s mean=0.8634947s max=1.6078096s
  2020-09-04 19:16:29.086 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: http.server.requests{exception=None,method=GET,outcome=SUCCESS,path=/action/project/index,status=200} throughput=0.4/s mean=0.27510795s max=0.4464502s
  2020-09-04 19:16:29.086 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: http.server.requests{exception=None,method=GET,outcome=SUCCESS,path=/action/projectUpload,status=200} throughput=0.2/s mean=0.4478871s max=0.4478871s
  2020-09-04 19:16:29.086 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: http.server.requests{exception=None,method=POST,outcome=REDIRECTION,path=/action/login,status=303} throughput=0.2/s mean=0.4280518s max=0.4280518s
  2020-09-04 19:16:34.084 [INFO ]      i.m.c.i.l.LoggingMeterRegistry: http.server.requests{exception=None,method=GET,outcome=SUCCESS,path=/action/project/index,status=200} throughput=0.2/s mean=0.0953379s max=0.4464502s

本ハンドラが収集するメトリクスは、 ``http.server.requests`` という名前で作成される。

また、メトリクスには以下のタグが付与される。

.. list-table::

  * - タグ名
    - 説明
  * - ``path``
    - リクエストのパス（クエリ文字列を除く）
  * - ``method``
    - HTTPメソッド
  * - ``status``
    - HTTPステータスコード
  * - ``outcome``
    - ステータスコードの種類を表す文字列（1XX: ``INFORMATION``, 2XX: ``SUCCESS``, 3XX: ``REDIRECTION``, 4XX: ``CLIENT_ERROR``, 5XX: ``SERVER_ERROR``, その他: ``UNKNOWN``）
  * - ``exception``
    - リクエスト処理中のスローされた例外の単純名（例外スローされていない場合は ``None``）


.. _MeterBinder(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-core/1.5.4/io/micrometer/core/instrument/binder/MeterBinder.html
.. _DatadogConfig(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-registry-datadog/1.5.4/io/micrometer/datadog/DatadogConfig.html
.. _CloudWatchConfig(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-registry-cloudwatch2/1.5.4/io/micrometer/cloudwatch2/CloudWatchConfig.html
.. _StatsdConfig(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-registry-statsd/1.5.4/io/micrometer/statsd/StatsdConfig.html
.. _MeterRegistry(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-core/1.5.4/io/micrometer/core/instrument/MeterRegistry.html
.. _DatadogMeterRegistry(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-registry-datadog/1.5.4/io/micrometer/datadog/DatadogMeterRegistry.html
.. _StatsdMeterRegistry(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-registry-statsd/1.5.4/io/micrometer/statsd/StatsdMeterRegistry.html
.. _DatadogMeterRegistry(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-registry-datadog/1.5.4/io/micrometer/datadog/DatadogMeterRegistry.html
.. _CloudWatchMeterRegistry(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-registry-cloudwatch2/1.5.4/io/micrometer/cloudwatch2/CloudWatchMeterRegistry.html
.. _LoggingMeterRegistry(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-core/1.5.4/io/micrometer/core/instrument/logging/LoggingMeterRegistry.html
.. _SimpleMeterRegistry(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-core/1.5.4/io/micrometer/core/instrument/simple/SimpleMeterRegistry.html
.. _JvmMemoryMetrics(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-core/1.5.4/io/micrometer/core/instrument/binder/jvm/JvmMemoryMetrics.html
.. _ProcessorMetrics(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-core/1.5.4/io/micrometer/core/instrument/binder/system/ProcessorMetrics.html
.. _JvmGcMetrics(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-core/1.5.4/io/micrometer/core/instrument/binder/jvm/JvmGcMetrics.html
.. _JvmThreadMetrics(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-core/1.5.4/io/micrometer/core/instrument/binder/jvm/JvmThreadMetrics.html
.. _ClassLoaderMetrics(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-core/1.5.4/io/micrometer/core/instrument/binder/jvm/ClassLoaderMetrics.html
.. _FileDescriptorMetrics(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-core/1.5.4/io/micrometer/core/instrument/binder/system/FileDescriptorMetrics.html
.. _UptimeMetrics(外部サイト、英語): https://javadoc.io/doc/io.micrometer/micrometer-core/1.5.4/io/micrometer/core/instrument/binder/system/UptimeMetrics.html
