.. -*- mode: rst; coding: utf-8-unix -*-

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
      * 疎通確認用都度起動バッチアプリケーション
      * 疎通確認用のテーブルをキューとして使ったメッセージング
      * メール送信バッチの設定 \ [#mailSendBatch]_\
      * Mavenと連動して動作するツールの初期設定( :ref:`about_maven_parent_module` を参照することによって取り込んでいる)。


.. [#mailSendBatch]
   メール送信バッチは、:ref:`常駐バッチ<nablarch_batch-resident_batch>`  として動作し、SMTPサーバに対してメール送信を行うものである。
   コンポーネント定義ファイルのサンプルは ``src/main/resources/mail-sender-boot.xml`` に存在する。
   メール送信バッチは初期環境構築時には必要ないが、必要になったタイミングで :ref:`メール送信<mail>` の解説を読んだ上で使用する。


他のプロジェクトとの関係、及びディレクトリ構成は、 :doc:`../MavenModuleStructures/index` を参照。


.. _firstStepGenerateBatchBlankProject:

ブランクプロジェクト作成
----------------------------------------------------------

Nablarchが提供するアーキタイプを使用してブランクプロジェクトを生成する。


mvnコマンドの実行
~~~~~~~~~~~~~~~~~

カレントディレクトリを、ブランクプロジェクトを作成したいディレクトリ(任意のディレクトリで可)に変更し、以下のファイルを配置する。

:download:`バッチファイル <bat/generateNablarchBatchProject.bat>`

配置後、引数に必要なパラメータを指定しbatファイルを実行する。

generateNablarchBatchProject.bat |nablarch_version| <<groupId>> <<artifactId>> <<version>> <<package(任意)>>

上記コマンドに設定するパラメータは以下の通り。
なお、nablarchのバージョンを変更したい場合には |nablarch_version| を変更すること。
カレントディレクトリを、ブランクプロジェクトを作成したいディレクトリ(任意のディレクトリで可)に変更する。

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
  [INFO] ------------------------------------------------------------------------
  [INFO] Building myapp-batch 0.1.0
  [INFO] ------------------------------------------------------------------------
  (中略)
  Tests run: 1, Failures: 0, Errors: 0, Skipped: 0

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

以下のコマンドを実行することで、依存するライブラリを一箇所に集める。

.. code-block:: text

  mvn dependency:copy-dependencies -DoutputDirectory=target/dependency -DincludeScope=runtime


都度起動バッチアプリケーションの起動
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

以下のコマンドを実行する。


**Unix系の場合：**

.. code-block:: bash

  java -cp "target/myapp-batch-0.1.0-dev.jar:target/dependency/*" nablarch.fw.launcher.Main -diConfig classpath:batch-boot.xml -requestPath SampleBatch -userId batch_user


**Windowsの場合：**

.. code-block:: bat

  java -cp "target/myapp-batch-0.1.0-dev.jar;target/dependency/*" nablarch.fw.launcher.Main -diConfig classpath:batch-boot.xml -requestPath SampleBatch -userId batch_user


起動に成功すると、以下のようなログがコンソールに出力される。

.. code-block:: text

  2016-09-01 16:00:20.620 -INFO- ROO [201609011600206200001] 疎通確認を開始します。
  2016-09-01 16:00:20.646 -INFO- ROO [201609011600206200001] 取得したコード名称：ロック
  2016-09-01 16:00:20.648 -INFO- ROO [201609011600206200001] 疎通確認が完了しました。
  2016-09-01 16:00:20.652 -INFO- ROO [null]
  Thread Status: normal end.
  Thread Result:[200 Success] The request has succeeded.
  2016-09-01 16:00:20.655 -INFO- ROO [null] TOTAL COMMIT COUNT = [1]
  2016-09-01 16:00:20.658 -INFO- ROO [null] @@@@ END @@@@ exit code = [0] execute time(ms) = [1054]




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


アプリケーションの起動
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

以下のコマンドを実行する。


**Unix系の場合：**

.. code-block:: bash

  java -cp "target/myapp-batch-0.1.0-dev.jar:target/dependency/*" nablarch.fw.launcher.Main -diConfig classpath:resident-batch-boot.xml -requestPath SampleResiBatch -userId batch_user


**Windowsの場合：**

.. code-block:: bat

  java -cp "target/myapp-batch-0.1.0-dev.jar;target/dependency/*" nablarch.fw.launcher.Main -diConfig classpath:resident-batch-boot.xml -requestPath SampleResiBatch -userId batch_user


.. tip::

  上記引数の都度起動バッチアプリケーションとの相違点は以下の通りである。

  * -diConfigで指定するxmlファイル
  * -requestPathで指定するリクエストパス


起動に成功すると、以下のようなログがコンソールに出力される。

.. code-block:: text

    2016-04-11 15:18:07.916 -INFO- ROO [201604111518078810001] read database record. key info: {USER_INFO_ID=00000000000000000001}
    2016-04-11 15:18:07.917 -INFO- ROO [201604111518079170002] handleが呼ばれました。
    2016-04-11 15:18:07.917 -INFO- ROO [201604111518079170002] USER_INFO_ID:00000000000000000001
    2016-04-11 15:18:07.918 -INFO- ROO [201604111518079170002] LOGIN_ID:tarou
    2016-04-11 15:18:07.918 -INFO- ROO [201604111518079170002] KANA_NAME:たろう
    2016-04-11 15:18:07.919 -INFO- ROO [201604111518079170002] KANJI_NAME:太郎


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
