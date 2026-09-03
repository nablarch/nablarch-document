.. _entity_unit_test:

エンティティ単体テスト
==================================================

.. contents:: 目次
  :depth: 3
  :local:

機能概要
--------------------------------------------------

エンティティ単体テストは、\ Form\ クラスと\ Entity\ クラスを対象とするクラス単体テストである。テスティングフレームワークが入力値の生成・バリデーションの実行・結果の確認を行うため、プロパティごとの条件をテストデータに記述するだけで、文字種と文字列長を網羅したテストを実施できる。

テストクラスは\ :java:extdoc:`EntityTestSupport <nablarch.test.core.db.EntityTestSupport>`\ をインジェクションして作成する。入力値・期待するバリデーションメッセージ・期待値はテストデータに記述し、テストクラスにはサポートクラスのメソッドを呼び出すテストコードだけを書く。バリデーションの実行と結果の確認は、呼び出したメソッドの内部で行われる。

このページで扱う主なクラスとリソースを次に示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 1
  :widths: 30,45,25

  * - 名称
    - 役割
    - 作成単位
  * - テストクラス
    - テストデータの読み込み単位を指定して、サポートクラスのメソッドを呼び出す。
    - テスト対象クラスにつき1つ作成する。
  * - テストデータ
    - 入力値・期待するバリデーションメッセージ・期待値を記述する。
    - 確認する対象につき1つの読み込み単位を作成する。
  * - テスト対象クラス
    - テストされる\ Form\ クラスまたは\ Entity\ クラス。
    - －
  * - ``EntityTestSupport``
    - 入力値の生成、バリデーションの実行、結果の確認を行うメソッドを提供する。
    - －

.. tip::

  Form\ と\ Entity\ の責務については、処理方式ごとの責務配置を参照（\ :ref:`ウェブアプリケーションの責務配置 <application_design>`\ 、\ :ref:`Nablarchバッチアプリケーションの責務配置 <nablarch_batch-application_design>`\ ）。

エンティティ単体テストで確認する対象は、次の6つに分かれる。テスト対象クラスが使用するバリデーション方式によって、実施する対象と使用するメソッドが変わる。

.. list-table::
  :class: white-space-normal
  :header-rows: 1
  :widths: 35,35,30

  * - 確認する対象
    - 使用するメソッド
    - 対象となるバリデーション方式
  * - 文字種と文字列長の単項目バリデーション
    - ``testValidateCharsetAndLength``
    - 両方
  * - その他の単項目バリデーション
    - ``testSingleValidation``
    - 両方
  * - setter\ と\ getter
    - ``testSetterAndGetter``
    - 両方
  * - 相関バリデーション
    - ``testBeanValidation``
    - :ref:`bean_validation`
  * - バリデーションメソッド
    - ``testValidateAndConvert``
    - :ref:`nablarch_validation`
  * - コンストラクタ
    - ``testConstructorAndGetter``
    - :ref:`nablarch_validation`

.. important::

  どちらのバリデーション方式を使用するかは、\ ``validationTestStrategy``\ の設定で決まる（\ :ref:`クラス単体テストの設定 <class_unit_test_setting>`\ ）。設定した方式に対応しない\ ``testBeanValidation``\ または\ ``testValidateAndConvert``\ を呼び出すと、\ ``UnsupportedOperationException``\ が発生する。\ ``testConstructorAndGetter``\ にはこの検査が無く、\ ``Map``\ を引数にとるコンストラクタが無い場合はデフォルトコンストラクタが使用されるため、\ Bean Validation\ を設定したクラスに対して呼び出しても例外は発生しない。

使用方法
--------------------------------------------------

エンティティ単体テストは、テストクラスとテストデータを作成し、\ JUnit\ でテストを実行するという流れで進める。テストの実行に先立って、期待するメッセージ\ ID\ のデフォルト値と入力値を生成するクラスを\ :ref:`クラス単体テストの設定 <class_unit_test_setting>`\ に従って設定しておく。

テストクラスを作成する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
テストクラスは、次の条件を満たすように作成する。

* パッケージは、テスト対象のクラスと同じとする。
* クラス名は\ ``<テスト対象クラス名>Test``\ とする。
* :java:extdoc:`EntityTest <nablarch.test.junit5.extension.db.EntityTest>`\ をテストクラスに設定し、\ :java:extdoc:`EntityTestSupport <nablarch.test.core.db.EntityTestSupport>`\ 型のフィールドを宣言する。

.. code-block:: java

  package com.example.web.form;   // テスト対象クラスと同じパッケージ

  import nablarch.test.core.db.EntityTestSupport;
  import nablarch.test.junit5.extension.db.EntityTest;
  import org.junit.jupiter.api.Test;

  @EntityTest
  class UserRegistrationFormTest {

      EntityTestSupport support;

      /** テスト対象クラス。 */
      static final Class<?> TARGET_CLASS = UserRegistrationForm.class;

      // テストメソッドは後述
  }

.. tip::

  JUnit 4\ でテストを書く場合は、インジェクションではなく継承でテスティングフレームワークの機能を使用する（\ :ref:`JUnit 4での使用 <junit4_support>`\ ）。

テストメソッドを作成する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
確認する対象ごとに、テストデータに用意するカラムと、呼び出すサポートクラスのメソッドを示す。テストメソッドには、テストデータの読み込み単位の名前とデータブロックの\ ID\ を指定してサポートクラスのメソッドを呼び出すコードだけを書く。両方のバリデーション方式に共通する3つを先に示し、続いて方式ごとに固有の3つを示す。

文字種と文字列長をテストする
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
単項目バリデーションは、入力される文字種と文字列長に関するものがほとんどである。例えば、最大文字列長50文字・必須入力・全角カタカナのみを許容するプロパティであれば、全角カタカナ50文字・全角カタカナ51文字・全角カタカナ1文字・空文字・許容しない文字種の入力といったテストショットが必要になり、プロパティ1つあたりのテストショット数が多くなる。

このテスト方法では、プロパティの条件を1行に記述するだけで、必要なテストショットがすべて自動的に実行される。テストデータの作成が容易になり、条件が一覧の形になるためレビューと保守もしやすくなる。

.. important::

  このテスト方法は、プロパティとして別の\ Form\ を保持する\ Form\ には使用できない。この場合はバリデーションのテストを個別に実装する。プロパティとして別の\ Form\ を保持する\ Form\ とは、\ ``<親Form>.<子Form>.<子Formのプロパティ名>``\ という形式でプロパティにアクセスする親\ Form\ のことである。

テストデータは\ ``LIST_MAP``\ のデータブロックとして記述し、プロパティ1つにつき1行を記述する。使用するカラムを次に示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 1
  :widths: 30,45,25

  * - カラム名
    - 記載内容
    - 使用できる方式
  * - ``propertyName``
    - テスト対象のプロパティ名。
    - 両方
  * - ``allowEmpty``
    - そのプロパティが未入力を許容するか。
    - 両方
  * - ``min``
    - 入力値として許容する最小文字列長（省略可）。
    - 両方
  * - ``max``
    - 入力値として許容する最大文字列長。\ Bean Validation\ では省略できる。
    - 両方
  * - ``messageIdWhenEmptyInput``
    - 未入力時に期待するメッセージ（省略可）。
    - 両方
  * - ``messageIdWhenInvalidLength``
    - 文字列長が不適合な場合に期待するメッセージ（省略可）。
    - 両方
  * - ``messageIdWhenNotApplicable``
    - 文字種が不適合な場合に期待するメッセージ。
    - 両方
  * - 文字種のカラム
    - その文字種を許容するか。カラム名には文字種の名前をそのまま使う。
    - 両方
  * - ``group``
    - Bean Validation\ のグループ（省略可）。グループに指定するクラスを\ FQCN\ で指定する。内部クラスを指定する場合は\ ``$``\ で区切る。
    - Bean Validation
  * - ``interpolateKey_``\ *n*
    - 埋め込み文字のキー名（\ *n*\ は1からの連番。省略可）。
    - Bean Validation
  * - ``interpolateValue_``\ *n*
    - 埋め込み文字の値（\ *n*\ は1からの連番。省略可）。
    - Bean Validation

.. important::

  ``propertyName``\ ・\ ``allowEmpty``\ ・\ ``min``\ ・\ ``max``\ ・\ ``messageIdWhenNotApplicable``\ は、値が空欄であってもカラム自体を用意する。カラムが無い場合はテストの実行時にエラーになる。

  また、上記以外のカラムはすべて文字種のカラムとみなされる。カラム名を誤って記述すると、その名前の文字種を生成できずにテストの実行時にエラーになる。

文字種のカラム名には、\ ``characterGenerator``\ に設定したクラスが生成できる文字種の名前を指定する。\ :java:extdoc:`BasicJapaneseCharacterGenerator <nablarch.test.core.util.generator.BasicJapaneseCharacterGenerator>`\ を設定した場合に指定できる文字種は、半角英字・半角数字・半角記号・半角カナ・全角英字・全角数字・全角ひらがな・全角カタカナ・全角漢字・全角記号その他・中国語・サロゲートペア・改行・外字である。

許容するかどうかを記入するカラム（\ ``allowEmpty``\ と文字種のカラム）には、次の値を設定する。

.. list-table::
  :class: white-space-normal
  :header-rows: 1
  :widths: 30,20,50

  * - 設定内容
    - 設定値
    - 備考
  * - 許容する
    - ``o``
    - 半角英小文字のオー
  * - 許容しない
    - ``x``
    - 半角英小文字のエックス

メッセージを指定するカラムには、バリデーションエラー時に期待するメッセージを記載する。記載の形式は、バリデーション方式によって次のように異なる。

* Bean Validation\ の場合は、メッセージをそのまま記載する。メッセージ内の\ ``{}``\ で囲まれた部分は\ :ref:`埋め込み文字を使用する <message-format-spec>`\ で述べる埋め込み文字とみなされる。メッセージ全体を\ ``{}``\ で囲んだ場合はメッセージ\ ID\ とみなされ、\ :ref:`message`\ で解決される。
* Nablarch Validation\ の場合は、メッセージ\ ID\ を記載する。

Bean Validation\ での記載例を次に示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 1
  :widths: 50,50

  * - 記載例
    - 説明
  * - ``入力必須です。``
    - メッセージをそのまま記載した場合（埋め込み文字なし）
  * - ``{min}文字以上{max}文字以下で入力してください。``
    - メッセージをそのまま記載した場合（埋め込み文字あり）
  * - ``{nablarch.core.validation.ee.SystemChar.message}``
    - メッセージ\ ID\ としてメッセージを記載した場合

``messageIdWhenInvalidLength``\ を省略した場合は、\ :ref:`クラス単体テストの設定 <class_unit_test_setting>`\ で設定したデフォルト値が使用される。どのデフォルト値が使用されるかは、\ ``max``\ 欄と\ ``min``\ 欄の記載によって次のように決まる。\ ``messageIdWhenEmptyInput``\ を省略した場合は、同じく設定した\ ``emptyInputMessageId``\ の値が使用される。

.. list-table::
  :class: white-space-normal
  :header-rows: 1
  :widths: 15,15,20,50

  * - ``max``\ 欄
    - ``min``\ 欄
    - 両者の比較
    - 使用されるデフォルト値
  * - あり
    - なし
    - （該当なし）
    - ``maxMessageId``
  * - あり
    - あり
    - ``max`` > ``min``
    - 超過時は\ ``maxAndMinMessageId``\ 、不足時は\ ``underLimitMessageId``
  * - あり
    - あり
    - ``max`` = ``min``
    - ``fixLengthMessageId``
  * - なし
    - あり
    - （該当なし）
    - ``minMessageId``\ （\ Bean Validation\ の場合のみ。\ Nablarch Validation\ では\ ``max``\ を省略できない）

サポートクラスの次のメソッドを起動すると、テストデータの1行ごとに、次表の観点でテストが実行される。

.. code-block:: java

  void testValidateCharsetAndLength(Class entityClass, String sheetName, String id)

.. list-table::
  :class: white-space-normal
  :header-rows: 1
  :widths: 20,40,40

  * - 観点
    - 入力値
    - テストが実行されない条件
  * - 文字種
    - その文字種で構成した文字列。長さは\ ``max``\ とし、\ ``max``\ を省略した場合は\ ``min``\ 、両方を省略した場合は1とする。
    - なし（文字種のカラムの数だけ実行される）
  * - 未入力
    - 長さ0の文字列
    - なし
  * - 最短文字列長
    - ``min``\ の長さの文字列
    - なし
  * - 最長文字列長
    - ``max``\ の長さの文字列
    - ``max``\ を省略した場合
  * - 文字列長不足
    - ``min``\ から1を引いた長さの文字列
    - ``min``\ が1以下の場合
  * - 文字列長超過
    - ``max``\ に1を足した長さの文字列
    - ``max``\ を省略した場合

文字種のテストでは、\ ``o``\ を設定した文字種はバリデーションエラーが発生しないこと、\ ``x``\ を設定した文字種は\ ``messageIdWhenNotApplicable``\ のメッセージが発生することを確認する。未入力のテストでは、\ ``allowEmpty``\ が\ ``o``\ ならバリデーションエラーが発生しないこと、\ ``x``\ なら\ ``messageIdWhenEmptyInput``\ のメッセージが発生することを確認する。文字種以外の観点の入力値は、\ ``o``\ を設定した文字種で構成される。このため、\ ``o``\ を設定した文字種が1つも無い行があると、テストの実行時にエラーになる。

.. tip::

  ``min``\ を省略した場合の最小文字列長は、\ ``allowEmpty``\ が\ ``o``\ なら0、\ ``x``\ なら1として扱われる。いずれの場合も文字列長不足のテストは実行されない。

テストメソッドの記述例を次に示す。

.. code-block:: java

  /** 文字種と文字列長の単項目バリデーション */
  @Test
  void testCharsetAndLength() {
      String sheetName = "testCharsetAndLength";
      String id = "charsetAndLength";
      support.testValidateCharsetAndLength(TARGET_CLASS, sheetName, id);
  }

その他の単項目バリデーションをテストする
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
文字種と文字列長のテストでは大部分の単項目バリデーションをテストできるが、日付項目のフォーマットや数値項目の範囲のように、これでカバーできないものもある。このような単項目バリデーションは、プロパティごとに入力値と期待するメッセージのペアを記述してテストする。このテスト方法も、前述のとおりプロパティとして別の\ Form\ を保持する\ Form\ には使用できない。

テストデータは\ ``LIST_MAP``\ のデータブロックとして記述し、テストショット1件につき1行を記述する。使用するカラムを次に示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 1
  :widths: 30,45,25

  * - カラム名
    - 記載内容
    - 使用できる方式
  * - ``propertyName``
    - テスト対象のプロパティ名。
    - 両方
  * - ``case``
    - テストショットの簡単な説明。
    - 両方
  * - ``input1``
    - 入力値。1つのプロパティに複数の値を指定する場合は、\ ``input2``\ ・\ ``input3``\ ...とカラムを増やす。
    - 両方
  * - ``messageId``
    - その入力値で単項目バリデーションを実行した場合に発生すると期待するメッセージ。バリデーションエラーにならないことを期待する場合は空欄にする。
    - 両方
  * - ``group``
    - Bean Validation\ のグループ（省略可）。指定方法は文字種と文字列長のテストと同じである。
    - Bean Validation
  * - ``interpolateKey_``\ *n*
    - 埋め込み文字のキー名（\ *n*\ は1からの連番。省略可）。
    - Bean Validation
  * - ``interpolateValue_``\ *n*
    - 埋め込み文字の値（\ *n*\ は1からの連番。省略可）。
    - Bean Validation

``propertyName``\ ・\ ``input1``\ ・\ ``messageId``\ は必須のカラムである。メッセージの記載形式は、文字種と文字列長のテストと同じである。入力値は\ :ref:`null・空文字・改行など特殊な値を記述する <testdata_notation-special_notation>`\ の特殊記法を使うと効率よく作成できる。

サポートクラスの次のメソッドを起動する。

.. code-block:: java

  void testSingleValidation(Class entityClass, String sheetName, String id)

.. code-block:: java

  /** その他の単項目バリデーション */
  @Test
  void testSingleValidation() {
      String sheetName = "testSingleValidation";
      String id = "singleValidation";
      support.testSingleValidation(TARGET_CLASS, sheetName, id);
  }

setterとgetterをテストする
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
setter\ で設定した値が\ getter\ で期待どおりに取得できることを確認する。対象となるのは、テスト対象クラスに定義されているすべてのプロパティである。ただし、この方法でテストできるプロパティの型には後述の制限があり、制限に該当する型のプロパティは個別にテストする。

テストデータは\ ``LIST_MAP``\ のデータブロックとして記述し、プロパティ1つにつき1行を記述する。使用するカラムを次に示す。

.. list-table::
  :class: white-space-normal
  :header-rows: 1
  :widths: 20,80

  * - カラム名
    - 記載内容
  * - ``name``
    - プロパティ名。
  * - ``set``
    - setter\ に渡す値。空欄にした行は\ setter\ を呼び出さない。
  * - ``get``
    - getter\ から取得される期待値。空欄にした行は確認しない。

サポートクラスの次のメソッドを起動する。テスト対象クラスのインスタンスを生成し、\ ``set``\ の値を\ setter\ で設定したうえで、\ getter\ から取得した値が\ ``get``\ の値と等しいことを確認する。

.. code-block:: java

  void testSetterAndGetter(Class entityClass, String sheetName, String id)

.. code-block:: java

  /** setterとgetterのテスト */
  @Test
  void testSetterAndGetter() {
      String sheetName = "testSetterAndGetter";
      String id = "setterAndGetter";
      support.testSetterAndGetter(TARGET_CLASS, sheetName, id);
  }

.. important::

  Entity\ は自動生成されるため、アプリケーションで使用されない\ setter\ と\ getter\ が生成される可能性がある。これらはリクエスト単体テストではテストできないため、エンティティ単体テストで必ずテストする。一方、一般的な\ Form\ にはアプリケーションで使用する\ setter\ と\ getter\ だけを作成するため、リクエスト単体テストでテストできる。この場合、エンティティ単体テストでテストする必要はない。

.. tip::

  ``testSetterAndGetter``\ でテストできるプロパティの型には、次の制限がある。

  * String\ 、および\ String\ の配列
  * BigDecimal\ 、および\ BigDecimal\ の配列
  * java.util.Date\ 、および\ java.util.Date\ の配列（テストデータには\ ``yyyy-MM-dd``\ 形式または\ ``yyyy-MM-dd HH:mm:ss``\ 形式で記述する）
  * ``valueOf(String)``\ メソッドを持つクラス、およびその配列（例えば\ Integer\ 、\ Long\ 、\ java.sql.Date\ 、\ java.sql.Timestamp\ など）

  これらに該当しない型のプロパティは、テストクラスで\ setter\ と\ getter\ を明示的に呼び出してテストする。テストデータは別の\ ID\ のデータブロックに記述し、\ ``getParamMap``\ （テスト対象のプロパティが複数ある場合は\ ``getListParamMap``\ ）で取得する。次の例は、\ ``List<String>``\ 型のプロパティ\ ``users``\ を個別にテストしている。

  .. code-block:: java

    /** setterとgetterのテスト */
    @Test
    void testSetterAndGetter() {
        String sheetName = "testSetterAndGetter";

        // 共通にテストできるプロパティ
        support.testSetterAndGetter(TARGET_CLASS, sheetName, "setterAndGetter");

        // 共通にテストできないプロパティ
        Map<String, String[]> data = support.getParamMap(sheetName, "setterAndGetterOther");
        UserRegistrationForm form = new UserRegistrationForm();
        form.setUsers(Arrays.asList(data.get("set")));
        assertEquals(Arrays.asList(data.get("get")), form.getUsers());
    }

.. tip::

  setter\ や\ getter\ にロジックを記述した場合（例えば、\ setter\ は郵便番号を上3桁と下4桁に分けて受け取るが、\ getter\ は7桁をまとめて返す場合など）は、そのロジックを確認するテストショットも作成する。

相関バリデーションをテストする
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ここで示すのは、\ :ref:`bean_validation`\ を使用する場合のテストである。\ :java:extdoc:`@AssertTrue <jakarta.validation.constraints.AssertTrue>`\ を指定した相関バリデーションなど、単項目バリデーションのテストではテストできないものは、別にテストを作成する。

テストデータには、テストショット一覧（\ ``testShots``\ ）と入力パラメータ（\ ``params``\ ）を記述する。必須カラムと両者の対応は\ :ref:`テストショット一覧（testShots）を記述する <testdata_notation-test_shots>`\ に従う。記述例は\ :ref:`テストショット一覧（testShots）を記述する <testdata_examples-test_shots>`\ のうち、エンティティバリデーションの例を参照。相関バリデーションのテストでは、必須カラムに加えて次のカラムを使用できる。

.. list-table::
  :class: white-space-normal
  :header-rows: 1
  :widths: 35,65

  * - カラム名
    - 記載内容
  * - ``description``
    - テストショットの簡単な説明。
  * - ``group``
    - Bean Validation\ のグループ（省略可）。指定方法は文字種と文字列長のテストと同じである。
  * - ``interpolateKey``\ *n*\ ``_``\ *k*
    - 埋め込み文字のキー名（\ *n*\ は\ ``expectedMessageId``\ *n*\ の\ *n*\ に対応し、\ *k*\ は1からの連番。省略可）。
  * - ``interpolateValue``\ *n*\ ``_``\ *k*
    - 埋め込み文字の値（\ *n*\ ・\ *k*\ の意味は上記と同じ。省略可）。

テストショット一覧には、バリデーションエラーが発生するプロパティ名と、そのプロパティのバリデーションエラーメッセージだけを記載する。バリデーションエラーが発生しないプロパティは記載しない。入力パラメータには、相関バリデーションで検証したいプロパティの値に加えて、入力必須のプロパティの値も記載する。入力値は\ :ref:`null・空文字・改行など特殊な値を記述する <testdata_notation-special_notation>`\ の特殊記法を使うと効率よく作成できる。

.. tip::

  プロパティとして保持している別の\ Form\ のプロパティは、次のように指定できる。

  .. code-block:: java

    public class SampleForm {
        /** システムユーザ */
        private SystemUserEntity systemUser;
        /** 電話番号配列 */
        private UserTelEntity[] userTelArray;
    }

  保持している\ Form\ のプロパティ（\ ``SystemUserEntity``\ の\ ``userId``\ ）を指定する場合は次のように記述する。

  .. code-block:: text

    sampleForm.systemUser.userId

  Form\ の配列の要素のプロパティ（\ ``UserTelEntity``\ の配列の先頭要素）を指定する場合は次のように記述する。

  .. code-block:: text

    sampleForm.userTelArray[0].telNoArea

サポートクラスの次のメソッドを起動する。テストショット一覧の\ ID\ は\ ``testShots``\ で固定であるため、引数に\ ID\ を指定しない。

.. code-block:: java

  void testBeanValidation(Class entityClass, String sheetName)

.. code-block:: java

  /** 相関バリデーションのテスト */
  @Test
  void testWholeFormValidation() {
      String sheetName = "testWholeFormValidation";
      support.testBeanValidation(TARGET_CLASS, sheetName);
  }

バリデーションメソッドをテストする
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ここで示すのは、\ :ref:`nablarch_validation`\ を使用する場合のテストである。単項目バリデーションのテストでは、\ setter\ に付与したアノテーションが正しいかは確認されるが、\ Entity\ に実装したバリデーションメソッド（\ ``@ValidateFor``\ を付与した\ static\ メソッド）は実行されない。独自のバリデーションメソッドを実装した場合は、別にテストを作成する。

テストデータには、テストショット一覧（\ ``testShots``\ ）と入力パラメータ（\ ``params``\ ）を記述する。必須カラムと両者の対応は\ :ref:`テストショット一覧（testShots）を記述する <testdata_notation-test_shots>`\ に従い、テストショットの簡単な説明を記載する\ ``description``\ カラムを加えられる。記述例は\ :ref:`テストショット一覧（testShots）を記述する <testdata_examples-test_shots>`\ のうち、エンティティバリデーションの例を参照。入力値は\ :ref:`null・空文字・改行など特殊な値を記述する <testdata_notation-special_notation>`\ の特殊記法を使うと効率よく作成できる。

テストショットは、次の2つの観点で作成する。

1. バリデーション対象プロパティの指定が正しいことを確認する。すべてのプロパティに対して、それぞれ単項目バリデーションエラーとなる入力値を用意し、期待値としてバリデーション対象プロパティのプロパティ名と、そのプロパティの単項目バリデーションエラー時のメッセージ\ ID\ を記載する。指定が正しければ、バリデーション対象のプロパティだけがバリデーションエラーになる。
2. 相関バリデーションなど、バリデーション対象の指定以外の動作を確認する。

.. tip::

  バリデーション対象プロパティが誤ってバリデーション対象から漏れていた場合、期待したメッセージが出力されないためメッセージ\ ID\ の確認が失敗する。逆にバリデーション対象でないプロパティが誤ってバリデーション対象になっていた場合は、入力値が不正であるため単項目バリデーションが失敗し、期待しないメッセージが出力される。これによりバリデーション対象の誤りを検出できる。

サポートクラスの次のメソッドを起動する。\ ``validateFor``\ には、\ ``@ValidateFor``\ に指定した値を渡す。

.. code-block:: java

  void testValidateAndConvert(Class entityClass, String sheetName, String validateFor)

.. code-block:: java

  /** テスト対象エンティティクラス */
  static final Class<SystemAccountEntity> ENTITY_CLASS = SystemAccountEntity.class;

  /** バリデーションメソッドのテスト */
  @Test
  void testValidateForRegisterUser() {
      String sheetName = "testValidateForRegisterUser";
      String validateFor = "registerUser";
      support.testValidateAndConvert(ENTITY_CLASS, sheetName, validateFor);
  }

コンストラクタをテストする
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ここで示すのは、\ :ref:`nablarch_validation`\ を使用する場合のテストである。\ Nablarch Validation\ で入力値チェックを実施している\ Entity\ には、\ :ref:`nablarch_validation-execute`\ に記載のとおり\ ``Map<String, Object>``\ を引数にとるコンストラクタが実装される。このコンストラクタに指定した値が、正しくプロパティに設定されることを確認する。対象となるのは、テスト対象クラスに定義されているすべてのプロパティである。

テストデータの記述方法は、前述の\ setter\ と\ getter\ のテストと同じである。\ ``name``\ ・\ ``set``\ ・\ ``get``\ のカラムを持つ\ ``LIST_MAP``\ のデータブロックとして記述する。\ ``set``\ に記載した値がコンストラクタの引数となり、\ ``get``\ に記載した値が\ getter\ から取得される期待値となる。テストできるプロパティの型の制限も、\ setter\ と\ getter\ のテストと同じである。

サポートクラスの次のメソッドを起動する。

.. code-block:: java

  void testConstructorAndGetter(Class entityClass, String sheetName, String id)

.. code-block:: java

  /** コンストラクタのテスト */
  @Test
  void testConstructor() {
      String sheetName = "testAccessor";
      String id = "testConstructor";
      support.testConstructorAndGetter(ENTITY_CLASS, sheetName, id);
  }

.. important::

  コンストラクタについても、\ setter\ と\ getter\ のテストで述べたのと同じ理由から、\ Entity\ ではエンティティ単体テストで必ずテストし、一般的な\ Form\ ではテストする必要がない。

テストデータを作成する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
テストデータの格納場所と記述方法は\ :ref:`テストデータの書き方 <testdata_notation>`\ に従う。記述例は\ :ref:`文字種と文字列長のテストデータを記述する <testdata_examples-charset_and_length>`\ ・\ :ref:`setterとgetterのテストデータを記述する <testdata_examples-setter_and_getter>`\ 、およびエンティティバリデーションの例（\ :ref:`テストショット一覧（testShots）を記述する <testdata_examples-test_shots>`\ ）を参照。

確認する対象ごとに、1つの読み込み単位（\ Excel\ 形式ではシート、\ YAML\ 形式ではファイル）を使用する。

メッセージデータやコードマスタなど、データベースに格納する静的マスタデータは、プロジェクトで管理されたデータがあらかじめ投入されていることを前提とする。テストデータとして個別に作成しない。

テストを実行する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
通常の\ JUnit\ テストと同じように実行する。

テスト結果を確認する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
バリデーションの実行結果と\ getter\ の戻り値の確認は、起動したサポートクラスのメソッドの内部で行われる。テストメソッドに確認のコードを書く必要はない。ただし、\ setter\ と\ getter\ のテストで型の制限に該当しないプロパティを個別にテストする場合は、\ JUnit\ の\ ``assertEquals``\ などで確認する。

テストが失敗した場合、どのテストショットが失敗したかを特定できるように、次の情報がメッセージとして出力される。

.. list-table::
  :class: white-space-normal
  :header-rows: 1
  :widths: 40,60

  * - 確認する対象
    - 出力される情報
  * - 文字種と文字列長の単項目バリデーション
    - どの観点のテストか（最長文字列長・文字列長超過・未入力・文字種など）、対象のプロパティ名、期待したメッセージ、実際に発生したメッセージ、入力値とその文字列長
  * - その他の単項目バリデーション
    - 対象のプロパティ名、期待したメッセージ、実際に発生したメッセージ、入力値とその文字列長（観点は出力されない）
  * - 相関バリデーション、バリデーションメソッド
    - ``title``\ カラムに記載した内容
  * - setter\ と\ getter\ 、コンストラクタ
    - ``name``\ カラムに記載したプロパティ名

.. tip::

  相関バリデーションとバリデーションメソッドのテストでは、失敗時に出力されるのが\ ``title``\ カラムの内容だけである。テストショットを識別できる内容を\ ``title``\ に記載する。その他の単項目バリデーションのテストでは\ ``case``\ カラムの内容が出力されないため、失敗したテストショットはプロパティ名と入力値から特定する。
