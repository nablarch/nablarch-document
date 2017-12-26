.. _jsr310_adaptor:

JSR310(Date and Time API)アダプタ
==================================================

.. contents:: 目次
  :depth: 3
  :local:
  
JSR310(Date and Time API)で追加された日時関連を利用可能にするためのアダプタを提供する。
このアダプタを使用することで、 :ref:`bean_util` でJSR310(Date and Time API)を利用できる。

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

変換可能な型や変換ルールなどの詳細は、 :java:extdoc:`converter一覧 <nablarch.integration.jsr310.beans.converter>` を参照。

設定
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
      