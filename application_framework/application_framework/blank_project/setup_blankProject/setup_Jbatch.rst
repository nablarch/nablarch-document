=========================================================
JSR352に準拠したバッチプロジェクトの初期セットアップ
=========================================================

JSR352に準拠したバッチプロジェクトの初期セットアップでは以下を行う。

* JSR352に準拠したバッチプロジェクトの生成
* JSR352に準拠したバッチプロジェクトの動作確認


生成するプロジェクトの概要
=========================================================

本手順で生成するプロジェクトの概要は以下の通りである。

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 7,20

  * - 項目
    - 説明
  * - プロジェクト種別
    - Mavenプロジェクト
  * - プロジェクト構成
    - 単一プロジェクト構成
  * - 使用DB
    - H2 Database Engine(アプリケーションに組み込み)
  * - 生成するプロジェクトに含まれるもの
    - 生成されたプロジェクトには以下が含まれる。
       
      * JSR352に準拠したバッチアプリケーション用の基本的な設定
      * batchlet方式による疎通確認用バッチアプリケーション
      * chunk方式による疎通確認用バッチアプリケーション
      * ETL機能を使用した疎通確認用アプリケーション \ [#etl]_\
      * Mavenと連動して動作するツールの初期設定( :ref:`about_maven_parent_module` を参照することによって取り込んでいる)。


.. [#etl] ETLを実行するクラスはNablarch内に存在するため、プロジェクトには設定ファイル、及びETLが使用するDTOクラス、entityクラスのみ存在する。


他のプロジェクトとの関係、及びディレクトリ構成は、 :doc:`../MavenModuleStructures/index` を参照。


.. _firstStepGenerateBatchEEBlankProject:

ブランクプロジェクト作成
=======================================================

Nablarchが提供するアーキタイプを使用してブランクプロジェクトを生成する。


mvnコマンドの実行
-------------------------------------------------------

カレントディレクトリを、ブランクプロジェクトを作成したいディレクトリ(任意のディレクトリで可)に変更し、以下のファイルを配置する。

:download:`バッチファイル <bat/generateJbatchProject.bat>`

配置後、引数に必要なパラメータを指定しbatファイルを実行する。

generateJbatchProject.bat |nablarch_version| <<groupId>> <<artifactId>> <<version>> <<package(任意)>>

上記コマンドに設定するパラメータは以下の通り。
なお、nablarchのバージョンを変更したい場合には |nablarch_version| を変更すること。

=========== ========================================= =======================
入力項目    説明                                      設定例
=========== ========================================= =======================
groupId      グループID（通常はパッケージ名を入力）   ``com.example``
artifactId   アーティファクトID                       ``myapp-batch-ee``
version      バージョン番号                           ``0.1.0``
package      パッケージ(通常はグループIDと同じ)       ``com.example``
=========== ========================================= =======================

.. important::
   項目groupIdおよびpackageは、Javaのパッケージ名にマッピングされる。
   よって、これらの入力値には、英小文字、数字、ドットを使用し、ハイフンは使用しないこと。

コマンドが正常終了した場合、ブランクプロジェクトがカレントディレクトリ配下に作成される。


.. _firstStepBatchEEStartupTest:

疎通確認
=====================================================

自動テスト
-----------------------------------------------------

アーキタイプから生成したプロジェクトには、以下のユニットテストが含まれている。

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 9,20

  * - ユニットテストのクラス
    - テスト内容
  * - SampleBatchletTest
    - データベース接続を伴うクラスのJUnitテスト。


ユニットテストを実行することで、ブランクプロジェクトの生成に成功していることを確認する。

以下のコマンドを実行する。

.. code-block:: text

  cd myapp-batch-ee
  mvn test


実行に成功すると、以下のようなログがコンソールに出力される。

.. code-block:: text

  (中略)
  [INFO] ------------------------------------------------------------------------
  [INFO] Building myapp-batch-ee 0.1.0
  [INFO] ------------------------------------------------------------------------
  (中略)
  2020-03-25 18:39:11.013 -WARN- nablarch.core.repository.di.config.xml.XmlComponentDefinitionLoader [null] boot_proc = [] proc_sys = [] req_id = [null] usr_id = [null] component property was overridden. component name = businessDateProvider, property = dbTransactionManager
  18:39:11.060 INFO  c.z.h.HikariDataSource HikariPool-1 - Starting...
  18:39:11.411 INFO  c.z.h.p.PoolBase HikariPool-1 - Driver does not support get/set network timeout for connections. (org.h2.jdbc.JdbcConnection.getNetworkTimeout()I)
  18:39:11.415 INFO  c.z.h.HikariDataSource HikariPool-1 - Start completed.
  2020-03-25 18:39:11.499 -INFO- com.example.batchlet.SampleBatchlet [null] boot_proc = [] proc_sys = [] req_id = [null] usr_id = [null] 削除件数：10件
  [INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.877 s - in com.example.batchlet.SampleBatchletTest
  [INFO]
  [INFO] Results:
  [INFO]
  [INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0
  [INFO]
  [INFO] ------------------------------------------------------------------------
  [INFO] BUILD SUCCESS
  [INFO] ------------------------------------------------------------------------
  (以下略)



起動テスト
--------------------------------------------------------

生成したプロジェクトには、以下のバッチアプリケーションが組み込まれている。

=================== ================================================================================
ジョブID            内容
=================== ================================================================================
sample-batchlet     batchlet方式で実装されたサンプルアプリケーション。
sample-chunk        chunk方式で実装されたサンプルアプリケーション。
sample-etl          Nablarchが提供するETL機能のサンプルアプリケーション。
=================== ================================================================================


上記3つのバッチアプリケーションの動作確認を行うことで、ブランクプロジェクトの生成に成功していることを確認する。


.. _firstStepBatchEEBuild:

バッチアプリケーションのビルド
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

まだ、生成したプロジェクトにカレントディレクトリを移動していない場合は移動する。

.. code-block:: text

  cd myapp-batch-ee


以下のコマンドを実行することで、バッチアプリケーションのビルドを行う。

.. code-block:: text

  mvn package

batchlet方式のバッチアプリケーションの起動
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
batchlet方式のバッチアプリケーションでは、SAMPLE_USERテーブルのデータを削除する処理が実装されている。

以下のコマンドを実行する。

.. code-block:: bash

  mvn exec:java -Dexec.mainClass=nablarch.fw.batch.ee.Main -Dexec.args="'sample-batchlet'"

実行に成功すると、以下のようなログが ``./progress.log`` に出力される。

.. code-block:: text

  2020-03-25 18:32:26.669 -INFO- progress [null] boot_proc = [] proc_sys = [] req_id = [null] usr_id = [null] start job. job name: [sample-batchlet]
  2020-03-25 18:32:26.680 -INFO- progress [null] boot_proc = [] proc_sys = [] req_id = [null] usr_id = [null] start step. job name: [sample-batchlet] step name: [step1]
  2020-03-25 18:32:26.923 -INFO- progress [null] boot_proc = [] proc_sys = [] req_id = [null] usr_id = [null] finish step. job name: [sample-batchlet] step name: [step1] step status: [SUCCESS]
  2020-03-25 18:32:26.929 -INFO- progress [null] boot_proc = [] proc_sys = [] req_id = [null] usr_id = [null] finish job. job name: [sample-batchlet]


.. tip::

  このbatchletはSAMPLE_USERテーブルのデータの全件削除を行っている。削除したデータを復元したい場合は、 :ref:`firstStepBatchEERunETL` のコマンドを実行すること。



.. _firstStepBatchEERunETL:

ETL機能を使用するアプリケーションの起動
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ETL機能を使用したアプリケーションでは、SAMPLE_USERテーブルにデータを投入するように設定されている。


以下のコマンドを実行する。

.. code-block:: bash

  mvn exec:java -Dexec.mainClass=nablarch.fw.batch.ee.Main -Dexec.args="'sample-etl'"

起動に成功すると、以下のようなログが ``./progress.log`` に出力される。

.. code-block:: text

  2020-03-25 18:33:43.331 -INFO- progress [null] boot_proc = [] proc_sys = [] req_id = [null] usr_id = [null] start step. job name: [sample-etl] step name: [load]
  2020-03-25 18:33:43.345 -INFO- progress [null] boot_proc = [] proc_sys = [] req_id = [null] usr_id = [null] job name: [sample-etl] step name: [load] input count: [10]
  2020-03-25 18:33:43.353 -INFO- progress [null] boot_proc = [] proc_sys = [] req_id = [null] usr_id = [null] job name: [sample-etl] step name: [load] write table name: [SAMPLE_USER]
  2020-03-25 18:33:43.359 -INFO- progress [null] boot_proc = [] proc_sys = [] req_id = [null] usr_id = [null] job name: [sample-etl] step name: [load] total tps: [769.23] current tps: [769.23] estimated end time: [2020/03/25 06:33:43.359] remaining count: [0]
  2020-03-25 18:33:43.365 -INFO- progress [null] boot_proc = [] proc_sys = [] req_id = [null] usr_id = [null] finish step. job name: [sample-etl] step name: [load] step status: [COMPLETED]
  2020-03-25 18:33:43.370 -INFO- progress [null] boot_proc = [] proc_sys = [] req_id = [null] usr_id = [null] finish job. job name: [sample-etl]



chunk方式のバッチアプリケーションの起動
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
chunk方式のバッチアプリケーションでは、SAMPLE_USERテーブルからデータを取り出し、編集してCSVファイルに出力する処理が実装されている。

以下のコマンドを実行する。

.. code-block:: bash

  mvn exec:java -Dexec.mainClass=nablarch.fw.batch.ee.Main -Dexec.args="'sample-chunk'"

起動に成功すると、以下のようなログが ``./progress.log`` に出力される。

.. code-block:: text

  2020-03-25 18:34:50.681 -INFO- progress [null] boot_proc = [] proc_sys = [] req_id = [null] usr_id = [null] start job. job name: [sample-chunk]
  2020-03-25 18:34:50.691 -INFO- progress [null] boot_proc = [] proc_sys = [] req_id = [null] usr_id = [null] start step. job name: [sample-chunk] step name: [step1]
  2020-03-25 18:34:50.925 -INFO- progress [null] boot_proc = [] proc_sys = [] req_id = [null] usr_id = [null] job name: [sample-chunk] step name: [step1] input count: [10]
  2020-03-25 18:34:50.960 -INFO- progress [null] boot_proc = [] proc_sys = [] req_id = [null] usr_id = [null] job name: [sample-chunk] step name: [step1] total tps: [151.52] current tps: [151.52] estimated end time: [2020/03/25 06:34:50.959] remaining count: [5]
  2020-03-25 18:34:50.966 -INFO- progress [null] boot_proc = [] proc_sys = [] req_id = [null] usr_id = [null] job name: [sample-chunk] step name: [step1] total tps: [243.90] current tps: [714.29] estimated end time: [2020/03/25 06:34:50.966] remaining count: [0]
  2020-03-25 18:34:50.977 -INFO- progress [null] boot_proc = [] proc_sys = [] req_id = [null] usr_id = [null] finish step. job name: [sample-chunk] step name: [step1] step status: [COMPLETED]
  2020-03-25 18:34:50.984 -INFO- progress [null] boot_proc = [] proc_sys = [] req_id = [null] usr_id = [null] finish job. job name: [sample-chunk]



また、testdata/output/outputdata.csvに以下のデータが出力される。

.. code-block:: text
  
  ユーザID,氏名
  1,名部楽 一郎
  2,名部楽 二郎
  3,名部楽 三郎
  4,名部楽 四朗
  5,名部楽 五郎
  6,名部楽 六郎
  7,名部楽 七郎
  8,名部楽 八郎
  9,名部楽 九郎
  10,名部楽 十郎


.. tip::

  testdata/output/outputdata.csvはUTF-8で出力される。
  testdata/output/outputdata.csvの内容を確認する際、Excelで開くと化けて表示されるため、テキストエディタで開くこと。


疎通確認になぜか失敗する場合
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

原因は分からないが疎通確認に失敗する場合、どこかで手順を誤っている可能性がある。

原因が分からない場合は、:ref:`firstStepGenerateBatchEEBlankProject` からやり直してみること。



補足
--------------------

H2のデータの確認方法や、ブランクプロジェクトに組み込まれているツールに関しては、 :doc:`../firstStep_appendix/firststep_complement` を参照すること。
