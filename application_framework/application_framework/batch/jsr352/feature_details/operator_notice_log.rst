運用担当者向けのログ出力
==================================================
.. contents:: 目次
  :depth: 3
  :local:

運用担当者向けログの出力内容
--------------------------------------------
運用担当者向けログには、運用担当者がログをもとに対処を行えるよう、最低限以下の内容を出力する必要がある。

* 何が発生したか
* どのように対処すべきか

これらの内容が出力されていないと、運用担当者が発生した事象に対しどう対処すればよいか判断できない恐れがある。

運用担当者向けのログを専用のログファイルに出力するための設定を追加する
----------------------------------------------------------------------
運用担当者向けのログは、ログカテゴリ名を ``operator`` として出力する。
このカテゴリ名を使用して、運用担当者向けのログ用のファイルにログを出力することが出来る。

:ref:`log` を使用した場合の ``log.properties`` の設定例を以下に示す。
:ref:`log_adaptor` を使用している場合には、アダプタに対応したログライブラリのマニュアルなどを参照し設定を行うこと。

.. code-block:: properties

  # operation log file
  writer.operationLog.className=nablarch.core.log.basic.FileLogWriter
  writer.operationLog.filePath=./log/operation.log
  writer.operationLog.encoding=UTF-8
  writer.operationLog.formatter.className=nablarch.core.log.basic.BasicLogFormatter
  writer.operationLog.formatter.format=$date$ -$logLevel$- $message$

  # logger list
  availableLoggersNamesOrder=SQL,MON,OPERATOR,ROO

  # operation logger setting
  loggers.OPERATOR.nameRegex=operator
  loggers.OPERATOR.level=INFO
  loggers.OPERATOR.writerNames=operationLog

運用担当者向けのログを出力する
--------------------------------------------------

運用担当者向けのログを出力するための実装例を以下に示す。

ポイント
  * :java:extdoc:`OperationLogger#write <nablarch.core.log.operation.OperationLogger.write(nablarch.core.log.basic.LogLevel,java.lang.String,java.lang.Throwable)>`
    を使用してログを出力する。

実装例
  .. code-block:: java

    @Named
    @Dependent
    public class SampleBatchlet extends AbstractBatchlet {

        @Override
        public String process() throws Exception {

            try {
                // 省略
            } catch (FileNotFoundException e) {
                // 入力ファイルが存在しないことを運用担当者に通知して例外を送出する
                OperationLogger.write(
                        LogLevel.ERROR,
                        "ファイルが存在しません。正しく受信できているか確認してください。",
                        e);
                throw e;
            }

            // 省略
        }
    }

出力例
  .. code-block:: bash

    ERROR operator ファイルが存在しません。正しく受信できているか確認してください。

