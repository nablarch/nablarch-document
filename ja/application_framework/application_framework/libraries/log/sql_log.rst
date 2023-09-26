.. _sql_log:

SQLログの出力
==================================================

.. contents:: 目次
  :depth: 3
  :local:

SQLログは、パフォーマンスチューニングに使用するために、SQL文の実行時間やSQL文を出力する。
アプリケーションでは、ログ出力を設定することにより出力する。

SQLログの出力方針
--------------------------------------------------
SQLログは、ログのサイズが大きくなりディスクフルになったり、パフォーマンスに影響を与える可能性がある。
そのため、SQLログは開発時の使用を想定し、DEBUGレベル以下で出力する。

.. list-table:: SQLログの出力方針
   :header-rows: 1
   :class: white-space-normal
   :widths: 15,15,70

   * - ログレベル
     - ロガー名
     - 出力内容

   * - DEBUG
     - SQL
     - SQL文、実行時間、件数(検索件数や更新件数など)、トランザクションの処理結果(コミット又はロールバック)

   * - TRACE
     - SQL
     - SQLパラメータ(バインド変数の値)

上記出力方針に対するログ出力の設定例を下記に示す。

log.propertiesの設定例
 .. code-block:: properties

  writerNames=appLog

  # アプリケーションログの出力先
  writer.appLog.className=nablarch.core.log.basic.FileLogWriter
  writer.appLog.filePath=/var/log/app/app.log
  writer.appLog.encoding=UTF-8
  writer.appLog.maxFileSize=10000
  writer.appLog.formatter.className=nablarch.core.log.basic.BasicLogFormatter
  writer.appLog.formatter.format=$date$ -$logLevel$- $runtimeLoggerName$ [$executionId$] boot_proc = [$bootProcess$] proc_sys = [$processingSystem$] req_id = [$requestId$] usr_id = [$userId$] $message$$information$$stackTrace$

  availableLoggersNamesOrder=SQL,ROO

  # アプリケーションログの設定
  loggers.ROO.nameRegex=.*
  loggers.ROO.level=INFO
  loggers.ROO.writerNames=appLog

  # SQLログの設定
  loggers.SQL.nameRegex=SQL
  loggers.SQL.level=TRACE
  loggers.SQL.writerNames=appLog

app-log.propertiesの設定例
 .. code-block:: properties

  # SqlLogFormatter
  #sqlLogFormatter.className=
  # SqlPStatement#retrieveのフォーマット
  sqlLogFormatter.startRetrieveFormat=$methodName$\
                                        \n\tSQL = [$sql$]\
                                        \n\tstart_position = [$startPosition$] size = [$size$]\
                                        \n\tquery_timeout = [$queryTimeout$] fetch_size = [$fetchSize$]\
                                        \n\tadditional_info:\
                                        \n\t$additionalInfo$
  sqlLogFormatter.endRetrieveFormat=$methodName$\
                                      \n\texecute_time(ms) = [$executeTime$] retrieve_time(ms) = [$retrieveTime$] count = [$count$]
  # SqlPStatement#executeのフォーマット
  sqlLogFormatter.startExecuteFormat=$methodName$\
                                        \n\tSQL = [$sql$]\
                                        \n\tadditional_info:\
                                        \n\t$additionalInfo$
  sqlLogFormatter.endExecuteFormat=$methodName$\
                                      \n\texecute_time(ms) = [$executeTime$]
  # SqlPStatement#executeQueryのフォーマット
  sqlLogFormatter.startExecuteQueryFormat=$methodName$\
                                            \n\tSQL = [$sql$]\
                                            \n\tadditional_info:\
                                            \n\t$additionalInfo$
  sqlLogFormatter.endExecuteQueryFormat=$methodName$\
                                          \n\texecute_time(ms) = [$executeTime$]
  # SqlPStatement#executeUpdateのフォーマット
  sqlLogFormatter.startExecuteUpdateFormat=$methodName$\
                                              \n\tSQL = [$sql$]\
                                              \n\tadditional_info:\
                                              \n\t$additionalInfo$
  sqlLogFormatter.endExecuteUpdateFormat=$methodName$\
                                          \n\texecute_time(ms) = [$executeTime$] update_count = [$updateCount$]
  # SqlStatement#executeBatchのフォーマット
  sqlLogFormatter.startExecuteBatchFormat=$methodName$\
                                            \n\tSQL = [$sql$]\
                                            \n\tadditional_info:\
                                            \n\t$additionalInfo$
  sqlLogFormatter.endExecuteBatchFormat=$methodName$\
                                          \n\texecute_time(ms) = [$executeTime$] batch_count = [$updateCount$]

使用方法
--------------------------------------------------

.. _sql_log-setting:

SQLログの設定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SQLログの設定は、 :ref:`log-app_log_setting` で説明したプロパティファイルに行う。

記述ルール
 \

 sqlLogFormatter.className
  :java:extdoc:`SqlLogFormatter <nablarch.core.db.statement.SqlLogFormatter>` を実装したクラス。
  差し替える場合に指定する。

 sqlLogFormatter.startRetrieveFormat
  :java:extdoc:`SqlPStatement#retrieve <nablarch.core.db.statement.SqlPStatement.retrieve()>`
  の開始時に使用するフォーマット。

  フォーマットに指定可能なプレースホルダ
   :メソッド名: $methodName$
   :SQL文: $sql$
   :取得開始位置: $startPosition$
   :取得最大件数: $size$
   :タイムアウト時間: $queryTimeout$
   :フェッチする行数: $fetchSize$
   :付加情報: $additionalInfo$

  デフォルトのフォーマット
   .. code-block:: bash

    $methodName$
        \n\tSQL = [$sql$]
        \n\tstart_position = [$startPosition$] size = [$size$]
        \n\tquery_timeout = [$queryTimeout$] fetch_size = [$fetchSize$]
        \n\tadditional_info:
        \n\t$additionalInfo$

 sqlLogFormatter.endRetrieveFormat
  :java:extdoc:`SqlPStatement#retrieve <nablarch.core.db.statement.SqlPStatement.retrieve()>`
  の終了時に使用するフォーマット。

  フォーマットに指定可能なプレースホルダ
   :メソッド名: $methodName$
   :実行時間: $executeTime$
   :データ取得時間: $retrieveTime$
   :検索件数: $count$

  デフォルトのフォーマット
   .. code-block:: bash

    $methodName$
        \n\texecute_time(ms) = [$executeTime$] retrieve_time(ms) = [$retrieveTime$] count = [$count$]

 sqlLogFormatter.startExecuteFormat
  :java:extdoc:`SqlPStatement#execute <nablarch.core.db.statement.SqlPStatement.execute()>`
  の開始時に使用するフォーマット。

  フォーマットに指定可能なプレースホルダ
   :メソッド名: $methodName$
   :SQL文: $sql$
   :付加情報: $additionalInfo$

  デフォルトのフォーマット
   .. code-block:: bash

    $methodName$
        \n\tSQL = [$sql$]
        \n\tadditional_info:
        \n\t$additionalInfo$

 sqlLogFormatter.endExecuteFormat
  :java:extdoc:`SqlPStatement#execute <nablarch.core.db.statement.SqlPStatement.execute()>`
  の終了時に使用するフォーマット。

  フォーマットに指定可能なプレースホルダ
   :メソッド名: $methodName$
   :実行時間: $executeTime$

  デフォルトのフォーマット
   .. code-block:: bash

    $methodName$
        \n\texecute_time(ms) = [$executeTime$]

 sqlLogFormatter.startExecuteQueryFormat
  :java:extdoc:`SqlPStatement#executeQuery <nablarch.core.db.statement.SqlPStatement.executeQuery()>`
  の開始時に使用するフォーマット。

  フォーマットに指定可能なプレースホルダ
   :メソッド名: $methodName$
   :SQL文: $sql$
   :付加情報: $additionalInfo$

  デフォルトのフォーマット
   .. code-block:: bash

    $methodName$
        \n\tSQL = [$sql$]
        \n\tadditional_info:
        \n\t$additionalInfo$

 sqlLogFormatter.endExecuteQueryFormat
  :java:extdoc:`SqlPStatement#executeQuery <nablarch.core.db.statement.SqlPStatement.executeQuery()>`
  の終了時に使用するフォーマット。

  フォーマットに指定可能なプレースホルダ
   :メソッド名: $methodName$
   :実行時間: $executeTime$

  デフォルトのフォーマット
   .. code-block:: bash

    $methodName$
        \n\texecute_time(ms) = [$executeTime$]

 sqlLogFormatter.startExecuteUpdateFormat
  :java:extdoc:`SqlPStatement#executeUpdate <nablarch.core.db.statement.SqlPStatement.executeUpdate()>`
  の開始時に使用するフォーマット。

  フォーマットに指定可能なプレースホルダ
   :メソッド名: $methodName$
   :SQL文: $sql$
   :付加情報: $additionalInfo$

  デフォルトのフォーマット
   .. code-block:: bash

    $methodName$
        \n\tSQL = [$sql$]
        \n\tadditional_info:
        \n\t$additionalInfo$

 sqlLogFormatter.endExecuteUpdateFormat
  :java:extdoc:`SqlPStatement#executeUpdate <nablarch.core.db.statement.SqlPStatement.executeUpdate()>`
  の終了時に使用するフォーマット。

  フォーマットに指定可能なプレースホルダ
   :メソッド名: $methodName$
   :実行時間: $executeTime$
   :更新件数: $updateCount$

  デフォルトのフォーマット
   .. code-block:: bash

    $methodName$
        \n\texecute_time(ms) = [$executeTime$] update_count = [$updateCount$]

 sqlLogFormatter.startExecuteBatchFormat
  :java:extdoc:`SqlStatement#executeBatch <nablarch.core.db.statement.SqlStatement.executeBatch()>`
  の開始時に使用するフォーマット。

  フォーマットに指定可能なプレースホルダ
   :メソッド名: $methodName$
   :SQL文: $sql$
   :付加情報: $additionalInfo$

  デフォルトのフォーマット
   .. code-block:: bash

    $methodName$
        \n\tSQL = [$sql$]
        \n\tadditional_info:
        \n\t$additionalInfo$

 sqlLogFormatter.endExecuteBatchFormat
  :java:extdoc:`SqlStatement#executeBatch <nablarch.core.db.statement.SqlStatement.executeBatch()>`
  の終了時に使用するフォーマット。

  フォーマットに指定可能なプレースホルダ
   :メソッド名: $methodName$
   :実行時間: $executeTime$
   :バッチ件数: $batchCount$

  デフォルトのフォーマット
   .. code-block:: bash

    $methodName$
        \n\texecute_time(ms) = [$executeTime$] batch_count = [$updateCount$]

記述例
 .. code-block:: properties

  sqlLogFormatter.className=nablarch.core.db.statement.SqlLogFormatter
  sqlLogFormatter.startRetrieveFormat=$methodName$\n\tSQL:$sql$\n\tstart:$startPosition$ size:$size$\n\tadditional_info:\n\t$additionalInfo$
  sqlLogFormatter.endRetrieveFormat=$methodName$\n\texe:$executeTime$ms ret:$retrieveTime$ms count:$count$
  sqlLogFormatter.startExecuteFormat=$methodName$\n\tSQL:$sql$\n\tadditional_info:\n\t$additionalInfo$
  sqlLogFormatter.endExecuteFormat=$methodName$\n\texe:$executeTime$ms
  sqlLogFormatter.startExecuteQueryFormat=$methodName$\n\tSQL:$sql$\n\tadditional_info:\n\t$additionalInfo$
  sqlLogFormatter.endExecuteQueryFormat=$methodName$\n\texe:$executeTime$ms
  sqlLogFormatter.startExecuteUpdateFormat=$methodName$\n\tSQL:$sql$\n\tadditional_info:\n\t$additionalInfo$
  sqlLogFormatter.endExecuteUpdateFormat=$methodName$\n\texe:$executeTime$ms count:$updateCount$
  sqlLogFormatter.startExecuteBatchFormat=$methodName$\n\tSQL:$sql$\n\tadditional_info:\n\t$additionalInfo$
  sqlLogFormatter.endExecuteBatchFormat=$methodName$\n\texe:$executeTime$ms count:$updateCount$

.. _sql_log-json_setting:

JSON形式の構造化ログとして出力する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`log-json_log_setting` 設定によりログをJSON形式で出力できるが、
:java:extdoc:`SqlLogFormatter <nablarch.core.db.statement.SqlLogFormatter>` では
SQLログの各項目はmessageの値に文字列として出力される。
SQLログの各項目もJSONの値として出力するには、
:java:extdoc:`SqlJsonLogFormatter <nablarch.core.db.statement.SqlJsonLogFormatter>` を使用する。
設定は、 :ref:`log-app_log_setting` で説明したプロパティファイルに行う。

記述ルール
 :java:extdoc:`SqlJsonLogFormatter <nablarch.core.db.statement.SqlJsonLogFormatter>` を用いる際に
 指定するプロパティは以下の通り。
 
 sqlLogFormatter.className ``必須``
  JSON形式でログを出力する場合、
  :java:extdoc:`SqlJsonLogFormatter <nablarch.core.db.statement.SqlJsonLogFormatter>` を指定する。

 sqlLogFormatter.startRetrieveTargets
  :java:extdoc:`SqlPStatement#retrieve <nablarch.core.db.statement.SqlPStatement.retrieve()>`
  の開始時のログ出力項目。カンマ区切りで指定する。

  指定可能な出力項目
   :メソッド名: methodName
   :SQL文: sql
   :取得開始位置: startPosition
   :取得最大件数: size
   :タイムアウト時間: queryTimeout
   :フェッチする行数: fetchSize
   :付加情報: additionalInfo
 
  デフォルトは全ての出力項目が対象となる。

 sqlLogFormatter.endRetrieveTargets
  :java:extdoc:`SqlPStatement#retrieve <nablarch.core.db.statement.SqlPStatement.retrieve()>`
  の終了時のログ出力項目。カンマ区切りで指定する。

  指定可能な出力項目
   :メソッド名: methodName
   :実行時間: executeTime
   :データ取得時間: retrieveTime
   :検索件数: count

  デフォルトは全ての出力項目が対象となる。

 sqlLogFormatter.startExecuteTargets
  :java:extdoc:`SqlPStatement#execute <nablarch.core.db.statement.SqlPStatement.execute()>`
  の開始時のログ出力項目。カンマ区切りで指定する。

  指定可能な出力項目
   :メソッド名: methodName
   :SQL文: sql
   :付加情報: additionalInfo

  デフォルトは全ての出力項目が対象となる。

 sqlLogFormatter.endExecuteTargets
  :java:extdoc:`SqlPStatement#execute <nablarch.core.db.statement.SqlPStatement.execute()>`
  の終了時のログ出力項目。カンマ区切りで指定する。

  指定可能な出力項目
   :メソッド名: methodName
   :実行時間: executeTime

  デフォルトは全ての出力項目が対象となる。

 sqlLogFormatter.startExecuteQueryTargets
  :java:extdoc:`SqlPStatement#executeQuery <nablarch.core.db.statement.SqlPStatement.executeQuery()>`
  の開始時のログ出力項目。カンマ区切りで指定する。

  指定可能な出力項目
   :メソッド名: methodName
   :SQL文: sql
   :付加情報: additionalInfo

  デフォルトは全ての出力項目が対象となる。

 sqlLogFormatter.endExecuteQueryTargets
  :java:extdoc:`SqlPStatement#executeQuery <nablarch.core.db.statement.SqlPStatement.executeQuery()>`
  の終了時のログ出力項目。カンマ区切りで指定する。

  指定可能な出力項目
   :メソッド名: methodName
   :実行時間: executeTime

  デフォルトは全ての出力項目が対象となる。

 sqlLogFormatter.startExecuteUpdateTargets
  :java:extdoc:`SqlPStatement#executeUpdate <nablarch.core.db.statement.SqlPStatement.executeUpdate()>`
  の開始時のログ出力項目。カンマ区切りで指定する。

  指定可能な出力項目
   :メソッド名: methodName
   :SQL文: sql
   :付加情報: additionalInfo

  デフォルトは全ての出力項目が対象となる。

 sqlLogFormatter.endExecuteUpdateTargets
  :java:extdoc:`SqlPStatement#executeUpdate <nablarch.core.db.statement.SqlPStatement.executeUpdate()>`
  の終了時のログ出力項目。カンマ区切りで指定する。

  指定可能な出力項目
   :メソッド名: methodName
   :実行時間: executeTime
   :更新件数: updateCount

  デフォルトは全ての出力項目が対象となる。

 sqlLogFormatter.startExecuteBatchTargets
  :java:extdoc:`SqlStatement#executeBatch <nablarch.core.db.statement.SqlStatement.executeBatch()>`
  の開始時のログ出力項目。カンマ区切りで指定する。

  指定可能な出力項目
   :メソッド名: methodName
   :SQL文: sql
   :付加情報: additionalInfo

  デフォルトは全ての出力項目が対象となる。

 sqlLogFormatter.endExecuteBatchTargets
  :java:extdoc:`SqlStatement#executeBatch <nablarch.core.db.statement.SqlStatement.executeBatch()>`
  の終了時のログ出力項目。カンマ区切りで指定する。

  指定可能な出力項目
   :メソッド名: methodName
   :実行時間: executeTime
   :バッチ件数: batchCount

  デフォルトは全ての出力項目が対象となる。

 sqlLogFormatter.structuredMessagePrefix
  フォーマット後のメッセージ文字列が JSON 形式に整形されていることを識別できるようにするために、メッセージの先頭に付与するマーカー文字列。
  メッセージの先頭にあるマーカー文字列が :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` に設定しているマーカー文字列と一致する場合、 :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` はメッセージを JSON データとして処理する。
  デフォルトは ``"$JSON$"`` となる。
  変更する場合は、LogWriterの ``structuredMessagePrefix`` プロパティを使用して :java:extdoc:`JsonLogFormatter <nablarch.core.log.basic.JsonLogFormatter>` にも同じ値を設定すること（LogWriterのプロパティについては :ref:`log-basic_setting` を参照）。

記述例
 .. code-block:: properties

  sqlLogFormatter.className=nablarch.core.db.statement.SqlJsonLogFormatter
  sqlLogFormatter.structuredMessagePrefix=$JSON$
  sqlLogFormatter.startRetrieveTargets=methodName,sql,startPosition,size,additionalInfo
  sqlLogFormatter.endRetrieveTargets=methodName,executeTime,retrieveTime,count
  sqlLogFormatter.startExecuteTargets=methodName,sql,additionalInfo
  sqlLogFormatter.endExecuteTargets=methodName,executeTime
  sqlLogFormatter.startExecuteQueryTargets=methodName,sql,additionalInfo
  sqlLogFormatter.endExecuteQueryTargets=methodName,executeTime
  sqlLogFormatter.startExecuteUpdateTargets=methodName,sql,additionalInfo
  sqlLogFormatter.endExecuteUpdateTargets=methodName,executeTime,updateCount
  sqlLogFormatter.startExecuteBatchTargets=methodName,sql,additionalInfo
  sqlLogFormatter.endExecuteBatchTargets=methodName,executeTime,batchCount
