.. _global_error_handler:

グローバルエラーハンドラ
========================================
.. contents:: 目次
  :depth: 3
  :local:

後続ハンドラで発生した未捕捉の例外及びエラーを捕捉し、ログ出力及び結果返却を行うハンドラ。

処理の流れは以下のとおり。


.. image:: ../images/GlobalErrorHandler/flow.png

ハンドラクラス名
--------------------------------------------------
* :java:extdoc:`nablarch.fw.handler.GlobalErrorHandler`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw</artifactId>
  </dependency>

制約
--------------------------------------------------

できるだけハンドラキューの先頭に配置すること
  このハンドラは未補足例外を処理するため、特に理由がない限り、できるだけハンドラキューの先頭に配置すること。
  
  もし、このハンドラより手前のハンドラで例外が発生した場合は、ウェブアプリケーションサーバやJVMにより例外処理が行われる。

例外及びエラーに応じた処理内容
--------------------------------------------------
このハンドラでは捕捉した例外及びエラーの内容に応じて、以下の処理と結果の生成を行う。

例外に応じた処理内容
  .. list-table::
    :header-rows: 1
    :class: white-space-normal
    :widths: 25 75

    * - 例外クラス
      - 処理内容

    * - :java:extdoc:`ServiceError <nablarch.fw.results.ServiceError>` 
      
        (サブクラス含む)

      - :java:extdoc:`ServiceError#writeLog <nablarch.fw.results.ServiceError.writeLog(nablarch.fw.ExecutionContext)>` を呼び出し、ログ出力を行う。

        ログレベルは、 :java:extdoc:`ServiceError <nablarch.fw.results.ServiceError>` の実装クラスにより異なる。

        ログ出力後、ハンドラの処理結果として、 :java:extdoc:`ServiceError <nablarch.fw.results.ServiceError>` を返却する。

    * - :java:extdoc:`Result.Error <nablarch.fw.Result.Error>`

        (サブクラス含む)

      - FATALレベルのログ出力を行う。

        ログ出力後、ハンドラの処理結果として、 :java:extdoc:`Result.Error <nablarch.fw.Result.Error>` を返却する。

    * - 上記以外の例外クラス

      - FATALレベルのログ出力を行う。
        
        ログ出力後、捕捉した例外を原因に持つ :java:extdoc:`InternalError <nablarch.fw.results.InternalError>` を生成し、ハンドラの処理結果として返却する。

エラーに応じた処理内容
  .. list-table::
    :header-rows: 1
    :class: white-space-normal
    :widths: 25 75

    * - エラークラス
      - 処理内容

    * - :java:extdoc:`ThreadDeath <java.lang.ThreadDeath>`

        (サブクラス含む)

      - INFOレベルのログ出力を行う。

        ログ出力後、捕捉したエラーをリスローする。

    * - :java:extdoc:`StackOverflowError <java.lang.StackOverflowError>`

        (サブクラス含む)

      - FATALレベルのログ出力を行う。
        
        ログ出力後、捕捉したエラーを原因に持つ :java:extdoc:`InternalError <nablarch.fw.results.InternalError>` を生成し、ハンドラの処理結果として返却する。

    * - :java:extdoc:`OutOfMemoryError <java.lang.OutOfMemoryError>`

        (サブクラス含む)

      - FATALレベルのログ出力を行う。

        なお、FATALレベルのログ出力に失敗する可能性(再度 `OutOfMemoryError` が発生する可能性)があるため、
        ログ出力前に標準エラー出力に `OutOfMemoryError` が発生したことを出力する。

        ログ出力後、捕捉したエラーを原因に持つ :java:extdoc:`InternalError <nablarch.fw.results.InternalError>` を生成し、ハンドラの処理結果として返却する。

    * - :java:extdoc:`VirtualMachineError <java.lang.VirtualMachineError>`

        (サブクラス含む)

      - FATALレベルのログ出力を行う。

        ログ出力後、捕捉したエラーをリスローする。

        .. tip::
          
          :java:extdoc:`StackOverflowError <java.lang.StackOverflowError>` 及び :java:extdoc:`OutOfMemoryError <java.lang.OutOfMemoryError>` 以外が対象となる。

    * - 上記以外のエラークラス

      - FATALレベルのログ出力を行う。
        
        ログ出力後、捕捉したエラーを原因に持つ :java:extdoc:`InternalError <nablarch.fw.results.InternalError>` を生成し、ハンドラの処理結果として返却する。



グローバルエラーハンドラでは要件を満たせない場合
--------------------------------------------------
このハンドラは、設定などで実装を切り替えることはできない。
このため、この実装で要件を満たすことができない場合は、
プロジェクト固有のエラー処理用ハンドラを作成し対応すること。

例えば、ログレベルを細かく切り替えたい場合などは、このハンドラを使用するのではなく、ハンドラを新たに作成すると良い。




