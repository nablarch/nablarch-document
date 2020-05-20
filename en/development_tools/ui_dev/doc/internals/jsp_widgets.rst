==========================================
UI部品ウィジェット
==========================================

-----------
概要
-----------

ウィジェットの利用
====================================
:doc:`jsp_widgets` は、ボタンや検索結果テーブル、各種入力フィールドといった
画面内に配置される **UI部品** について **UI標準** に準拠した形で
実装された **JSPタグファイル** である。

以下のソースコードは、業務画面JSPにおいて :doc:`jsp_widgets` を使用して入力フォームを記述した例である。

  .. code-block:: jsp

    <n:form windowScopePrefixes="W11AC02,11AC_W11AC01">
    <field:block title="ユーザ基本情報">
      <field:text title="ログインID"
                  domain="LOGIN_ID"
                  required="true"
                  maxlength="20"
                  hint="半角英数記号20文字以内"
                  name="W11AC02.systemAccount.loginId"
                  sample="test01">
      </field:text>
      <field:password title="パスワード"
                      domain="PASSWORD"
                      required="true"
                      maxlength="20"
                      name="W11AC02.newPassword"
                      sample="password">
      </field:password>
      <field:password title="パスワード（確認用）"
                      domain="PASSWORD"
                      required="true"
                      maxlength="20"
                      name="W11AC02.confirmPassword"
                      sample="password">
      </field:password>
      <field:hint>半角英数記号20文字以内</field:hint>
    </field:block>
    </n:form>
 
この例をみるとわかるように、 :doc:`jsp_widgets` は通常のHTMLのレベルより一段上の抽象度で
業務画面の内容を定義することができるため、HTML/JSPを直接利用するのに比べて
開発者が記述するコード量を大幅に減少させることができる。

また、JSPに見た目に関する記述が含まれないため、設計・開発中に画面デザインの変更が入った
場合でも、既に作成された業務画面JSPに一切影響が発生しない。

このため、業務機能設計と画面デザインのワークフローを並行で進めた場合のリスクを最小化
することが可能である。


ウィジェットの分類
==================================
:doc:`jsp_widgets` は、その用途ごとに異なったカテゴリに分類され
個別の名前空間が与えられている。

================== ==============================================================================
名前空間           内容 
================== ==============================================================================
button             画面遷移用のボタンを描画するために使用するウィジェット群。
                   UI標準に記載された標準文言(更新、検索など)、
                   標準サイズに沿ったボタンがデフォルトで表示される。

field              画面内の入出力項目を描画するために使用するウィジェット群。
                   UI標準に定義された各種入力項目
                   (単行テキスト入力、プルダウン、ラジオボタン、カレンダー日付入力など)
                   に応じたタグファイルが用意されている。

link               画面内の各種リンクを描画するために使用するウィジェット群。
                   UI標準の「リンク」に準じたリンクを表示する。

tab                UI標準の「タブ」に記述されたUIを実装するウィジェット群。
                   JavaScriptによるページ内タブ切り替えと通常のリンクと画面遷移によるタブ切り替え
                   の双方を実現する。

table              検索結果テーブルなどの各種テーブルを描画するためのウィジェット群。
                   テーブルの描画については、Nablarchが提供する **<listSearchResult:xxx>**
                   タグを利用して行う。
                   テーブルカラムの内容については、次の「column」を使用する。

column             テーブルの各行の内容を定義するためのウィジェット群。
                   カラムの内容ごと(テキスト、詳細リンク、処理対象選択用チェックボックスなど)に
                   ウィジェットが用意されている。

box                画面内を構造化するためのウィジェット群。
                   PJのポリシーでスタイルを調整するウィジェットが用意されている。

================== ==============================================================================


----------------------
構造
----------------------
:doc:`jsp_widgets` の本体は、ウィジェットごとに作成される **JSPタグファイル** である。
これに、必要に応じて :doc:`js_framework` や スタイルファイルなどが付随する。


タグファイル実装例
=======================
以下は :doc:`../reference_jsp_widgets/field_calendar` におけるタグファイルのソースコードである。
このファイルでは :doc:`jsp_widgets` の
`日付入力機能(nablarch_DatePicker) <../../../../_static/ui_dev/yuidoc/classes/nablarch.ui.DatePicker.html>`_
を **マーカCSS** を使って利用している。

.. code-block:: javascript

  <%--
    カレンダー日付入力UI部品
    @author Iwauo Tajima
  --%>

  <%@ tag pageEncoding="UTF-8" description="日付入力項目を出力するウィジェット" %>
  <%@ taglib prefix="n"      uri="http://tis.co.jp/nablarch" %>
  <%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
  <%@ taglib prefix="field"  tagdir="/WEB-INF/tags/widget/field" %>

  <%---------------------- 属性定義 ----------------------%>
  <%@ attribute name="title"     description="項目名" required="true" rtexprvalue="true" %>
  <%@ attribute name="domain"    description="項目のドメイン型" rtexprvalue="true" %>
  <%@ attribute name="required"  description="必須項目かどうか" rtexprvalue="true" %>
  <%@ attribute name="readonly"  description="編集可能かどうか" rtexprvalue="true" %>
  <%@ attribute name="disabled"  description="サーバに対する入力値の送信を抑制するかどうか" rtexprvalue="true" %>
  <%@ attribute name="name"      description="HTMLのname属性値" required="true" rtexprvalue="true" %>
  <%@ attribute name="id"        description="HTMLのid属性値 (省略時はname属性と同じ値を使用する)" rtexprvalue="true" %>
  <%@ attribute name="cssClass"  description="HTMLのclass属性値" rtexprvalue="true" %>
  <%@ attribute name="maxlength" description="入力文字数の上限(デフォルト:10文字)" rtexprvalue="true" %>
  <%@ attribute name="example"   description="具体的な入力例を表すテキスト(placeholderなどの形式で表示する)" rtexprvalue="true" %>
  <%@ attribute name="nameAlias" description="一つのエラーメッセージに対して複数の入力項目をハイライト表示する場合に指定する（項目間精査など）。詳細については、Application Framework解説書の「エラー表示」を参照。" rtexprvalue="true" %>
  <%@ attribute name="hint"      description="入力内容や留意点などの補助テキスト" rtexprvalue="true" %>
  <%@ attribute name="sample"    description="テスト用のダミー入力値(本番動作では使用されない)" rtexprvalue="true" %>
  <%-----------------------追加属性---------------------------%>
  <%@ attribute name="format"    description="日付フォーマット(デフォルト:yyyy/MM/dd)" rtexprvalue="true" %>
  <%@ attribute name="locale"    description="言語設定(デフォルト:ja)" rtexprvalue="true" %>

  <%---------------------- 設計書用属性定義 ----------------------%>
  <%@ attribute name="dataFrom" description="表示するデータの取得元（画面項目定義に記載する、「表示情報取得元」.「表示項目名」の形式で設定する）" %>
  <%@ attribute name="comment"    description="このカレンダーについての備考（画面項目定義の項目定義一覧で、備考欄に表示される）" %>
  <%@ attribute name="initialValueDesc"    description="初期表示内容に関する説明。" %>

  <%---------------------- マルチレイアウト用属性 ----------------------%>
  <%@ attribute name="titleSize" description="タイトル部の幅（グリッド数）※マルチレイアウトモードの場合に使用する。" rtexprvalue="true" type="java.lang.Integer" %>
  <%@ attribute name="inputSize" description="入力部の幅（グリッド数）※マルチレイアウトモードの場合に使用する。" rtexprvalue="true" %>

  <%-- デフォルトの日付フォーマットの最大入力文字数 --%>
  <c:if test="${empty format}">
    <n:set var="maxlengthValue" value="10" scope="page"/>
  </c:if>
  <c:if test="${not empty format}">
    <n:set var="maxlengthValue" name="maxlength" scope="page"/>
  </c:if>

  <%-- デフォルトの日付フォーマット --%>
  <c:if test="${empty format}"><n:set var="format" value="yyyy/MM/dd" scope="page" /></c:if>

  <%-- デフォルトのロケール --%>
  <c:if test="${empty locale}"><n:set var="locale" value="ja" scope="page" /></c:if>

  <field:inputbase
    title      = "${title}"
    name       = "${name}"
    required   = "${required}"
    hint       = "${hint}"
    fieldClass = "${disabled ? 'disabled' : ''}"
    titleSize  = "${titleSize}"
    inputSize  = "${inputSize}">
    <jsp:attribute name="fieldContent">
      <c:if test="${empty maxlengthValue}">
        <n:text
          name        = "${name}"
          id          = "${(empty id) ? name : id}"
          disabled    = "${disabled}"
          cssClass    = "${cssClass} ${(readonly) ? 'nablarch_readonly' : ''}"
          placeholder = "${example}"
          valueFormat = "yyyymmdd{${format}}"
          nameAlias   = "${nameAlias}"
        />
      </c:if>
      <c:if test="${not empty maxlengthValue}">
        <n:text
          name        = "${name}"
          id          = "${(empty id) ? name : id}"
          disabled    = "${disabled}"
          cssClass    = "${cssClass} ${(readonly) ? 'nablarch_readonly' : ''}"
          placeholder = "${example}"
          valueFormat = "yyyymmdd{${format}}"
          nameAlias   = "${nameAlias}"
          maxlength   = "${maxlengthValue}"
        />
      </c:if>
      <n:forInputPage>
        <n:set
          var   = "classText"
          value = "${(readonly || disabled) ? 'disabled' : ''}
                   nablarch_DatePicker
                     -format ${format}
                     -locale ${locale}
                     -input  ${(empty id) ? name : id}"
        />
        <c:if test="${disabled || readonly }">
          <button class="<n:write name='classText' withHtmlFormat='false' />"  disabled="disabled" type="button">
            <i class="fa fa-calendar"></i>
          </button>
        </c:if>
        <c:if test="${!disabled && !readonly}">
          <button class="<n:write name='classText' withHtmlFormat='false' />" type="button">
            <i class="fa fa-calendar"></i>
          </button>
        </c:if>
      </n:forInputPage>
    </jsp:attribute>
  </field:inputbase>




構成ファイル一覧
==========================
各 :doc:`jsp_widgets` の実体となるタグファイルは **(サーブレットコンテキストルート)/WEB-INF/tags/widget/** の配下に
カテゴリごとのサブフォルダごとに置かれている。

============================ ======== ======= ============================ ===================================================
名称                         動作環境 [#1]_   パス                         内容                       
---------------------------- ---------------- ---------------------------- ---------------------------------------------------
_                            ローカル サーバ  _                            _
============================ ======== ======= ============================ ===================================================
**buttonタグ**
------------------------------------------------------------------------------------------------------------------------------
<button:xxx>タグファイル     ○        ○       /WEB-INF/tags/widget/\       ボタンカテゴリのタグファイル群
                                              button/\*.tag                  

<button:xxx>スタブ           ○        ×       /js/jsp/taglib/\             ボタンカテゴリ配下の各タグファイルを読み込んで
                                              button.js                    ローカルレンダリングを行うスクリプト。

**fieldタグ**
------------------------------------------------------------------------------------------------------------------------------
<field:xxx>タグファイル      ○        ○       /WEB-INF/tags/widget/\       入出力項目カテゴリのタグファイル群
                                              field/\*.tag                  

<field:xxx>スタブ            ○        ×       /js/jsp/taglib\              入出力項目カテゴリ配下の各タグファイルを読み込んで
                                              field.js                     ローカルレンダリングを行うスクリプト。

カレンダー日付入力機能       ○        △       /js/nablarch/ui/\            カレンダーを用いて日付を入力させる
                                              DatePicker.js                JavaScript UI部品。
                                                                           <field:calendar> タグで内部的に使用する。

リストビルダー機能           ○        △       /js/nablarch/ui/\            2つのリストボックス間の要素移動により項目選択を行う
                                              ListBuilder.js               JavaScript UI部品。
                                                                           <field:listbuilder> タグで内部的に使用する。

プレースホルダー機能         ○        △       /js/nablarch/ui/\            HTML5のplaceholder属性をサポートしていないブラウザで\
                                              Placeholder.js               同等の機能を実現するJavaScript UI部品。
                                                                           <field:text> タグ等のテキスト入力を行うタグ全般で使用
                                                                           している。

入力不可項目機能             ○        △       /js/nablarch/ui/\            HTMLのreadonly属性の拡張機能を実装する
                                              readonly.js                  JavaScript UI部品。
                                                                           テキスト入力項目だけでなく、プルダウンやラジオボタンの
                                                                           ような選択項目にも対応する。
                                                                           <field:pulldown>など、入力項目タグ全般で使用している。

**linkタグ**
------------------------------------------------------------------------------------------------------------------------------
<link:xxx>タグファイル       ○        ○       /WEB-INF/tags/widget/\       リンクカテゴリのタグファイル群
                                              link/\*.tag                  

<link:xxx>スタブ             ○        ×       /js/jsp/taglib/\             リンクカテゴリ配下の各タグファイルを読み込んで
                                              link.js                      ローカルレンダリングを行うスクリプト。


**tabタグ**
------------------------------------------------------------------------------------------------------------------------------
<tab:xxx>タグファイル        ○        ○       /WEB-INF/tags/widget/\       タグカテゴリのタグファイル群
                                              tab/\*.tag                   

<tab:xxx>スタブ              ○        ×       /js/jsp/taglib/\             タブカテゴリ配下の各タグファイルを読み込んで
                                              tab.js                       ローカルレンダリングを行うスクリプト。

タブ表示機能                 ○        △       /js/nablarch/ui/Tab.js       ページ内タブ機能を実現する JavaScript UI部品。
                                                                           <tab:content>で使用している。

**tableタグ**
------------------------------------------------------------------------------------------------------------------------------
<table:xxx>タグファイル      ○        ○       /WEB-INF/tags/widget/\       テーブルカテゴリのタグファイル群
                                              table/\*.tag                  

<table:xxx>スタブ            ○        ×       /js/jsp/taglib/\             テーブルカテゴリ配下の各タグファイルを読み込んで
                                              table.js                     ローカルレンダリングを行うスクリプト。
                                                                           ローカル動作で表示するダミーデータのレコード件数 
                                                                           などを設定する。

listSearchResultタグ         ○        ○       /WEB-INF/tags/\              Nablarchフレームワークが提供している
                                              listSearchResult/\*.tag      検索結果テーブル表示用の共通部品。            
                                                                           <table:xxx> タグが内部的に使用する。

listSearchResultスタブ       ○        ×       /js/jsp/taglib/\             <listSearchResult:xxx>タグを読み込んで、
                                              listsearchresult.js          ローカルレンダリングを行うスクリプト。

階層テーブル表示機能         ○        △       /js/nablarch/ui/\            組織表のような階層構造を持ったテーブルを表示する
                                              TreeList.js                  JavaScript UI部品。
                                                                           <table:treelist>で使用している。

**columnタグ**
------------------------------------------------------------------------------------------------------------------------------
<column:xxx>タグファイル     ○        ○       /WEB-INF/tags/widget/\       カラムカテゴリのタグファイル群
                                              column/\*.tag                   

<column:xxx>スタブ           ○        ○       /js/jsp/taglib/column.js     カラムカテゴリ配下の各タグファイルを読み込んで 
                                                                           ローカルレンダリングを行うスクリプト。

**boxタグ**
------------------------------------------------------------------------------------------------------------------------------
<box:XXX>タグファイル        ○        ○       /WEB-INF/tags/widget/\       ボックスカテゴリのタグファイル群。
                                              box/\*.tag

<box:XXX>スタブ              ○        ×       /js/jsp/taglib/\             ボックスカテゴリのタグファイルを読み込んで
                                              box.js                       ローカルレンダリングに使用するファイル。

============================ ======== ======= ============================ ===================================================

.. [#1]
  **「サーバ」:**
    実働環境にデプロイして使用するかどうか
  **「ローカル」:**
    ローカル動作時に使用するかどうか
  **○ :**
    使用する 
  **△ :**
    直接は使用しないがミニファイしたファイルの一部として使用する。
  **× :**
    使用しない


------------------------------
ローカル動作時の挙動
------------------------------
ローカル動作時でのJSPウィジェットタグの評価は、 **js/jsp/taglib/** 配下にカテゴリの名前空間ごとに用意された
スタブ動作スクリプトによって行われる。
これらのスクリプトは、基本的にカテゴリ内の当該のタグファイルを読み込んで、その内容をレンダリングする。

