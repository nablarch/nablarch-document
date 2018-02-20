.. _`format`:

フォーマッタ
==================================================

.. contents:: 目次
  :depth: 3
  :local:

.. toctree::
  :maxdepth: 1
  :hidden:

機能概要
---------------------------------------------------------------------

日付型や数値型などのデータをフォーマットして文字列型に変換する機能を提供する。
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

フォーマッタの設定を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
本機能は特に設定をしない場合でも、フレームワークがデフォルトでサポートしている
フォーマッタを利用できる。フォーマット対象のデータ型に合わせて、フォーマッタを複数サポートしている。

デフォルトのフォーマットパターンの変更や、フォーマッタの追加をしたい場合は、
:ref:`format_custom`　を参照してシステムリポジトリに設定を追加すること。

フォーマッタを使用する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

フォーマットをする際は
:java:extdoc:`FormatterUtil <nablarch.core.text.FormatterUtil>`
を使用する。

呼び出す際に、使用するフォーマッタ名、フォーマット対象、フォーマットのパターンを指定する。
明示的にフォーマットのパターンを指定しない場合は、フォーマッタ毎に設定されたデフォルトのパターンでフォーマットする。

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
  :widths: 20,40,40

  * - フォーマッタ名
    - フォーマットするデータの型
    - デフォルトのフォーマットパターン

  * - :ref:`dateTime <format_datetime>`
    - :java:extdoc:`Date <java.util.Date>`
    - yyyy/MM/dd

  * - :ref:`number <format_number>`
    - :java:extdoc:`Number <java.lang.Number>`
    - デフォルトのロケールに対応したパターン


.. _`format_dateTime`:

dateTime
  日時のフォーマット。

  フォーマット対象の型は :java:extdoc:`Date <java.util.Date>` である。
  パターンには
  :java:extdoc:`SimpleDateFormat <java.text.SimpleDateFormat>`
  が規定している構文を指定する。
  デフォルトのパターンはyyyy/MM/ddである。

.. _`format_number`:

number
  数値のフォーマット。

  フォーマット対象の型は :java:extdoc:`Number <java.lang.Number>` である。
  パターンには
  :java:extdoc:`DecimalFormat <java.text.DecimalFormat>`
  が規定している構文を指定する。
  パターンを指定しない場合はデフォルトロケールに対して、デフォルトのパターンでフォーマットする。

実際に使用する場合
  例えば、データバインドを利用してファイルに出力する際に本機能を利用したい場合は、
  Beanのgetterで使用するとよい。

  実装例

  .. code-block:: java

    import java.util.Date;

    public class SampleDto {
        private Date startDate;
        private Integer sales;
        // getter & setter は省略

        // フォーマットされた文字列を取得するgetterを作成
        public String getFormattedStartDate() {
            return FormatterUtil.format("dateTime", startDate);
        }

        public String getFormattedSales() {
            return FormatterUtil.format("number", sales, "#,### 円");
        }
    }


.. _`format_custom`:

フォーマッタの設定を変更する
---------------------------------------------------------------------

以下を実現したい場合は、システムリポジトリに設定を追加する必要がある。

 * フレームワークがサポートしているフォーマッタのデフォルトのフォーマットパターンを変更する
 * 新たにフォーマッタを追加する

``nablarch.core.text.FormatterConfig`` がフォーマッタのリストを保持している。リストのプロパティ名は ``formatters`` を指定する。

フォーマッタのコンポーネントをリストに追加する。
``formatterName`` にフォーマッタの名前を、``defaultPattern`` にデフォルトのフォーマットパターンを設定する。

フレームワークがデフォルトでサポートしているフォーマットに対する設定例を以下に示す。

.. code-block:: xml

  <component name="formatter-config" class="nablarch.core.text.FormatterConfig">
    <!-- フォーマッタを保持するリスト -->
    <property name="formatters">
      <list>
        <!-- フレームワークがサポートしているフォーマッタクラス -->
        <component class="nablarch.core.text.DateTimeFormatter">
          <!-- フォーマッタを呼び出す際に使用する名前 -->
          <property name="formatterName" value="dateTime" />
          <!-- デフォルトのフォーマットパターンの設定 -->
          <property name="defaultPattern" value="yyyy/MM/dd" />
        </component>
        <!-- フレームワークがサポートしているフォーマッタクラス -->
        <component class="nablarch.core.text.NumberFormatter">
          <!-- フォーマッタを呼び出す際に使用する名前 -->
          <property name="formatterName" value="number" />
          <!-- デフォルトのフォーマットパターンの設定 -->
          <property name="defaultPattern" value="#,###,##0.000" />
        </component>
      </list>
    </property>
  </component>

.. important::
  コンポーネント定義でデフォルトのフォーマッタの設定を変更する場合は、
  変更を加えないフォーマッタやプロパティに関しても必ず 設定を記述すること。

フォーマットは、
:java:extdoc:`Formatter <nablarch.core.text.Formatter>`
インタフェースを実装したクラスが行う。

実装したクラスをコンポーネント定義に追加することでフォーマッタを追加することができる。

.. important::
  新たに追加したフォーマッタに加え、デフォルトのフォーマッタも使用したい場合は
  コンポーネント定義にデフォルトのフォーマッタも定義すること。コンポーネント定義に記述がない場合は
  デフォルトのフォーマッタは使用できない。
