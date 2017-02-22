JSR352バッチアプリケーションの起動
==================================================
.. contents:: 目次
  :depth: 3
  :local:

.. _jsr352_run_batch_application:

バッチアプリケーションを起動する
--------------------------------------------------
JSR352に準拠したバッチアプリケーションの場合、バッチの起動はJSR352で規定されたAPIを使用して行う。

Nablarchでは、標準の実装クラスとして、:java:extdoc:`nablarch.fw.batch.ee.Main` を提供している。
このクラスは実行引数として対象JOBのXMLファイル名(.xmlを除いたファイル名)を指定する。

プロジェクト独自で起動クラスを作成する際にも、このMainクラスを参考に実装することができる。


.. _jsr352_exitcode_batch_application:

バッチアプリケーションの終了コード
--------------------------------------------------
上記のMainクラスのプログラムの終了コードは以下のようになる。

* 正常終了：0 - 終了ステータスが “WARNING” 以外の場合で、バッチステータスが  :java:extdoc:`BatchStatus.COMPLETED <javax.batch.runtime.BatchStatus>` の場合
* 異常終了：1 - 終了ステータスが “WARNING” 以外の場合で、バッチステータスが  :java:extdoc:`BatchStatus.COMPLETED <javax.batch.runtime.BatchStatus>` 以外の場合
* 警告終了：2 - 終了ステータスが “WARNING” の場合

なお、JOBの終了待ちの間に中断された場合は、異常終了のコードを返す。

バリデーションエラーなど警告すべき事項が発生している場合に、警告終了させることができる。
警告終了の方法はchunkまたはbatchlet内で、 :java:extdoc:`JobContext#setExitStatus(String) <javax.batch.runtime.context.JobContext.setExitStatus(java.lang.String)>`
を呼び出し "WARNING" を終了ステータスとして設定する。警告終了時は、バッチステータスは任意の値を許可するため、chunkまたはbatchlet内で、
例外を送出しバッチステータスが :java:extdoc:`BatchStatus.COMPLETED <javax.batch.runtime.BatchStatus>` 以外となる場合であっても、
終了ステータスに "WARNING" を設定していれば、上記クラスは警告終了する。

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
