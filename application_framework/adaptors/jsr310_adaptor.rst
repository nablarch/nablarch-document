.. _jsr310_adaptor:

JSR310(Date and Time API)アダプタ
==================================================

.. contents:: 目次
  :depth: 3
  :local:
  
JSR310(Date and Time API)で追加された日時関連を利用可能にするためのアダプタを提供する。
このアダプタを使用することで、以下の機能でJSR310(Date and Time API)を利用できる。

* :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <!-- JSR310アダプタ -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-jsr310-adaptor</artifactId>
  </dependency>

BeanUtilでJSR310(Date and Time API)を利用する
--------------------------------------------------
:java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` でJSR310(Date and Time API)を扱いたい場合に利用する。
本機能を使用することで、プロパティ値のコピー時にLocalDate等への型変換や移送が行われるようになる。

変換可能な型や変換ルールなどの詳細は、 :java:extdoc:`converter一覧 <nablarch.integration.jsr310.beans.converter>` を参照。

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
    
  



