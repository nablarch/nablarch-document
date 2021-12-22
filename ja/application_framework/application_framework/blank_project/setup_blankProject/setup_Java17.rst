.. _setup_blank_project_for_Java17:

----------------------------------------------------------
Java17で使用する場合のセットアップ方法
----------------------------------------------------------

ブランクプロジェクトをJava17で使用する場合、各ブランクプロジェクトの疎通確認前に以下の手順を行う。

* 依存モジュールの追加
* gsp-dba-maven-pluginがJava17で動くように設定する
* 自動テストで使用するJettyのモジュール変更(ウェブプロジェクト または RESTfulウェブサービスプロジェクトの場合のみ)
* --add-opensオプションの追加（JSR352に準拠したバッチプロジェクトの場合のみ）

依存モジュールの追加
-------------------------------------------------------------

作成したブランクプロジェクトのPOMに以下のモジュールを追加する。

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
対応内容自体はJava11の場合と同じであるため、詳細な手順については :ref:`Java11の説明 <setup_java11_jetty9>` を参照。


--add-opensオプションの追加（JSR352に準拠したバッチプロジェクトの場合のみ）
------------------------------------------------------------------------------------------------------------------

JSR352に準拠したバッチプロジェクトを動かす際は、以下のJVMオプションを設定する必要がある。

* ``--add-opens java.base/java.lang=ALL-UNNAMED``
* ``--add-opens java.base/java.security=ALL-UNNAMED``

以下に、オプションを指定した場合のコマンドの例を記載する。

.. code-block:: batch

  > java --add-opens java.base/java.lang=ALL-UNNAMED ^
         --add-opens java.base/java.security=ALL-UNNAMED ^
         -jar target\myapp-batch-ee-0.1.0\myapp-batch-ee-0.1.0.jar ^
         sample-batchlet

.. tip::
  Mavenから実行する場合は、環境変数 ``MAVEN_OPTS`` を使うことでJVMオプションを設定できる。
