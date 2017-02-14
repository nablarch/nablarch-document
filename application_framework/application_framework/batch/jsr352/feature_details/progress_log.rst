進捗状況のログ出力
==================================================
.. contents:: 目次
  :depth: 3
  :local:
  
.. _jsr352-progress_log:

進捗ログで出力される内容
--------------------------------------------------
以下の内容をログに出力する。

* ジョブの開始と終了ログ
* ステップの開始と終了ログ
* 処理対象の件数ログ(処理対象の件数は、アプリケーション側で求める必要がある)
* ステップの進捗状況ログ

  * TPS(処理対象の件数及び処理済み件数から算出したTPS)
  * 未処理件数
  * 終了予測時間(未処理件数とTPSから求めたステップの終了予測時間)
  
以下に出力例を示す。

.. code-block:: bash

  INFO progress start job. job name: [test-job]
  INFO progress start step. job name: [test-job] step name: [test-step]
  INFO progress job name: [test-job] step name: [test-step] input count: [25]
  INFO progress job name: [test-job] step name: [test-step] tps: [250.00] estimated end time: [2017/02/13 04:02:25.656] remaining count: [15]
  INFO progress job name: [test-job] step name: [test-step] tps: [384.62] estimated end time: [2017/02/13 04:02:25.668] remaining count: [5]
  INFO progress job name: [test-job] step name: [test-step] tps: [409.84] estimated end time: [2017/02/13 04:02:25.677] remaining count: [0]
  INFO progress finish step. job name: [test-job] step name: [test-step] step status: [null]
  INFO progress finish job. job name: [test-job]

進捗ログを専用のログファイルに出力するための設定を追加する
-----------------------------------------------------------------
進捗を示すログは、ログカテゴリ名を ``progress`` として出力する。
このカテゴリ名を使用して、進捗ログ用のファイルにログを出力することが出来る。

:ref:`log` を使用した場合の ``log.properties`` の設定例を以下に示す。
:ref:`log_adaptor` を使用している場合には、アダプタに対応したログライブラリのマニュアルなどを参照し設定を行うこと。

.. code-block:: properties

  # progress log file
  writer.progressLog.className=nablarch.core.log.basic.FileLogWriter
  writer.progressLog.filePath=./log/progress.log
  writer.progressLog.encoding=UTF-8
  writer.progressLog.formatter.className=nablarch.core.log.basic.BasicLogFormatter
  writer.progressLog.formatter.format=$date$ -$logLevel$- $message$
  
  # logger list
  availableLoggersNamesOrder=SQL,MON,PROGRESS,ROO
  
  # progress logger setting
  loggers.PROGRESS.nameRegex=progress
  loggers.PROGRESS.level=INFO
  loggers.PROGRESS.writerNames=progressLog

Batchletステップで進捗ログを出力する
--------------------------------------------------
Batchletステップで進捗状況をログに出力するための実装例を以下に示す。

なお、Batchletは基本的にはタスク指向の処理を実行するため進捗ログを必要とするケースは少ない。
Batchletで、ループを伴う処理を行う必要がある場合には、下の実装例を元に進捗ログを出力すると良い。

ポイント
  * processメソッドの先頭で、処理対象件数(データベースへのcount結果やファイルのレコード数等)を取得し、 :java:extdoc:`inputCount <nablarch.fw.batch.ee.progress.ProgressManager.setInputCount(long)>` に設定する。
  * 処理を行うループ処理内で、一定間隔ごとに進捗ログを出力する :java:extdoc:`outputProgressInfo <nablarch.fw.batch.ee.progress.ProgressManager.outputProgressInfo(long)>` を呼び出す。

実装例
  .. code-block:: java

    @Named
    @Dependent
    public class SampleBatchlet extends AbstractBatchlet {

        /** 進捗ログを出力するための機能 */
        private final ProgressManager progressManager;
        
        /** 進捗ログを出力する間隔 */
        private static final int PROGRESS_LOG_INTERVAL = 1000;

        /**
         * 進捗ログを出力するための機能をコンストラクタインジェクションを使用してインジェクションする。
         */
        @Inject
        public ProgressBatchlet(ProgressManager progressManager) {
          this.progressManager = progressManager;
        }

        @Override
        public String process() throws Exception {
         
          // 処理対象の件数を設定する。
          // 実際には、データベースやファイルのレコード数などが処理件数となる。
          progressManager.setInputCount(10000);
          
          // 処理済みの件数
          long processedCount = 0;
          
          while (処理対象が存在している間) {
              processedCount++;
              
              // 実際の処理は省略
              
              if (processedCount % PROGRESS_LOG_INTERVAL == 0) {
                // 処理済みの件数を進捗ログ出力機能に渡すことで、進捗ログが出力される
                progressManager.outputProgressInfo(processedCount);
              }
          }
          return "SUCCESS";
        }
    }
  
Chunkステップで進捗ログを出力する
--------------------------------------------------
Chunkステップで進捗状況をログに出力するための実装例を以下に示す。

.. _jsr352-progress_reader:

ItemReader
  ポイント
    * コンストラクタインジェクションを使用して、進捗ログを出力するインタフェース( :java:extdoc:`ProgressManager <nablarch.fw.batch.ee.progress.ProgressManager>` )をインジェクションする。
    * openメソッドにて、処理対象件数(データベースへのcount結果やファイルのレコード数等)を取得し、 :java:extdoc:`inputCount <nablarch.fw.batch.ee.progress.ProgressManager.setInputCount(long)>` に設定する。
    
  実装例
    .. code-block:: java

      @Named
      @Dependent
      public class ProgressReader extends AbstractItemReader {

        /** 進捗ログを出力する機能 */
        private final ProgressManager progressManager;

        /**
         * 進捗ログを出力するための機能をコンストラクタインジェクションを使用してインジェクションする。
         */
        @Inject
        public ProgressReader(ProgressManager progressManager) {
            this.progressManager = progressManager;
        }

        @Override
        public void open(Serializable checkpoint) throws Exception {
          // openメソッド内で、処理対象の件数を進捗ログを出力する機能に設定する。
          // 実際には、データベースに対するcount文の結果やファイルのレコード数を設定する。
          progressManager.setInputCount(10000);
        }

        @Override
        public Object readItem() throws Exception {
          // 省略
        }
      }

.. _jsr352-progress_listener:

ジョブ定義ファイル
  ポイント
    * step配下のリスナーのリストに進捗ログを出力するリスナー(名前は、 ``progressLogListener`` 固定)を設定する。
    
  実装例
    .. code-block:: xml
    
      <job id="batchlet-progress-test" xmlns="http://xmlns.jcp.org/xml/ns/javaee" version="1.0">
        <listeners>
          <listener ref="nablarchJobListenerExecutor" />
        </listeners>
      
        <step id="step">
          <listeners>
            <listener ref="nablarchStepListenerExecutor" />
            <listener ref="nablarchItemWriteListenerExecutor" />
            <!-- step配下に進捗ログを出力するリスナーを設定する。 -->
            <listener ref="progressLogListener" />
          </listeners>
          <chunk item-count="1000">
            <reader ref="progressReader" />
            <writer ref="progressWriter" />
          </chunk>
        </step>
      </job>

.. important::
  :ref:`ItemReader <jsr352-progress_reader>` で処理対象件数の設定を行わずに、
  :ref:`進捗ログ出力リスナー <jsr352-progress_listener>` を設定した場合には、設定不備として例外を送出し処理を異常終了させる。
  このため、進捗ログを必要としない場合には、 :ref:`進捗ログ出力リスナー <jsr352-progress_listener>` の設定を必ず削除すること。
  
.. important::
  chunkステップでRetrying Exceptionsの設定を行った場合は、リスナーによる進捗ログの出力が正しく機能しなくなる。
  これは、リスナーが処理済み件数として使用している :java:extdoc:`metrics <javax.batch.runtime.context.StepContext.getMetrics()>`
  の読み込み済み件数が実態とずれることに起因する。
  
  このため、Retrying Exceptionsを使用して例外発生時のリトライ処理を行いたい場合には、 :java:extdoc:`ItemWriter <javax.batch.api.chunk.ItemWriter>` の実装クラスにて処理済み件数を計算し、
  :java:extdoc:`outputProgressInfo <nablarch.fw.batch.ee.progress.ProgressManager.outputProgressInfo(long)>` を使用して進捗ログの出力を行うこと。
  

