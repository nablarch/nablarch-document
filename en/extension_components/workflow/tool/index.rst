.. _workflow_tool:

ワークフロー定義データ生成ツール
==================================================
.. contents:: 目次
  :depth: 3
  :local:
  
本ツールは、BPMN2.0に準拠したワークフロー定義ファイル(xmlファイル)を読み込み、 :ref:`ワークフロー関連テーブル <workflow-table_definition>` に投入用のCSVファイルを出力するMavenプラグインである。
CSVファイルの出力時には、ワークフロー定義ファイルの内容が、 :ref:`workflow` で利用できるかのバリデーションも行う。

モジュール一覧
--------------------------------------------------
プラグインに対する設定値の詳細は、 :ref:`workflow_tool-plugin_configuration` を参照。

.. code-block:: xml

  <plugin>
    <groupId>com.nablarch.workflow</groupId>
    <artifactId>nablarch-workflow-tool</artifactId>
  </plugin>

使用方法
--------------------------------------------------

.. _workflow_tool-plugin_configuration:

プラグインに対する設定を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
本プラグインを使用するためには、幾つかの設定を行う必要がある。
以下に設定値の詳細を及び設定例を示す。

outputPath
  CSVの出力先ディレクトリ
  
workflowBpmnDir
  ワークフロー用のワークフロー定義ファイルの配置ディレクトリ
  
  本ディレクトリ配下のワークフロー定義(拡張子が ``bpmn`` のファイル)が自動的に読み込まれ、CSVに出力される。
  
stateMachineBpmnDir
  ステートマシン用のワークフロー定義ファイルの配置ディレクトリ
  
  本ディレクトリ配下のステートマシン定義(拡張子が ``bpmn`` のファイル)が自動的に読み込まれ、CSVに出力される。
  
configurationFilePath
  テーブル名やカラム名を定義したコンポーネント設定ファイルのパス

設定例
  .. code-block:: xml
  
    <plugin>
      <groupId>com.nablarch.workflow</groupId>
      <artifactId>nablarch-workflow-tool</artifactId>
      <version>1.1.0</version>
      <configuration>
        <!-- CSV出力先ディレクトリ -->
        <outputPath>src/test/resources/data</outputPath>
        <!-- テーブル名やカラム名を定義したコンポーネント設定ファイル -->
        <configurationFilePath>src/design/workflow-tool.xml</configurationFilePath>
        <!-- ワークフローのワークフロー定義ファイルの配置ディレクトリ -->
        <workflowBpmnDir>src/design/workflow</workflowBpmnDir>
        <!-- ステートマシンのワークフロー定義ファイルの配置ディレクトリ -->
        <stateMachineBpmnDir>src/design/statemachine</stateMachineBpmnDir>
      </configuration>
    </plugin>

プラグインを実行する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
本プラグインのゴールである ``generate-csv`` を実行することで、設定に従いCSVファイルが出力される。
なお、以下の定義例のようにMavenのビルドプロセス内に組み込むことで、ビルド時に自動的にCSVファイルが生成されるようになる。

.. code-block:: xml

  <plugin>
    <groupId>com.nablarch.workflow</groupId>
    <artifactId>nablarch-workflow-tool</artifactId>
    <version>1.1.0</version>
    
    <executions>
      <execution>
        <id>generate-csv</id>
        <phase>generate-resources</phase>
        <goals>
          <goal>generate-csv</goal>
        </goals>
        <configuration>
          <!-- 設定値は省略 -->
        </configuration>
      </execution>
    </executions>
  </plugin>

バリデーション内容
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
本ツールでは、 :ref:`workflow` が想定している要素のみを使用しているかや、各要素がシーケンスフローでつながっているかなどの簡易的なバリデーションを行う。

バリデーション内容は以下の通り

* 想定している要素のみを使用しているか

  * プール
  * レーン
  * ユーザタスク(ワークフローの場合)
  * タスク(ステートマシンの場合)
  * XORゲートウェイ
  * 開始イベント
  * 停止イベント
  * 中断メッセージ境界イベント
  * シーケンスフロー
* 遷移可能な要素となっているか
* 開始イベントから始まり停止イベントで終了できるか

バリデーションエラーがある場合は、エラー内容を標準エラー出力に出力する。

エラーの出力例
  .. code-block:: text

    [ERROR] sm1_ステートマシン_ver1_20170101.bpmn
    [ERROR] 	境界イベントに遷移先が設定されていません。 id:manual_sinsa_message, name:null
    [ERROR] wf1_ワークフロー_ver1_20170101.bpmn
    [ERROR] 	ゲートウェイから伸びるシーケンスフローの場合、フロー進行条件は必須です。[条件]を設定してください。 id = [SequenceFlow_06] name = [確認OK]
    [ERROR] 	サポート対象外の要素です。 id = [T001] name = [確認]


Java11で使用する場合の設定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. important::

  本プラグインをJava11で使用する場合は、Mavenのバージョンを3.6.1以上にする必要がある。

本プラグインをJava11で使用するためには、以下の設定をします。

.. code-block:: xml

  <plugin>
    <groupId>com.nablarch.workflow</groupId>
    <artifactId>nablarch-workflow-tool</artifactId>
    <version>1.1.0</version>
    <!-- 中略 -->
    <dependencies>
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
    </dependencies>
  </plugin>
