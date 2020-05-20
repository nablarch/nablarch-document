業務画面テンプレートとUI部品を利用して業務画面JSPを作成する
======================================================================

画面のテンプレートを用意する
------------------------------------------

作成する業務画面JSPに、業務画面テンプレート・UI部品を利用するために必要な内容を記載する。

業務画面テンプレート・UI部品を利用するために必要な内容は以下の通り。

  * DOCTYPE宣言

    .. code-block:: html

       <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">

  * ローカルJSPレンダリング機能を有効にするスクリプトタグ（本番稼働時には出力されないように、コメントアウトする。）

    .. code-block:: jsp

       <!-- <%/* --> <script src="js/devtool.js"></script><meta charset="utf-8"><body> <!-- */%> -->

  * JSPとして必要なディレクティブ

    .. code-block:: jsp

       <%@page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

  * 利用するtaglib

    各taglibで提供されるタグの詳細については、それぞれのtaglibで提供されているタグファイルを参照のこと。
    一覧は :doc:`widget_list` を参照。
    （IDEを利用している場合、補完やドキュメント参照を行うこともできる。）

    * **業務画面テンプレート** (``/WEB-INF/tags/template``)

       .. code-block:: jsp

          <%@taglib prefix="t" tagdir="/WEB-INF/tags/template" %>


    * **fieldウィジェット** (``/WEB-INF/tags/widget/field``)
       「入力項目」や「表示項目」を表示するUI部品が提供されている。

       .. code-block:: jsp

          <%@taglib prefix="field" tagdir="/WEB-INF/tags/widget/field" %>


    * **buttonウィジェット** (``/WEB-INF/tags/widget/button``)
       「ボタン」を表示するためのUI部品が提供されている。

       .. code-block:: jsp

          <%@taglib prefix="button" tagdir="/WEB-INF/tags/widget/button" %>


    * **tableウィジェット** (``/WEB-INF/tags/widget/table``)
       検索結果などを表形式で表示するためのUI部品が提供されている。

       .. code-block:: jsp

          <%@taglib prefix="table" tagdir="/WEB-INF/tags/widget/table" %>


    * **columnウィジェット** (``/WEB-INF/tags/widget/column``)
       表の列を表示するためのUI部品が提供されている。

       .. code-block:: jsp

          <%@taglib prefix="column" tagdir="/WEB-INF/tags/widget/column" %>


    * **tabウィジェット** (``/WEB-INF/tags/widget/tab``)
       タブ形式でリンクやコンテンツを表示するためのUI部品が提供されている。

       .. code-block:: jsp

          <%@taglib prefix="tab" tagdir="/WEB-INF/tags/widget/tab" %>


    * **linkウィジェット** (``/WEB-INF/tags/widget/link``)
       リンクを表示するためのUI部品が提供されている。

       .. code-block:: jsp

          <%@taglib prefix="link" tagdir="/WEB-INF/tags/widget/link" %>

    * **画面表示パターン定義ウィジェット** (``/WEB-INF/tags/widget/spec``)
       画面状態を設計情報として記述するためのUI部品が提供されている。
       詳細については\ :ref:`spec_condition_widget`\ を参照。

       .. code-block:: jsp

          <%@ taglib prefix="spec" tagdir="/WEB-INF/tags/widget/spec" %>

    * **Nablarch タグライブラリ** （ ``nablarch.jar`` に同梱）

       .. code-block:: jsp

          <%@taglib prefix="n" uri="http://tis.co.jp/nablarch" %>


  * 利用する業務画面テンプレート

    ``t:テンプレート名`` を利用する。

    .. code-block:: jsp

       <t:page_template
           title="画面タイトル"
           confirmationPageTitle="確認画面タイトル（入力・確認画面でJSPを共用しない場合は不要）">

         <jsp:attribute name="contentHtml">
             <%-- 業務領域 --%>
             ここに、業務領域や、自動生成する設計書に表示する内容を記載する。
         </jsp:attribute>
       </t:page_template>


上記の内容を記載すると、業務画面JSPファイルは :download:`このファイル <source/sample_template.jsp>` のようになる。

.. tip::

   Nablarchの提供するタグの詳細については、Nablarch Application Framework解説書「タグリファレンス」を参照。


画面をブラウザで表示する
------------------------------------------

作成した業務画面JSPをブラウザを利用して表示する。

作成した業務画面JSPは、業務JSP作成用プロジェクトの、サブシステムIDのディレクトリ配下に配置する。（ :doc:`project_structure` 参照）

ローカル画面確認.batを実行すれば、作成した画面に遷移し、レイアウトを確認することができる。

:download:`このファイル <source/sample_template.jsp>` のブラウザ表示のイメージは以下のようになる。

.. image:: _image/view_template.png
   :align: center
   :scale: 70



.. important::
  IEを使用している場合は、開発者ツールを開き、
  ブラウザモードおよびドキュメントモードが下記の設定となっていることを確認すること。

    **ブラウザーモード:** 使用しているIEのバージョンと同じ

    **ドキュメントモード:** 標準



  以下の図はIE10での設定例である。

  (なお、開発者ツールを開いた状態では、画面表示が崩れる場合があるので、設定確認後はツールを閉じること。)

  .. image:: _image/display_settings_for_ie.png
     :align: center
     :scale: 70


UI部品（ウィジェット）を配置していく
------------------------------------------

ここまでで作成した業務画面テンプレート表示を行うJSPに、UI部品（ウィジェット）を配置して業務画面JSPを作成していく。

具体的なウィジェットの利用方法や、ウィジェットと画面項目の対応については、 :ref:`example` を参照のこと。

.. important::

   ウィジェットは以下のようなタグ形式で記述するが、自己終了エレメントとして記述するとブラウザでのレイアウト確認が行えなくなるため注意すること。

   （自己終了エレメントとして記述したタグ以降が表示されなくなる。）

   OK!!

   .. code-block:: jsp

      <field:label title="ログインID" sample="login-id"></field:label>

   NG!!

   .. code-block:: jsp

      <field:label title="ログインID" sample="login-id" />


ウィジェットに定義されている属性について
----------------------------------------------------------------------

ウィジェットに定義されている属性のうち、注意の必要なものについて以下に記載する。

**name属性**
  name属性については、基本的にはPG・UT工程で定義するものであるため、空として定義しておけばよい。

  ただし、ローカル表示でname属性の指定が必要なウィジェットが一部存在する。
  各ウィジェットのガイドを参照し、name属性の指定が必要な場合には、name属性の指定を行うこと。

  ※設計時にname属性の物理名を設定することが難しい場合には、その項目の項目論理名を指定すれば良い。
  この場合、PG担当者がname属性の値を実装開始時に物理名へと変換する必要がある。

**sample属性**
  sample属性に値を設定することで、JSPをブラウザで表示した際にダミーの値を画面上に表示することができる。

  プルダウンやチェックボックス、ラジオボタン、テーブルなどに複数のダミーの値を表示する場合、
  sample属性に「|」区切りで記載することができる。

  それらの値を「[]」で囲むことで、囲まれた値を初期表示時点での選択項目とすることができる。

  また、sample属性が指定されていない場合に画面に出力されるコード名称は"codeId"属性および"pattern"属性、"optionColumnName"属性に指定された値を元に、
  「js/devtool/resource/コード値定義.js」から該当する名称が取得される。

**key属性**
  **key属性** は **<column:label>** などのタグにおいて、表示するレコードセットのキー名を指定する属性である。
  この属性は基本的にはPG・UT工程で決定するものなので、設計段階では指定不要である。

  ただし、その場合、 **sample属性** が未指定もしくは空文字を指定すると、
  別の項目のsample属性値が表示される問題がある。
  そのようなケースでは適当な文字列を **key属性** に指定するか **sample属性** にスペース文字を指定すること。


**domain属性**
  画面項目定義を出力するために、項目のドメイン物理名を記載する。また、下記のウィジェットでは、ドメイン毎に表示レイアウトを制御するために、HTMLのclass属性にドメイン物理名を出力する。

  * field:label
  * column:label
  * column:link

  提供している状態では、テーブル内で「Number」というdomain属性が指定されている項目については右寄せで表示されるようになっている。

**dataFrom属性**
  画面項目定義を出力するために、項目に表示するデータの取得元を「表示情報取得元」.「表示項目名」 の形式で記載する。


**hint属性**
  ここで指定した文言が、項目に対する備考として表示される。

また、ウィジェットの属性として必須となっている項目があったとしても、画面設計段階で決定できない場合には空として定義しておけばよい。


画面遷移について
----------------------------------

buttonウィジェットには、紙芝居を行うための ``dummyUri`` 属性を指定することができる。

JSPを直接ブラウザで開いた場合に、ボタンをクリックすると、 ``dummyUri`` 属性で指定されたJSPファイルに遷移する。

ただし、遷移先リクエストIDを条件によって変化させる、などの実際の遷移を忠実に再現させることはできない。（必要がなければ、 ``dummyUri`` 属性を指定する必要はない。）

あくまでも顧客への説明をより容易に行えるように準備されている属性であり、実際に行われるべき遷移については、PG・UT工程で実装される。


ウィジェットの作成について
----------------------------------

以下のサンプルファイルで利用している内線番号ウィジェットは、field:textウィジェットの組み合わせで作成している。
「住所」「電話番号」「氏名」など、典型的であり複数画面で利用されうる項目については内線番号ウィジェットのように、各PJで作成することを推奨する。

作成方法の詳細については、UI開発基盤用プロジェクトテンプレートの内線番号ウィジェットの実装を参照のこと。


入力画面と確認画面の共用
----------------------------------

fieldウィジェットを利用して表示する入力項目は、入力画面と確認画面で自動的に切り替わり、入力画面ではテキストボックス、確認画面では単に表示されるだけとなる。

入力画面と確認画面を共用する場合には、確認画面は下記のように作成すればよい。

.. code-block:: jsp

   <!DOCTYPE html>
   <!-- <%/* --> <script src="js/devtool.js"></script><meta charset="utf-8"><body> <!-- */%> -->
   <%@ taglib prefix="n" uri="http://tis.co.jp/nablarch" %>
   <n:confirmationPage path="./W11AC0201.jsp" />



入力画面と確認画面で異なる項目を表示する必要がある場合、以下の実装例のように

* 入力画面で出力する項目は ``<n:forInputPage>`` で囲む。

* 確認画面で出力する項目は ``<n:forConfirmationPage>`` で囲む。

とする。


.. _example:

業務画面JSPの例
----------------------------------

* :ref:`入力画面 <input>`
* :ref:`確認画面 <confirm>`
* :ref:`検索・一覧画面 <list_search>`
* :ref:`詳細画面 <detail>`

---------------------------------

.. _input:

**入力画面**： :download:`W11AC0201.jsp <source/W11AC0201.jsp>`

.. image:: _image/view_input.png
   :align: center
   :scale: 70

---------------------------------

.. _confirm:

**確認画面**： :download:`W11AC0202.jsp <source/W11AC0202.jsp>`

.. image:: _image/view_confirm.png
   :align: center
   :scale: 70

---------------------------------

.. _list_search:

**一覧・検索画面**： :download:`W11AC0101.jsp <source/W11AC0101.jsp>`

.. image:: _image/view_search.png
   :align: center
   :scale: 70

---------------------------------

.. _detail:

**詳細画面**： :download:`W11AC0102.jsp <source/W11AC0102.jsp>`

.. image:: _image/view_detail.png
   :align: center
   :scale: 70
