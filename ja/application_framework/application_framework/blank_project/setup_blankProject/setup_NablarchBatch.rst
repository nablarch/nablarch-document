----------------------------------------------------------
Nablarchバッチプロジェクトの初期セットアップ
----------------------------------------------------------

Nablarchバッチプロジェクトの初期セットアップでは以下を行う。

* Nablarchバッチプロジェクトの生成
* Nablarchバッチプロジェクトの動作確認


生成するプロジェクトの概要
----------------------------------------------------------

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
    - H2 Databaes Engine(アプリケーションに組み込み)
  * - 生成するプロジェクトに含まれるもの
    - 生成されたプロジェクトには以下が含まれる。
       
      * Nablarchバッチアプリケーション用の基本的な設定
      * 疎通確認用の都度起動バッチアプリケーション
      * 疎通確認用のテーブルをキューとして使ったメッセージング
      * メール送信バッチの設定 \ [#mailSendBatch]_\
      * Mavenと連動して動作するツールの初期設定( :ref:`about_maven_parent_module` を参照することによって取り込んでいる)。


.. [#mailSendBatch]
   メール送信バッチは、:ref:`常駐バッチ<nablarch_batch-resident_batch>`  として動作し、SMTPサーバに対してメールを送信するものである。
   コンポーネント設定ファイルのサンプルは ``src/main/resources/mail-sender-boot.xml`` に存在する。
   メール送信バッチは初期環境構築時には必要ないが、必要になったタイミングで :ref:`メール送信<mail>` の解説を読んだ上で使用する。


他のプロジェクトとの関係、及びディレクトリ構成は、 :doc:`../MavenModuleStructures/index` を参照。


.. _firstStepGenerateBatchBlankProject:

ブランクプロジェクト作成
----------------------------------------------------------

Nablarchが提供するアーキタイプを使用してブランクプロジェクトを生成する。


mvnコマンドの実行
~~~~~~~~~~~~~~~~~

`Maven Archetype Plugin(外部サイト、英語) <https://maven.apache.org/archetype/maven-archetype-plugin/usage.html>`_ を使用して、ブランクプロジェクトを生成する。

カレントディレクトリを、ブランクプロジェクトを作成したいディレクトリ(任意のディレクトリで可)に変更する。

その後、以下のコマンドを実行する。

.. code-block:: bat

  mvn archetype:generate -DarchetypeGroupId=com.nablarch.archetype -DarchetypeArtifactId=nablarch-batch-archetype -DarchetypeVersion={nablarch_version}

上記コマンドで使用されているNablarchのバージョンは |nablarch_version| となっている。バージョンを変更したい場合は、以下のパラメータを変更すること。

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 6,20

  * - 設定値
    - 説明
  * - archetypeVersion
    - 使用したいアーキタイプのバージョンを指定する。（Nablarch 5u25以降を指定すること）

.. tip::
  Nablarch 5u24以前のバージョンでブランクプロジェクトを生成したい場合は、上記コマンドの ``archetype:generate`` を ``org.apache.maven.plugins:maven-archetype-plugin:2.4:generate`` に変更して以下の例のように実行すること。

  .. code-block:: bat

    mvn org.apache.maven.plugins:maven-archetype-plugin:2.4:generate -DarchetypeGroupId=com.nablarch.archetype -DarchetypeArtifactId=nablarch-batch-archetype -DarchetypeVersion=5u24

  この例で使用されているNablarchのバージョンは 5u24 となっている。バージョン変更したい場合は、同様にパラメータarchetypeVersionを変更すること。

プロジェクト情報の入力
~~~~~~~~~~~~~~~~~~~~~~~~

上記コマンドを実行すると、以下の項目について入力を求められるので、 生成されるブランクプロジェクトに関する情報を入力する。

=========== ========================================= =======================
入力項目    説明                                      設定例
=========== ========================================= =======================
groupId      グループID（通常はパッケージ名を入力）   ``com.example``
artifactId   アーティファクトID                       ``myapp-batch``
version      バージョン番号                           ``0.1.0``
package      パッケージ(通常はグループIDと同じ)       ``com.example``
=========== ========================================= =======================

.. important::
   項目groupIdおよびpackageは、Javaのパッケージ名にマッピングされる。
   よって、これらの入力値には、英小文字、数字、ドットを使用し、ハイフンは使用しないこと。

プロジェクト情報の入力が終わると、Y: :と表示される。

 * 入力した内容をもとに、ひな形を生成する場合には「Y」を入力してください。
 * プロジェクト情報の入力をやり直したい場合には「N」を入力してください。

コマンドが正常終了した場合、ブランクプロジェクトがカレントディレクトリ配下に作成される。


.. _firstStepBatchStartupTest:

疎通確認(都度起動バッチ)
------------------------

自動テスト(都度起動バッチ)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

アーキタイプから生成したプロジェクトには、以下のユニットテストが含まれている。

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 9,20

  * - ユニットテストのクラス
    - テスト内容
  * - SampleBatchActionRequestTest
    - Nablarchのテスティングフレームワークを使用して、バッチを起動可能であるかを確認する。


ユニットテストを実行することで、ブランクプロジェクトの生成に成功していることを確認する。

以下のコマンドを実行する。

.. code-block:: text

  cd myapp-batch
  mvn test


実行に成功すると、以下のようなログがコンソールに出力される。

.. code-block:: text

  (中略)
  [INFO] ----------------------< com.example:myapp-batch >-----------------------
  [INFO] Building myapp-batch 0.1.0
  [INFO] --------------------------------[ jar ]---------------------------------
  (中略)
  [INFO] Results:
  [INFO]
  [INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0
  [INFO]
  [INFO] ------------------------------------------------------------------------
  [INFO] BUILD SUCCESS
  [INFO] ------------------------------------------------------------------------
  (以下略)

起動テスト(都度起動バッチ)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

生成したプロジェクトには、以下の都度起動バッチが含まれている。

======================== ================================================================================
バッチのクラス           内容
======================== ================================================================================
SampleAction             バッチアプリケーション実装する際に一般的に使用するNablarchの機能の動作確認
======================== ================================================================================


都度起動バッチが起動することで、ブランクプロジェクトの生成に成功していることを確認する。


.. _firstStepBatchBuild:

バッチアプリケーションのビルド
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

まだ、生成したプロジェクトにカレントディレクトリを移動していない場合は移動する。

.. code-block:: text

  cd myapp-batch


以下のコマンドを実行することで、バッチアプリケーションのビルドを行う。

.. code-block:: text

  mvn package

.. _firstStepBatchExecOnDemandBatch:

都度起動バッチアプリケーションの起動
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

以下のコマンドを実行する。

.. code-block:: bash

  mvn exec:java -Dexec.mainClass=nablarch.fw.launcher.Main ^
      -Dexec.args="'-diConfig' 'classpath:batch-boot.xml' '-requestPath' 'SampleBatch' '-userId' 'batch_user'"

起動に成功すると、以下のようなログがコンソールに出力される。

.. code-block:: text

  2020-04-28 08:56:23.353 -INFO- com.example.SampleBatch [202004280856233530002] boot_proc = [] proc_sys = [batch] req_id = [SampleBatch] usr_id = [batch_user] 疎通確認を開始します。
  2020-04-28 08:56:23.379 -INFO- com.example.SampleBatch [202004280856233530002] boot_proc = [] proc_sys = [batch] req_id = [SampleBatch] usr_id = [batch_user] 取得したコード名称：ロック
  2020-04-28 08:56:23.383 -INFO- com.example.SampleBatch [202004280856233530002] boot_proc = [] proc_sys = [batch] req_id = [SampleBatch] usr_id = [batch_user] 疎通確認が完了しました。
  2020-04-28 08:56:23.396 -INFO- nablarch.fw.handler.MultiThreadExecutionHandler [202004280856233470001] boot_proc = [] proc_sys = [batch] req_id = [SampleBatch] usr_id = [batch_user] 
  Thread Status: normal end.
  Thread Result:[200 Success] The request has succeeded.
  2020-04-28 08:56:23.407 -INFO- nablarch.core.log.app.BasicCommitLogger [202004280856233470001] boot_proc = [] proc_sys = [batch] req_id = [SampleBatch] usr_id = [batch_user] TOTAL COMMIT COUNT = [1]
  2020-04-28 08:56:23.413 -INFO- nablarch.fw.launcher.Main [null] boot_proc = [] proc_sys = [batch] req_id = [null] usr_id = [null] @@@@ END @@@@ exit code = [0] execute time(ms) = [559]

.. _firstStepBatchStartupTestDbMessagingBatch:

疎通確認(テーブルをキューとして使ったメッセージング)
--------------------------------------------------------------------

生成したプロジェクトには、以下のアプリケーションが含まれている。

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 5,20

  * - バッチのクラス
    - 内容
  * - SampleResiAction
    - テーブルをキューとして使ったメッセージングの基本的な処理である「処理対象テーブルから値を取得し、処理済みフラグを立てる」処理を実装したアプリケーション


上記アプリケーションが起動することで、ブランクプロジェクトの生成に成功していることを確認する。


起動テスト(テーブルをキューとして使ったメッセージング)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

アプリケーションのビルド
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

まだビルドしていない場合は、 :ref:`firstStepBatchBuild` を参照してビルドする。

.. _firstStepBatchExecDbMessagingBatch:

アプリケーションの起動
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

以下のコマンドを実行する。

.. code-block:: bash

  mvn exec:java -Dexec.mainClass=nablarch.fw.launcher.Main ^
      -Dexec.args="'-diConfig' 'classpath:resident-batch-boot.xml' '-requestPath' 'SampleResiBatch' '-userId' 'batch_user'"

.. tip::

  上記引数の都度起動バッチアプリケーションとの相違点は以下の通りである。

  * -diConfigで指定するxmlファイル
  * -requestPathで指定するリクエストパス


起動に成功すると、以下のようなログがコンソールに出力される。

.. code-block:: text

    2020-04-28 08:58:15.350 -INFO- nablarch.fw.reader.DatabaseTableQueueReader [202004280858153390001] boot_proc = [] proc_sys = [batch] req_id = [SampleResiBatch] usr_id = [batch_user] read database record. key info: {USER_INFO_ID=00000000000000000001}
    2020-04-28 08:58:15.356 -INFO- com.example.SampleResiBatch [202004280858153560002] boot_proc = [] proc_sys = [batch] req_id = [SampleResiBatch] usr_id = [batch_user] handleが呼ばれました。
    2020-04-28 08:58:15.363 -INFO- com.example.SampleResiBatch [202004280858153560002] boot_proc = [] proc_sys = [batch] req_id = [SampleResiBatch] usr_id = [batch_user] USER_INFO_ID:00000000000000000001
    2020-04-28 08:58:15.367 -INFO- com.example.SampleResiBatch [202004280858153560002] boot_proc = [] proc_sys = [batch] req_id = [SampleResiBatch] usr_id = [batch_user] LOGIN_ID:TAROU
    2020-04-28 08:58:15.371 -INFO- com.example.SampleResiBatch [202004280858153560002] boot_proc = [] proc_sys = [batch] req_id = [SampleResiBatch] usr_id = [batch_user] KANA_NAME:たろう
    2020-04-28 08:58:15.379 -INFO- com.example.SampleResiBatch [202004280858153560002] boot_proc = [] proc_sys = [batch] req_id = [SampleResiBatch] usr_id = [batch_user] KANJI_NAME:太郎

終了はctrl + c等で強制終了すること。


.. important ::

  Nablarchが想定している正しい終了方法は、BATCH_REQUESTテーブルのPROCESS_HALT_FLGのフラグに1を設定するという方法である。本手順上では、簡単に停止させるために、ctrl + cで停止している。


  テーブルをキューとして使ったメッセージングを一端終了した後に再び起動させたい場合、 :doc:`../firstStep_appendix/ResiBatchReboot` を参照。


疎通確認になぜか失敗する場合
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

原因は分からないが疎通確認に失敗する場合、どこかで手順を誤っている可能性がある。

原因が分からない場合は、:ref:`firstStepGenerateBatchBlankProject` からやり直してみること。



補足
--------------------

H2のデータの確認方法や、ブランクプロジェクトに組み込まれているツールに関しては、 :doc:`../firstStep_appendix/firststep_complement` を参照すること。
