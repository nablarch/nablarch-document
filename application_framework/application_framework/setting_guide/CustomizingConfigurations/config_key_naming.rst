
==========================
 環境設定値の項目名ルール
==========================

Nablarchが提供するデフォルト設定には、個別PJにてカスタマイズしやすいように
あらかじめ項目が抽出されている。その名称の命名ルールを記載する。

全般的なルール
==============

* 項目名は、lowerCamelCaseで記述する。
* 区切り文字に\ ``.``\ （ドット）を使用する。

共通プレフィックス
==================

Nablarchがデフォルトで用意する設定項目の項目名には、プレフィックス\ ``nablarch.``\ が付与される。
これにより、このプレフィックスが名前空間となり、適用PJと項目名が重複することを防止することができる。
また、ある設定項目が、Nablarchデフォルトのものか、PJで個別に作成したものかを判別することができる。

**【例】**

.. code-block:: bash
                
  # コードを起動時に読み込むかどうか
  nablarch.codeCache.loadOnStartUp=true


.. tip::
   PJが個別に作成する項目については、所定のプレフィックスを付与することを推奨する。
   これはPJ個別の項目を検索しやすくするためである。


単一のコンポーネント内でのみ使用される設定項目
==============================================

この場合、以下のルールで命名される。

``nablarch.<コンポーネント名>.<プロパティ名>``


前述の例で説明する。

.. code-block:: bash
                
  # コードを起動時に読み込むかどうか
  nablarch.codeCache.loadOnStartUp=true

この設定項目は、実際は以下のコンポーネント定義で使用される。
  
.. code-block:: xml
                
  <!-- コンポーネント名は 'codeCache' -->
  <component name="codeCache"
             class="nablarch.core.cache.BasicStaticDataCache">
             
    <!-- プロパティ名は 'loadOnStartUp' -->             
    <property name="loadOnStartup" value="${nablarch.codeCache.loadOnStartUp}"/>
              
    <!-- 中略 -->
  </component>
  
この場合、
``codeCache``\ がコンポーネント名称、\ ``loadOnStartUp``\ がそのコンポーネントのプロパティである。
これに、前述の\ `共通プレフィックス`_\ が付与されるので、\ ``nablarch.codeCache.loadOnStartUp``\ となる。


このルールにより、ある項目がどのコンポーネントで使用されるものであるか調査が容易になる。


複数のコンポーネント定義に跨る設定項目
======================================

この場合、以下のルールで命名される。


``nablarch.commonProperty.<項目名>``


   
DBテーブルのスキーマ情報
========================

Nablarch Application Frameworkが使用するテーブルのスキーマ情報については、
以下のルールで命名される。

``nablarch.<Nablarchデフォルトのテーブル名>Table.<各種設定値>``

例えば、メッセージ機能で使用するデフォルトのテーブル名は\ ``MESSAGE``\ であるので、
その項目名は以下のようになる。

**【例】**

.. code-block:: bash
                
  # メッセージテーブルのテーブル物理名
  nablarch.messageTable.tableName=MESSAGE
  # メッセージテーブルのIDカラム物理名
  nablarch.messageTable.idColumnName=MESSAGE_ID
  # メッセージテーブルの言語カラム物理名
  nablarch.messageTable.langColumnName=LANG
  # メッセージテーブルのメッセージカラム物理名
  nablarch.messageTable.valueColumnName=MESSAGE


.. tip::
   Nablarch Application Frameworkが使用するテーブルをデフォルト値のまま使用する場合は、
   この設定値を意識する必要はない。
