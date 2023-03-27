.. _`format`:

フォーマッタ
==================================================

.. contents:: 目次
  :depth: 3
  :local:

機能概要
---------------------------------------------------------------------

日付や数値などのデータをフォーマットして文字列型に変換する機能を提供する。
フォーマットの設定を本機能に集約することで、画面やファイル、メールなど形式毎に
設定をする必要がなくなる。


モジュール一覧
---------------------------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core</artifactId>
  </dependency>

使用方法
---------------------------------------------------------------------

フォーマッタの設定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
本機能は特に設定をしない場合でも、フレームワークがデフォルトでサポートしている
フォーマッタを使用できる。

デフォルトのフォーマットパターンの変更や、フォーマッタの追加をしたい場合は、
:ref:`format_custom` を参照してシステムリポジトリに設定を追加すること。

フォーマッタを使用する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

フォーマットをする際は
:java:extdoc:`FormatterUtil <nablarch.core.text.FormatterUtil>`
を使用する。

フォーマッタは、使用するフォーマッタを特定するためにクラス名とは別にフォーマッタ名を持つ。

FormatterUtil.formatを呼び出す際、フォーマッタ名、フォーマット対象、フォーマットのパターンを指定するが、
フォーマット名とフォーマット対象のデータ型に応じて、適切なフォーマッタが選択される。

選択されたフォーマッタと指定されたフォーマットのパターンを使用してフォーマットされる。
明示的にフォーマットのパターンを指定しない場合は、フォーマッタ毎に設定されたデフォルトのパターンが使用される。

実装例

.. code-block:: java

  // デフォルトのパターンを使用してフォーマットする場合
  // 第1引数に使用したいフォーマッタの名前を指定する
  // 第2引数にフォーマットしたい値を指定する
  FormatterUtil.format("dateTime", input);

  // パターンを指定してフォーマットする場合
  // 第1、第2引数はデフォルトのパターンの時と同様
  // 第3引数に使用したいフォーマットのパターンを指定する。
  FormatterUtil.format("dateTime", input, "yyyy年MM月dd日");

本機能でデフォルトで提供しているフォーマッタを以下に示す。

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 20,40,40,40

  * - フォーマッタ名
    - フォーマットするデータの型
    - デフォルトのフォーマットパターン
    - 備考

  * - :ref:`dateTime <format_datetime>`
    - :java:extdoc:`Date <java.util.Date>`
    - yyyy/MM/dd
    -

  * - :ref:`dateTime <format_datetime>`
    - :java:extdoc:`String <java.lang.String>`
    - yyyy/MM/dd
    - フォーマット対象の日付文字列のパターンが必要(デフォルトは ``yyyyMMdd`` )

  * - :ref:`number <format_number>`
    - :java:extdoc:`Number <java.lang.Number>`
    - #,###.###
    -

  * - :ref:`number <format_number>`
    - :java:extdoc:`String <java.lang.String>`
    - #,###.###
    -

.. _`format_dateTime`:

dateTime
  日付をフォーマットするフォーマッタ。

  フォーマット対象の型は :java:extdoc:`Date <java.util.Date>` 及びその派生クラスと :java:extdoc:`String <java.lang.String>` である。
  パターンには
  :java:extdoc:`SimpleDateFormat <java.text.SimpleDateFormat>`
  が規定している構文を指定する。
  デフォルトのパターンは ``yyyy/MM/dd`` である。

  :java:extdoc:`String <java.lang.String>` 型をフォーマットする場合は、フォーマット対象となる日付文字列のパターンも設定する必要がある。
  デフォルトでは、フォーマット対象の日付文字列のパターンは ``yyyyMMdd`` となっている。
  設定を変更したい場合は :ref:`format_custom` を参照すること。

.. _`format_number`:

number
  数値をフォーマットするフォーマッタ。

  フォーマット対象の型は :java:extdoc:`Number <java.lang.Number>` の派生クラスと :java:extdoc:`String <java.lang.String>` である。
  パターンには
  :java:extdoc:`DecimalFormat <java.text.DecimalFormat>`
  が規定している構文を指定する。
  デフォルトのパターンは ``#,###.###`` である。

使用例
  例えば、データバインドを使用してファイルに出力する際に本機能を使用したい場合は、
  Beanのgetterで使用するとよい。

  .. code-block:: java

    import java.util.Date;

    public class SampleDto {
        private Date startDate;
        private Integer sales;

        // フォーマットされた文字列を取得するgetterを作成
        public String getFormattedStartDate() {
            return FormatterUtil.format("dateTime", startDate);
        }

        public String getFormattedSales() {
            return FormatterUtil.format("number", sales, "#,### 円");
        }

        // 他の getter & setter は省略
    }


.. _`format_custom`:

フォーマッタの設定を変更する
---------------------------------------------------------------------

フォーマッタの設定を変更するには、以下の手順が必要となる。

コンポーネント設定ファイルに ``nablarch.core.text.FormatterConfig`` の設定をする。

  ポイント
   * コンポーネント名は ``formatterConfig`` とすること。

  ``nablarch.core.text.FormatterConfig`` に使用するフォーマッタのリストの設定をする。
  リストのプロパティ名は ``formatters`` とすること。


  以下に、フレームワークがデフォルトでサポートしているフォーマッタの初期設定を示す。

  .. code-block:: xml

    <component name="formatterConfig" class="nablarch.core.text.FormatterConfig">
      <!-- フォーマッタを保持するリスト -->
      <property name="formatters">
        <list>
          <component class="nablarch.core.text.DateTimeFormatter">
            <!-- フォーマッタを呼び出す際に使用する名前 -->
            <property name="formatterName" value="dateTime" />
            <!-- デフォルトのフォーマットパターンの設定 -->
            <property name="defaultPattern" value="yyyy/MM/dd" />
          </component>
          <component class="nablarch.core.text.DateTimeStrFormatter">
            <property name="formatterName" value="dateTime" />
            <property name="defaultPattern" value="yyyy/MM/dd" />
            <!-- 日付文字列のフォーマッタは、日付文字列のパターンを表すプロパティも設定する必要がある -->
            <property name="dateStrPattern" value="yyyyMMdd" />
          </component>
          <component class="nablarch.core.text.NumberFormatter">
            <property name="formatterName" value="number" />
            <property name="defaultPattern" value="#,###.###" />
          </component>
          <component class="nablarch.core.text.NumberStrFormatter">
            <property name="formatterName" value="number" />
            <property name="defaultPattern" value="#,###.###" />
          </component>
        </list>
      </property>
    </component>

  .. important::
    コンポーネント定義でデフォルトのフォーマッタの設定を変更する場合は、
    変更を加えないフォーマッタやプロパティに関しても必ず設定を記述すること。
    コンポーネント定義に記述がないフォーマッタは使用できない。


フォーマッタを追加する
---------------------------------------------------------------------

フォーマッタを追加する場合は、以下の手順が必要となる。

1. :java:extdoc:`Formatter <nablarch.core.text.Formatter>` の実装クラスを作成する。

  フォーマット処理は :java:extdoc:`Formatter <nablarch.core.text.Formatter>` を実装したクラスが行う。


2. コンポーネント設定ファイルに作成したフォーマッタの設定を追加する

  :ref:`format_custom` を参照して、コンポーネント設定ファイルに ``nablarch.core.text.FormatterConfig`` とフォーマッタのリストの設定を行う。

  .. code-block:: xml

    <component name="formatterConfig" class="nablarch.core.text.FormatterConfig">
      <property name="formatters">
        <list>
          <!-- デフォルトのフォーマッタ -->
          <component class="nablarch.core.text.DateTimeFormatter">
            <property name="formatterName" value="dateTime" />
            <property name="defaultPattern" value="yyyy/MM/dd" />
          </component>
          <component class="nablarch.core.text.DateTimeStrFormatter">
            <property name="formatterName" value="dateTime" />
            <property name="defaultPattern" value="yyyy/MM/dd" />
            <property name="dateStrPattern" value="yyyyMMdd" />
          </component>
          <component class="nablarch.core.text.NumberFormatter">
            <property name="formatterName" value="number" />
            <property name="defaultPattern" value="#,###.###" />
          </component>
          <component class="nablarch.core.text.NumberStrFormatter">
            <property name="formatterName" value="number" />
            <property name="defaultPattern" value="#,###.###" />
          </component>
          <!-- 追加したフォーマッタ -->
          <component class="sample.SampleFormatter">
            <property name="formatterName" value="sample" />
            <property name="defaultPattern" value="#,### 円" />
          </component>
        </list>
      </property>
    </component>
