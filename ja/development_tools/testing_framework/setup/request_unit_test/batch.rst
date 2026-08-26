.. _request_unit_test_setting_batch:

リクエスト単体テストの設定（Nablarchバッチアプリケーション）
============================================================

.. contents:: 目次
  :depth: 3
  :local:

機能概要
--------------------------------------------------

Nablarchバッチアプリケーションのリクエスト単体テストでは、テスト対象のハンドラ構成にリクエストスレッド内ループ制御ハンドラが含まれる場合に、これをテスト用のハンドラに置き換える。応答不要メッセージ送信のテストでは、メッセージングプロバイダもテスト用のものに差し替える。ディレクティブのデフォルト値と、固定長ファイルの数値フィールドで使用するテスト用のデータ型も、コンポーネント設定ファイルに設定できる。後の2つはNablarchバッチアプリケーションに固有の設定ではなく、ファイルデータや電文のテストデータを扱うテストで使用する。

使用方法
--------------------------------------------------

リクエストスレッド内ループ制御ハンドラを置き換える
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`リクエストスレッド内ループ制御ハンドラ <request_thread_loop_handler>`\ をハンドラ構成に含むアプリケーションは、本番用のハンドラ構成のままではリクエスト単体テストを実施できない。このハンドラは、プロセスの停止要求があるまで後続のハンドラを繰り返し実行する。準備した要求データを処理し終えた後も要求データの検索が続くため、処理が終了しない。このハンドラは\ :ref:`テーブルをキューとして使ったメッセージング <db_messaging>`\ のハンドラ構成に含まれる。

テスティングフレームワークが提供する\ :java:extdoc:`OneShotLoopHandler <nablarch.test.OneShotLoopHandler>`\ は、後続のハンドラが処理するデータが無くなった時点で繰り返しを終える。これに置き換えると、準備した要求データの処理を終えた時点でテストコードに制御が戻る。本番用のコンポーネント設定ファイルに、次のようなリクエストスレッド内ループ制御ハンドラの設定があるとする。

.. code-block:: xml

  <!-- リクエストスレッド内ループ制御ハンドラ -->
  <component name="requestThreadLoopHandler" class="nablarch.fw.handler.RequestThreadLoopHandler">
    <!-- プロパティへの値の設定は省略 -->
  </component>

テスト用のコンポーネント設定ファイルでは、この設定を同じコンポーネント名で上書きする。上書きの記述は、本番用のコンポーネント設定ファイルの読み込みより後に置く。

.. code-block:: xml

  <!-- リクエストスレッド内ループ制御ハンドラをテスト用のハンドラに置き換える -->
  <component name="requestThreadLoopHandler" class="nablarch.test.OneShotLoopHandler"/>

.. tip::

  上書き前後でクラスが異なるため、本番用の設定で指定したプロパティの値は引き継がれない。詳細は\ :ref:`Java Beansオブジェクトの設定を上書きする <repository-override_bean>`\ を参照。

応答不要メッセージ送信用のメッセージングプロバイダに差し替える
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
応答不要メッセージ送信のリクエスト単体テストでは、キューへのメッセージ送信は行われない。送信される要求電文は、テスティングフレームワークが提供する\ ``RequestTestingMessagingProvider``\ が保持し、テストデータに記述した期待値と照合する。テスト用のコンポーネント設定ファイルに、次のとおり登録する。

.. code-block:: xml

  <!-- リクエスト単体テスト用のメッセージングプロバイダ -->
  <component name="messagingProvider"
             class="nablarch.test.core.messaging.RequestTestingMessagingProvider"/>

コンポーネント名には、本番用のコンポーネント設定ファイルでメッセージングプロバイダに付けた名前を使用する。同じ名前で登録することで、テスト用のプロバイダに置き換わる。上書きの記述は、本番用のコンポーネント設定ファイルの読み込みより後に置く。

.. important::

  この差し替えを行わないと、要求電文が実際のキューへ送信され、テスティングフレームワークが要求電文を保持できない。テストショット一覧の\ ``expectedMessage``\ に記述した要求電文の期待値との照合が、送信件数の不一致で失敗する。

ディレクティブのデフォルト値を設定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ファイルのディレクティブがシステム内である程度統一されている場合、個々のファイルデータブロックに同じディレクティブを繰り返し記述することになる。コンポーネント設定ファイルにデフォルト値をmap形式で登録すると、この記述を省略できる。mapの\ ``name``\ 属性には、デフォルト値を適用するファイルの種別に応じて次の名前を指定する。

.. list-table::
  :header-rows: 1
  :widths: 40,60

  * - 対象となるファイルの種別
    - ``name``\ 属性
  * - 共通
    - ``defaultDirectives``
  * - 固定長ファイル
    - ``fixedLengthDirectives``
  * - 可変長ファイル
    - ``variableLengthDirectives``

記述例を示す。

.. code-block:: xml

  <!-- ディレクティブのデフォルト値（共通） -->
  <map name="defaultDirectives">
    <entry key="text-encoding" value="Windows-31J"/>
  </map>

  <!-- ディレクティブのデフォルト値（固定長ファイル） -->
  <map name="fixedLengthDirectives">
    <entry key="record-separator" value="NONE"/>
  </map>

  <!-- ディレクティブのデフォルト値（可変長ファイル） -->
  <map name="variableLengthDirectives">
    <entry key="quoting-delimiter" value="&quot;"/>
    <entry key="record-separator" value="CRLF"/>
  </map>

共通のデフォルト値が先に適用され、ファイルの種別ごとのデフォルト値がその後に適用される。同じディレクティブを両方に設定した場合は、ファイルの種別ごとの設定が有効になる。個々のファイルデータブロックに記述したディレクティブは、いずれのデフォルト値よりも優先される。

指定できるディレクティブキーはファイルの種別ごとに決まっており、それ以外のキー名を指定するとエラーになる。\ ``defaultDirectives``\ は固定長ファイル・可変長ファイルの両方に適用されるため、共通のデフォルト値には両方の種別で有効なキーだけを設定する（片方の種別にしかないキーを設定すると、もう一方の種別のテストデータを読み込む時点でエラーになる）。ディレクティブキーの一覧は\ :ref:`ファイルのデータを記述する <testdata_notation-file_data>`\ を参照。

符号無数値・符号付数値のテスト用のデータ型を登録する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
固定長ファイルのフィールドのうち、データ型が符号無数値（型記号\ ``X9``\ ）・符号付数値（型記号\ ``SX9``\ ）のものは、パディング文字や符号を含めた固定長ファイル上の表現を、テストデータにそのまま記述する。記述方法は\ :ref:`ファイルのデータを記述する <testdata_notation-file_data>`\ を参照。

テストデータの記述をそのまま使用するには、テスト用のデータ型を登録する。テスティングフレームワークは、型記号の前に\ ``TEST_``\ を付けた名前のデータ型が登録されている場合、元の型に代えてその型を使用する。\ ``TEST_X9``\ ・\ ``TEST_SX9``\ に\ :java:extdoc:`StringDataType <nablarch.test.core.file.StringDataType>`\ を割り当てると、数値としての変換を行わずにテストデータの記述がそのまま入出力される。

.. important::

  ``convertorTable``\ を設定すると、データ型の対応表はここで指定した内容に置き換わる。テスト用のデータ型だけを記述すると、それ以外のデータ型が使用できなくなるため、デフォルトの対応表の内容も併せて記述する。

.. code-block:: xml

  <component name="fixedLengthConvertorSetting"
             class="nablarch.core.dataformat.convertor.FixedLengthConvertorSetting">
    <property name="convertorTable">
      <map>
        <!-- デフォルトの対応表 -->
        <entry key="X" value="nablarch.core.dataformat.convertor.datatype.SingleByteCharacterString"/>
        <entry key="N" value="nablarch.core.dataformat.convertor.datatype.DoubleByteCharacterString"/>
        <entry key="XN" value="nablarch.core.dataformat.convertor.datatype.ByteStreamDataString"/>
        <entry key="Z" value="nablarch.core.dataformat.convertor.datatype.ZonedDecimal"/>
        <entry key="SZ" value="nablarch.core.dataformat.convertor.datatype.SignedZonedDecimal"/>
        <entry key="P" value="nablarch.core.dataformat.convertor.datatype.PackedDecimal"/>
        <entry key="SP" value="nablarch.core.dataformat.convertor.datatype.SignedPackedDecimal"/>
        <entry key="B" value="nablarch.core.dataformat.convertor.datatype.Bytes"/>
        <entry key="X9" value="nablarch.core.dataformat.convertor.datatype.NumberStringDecimal"/>
        <entry key="SX9" value="nablarch.core.dataformat.convertor.datatype.SignedNumberStringDecimal"/>
        <entry key="pad" value="nablarch.core.dataformat.convertor.value.Padding"/>
        <entry key="encoding" value="nablarch.core.dataformat.convertor.value.UseEncoding"/>
        <entry key="_LITERAL_" value="nablarch.core.dataformat.convertor.value.DefaultValue"/>
        <entry key="number" value="nablarch.core.dataformat.convertor.value.NumberString"/>
        <entry key="signed_number" value="nablarch.core.dataformat.convertor.value.SignedNumberString"/>
        <entry key="replacement" value="nablarch.core.dataformat.convertor.value.CharacterReplacer"/>

        <!-- テスト用のデータ型 -->
        <entry key="TEST_X9" value="nablarch.test.core.file.StringDataType"/>
        <entry key="TEST_SX9" value="nablarch.test.core.file.StringDataType"/>
      </map>
    </property>
  </component>
