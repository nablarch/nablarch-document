---------------------------------------------------------------------------------
コンテナ用RESTfulウェブサービスプロジェクトの初期セットアップ
---------------------------------------------------------------------------------

コンテナ用RESTfulウェブサービスプロジェクトの初期セットアップでは以下を行う。

* RESTfulウェブサービスプロジェクトの生成
* RESTfulウェブサービスプロジェクトの動作確認
* コンテナイメージの作成
* コンテナイメージの実行


事前準備
-------------------------------------------------------------

後の :ref:`firstStepContainerWebServiceStartupTest` で使用するため、以下のいずれかをインストールする。

* Firefox
* Chrome


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
  * - 使用DB
    - H2 Databaes Engine(アプリケーションに組み込み)
  * - 組み込まれているアダプタ
    - * Jersey用アダプタ(詳細は、 :ref:`jaxrs_adaptor` を参照)
      * ルーティングアダプタ(詳細は、 :ref:`router_adaptor` を参照)
  * - 生成するプロジェクトに含まれるもの
    - 生成されたプロジェクトには以下が含まれる。
       
      * NablarchのRESTfulウェブサービス用の基本的な設定
      * 疎通確認用RESTfulウェブサービス
      * Mavenと連動して動作するツールの初期設定( :ref:`about_maven_parent_module` を参照することによって取り込んでいる)。


他のプロジェクトとの関係、及びディレクトリ構成は、 :doc:`../MavenModuleStructures/index` を参照。


.. _firstStepGenerateContainerJaxrsBlankProject:

ブランクプロジェクト作成
----------------------------------------------------------

Nablarchが提供するアーキタイプを使用してブランクプロジェクトを生成する。


~~~~~~~~~~~~~~~~~
mvnコマンドの実行
~~~~~~~~~~~~~~~~~

`Maven Archetype Plugin(外部サイト、英語) <https://maven.apache.org/archetype/maven-archetype-plugin/usage.html>`_ を使用して、ブランクプロジェクトを生成する。

カレントディレクトリを、ブランクプロジェクトを作成したいディレクトリ(任意のディレクトリで可)に変更する。

その後、以下のコマンドを実行する。

.. code-block:: bat

  mvn archetype:generate -DarchetypeGroupId=com.nablarch.archetype -DarchetypeArtifactId=nablarch-container-jaxrs-archetype -DarchetypeVersion={nablarch_version}

上記コマンドで使用されているNablarchのバージョンは |nablarch_version| となっている。バージョンを変更したい場合は、以下のパラメータを変更すること。

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 6,20

  * - 設定値
    - 説明
  * - archetypeVersion
    - 使用したいアーキタイプのバージョンを指定する。（Nablarch 6u2以降を指定すること）


プロジェクト情報の入力
~~~~~~~~~~~~~~~~~~~~~~~

上記コマンドを実行すると、以下の項目について入力を求められるので、 生成されるブランクプロジェクトに関する情報を入力する。

=========== ========================================= =======================
入力項目    説明                                      設定例
=========== ========================================= =======================
groupId      グループID（通常はパッケージ名を入力）   ``com.example``
artifactId   アーティファクトID                       ``myapp-container-jaxrs``
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


.. _firstStepContainerWebServiceStartupTest:

疎通確認
-------------------------------------------

疎通確認の仕組みや手順は通常のRESTfulウェブサービスプロジェクトと同じなので、 :ref:`RESTfulウェブサービスプロジェクトの初期セットアップ <firstStepWebServiceStartupTest>` を参照。

.. note::

  アーティファクトID が ``myapp-container-jaxrs`` になっている点は、適宜読み替えてディレクトリやコマンドを指定すること。


.. _firstStepBuildContainerWebServiceDockerImage:

コンテナイメージを作成する
----------------------------------

コンテナイメージの作成方法はコンテナ用のウェブプロジェクトと同じなので、 :ref:`コンテナ用ウェブプロジェクトの初期セットアップ <firstStepBuildContainerWebDockerImage>` を参照。

.. note::

  アーティファクトID が ``myapp-container-jaxrs`` になっている点は、適宜読み替えてディレクトリやコマンドを指定すること。


.. _firstStepRunContainerWebServiceDockerImage:

コンテナイメージを実行する
----------------------------------

コンテナイメージの実行方法はコンテナ用のウェブプロジェクトと同じなので、 :ref:`コンテナ用ウェブプロジェクトの初期セットアップ <firstStepRunContainerWebDockerImage>` を参照。

.. note::

  アーティファクトID が ``myapp-container-jaxrs`` になっている点は、適宜読み替えてディレクトリやコマンドを指定すること。

.. note::

  動作確認は、以下のURLで行える。

  * ``http://localhost:8080/find/json``
  * ``http://localhost:8080/find/xml``



補足
--------------------

H2のデータの確認方法や、ブランクプロジェクトに組み込まれているツールに関しては、 :doc:`../firstStep_appendix/firststep_complement` を参照すること。
