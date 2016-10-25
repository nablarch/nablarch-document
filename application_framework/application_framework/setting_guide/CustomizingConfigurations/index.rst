==================================
デフォルト設定値からの設定変更方法
==================================

.. contents:: 目次
  :depth: 2
  :local:



設定ファイルの構成
==========================

Nablarchの設定は、デフォルトコンフィグレーション内の設定ファイルと、PJ成果物内の設定ファイルで構成される。


以下に設定ファイルの構成を示す。

.. image:: abstract.png

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 5,18


  * - モジュール
    - 説明

  * - デフォルトコンフィギュレーション(jar)
    - nablarch-main-default-configuration-XXXX.jarやnablarch-testing-default-configuration-XXXX.jarなどjar形式でパッケージされ、Mavenのアーティファクトとして配布される。|br|
      プレースホルダーに対する設定値が設定されている項目と、プレースホルダーのみが定義されている項目が存在する。|br|
      また、変更頻度の極めて低い項目については、プレースホルダー化されておらず直接値が設定されている。

  * - PJ成果物
    - Nablarchが提供するアーキタイプを使用した場合、デフォルトコンフィギュレーション(jar)への依存関係があらかじめ設定される。|br|
      PJ成果物のコンポーネント定義ファイルには、アーキタイプから生成した直後の状態で、初期値が設定された状態で提供されている。


カスタマイズ方法
======================

カスタマイズのパターン
----------------------

PJ成果物の設定ファイルのカスタマイズ方法には、以下のパターンが存在する。

* :ref:`how_to_customize_config_files`
* :ref:`how_to_customize_overwite_config_files`
* :ref:`how_to_customize_overwite_componet_file`
* :ref:`how_to_customize_handler_queue`

詳細は以降に記載する。


カスタマイズ作業手順
====================

.. _how_to_customize_config_files:

環境設定値の書き換え
--------------------

PJで変更する頻度が高い環境設定値については、アーキタイプで生成したブランクプロジェクトの環境設定ファイルに設定されている。

設定項目名の命名ルールについては、\ :doc:`config_key_naming`\ を参照。 


.. toctree::
   :maxdepth: 1
   :hidden:

   config_key_naming


TODOコメントの埋め込まれている設定項目を修正する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DBの接続設定等、プロジェクト毎にほぼ確実に修正する箇所には、環境設定ファイル(configファイル)にTODOコメントが埋め込まれているため、設定値を修正する。


デフォルト値でPJ要件を満たせない場合は、デフォルト値を変更する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

\ :download:`デフォルト設定一覧 <デフォルト設定一覧.xlsx>`\ を確認の上、デフォルト値でPJ要件を満たせない箇所については、環境設定ファイル(configファイル)を修正する。


.. _how_to_customize_overwite_config_files:

環境設定値の上書き
----------------------------------

デフォルトコンフィグレーションの環境設定ファイル(config)で設定されている環境設定値を上書きしたい場合は、同名のプレースホルダーで再定義する。

\ :download:`デフォルト設定一覧 <デフォルト設定一覧.xlsx>`\ でデフォルトコンフィグレーションで設定されている内容が確認できる。


.. _how_to_customize_overwite_componet_file:

コンポーネント定義の上書き
--------------------------------------

変更したいデフォルトコンフィグレーションのコンポーネント定義ファイルのコンポーネントのプロパティがプレースホルダー化されていない場合、
もしくはコンポーネント自体をプロジェクトでカスタマイズした別のクラスに変更したい場合、
PJ成果物のコンポーネント定義ファイルにコンポーネント定義ごと再定義する。

\ :download:`デフォルト設定一覧 <デフォルト設定一覧.xlsx>`\ でデフォルトコンフィグレーションで、プレースホルダーが使われていない設定を確認できる。

デフォルト設定からコンポーネント定義を変更する必要がある場合、以下の手順に従って
コンポーネントの再定義を行う。


同名のコンポーネントを定義する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

デフォルトコンフィグレーションのコンポーネント定義(xml)から、変更対象となるコンポーネントを特定し、そのコンポーネント名を取得する。


例えば、以下のコンポーネントを差し替える場合、コンポーネント名は\ ``idGenerator``\ であるとわかる。

.. code-block:: xml
  
  <!-- 採番モジュールの設定 -->
  <component name="idGenerator"
      class="nablarch.common.idgenerator.TableIdGenerator">
    <!-- 採番テーブルの定義 -->
    <property name="tableName" value="ID_GENERATE" />
    <property name="idColumnName" value="ID" />
    <property name="noColumnName" value="NO" />
  </component>


任意のコンポーネント定義ファイルに、差し替えたいコンポーネントと同名のコンポーネントを定義する。

**【再定義ファイルの中身】**

.. code-block:: xml

  <!-- 採番モジュールの設定(oracle sequenceを使用する) -->
  <component name="idGenerator"
             class="com.example.common.idgenerator.OracleSequenceIdGenerator">
    <property name="idTable">
      <map>
        <entry key="1101" value="USER_ID_SEQ"/>
      </map>
    </property>
  </component>


.. tip ::

  同名のコンポーネント定義が複数存在する場合は、後に記述した設定が優先される。

  このNablarchの仕様を使用して、コンポーネントの再定義を行う。


(コンポーネント定義ファイルを作成した場合)作成したコンポーネント定義ファイルの読み込み
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

コンポーネント定義ファイルの記述例を以下に示す。   

.. code-block:: xml

     <!-- 前略 -->
     <!-- 採番機能 -->
     <import file="nablarch/common/idgenerator.xml" />
    
     <!-- PJのコンポーネント定義を読み込み、デフォルトのコンポーネント定義を上書きする -->
     <import file="pj_component.xml"/>

     </component>
   </component-configuration>


.. _how_to_customize_handler_queue:

ハンドラ構成のカスタマイズ
------------------------------

生成されたコンポーネントのハンドラ構成をもとに、PJに必要なハンドラ構成を検討する。

以下にカスタマイズ例を挙げる。

* フィーチャフォン対応を実現するため、専用のハンドラを追加する。
* PJで使用しない機能のハンドラを除外する。

Mavenアーキタイプによって生成されたコンポーネント定義ファイル
(\ ``XXX_component_configuration.xml``\ )に
当該処理方式における最小ハンドラ構成が予め定義されている。
PJでハンドラ構成を変更する場合、このファイルを編集する。


設定変更例
==========

コンポーネント定義ファイルや環境設定ファイル(configファイル)の設定変更の具体例は以下を参照のこと。

* :doc:`CustomizeMessageIDAndMessage`
* :doc:`CustomizeAvailableCharacters`
* :doc:`CustomizeSystemTableName`


.. toctree::
   :maxdepth: 1
   :hidden:

   CustomizeMessageIDAndMessage
   CustomizeAvailableCharacters
   CustomizeSystemTableName


デフォルト設定一覧
====================
デフォルト設定一覧には、Nablarchが提供しているデフォルトコンフィグレーションで設定している設定値とブランクプロジェクトが設定している設定値が一覧形式で記述されている。

デフォルト設定一覧は、以下のリンクより取得できる。

:download:`デフォルト設定一覧.xlsx <デフォルト設定一覧.xlsx>`


.. |br| raw:: html

  <br />