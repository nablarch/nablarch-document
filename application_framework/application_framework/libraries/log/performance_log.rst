.. _performance_log:

パフォーマンスログの出力
==================================================

.. contents:: 目次
  :depth: 3
  :local:

パフォーマンスログは、任意の処理範囲に対する実行時間とメモリ使用量を出力し、
開発時のパフォーマンスチューニングに使用する。
アプリケーションでは、ソースコード上でフレームワークが提供するAPIを呼び出し、計測対象の処理範囲を指定して出力する。

パフォーマンスログの出力方針
--------------------------------------------------
パフォーマンスログは、ヒープサイズの取得などでパフォーマンスに影響を与える可能性がある。
そのため、開発時の使用を想定しているためDEBUGレベルで出力する。

.. list-table:: パフォーマンスログの出力方針
   :header-rows: 1
   :class: white-space-normal
   :widths: 15,15

   * - ログレベル
     - ロガー名

   * - DEBUG
     - PERFORMANCE

上記出力方針に対するログ出力の設定例を下記に示す。

log.propertiesの設定例
 .. code-block:: properties

  loggers.PER.nameRegex=PERFORMANCE
  loggers.PER.level=DEBUG
  loggers.PER.writerNames=<出力先のLogWriter>

使用方法
--------------------------------------------------

.. _performance_log-logging:

パフォーマンスログを出力する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
パフォーマンスログは、 :java:extdoc:`PerformanceLogUtil <nablarch.core.log.app.PerformanceLogUtil>` を使用して出力する。
:java:extdoc:`PerformanceLogUtil <nablarch.core.log.app.PerformanceLogUtil>` は、
処理の開始時に呼び出す :java:extdoc:`PerformanceLogUtil#start <nablarch.core.log.app.PerformanceLogUtil.start(java.lang.String)>` と
終了時に呼び出す :java:extdoc:`PerformanceLogUtil#end <nablarch.core.log.app.PerformanceLogUtil.end(java.lang.String, java.lang.String, java.lang.Object...)>`
を提供する。
:java:extdoc:`PerformanceLogUtil <nablarch.core.log.app.PerformanceLogUtil>` は、
:java:extdoc:`PerformanceLogUtil#end <nablarch.core.log.app.PerformanceLogUtil.end(java.lang.String, java.lang.String, java.lang.Object...)>`
が呼ばれた時点で、 :java:extdoc:`PerformanceLogUtil#start <nablarch.core.log.app.PerformanceLogUtil.start(java.lang.String)>`
で取得した日時とメモリ使用量を合わせて出力する。

:java:extdoc:`PerformanceLogUtil <nablarch.core.log.app.PerformanceLogUtil>` の使用例を下記に示す。

.. code-block:: java

 // startメソッドでは、測定対象を識別するポイントを指定する。
 // 誤設定による無駄な出力を防ぐため、
 // このポイント名が設定ファイルに定義されていないとログは出力されない。
 String point = "UserSearchAction#doUSERS00101";
 PerformanceLogUtil.start(point);

 // 検索実行
 UserSearchService searchService = new UserSearchService();
 SqlResultSet searchResult = searchService.selectByCondition(condition);

 // endメソッドでは、ポイント、処理結果を表す文字列、ログ出力のオプション情報を指定できる。
 // 以下ではログ出力のオプション情報は指定していない。
 PerformanceLogUtil.end(point, String.valueOf(searchResult.size()));

.. important::
 :java:extdoc:`PerformanceLogUtil <nablarch.core.log.app.PerformanceLogUtil>` は、
 測定対象を :ref:`実行時ID <log-execution_id>` ＋ポイント名で一意に識別している。
 このため、再帰呼び出しの中で :java:extdoc:`PerformanceLogUtil <nablarch.core.log.app.PerformanceLogUtil>`
 を使用すると計測を実施出来ないため注意すること。

.. _performance_log-setting:

パフォーマンスログの設定を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
パフォーマンスログの設定は、 :ref:`log-app_log_setting` で説明したプロパティファイルに行う。

記述ルール
 \

 performanceLogFormatter.className
  :java:extdoc:`PerformanceLogFormatter <nablarch.core.log.app.PerformanceLogFormatter>` を実装したクラス。
  差し替える場合に指定する。

 performanceLogFormatter.format
  パフォーマンスログの個別項目のフォーマット。

  フォーマットに指定可能なプレースホルダ
   :測定対象を識別するID: $point$
   :処理結果を表す文字列: $result$
   :処理の開始日時: $startTime$
   :処理の終了日時: $endTime$
   :処理の実行時間(終了日時 - 開始日時): $executionTime$
   :処理の開始時点のヒープサイズ: $maxMemory$
   :処理の開始時点の空きヒープサイズ: $startFreeMemory$
   :処理の開始時点の使用ヒープサイズ: $startUsedMemory$
   :処理の終了時点の空きヒープサイズ: $endFreeMemory$
   :処理の終了時点の使用ヒープサイズ: $endUsedMemory$

  デフォルトのフォーマット
   .. code-block:: bash

    \n\tpoint = [$point$] result = [$result$]
    \n\tstart_time = [$startTime$] end_time = [$endTime$]
    \n\texecution_time = [$executionTime$]
    \n\tmax_memory = [$maxMemory$]
    \n\tstart_free_memory = [$startFreeMemory$] start_used_memory = [$startUsedMemory$]
    \n\tend_free_memory = [$endFreeMemory$] end_used_memory = [$endUsedMemory$]

 performanceLogFormatter.datePattern
  開始日時と終了日時に使用する日時パターン。
  パターンには、 :java:extdoc:`SimpleDateFormat <java.text.SimpleDateFormat>` が規程している構文を指定する。
  デフォルトは”yyyy-MM-dd HH:mm:ss.SSS”。

 performanceLogFormatter.targetPoints
  出力対象とするポイント名。
  複数指定する場合はカンマ区切り。
  パフォーマンスログは、誤設定による無駄な出力を防ぐため、この設定に基づき出力する。

記述例
 .. code-block:: properties

  performanceLogFormatter.className=nablarch.core.log.app.PerformanceLogFormatter
  performanceLogFormatter.targetPoints=UserSearchAction#doUSERS00101
  performanceLogFormatter.datePattern=yyyy-MM-dd HH:mm:ss.SSS
  performanceLogFormatter.format=point:$point$ result:$result$ exe_time:$executionTime$ms
