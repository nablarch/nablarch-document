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

.. important::

  本アダプタで対応している型は以下の通り。
  これら以外の型を扱いたい場合は、プロジェクト側でConverterの追加などを行う必要がある。
  
  * :java:extdoc:`LocalDate <java.time.LocalDate>`
  * :java:extdoc:`LocalDateTime <java.time.LocalDateTime>`

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

変換可能な型や変換ルールなどの詳細は、 :java:extdoc:`converter一覧 <nablarch.integration.jsr310.beans.converter>` を参照。

使用方法
  :ref:`repository` のコンポーネント設定ファイルに以下を追加することで、本機能が有効になる。

  .. code-block:: xml

      <import file="JSR310.xml" />

.. tip::
 
  文字列から変換する際のフォーマットを変更したい場合は、以下の作業が必要となる。
  
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
データベースアクセス機能で、JSR310(Date and Time API)を扱いたい場合に利用する。
データベースとの入出力時の変換ルールの詳細は、 :java:extdoc:`converter一覧 <nablarch.integration.jsr310.db.converter>` を参照。

ユニバーサルDAO
 :ref:`universal_dao` では、登録時に指定するEntityクラスや検索結果を受け取るクラスのプロパティでLocalDateなどが利用できる。
  
データベースアクセス(JDBCラッパー)
  :ref:`database` 機能の場合は、 :java:extdoc:`SqlPStatement#setObject <nablarch.core.db.statement.SqlPStatement.setObject(int-java.lang.Object)>` でLocalDateなどが利用できる。
  
  データベースからの取得結果( :java:extdoc:`SqlRow <nablarch.core.db.statement.SqlRow>` )は、型変換の対象外となる。

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

