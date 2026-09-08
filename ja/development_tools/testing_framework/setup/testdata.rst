.. _testdata_setting:

テストデータの設定（形式・配置・記述の省略）
==================================================

.. contents:: 目次
  :depth: 3
  :local:

機能概要
--------------------------------------------------
テストデータの設定は、テストデータの形式・配置・記述の省略に関わる設定で、テストの種類によらず共通である。\ Excel\ 形式のテストデータを\ ``src/test/java``\ 配下に置くデフォルトのまま使う場合、設定は要らない。

使用方法
--------------------------------------------------

.. _testdata_setting-yaml:

テストデータの形式をYAMLに変更する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
テストデータは、デフォルトでは\ Excel\ 形式で読み込まれる。\ Excel\ 形式で記述する場合、設定は不要である。

YAML\ 形式で記述する場合は、\ ``nablarch-testing-yaml``\ を依存関係に追加する。\ YAML\ 形式のテストデータを解析するクラスは、このモジュールが提供する。

.. code-block:: xml

  <!-- YAML形式のテストデータ -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-testing-yaml</artifactId>
    <scope>test</scope>
  </dependency>

あわせて、テストデータを解析するコンポーネント\ ``testDataParser``\ を\ :java:extdoc:`YamlTestDataParser <nablarch.test.core.reader.YamlTestDataParser>`\ に差し替える。特殊記法を解釈するクラス（Interpreter）は、\ :ref:`テスト用のコンポーネント設定ファイル <testing_framework_introduction-test_component_config>`\ がimportしているデフォルト設定\ ``nablarch/test/test-data.xml``\ に、\ Excel\ 形式用として5つ定義されている。\ YAML\ 形式では、そのうち次の2つだけを\ ``interpreters``\ に指定する。

``testDataParser``\ は1つのコンポーネントであるため、1つのプロジェクトでExcel形式とYAML形式のテストデータを混在させることはできない。既存のExcel形式のテストデータは、\ :ref:`テストデータ変換ツール <testdata_converter>`\ でYAML形式に変換する。

- ``dateTimeInterpreter``\ … ``${systemTime}``\ ・\ ``${updateTime}``\ ・\ ``${setUpTime}``\ を日時に変換する
- ``compositeInterpreter``\ … ``${文字種,文字数}``\ を、その文字種の文字列に変換する

残りの3つ（\ ``nullInterpreter``\ ・\ ``quotationTrimmer``\ ・\ ``lineSeparatorInterpreter``\ ）は、null・ダブルクォート・改行を\ Excel\ のセル値から読み取るためのもので、\ YAML\ では構文がその役割を担うため指定しない。

.. code-block:: xml

  <!-- テストデータを解析するコンポーネント -->
  <component name="testDataParser" class="nablarch.test.core.reader.YamlTestDataParser">
    <property name="dbInfo" ref="dbInfo"/>
    <property name="interpreters">
      <list>
        <component-ref name="dateTimeInterpreter"/>
        <component-ref name="compositeInterpreter"/>
      </list>
    </property>
  </component>

``dbInfo``\ には、テーブルの主キー・カラム名・カラム型をデータベースのメタデータから取得する\ :java:extdoc:`DbInfo <nablarch.test.core.db.DbInfo>`\ の実装を指定する。この名前のコンポーネントは\ ``nablarch/test/test-data.xml``\ には含まれないため、テスト用のコンポーネント設定ファイルで\ :java:extdoc:`GenericJdbcDbInfo <nablarch.test.core.db.GenericJdbcDbInfo>`\ などの実装を\ ``dbInfo``\ という名前で登録する。

``testDataReader``\ は指定しない。\ :java:extdoc:`YamlTestDataParser <nablarch.test.core.reader.YamlTestDataParser>`\ は\ YAML\ ファイルを直接読み込むため、この設定を使用しない。

.. _testdata_setting-base_dir:

テストデータの読み込み先を変更する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
テストデータは、デフォルトでは\ ``src/test/java``\ 配下から読み込まれる。プロジェクトのディレクトリ構成に合わせて読み込み先を変更する場合は、環境設定ファイルに\ ``nablarch.test.resource-root``\ を設定する。値には、テスト実行時のカレントディレクトリからの相対パスを指定する。

.. code-block:: properties

  nablarch.test.resource-root=path/to/test-data-dir

読み込み先は、セミコロン（\ ``;``\ ）で区切って複数指定できる。

.. code-block:: properties

  nablarch.test.resource-root=test/online;test/batch

.. important::

  同名のテストデータが複数のディレクトリに存在する場合、最初に見つかったものが読み込まれる。

.. _testdata_setting-column_default_values:

省略したテーブルのカラムのデフォルト値を変更する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データベースの準備データや\ ``EXPECTED_COMPLETE_TABLE``\ でカラムの記述を省略した場合、そのカラムにはカラム型に応じたデフォルト値が設定されているものとして扱われる（\ :ref:`カラムを省略する <testdata_notation-column_omission>`\ を参照）。このデフォルト値は\ :java:extdoc:`BasicDefaultValues <nablarch.test.core.db.BasicDefaultValues>`\ で変更できる。テストデータを解析するコンポーネントの\ ``defaultValues``\ プロパティに指定する。

.. list-table::
  :class: white-space-normal
  :header-rows: 1
  :widths: 25,35,40

  * - 設定項目名
    - 説明
    - 指定できる値
  * - ``charValue``
    - 文字列型のデフォルト値。固定長文字列型（\ CHAR\ ・\ NCHAR\ ）では、指定した値をカラム長の数だけ繰り返した文字列が使われる
    - 1文字のASCII文字
  * - ``numberValue``
    - 数値型のデフォルト値。カラム長を超える値を指定した場合は、先頭からカラム長の分だけ切り出した値が使われる
    - 0または正の整数
  * - ``dateValue``
    - 日付型のデフォルト値
    - JDBCタイムスタンプエスケープ形式（\ ``yyyy-mm-dd hh:mm:ss.fffffffff``\ ）

記述例を示す。

.. code-block:: xml

  <!-- TestDataParser -->
  <component name="testDataParser" class="nablarch.test.core.reader.BasicTestDataParser">
    <!-- データベース情報 -->
    <property name="dbInfo" ref="dbInfo"/>
    <!-- データベースのデフォルト値 -->
    <property name="defaultValues">
      <component class="nablarch.test.core.db.BasicDefaultValues">
        <property name="charValue" value="a"/>
        <property name="numberValue" value="1"/>
        <property name="dateValue" value="2000-01-01 12:34:56.123456789"/>
      </component>
    </property>
    <!-- 中略 -->
  </component>

.. _testdata_setting-directive_defaults:

ディレクティブのデフォルト値を設定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ファイルのディレクティブがシステム内である程度統一されている場合、個々のファイルデータブロックに同じディレクティブを繰り返し記述することになる。コンポーネント設定ファイルにデフォルト値をmap形式で登録すると、この記述を省略できる。mapの\ ``name``\ 属性には、デフォルト値を適用するファイルの種別に応じて次の名前を指定する。

.. list-table::
  :class: white-space-normal
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

指定できるディレクティブキーはファイルの種別ごとに決まっており、それ以外のキー名を指定するとエラーになる。\ ``defaultDirectives``\ は固定長ファイル・可変長ファイルの両方に適用されるため、共通のデフォルト値には両方の種別で有効なキーだけを設定する。片方の種別にしかないキーを設定すると、もう一方の種別のテストデータを読み込む時点でエラーになる。ディレクティブキーの一覧は\ :ref:`ファイルのデータを記述する <testdata_notation-file_data>`\ を参照。

.. _testdata_setting-test_data_types:

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

拡張例
--------------------------------------------------

.. _testdata_setting-test_data_converter:

テストデータの変換処理を実装する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
電文のテストデータに記述した値は、デフォルトではテストデータのディレクティブ\ ``text-encoding``\ に指定したエンコーディングでバイト列に変換されるだけである。例えば、URLエンコードされたデータが外部システムから連携される場合、URLエンコード済みの値をテストデータに記述することになり、可読性や保守性、作業効率の面で現実的ではない。テスティングフレームワークは、読み込んだテストデータに定型的な変換処理を加える手段を提供する。

拡張するには\ :java:extdoc:`TestDataConverter <nablarch.test.core.file.TestDataConverter>`\ を実装する。XMLやJSONといったデータ形式ごとに、必要に応じてアーキテクトが用意する。実装するメソッドは次の2つである。

.. list-table::
  :class: white-space-normal
  :header-rows: 1
  :widths: 35,65

  * - メソッド
    - 実装する内容
  * - ``convertData``
    - テストデータに記述されたデータを、任意の値に変換する
  * - ``createDefinition``
    - 変換後のデータに対応するレイアウト定義を動的に生成する

実装したクラスは、テスト用のコンポーネント設定ファイルに\ ``TestDataConverter_``\ で始まるコンポーネント名で登録する。\ ``TestDataConverter_``\ に続く部分には、テストデータのディレクティブ\ ``file-type``\ に指定した値を使う。

.. code-block:: xml

  <!-- テストデータコンバータ -->
  <component name="TestDataConverter_FormUrlEncoded"
             class="com.example.test.core.file.FormUrlEncodedTestDataConverter"/>

登録したコンバータは、\ ``file-type``\ に\ ``FormUrlEncoded``\ を指定した電文のテストデータに適用される。URLエンコードを行うコンバータを実装しておけば、テストデータに日本語のまま記述した値が、URLエンコード済みの値を記述した場合と同じように扱われる。

.. tip::

  ``file-type``\ の値は、応答電文のアサート方式にも影響する。電文のテストデータの記述方法とあわせて\ :ref:`メッセージングのデータを記述する <testdata_notation-messaging_data>`\ を参照。
