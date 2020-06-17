=================================
準備
=================================

モジュール一覧
--------------------------------------------------
.. code-block:: xml

    <!--  テスティングフレームワーク本体  -->
    <dependency>
      <groupId>com.nablarch.framework</groupId>
      <artifactId>nablarch-testing-rest</artifactId>
      <scope>test</scope>
    </dependency>
    <!--  テスティングフレームワークで使用するデフォルト設定  -->
    <dependency>
      <groupId>com.nablarch.configuration</groupId>
      <artifactId>nablarch-testing-default-configuration</artifactId>
      <scope>test</scope>
    </dependency>
    <!--  テスティングフレームワークで使用する内蔵サーバの実装  -->
    <dependency>
      <groupId>com.nablarch.framework</groupId>
      <artifactId>nablarch-testing-jetty6</artifactId>
      <scope>test</scope>
    </dependency>


.. important::
   ``nablarch-testing-rest`` は ``nablarch-testing`` (:ref:`大規模開発向け重厚なテスティングフレームワーク <unitTestGuide>`) に依存している。
   上記のモジュールを依存に追加することで :ref:`大規模開発向け重厚なテスティングフレームワーク <unitTestGuide>` のAPIを使用することができる。
   既に ``nablarch-testing`` が pom.xml に記載されている場合は重複するため、 ``nablarch-testing-rest`` だけが pom.xml に記載されるよう
   ``nablarch-testing`` を削除してください。

.. tip::
  Java11を使用している場合は :ref:`自動テストで使用するJettyのモジュール変更 <setup_java11_jetty9>` の通り
  内蔵サーバの差し替えが必要となる。

設定
---------------

アーキタイプからブランクプロジェクトを作成した場合、 ``src/test/resources/unit-test.xml`` に
テスティングフレームワークの設定がされている。RESTfulウェブサービス向けテスティングフレームワークの
設定を追加するためデフォルト設定で提供している以下の設定ファイルを読み込む。

.. code-block:: xml

    <import file="nablarch/test/rest-request-test.xml"/>

リクエスト単体テストの設定は :ref:`rest-test-configuration` を参照。

.. tip::
  Nablarch5u18以降のアーキタイプからブランクプロジェクトを作成した場合
  :doc:`RESTfulウェブサービス <../../../application_framework/application_framework/blank_project/setup_blankProject/setup_WebService>` では
  上記が既に設定されている。:doc:`ウェブプロジェクト <../../../application_framework/application_framework/blank_project/setup_blankProject/setup_Web>` や
  :doc:`バッチプロジェクト <../../../application_framework/application_framework/blank_project/setup_blankProject/setup_NablarchBatch>` では追加が必要となる。
