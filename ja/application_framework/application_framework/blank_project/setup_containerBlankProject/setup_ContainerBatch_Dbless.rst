--------------------------------------------------------------------
コンテナ用Nablarchバッチ（DB接続無し）プロジェクトの初期セットアップ
--------------------------------------------------------------------

コンテナ用Nablarchバッチ（DB接続無し）プロジェクトの初期セットアップでは以下を行う。

* コンテナ用Nablarchバッチ（DB接続無し）プロジェクトの生成
* コンテナ用Nablarchバッチ（DB接続無し）プロジェクトの動作確認
* コンテナイメージの作成
* コンテナイメージの実行


生成するプロジェクトの概要
----------------------------------------------------------

本手順で生成するプロジェクトの概要は以下の通りである。

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 8,20

  * - 項目
    - 説明
  * - プロジェクト種別
    - Mavenプロジェクト
  * - プロジェクト構成
    - 単一プロジェクト構成
  * - 生成するプロジェクトに含まれるもの
    - 生成されたプロジェクトには以下が含まれる。
       
      * Nablarchバッチアプリケーション用の基本的な設定
      * 疎通確認用の都度起動バッチアプリケーション
      * Mavenと連動して動作するツールの初期設定( :ref:`about_maven_parent_module` を参照することによって取り込んでいる)。


他のプロジェクトとの関係、及びディレクトリ構成は、 :doc:`../MavenModuleStructures/index` を参照。


.. _firstStepGenerateContainerBatchDblessBlankProject:

ブランクプロジェクト作成
----------------------------------------------------------

Nablarchが提供するアーキタイプを使用してブランクプロジェクトを生成する。

mvnコマンドの実行
~~~~~~~~~~~~~~~~~

`Maven Archetype Plugin(外部サイト、英語) <https://maven.apache.org/archetype/maven-archetype-plugin/usage.html>`_ を使用して、ブランクプロジェクトを生成する。

カレントディレクトリを、ブランクプロジェクトを作成したいディレクトリ(任意のディレクトリで可)に変更する。

その後、以下のコマンドを実行する。

.. code-block:: bat

  mvn archetype:generate -DarchetypeGroupId=com.nablarch.archetype -DarchetypeArtifactId=nablarch-container-batch-dbless-archetype -DarchetypeVersion={nablarch_version}

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

    mvn org.apache.maven.plugins:maven-archetype-plugin:2.4:generate -DarchetypeGroupId=com.nablarch.archetype -DarchetypeArtifactId=nablarch-container-batch-dbless-archetype -DarchetypeVersion=5u24

  この例で使用されているNablarchのバージョンは 5u24 となっている。バージョン変更したい場合は、同様にパラメータarchetypeVersionを変更すること。

プロジェクト情報の入力
~~~~~~~~~~~~~~~~~~~~~~~~

上記コマンドを実行すると、以下の項目について入力を求められるので、 生成されるブランクプロジェクトに関する情報を入力する。

=========== ========================================= =======================
入力項目    説明                                      設定例
=========== ========================================= =======================
groupId      グループID（通常はパッケージ名を入力）   ``com.example``
artifactId   アーティファクトID                       ``myapp-container-batch-dbless``
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


.. _firstStepContainerBatchDblessStartupTest:

疎通確認
-------------------------

疎通確認の仕組みや手順は通常のNablarchバッチ（DB接続無し）プロジェクトと同じなので、 :ref:`Nablarchバッチ（DB接続無し）プロジェクトの初期セットアップ手順 <firstStepDblessBatchStartupTest>` を参照。

.. note::

  アーティファクトID が ``myapp-container-batch-dbless`` になっている点は、適宜読み替えてディレクトリやコマンドを指定すること。


.. _firstStepBuildContainerBatchDblessDockerImage:

コンテナイメージを作成する
----------------------------------

コンテナイメージの作成手順は通常のコンテナ用Nablarchバッチプロジェクトと同じなので、 :ref:`コンテナ用Nablarchバッチプロジェクトのコンテナイメージ作成手順 <firstStepBuildContainerBatchDockerImage>` を参照。

.. note::

  アーティファクトID が ``myapp-container-batch-dbless`` になっている点は、適宜読み替えてディレクトリやコマンドを指定すること。


.. _firstStepRunContainerBatchDblessDockerImage:

コンテナイメージを実行する
----------------------------------

コンテナイメージの実行手順は通常のコンテナ用Nablarchバッチプロジェクトと同じなので、 :ref:`コンテナ用Nablarchバッチプロジェクトのコンテナイメージ実行手順 <firstStepRunContainerBatchDockerImage>` を参照。

.. note::

  アーティファクトID が ``myapp-container-batch-dbless`` になっている点は、適宜読み替えてディレクトリやコマンドを指定すること。
  また、コンテナ用Nablarchバッチ（DB接続無し）プロジェクトでは都度起動バッチのみ実行可能である。
