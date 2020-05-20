.. _jsp_static_analysis_tool:

=========================
JSP静的解析ツール
=========================

.. contents:: 目次
  :depth: 2
  :local:

----
概要
----

JSPで使用を許可する構文とタグを規定し、許可する構文とタグのみを使用していることをチェックする。
これにより、次のことを保証できる。

* 使用されている構文とタグを限定できるため、保守性が向上する。
* 使用できる構文とタグを限定することにより、サニタイジング漏れを検出することができる。

本ツールでは、JSPコンパイルが成功するファイルに対するチェックを行うものである。
このため、JSPコンパイルが通らないファイル（例えばtaglibのとじタグが存在していない等）の場合には、本ツールは正しくJSPファイルの解析を行うことは出来ない。

なお、本ツールはnablarch-testing-XXX.jarに含まれる。

----
仕様
----

許可するタグの指定方法
===========================

本ツールは、 **JSPで使用を許可する構文とタグ** を設定ファイルに定義することで、設定ファイルに定義されていない構文とタグが使用されている箇所を指摘する。
チェック結果は、HTMLまたはXML形式で出力する。

本ツールで指定可能な構文とタグを下記に示す。

* XMLコメント
* HTMLコメント [#html_comment]_
* EL式
* 宣言
* 式
* スクリプトレット
* ディレクティブ
* アクションタグ
* カスタムタグ

本ツールではHTMLタグ等の上記以外の構文とタグは指定できない。

本ツールでは、下記の場所をチェック対象外とする。下記以外の場所は常にチェックする。

* 使用を許可したタグの属性

下記に例として、EL式を禁止した場合のチェック結果を示す。

* 使用を許可したタグの属性にEL式を指定した場合は、指摘しない。 ::

    <jsp:include page="${ Expression }" />

* 使用を許可したタグのボディにEL式を指定した場合は、指摘する。 ::
     
    <jsp:text> 
       ${ Expression }
    </jsp:text>

* HTMLタグの属性にEL式を指定した場合は、指摘する。 ::

    <td height="${ Expression }"> </td>

* HTMLタグのボディにEL式を指定した場合は、指摘する。 ::

    <td> ${ Expression } </td>

* JavaScript中にEL式を指定した場合は、指摘する。 ::

    function samplefunc() {
        var id = ${user.id}
    }

設定ファイルの記述方法は :ref:`01_customJspAnalysis` を参照のこと。

.. [#html_comment]

  HTMLコメントを使用不可とした場合でも、以下のコメントについてはエラーとして検出しない。

  * 条件付きコメント(IEによって解釈される条件付きのコメント)
  * 業務画面作成支援ツールをロードするためのコメント

  これらのコメントは、ブラウザによるCSSの切り替えや業務画面作成支援ツールを使用した際に
  使用必須のコメントとなるため、エラーとして検出することは不適切であるため。



チェック対象ファイルの指定方法
===============================
チェック対象のファイル（ディレクトリ）は、本ツールへの起動引数として指定する。
ディレクトリを指定した場合は、対象のファイル(デフォルトでは拡張子がjspのファイルで、設定により拡張子は追加可能)を再帰的にチェックする。

UI開発基盤の開発プロジェクトでは、チェック対象のファイル（本番環境にデプロイされるファイル）と、
チェック対象外のファイル（テスト用のファイルなどで本番環境にはデプロイされないファイル）が、
チェック対象ディレクトリに混在するケースがある。
このような場合には、除外ファイル設定を使用することで、不要なファイルへのチェックを無効にできる。

チェック対象のファイル（ディレクトリ）、チェック対象外ファイル（ディレクトリ）の設定方法は、 :ref:`01_customJspAnalysisProp` を参照

対象ファイル内の一部を強制的にチェック対象外にする方法
===================================================================
アーキテクトが作成するJSPやタグファイルなどで、やむを得ない事情で許可されていないタグを使う必要性が出てくる場合がある。 
例えば、アプリケーション開発者が作成するJSPファイルから使用されたくないタグを、
アーキテクトが作成するタグファイル内に隠蔽する場合等がこれに該当する。

このような場合には、特定箇所のチェックを強制的に無効化する機能を利用する。
特定箇所のチェックを無効化するには、該当行のすぐ上の行にチェックを無効化するJSPコメントを記述する。
無効化コメントは、本ツールのチェックっ対象外のタグとなる。このため、JSPコメントを使用不可とした場合でもエラーとはならない。

無効化するJSPコメントは以下のルールに従い記述する。

* コメントの開始タグと終了タグを同一行に記述する
* コメントは必ず **suppress jsp check** で始める

  **suppress jsp check**  以降は、任意のコメントを記述できる。
  任意のコメント部には、チェックを無効化する理由を記述すると良い



以下に例を示す::

  <%@tag import="java.util.regex.Pattern" %>
  <%@tag import="java.util.regex.Matcher" %>
  <%@taglib prefix="n" uri="http://tis.co.jp/nablarch" %>

  <%-- suppress jsp check:サーバサイドで判定し、bodyのクラスに埋め込むために必要なコード --%>
  <%!
    static class UserAgent { 
    }
  %>

---------
前提条件
---------

* アーキタイプからブランクプロジェクトの生成が完了していること。


---------
使用方法
---------

設定ファイルの存在確認
======================

toolsプロジェクトのstatic-analysis/jspanalysisディレクトリに、本ツールを実行するために必要な以下のファイルが存在することを確認する。

* :download:`config.txt<../tools/JspStaticAnalysis/config.txt>` … JSP静的解析ツール設定ファイル
* :download:`transform-to-html.xsl<../tools/JspStaticAnalysis/transform-to-html.xsl>` … JSP静的解析結果XMLをHTMLに変換する際の定義ファイル

これらファイルについての詳細は :doc:`02_JspStaticAnalysisInstall` を参照のこと。


Antタスクの定義ファイル確認
===========================

toolsプロジェクトのnablarch-tools.xmlに以下の定義が存在することを確認する。

.. code-block:: xml

  <project name="Nablarch Toolbox">
    <!-- 中略 -->
    <target name="analyzeJsp" depends="analyzeJspOutputXml" description="JSPの解析を行い、HTMLレポートを出力する。">
      <java classname="nablarch.test.tool.sanitizingcheck.HtmlConvert" dir="${nablarch.tools.dir}" fork="true">
        <arg value="${jspanalysis.xmloutput}" />
        <arg value="${jspanalysis.xsl}" />
        <arg value="${jspanalysis.htmloutput}" />
        <classpath>
          <path refid="classpath.common" />
        </classpath>
      </java>
    </target>

    <target name="analyzeJspOutputXml" description="JSPの解析を行い、XMLレポートを出力する。">
      <java classname="nablarch.test.tool.sanitizingcheck.SanitizingCheckTask" dir="${nablarch.tools.dir}" fork="true">
        <arg value="${jspanalysis.checkjspdir}" />
        <arg value="${jspanalysis.xmloutput}" />
        <arg value="${jspanalysis.checkconfig}" />
        <arg value="${jspanalysis.charset}" />
        <arg value="${jspanalysis.lineseparator}" />
        <arg value="${jspanalysis.additionalexts}" />
        <!-- JSP静的解析ツールにおいて、「チェック対象外とするディレクトリ（ファイル）名を正規表現で設定する」ための項目。
             parentプロジェクトのpom.xmlにて、本値を有効にした場合は、コメントアウトを解除する。
        <arg value="${jspanalysis.excludePatterns}" />
        -->
        <classpath>
          <path refid="classpath.common" />
        </classpath>
      </java>
    </target>
    <!-- 中略 -->
  </project>


JSP静的解析ツールでチェックしたい対象の存在するプロジェクトのpom.xmlの確認
===========================================================================================

JSP静的解析ツールでチェックしたい対象の存在するプロジェクトのpom.xmlに、以下の記述が存在することを確認する。

.. code-block:: xml

  <properties>
    <!-- 中略 -->
    <!-- JSP静的解析ツールにおいて、「チェック対象外とするディレクトリ（ファイル）名を正規表現で設定する」ための項目。
         本設定を有効にする場合は、toolsプロジェクト中のnablarch-tools.xml中の設定のコメントアウトも解除すること。
    <jspanalysis.excludePatterns></jspanalysis.excludePatterns>
    -->
    <!-- 中略 -->
  </properties>
  
  <!-- 中略 -->
  
  <build>
    <!-- 中略 -->
    <plugins>
      <!-- 中略 -->
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-antrun-plugin</artifactId>
      </plugin>
      <!-- 中略 -->
    </plugins>
  </build>

.. tip::
    
    JSP静的解析ツールの設定値は、nablarch-archetype-parentのpom.xmlに記述している。
    
    .. code-block:: xml
    
      <properties>
        <!-- 中略 -->
        <!-- JSP静的解析ツールの設定項目 -->
        <jspanalysis.checkjspdir>${project.basedir}/src/main/webapp</jspanalysis.checkjspdir>
        <jspanalysis.xmloutput>${project.basedir}/target/jspanalysis-result.xml</jspanalysis.xmloutput>
        <jspanalysis.checkconfig>${nablarch.tools.dir}/static-analysis/jspanalysis/config.txt</jspanalysis.checkconfig>
        <jspanalysis.charset>UTF-8</jspanalysis.charset>
        <jspanalysis.lineseparator>\n</jspanalysis.lineseparator>
        <jspanalysis.htmloutput>${project.basedir}/target/jspanalysis-result.html</jspanalysis.htmloutput>
        <jspanalysis.xsl>${nablarch.tools.dir}/static-analysis/jspanalysis/transform-to-html.xsl</jspanalysis.xsl>
        <jspanalysis.additionalexts>tag</jspanalysis.additionalexts>
      </properties>
      
    各設定項目に関しては、 :doc:`02_JspStaticAnalysisInstall` を参照のこと。
      


.. _01_customJspAnalysis:

JSP静的解析ツール設定ファイルの記述方法
============================================

プロジェクトの規約を反映するために設定ファイルを変更する。

.. important::
  開発時にアプリケーションプログラマの都合に合わせて設定を変えてはいけない。

設定ファイルには使用を許可する構文とタグの一覧を下表に従って記載する。
「--」で始まる行はコメント行とする。

================= ============================================== ========================================================  
構文又はタグ       JSPでの使用例                                   設定ファイルへの記述方法                           
================= ============================================== ======================================================== 
XMLコメント       <%-- comment --%>                               <%--
HTMLコメント      <!-- comment -->                                <!--
EL式              ${10 mod 4}                                     ${
宣言              <%! int i = 0; %>                               <%!
式                <%= map.size() %>                               <%=
スクリプトレット   <%  String name = null; %>                      <%
ディレクティブ    <%@ taglib prefix="n" uri=  |br|               「<%@」から始まり、最初の空白までの |br|
                  "http://tis.co.jp/nablarch" %>                 部分を記述する。

                                                                 例：） <%@ taglib
アクションタグ    <jsp:attribute name="attrName" />              「<jsp:」から始まり、最初の空白までの |br|
                                                                 部分を記述する。|br|
                                                                 「<jsp:」のみを設定した場合、|br|
                                                                 アクションタグ全てが使用可能となる。

                                                                 例：） <jsp:attribute

カスタムタグ      <n:error name="attrName" />                    設定方法は、アクションタグと同じ。

================= ============================================== ======================================================== 


デフォルトの設定は下記のとおりである。 ::

  <n:
  <c:
  <%--
  <%@ include
  <%@ page
  <%@ tag
  <%@ taglib
  <jsp:include
  <jsp:directive.include
  <jsp:directive.page
  <jsp:directive.tag
  <jsp:param
  <jsp:params
  <jsp:attribute


デフォルトの設定で除外した構文とタグは下記のとおりである。

これらは、Nablarchカスタムタグに同様の機能を有するか、セキュリティホールとなりうる可能性がある構文とタグである。 ::

  <!--
  <%!
  ${
  <%
  <%@ attribute
  <%@ variable
  <jsp:declaration
  <jsp:expression
  <jsp:scriptlet
  <jsp:directive.attribute
  <jsp:directive.variable
  <jsp:body
  <jsp:element
  <jsp:doBody
  <jsp:forward
  <jsp:getProperty
  <jsp:invoke
  <jsp:output
  <jsp:plugin
  <jsp:fallback
  <jsp:root
  <jsp:setProperty
  <jsp:text
  <jsp:useBean

pom.xmlの修正の修正
============================================

pom.xmlに記述されているプロパティを、実行環境にあわせて修正すること。

詳細は、 :ref:`01_customJspAnalysisProp` を参照


実行方法
=========

カレントディレクトリを解析対象のディレクトリにし、verifyフェーズを実行する。

以下に例を示す。

.. code-block:: text
                
  cd XXX-web              
  mvn verify -DskipTests=true


.. _01_outputJspAnalysis:


出力結果確認方法
=================

* JSP解析(HTMLレポート出力)

  JSPのチェックを行い、チェック結果をHTMLに出力する。

  デフォルトの設定では、target/jspanalysis-result.htmlに出力される。

  出力先は、 pom.xml の jspanalysis.htmloutput プロパティの設定で変更できる。

  出力内容の例を以下に示す。

  .. image:: ./_image/how-to-trace-jsp.png
     :scale: 70

  上記の例では、指摘内容は2通りあり、各指摘への対処方法は次のとおりである。

  * 許可されていないタグが使用されている場合。

    「"構文またはタグ名" + "指摘位置" is forbidden.」というエラー内容が表示される。
    プロジェクトの規約にて使用を許可されている構文とタグを使用し対処する。


* JSP解析(XMLレポート出力)

  JSPのチェックを行い、チェック結果をXMLに出力する。

  XMLの出力先は pom.xml の jspanalysis.xmloutputプロパティにて指定する。

  出力したXMLをXSLT等で整形すれば、任意のレポート作成が可能である。

  出力されるXMLフォーマットは次のとおりである。

  ======  ===============================
  要素名  説明
  ======  ===============================
  result  ルートノード
  item    各JSPに対して作成されるノード
  path    該当のJSPのパスを表すノード
  errors  該当のJSPに対する指摘を表すノード
  error   個々の指摘内容
  ======  ===============================

  .. code-block:: xml
        
   <?xml version="1.0" encoding="UTF-8" standalone="no"?>
   <result>
     <item>
       <path>C:\tisdev\workspace\Nablarch_sample\web\management\user\USER-001.jsp</path>
       <errors>
         <error>&lt;!-- (at line=17 column=6) is forbidden.</error>
         <error>&lt;c:if (at line=121 column=2) is forbidden.</error>
         <error>&lt;!-- (at line=150 column=8) is forbidden.</error>
         <error>&lt;!-- (at line=151 column=8) is forbidden.</error>
         <error>&lt;!-- (at line=160 column=8) is forbidden.</error>
       </errors>
     </item>
     <item>
       <path>C:\tisdev\workspace\Nablarch_sample\web\management\user\USER-002.jsp</path>
       <errors>
         <error>&lt;!-- (at line=20 column=10) is forbidden.</error>
         <error>&lt;c:if (at line=152 column=46) is forbidden.</error>
       </errors>
     </item>
     <item>
       <path>C:\tisdev\workspace\Nablarch_sample\web\management\user\USER-004.jsp</path>
       <errors>
         <error>&lt;!-- (at line=16 column=10) is forbidden.</error>
       </errors>
     </item>
   </result>

.. tip::

 本ツールの実行は、アプリケーション開発者任せでではなくJenkinsのようなCIサーバで定期的に実行し、
 許可されていなタグが使われていないことを常に保証する必要がある。


.. |br| raw:: html

  <br />