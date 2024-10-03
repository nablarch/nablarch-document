.. _setup_blank_project_for_Java11:

----------------------------------------------------------
Java11で使用する場合のセットアップ方法
----------------------------------------------------------

ブランクプロジェクトをJava11で使用する場合、各ブランクプロジェクトの疎通確認前に以下の手順を行う。

* 依存モジュールの追加
* gsp-dba-maven-pluginが使用する依存モジュールの追加
* 自動テストで使用するJettyのモジュール変更(ウェブプロジェクト または RESTfulウェブサービスプロジェクトの場合のみ)
* Javaバージョンの変更

.. tip::
   コンテナ用のブランクプロジェクトはJava11を前提としており、本章で説明している修正があらかじめ適用されている。
   したがって、コンテナ用のブランクプロジェクトでは本章の手順は必要ない。

.. _setup_blank_project_for_Java11_add_dependencies:

依存モジュールの追加
-------------------------------------------------------------

Java 11で、JAXBなど一部のモジュールが標準ライブラリから削除された。
削除されたモジュールは明示的に依存関係に追加する必要がある。
このため、作成したブランクプロジェクトのPOMに以下のモジュールを追加する。

.. code-block:: xml

  <dependencies>
    <!-- 中略 -->
    <!-- 以下を追加する。 -->
    <dependency>
      <groupId>com.sun.activation</groupId>
      <artifactId>javax.activation</artifactId>
      <version>1.2.0</version>
    </dependency>
    <dependency>
      <groupId>javax.xml.bind</groupId>
      <artifactId>jaxb-api</artifactId>
      <version>2.3.0</version>
    </dependency>
    <dependency>
      <groupId>com.sun.xml.bind</groupId>
      <artifactId>jaxb-core</artifactId>
      <version>2.3.0</version>
    </dependency>
    <dependency>
      <groupId>com.sun.xml.bind</groupId>
      <artifactId>jaxb-impl</artifactId>
      <version>2.3.0</version>
    </dependency>
    <dependency>
      <groupId>javax.annotation</groupId>
      <artifactId>javax.annotation-api</artifactId>
      <version>1.3.2</version>
    </dependency>
  </dependencies>


gsp-dba-maven-pluginが使用する依存モジュールの追加
----------------------------------------------------------

以下を参照して設定する。

`Java 11 での設定 <https://github.com/coastland/gsp-dba-maven-plugin/tree/4.x.x-main?tab=readme-ov-file#java11%E3%81%A7%E3%81%AE%E8%A8%AD%E5%AE%9A>`_ (外部サイト)

.. _setup_java11_jetty9:

自動テストで使用するJettyのモジュール変更(ウェブプロジェクト または RESTfulウェブサービスプロジェクトの場合のみ)
------------------------------------------------------------------------------------------------------------------

ブランクプロジェクトのデフォルトで設定されているJettyのバージョンはJava11に対応していない。
そのため以下のように2ファイルを変更する。

* pom.xml

.. code-block:: xml

  <!-- nablarch-testing-jetty6の箇所を以下のように変更する -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-testing-jetty9</artifactId>
    <scope>test</scope>
  </dependency>


* src/test/resources/unit-test.xml

.. code-block:: xml

  <!-- HttpServerFactoryJetty6の箇所を以下のように変更する -->
  <component name="httpServerFactory" class="nablarch.fw.web.httpserver.HttpServerFactoryJetty9"/>

Javaバージョンの変更
-----------------------------

ブランクプロジェクトではソース及びclassファイルが準拠するJavaのバージョンとしてJava8が設定されているため
以下のようにファイルを変更する。

* pom.xml

.. code-block:: xml

    <!-- Javaバージョンの箇所を以下のように変更する-->
    <java.version>11</java.version>

