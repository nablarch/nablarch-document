.. _docker_container:

Azureにおける分散トレーシング
=========================================

本章では、Azure上で分散トレーシングを行う方法について説明する。

.. _how_to_enable_distributed_tracing:

Azureで分散トレーシングを行う方法
--------------------------------------------------------------------------------------------------

  Azureでは、 ``Azure Application Insights`` を使用して分散トレーシングを行う。

  * `Azure Application Insights における分散トレース(外部サイト) <https://docs.microsoft.com/ja-jp/azure/azure-monitor/app/distributed-tracing>`_

  Javaアプリケーションから分散トレーシングを有効化するための仕組みとして、Javaエージェントを用いた方法(**Java 3.0 エージェント**)が提供されている。

  * `Azure Monitor Application Insights を監視する Java のコード不要のアプリケーション(外部サイト) <https://docs.microsoft.com/ja-jp/azure/azure-monitor/app/java-in-process-agent>`_

  .. important::
    Java 3.0 エージェントは、初期化処理中に大量のjarファイルをロードする。
    これにより、Java 3.0 エージェントの初期化処理中はGCが頻発することがある。

    このため、アプリケーション起動後しばらくは、GCの影響により性能が一時的に劣化する可能性がある点に注意すること。

  以下に、コンテナ用のアーキタイプを使用した場合の例を示す。

  まず、 `Azureの公式サイト <https://docs.microsoft.com/ja-jp/azure/azure-monitor/app/java-in-process-agent#quickstart>`_  よりエージェントをダウンロードする。
  その後、``src/main/jib`` 以下に任意のディレクトリを作成し、エージェントを格納する。

  次に、 ``pom.xml`` の ``jib-maven-plugin`` に 環境変数として ``CATALINA_OPTS`` を追加する。
  設定内容は、先程配置したエージェントを指定する。
  （例では ``applicationInsights`` ディレクトリ直下に配置した ``applicationinsights-agent-3.0.2.jar`` を指定している）

  * pom.xml

  .. code-block:: xml

    <!-- Dockerコンテナ化 -->
    <plugin>
        <groupId>com.google.cloud.tools</groupId>
        <artifactId>jib-maven-plugin</artifactId>
        <configuration>
            <container>
                <appRoot>/usr/local/tomcat/webapps/ROOT</appRoot>
                <ports>
                    <port>8080</port>
                </ports>
                <environment>
                    <CATALINA_OPTS>-javaagent:/applicationInsights/applicationinsights-agent-3.0.2.jar</CATALINA_OPTS>
                </environment>
            </container>
        </configuration>
    </plugin>


これでJibを使用してビルドすることにより、 ``Azure Application Insights`` を使用して分散トレーシングを行うことができる。

詳細な設定方法については、 `Azureのドキュメント <https://docs.microsoft.com/ja-jp/azure/azure-monitor/app/java-in-process-agent#quickstart>`_ を参照のこと。
