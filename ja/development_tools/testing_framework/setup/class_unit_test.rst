.. _class_unit_test_setting:

クラス単体テストの設定
==================================================

.. contents:: 目次
  :depth: 3
  :local:

機能概要
--------------------------------------------------
クラス単体テストの設定は、エンティティ単体テストとコンポーネント単体テストに固有の設定である。エンティティ単体テストでは、文字種・文字列長のテストで期待するメッセージIDのデフォルト値など、プロジェクトの規約に合わせる項目を登録する。コンポーネント単体テストでデフォルト以外のトランザクションも使う場合は、そのトランザクションを環境設定ファイルに指定する。

使用方法
--------------------------------------------------

エンティティ単体テストの設定項目を登録する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
文字種と文字列長の単項目バリデーションのテストでは、テスティングフレームワークが文字種と文字列長を変えた入力値を自動的に生成してバリデーションを実行し、発生したメッセージIDを期待値と比較する。このうち文字列長が不正な場合と未入力の場合に期待するメッセージIDのデフォルト値と、入力値の生成やバリデーションの実行に使うクラスは、\ :java:extdoc:`EntityTestConfiguration <nablarch.test.core.entity.EntityTestConfiguration>`\ で設定する。テスト用のコンポーネント設定ファイルに、\ ``entityTestConfiguration``\ という名前で登録する。なお、文字種が適合しない場合に期待するメッセージIDにデフォルト値は無く、文字種と文字列長のテストデータの必須カラム\ ``messageIdWhenNotApplicable``\ で行ごとに指定する。

.. list-table::
  :class: white-space-normal
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

.. _class_unit_test_setting-db_transaction:

コンポーネント単体テストでデフォルト以外のトランザクションを使用する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
コンポーネント単体テストでは、テストメソッドの実行前後に、\ :java:extdoc:`DbAccessTestSupport <nablarch.test.core.db.DbAccessTestSupport>`\ がデフォルトのデータベーストランザクションを開始・終了する。これ以外のトランザクションも使用する場合は、テスト用のコンポーネント設定ファイルに\ :java:extdoc:`SimpleDbTransactionManager <nablarch.core.db.transaction.SimpleDbTransactionManager>`\ を登録し、環境設定ファイルの\ ``dbAccessTest.dbTransactionName``\ にそのコンポーネント名を記述する。複数指定する場合はカンマで区切る。指定した名前のコンポーネントが登録されていない場合は、テストメソッドの実行前に例外が発生する。デフォルトのトランザクションは、この記述の有無にかかわらず開始される。この設定を読むのは\ :java:extdoc:`DbAccessTestSupport <nablarch.test.core.db.DbAccessTestSupport>`\ だけであり、リクエスト単体テストには影響しない。

.. code-block:: properties

  dbAccessTest.dbTransactionName=employeeTransaction,departmentTransaction
