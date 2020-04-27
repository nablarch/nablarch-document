----------------------------------------------------------
RESTfulウェブサービスプロジェクトの初期セットアップ
----------------------------------------------------------

RESTfulウェブサービスプロジェクトの初期セットアップでは以下を行う。

* RESTfulウェブサービスプロジェクトの生成
* RESTfulウェブサービスプロジェクトの動作確認


事前準備
-------------------------------------------------------------

後の :ref:`setup_webService_startup_test` で使用するため、以下のいずれかをインストールする。

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


.. _firstStepGenerateJaxrsBlankProject:

ブランクプロジェクト作成
----------------------------------------------------------

Nablarchが提供するアーキタイプを使用してブランクプロジェクトを生成する。


~~~~~~~~~~~~~~~~~
mvnコマンドの実行
~~~~~~~~~~~~~~~~~

`Maven Archetype Plugin(外部サイト、英語) <https://maven.apache.org/archetype/maven-archetype-plugin/usage.html>`_ を使用して、ブランクプロジェクトを生成する。

カレントディレクトリを、ブランクプロジェクトを作成したいディレクトリ(任意のディレクトリで可)に変更し、以下のファイルを配置する。

:download:`バッチファイル <bat/generateWebServiceProject.bat>`

配置後、引数に必要なパラメータを指定しbatファイルを実行する。

generateWebServiceProject.bat |nablarch_version| <<groupId>> <<artifactId>> <<version>> <<package(任意)>>

上記コマンドに設定するパラメータは以下の通り。
なお、nablarchのバージョンを変更したい場合には |nablarch_version| を変更すること。

=========== ========================================= =======================
入力項目    説明                                      設定例
=========== ========================================= =======================
groupId      グループID（通常はパッケージ名を入力）   ``com.example``
artifactId   アーティファクトID                       ``myapp-jaxrs``
version      バージョン番号                           ``0.1.0``
package      パッケージ(通常はグループIDと同じ)       ``com.example``
=========== ========================================= =======================

.. important::
   項目groupIdおよびpackageは、Javaのパッケージ名にマッピングされる。
   よって、これらの入力値には、英小文字、数字、ドットを使用し、ハイフンは使用しないこと。


コマンドが正常終了した場合、ブランクプロジェクトがカレントディレクトリ配下に作成される。


.. _firstStepWebServiceStartupTest:

疎通確認
-------------------------------------------

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
自動テスト
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

アーキタイプから生成したプロジェクトには、以下のユニットテストが含まれている。

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 12,20

  * - ユニットテストのクラス
    - テスト内容
  * - SampleActionTest
    - DBアクセスを伴うテストが可能かを確認する。



ユニットテストを実行することで、ブランクプロジェクトの生成に成功していることを確認する。


以下のコマンドを実行する。

.. code-block:: text

  cd myapp-jaxrs
  mvn test

.. tip::

  ここで使用しているMavenの「clean」「test」は、MavenのBuilt-in Lifecycleである。
  
  他にどのようなLifecycleが存在するかについては、 `Built-in Lifecycle Bindings(外部サイト、英語) <https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html#Built-in_Lifecycle_Bindings>`_  を参照。


実行に成功すると、以下のようなログがコンソールに出力される。

.. code-block:: text

  (中略)
  [INFO] ------------------------------------------------------------------------
  [INFO] Building myapp-jaxrs 0.1.0
  [INFO] ------------------------------------------------------------------------
  (中略)
  Tests run: 2, Failures: 0, Errors: 0, Skipped: 0

  [INFO] ------------------------------------------------------------------------
  [INFO] BUILD SUCCESS
  [INFO] ------------------------------------------------------------------------
  (以下略)


.. _setup_webService_startup_test:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
起動確認
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

生成したプロジェクトには、以下のサービスが含まれている。

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 10,20

  * - サービスを実装しているクラス
    - 内容
  * - SampleAction
    - RESTfulウェブサービスを実装する際に、一般的に使用するNablarchの機能についての動作確認用サービス。
      
      応答にJSONを使用するサービスと、XMLを使用するサービスが存在する。

ブラウザからサービスを呼び出すことによって、ブランクプロジェクトの生成に成功していることを確認する。


サービスの起動
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

まだ、生成したプロジェクトにカレントディレクトリを移動していない場合は移動する。

.. code-block:: text

  cd myapp-jaxrs

次に、以下のコマンドを実行し、RESTfulウェブサービスをビルドする。

.. code-block:: text

  mvn compile


その後、以下のコマンドを実行することで、RESTfulウェブサービスの疎通確認用のアプリケーションを起動する。

.. code-block:: text

  mvn waitt:run-headless

.. tip::

  上記のコマンド例で使用しているMavenの「waitt:run-headless」は、 waitt maven pluginのrun-headlessゴールを使用するという指定である。
  
  waitt maven pluginについては `waitt maven plugin(外部サイト、英語) <https://github.com/kawasima/waitt>`_  を参照。


起動に成功するとコンソールに以下のようなログが出力される。

.. code-block:: text

  (中略)
  2020-03-25 18:24:37.049 -INFO- nablarch.fw.web.servlet.NablarchServletContextListener [null] boot_proc = [] proc_sys = [] req_id = [null] usr_id = [null] [nablarch.fw.web.servlet.NablarchServletContextListener#contextInitialized] initialization completed.


応答にJSONを使用するサービスを呼び出す
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

FireFoxまたはChromeを起動し、以下のURLをアドレスバーに入力する。


.. code-block:: text

  http://localhost:9080/find/json (左記の通り末尾に「/」は不要)


成功するとブラウザに以下のようにJSON形式の応答が表示される。

.. code-block:: text

  [{"userId":1,"kanjiName":"名部楽太郎","kanaName":"なぶらくたろう"},{"userId":2,"kanjiName":"名部楽次郎","kanaName":"なぶらくじろう"}]


.. tip::

  FireFoxまたはChromeの代わりにInternet Explorer 11を使用すると、ダウンロードするか否かの確認メッセージが表示される。


応答にXMLを使用するサービスを呼び出す
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

FireFoxまたはChromeを起動し、以下のURLをアドレスバーに入力する。


.. code-block:: text

  http://localhost:9080/find/xml (左記の通り末尾に「/」は不要)


成功するとブラウザに以下のようにXML形式の応答が表示される。

.. code-block:: xml

  <userList>
    <sampleUser>
      <kanaName>なぶらくたろう</kanaName>
      <kanjiName>名部楽太郎</kanjiName>
      <userId>1</userId>
    </sampleUser>
    <sampleUser>
      <kanaName>なぶらくじろう</kanaName>
      <kanjiName>名部楽次郎</kanjiName>
      <userId>2</userId>
    </sampleUser>
  </userList>


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
疎通確認になぜか失敗する場合
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

原因は分からないが疎通確認に失敗する場合、どこかで手順を誤っている可能性がある。

原因が分からない場合は、:ref:`firstStepGenerateJaxrsBlankProject` からやり直してみること。



補足
--------------------

H2のデータの確認方法や、ブランクプロジェクトに組み込まれているツールに関しては、 :doc:`../firstStep_appendix/firststep_complement` を参照すること。
