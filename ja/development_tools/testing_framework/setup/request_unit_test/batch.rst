.. _request_unit_test_setting_batch:

リクエスト単体テストの設定（Nablarchバッチアプリケーション）
============================================================

.. contents:: 目次
  :depth: 3
  :local:

Nablarchバッチアプリケーションのリクエスト単体テストでは、常駐バッチのループ制御ハンドラをテスト用のハンドラに置き換える。ファイルを入出力するテストでは、ディレクティブの既定値と、固定長ファイルの数値フィールドで使用するテスト用のデータ型をコンポーネント設定ファイルに設定できる。

使用方法
--------------------------------------------------

常駐バッチのループ制御ハンドラを置き換える
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`常駐バッチ <nablarch_batch-resident_batch>`\ のリクエスト単体テストは、本番用のハンドラ構成のままでは実施できない。\ :ref:`リクエストスレッド内ループ制御ハンドラ <request_thread_loop_handler>`\ はプロセスの停止要求があるまで後続のハンドラを繰り返し実行するため、準備した要求データを処理し終えてもバッチが終了せず、テストコードに制御が戻らないためである。

テスティングフレームワークが提供する\ :java:extdoc:`OneShotLoopHandler <nablarch.test.OneShotLoopHandler>`\ に置き換えると、準備した要求データを処理し終えた時点でバッチが終了し、テストコードに制御が戻る。本番用のコンポーネント設定ファイルに、次のようなリクエストスレッド内ループ制御ハンドラの設定があるとする。

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

ディレクティブの既定値を設定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ファイルのディレクティブがシステム内である程度統一されている場合、個々のテストデータに同じディレクティブを記述するのは冗長である。コンポーネント設定ファイルに既定値をmap形式で登録すると、テストデータでの記述を省略できる。mapの\ ``name``\ 属性には、既定値を適用するファイルの種別に応じて次の名前を指定する。

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

設定例を示す。

.. code-block:: xml

  <!-- ディレクティブの既定値（共通） -->
  <map name="defaultDirectives">
    <entry key="text-encoding" value="Windows-31J"/>
  </map>

  <!-- ディレクティブの既定値（固定長ファイル） -->
  <map name="fixedLengthDirectives">
    <entry key="record-separator" value="NONE"/>
  </map>

  <!-- ディレクティブの既定値（可変長ファイル） -->
  <map name="variableLengthDirectives">
    <entry key="quoting-delimiter" value="&quot;"/>
    <entry key="record-separator" value="CRLF"/>
  </map>

共通の既定値が先に適用され、ファイルの種別ごとの既定値がその後に適用される。同じディレクティブを両方に設定した場合は、ファイルの種別ごとの設定が有効になる。個々のテストデータに記述したディレクティブは、いずれの既定値よりも優先される。

指定できるディレクティブはファイルの種別ごとに決まっており、それ以外の名前を指定するとエラーになる。一覧は\ :ref:`ファイルのデータを記述する <testdata_notation-file_data>`\ を参照。

符号無数値・符号付数値のテスト用データ型を登録する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
固定長ファイルのフィールドのうち、データ型が符号無数値（型記号\ ``X9``\ ）・符号付数値（型記号\ ``SX9``\ ）のものは、パディング文字や符号を含めた固定長ファイル上の表現を、テストデータにそのまま記述する。フィールド長10桁・パディング文字\ ``0``\ ・小数点あり・符号位置固定・正の符号なしのフォーマット定義であれば、12345は\ ``0000012345``\ 、-12.34は\ ``-000012.34``\ と記述する。記述方法は\ :ref:`ファイルのデータを記述する <testdata_notation-file_data>`\ を参照。

テストデータの記述をそのまま使用するには、テスト用のデータ型を登録する。テスティングフレームワークは、型記号の前に\ ``TEST_``\ を付けた名前のデータ型が登録されている場合、元の型に代えてその型を使用する。\ ``TEST_X9``\ ・\ ``TEST_SX9``\ に\ :java:extdoc:`StringDataType <nablarch.test.core.file.StringDataType>`\ を割り当てると、数値としての変換を行わずにテストデータの記述がそのまま入出力される。

.. important::

  ``convertorTable``\ を設定すると、データ型の対応表はここで指定した内容に置き換わる。テスト用のデータ型だけを記述すると、それ以外のデータ型が使用できなくなるため、既定の対応表の内容も併せて記述する。

.. code-block:: xml

  <component name="fixedLengthConvertorSetting"
             class="nablarch.core.dataformat.convertor.FixedLengthConvertorSetting">
    <property name="convertorTable">
      <map>
        <!-- 既定の対応表 -->
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
