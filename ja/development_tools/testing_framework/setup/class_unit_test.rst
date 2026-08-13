.. _class_unit_test_setting:

クラス単体テストの設定
==================================================

.. contents:: 目次
  :depth: 3
  :local:

クラス単体テストでは、エンティティ単体テストで使用する設定項目と、データベースを使用するクラスのテストでカラムの記述を省略したときのデフォルト値を設定できる。いずれもテスト用のコンポーネント設定ファイルに記述する。

使用方法
--------------------------------------------------

エンティティ単体テストの設定項目を登録する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
文字種と文字列長の単項目バリデーションのテストでは、テスティングフレームワークが文字種と文字列長を変えた入力値を自動的に生成してバリデーションを実行し、発生したメッセージIDを期待値と比較する。このうち文字列長が不正な場合と未入力の場合に期待するメッセージIDのデフォルト値と、入力値の生成やバリデーションの実行に使うクラスは、\ :java:extdoc:`EntityTestConfiguration <nablarch.test.core.entity.EntityTestConfiguration>`\ で設定する。テスト用のコンポーネント設定ファイルに、\ ``entityTestConfiguration``\ という名前で登録する。なお、文字種が適合しない場合に期待するメッセージIDにデフォルト値は無く、文字種と文字列長のテストデータの必須カラム\ ``messageIdWhenNotApplicable``\ で行ごとに指定する。

.. list-table::
  :header-rows: 1
  :widths: 30,70

  * - 設定項目名
    - 説明
  * - ``maxMessageId``
    - 最大文字列長だけを指定した項目で、文字列長が超過した場合に期待するメッセージID
  * - ``maxAndMinMessageId``
    - 最大文字列長と最小文字列長に異なる値を指定した項目で、文字列長が超過した場合に期待するメッセージID
  * - ``minMessageId``
    - 最小文字列長だけを指定した項目で、文字列長が不足した場合に期待するメッセージID。最大文字列長を省略できるBean Validationを使用する場合の設定項目である
  * - ``underLimitMessageId``
    - 最大文字列長と最小文字列長に異なる値を指定した項目で、文字列長が不足した場合に期待するメッセージID
  * - ``fixLengthMessageId``
    - 最大文字列長と最小文字列長に同じ値を指定した項目（固定長）で、文字列長が一致しない場合に期待するメッセージID。超過・不足のいずれの場合も使われる
  * - ``emptyInputMessageId``
    - 未入力の場合に期待するメッセージID
  * - ``characterGenerator``
    - テスト用の入力値を生成するクラス。\ :java:extdoc:`CharacterGenerator <nablarch.test.core.util.generator.CharacterGenerator>`\ の実装クラスを指定する。通常は\ :java:extdoc:`BasicJapaneseCharacterGenerator <nablarch.test.core.util.generator.BasicJapaneseCharacterGenerator>`\ を指定すればよい。指定を省略するとテストの実行時に例外が発生する
  * - ``validationTestStrategy``
    - 使用するバリデーション機能に対応するクラス。Bean Validationを使用する場合は\ :java:extdoc:`BeanValidationTestStrategy <nablarch.test.core.entity.BeanValidationTestStrategy>`\ を指定する。指定を省略した場合は、Nablarch Validation用の\ :java:extdoc:`NablarchValidationTestStrategy <nablarch.test.core.entity.NablarchValidationTestStrategy>`\ が使われる

メッセージIDは、いずれもデフォルト値として使われる。文字種と文字列長のテストデータで期待するメッセージIDを明示的に指定した場合は、そちらが優先される。文字列長に関する5つのメッセージIDのうちどれが使われるかは、テストデータに指定された最大文字列長（\ ``max``\ カラム）・最小文字列長（\ ``min``\ カラム）の組み合わせと、文字列長が超過したか不足したかで決まる。

.. important::

  Nablarch Validationを使用する場合、文字種と文字列長のテストデータには最大文字列長を必ず指定する。省略すると例外が発生するため、\ ``minMessageId``\ が使われることはない。Bean Validationを使用する場合は最大文字列長を省略できる。最大文字列長を省略した行で、最小文字列長に2以上を指定し、かつテストデータの\ ``messageIdWhenInvalidLength``\ カラムでメッセージIDを明示的に指定していないときは、\ ``minMessageId``\ の指定が必須である。指定していないと例外が発生する。

Bean Validationを使用する場合の記述例を示す。メッセージIDには、アノテーションで指定されているメッセージIDを\ ``{``\ 、\ ``}``\ で囲んだ形式で指定する。テスティングフレームワークが、この値を\ :java:extdoc:`MessageInterpolator <jakarta.validation.MessageInterpolator>`\ で変換して期待するメッセージを組み立てるためである。

.. code-block:: xml

  <!-- エンティティ単体テストの設定 -->
  <component name="entityTestConfiguration" class="nablarch.test.core.entity.EntityTestConfiguration">
    <property name="maxMessageId"        value="{nablarch.core.validation.ee.Length.max.message}"/>
    <property name="maxAndMinMessageId"  value="{nablarch.core.validation.ee.Length.min.max.message}"/>
    <property name="minMessageId"        value="{nablarch.core.validation.ee.Length.min.message}"/>
    <property name="underLimitMessageId" value="{nablarch.core.validation.ee.Length.min.max.message}"/>
    <property name="fixLengthMessageId"  value="{nablarch.core.validation.ee.Length.fixed.message}"/>
    <property name="emptyInputMessageId" value="{nablarch.core.validation.ee.Required.message}"/>
    <property name="characterGenerator">
      <component name="characterGenerator"
                 class="nablarch.test.core.util.generator.BasicJapaneseCharacterGenerator"/>
    </property>
    <property name="validationTestStrategy">
      <component class="nablarch.test.core.entity.BeanValidationTestStrategy"/>
    </property>
  </component>

Nablarch Validationを使用する場合の記述例を示す。

.. code-block:: xml

  <!-- エンティティ単体テストの設定 -->
  <component name="entityTestConfiguration" class="nablarch.test.core.entity.EntityTestConfiguration">
    <property name="maxMessageId"        value="MSG00011"/>
    <property name="maxAndMinMessageId"  value="MSG00011"/>
    <property name="underLimitMessageId" value="MSG00011"/>
    <property name="fixLengthMessageId"  value="MSG00023"/>
    <property name="emptyInputMessageId" value="MSG00010"/>
    <property name="characterGenerator">
      <component name="characterGenerator"
                 class="nablarch.test.core.util.generator.BasicJapaneseCharacterGenerator"/>
    </property>
  </component>

Nablarch Validationを使用する場合、ここで指定するメッセージIDは、バリデータ側のコンポーネント設定ファイルと一致させる。上記の記述例に対応するバリデータ側の設定を示す。

.. code-block:: xml

  <property name="validators">
    <list>
      <component class="nablarch.core.validation.validator.RequiredValidator">
        <property name="messageId" value="MSG00010"/>
      </component>
      <component class="nablarch.core.validation.validator.LengthValidator">
        <property name="maxMessageId" value="MSG00011"/>
        <property name="maxAndMinMessageId" value="MSG00011"/>
        <property name="fixLengthMessageId" value="MSG00023"/>
      </component>
      <!-- 中略 -->
    </list>
  </property>

.. _class_unit_test_setting-column_default_values:

省略したテーブルのカラムのデフォルト値を変更する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
データベースの準備データや\ ``EXPECTED_COMPLETE_TABLE``\ でカラムの記述を省略した場合、そのカラムにはカラム型に応じたデフォルト値が設定されているものとして扱われる（\ :ref:`カラムを省略する <testdata_notation-column_omission>`\ を参照）。このデフォルト値は\ :java:extdoc:`BasicDefaultValues <nablarch.test.core.db.BasicDefaultValues>`\ で変更できる。テストデータを解析するコンポーネントの\ ``defaultValues``\ プロパティに指定する。

.. list-table::
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
