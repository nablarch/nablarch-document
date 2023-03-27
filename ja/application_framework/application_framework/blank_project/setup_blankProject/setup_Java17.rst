.. _setup_blank_project_for_Java17:

----------------------------------------------------------
Java17で使用する場合のセットアップ方法
----------------------------------------------------------

ブランクプロジェクトをJava17で使用する場合、各ブランクプロジェクトの疎通確認前に以下の手順を行う。

* 依存モジュールの追加
* gsp-dba-maven-pluginがJava17で動くように設定する
* 自動テストで使用するJettyのモジュール変更(ウェブプロジェクト または RESTfulウェブサービスプロジェクトの場合のみ)
* --add-opensオプションの追加（JSR352に準拠したバッチプロジェクトの場合のみ）
* Javaバージョンの変更

依存モジュールの追加
-------------------------------------------------------------

Java 11で、JAXBなど一部のモジュールが標準ライブラリから削除された。
削除されたモジュールは明示的に依存関係に追加する必要がある。
このため、作成したブランクプロジェクトのPOMに以下のモジュールを追加する。

なお、 :ref:`Java 11 の依存モジュールの追加<setup_blank_project_for_Java11_add_dependencies>` とは、以下2点の違いがある。

* ``jaxb-impl`` のバージョンに ``2.3.5`` を指定する

  * Java 17 で強化されたカプセル化への対応が、このバージョンでは入っているため

* ``jaxb-api`` のアーティファクトを外す

  * ``jaxb-impl`` の ``2.3.5`` が、 ``jakarta.xml.bind-api`` という別のアーティファクトを推移的に使用するため

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
      <groupId>com.sun.xml.bind</groupId>
      <artifactId>jaxb-core</artifactId>
      <version>2.3.0</version>
    </dependency>
    <dependency>
      <groupId>com.sun.xml.bind</groupId>
      <artifactId>jaxb-impl</artifactId>
      <version>2.3.5</version>
    </dependency>
    <dependency>
      <groupId>javax.annotation</groupId>
      <artifactId>javax.annotation-api</artifactId>
      <version>1.3.2</version>
    </dependency>
  </dependencies>


gsp-dba-maven-pluginがJava17で動くように設定する
----------------------------------------------------------

以下を参照して設定する。

`Java 17 での設定 <https://github.com/coastland/gsp-dba-maven-plugin#java17%E3%81%A7%E3%81%AE%E8%A8%AD%E5%AE%9A>`_ (外部サイト)

.. _setup_java17_jetty9:

自動テストで使用するJettyのモジュール変更(ウェブプロジェクト または RESTfulウェブサービスプロジェクトの場合のみ)
------------------------------------------------------------------------------------------------------------------

ブランクプロジェクトのデフォルトで設定されているJettyのバージョンはJava17に対応していない。
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


--add-opensオプションの追加（JSR352に準拠したバッチプロジェクトの場合のみ）
------------------------------------------------------------------------------------------------------------------

Java 17でカプセル化が強化され、デフォルトでは標準APIなど内部APIをリフレクションで使用できなくなった。
この変更に対する正規の対応は、代替APIへの移行となる。しかし、JSR352に準拠したバッチプロジェクトで使用しているJSR352の実装であるjBeretにはこの対応が入っていない。

このため、Java 17でもJSR352に準拠したバッチプロジェクトを動かすためには、以下のJVMオプションを設定して内部APIをリフレクションで使用できるようにする必要がある。

* ``--add-opens java.base/java.lang=ALL-UNNAMED``
* ``--add-opens java.base/java.security=ALL-UNNAMED``

.. tip::
  このJVMオプションの指定は、jBeretを組み込んでいるWildFlyでも使用されている方法になる。
  
  * `Running WildFly with SE 17 (外部サイト、英語) <https://www.wildfly.org/news/2021/12/16/WildFly26-Final-Released/#running-wildfly-with-se-17>`_

以下に、オプションを指定した場合のコマンドの例を記載する。

.. code-block:: batch

  > java --add-opens java.base/java.lang=ALL-UNNAMED ^
         --add-opens java.base/java.security=ALL-UNNAMED ^
         -jar target\myapp-batch-ee-0.1.0\myapp-batch-ee-0.1.0.jar ^
         sample-batchlet

.. tip::
  Mavenから実行する場合は、環境変数 `MAVEN_OPTS (外部サイト) <https://maven.apache.org/configure.html#maven_opts-environment-variable>`_ を使うことでJVMオプションを設定できる。

Javaバージョンの変更
-----------------------------

ブランクプロジェクトではソース及びclassファイルが準拠するJavaのバージョンとしてJava8が設定されているため
以下のようにファイルを変更する。

* pom.xml

.. code-block:: xml

    <!-- Javaバージョンの箇所を以下のように変更する-->
    <java.version>17</java.version>

