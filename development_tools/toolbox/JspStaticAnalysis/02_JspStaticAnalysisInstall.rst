====================================
JSP静的解析ツール 設定変更ガイド
====================================

.. contents:: 目次
  :depth: 2
  :local:

:doc:`index`\ の設定変更方法について説明する。

前提条件
--------

* アーキタイプからブランクプロジェクトの生成が完了していること。


設定ファイル構成
----------------

設定ファイルの構成は下表の通り。

.. list-table::
  :header-rows: 1
  :class: white-space-normal
  :widths: 10,13


  * - ファイル名
    - 説明

  * - pom.xml
    - 起動に必要な設定と、jspanalysis.excludePatternsの設定を行う。

  * - tools/nablarch-tools.xml
    - Antタスクの定義ファイル [1]_ 。通常編集することはない。

  * - tools/static-analysis/jspanalysis/config.txt
    - JSP静的解析ツール設定ファイル。記述方法は、 :ref:`01_customJspAnalysis` を参照。

  * - tools/static-analysis/jspanalysis/transform-to-html.xsl
    - JSP静的解析結果XMLをHTMLに変換する際の定義ファイル。|br|
      記述方法は、 :ref:`01_outputJspAnalysis` の「JSP解析(XMLレポート出力)」を参照。

  * - nablarch-archetype-parentのpom.xml
    - jspanalysis.excludePatterns以外の設定を行う。




.. [1] 内部でAntを使用しているため存在する。利用者はMaven経由で実行するため通常意識することはない。

.. _01_customJspAnalysisProp:

pom.xmlの書き換え
-----------------------------------------------
JSP静的解析ツール用のプロパティを実行環境にあわせて修正する際は、jspanalysis.excludePatternsの修正であればツールを実行するプロジェクトのpom.xmlを修正する。それ以外の項目の修正であればnablarch-archetype-parentのpom.xmlを修正する。

================================  ======================================================================================
設定プロパティ                    説明
================================  ======================================================================================
jspanalysis.checkjspdir           チェック対象JSPディレクトリパスもしくはファイルパスを設定する。

                                  CI環境のように一括でチェックを実行する場合には、|br|
                                  ディレクトリパスを設定する。

                                  例::

                                     ./main/web

                                  ディレクトリを指定した場合は、再帰的にチェックが実行される。

jspanalysis.xmloutput             チェック結果のXMLレポートファイルの出力パスを設定する。

                                  例::

                                     ./build/reports/jsp/report.xml

jspanalysis.htmloutput            チェック結果のHTMLレポートファイルの出力パスを設定する。

                                  例::

                                     ./build/reports/jsp/report.html

jspanalysis.checkconfig           JSP静的解析ツール設定ファイルのファイルパスを設定する。

                                  例::

                                    ./tool/jspanalysis/config.txt

jspanalysis.charset               チェック対象JSPファイルの文字コードを設定する。

                                  例::

                                     utf-8

jspanalysis.lineseparator         チェック対象JSPファイルで使用されている改行コードを |br|
                                  設定する。

                                  例::

                                     \n

jspanalysis.xsl                   チェック結果のXMLをHTMLファイルに変換する際のXSLT |br|
                                  ファイルパスを設定する。

                                  例::

                                    ./tool/jspanalysis/transform-to-html.xsl

jspanalysis.additionalext         チェック対象とするJSPファイルの拡張子を設定する。

                                  複数の拡張子を指定する場合には、カンマ(,)区切りで指定する。|br|
                                  この設定値の内容にかかわらず、拡張子が ``jsp`` のファイル |br|
                                  は必ずチェック対象となる。

                                  例::

                                    tag

jspanalysis.excludePatterns [2]_  チェック対象外とするディレクトリ（ファイル）名を正規表現で設 |br|
                                  定する。

                                  複数のパターンを設定する場合にはカンマ(,)区切りで指定する。

                                  例::

                                    ui_local,ui_test,ui_test/.*/set.tag
================================  ======================================================================================

.. [2] 本設定は、デフォルトではコメントアウトしている。本設定を使用する場合は、pom.xmlと、toolsディレクトリのnablarch-tools.xmlについてコメントアウトを解除すること。

.. tip::

  ファイルパス(ディレクトリパス)は、絶対パスでの指定も可能となっている。

.. _how_to_setup_ant_view_in_eclipse_jsp_analysis:


.. |br| raw:: html

  <br />