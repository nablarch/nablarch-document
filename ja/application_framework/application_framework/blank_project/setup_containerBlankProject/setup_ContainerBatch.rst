----------------------------------------------------------
コンテナ用Nablarchバッチプロジェクトの初期セットアップ
----------------------------------------------------------

コンテナ用Nablarchバッチプロジェクトの初期セットアップでは以下を行う。

* コンテナ用Nablarchバッチプロジェクトの生成
* コンテナ用Nablarchバッチプロジェクトの動作確認
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


.. _firstStepGenerateContainerBatchBlankProject:

ブランクプロジェクト作成
----------------------------------------------------------

Nablarchが提供するアーキタイプを使用してブランクプロジェクトを生成する。

mvnコマンドの実行
~~~~~~~~~~~~~~~~~

`Maven Archetype Plugin(外部サイト、英語) <https://maven.apache.org/archetype/maven-archetype-plugin/usage.html>`_ を使用して、ブランクプロジェクトを生成する。

カレントディレクトリを、ブランクプロジェクトを作成したいディレクトリ(任意のディレクトリで可)に変更する。

その後、以下のコマンドを実行する。

.. code-block:: bat

  mvn archetype:generate -DarchetypeGroupId=com.nablarch.archetype -DarchetypeArtifactId=nablarch-container-batch-archetype -DarchetypeVersion={nablarch_version}

上記コマンドで使用されているnablarchのバージョンは |nablarch_version| となっている。バージョンを変更したい場合は、以下のパラメータを変更すること。

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
artifactId   アーティファクトID                       ``myapp-container-batch``
version      バージョン番号                           ``0.1.0``
package      パッケージ(通常はグループIDと同じ)       ``com.example``
=========== ========================================= =======================

.. important::
   項目groupIdおよびpackageは、Javaのパッケージ名にマッピングされる。
   よって、これらの入力値には、英小文字、数字、ドットを使用し、ハイフンは使用しないこと。

コマンドが正常終了した場合、ブランクプロジェクトがカレントディレクトリ配下に作成される。

プロジェクト情報の入力が終わると、Y: :と表示される。

 * 入力した内容をもとに、ひな形を生成する場合には「Y」を入力してください。
 * プロジェクト情報の入力をやり直したい場合には「N」を入力してください。

.. _firstStepContainerBatchStartupTest:

疎通確認
-------------------------

疎通確認の仕組みや手順は通常のNablarchバッチプロジェクトと同じなので、 :ref:`Nablarchバッチプロジェクトの初期セットアップ手順 <firstStepBatchStartupTest>` を参照。

.. note::

  アーティファクトID が ``myapp-container-batch`` になっている点は、適宜読み替えてディレクトリやコマンドを指定すること。


.. _firstStepBuildContainerBatchDockerImage:

コンテナイメージを作成する
----------------------------------

ブランクプロジェクトには、Dockerコンテナのイメージを作成するために `Jib <https://github.com/GoogleContainerTools/jib/tree/master/jib-maven-plugin>`_ (外部サイト、英語)というプラグインがあらかじめ組み込まれている。

このプラグインの ``jib:dockerBuild`` ゴールを実行することで、コンテナイメージを作成できる。

.. code-block:: text

  cd myapp-container-batch
  mvn compile jib:dockerBuild


実行に成功すると、以下のようなログがコンソールに出力される。

.. code-block:: text

  (中略)
  [INFO] Built image to Docker daemon as myapp-container-batch, myapp-container-batch, myapp-container-batch:0.1.0
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
  myapp-container-batch   0.1.0       1cafd4108237   51 years ago   253MB
  myapp-container-batch   latest      1cafd4108237   51 years ago   253MB

``myapp-container-batch:0.1.0`` と ``myapp-container-batch:latest`` という２つのイメージが登録されていることが分かる。

このように、ブランクプロジェクトでは ``jib:dockerBuild`` を実行すると次の２つのイメージが作成されるように設定されている。

* ``${project.artifactId}:latest``
* ``${project.artifactId}:${project.version}``

また、初期設定ではベースイメージとして `OpenJDK のイメージ <https://hub.docker.com/_/eclipse-temurin>`_ (外部サイト、英語)が使用される。

ベースイメージは ``jib.from.image`` プロパティで変更できる。
例えば、ベースイメージに ``eclipse-temurin:17.0.6_10-jre-jammy`` を使用したい場合は、次のように ``pom.xml`` に記述する。

.. code-block:: xml

  <project>
    <!--省略...-->
    <properties>
      <!--省略...-->
      <jib.from.image>eclipse-temurin:17.0.6_10-jre-jammy</jib.from.image>
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

    <jib.from.image>eclipse-temurin@sha256:7dacdab7c335d90cf4e110f5744ca27d5a3ed87901a7c08022c8c12055438bd2</jib.from.image>

.. _firstStepRunContainerBatchDockerImage:

コンテナイメージを実行する
----------------------------------

作成したコンテナイメージは、次のコマンドで実行できる。

.. _firstStepContainerBatchStartupInnerBatchOndemand:

都度起動バッチ
~~~~~~~~~~~~~~~~~
.. code-block:: text

  cd myapp-container-batch
  docker run --rm -v %CD%\\h2:/h2 -v %CD%\\src\\main\\format:/var/nablarch/format -v %CD%\\work\\output:/var/nablarch/output --name myapp-container-batch myapp-container-batch:latest -diConfig classpath:batch-boot.xml -requestPath SampleBatch -userId batch_user

動作は :ref:`疎通確認(都度起動バッチ)<firstStepBatchStartupTest>` と同じである。
起動に成功すると、:ref:`都度起動バッチアプリケーションの起動 <firstStepBatchExecOnDemandBatch>` と同様なログがコンソールに出力される。

.. _firstStepContainerBatchStartupInnerBatchDbMessaging:

テーブルをキューとして使ったメッセージング
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: text

  cd myapp-container-batch
  docker run -it --rm -v %CD%\\h2:/h2 --name myapp-container-batch myapp-container-batch:latest -diConfig classpath:resident-batch-boot.xml -requestPath SampleResiBatch -userId batch_user

動作は :ref:`疎通確認(テーブルをキューとして使ったメッセージング)<firstStepBatchStartupTestDbMessagingBatch>` と同じである。
起動に成功すると、:ref:`アプリケーションの起動 <firstStepBatchExecDbMessagingBatch>` と同様なログがコンソールに出力される。
待機状態となるので、確認後はctrl+c等で強制終了させる。


補足
--------------------

 コンテナイメージの実行コマンドについて
  * 上記コマンドを実行すると、コンテナが起動し、バッチ処理実行後、コンテナは自動的に終了する。
    また、 ``-rmオプション`` により、コンテナ終了時に、コンテナを自動削除するようにしている。

  * 上記コマンドは、データベースとしてブランクプロジェクトにあらかじめ組み込んでいるSAMPLE.h2.dbを使用する場合の例となっている。
    SAMPLE.h2.dbを使用しない場合は、``%CD%\\h2:/h2`` のボリュームの指定(``-v``)は不要になる。

  * :ref:`都度起動バッチ<firstStepContainerBatchStartupInnerBatchOndemand>` では上記に加えてブランクプロジェクトの ``./work/format`` , ``./work/output`` のディレクトリをコンテナにマウントしている。

  * :ref:`テーブルをキューとして使ったメッセージング<firstStepContainerBatchStartupInnerBatchDbMessaging>` においてもdockerコマンドの ``-itオプション`` は省略できるが、ホスト側からのctrl+cでバッチを強制終了できなくなる。
    その場合は、以下のコマンドにてコンテナを終了させればよい。

     .. code-block:: text

      docker stop myapp-container-batch


 Docker環境について
  Dockerの実行は、Docker Desktopを使用していることを :ref:`前提 <firstStepPreamble>` としている。
  Docker Toolboxを使用している場合は、上記例のボリューム指定ではエラーになる。

  Docker Toolboxを使用している場合、DockerはVirtualBox上のVMで動いている。
  このため、ボリュームのホスト側に指定できるパスは、VM上のパスになる。

  Windowsの場合、デフォルトでは ``C:\Users`` がVM上の ``/c/users`` にマウントされている。
  したがって、Docker Toolboxを使用している場合は、ボリュームの指定を ``-v /c/users/path/to/project/h2:/usr/local/tomcat/h2`` のようにしなければならない。

 H2、ツールについて
  H2のデータの確認方法や、ブランクプロジェクトに組み込まれているツールに関しては、 :doc:`../firstStep_appendix/firststep_complement` を参照すること。

