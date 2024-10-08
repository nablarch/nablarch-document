----------------------------------------------------------
ウェブプロジェクトの初期セットアップ
----------------------------------------------------------

ウェブプロジェクトの初期セットアップでは以下を行う。

* ウェブプロジェクトの生成
* ウェブプロジェクトの動作確認


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


.. _firstStepGenerateWebBlankProject:

ブランクプロジェクト作成
----------------------------------------------------------

Nablarchが提供するアーキタイプを使用してブランクプロジェクトを生成する。

mvnコマンドの実行
~~~~~~~~~~~~~~~~~

`Maven Archetype Plugin(外部サイト、英語) <https://maven.apache.org/archetype/maven-archetype-plugin/usage.html>`_ を使用して、ブランクプロジェクトを生成する。

カレントディレクトリを、ブランクプロジェクトを作成したいディレクトリ(任意のディレクトリで可)に変更する。

その後、以下のコマンドを実行する。

.. code-block:: bat

  mvn archetype:generate -DarchetypeGroupId=com.nablarch.archetype -DarchetypeArtifactId=nablarch-web-archetype -DarchetypeVersion={nablarch_version}

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
artifactId   アーティファクトID                       ``myapp-web``
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


.. _firstStepWebStartupTest:

疎通確認
-------------------------

自動テスト
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

アーキタイプから生成したプロジェクトには、以下のユニットテストが含まれている。

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 9,20

  * - ユニットテストのクラス
    - テスト内容
  * - SampleActionRequestTest
    - Nablarchのテスティングフレームワークを使用して、画面が表示可能であるかを確認する。



ユニットテストを実行することで、ブランクプロジェクトの生成に成功していることを確認する。


以下のコマンドを実行する。

.. code-block:: text

  cd myapp-web
  mvn test

.. tip::

  ここで使用しているMavenの「clean」「test」は、MavenのBuilt-in Lifecycleである。
  
  他にどのようなLifecycleが存在するかについては、 `Built-in Lifecycle Bindings(外部サイト、英語) <https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html#Built-in_Lifecycle_Bindings>`_  を参照。


実行に成功すると、以下のようなログがコンソールに出力される。

.. code-block:: text

  (中略)
  [INFO] -----------------------< com.example:myapp-web >------------------------
  [INFO] Building myapp-web 0.1.0
  [INFO] --------------------------------[ war ]---------------------------------
  (中略)
  [INFO] Results:
  [INFO]
  [INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0
  [INFO]
  [INFO] ------------------------------------------------------------------------
  [INFO] BUILD SUCCESS
  [INFO] ------------------------------------------------------------------------
  (以下略)


起動確認
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

生成したプロジェクトには、以下の画面が含まれている。

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 9,20

  * - 画面表示に使用するクラス
    - 内容
  * - SampleAction
    - ウェブアプリケーション実装する際に一般的に使用するNablarchの機能についての動作確認。

ブラウザで画面を表示することで、ブランクプロジェクトの生成に成功していることを確認する。

まだ、生成したプロジェクトにカレントディレクトリを移動していない場合は移動する。

.. code-block:: text

  cd myapp-web

その後、以下のコマンドを実行することで、疎通確認用のアプリケーションをビルドしてから起動する。

.. code-block:: text

  mvn jetty:run

.. tip::

  上記のコマンド例で使用しているMavenの「jetty:run」は、 Jetty Maven Pluginのrunゴールを使用するという指定である。
  アプリケーションのビルドを行うcompileゴールは「jetty:run」で合わせて実行されるため、明示的に実行する必要はない。
  
  Jetty Maven Pluginについては `Jetty Maven Plugin(外部サイト、英語) <https://jetty.org/docs/jetty/12/programming-guide/maven-jetty/jetty-maven-plugin.html>`_  を参照。

起動に成功するとコンソールに以下のようなログが出力される。

.. code-block:: text

  (中略)
  2023-03-30 10:04:42.148 -INFO- nablarch.fw.web.servlet.NablarchServletContextListener [null] boot_proc = [] proc_sys = [web] req_id = [null] usr_id = [null] [nablarch.fw.web.servlet.NablarchServletContextListener#contextInitialized] initialization completed.

起動に成功したらブラウザで ``http://localhost:9080/`` にアクセスし、疎通確認画面を開く。
表示されたページの内容を読み、成功していることを確認する。

また、ログを確認しエラーが出ていないことを確認する。


疎通確認になぜか失敗する場合
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

原因は分からないが疎通確認に失敗する場合、どこかで手順を誤っている可能性がある。

原因が分からない場合は、:ref:`firstStepGenerateWebBlankProject` からやり直してみること。

データベースに関する設定を行う
------------------------------------

ブランクプロジェクトは、初期状態ではH2 Database Engineを使用するように設定されている。使用するRDBMSを変更する場合は、:ref:`customize-db` を参照して設定すること。

またER図からのDDL生成や実行、Entityクラスの自動生成を行うにはgsp-dba-maven-pluginの初期設定および実行を行う。詳細は :ref:`gsp-maven-plugin` を参照。

補足（web.xml）
--------------------

JNDI経由で接続を取得させる場合、web.xmlに<resource-ref>要素を定義する必要があるが、
管理を容易にするため、web.xmlは、環境別にわけず、共用するようにしている。

本番環境のみJNDI経由で接続を取得する場合、<resource-ref>要素の定義はローカルＰＣの開発環境向けの設定としては不要なものとなるが、
アプリケーション内でその定義を使用するコードを書かない限り、<resource-ref>要素は使用されない。
よって、ローカルＰＣの開発環境内でのアプリケーションの動作において問題は発生しない。

補足
--------------------

H2のデータの確認方法や、ブランクプロジェクトに組み込まれているツールに関しては、 :doc:`../firstStep_appendix/firststep_complement` を参照すること。
