----------------------------------------------------------
コンテナ用ウェブプロジェクトの初期セットアップ
----------------------------------------------------------

コンテナ用ウェブプロジェクトの初期セットアップでは以下を行う。

* コンテナ用ウェブプロジェクトの生成
* コンテナ用ウェブプロジェクトの動作確認
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
  * - 使用DB
    - H2 Databaes Engine(アプリケーションに組み込み)
  * - 組み込まれているアダプタ
    - ルーティングアダプタ(詳細は、 :ref:`router_adaptor` を参照)
  * - 生成するプロジェクトに含まれるもの
    - 生成されたプロジェクトには以下が含まれる。
       
      * Nablarchのウェブアプリケーション用の基本的な設定
      * 疎通確認用ウェブアプリケーション
      * Mavenと連動して動作するツールの初期設定( :ref:`about_maven_parent_module` を参照することによって取り込んでいる)。


他のプロジェクトとの関係、及びディレクトリ構成は、 :doc:`../MavenModuleStructures/index` を参照。


.. _firstStepGenerateContainerWebBlankProject:

ブランクプロジェクト作成
----------------------------------------------------------

Nablarchが提供するアーキタイプを使用してブランクプロジェクトを生成する。

mvnコマンドの実行
~~~~~~~~~~~~~~~~~

`Maven Archetype Plugin(外部サイト、英語) <https://maven.apache.org/archetype/maven-archetype-plugin/usage.html>`_ を使用して、ブランクプロジェクトを生成する。

カレントディレクトリを、ブランクプロジェクトを作成したいディレクトリ(任意のディレクトリで可)に変更し、以下のファイルを配置する。

:download:`バッチファイル <bat/generateContainerWebProject.bat>`

配置後、引数に必要なパラメータを指定しbatファイルを実行する。

generateContainerWebProject.bat |nablarch_version| <<groupId>> <<artifactId>> <<version>> <<package(任意)>>

上記コマンドに設定するパラメータは以下の通り。
なお、nablarchのバージョンを変更したい場合には |nablarch_version| を変更すること。

=========== ========================================= =======================
入力項目    説明                                      設定例
=========== ========================================= =======================
groupId      グループID（通常はパッケージ名を入力）   ``com.example``
artifactId   アーティファクトID                       ``myapp-container-web``
version      バージョン番号                           ``0.1.0``
package      パッケージ(通常はグループIDと同じ)       ``com.example``
=========== ========================================= =======================

.. important::
   項目groupIdおよびpackageは、Javaのパッケージ名にマッピングされる。
   よって、これらの入力値には、英小文字、数字、ドットを使用し、ハイフンは使用しないこと。

コマンドが正常終了した場合、ブランクプロジェクトがカレントディレクトリ配下に作成される。


.. _firstStepContainerWebStartupTest:

疎通確認
-------------------------

疎通確認の仕組みや手順は通常のウェブプロジェクトと同じなので、 :ref:`ウェブプロジェクトの初期セットアップ手順 <firstStepWebStartupTest>` を参照。

.. note::

  アーティファクトID が ``myapp-container-web`` になっている点は、適宜読み替えてディレクトリやコマンドを指定すること。


.. _firstStepBuildContainerWebDockerImage:

コンテナイメージを作成する
----------------------------------

ブランクプロジェクトには、Dockerコンテナのイメージを作成するために `Jib <https://github.com/GoogleContainerTools/jib/tree/master/jib-maven-plugin>`_ (外部サイト、英語)というプラグインがあらかじめ組み込まれている。

このプラグインの ``jib:dockerBuild`` ゴールを実行することで、コンテナイメージを作成できる。

.. code-block:: text

  cd myapp-container-web
  mvn package jib:dockerBuild


実行に成功すると、以下のようなログがコンソールに出力される。

.. code-block:: text

  (中略)
  [INFO] Built image to Docker daemon as myapp-container-web, myapp-container-web, myapp-container-web:0.1.0
  (中略)
  [INFO] Executing tasks:
  [INFO] [==============================] 100.0% complete
  [INFO]
  [INFO] ------------------------------------------------------------------------
  [INFO] BUILD SUCCESS
  [INFO] ------------------------------------------------------------------------
  (以下略)

ビルドされたDockerイメージは、ローカルリポジトリに保存される。
以下のコマンドで、ローカルリポジトリに保存されたイメージを確認できる。

.. code-block:: text

  docker image ls
  REPOSITORY              TAG         IMAGE ID       CREATED        SIZE
  myapp-container-web     0.1.0       dd60cbdc7722   50 years ago   449MB
  myapp-container-web     latest      dd60cbdc7722   50 years ago   449MB

``myapp-container-web:0.1.0`` と ``myapp-container-web:latest`` という２つのイメージが登録されていることが分かる。

このように、ブランクプロジェクトでは ``jib:dockerBuild`` を実行すると次の２つのイメージが作成されるように設定されている。

* ``${project.artifactId}:latest``
* ``${project.artifactId}:${project.version}``

また、初期設定ではベースイメージとして `Tomcat のイメージ <https://hub.docker.com/_/tomcat>`_ (外部サイト、英語)が使用される。

ベースイメージは ``jib.from.image`` プロパティで変更できる。
例えば、ベースイメージに ``tomcat:10.1.28-jre17-temurin-jammy`` を使用したい場合は、次のように ``pom.xml`` に記述する。

.. code-block:: xml

  <project>
    <!--省略...-->
    <properties>
      <!--省略...-->
      <jib.from.image>tomcat:10.1.28-jre17-temurin-jammy</jib.from.image>
      <!--省略...-->
    </properties>
    <!--省略...-->
  </project>

.. tip::

  ブランクプロジェクトではイメージをタグで指定しているが、この場合、指定したイメージの最新バージョンが選択される。
  検証時と異なるバージョンが選択された場合、アプリケーションの動作に影響が出る可能性があるので、
  プロジェクトにおける検証が完了した段階で、バージョンを固定するために、イメージをダイジェストで指定することを推奨する。

  ダイジェストによる設定例を以下に示す。

  .. code-block:: xml

    <jib.from.image>tomcat@sha256:28fde3a9cf9ff62b250cd2ce5b8981a75eedbe6a37a9954c8432f6f52483cfb8</jib.from.image>

.. _firstStepRunContainerWebDockerImage:

コンテナイメージを実行する
----------------------------------

作成したコンテナイメージは、次のコマンドで実行できる。

.. code-block:: text

  cd myapp-container-web
  docker run -d -p 8080:8080 -v %CD%\h2:/usr/local/tomcat/h2 --name myapp-container-web myapp-container-web

コンテナが起動したら、ウェブブラウザで ``http://localhost:8080/`` にアクセスすることで、アプリケーションの動作を確認できる。

.. tip::

  上記コマンドは、データベースとしてブランクプロジェクトにあらかじめ組み込んでいるSAMPLE.h2.dbを使用する場合の例となっている。
  SAMPLE.h2.dbを使用しない場合は、ボリュームの指定(``-v``)は不要になる。

.. tip::

  Dockerの実行は、Docker Desktopを使用していることを :ref:`前提 <firstStepPreamble>` としている。
  Docker Toolboxを使用している場合は、上記例のボリューム指定ではエラーになる。

  Docker Toolboxを使用している場合、DockerはVirtualBox上のVMで動いている。
  このため、ボリュームのホスト側に指定できるパスは、VM上のパスになる。

  Windowsの場合、デフォルトでは ``C:\Users`` がVM上の ``/c/users`` にマウントされている。
  したがって、Docker Toolboxを使用している場合は、ボリュームの指定を ``-v /c/users/path/to/project/h2:/usr/local/tomcat/h2`` のようにしなければならない。

コンテナを終了するには、次のコマンドを実行する。

.. code-block:: text

  docker stop myapp-container-web

また、コンテナを削除するには、次のコマンドを実行する。

.. code-block:: text

  docker rm myapp-container-web


補足
--------------------

H2のデータの確認方法や、ブランクプロジェクトに組み込まれているツールに関しては、 :doc:`../firstStep_appendix/firststep_complement` を参照すること。
