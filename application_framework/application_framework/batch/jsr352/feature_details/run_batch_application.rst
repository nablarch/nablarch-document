
JSR352バッチアプリケーションの起動
==================================================
.. contents:: 目次
  :depth: 3
  :local:

.. _jsr352_run_batch_application:

バッチアプリケーションの起動クラスを作成する
--------------------------------------------------
JSR352に準拠したバッチアプリケーションの場合、バッチの起動はJSR352で規定されたAPIを使用して行う。

以下に起動例を示す。

.. code-block:: java

  public static void main(final String[] args) throws BatchRuntimeException {
    final String jobXml = args[0];

    // BatchRuntimeからJobOperatorを取得し、起動引数で与えられたジョブを実行する。
    final JobOperator jobOperator = BatchRuntime.getJobOperator();
    final long jobExecutionId = jobOperator.start(jobXml, null);

    // バッチの実行が終わるまで待機し、結果を判定するなどを処理をここに実装する。
  }

.. tip::

  `jBeret(外部サイト、英語) <https://jberet.gitbooks.io/jberet-user-guide/content/>`_ を使用した場合、
  ``jberet-se`` モジュールに含まれる起動クラスを使用してバッチアプリケーションを実行できる。

  詳細は、 ``jberet-se`` モジュール内の ``org.jberet.se.Main`` クラスを参照

  ※プロジェクト独自で起動クラスを作成する際にも、上記 ``Main`` クラスを参考にすることができる。

.. _jsr352_run_batch_init_repository:

システムリポジトリを初期化する
--------------------------------------------------
:ref:`repository` は、ジョブリスナーに ``nablarchJobListenerExecutor`` を設定することで初期化できる。

システムリポジトリのルートxmlファイルのファイル名は、 ``batch-boot.xml`` としクラスパス直下に配置する。
ファイル名や、配置場所を変更したい場合には、 ``nablarchJobListenerExecutor`` のパラメータで変更する。

以下に例を示す。

デフォルトの ``batch-boot.xml`` を使用する場合の例
  .. code-block:: xml

    <job id="sample-job" xmlns="http://xmlns.jcp.org/xml/ns/javaee" version="1.0">
      <listeners>
        <!-- ジョブリスナーにnablarchJobListenerExecutorを設定する -->
        <listener ref="nablarchJobListenerExecutor" />
      </listeners>

      <!-- ステップ定義は省略 -->
    </job>

デフォルト以外の設定ファイルを使用する例
  .. code-block:: xml

    <job id="sample-job" xmlns="http://xmlns.jcp.org/xml/ns/javaee" version="1.0">
      <listeners>
        <listener ref="nablarchJobListenerExecutor">
          <properties>
            <!--
            diConfigFilePathプロパティに読み込むxmlを設定する
            この例の場合、クラスパス配下の「sample_project/batch-boot.xml」が
            システムリポジトリにロードされる
            -->
            <property name="diConfigFilePath" value="sample_project/batch-boot.xml" />
          </properties>
        </listener>
      </listeners>

      <!-- ステップ定義は省略 -->
    </job>
