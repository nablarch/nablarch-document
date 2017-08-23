.. _jsr310_adaptor:

JSR310(Date and Time API)アダプタ
==================================================

.. contents:: 目次
  :depth: 3
  :local:
  
JSR310(Date and Time API)で追加された日時関連を利用可能にするためのアダプタを提供する。
このアダプタを使用することで、以下の機能でJSR310(Date and Time API)を利用できる。

* :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>`
* :ref:`database`
* :ref:`universal_dao`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <!-- JSR310アダプタ -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-jsr310-adaptor</artifactId>
  </dependency>
  
使用方法
---------------------------------------------------------------------

BeanUtilでJSR310(Date and Time API)を利用する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` でJSR310(Date and Time API)を扱いたい場合に利用する。
本機能を使用することで、プロパティ値のコピー時にLocalDate等への型変換や移送が行われるようになる。

変換可能な型や変換ルールなどの詳細は、 :java:extdoc:`converter一覧 <nablarch.integration.jsr310.beans.converter>` を参照。

使用方法
  :ref:`repository` のコンポーネント設定ファイルに以下を追加することで、本機能が有効になる。

  .. code-block:: xml

      <import file="JSR310.xml" />

.. tip::
 
  文字列からLocalDateなどへ変換する際のフォーマットを変更したい場合は、以下の作業が必要となる。
  
  フォーマットなどの定義を持つクラスを作成する
    :java:extdoc:`DateTimeConfiguration <nablarch.integration.jsr310.util.DateTimeConfiguration>` の実装クラスを追加し、
    日付や日時のフォーマットを定義する。
    基本実装の :java:extdoc:`BasicDateTimeConfiguration <nablarch.integration.jsr310.util.BasicDateTimeConfiguration>` を参考にすると良い
    
  追加したクラスをコンポーネント設定ファイルに定義する
    コンポーネント名を ``dateTimeConfiguration`` として、コンポーネント定義を行う。
    
    例を以下に示す。
    
    .. code-block:: xml
    
      <component name="dateTimeConfiguration" class="sample.SampleDateTimeConfiguration" />
    
  
データベースアクセス機能(UniversalDao含む)でJSR310を利用する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
以下のデータベースアクセス機能で、JSR310(Date and Time API)を扱いたい場合に利用する。
データベースとの入出力時の変換ルールの詳細は、 :java:extdoc:`converter一覧 <nablarch.integration.jsr310.db.converter>` を参照。

ユニバーサルDAO
 :ref:`universal_dao` では、データベースとの入出力でJSR310を使用できる。
 例えば、登録時に指定するEntityクラスや検索結果を受け取るクラスで :java:extdoc:`LocalDate <java.time.LocalDate>` や
 :java:extdoc:`LocalDateTime <java.time.LocalDateTime>` が使用できる。
  
データベースアクセス(JDBCラッパー)
  :ref:`database` 機能の場合は、データベースの出力時にJSR310を扱えるようになる。
  例えば、 :java:extdoc:`SqlPStatement#setObject <nablarch.core.db.statement.SqlPStatement.setObject(int-java.lang.Object)>` で
  :java:extdoc:`LocalDate <java.time.LocalDate>` や :java:extdoc:`LocalDateTime <java.time.LocalDateTime>` を指定できる。
  
  データベースからの取得結果の場合は、:java:extdoc:`SqlRow <nablarch.core.db.statement.SqlRow>` から取得した値を必要に応じて変換すること。

使用方法
  :ref:`repository` のコンポーネント設定ファイルに以下を追加し、変換ルールをDialectに設定することで本機能が利用できる状態となる。

  .. code-block:: xml

      <import file="JSR310.xml" />
      
      <!--
      Dialectに対して、コンバータを設定する。
      
      設定するコンポーネント名は「attributeConverter」
      Dialectクラスは、使用するデータベースに応じて変更すること
      -->
      <component name="dialect" class="nablarch.core.db.dialect.H2Dialect">
        <property name="attributeConverterFactory" ref="attributeConverter" />
      </component>
