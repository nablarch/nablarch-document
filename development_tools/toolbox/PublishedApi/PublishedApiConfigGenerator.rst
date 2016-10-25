.. _published_api:

==================================
使用許可API一覧作成ツール
==================================

.. contents:: 目次
  :depth: 2
  :local:

概要
====

本ツールは、使用不許可APIチェックツールの設定ファイルとなる公開APIの一覧と、公開APIのJavadocを生成する。

生成される使用許可API一覧をそのまま「使用不許可APIチェックツール」の設定ファイルとして利用することで、
プロジェクトで実装した基盤部品などについて、業務アプリからの利用を想定していない非公開APIが利用されていないかどうかを使用不許可APIチェックツールを利用してチェックすることができる。

Nablarchが提供する公開APIの一覧は、以下のURLから取得できる。
使用しているNablarchバージョンに対応したファイルをtagから取得すること。

https://github.com/nablarch/nablarch-single-module-archetype/tree/master/nablarch-web/tools/static-analysis/findbugs/published-config (外部サイト)

各ファイルの詳細は :doc:`../UnpublishedMethodDetector/UnpublishedApi` を参照すること。


ツール配置場所
==============

本ツールはnablarch-toolbox-XXX.jarの一部であり、maven antrun plugin を使用してantのJavadocタスクとして実行する。[1]_
詳細は、\ `使用方法`_\ の項を参照。

.. [1] maven javadoc pluginを使用した場合、タグの複数入力機能が動作しなくなるため、maven antrun pluginからantのjavadocタスクを使用している。

使用方法
========

本ツールは、Javadocを生成する際に利用するDocletとして提供される。

Javadoc生成時に以下のDocletを利用し、必要なオプションを渡すことで使用許可API一覧および使用許可APIのみが出力されているJavadocが生成される。

**本ツールが提供するDoclet**
  nablarch.tool.published.doclet.PublishedDoclet

**必要な引数**

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 3,12,3


  * - 引数
    - 説明
    - 必須

  * - output
    - 使用許可API一覧の出力先ファイルを指定する。|br|
      使用不許可APIチェックツールの設定ファイルとして利用する場合には、拡張子を **config** とすること。
    - ○

  * - tag
    - 出力対象とするタグを指定する。カンマ区切りで複数指定することができる。
    - ×

**出力対象**
  nablarch.core.util.annotation.Publishedアノテーションの付与された、

    * クラス
    * コンストラクタ
    * メソッド
    * フィールド
    * アノテーション

  が出力対象となる。

  引数tagに出力対象タグが指定されている場合、該当するtag属性が指定されているPublishedアノテーションが付与されたものと、
  tag属性が指定されていないPublishedアノテーションが付与されたものが出力対象となる。

  引数tagが指定されない場合には、tag属性が指定されていないPublishedアノテーションが付与されたものが出力対象となる。


ツールの設定方法
---------------------------------

本ツールを利用するためには、antのjavadocタスクに以下の設定を行う。

============================ =============================================================== ================================================
設定項目                     設定値                                                          備考
============================ =============================================================== ================================================
**docletタグ**
---------------------------------------------------------------------------------------------------------------------------------------------
docletタグ                   nablarch.tool.published.doclet.PublishedDoclet
**paramタグ**
---------------------------------------------------------------------------------------------------------------------------------------------
-output                      ファイル出力先パス                                              必ず設定する必要がある
-tag                         出力対象とするタグ                                              引数tagを指定しない場合は、この設 |br|
                                                                                             定は不要
============================ =============================================================== ================================================

tools内のnablarch-tools.xmlに以下のターゲットを追記する。Nablarchが提供するアーキタイプから作成したプロジェクトにはあらかじめ設定されている。

.. code-block:: xml


    <target name="PublishedDoclet">
      <javadoc sourcepath="${executed.project.basedir}/src/main/java" 
               destdir="${executed.project.basedir}/target/apidocs"
               Encoding="UTF-8"
               classpathref="classpath.common"
               failonerror="false" >
        <!-- docletタグで、使用許可API一覧作成ツールのDocletクラスと、必要なクラスパスを設定する。 -->
        <doclet name="nablarch.tool.published.doclet.PublishedDoclet" pathref="classpath.common">
          <!-- 出力対象とするタグを指定する。指定しない場合には不要。 -->
          <param name="-tag" value="${publish_config_tag}"/>
          <!-- 使用許可API一覧の出力先ファイルを指定する。 -->
          <param name="-output" value="${nablarch.tools.dir}/static-analysis/findbugs/published-config/production/${publish_config_name}.config"/>
        </doclet>
      </javadoc>
    </target>
    

ツールの実行方法
---------------------------------

下記の場合のツール実行例を記載する。

* 出力先ファイルパス：tools/static-analysis/findbugs/published-config/production/Test.config
* 出力対象①：@Publishedアノテーションが付加されており、「architect」タグが指定されているクラス
* 出力対象②：@Publishedアノテーションが付加されており、タグが指定されていないクラス

.. code-block:: xml

    mvn antrun:run -Dtarget=PublishedDoclet -Dpublish_config_name=Test -Dpublish_config_tag=architect


.. |br| raw:: html

  <br />