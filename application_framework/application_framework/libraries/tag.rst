.. _`tag`:

JSPカスタムタグ
==================================================

.. contents:: 目次
  :depth: 3
  :local:

.. toctree::
  :maxdepth: 1
  :hidden:

  tag/tag_reference


この機能では、ウェブアプリケーションの画面作成を支援するカスタムタグを提供する。

カスタムタグには、以下の制約がある。

* JSP2.1以降をサポートしているWebコンテナで動作する。
* 条件分岐やループなどの制御にはJSTLを使用する。
* XHTML 1.0 Transitionalに対応した属性をサポートする。(HTML5の属性には未対応)
* クライアントのJavaScriptが必須である。( :ref:`tag-onclick_override` を参照)
* GETリクエストで一部のカスタムタグが使用できない。( :ref:`tag-using_get` を参照)

.. important::
 カスタムタグはHTML5に対応できていない。
 ただし、HTML5の属性のうち、頻繁に使用されそうな次の属性のみ先行で取り込んでいる。
 属性を追加したHTMLのタグ名をカッコ内に記載する。

 * autocomplete(input、password、form)
 * autofocus(input、textarea、select、button)
 * placeholder(text、password、textarea)
 * maxlength(textarea)
 * multiple(input)

 上記以外のHTML5の属性は使用できないため、必要となった場合は各プロジェクトでカスタムタグを拡張する。

.. important::
 カスタムタグは、以下のような単純な画面遷移を行うウェブアプリケーションを対象にしている。
 そのため、操作性を重視したリッチな画面作成やSPA(シングルページアプリケーション)に対応していない。

 * 検索画面→詳細画面による検索/詳細表示
 * 入力画面→確認画面→完了画面による登録/更新/削除
 * ポップアップ(別ウィンドウ、別タブ)による入力補助

 プロジェクトでJavaScriptを多用する場合は、カスタムタグが出力するJavaScriptと
 プロジェクトで作成するJavaScriptで副作用が起きないように注意する。
 カスタムタグが出力するJavaScriptについては :ref:`tag-onclick_override` を参照。

機能概要
---------------------------------------------------------------------

HTMLエスケープ漏れを防げる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
HTMLの中では「<」「>」「"」といった文字は、特別な意味を持つため、
それらを含む値をそのままJSPで出力してしまうと、悪意のあるユーザが容易にスクリプトを埋め込むことができ、
クロスサイトスクリプティング(XSS)と呼ばれる脆弱性につながってしまう。
そのため、入力値を出力する場合、HTMLエスケープを行う。

ところが、JSPでEL式を使って値を出力すると、HTMLエスケープされない。
そのため、値の出力時はHTMLエスケープを考慮した実装が常に必要になり、生産性の低下につながる。

カスタムタグは、デフォルトでHTMLエスケープを行うので、
カスタムタグを使って実装している限り、HTMLエスケープ漏れを防げる。

.. important::
  JavaScriptに対するエスケープ処理は、提供してないため、
  scriptタグのボディやonclick属性など、JavaScriptを記述する部分には、動的な値(入力データなど)を埋め込まないこと。
  JavaScriptを記述する部分に動的な値(入力データなど)を埋め込む場合は、プロジェクトの責任でエスケープ処理を実施すること。

HTMLエスケープの詳細は以下を参照。

* :ref:`tag-html_escape`
* :ref:`tag-html_unescape`

入力画面と確認画面のJSPを共通化して実装を減らす
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
多くのシステムでは、入力画面と確認画面でレイアウトが変わらず、
似たようなJSPを作成している。

カスタムタグでは、入力画面と確認画面のJSPを共通化する機能を提供しているので、
入力画面向けに作成したJSPに、確認画面との差分(例えば、ボタンなど)のみを追加実装するだけで、
確認画面を作成することができ、生産性の向上が期待できる。

入力画面と確認画面の共通化については以下を参照。

* :ref:`tag-make_common`

モジュール一覧
---------------------------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web-tag</artifactId>
  </dependency>

  <!-- hidden暗号化を使う場合のみ -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-encryption</artifactId>
  </dependency>

  <!-- ファイルダウンロードを使う場合のみ -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web-extension</artifactId>
  </dependency>

使用方法
---------------------------------------------------------------------

.. tip::
 カスタムタグの説明では、すべての属性について説明していないので、
 各カスタムタグで指定できる属性については、 :ref:`tag_reference` を参照。

.. _`tag-setting`:

カスタムタグの設定を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
カスタムタグの設定は、 :ref:`nablarch_tag_handler` と
:java:extdoc:`CustomTagConfig<nablarch.common.web.tag.CustomTagConfig>`
により行う。

:ref:`nablarch_tag_handler`
 カスタムタグを使用したリクエストを処理する際に、以下の機能に必要となる前処理を行うハンドラ。
 カスタムタグを使用する場合は、このハンドラの設定が必須となる。

 * :ref:`tag-checkbox_off_value`
 * :ref:`tag-hidden_encryption`
 * :ref:`tag-submit_change_parameter`
 * :ref:`tag-composite_key`

 このハンドラの設定値については、 :ref:`nablarch_tag_handler` を参照。

:java:extdoc:`CustomTagConfig<nablarch.common.web.tag.CustomTagConfig>`
 カスタムタグのデフォルト値の設定を行うクラス。
 選択項目のラベルパターンなど、カスタムタグの属性は、個々の画面で毎回設定するよりも、
 アプリケーション全体で統一したデフォルト値を使用したい場合がある。
 そのため、カスタムタグのデフォルト値の設定をこのクラスで行う。

 デフォルト値の設定は、 このクラスを ``customTagConfig`` という名前でコンポーネント定義に追加する。
 設定項目については、 :java:extdoc:`CustomTagConfig<nablarch.common.web.tag.CustomTagConfig>` を参照。

.. _`tag-specify_taglib`:

カスタムタグを使用する(taglibディレクティブの指定方法)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
カスタムタグとJSTLを使用する想定なので、それぞれのtaglibディレクティブを指定する。

.. code-block:: jsp

 <%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
 <%@ taglib prefix="n" uri="http://tis.co.jp/nablarch" %>

.. _`tag-input_form`:

入力フォームを作る
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
入力フォームは、次のカスタムタグを使用して作成する。
以下に列挙したカスタムタグの詳細は、 :ref:`tag_reference` を参照。

* :ref:`tag-form_tag`
* :ref:`tag-text_tag` などの入力を行うカスタムタグ
* :ref:`tag-submit_tag`  などのサブミットを行うカスタムタグ
* :ref:`tag-error_tag` などのエラー表示を行うカスタムタグ

入力フォームを作る上でのポイント
 \

 入力値の復元
  バリデーションエラーなどで、入力フォームを再表示した場合、カスタムタグによりリクエストパラメータから入力値が復元される。

 初期値の出力
  入力項目に初期値を出力したい場合は、アクション側でリクエストスコープに初期値を設定したオブジェクトを設定する。
  そして、カスタムタグのname属性と、リクエストスコープ上の変数名が対応するように、name属性を指定する。
  指定方法の詳細や実装例は、 :ref:`tag-access_rule` を参照。

 サブミット先のURI指定
  カスタムタグでは、フォームに配置された複数のボタン/リンクから、それぞれ別々のURIにサブミットできる。
  ボタン/リンクのサブミット先となるURIは、uri属性に指定する。
  指定方法の詳細や実装例は、 :ref:`tag-specify_uri` を参照。

実装例
 \

 .. code-block:: jsp

  <n:form>
    <div>
      <label>ユーザID</label>
      <n:text name="form.userId" />
      <n:error name="form.userId" messageFormat="span" errorCss="alert alert-danger" />
    </div>
    <div>
      <label>パスワード</label>
      <n:password name="form.password" />
      <n:error name="form.password" messageFormat="span" errorCss="alert alert-danger" />
    </div>
    <div style="padding: 8px 0;">
      <n:submit type="submit" uri="/action/login" value="ログイン" />
    </div>
  </n:form>

出力結果
 \

 .. image:: images/tag/login_form.png

\

.. tip::

 .. _`tag-input_form_name_constraint`:

 :ref:`tag-form_tag` のname属性には以下の制約がある。

 * 画面内で一意な名前をname属性に指定する
 * JavaScriptの変数名の構文に則った値を指定する

 画面内で一意な名前をname属性に指定する
  カスタムタグでは、サブミット制御にJavaScriptを使用する。
  JavaScriptについては :ref:`tag-onclick_override` を参照。

  このJavaScriptでは、サブミット対象のフォームを特定するために、
  :ref:`tag-form_tag` のname属性を使用する。
  そのため、アプリケーションで :ref:`tag-form_tag` のname属性を指定する場合は、
  画面内で一意な名前をname属性に指定する必要がある。

  アプリケーションで :ref:`tag-form_tag` のname属性を指定しなかった場合、
  カスタムタグは一意な値をname属性に設定する。

 JavaScriptの変数名の構文に則った値を指定する
  :ref:`tag-form_tag` のname属性はJavaScriptで使用するため、
  JavaScriptの変数名の構文に則った値を指定する必要がある。

  変数名の構文
   * 値の先頭は英字始まり
   * 先頭以降の値は英数字またはアンダーバー

.. _`tag-selection`:

選択項目(プルダウン/ラジオボタン/チェックボックス)を表示する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
選択項目には、次のカスタムタグを使用する。

* :ref:`tag-select_tag` (プルダウン)
* :ref:`tag-radio_buttons_tag` (複数のラジオボタン)
* :ref:`tag-checkboxes_tag` (複数のチェックボックス)

アクション側で選択肢リスト(選択肢のラベルと値をもつオブジェクトのリスト)をリクエストスコープに設定し、
カスタムタグで選択肢リストを使用して表示する。

.. tip::
 選択状態の判定は、選択された値と選択肢の値をともに
 :java:extdoc:`Object#toString <java.lang.Object.toString()>` してから行う。

実装例
 \

 選択肢のクラス
  \

  .. code-block:: java

   public class Plan {

       // 選択肢の値
       private String planId;

       // 選択肢のラベル
       private String planName;

       public Plan(String planId, String planName) {
           this.planId = planId;
           this.planName = planName;
       }

       // カスタムタグはこのプロパティから選択肢の値を取得する。
       public String getPlanId() {
           return planId;
       }

       // カスタムタグはこのプロパティから選択肢のラベルを取得する。
       public String getPlanName() {
           return planName;
       }
   }

 アクション
  \

  .. code-block:: java

   // 選択肢リストをリクエストスコープに設定する。
   List<Plan> plans = Arrays.asList(new Plan("A", "フリー"),
                                    new Plan("B", "ベーシック"),
                                    new Plan("C", "プレミアム"));

   // カスタムタグはここで指定した名前を使ってリクエストスコープから選択肢リストを取得する。
   context.setRequestScopedVar("plans", plans);

 プルダウン
  JSP
   .. code-block:: jsp

    <!--
      以下の属性指定により、選択肢の内容にアクセスする。
      listName属性: 選択肢リストの名前
      elementLabelProperty属性: ラベルを表すプロパティ名
      elementValueProperty属性: 値を表すプロパティ名
    -->
    <n:select name="form.plan1"
              listName="plans"
              elementLabelProperty="planName"
              elementValueProperty="planId" />

  出力されるHTML
   .. code-block:: html

    <!--
      "form.plan1"の値が"A"だった場合。
    -->
    <select name="form.plan1">
      <option value="A" selected="selected">フリー</option>
      <option value="B">ベーシック</option>
      <option value="C">プレミアム</option>
    </select>

 ラジオボタン
  JSP
   .. code-block:: jsp

    <!-- 属性指定はselectタグと同じ。 -->
    <n:radioButtons name="form.plan2"
                    listName="plans"
                    elementLabelProperty="planName"
                    elementValueProperty="planId" />

  出力されるHTML
   .. code-block:: html

    <!--
     "form.plan2"の値が"B"だった場合。
     デフォルトだとbrタグで出力する。
     listFormat属性を指定して、divタグ、spanタグ、ulタグ、olタグ、スペース区切りに変更できる。
    -->
    <input id="nablarch_radio1" type="radio" name="form.plan2" value="A" />
    <label for="nablarch_radio1">フリー</label><br />
    <input id="nablarch_radio2" type="radio" name="form.plan2" value="B" checked="checked" />
    <label for="nablarch_radio2">ベーシック</label><br />
    <input id="nablarch_radio3" type="radio" name="form.plan2" value="C" />
    <label for="nablarch_radio3">プレミアム</label><br />

 チェックボックス
  JSP
   .. code-block:: jsp

    <!-- 属性指定はselectタグと同じ。 -->
    <n:checkboxes name="form.plan4"
                  listName="plans"
                  elementLabelProperty="planName"
                  elementValueProperty="planId" />

  出力されるHTML
   .. code-block:: html

    <!--
     "form.plan4"の値が"C"だった場合。
     デフォルトだとbrタグで出力する。
     listFormat属性を指定して、divタグ、spanタグ、ulタグ、olタグ、スペース区切りに変更できる。
    -->
    <input id="nablarch_checkbox1" type="checkbox" name="form.plan4" value="A"
           checked="checked" />
    <label for="nablarch_checkbox1">フリー</label><br />
    <input id="nablarch_checkbox2" type="checkbox" name="form.plan4" value="B" />
    <label for="nablarch_checkbox2">ベーシック</label><br />
    <input id="nablarch_checkbox3" type="checkbox" name="form.plan4" value="C" />
    <label for="nablarch_checkbox3">プレミアム</label><br />

.. important::
 :ref:`tag-radio_buttons_tag` と :ref:`tag-checkboxes_tag` は、
 簡単に選択項目を出力できる反面、カスタムタグで選択肢をすべて出力するので、
 どうしても出力されるHTMLに制限が出てくる。
 そのため、デザイン会社が作成したHTMLをベースに開発する場合など、プロジェクトでデザインをコントロールできない場合は、
 :ref:`tag-radio_buttons_tag` と :ref:`tag-checkboxes_tag` が出力するHTMLがデザインに合わないケースが出てくる。

 このような場合は、JSTLのc:forEachタグと :ref:`tag-radio_tag` または :ref:`tag-checkbox_tag` を使って実装すれば、
 選択肢を表示するHTMLを自由に実装できる。

 .. code-block:: jsp

  <c:forEach items="${plans}" var="plan">
    <!-- 前後に好きなHTMLを追加できる。 -->
    <n:radioButton name="form.plan3" label="${plan.planName}" value="${plan.planId}" />
  </c:forEach>

.. _`tag-checkbox_off_value`:

チェックボックスでチェックなしに対する値を指定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
HTMLのcheckboxタグは、チェックなしの場合にリクエストパラメータが送信されない。
単一の入力項目としてcheckboxタグを使用する場合は、データベース上でフラグとして表現されたデータ項目に対応することが多く、
通常はチェックなしの場合にも何らかの値を設定する。
そのため、 :ref:`tag-checkbox_tag` では、チェックなしに対応する値を指定できる機能を提供する。

実装例
 .. code-block:: jsp

  <!--
   以下の属性指定により、チェックなしの場合の動作を制御する。
   useOffValue属性: チェックなしの値設定を使用するか否か。デフォルトはtrue
                    一括削除などで複数選択させる場合にfalseを指定する。
   offLabel属性: チェックなしの場合に使用するラベル。
                 入力画面と確認画面を共通化した場合に確認画面で表示されるラベル。
   offValue属性: チェックなしの場合に使用する値。デフォルトは0。
  -->
  <n:checkbox name="form.useMail" value="true" label="使用する"
              offLabel="使用しない" offValue="false" />

.. tip::
 この機能は、:ref:`nablarch_tag_handler` と :ref:`hidden暗号化 <tag-hidden_encryption>` を使って実現している。
 checkboxタグ出力時にチェックなしに対応する値をhiddenタグに出力しておき、
 :ref:`nablarch_tag_handler` がリクエスト受付時に、checkboxタグがチェックされていない場合のみ、
 リクエストパラメータにチェックなしに対応する値を設定する。

.. _`tag-window_scope`:

入力データを画面間で持ち回る(ウィンドウスコープ)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. important::
 入力データ保持は、ここで説明するウィンドウスコープを使う方法と、
 ライブラリの :ref:`session_store` を使う方法の2通りがある。
 以下の理由から、画面間での入力データ保持には、 :ref:`session_store` を使用すること。

 * ウィンドウスコープでは、データをキー/値のペアで保持するため、Beanをそのまま格納することができない。
   Beanが保持するデータを格納したい場合は、データをバラすことになり、とても実装が煩雑となる。

   .. code-block:: java

    // こんなBeanがあるとする。
    Person person = new Person();
    person.setName("名前");
    person.setAge("年齢");

    // ウィンドウスコープへの設定(アクションで行う場合)
    request.setParam("person.name", person.getName());
    request.setParam("person.age", person.getAge());

    // ウィンドウスコープへの設定(JSPで行う場合)
    <n:hidden name="person.name" />
    <n:hidden name="person.age" />

 * ウィンドウスコープへの入力データの設定は、カスタムタグの属性指定により行うため、動きが把握しにくい。(実装難易度が高い)

入力データは、クライアント側にhiddenタグとして保持する。
クライアント側に保持することで、サーバ側(セッション)に保持する場合に比べ、
複数ウィンドウの使用やブラウザの戻るボタンの使用など、ブラウザの使用制限を減らし、柔軟な画面設計が可能となる。

ここでは、クライアント側に保持するデータの格納先をウィンドウスコープと呼ぶ。
ウィンドウスコープのデータは、 :ref:`hidden暗号化<tag-hidden_encryption>` により暗号化する。

.. important::
 ウィンドウスコープのデータは、:ref:`hidden暗号化<tag-hidden_encryption>` により暗号化されhiddenタグに出力される。
 そのため、Ajaxを使って取得したデータで書き換えるなど、クライアント側でウィンドウスコープの内容を書き換えることはできない。

ウィンドウスコープにデータを設定するには、 :ref:`tag-form_tag` のwindowScopePrefixes属性を指定する。

.. important::
 windowScopePrefixes属性を指定すると、リクエストパラメータのうち、
 パラメータ名がこの属性に指定された値に **前方一致** するパラメータが、
 ウィンドウスコープに設定される。

 例えば、 ``windowScopePrefixes="user"`` と指定すると、
 ``users`` で始まるパラメータもウィンドウスコープに設定される。

実装例
 検索機能の検索条件、更新機能の入力データを画面間で持ち回る。
 画面遷移とhiddenに格納されるデータの動きは以下のとおり。

 .. image:: images/tag/window_scope.png

 \ 検索条件のリクエストパラメータは ``searchCondition.*`` 、
 入力データのリクエストパラメータは ``user.*`` とする。

 検索画面
  .. code-block:: jsp

   <!-- ウィンドウスコープのデータを送信しない。 -->
   <n:form>

 更新画面
  .. code-block:: jsp

   <!-- 検索条件だけ送信する。 -->
   <n:form windowScopePrefixes="searchCondition">

 更新確認画面
  .. code-block:: jsp

   <!--
     検索条件と入力データを送信する。
     複数指定する場合はカンマ区切りで指定する。
   -->
   <n:form windowScopePrefixes="searchCondition,user">

 更新完了画面
  .. code-block:: jsp

   <!-- 検索条件だけ送信する。 -->
   <n:form windowScopePrefixes="searchCondition">

.. important::
 データベースのデータについては、更新対象データを特定する主キーや楽観ロック用のデータなど、必要最低限に留めること。
 特に入力画面と確認画面で表示するデータ(入力項目ではなく、表示するだけの項目)等は、
 hiddenで引き回すのではなくデータが必要となる度にデータベースから取得すること。
 hiddenのデータ量が増えると、通信速度の低下、メモリ圧迫につながるため。

.. important::
 ウィンドウスコープに格納したデータは、hiddenタグに出力し、リクエストパラメータとして画面間を持ち回っている。
 そのため、アクション側でウィンドウスコープに格納したデータを使用する場合は、
 :ref:`バリデーション<validation>` を行う必要がある。

.. tip::
 :ref:`tag-form_tag` では、一律リクエストパラメータを全てhiddenタグに出力するのではなく、
 既に入力項目として出力したリクエストパラメータはhiddenタグの出力から除外する。

.. tip::
 ログイン情報など、全ての業務に渡って必要になる情報はサーバ側(セッション)に保持する。

.. _`tag-hidden_encryption`:

クライアントに保持するデータを暗号化する(hidden暗号化)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`ウィンドウスコープ<tag-window_scope>` や :ref:`tag-hidden_tag` の値は、
クライアント側で改竄されたり、HTMLソースから容易に値を参照できる。
そのため、hiddenタグの改竄や参照を防ぐことを目的に、カスタムタグではhidden暗号化機能を提供する。

デフォルトで全ての :ref:`tag-form_tag` で暗号化を行い、全てのリクエストで復号及び改竄チェックを行う。
このため、アプリケーションプログラマは、hidden暗号化機能に関して実装する必要がない。

hidden暗号化
 hidden暗号化は、 :ref:`tag-form_tag` と :ref:`nablarch_tag_handler` により実現する。
 hidden暗号化の処理イメージを以下に示す。
 :ref:`tag-form_tag` が暗号化、 :ref:`nablarch_tag_handler` が復号及び改竄チェックを行う。

 .. image:: images/tag/hidden_encryption.png

 \

暗号化処理
 暗号化は、 :java:extdoc:`Encryptor <nablarch.common.encryption.Encryptor>` インタフェースを実装したクラスが行う。
 フレームワークでは、デフォルトの暗号化アルゴリズムとして ``AES(128bit)`` を使用する。
 暗号化アルゴリズムを変更したい場合は、
 :java:extdoc:`Encryptor <nablarch.common.encryption.Encryptor>` を実装したクラスを
 コンポーネント定義に ``hiddenEncryptor`` という名前で追加する。

 暗号化では、:ref:`tag-form_tag` 毎に、 :ref:`tag-form_tag` に含まれる以下のデータをまとめて暗号化し、
 1つのhiddenタグで出力する。

 * カスタムタグの :ref:`tag-hidden_tag` で明示的に指定したhiddenパラメータ
 * :ref:`ウィンドウスコープ<tag-window_scope>` の値
 * :ref:`サブミットを行うカスタムタグ <tag_reference_submit>` で指定したリクエストID
 * :ref:`サブミットを行うカスタムタグ <tag_reference_submit>` で追加した :ref:`パラメータ<tag-submit_change_parameter>`

 さらに、暗号化では、改竄を検知するために、上記のデータから生成したハッシュ値を含める。
 リクエストIDは、異なる入力フォーム間で暗号化した値を入れ替えた場合の改ざんを検知するために、
 ハッシュ値は、値の書き換えによる改竄を検知するために使用する。
 暗号化した結果は、BASE64でエンコードしhiddenタグに出力する。

 .. tip::
  カスタムタグの :ref:`tag-hidden_tag` で明示的に指定したhiddenパラメータは、
  暗号化に含まれるため、クライアント側でJavaScriptを使用して値を操作できない。
  クライアント側のJavaScriptでhiddenパラメータを操作したい場合は、
  :ref:`tag-plain_hidden_tag` を使用して、暗号化しないhiddenタグを出力する。

.. _`tag-hidden_encryption_decryption`:

復号処理
 復号処理は、 :ref:`nablarch_tag_handler` が行う。
 :ref:`nablarch_tag_handler` では以下の場合に改竄と判定し、設定で指定された画面に遷移させる。

 * 暗号化したhiddenパラメータ(nablarch_hidden)が存在しない。
 * BASE64のデコードに失敗する。
 * 復号に失敗する。
 * 暗号化時に生成したハッシュ値と復号した値で生成したハッシュ値が一致しない。
 * 暗号化時に追加したリクエストIDと受け付けたリクエストのリクエストIDが一致しない。

暗号化に使用する鍵の保存場所
 暗号化に使用する鍵は、鍵の有効期間をできるだけ短くするため、セッション毎に生成する。
 このため、同じユーザであってもログインをやり直すと、ログイン前に使用していた画面から処理を継続できない。

hidden暗号化の設定
 hidden暗号化では、 :ref:`tag-setting` により、以下の設定ができる。

 useHiddenEncryptionプロパティ
  hidden暗号化を使用するか否か。
  デフォルトはtrue。
  開発時にHTMLソース上でhiddenタグの内容を確認する場合に指定する。

  .. important::
   本番環境では必ず暗号化を行うこと。

 noHiddenEncryptionRequestIdsプロパティ
  hidden暗号化を行わないリクエストID。

 noHiddenEncryptionRequestIdsプロパティには、以下のように、hidden暗号化を使用できないリクエストを指定する。

 * ログイン画面など、アプリケーションの入口となるリクエスト
 * ブックマークから遷移してくるリクエスト
 * 外部サイトから遷移してくるリクエスト

 これらのリクエストは、暗号化したhiddenパラメータ(nablarch_hidden)が存在しない、
 またはセッション毎に生成する鍵が存在しないため、noHiddenEncryptionRequestIdsプロパティを設定しないと改竄エラーとなる。

 noHiddenEncryptionRequestIdsプロパティの設定値は、
 :ref:`tag-form_tag` と :ref:`nablarch_tag_handler` が、
 それぞれ暗号化と復号を行う際に参照して処理を行う。

 :ref:`tag-form_tag`
  :ref:`tag-form_tag` に暗号化対象のリクエストIDが1つでも含まれていれば暗号化を行う。
  反対に、暗号化対象のリクエストIDが1つも含まれていない場合、 :ref:`tag-form_tag` は暗号化を行わない。

 :ref:`nablarch_tag_handler`
  リクエストされたリクエストIDが暗号化対象のリクエストIDの場合のみ、復号を行う。

.. _`tag-composite_key`:

複合キーのラジオボタンやチェックボックスを作る
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
一覧画面でデータを選択する場合などは、ラジオボタンやチェックボックスを使用する。
データを識別する値が単一であれば、 :ref:`tag-radio_tag` や :ref:`tag-checkbox_tag` を使用すればよいが、
複合キーの場合は単純に実装できない。

カスタムタグでは、複合キーに対応したラジオボタンやチェックボックスを提供する。

* :ref:`tag-composite_key_radio_button_tag` (複合キーに対応したラジオボタン)
* :ref:`tag-composite_key_checkbox_tag` (複合キーに対応したチェックボックス)

.. important::
 この機能を使用するには、
 :java:extdoc:`CompositeKeyConvertor <nablarch.common.web.compositekey.CompositeKeyConvertor>` と
 :java:extdoc:`CompositeKeyArrayConvertor <nablarch.common.web.compositekey.CompositeKeyArrayConvertor>`
 をコンポーネント定義に追加しておく必要がある。
 設定方法については、 :ref:`nablarch_validation-definition_validator_convertor` を参照。

.. important::
 この機能は、
 :java:extdoc:`CompositeKeyConvertor <nablarch.common.web.compositekey.CompositeKeyConvertor>` と
 :java:extdoc:`CompositeKeyArrayConvertor <nablarch.common.web.compositekey.CompositeKeyArrayConvertor>`
 を使用するため、 :ref:`nablarch_validation` でのみ使用できる。
 :ref:`bean_validation` は対応していない。

実装例
 一覧表示で複合キーをもつチェックボックスを使用する例を元に、実装方法を説明する。

 フォーム
  フォームでは、複合キーを保持するプロパティを
  :java:extdoc:`CompositeKey<nablarch.common.web.compositekey.CompositeKey>`
  として定義する。

  .. code-block:: java

   public class OrderItemsForm {

       // 今回は、一覧表示で複数データに対する複合キーを受け付けるので、
       // 配列として定義する。
       public CompositeKey[] orderItems;

       // getter, コンストラクタ等は省略。

       // CompositeKeyTypeアノテーションで複合キーのサイズを指定する。
       @CompositeKeyType(keySize = 2)
       public void setOrderItems(CompositeKey[] orderItems) {
           this.orderItems = orderItems;
       }
   }

 JSP
  .. code-block:: jsp

   <table>
     <thead>
       <tr>
         <!-- ヘッダ出力は省略。 -->
       </tr>
     </thead>
     <tbody>
       <c:forEach var="orderItem" items="${orderItems}">
       <tr>
         <td>
           <!--
             以下の属性を指定する。
             name属性: フォームのプロパティ名に合わせて指定する。
             valueObject属性: 複合キーの値を持つオブジェクトを指定する。
             keyNames属性: valueObject属性で指定したオブジェクトから
                           複合キーの値を取得する際に使用するプロパティ名を指定する。
                           ここに指定した順番でCompositeKeyに設定される。
             namePrefix属性: 複合キーの値をリクエストパラメータに展開する際に使用する
                             プレフィクスを指定する。
                             name属性と異なる値を指定する必要がある。
           -->
           <n:compositeKeyCheckbox
             name="form.orderItems"
             label=""
             valueObject="${orderItem}"
             keyNames="orderId,productId"
             namePrefix="orderItems" />
         </td>
         <!-- 以下略 -->
       </tr>
       </c:forEach>
     </tbody>
   </table>

.. _`tag-submit`:

複数のボタン/リンクからフォームをサブミットする
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
フォームのサブミットは、ボタンとリンクに対応しており、次のカスタムタグを使用して行う。
1つのフォームに複数のボタンとリンクを配置することができる。

フォームのサブミット
 | :ref:`tag-submit_tag` (inputタグのボタン)
 | :ref:`tag-button_tag` (buttonタグのボタン)
 | :ref:`tag-submit_link_tag` (リンク)

別ウィンドウを開いてサブミット(ポップアップ)
 | :ref:`tag-popup_submit_tag` (inputタグのボタン)
 | :ref:`tag-popup_button_tag` (buttonタグのボタン)
 | :ref:`tag-popup_link_tag` (リンク)

ダウンロード用のサブミット
 | :ref:`tag-download_submit_tag` (inputタグのボタン)
 | :ref:`tag-download_button_tag` (buttonタグのボタン)
 | :ref:`tag-download_link_tag` (リンク)

タグ名が ``popup`` から始まるタグは、新しいウィンドウをオープンし、
オープンしたウィンドウに対してサブミットを行う。
タグ名が ``download`` から始まるタグは、ダウンロード用のサブミットを行う。
それぞれ詳細は、以下を参照。

* :ref:`tag-submit_popup`
* :ref:`tag-submit_download`

これらのカスタムタグでは、ボタン/リンクとURIを関連付けるためにname属性とuri属性を指定する。
name属性は、フォーム内で一意な名前を指定する。name属性の指定がない場合は、カスタムタグで一意な名前が自動で出力される。
uri属性の指定方法については、 :ref:`tag-specify_uri` を参照。

実装例
 .. code-block:: jsp

  <!-- name属性は自動で出力されるので指定しなくてよい。 -->
  <n:submit type="submit" uri="login" value="ログイン" />

.. _`tag-onclick_override`:

サブミット前に処理を追加する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
フォームのサブミットは、JavaScriptを使用してボタン/リンク毎のURIを組み立てることで実現している。
カスタムタグは、グローバル領域にこのJavaScript関数を出力し、
ボタン/リンクのonclick属性にその関数呼び出しを設定した状態でHTML出力を行う。

.. _`tag-submit_function`:

カスタムタグが出力するJavaScript関数のシグネチャ
 .. code-block:: javascript

  /**
   * @param event イベントオブジェクト
   * @param element イベント元の要素(ボタン又はリンク)
   * @return イベントを伝搬させないため常にfalse
   */
  function nablarch_submit(event, element)

出力例を以下に示す。

JSP
 .. code-block:: jsp

  <n:form>
    <!-- 省略 -->
    <n:submit type="submit" uri="login" value="ログイン" />
  </n:form>

HTML
 .. code-block:: html

  <script type="text/javascript">
  <!--
  function nablarch_submit(event, element) {
    // 省略
  }
  -->
  </script>
  <form name="nablarch_form1" method="post">
    <!-- onclick属性にサブミット制御を行うJavaScript関数が設定される。 -->
    <input type="submit" name="nablarch_form1_1" value="ログイン"
           onclick="return window.nablarch_submit(event, this);" />
  </form>

サブミット前に処理を追加したい場合は、onclick属性にアプリケーションで作成したJavaScript関数を指定する。
カスタムタグは、onclick属性が指定された場合、サブミット用のJavaScript関数の指定を行わない。
この場合、アプリケーションで作成したJavaScriptで、カスタムタグが設定する :ref:`JavaScript関数 <tag-submit_function>` を呼び出す必要がある。

実装例
 サブミット前に確認ダイアログを表示する。

 JavaScript
  .. code-block:: javascript

   function popUpConfirmation(event, element) {
     if (window.confirm("登録します。よろしいですか？")) {
       // カスタムタグが出力するJavaScript関数を明示的に呼び出す。
       return nablarch_submit(event, element);
     } else {
       // キャンセル
       return false;
     }
   }

 JSP
  .. code-block:: jsp

   <n:submit type="submit" uri="register" value="登録"
             onclick="return popUpConfirmation(event, this);" />

.. _`tag-onchange_submit`:

プルダウン変更などの画面操作でサブミットする
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
カスタムタグは、サブミット制御にJavaScriptを使用しており、
サブミット制御を行うJavaScript関数が、ボタンやリンクのイベントハンドラ(onclick属性)に指定されることを前提に動作する。
JavaScriptの詳細については、 :ref:`tag-onclick_override` を参照。

そのため、プルダウン変更などの画面操作でサブミットを行いたい場合は、サブミットさせたいボタンのクリックイベントを発生させる。

プルダウン変更でサブミットを行う場合の実装例を示す。

実装例
 .. code-block:: jsp

  <!-- onchange属性にて、サブミットしたいボタン要素のclick関数を呼ぶ。 -->
  <n:select name="form.plan"
            listName="plans"
            elementLabelProperty="planName"
            elementValueProperty="planId"
            onchange="window.document.getElementById('register').click(); return false;" />

  <n:submit id="register" type="submit" uri="register" value="登録" />

 .. important::
  上記の実装例では、説明がしやすいので、onchangeイベントハンドラに直接JavaScriptを記載しているが、
  実際のプロジェクトでは、オープンソースのJavaScriptライブラリを使うなどして、処理を動的にバインドすることを推奨する。

.. _`tag-submit_change_parameter`:

ボタン/リンク毎にパラメータを追加する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
更新機能などにおいて、一覧画面から詳細画面に遷移するケースでは、
同じURLだけどパラメータが異なるリンクを表示したい場合がある。

カスタムタグでは、フォームのボタンやリンク毎にパラメータを追加するためのカスタムタグを提供する。

* :ref:`tag-param_tag` (サブミット時に追加するパラメータの指定)

実装例
 検索結果から一覧画面でリンク毎にパラメータを追加する。

 .. code-block:: jsp

  <n:form>
    <table>
      <!-- テーブルのヘッダ行は省略 -->
      <c:forEach var="person" items="${persons}">
        <tr>
          <td>
            <n:submitLink uri="/action/person/show">
              <n:write name="person.personName" />
              <!-- パラメータ名に"personId"を指定している。 -->
              <n:param paramName="personId" name="person.personId" />
            </n:submitLink>
          </td>
        </tr>
      </c:forEach>
    </table>
  </n:form>

.. important::
 パラメータを追加する場合は、その数に応じてリクエストのデータ量は増大する。
 そのため、一覧画面で詳細画面へのリンク毎にパラメータを追加する場合は、
 パラメータをプライマリキーだけにするなど、必要最小限のパラメータのみ追加する。

.. _`tag-submit_display_control`:

認可チェック/サービス提供可否に応じてボタン/リンクの表示/非表示を切り替える
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`permission_check` と :ref:`service_availability` の結果に応じて、
:ref:`フォームのサブミットを行うボタン/リンク<tag_reference_submit>` の表示を切り替える機能を提供する。
これにより、ユーザーが実際にボタン/リンクを選択する前に該当機能が使用可能かどうかが分かるため、ユーザビリティの向上につながる。

:ref:`フォームのサブミットを行うボタン/リンク<tag_reference_submit>`
に指定されたリクエストIDに対して、 :ref:`permission_check` と :ref:`service_availability` を行い、
``権限なし`` または ``サービス提供不可`` の場合に表示切り替えを行う。

切り替え時の表示方法には次の3パターンがある。

非表示
 タグを出力しない。

非活性
 タグを非活性にする。
 ボタンの場合は、disabled属性を有効にする。
 リンクの場合は、ラベルのみ表示するか、非活性リンク描画用JSPをインクルードする。
 JSPインクルードを行うには、 :ref:`tag-setting` で
 :java:extdoc:`submitLinkDisabledJspプロパティ<nablarch.common.web.tag.CustomTagConfig.setSubmitLinkDisabledJsp(java.lang.String)>`
 を指定する。

通常表示
 通常どおりタグが出力される。
 表示方法の切り替えを行わない。

デフォルトは、 ``通常表示`` である。
:ref:`tag-setting` で
:java:extdoc:`displayMethodプロパティ<nablarch.common.web.tag.CustomTagConfig.setDisplayMethod(java.lang.String)>`
を指定することで、デフォルトを変更できる。

個別に表示方法を変更したい場合は、displayMethod属性に指定する。

実装例
 .. code-block:: jsp

  <!--
    NODISPLAY(非表示)、DISABLED(非活性)、NORMAL(通常表示)のいずれかを指定する。
    このタグは常に表示する。
  -->
  <n:submit type="button" uri="login" value="ログイン" displayMethod="NORMAL" />

.. tip::
 アプリケーションで表示制御に使用する判定処理を変更したい場合は、
 :ref:`tag-submit_display_control_change` を参照。

.. _`tag-submit_popup`:

別ウィンドウ/タブを開くボタン/リンクを作る(ポップアップ)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ユーザの操作性を向上させるために、複数ウィンドウを立ち上げたい場合がある。
例えば、郵便番号の入力欄から住所検索など、検索画面を別ウィンドウで立ち上げ入力補助を行う場合がある。

カスタムタグでは、複数ウィンドウの立ち上げをサポートするカスタムタグ(以降はポップアップタグと称す)を提供する。

* :ref:`tag-popup_submit_tag` (inputタグのボタン)
* :ref:`tag-popup_button_tag` (buttonタグのボタン)
* :ref:`tag-popup_link_tag` (リンク)

.. important::

  これらのタグは、以下の問題点があるため非推奨とする。
  
  * 外部サイトへのリンクやボタンを作成した場合、一部のブラウザで新しいウィンドウでページを開けない。(例えば、IEの保護モードを有効にした場合発生する)
  
    :ref:`tag-a_tag` やhtmlタグを使用することでこの問題を回避できる。
    
  * サブウィンドウを用いた画面遷移は利便性が低い。
  
    ページ内にポップアップウィンドウを表示する方式が一般的であり、サブウィンドウを用いた検索などは今や時代遅れである。
    ページ内でのポップアップウィンドウの表示処理は、オープンソースライブラリを用いることで対応出来る。

ポップアップタグは、画面内のフォームに対するサブミットを行うカスタムタグと以下の点が異なる。

* 新しいウィンドウをオープンし、オープンしたウィンドウに対してサブミットを行う。
* 入力項目のパラメータ名を変更できる。

ポップアップは、JavaScriptのwindow.open関数を使用して実現する。

実装例
 指定したスタイルでウィンドウを開く検索ボタンを作成する。

 .. code-block:: jsp

  <!--
    以下の属性指定により、ウィンドウをオープンする動作を制御する。
    popupWindowName属性: ポップアップのウィンドウ名。
                         新しいウィンドウを開く際にwindow.open関数の第2引数に指定する。
    popupOption属性: ポップアップのオプション情報。
                     新しいウィンドウを開く際にwindow.open関数の第3引数に指定する。
  -->
  <n:popupButton uri="/action/person/list"
                 popupWindowName="postalCodeSupport"
                 popupOption="width=400, height=300, menubar=no, toolbar=no, scrollbars=yes">
    検索
  </n:popupButton>

popupWindowName属性が指定されない場合、 :ref:`tag-setting` で
:java:extdoc:`popupWindowNameプロパティ<nablarch.common.web.tag.CustomTagConfig.setPopupWindowName(java.lang.String)>`
に指定したデフォルト値が使用される。
デフォルト値が設定されていない場合、カスタムタグは、JavaScriptのDate関数から取得した現在時刻(ミリ秒)を新しいウィンドウの名前に使用する。
デフォルト値の指定有無により、ポップアップのデフォルト動作が以下のとおり決まる。

 デフォルト値を指定した場合
  常に同じウィンドウ名を使用するため、オープンするウィンドウが1つとなる。

 デフォルト値を指定しなかった場合
  常に異なるウィンドウ名を使用するため、常に新しいウィンドウをオープンする。

.. _`tag-submit_change_param_name`:

パラメータ名変更
 ポップアップタグは、元画面のフォームに含まれる全てのinput要素を動的に追加してサブミットする。
 ポップアップタグにより開いたウィンドウに対するアクションと、元画面のアクションでパラメータ名が一致するとは限らない。
 そのため、カスタムタグでは、元画面の入力項目のパラメータ名を変更するために以下のカスタムタグを提供する。

 * :ref:`tag-change_param_name_tag` (ポップアップ用のサブミット時にパラメータ名の変更)

 実装例
  画面イメージを以下に示す。

  .. image:: images/tag/popup_postal_code.png

  \

  検索ボタンが選択されると、郵便番号欄に入力された番号に該当する住所を検索する別ウィンドウを開く。

  .. code-block:: jsp

   <n:form>
     <div>
       <label>郵便番号</label>
       <n:text name="form.postalCode" />
       <n:popupButton uri="/action/postalCode/show">
         検索
         <!--
           郵便番号のパラメータ名"form.postalCode"を"condition.postalCode"に変更する。
         -->
         <n:changeParamName inputName="form.postalCode" paramName="condition.postalCode" />
         <!--
           パラメータの追加もできる。
         -->
         <n:param paramName="condition.max" value="10" />
       </n:popupButton>
     </div>
   </n:form>

.. _`tag-submit_access_open_window`:

オープンしたウィンドウへのアクセス方法
 別ウィンドウを開いた状態で元画面が遷移した場合、元画面が遷移するタイミングで不要となった別ウィンドウを全て閉じるなど、
 アプリケーションでオープンしたウィンドウにアクセスしたい場合がある。
 そのため、カスタムタグは、オープンしたウィンドウに対する参照をJavaScriptのグローバル変数に保持する。
 オープンしたウィンドウを保持する変数名を以下に示す。

 .. code-block:: javascript

  // keyはウィンドウ名
  var nablarch_opened_windows = {};

 元画面が遷移するタイミングで不要となった別ウィンドウを全て閉じる場合の実装例を以下に示す。

 .. code-block:: javascript

  // onunloadイベントハンドラにバインドする。
  // nablarch_opened_windows変数に保持されたWindowのclose関数を呼び出す。
  onunload = function() {
    for (var key in nablarch_opened_windows) {
      var openedWindow = nablarch_opened_windows[key];
      if (openedWindow && !openedWindow.closed) {
        openedWindow.close();
      }
    }
    return true;
  };

.. _`tag-submit_download`:

ファイルダウンロードを行うボタン/リンクを作る
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ファイルダウンロードを行うボタン/リンクを作るために、
ダウンロード専用のサブミットを行うカスタムタグ(以降はダウンロードタグと称す)と
アクションの実装を容易にする :java:extdoc:`HttpResponse <nablarch.fw.web.HttpResponse>`
のサブクラス(以降はダウンロードユーティリティと称す)を提供する。

ダウンロードタグ
 * :ref:`tag-download_submit_tag` (inputタグのボタン)
 * :ref:`tag-download_button_tag` (buttonタグのボタン)
 * :ref:`tag-download_link_tag` (リンク)

ダウンロードユーティリティ
 :java:extdoc:`StreamResponse <nablarch.common.web.download.StreamResponse>`
  ストリームからHTTPレスポンスメッセージを生成するクラス。
  ファイルシステム上のファイルやデータベースのBLOB型のカラムに格納したバイナリデータをダウンロードする場合に使用する。
  :java:extdoc:`File <java.io.File>` または :java:extdoc:`Blob <java.sql.Blob>` のダウンロードをサポートする。

 :java:extdoc:`DataRecordResponse <nablarch.common.web.download.DataRecordResponse>`
  データレコードからHTTPレスポンスメッセージを生成するクラス。
  検索結果など、アプリケーションで使用するデータをダウンロードする場合に使用する。
  ダウンロードされるデータは :ref:`data_format` を使用してフォーマットされる。
  Map<String, ?>型データ( :java:extdoc:`SqlRow <nablarch.core.db.statement.SqlRow>` など)のダウンロードをサポートする。

.. important::
 カスタムタグではフォームのサブミット制御にJavaScriptを使用しているため、
 画面内のフォームに対するサブミット( :ref:`tag-submit_tag` など)でダウンロードを行うと、
 同じフォーム内の他のサブミットが機能しなくなる。
 そこで、カスタムタグでは、画面内のフォームに影響を与えずにサブミットを行うダウンロードタグを提供する。
 ダウンロードを行うボタンやリンクには必ずダウンロードタグを使用すること。

ダウンロードタグは、画面内のフォームに対するサブミットを行うカスタムタグと以下の点が異なる。

* 新しいフォームを作成し、新規に作成したフォームに対してサブミットを行う。
* 入力項目のパラメータ名を変更できる。

パラメータ名の変更は、 :ref:`tag-change_param_name_tag` を使用して行う。
:ref:`tag-change_param_name_tag` の使い方はポップアップタグと同じなので、
:ref:`ポップアップ時のパラメータ名変更 <tag-submit_change_param_name>` を参照。

ファイルのダウンロードの実装例
 ボタンが押されたらサーバ上のファイルをダウンロードする。

 JSP
  .. code-block:: jsp

   <!-- downloadButtonタグを使用してダウンロードボタンを作る。 -->
   <n:downloadButton uri="/action/download/tempFile">ダウンロード</n:downloadButton>

 アクション
  .. code-block:: java

   public HttpResponse doTempFile(HttpRequest request, ExecutionContext context) {

       // ファイルを取得する処理はプロジェクトの実装方式に従う。
       File file = getTempFile();

       // Fileのダウンロードには、StreamResponseを使用する。
       // コンストラクタ引数にダウンロード対象のファイルと
       // リクエスト処理の終了時にファイルを削除する場合はtrue、削除しない場合はfalseを指定する。
       // ファイルの削除はフレームワークが行う。
       // 通常ダウンロード用のファイルはダウンロード後に不要となるためtrueを指定する。
       StreamResponse response = new StreamResponse(file, true);

       // Content-Typeヘッダ、Content-Dispositionヘッダを設定する。
       response.setContentType("application/pdf");
       response.setContentDisposition(file.getName());

       return response;
   }

BLOB型カラムのダウンロードの実装例
 テーブルの行データ毎にリンクを表示し、
 選択されたリンクに対応するデータをダウンロードする。

 テーブル
  ==================== ==================== ==================== ====================
  カラム(論理名)       カラム(物理名)       データ型             補足
  ファイルID           FILE_ID              CHAR(3)              PK
  ファイル名           FILE_NAME            NVARCHAR2(100)
  ファイルデータ       FILE_DATA            BLOB
  ==================== ==================== ==================== ====================

 JSP
  .. code-block:: jsp

   <!--
     recordsという名前で行データのリストが
     リクエストスコープに設定されているものとする。
   -->
   <c:forEach var="record" items="${records}" varStatus="status">
     <n:set var="fileId" name="record.fileId" />
     <div>
       <!-- downloadLinkタグを使用してリンクを作成する。 -->
       <n:downloadLink uri="/action/download/tempFile">
         <n:write name="record.fileName" />(<n:write name="fileId" />)
         <!-- 選択されたリンクを判別するためにfileIdパラメータをparamタグで設定する。 -->
         <n:param paramName="fileId" name="fileId" />
       </n:downloadLink>
     </div>
   </c:forEach>

 アクション
  .. code-block:: java

   public HttpResponse tempFile(HttpRequest request, ExecutionContext context) {

       // fileIdパラメータを使用して選択されたリンクに対応する行データを取得する。
       SqlRow record = getRecord(request);

       // BlobのダウンロードにはStreamResponseクラスを使用する。
       StreamResponse response = new StreamResponse((Blob) record.get("FILE_DATA"));

       // Content-Typeヘッダ、Content-Dispositionヘッダを設定する。*/
       response.setContentType("image/jpeg");
       response.setContentDisposition(record.getString("FILE_NAME"));
       return response;
   }

データレコードのダウンロードの実装例
 テーブルの全データをCSV形式でダウンロードする。

 テーブル
  ==================== ==================== ==================== ====================
  カラム(論理名)       カラム(物理名)       データ型             補足
  メッセージID         MESSAGE_ID           CHAR(8)              PK
  言語                 LANG                 CHAR(2)              PK
  メッセージ           MESSAGE              NVARCHAR2(200)
  ==================== ==================== ==================== ====================

 フォーマット定義
  .. code-block:: bash

   #-------------------------------------------------------------------------------
   # メッセージ一覧のCSVファイルフォーマット
   # N11AA001.fmtというファイル名でプロジェクトで規定された場所に配置する。
   #-------------------------------------------------------------------------------
   file-type:        "Variable"
   text-encoding:    "Shift_JIS" # 文字列型フィールドの文字エンコーディング
   record-separator: "\n"        # レコード区切り文字
   field-separator:  ","         # フィールド区切り文字

   [header]
   1   messageId    N "メッセージID"
   2   lang         N "言語"
   3   message      N "メッセージ"

   [data]
   1   messageId    X # メッセージID
   2   lang         X # 言語
   3   message      N # メッセージ

 JSP
  .. code-block:: jsp

   <!-- downloadSubmitタグを使用してダウンロードボタンを実装する。 -->
   <n:downloadSubmit type="button" uri="/action/download/tempFile" value="ダウンロード" />

 アクション
  .. code-block:: java

   public HttpResponse doCsvDataRecord(HttpRequest request, ExecutionContext context) {

       // レコードを取得する。
       SqlResultSet records = getRecords(request);

       // データレコードのダウンロードにはDataRecordResponseクラスを使用する。
       // コンストラクタ引数にフォーマット定義のベースパス論理名と
       // フォーマット定義のファイル名を指定する。
       DataRecordResponse response = new DataRecordResponse("format", "N11AA001");

       // DataRecordResponse#writeメソッドを使用してヘッダーを書き込む。
       // フォーマット定義に指定したデフォルトのヘッダー情報を使用するため、
       // 空のマップを指定する。
       response.write("header", Collections.<String, Object>emptyMap());

       // DataRecordResponse#writeメソッドを使用してレコードを書き込む。
       for (SqlRow record : records) {

           // レコードを編集する場合はここで行う。

           response.write("data", record);
       }

       // Content-Typeヘッダ、Content-Dispositionヘッダを設定する。*/
       response.setContentType("text/csv; charset=Shift_JIS");
       response.setContentDisposition("メッセージ一覧.csv");

       return response;
   }

.. _`tag-double_submission`:

二重サブミットを防ぐ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
二重サブミットの防止は、データベースにコミットを伴う処理を要求する画面で使用する。
二重サブミットの防止方法は、クライアント側とサーバ側の2つがあり、2つの防止方法を併用する。

クライアント側では、ユーザが誤ってボタンをダブルクリックした場合や、
リクエストを送信したがサーバからのレスポンスが返ってこないので再度ボタンをクリックした場合に、
リクエストを2回以上送信するのを防止する。

一方、サーバ側では、ブラウザの戻るボタンにより完了画面から確認画面に遷移し再度サブミットした場合など、
アプリケーションが既に処理済みのリクエストを重複して処理しないように、処理済みリクエストの受け付けを防止する。

.. important::
 二重サブミットを防止する画面では、どちらか一方のみ使用した場合は以下の懸念がある。

 * クライアント側のみ使用した場合は、リクエストを重複して処理する恐れがある。
 * サーバ側のみ使用した場合は、ボタンのダブルクリックにより2回リクエストが送信されると、
   サーバ側の処理順によっては二重サブミットエラーが返されてしまい、ユーザに処理結果が返されない恐れがある。

.. _`tag-double_submission_client_side`:

クライアント側の二重サブミット防止
 クライアント側では、JavaScriptを使用して実現する。
 1回目のサブミット時に対象要素のonclick属性を書き換え、2回目以降のサブミット要求はサーバ側に送信しないことで防止する。
 さらにボタンの場合は、disabled属性を設定し、画面上でボタンをクリックできない状態にする。

 次のカスタムタグが対応している。

 フォームのサブミット
  | :ref:`tag-submit_tag` (inputタグのボタン)
  | :ref:`tag-button_tag` (buttonタグのボタン)
  | :ref:`tag-submit_link_tag` (リンク)
 ダウンロード用のサブミット
  | :ref:`tag-download_submit_tag` (inputタグのボタン)
  | :ref:`tag-download_button_tag` (buttonタグのボタン)
  | :ref:`tag-download_link_tag` (リンク)

 上記カスタムタグのallowDoubleSubmission属性に ``false`` を指定することで、
 特定のボタン及びリンクだけを対象に二重サブミットを防止する。

 実装例
  登録ボタンはデータベースにコミットを行うので、登録ボタンのみ二重サブミットを防止する。

  .. code-block:: jsp

   <!--
     allowDoubleSubmission属性: 二重サブミットを許可するか否か。
                                許可する場合は true 、許可しない場合は false 。
                                デフォルトは true 。
   -->
   <n:submit type="button" name="back" value="戻る" uri="./back" />
   <n:submit type="button" name="register" value="登録" uri="./register"
             allowDoubleSubmission="false" />

 .. tip::
  クライアント側の二重サブミット防止を使用している画面では、
  サブミット後にサーバ側からレスポンスが返ってこない(サーバ側の処理が重たいなど)ため、
  ユーザがブラウザの中止ボタンを押した場合、
  ボタンはクリックできない状態(disabled属性により非活性)が続くため、再度サブミットできなくなる。
  この場合、ユーザは、サブミットに使用したボタン以外のボタン又はリンクを使用して処理を継続することができる。

 .. tip::
  アプリケーションで二重サブミット発生時の振る舞いを追加したい場合は、
  :ref:`tag-double_submission_client_side_change` を参照。

.. _`tag-double_submission_server_side`:

サーバ側の二重サブミット防止
 サーバ側では、サーバ側で発行した一意なトークンをサーバ側(セッション)とクライアント側(hiddenタグ)に保持し、
 サーバ側で突合することで実現する。このトークンは、1回のチェックに限り有効である。

 サーバ側の二重サブミット防止では、トークンの設定を行うJSPとトークンのチェックを行うアクションにおいて、
 それぞれ作業が必要となる。

 .. _`tag-double_submission_token_setting`:

 トークンの設定を行う
  :ref:`tag-form_tag` のuseToken属性を指定することで行う。

  実装例
   .. code-block:: jsp

    <!--
      useToken属性: トークンを設定するか否か。
                    トークンを設定する場合は true 、設定しない場合は false 。
                    デフォルトは false 。
                    入力画面と確認画面を共通化した場合、確認画面ではデフォルトが true となる。
                    そのため、入力画面と確認画面を共通化した場合は指定しなくてよい。
    -->
    <n:form useToken="true">

 トークンのチェック
  トークンのチェックは、 :ref:`on_double_submission_interceptor` を使用する。
  使用方法の詳細は、 :ref:`on_double_submission_interceptor` を参照。

 .. important::
  サーバ側の二重サブミット防止では、トークンをサーバ側のセッションに格納しているため、
  同一ユーザの複数リクエストに対して、別々にトークンをチェックすることができない。

  このため、同一ユーザにおいて、サーバ側の二重サブミット防止を行う画面遷移
  (登録確認→登録完了や更新確認→更新完了など)のみ、
  複数ウィンドウや複数タブを使用して並行で行うことができない。

  これらの画面遷移を並行して行った場合は、後に確認画面に遷移した画面のみ処理を継続でき、
  先に確認画面に遷移した画面はトークンが古いため、二重サブミットエラーとなる。

 .. tip::
  トークンの発行は、 :java:extdoc:`RandomTokenGenerator <nablarch.common.web.token.RandomTokenGenerator>` が行う。
  :java:extdoc:`RandomTokenGenerator <nablarch.common.web.token.RandomTokenGenerator>`
  では、16文字のランダムな文字列を生成する。
  トークンの発行処理を変更したい場合は、:ref:`tag-double_submission_server_side_change` を参照。

.. _`tag-make_common`:

入力画面と確認画面を共通化する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`入力項目のカスタムタグ <tag_reference_input>` は、
入力画面と全く同じJSP記述のまま、確認画面用の出力を行うことができる。

入力画面と確認画面の共通化は、以下のカスタムタグを使用する。

:ref:`tag-confirmation_page_tag`
 確認画面のJSPで入力画面のJSPへのパスを指定して、入力画面と確認画面の共通化を行う。

:ref:`tag-for_input_page_tag`
 入力画面でのみ表示したい部分を指定する。

:ref:`tag-for_confirmation_page_tag`
 確認画面でのみ表示したい部分を指定する。

:ref:`tag-ignore_confirmation_tag`
 確認画面で、確認画面向けの表示を無効化したい部分に指定する。
 例えば、チェックボックスを使用した項目で、確認画面でもチェック欄を表示したい場合などに使用する。

実装例
 以下の画面出力を行うJSPの実装例を示す。

 .. image:: images/tag/make_common_input_confirm.png

 \

 入力画面のJSP
  .. code-block:: jsp

   <n:form>
     <!--
       入力欄は、入力画面と確認画面で同じJSP記述を使用する。
     -->
     <div>
       <label>名前</label>
       <n:text name="form.name" />
     </div>
     <div>
       <label>メール</label>
       <n:checkbox name="form.useMail" label="使用する" offLabel="使用しない" />
     </div>
     <div>
       <label>プラン</label>
       <n:select name="form.plan"
                 listName="plans"
                 elementLabelProperty="planName"
                 elementValueProperty="planId" />
     </div>
     <!--
      ボタン表示は、入力画面と確認画面で異なるので、
      forInputPageタグとforConfirmationPageタグを使用する。
     -->
     <div style="padding: 8px 0;">
       <n:forInputPage>
         <n:submit type="submit" uri="/action/sample/confirm" value="確認" />
       </n:forInputPage>
       <n:forConfirmationPage>
         <n:submit type="submit" uri="/action/sample/showNew" value="戻る" />
         <n:submit type="submit" uri="/action/sample/register" value="登録" />
       </n:forConfirmationPage>
     </div>
   </n:form>

 確認画面のJSP
  .. code-block:: jsp

   <!--
     入力画面のJSPへのパスを指定する。
   -->
   <n:confirmationPage path="./input.jsp" />

.. _`tag-set_variable`:

変数に値を設定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
画面タイトルなど、ページ内の複数箇所に同じ内容で出力する値は、
JSP上の変数に格納したものを参照することで、メンテナンス性を高められる。

カスタムタグでは変数に値を設定する :ref:`tag-set_tag` を提供する。

実装例
 画面タイトルを変数に設定して使用する。

 .. code-block:: jsp

  <!-- var属性に変数名を指定する。-->
  <n:set var="title" value="ユーザ情報登録" />
  <head>
    <!-- 変数の出力にはwriteタグを使用する。 -->
    <title><n:write name="title" /></title>
  </head>
  <body>
    <h1><n:write name="title" /></h1>
  </body>

.. important::
 :ref:`tag-set_tag` で設定した変数を使用して出力する場合、
 :ref:`tag-set_tag` ではHTMLエスケープ処理を実施しないため、実装例のように :ref:`tag-write_tag` を使用して出力すること。

変数を格納するスコープを指定する
 変数を格納するスコープは、scope属性で指定する。
 scope属性には、リクエストスコープ(request)又はページスコープ(page)を指定する。

 scope属性の指定がない場合、変数はリクエストスコープに設定される。

 ページスコープは、アプリケーション全体で共通利用されるUI部品を作成する場合に、他JSPの変数とのバッティングを防ぎたい場合に使用する。

変数に配列やコレクションの値を設定する
 :ref:`tag-set_tag` は、name属性が指定された場合、デフォルトで単一値として値を取得する。
 単一値での値取得では、name属性に対応する値が配列やコレクションの場合に先頭の要素を返す。

 多くのケースはデフォルトのままで問題ないが、共通利用されるUI部品を作成する場合に、
 配列やコレクションをそのまま取得したい場合がある。

 このようなケースでは、 :ref:`tag-set_tag` のbySingleValue属性に ``false`` を指定することで、
 配列やコレクションをそのまま取得することができる。

.. _`tag-using_get`:

GETリクエストを使用する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
検索エンジン等のクローラ対策、および利用者がブックマーク可能なURLとするために、GETリクエストの使用が必要となる場合がある。

カスタムタグは、 :ref:`hidden暗号化<tag-hidden_encryption>` や
:ref:`パラメータ追加<tag-submit_change_parameter>` といった機能を実現するため、
hiddenパラメータを出力して使用している。
そのため、 :ref:`tag-form_tag` を使用してGETリクエストを行おうとすると、業務機能として必要なパラメータに加えて、
このhiddenパラメータがURLに付与されてしまう。
その結果、不要なパラメータが付くことに加えて、URLの長さ制限により正しくリクエストできない可能性がある。

そこで、カスタムタグは、 :ref:`tag-form_tag` でGETが指定された場合、hiddenパラメータを出力しない。
これにより、 :ref:`tag-form_tag` でGETリクエストを使用しても上記問題が発生しないが、
hiddenパラメータが出力されないことで、使用制限のあるカスタムタグや使用不可となるカスタムタグが出てくる。
ここでは、それらのカスタムタグについて対応方法を説明する。

使用制限のあるカスタムタグ
 使用制限のあるカスタムタグを以下に示す。

 * :ref:`tag-checkbox_tag`
 * :ref:`tag-code_checkbox_tag`

 これらのカスタムタグは、 :ref:`チェックなしの場合にリクエストパラメータを設定する機能 <tag-checkbox_off_value>` があるが、
 :ref:`hidden暗号化<tag-hidden_encryption>` を使用して処理を行っているため、GETリクエストでは使用できない。

 対応方法
  GETリクエストでチェックボックスを使用した場合のチェックなしの判定は、
  :ref:`バリデーション <validation>` 後に該当項目の値についてnull判定で行う。
  そして、null判定の結果でチェック有無を判断し、アクション側でチェックなしに対する値を設定する。

使用不可となるカスタムタグ
 使用不可となるカスタムタグを以下に示す。

 * :ref:`hiddenタグ <tag-using_get_hidden_tag>`
 * :ref:`submitタグ <tag-using_get_submit_tag>`
 * :ref:`buttonタグ <tag-using_get_button_tag>`
 * :ref:`submitLinkタグ <tag-using_get_submit_link_tag>`
 * :ref:`popupSubmitタグ <tag-using_get_popup_submit_tag>`
 * :ref:`popupButtonタグ <tag-using_get_popup_button_tag>`
 * :ref:`popupLinkタグ <tag-using_get_popup_link_tag>`
 * :ref:`paramタグ <tag-using_get_param_tag>`
 * :ref:`changeParamNameタグ <tag-using_get_change_param_name_tag>`

 使用不可のタグに対する対応方法と実装例を以下に示す。

 .. _`tag-using_get_hidden_tag`:

 hiddenタグ
  対応方法
   :ref:`tag-plain_hidden_tag` を使用する。

  実装例
   .. code-block:: jsp

    <%-- POSTの場合 --%>
    <n:hidden name="test" />

    <%-- GETの場合 --%>
    <n:plainHidden name="test" />


 .. _`tag-using_get_submit_tag`:

 submitタグ
  対応方法
   HTMLのinputタグ(type=”submit”)を使用する。
   サブミット先のURIは :ref:`tag-form_tag` のaction属性に指定する。

  実装例
   .. code-block:: jsp

    <%-- POSTの場合 --%>
    <n:form>
      <n:submit type="button" uri="search" value="検索" />
    </n:form>

    <%-- GETの場合 --%>
    <n:form method="GET" action="search">
      <input type="submit" value="検索" />
    </n:form>

 .. _`tag-using_get_button_tag`:

 buttonタグ
  対応方法
   HTMLのbuttonタグ(type=”submit”)を使用する。
   サブミット先のURIは :ref:`tag-form_tag` のaction属性に指定する。

  実装例
   .. code-block:: jsp

    <%-- POSTの場合 --%>
    <n:form>
      <n:button type="submit" uri="search" value="検索" />
    </n:form>

    <%-- GETの場合 --%>
    <n:form method="GET" action="search">
      <button type="submit" value="検索" />
    </n:form>

 .. _`tag-using_get_submit_link_tag`:

 submitLinkタグ
  対応方法
   :ref:`tag-a_tag` を使用し、onclick属性に画面遷移を行うJavaScript関数を指定する。
   画面遷移を行う関数は :ref:`tag-script_tag` 内に記述する。

  実装例
   .. code-block:: jsp

    <%-- POSTの場合 --%>
    <n:form>
      <n:text name="test" />
      <n:submitLink type="button" uri="search" value="検索" />
    </n:form>

    <%-- GETの場合 --%>
    <input type="text" name="test" id="test" />
    <n:a href="javascript:void(0);" onclick="searchTest();">検索</n:a>
    <n:script type="text/javascript">
      var searchTest = function() {
        var test = document.getElementById('test').value;
        location.href = 'search?test=' + test;
      }
    </n:script>

 .. _`tag-using_get_popup_submit_tag`:

 popupSubmitタグ
  対応方法
   HTMLのinputタグ(type=”button”)を使用し、onclick属性にJavaScriptのwindow.open()関数を指定する。

  実装例
   .. code-block:: jsp

    <%-- POSTの場合 --%>
    <n:form>
      <n:popupSubmit type="button" value="検索" uri="search"
        popupWindowName="popupWindow" popupOption="width=700,height=500" />
    </n:form>

    <%-- GETの場合 --%>
    <n:form method="GET">
      <input type="button" value="検索"
        onclick="window.open('search', 'popupWindow', 'width=700,height=500')" />
    </n:form>

 .. _`tag-using_get_popup_button_tag`:

 popupButtonタグ
  対応方法
   HTMLのbuttonタグ(type=”submit”)を使用し、onclick属性にJavaScriptのwindow.open()関数を指定する。

  実装例
   .. code-block:: jsp

    <%-- POSTの場合 --%>
    <n:form>
      <n:popupButton type="submit" value="検索" uri="search"
        popupWindowName="popupWindow" popupOption="width=700,height=500" />
    </n:form>

    <%-- GETの場合 --%>
    <n:form method="GET">
      <button type="button" value="検索"
        onclick="window.open('search', 'popupWindow', 'width=700,height=500')" />
    </n:form>

 .. _`tag-using_get_popup_link_tag`:

 popupLinkタグ
  対応方法
   :ref:`tag-a_tag` を使用し、onclick属性にポップアップウィンドウの表示を行うJavaScript関数を指定する。
   画面遷移を行う関数は :ref:`tag-script_tag` 内に記述する。

  実装例
   .. code-block:: jsp

    <%-- POSTの場合 --%>
    <n:form>
      <n:text name="test" />
      <n:popupLink type="button" value="検索" uri="search"
        popupWindowName="popupWindow" popupOption="width=700,height=500" />
    </n:form>

    <%-- GETの場合 --%>
    <input type="text" name="test" id="test" />
    <n:a href="javascript:void(0);" onclick="openTest();" >検索</n:a>
    <n:script type="text/javascript">
      var openTest = function() {
        var test = document.getElementById('test').value;
        window.open('search?test=' + test,
                    'popupWindow', 'width=700,height=500')
      }
    </n:script>

 .. _`tag-using_get_param_tag`:

 paramタグ
  対応方法
   パラメータを追加したいボタンやリンク毎に :ref:`tag-form_tag` を記述し、そのform内にそれぞれパラメータを設定する。

  実装例
   .. code-block:: jsp

    <%-- POSTの場合 --%>
    <n:form>
      <n:submit type="button" uri="search" value="検索">
        <n:param paramName="changeParam" value="テスト１"/>
      </n:submit>
      <n:submit type="button" uri="search" value="検索">
        <n:param paramName="changeParam" value="テスト２"/>
      </n:submit>
    </n:form>

    <%-- GETの場合 --%>
    <n:form method="GET" action="search">
      <n:set var="test" value="テスト１" />
      <input type="hidden" name="changeParam" value="<n:write name='test' />" />
      <input type="submit" value="検索" />
    </n:form>

    <n:form method="GET" action="search">
      <n:set var="test" value="テスト２" />
      <input type="hidden" name="changeParam" value="<n:write name='test' />" />
      <input type="submit" value="検索" />
    </n:form>

 .. _`tag-using_get_change_param_name_tag`:

 changeParamNameタグ
  対応方法
   基本的な対応方法は :ref:`popupLinkタグ <tag-using_get_popup_link_tag>` と同じ。
   ポップアップウィンドウの表示を行う関数内のwindow.open()の第一引数に、
   クエリストリングのキーを変更したいパラメータ名で指定する。

  実装例
   .. code-block:: jsp

    <%-- POSTの場合 --%>
    <n:form>
      <n:text name="test" />
      <n:popupSubmit type="button" value="検索" uri="search"
          popupWindowName="popupWindow" popupOption="width=700,height=500">
        <n:changeParamName inputName="test" paramName="changeParam" />
      </n:popupSubmit>
    </n:form>

    <%-- GETの場合 --%>
    <input type="text" name="test" id="test" />
    <input type="button" value="検索" onclick="openTest();" />
    <n:script type="text/javascript">
      var openTest = function() {
        var test = document.getElementById('test').value;
        window.open('search?changeParam=' + test,
                    'popupWindow', 'width=700,height=500');
      }
    </n:script>

.. _`tag-write_value`:

値を出力する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
値の出力には、 :ref:`tag-write_tag` を使用する。

アクション側でリクエストスコープに設定したオブジェクトに、name属性を指定することでアクセスする。
name属性の指定方法は、 :ref:`tag-access_rule` を参照。

実装例
 アクション
  .. code-block:: java

   // リクエストスコープに"person"という名前でオブジェクトを設定する。
   Person person = new Person();
   person.setPersonName("名前");
   context.setRequestScopedVar("person", person);

 JSP
  .. code-block:: jsp

   <!-- name属性を指定してオブジェクトのpersonNameプロパティにアクセスする。 -->
   <n:write name="person.personName" />

.. _`tag-html_unescape`:

HTMLエスケープせずに値を出力する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
アクションなどで設定された値をページ上に出力する場合、 :ref:`tag-write_tag` を使用するが、
HTMLエスケープを行わず、変数内のHTMLタグを直接出力したい場合は、以下のカスタムタグを使用する。

* :ref:`prettyPrintタグ <tag-html_unescape_pretty_print_tag>`
* :ref:`rawWriteタグ <tag-html_unescape_raw_write_tag>`

これらのカスタムタグは、システム管理者がメンテナンス情報を設定できるようなシステムで、
特定の画面や表示領域のみで使用することを想定している。

.. _`tag-html_unescape_pretty_print_tag`:

:ref:`tag-pretty_print_tag`
 ``<b>`` や ``<del>`` のような装飾系のHTMLタグをエスケープせずに出力するカスタムタグ。
 使用可能なHTMLタグ及び属性は、 :ref:`tag-setting` で
 :java:extdoc:`safeTagsプロパティ<nablarch.common.web.tag.CustomTagConfig.setSafeTags(java.lang.String[])>` /
 :java:extdoc:`safeAttributesプロパティ<nablarch.common.web.tag.CustomTagConfig.setSafeAttributes(java.lang.String[])>`
 で任意に設定することができる。
 デフォルトで使用可能なタグ、属性はリンク先を参照。

 .. important::
  :ref:`tag-pretty_print_tag` で出力する変数の内容が、不特定のユーザによって任意に設定できるものであった場合、
  脆弱性の要因となる可能性があるため、使用可能なHTMLタグ及び属性を設定する場合は、その選択に十分に留意すること。
  例えば、<script>タグやonclick属性を使用可能とした場合、クロスサイトスクリプティング(XSS)脆弱性の直接要因となるため、
  これらのタグや属性を使用可能としないこと。

.. _`tag-html_unescape_raw_write_tag`:

:ref:`tag-raw_write_tag`
 変数中の文字列の内容をエスケープせずにそのまま出力するカスタムタグ。

 .. important::
  :ref:`tag-raw_write_tag` で出力する変数の内容が、不特定のユーザによって任意に設定できるものであった場合、
  クロスサイトスクリプティング(XSS)脆弱性の直接の要因となる。
  そのため、 :ref:`tag-raw_write_tag` の使用には十分な考慮が必要である。

.. _`tag-format_value`:

フォーマットして値を出力する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
カスタムタグでは、 :ref:`tag-write_tag` と :ref:`tag-text_tag` については、
日付や金額などの値を人が見やすい形式にフォーマットして出力する機能を提供する。

valueFormat属性を指定することでフォーマット出力を行う。valueFormat属性の指定がない場合は、フォーマットせずに値を出力する。

valueFormat属性
 出力時のフォーマット。

 フォーマットは、 ``データタイプ{パターン}`` 形式で指定する。
 カスタムタグでデフォルトで提供しているデータタイプを以下に示す。

 * :ref:`yyyymmdd (年月日)<tag-format_yyyymmdd>`
 * :ref:`yyyymm (年月)<tag-format_yyyymm>`
 * :ref:`dateTime (日時)<tag-format_datetime>`
 * :ref:`decimal (10進数)<tag-format_decimal>`

 .. _`tag-format_yyyymmdd`:

 yyyymmdd
  年月日のフォーマット。

  値はyyyyMMdd形式またはパターン形式の文字列を指定する。
  パターンには :java:extdoc:`SimpleDateFormat <java.text.SimpleDateFormat>` が規定している構文を指定する。
  パターン文字には、y(年)、M(月)、d(月における日)のみ指定可能。
  パターン文字列を省略した場合は、 :ref:`tag-setting` (yyyymmddPatternプロパティ)に設定されたデフォルトのパターンを使用する。

  また、パターンの後に区切り文字 ``|`` を使用してフォーマットのロケールを指定できる。
  ロケールを明示的に指定しない場合は、
  :java:extdoc:`ThreadContext <nablarch.core.ThreadContext>` の言語を使用する。
  :java:extdoc:`ThreadContext <nablarch.core.ThreadContext>` が設定されていない場合は、
  システムデフォルトロケール値を使用する。

  実装例
   .. code-block:: properties

    # デフォルトのパターンとスレッドコンテキストに設定されたロケールを使用する。
    valueFormat="yyyymmdd"

    # 明示的に指定されたパターンと、スレッドコンテキストに設定されたロケールを使用する。
    valueFormat="yyyymmdd{yyyy/MM/dd}"

    # デフォルトのパターンを使用し、ロケールのみ指定する場合。
    valueFormat="yyyymmdd{|ja}"

    # パターン、ロケールの両方を明示的に指定する場合。
    valueFormat="yyyymmdd{yyyy年MM月d日|ja}"

  .. important::
   :ref:`tag-text_tag` のvalueFormat属性を指定した場合、
   入力画面にもフォーマットした値が出力される。
   入力された年月日をアクションで取得する場合は、 :ref:`ウィンドウスコープ <tag-window_scope>` および
   :java:extdoc:`Nablarch独自のバリデーションが提供する年月日コンバータ <nablarch.common.date.YYYYMMDDConvertor>`
   を使用する。
   :ref:`tag-text_tag` と :ref:`ウィンドウスコープ <tag-window_scope>` 、
   :java:extdoc:`年月日コンバータ <nablarch.common.date.YYYYMMDDConvertor>`
   が連携し、valueFormat属性に指定されたパターンを使用した値変換とバリデーションを行う。

   なお、 :ref:`bean_validation` は :ref:`tag-text_tag` のvalueFormat属性に対応していない。

  .. important::
   :ref:`ウィンドウスコープ <tag-window_scope>` を使用しない場合は、 :ref:`tag-text_tag` のvalueFormat属性を指定しても
   valueFormat属性の値がサーバサイドに送信されないためバリデーションエラーが発生してしまう。
   その場合は :java:extdoc:`YYYYMMDD <nablarch.common.date.YYYYMMDD>` アノテーションのallowFormat属性を指定することで、
   入力値のチェックを行うことができる。

 .. _`tag-format_yyyymm`:

 yyyymm
  年月のフォーマット。

  値はyyyyMM形式またはパターン形式の文字列を指定する。
  使用方法は、 :ref:`yyyymmdd (年月日)<tag-format_yyyymmdd>` と同じ。

 .. _`tag-format_dateTime`:

 dateTime
  日時のフォーマット。

  値は :java:extdoc:`Date <java.util.Date>` 型を指定する。
  パターンには
  :java:extdoc:`SimpleDateFormat <java.text.SimpleDateFormat>`
  が規定している構文を指定する。
  デフォルトでは、 :java:extdoc:`ThreadContext <nablarch.core.ThreadContext>` に設定された
  言語とタイムゾーンに応じた日時が出力される。
  また、パターン文字列の後に区切り文字 ``|`` を使用してロケールおよびタイムゾーンを明示的に指定することができる。

  :ref:`tag-setting` (dateTimePatternプロパティ、patternSeparatorプロパティ)を使用して、
  パターンのデフォルト値の設定と、区切り文字 ``|`` の変更を行うことができる。

  実装例
   .. code-block:: properties

    # デフォルトのパターンとThreadContextに設定されたロケール、タイムゾーンを使用する場合。
    valueFormat="dateTime"

    #デフォルトのパターンを使用し、ロケールおよびタイムゾーンのみ指定する場合。
    valueFormat="dateTime{|ja|Asia/Tokyo}"

    # デフォルトのパターンを使用し、タイムゾーンのみ指定する場合。
    valueFormat="dateTime{||Asia/Tokyo}"

    # パターン、ロケール、タイムゾーンを全て指定する場合。
    valueFormat="dateTime{yyyy年MMM月d日(E) a hh:mm|ja|America/New_York}}"

    # パターンとタイムゾーンを指定する場合。
    valueFormat="dateTime{yy/MM/dd HH:mm:ss||Asia/Tokyo}"

 .. _`tag-format_decimal`:

 decimal
  10進数のフォーマット。

  値は :java:extdoc:`Number <java.lang.Number>` 型又は数字の文字列を指定する。
  文字列の場合、3桁ごとの区切り文字(1,000,000のカンマ)を取り除いた後でフォーマットされる。
  パターンには :java:extdoc:`DecimalFormat <java.text.DecimalFormat>` が規定している構文を指定する。

  デフォルトでは、 :java:extdoc:`ThreadContext <nablarch.core.ThreadContext>` に設定された言語を使用して、
  言語に応じた形式で値が出力される。
  言語を直接指定することで、指定された言語に応じた形式で値を出力することもできる。
  言語の指定は、パターンの末尾に区切り文字 ``|`` を使用して言語を付加することで行う。

  :ref:`tag-setting` (patternSeparatorプロパティ)を使用して、区切り文字 ``|`` の変更を行うことができる。

  実装例
   .. code-block:: properties

    # ThreadContextに設定された言語を使用し、パターンのみ指定する場合。
    valueFormat="decimal{###,###,###.000}"

    # パターンと言語を指定する場合。
    valueFormat="decimal{###,###,###.000|ja}"

  .. important::
   :ref:`tag-text_tag` のvalueFormat属性を指定した場合、入力画面にもフォーマットした値が出力される。
   入力された数値をアクションで取得する場合は数値コンバータ(
   :java:extdoc:`BigDecimalConvertor <nablarch.core.validation.convertor.BigDecimalConvertor>` 、
   :java:extdoc:`IntegerConvertor <nablarch.core.validation.convertor.IntegerConvertor>` 、
   :java:extdoc:`LongConvertor <nablarch.core.validation.convertor.LongConvertor>`
   )を使用する。
   :ref:`tag-text_tag` と数値コンバータが連携し、valueFormat属性に指定された言語に対応する値変換とバリデーションを行う。

   なお、 :ref:`bean_validation` は :ref:`tag-text_tag` のvalueFormat属性に対応していない。

  .. tip::
   パターンに桁区切りと小数点を指定する場合は、言語に関係なく常に桁区切りにカンマ、小数点にドットを使用すること。

   .. code-block:: properties

    # es(スペイン語)の場合は、桁区切りがドット、小数点がカンマにフォーマットされる。
    # パターン指定では常に桁区切りにカンマ、小数点にドットを指定する。
    valueFormat="decimal{###,###,###.000|es}"

    # 下記は不正なパターン指定のため実行時例外がスローされる。
    valueFormat="decimal{###.###.###,000|es}"

.. _`tag-write_error`:

エラー表示を行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
エラー表示では、以下の機能を提供する。

* :ref:`エラーメッセージの一覧表示 <tag-write_error_errors_tag>`
* :ref:`エラーメッセージの個別表示 <tag-write_error_error_tag>`
* :ref:`入力項目のハイライト表示 <tag-write_error_css>`

.. tip::
 エラー表示に使用するカスタムタグでは、リクエストスコープから
 :java:extdoc:`ApplicationException<nablarch.core.message.ApplicationException>`
 を取得してエラーメッセージを出力する。
 :java:extdoc:`ApplicationException<nablarch.core.message.ApplicationException>` は、
 :ref:`on_error_interceptor` を使用して、リクエストスコープに設定する。

.. _`tag-write_error_errors_tag`:

エラーメッセージの一覧表示
 画面上部にエラーメッセージを一覧表示する場合に :ref:`tag-errors_tag` を使用する。

 すべてのエラーメッセージを表示する場合
  \

  実装例
   .. code-block:: jsp

    <!-- filter属性に"all"を指定する。 -->
    <n:errors filter="all" errorCss="alert alert-danger" />

  出力結果
   .. image:: images/tag/errors_all.png

 入力項目に対応しないエラーメッセージのみを表示する場合
  \

  実装例
   アクション
    .. code-block:: java

     // データベースとの相関バリデーションなどで、ApplicationExceptionを送出する。
     throw new ApplicationException(
       MessageUtil.createMessage(MessageLevel.ERROR, "errors.duplicateName"));

   JSP
    .. code-block:: jsp

     <!-- filter属性に"global"を指定する。 -->
     <n:errors filter="global" errorCss="alert alert-danger" />

  出力結果
   .. image:: images/tag/errors_global.png

.. _`tag-write_error_error_tag`:

エラーメッセージの個別表示
 入力項目ごとにエラーメッセージを表示する場合に :ref:`tag-error_tag` を使用する。

 実装例
  .. code-block:: jsp

   <div>
     <label>名前</label>
     <n:text name="form.userName" />
     <!-- 入力項目と同じ名前をname属性に指定する。 -->
     <n:error name="form.userName" messageFormat="span" errorCss="alert alert-danger" />
   </div>

 出力結果
  .. image:: images/tag/error.png

 :ref:`bean_validation-correlation_validation` のエラーメッセージを特定の項目の近くに表示したい場合も、
 :ref:`tag-error_tag` を使用する。

 実装例
  フォーム
   .. code-block:: java

    // 相関バリデーションを行うメソッド
    // このプロパティ名でエラーメッセージが設定される。
    @AssertTrue(message = "パスワードが一致しません。")
    public boolean isComparePassword() {
        return Objects.equals(password, confirmPassword);
    }

  JSP
   .. code-block:: jsp

    <div>
      <label>パスワード</label>
      <n:password name="form.password" nameAlias="form.comparePassword" />
      <n:error name="form.password" messageFormat="span" errorCss="alert alert-danger" />
      <!--
        相関バリデーションで指定されるプロパティ名をname属性に指定する。
      -->
      <n:error name="form.comparePassword" messageFormat="span" errorCss="alert alert-danger" />
    </div>
    <div>
      <label>パスワード(確認用)</label>
      <n:password name="form.confirmPassword" nameAlias="form.comparePassword" />
      <n:error name="form.confirmPassword" messageFormat="span" errorCss="alert alert-danger" />
    </div>

 出力結果
  .. image:: images/tag/error_correlation_validation.png

.. _`tag-write_error_css`:

入力項目のハイライト表示
 入力項目のカスタムタグは、エラーの原因となった入力項目のclass属性に、
 元の値に対してCSSクラス名(デフォルトは”nablarch_error”)を追記する。

 このクラス名にCSSでスタイルを指定することで、エラーがあった入力項目をハイライト表示する。

 さらに、入力項目のカスタムタグでnameAlias属性を指定することで、
 複数の入力項目を紐付け、
 :ref:`bean_validation-correlation_validation` でエラーとなった場合に、
 複数の入力項目をハイライト表示できる。

 実装例
  CSS
   .. code-block:: css

    /* エラーがあった場合の入力項目の背景色を指定する。 */
    input.nablarch_error,select.nablarch_error {
      background-color: #FFFFB3;
    }

  JSP
   .. code-block:: jsp

    <div>
      <label>パスワード</label>
      <!-- nameAlias属性に相関バリデーションのプロパティ名を指定する。 -->
      <n:password name="form.password" nameAlias="form.comparePassword" />
      <n:error name="form.password" messageFormat="span" errorCss="alert alert-danger" />
      <n:error name="form.comparePassword" messageFormat="span" errorCss="alert alert-danger" />
    </div>
    <div>
      <label>パスワード(確認用)</label>
      <!-- nameAlias属性に相関バリデーションのプロパティ名を指定する。 -->
      <n:password name="form.confirmPassword" nameAlias="form.comparePassword" />
      <n:error name="form.confirmPassword" messageFormat="span" errorCss="alert alert-danger" />
    </div>

 出力結果
  .. image:: images/tag/error_css.png


.. _`tag-code_input_output`:

コード値を表示する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
カスタムタグでは、 :ref:`code` から取得したコード値の選択項目や表示項目を出力する
コード値専用のカスタムタグを提供する。

* :ref:`tag-code_tag` (コード値)
* :ref:`tag-code_select_tag` (コード値のプルダウン)
* :ref:`tag-code_checkbox_tag` (コード値のチェックボックス)
* :ref:`tag-code_radio_buttons_tag` (コード値の複数のラジオボタン)
* :ref:`tag-code_checkboxes_tag` (コード値の複数のチェックボックス)

:ref:`tag-code_tag` と :ref:`tag-code_select_tag` の実装例を示す。

実装例
 :ref:`code` のテーブルは以下とする。

 コードパターンテーブル
   ======= =========   ========  ===========
   ID      VALUE       PATTERN1  PATTERN2
   ======= =========   ========  ===========
   GENDER  MALE        1         1
   GENDER  FEMALE      1         1
   GENDER  OTHER       1         0
   ======= =========   ========  ===========

 コード名称テーブル
   ======= ========= ====  ==========  ==========  ===========
   ID      VALUE     LANG  SORT_ORDER  NAME        SHORT_NAME
   ======= ========= ====  ==========  ==========  ===========
   GENDER  MALE      ja    1           男性        男
   GENDER  FEMALE    ja    2           女性        女
   GENDER  OTHER     ja    3           その他      他
   ======= ========= ====  ==========  ==========  ===========

 :ref:`tag-code_tag` (コード値)
  JSP
   .. code-block:: jsp

    <!--
      以下の属性指定により、コード値の出力を制御する。
      codeId属性: コードID。
      pattern属性: 使用するパターンのカラム名。
                   デフォルトは指定なし。
      optionColumnName属性: 取得するオプション名称のカラム名。
      labelPattern属性: ラベルを整形するパターン。
                        使用できるプレースホルダは以下のとおり。
                        $NAME$: コード値に対応するコード名称
                        $SHORTNAME$: コード値に対応するコードの略称
                        $OPTIONALNAME$: コード値に対応するコードのオプション名称。
                                        このプレースホルダを使用する場合は、
                                        optionColumnName属性の指定が必須となる。
                        $VALUE$: コード値
                        デフォルトは$NAME$。
    -->
    <n:code name="user.gender"
            codeId="GENDER" pattern="PATTERN1"
            labelPattern="$VALUE$:$NAME$($SHORTNAME$)"
            listFormat="div" />

  出力されるHTML
   .. code-block:: jsp

    <!--
      "user.gender"が"FEMALE"の場合
      listFormat属性でdivを指定しているのでdivタグで出力される。
    -->
    <div>FEMALE:女性(女)</div>


 :ref:`tag-code_select_tag` (コード値のプルダウン)
  JSP
   .. code-block:: jsp

    <!--
      属性指定はcodeタグと同じ。
    -->
    <n:codeSelect name="form.gender"
                  codeId="GENDER" pattern="PATTERN2"
                  labelPattern="$VALUE$-$SHORTNAME$"
                  listFormat="div" />

  出力されるHTML
   .. code-block:: jsp

    <!-- "form.gender"が"FEMALE"の場合 -->

    <!-- 入力画面 -->
    <select name="form.gender">
      <option value="MALE">MALE-男</option>
      <option value="FEMALE" selected="selected">FEMALE-女</option>
    </select>

    <!-- 確認画面 -->
    <div>FEMALE-女</div>

.. important::
 カスタムタグでは、言語指定によるコード値の取得はできない。
 カスタムタグでは、 :java:extdoc:`CodeUtil<nablarch.common.code.CodeUtil>` のロケールを指定しないAPIを使用している。
 言語指定でコード値を取得したい場合は、アクションで
 :java:extdoc:`CodeUtil<nablarch.common.code.CodeUtil>`
 を使用して値を取得する。

.. _`tag-write_message`:

メッセージを出力する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
カスタムタグでは、 :ref:`message` を使用して取得したメッセージを出力するカスタムタグを提供する。

* :ref:`tag-message_tag` (メッセージ)

国際化を行うアプリケーションにおいて1つのJSPファイルで多言語に対応する場合、
:ref:`tag-message_tag` を使用することでユーザが選択した言語に応じて画面の文言を切り替えることができる。

実装例
 .. code-block:: jsp

  <!-- messageId属性にメッセージIDを指定する。 -->
  <n:message messageId="page.not.found" />

  <!--
    オプションを指定したい場合
  -->

  <!-- var属性を指定して埋め込み用の文言を取得する。-->
  <n:message var="title" messageId="title.user.register" />
  <n:message var="appName" messageId="title.app" />

  <!-- 埋め込み用の文言をoption属性に設定する。-->
  <n:message messageId="title.template" option0="${title}" option1="${appName}" />

  <!--
    画面内で一部のメッセージのみ言語を切り替えたい場合
  -->

  <!-- language属性に言語を指定する。 -->
  <n:message messageId="page.not.found" language="ja" />

  <!--
    HTMLエスケープしたくない場合
  -->

  <!-- htmlEscape属性にfalseを指定する。 -->
  <n:message messageId="page.not.found" htmlEscape="false" />

.. _tag_change_resource_path_of_lang:

言語毎にリソースパスを切り替える
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
リソースパスを扱うカスタムタグは、言語設定をもとにリソースパスを動的に切り替える機能をもつ。
以下のカスタムタグが言語毎のリソースパスの切り替えに対応している。

* :ref:`tag-a_tag`
* :ref:`tag-img_tag`
* :ref:`tag-link_tag`
* :ref:`tag-script_tag`
* :ref:`tag-confirmation_page_tag` (入力画面と確認画面を共通化)
* :ref:`tag-include_tag` (インクルード)

これらのカスタムタグでは、
:java:extdoc:`ResourcePathRule<nablarch.fw.web.i18n.ResourcePathRule>`
のサブクラスを使用して言語毎のリソースパスを取得することで切り替えを行う。
デフォルトで提供するサブクラスについては、 :ref:`http_response_handler-change_content_path` を参照。

.. tip::
 :ref:`tag-include_tag` は動的なJSPインクルードを言語毎のリソースパスの切り替えに対応させるために提供している。
 :ref:`tag-include_param_tag` を使用してインクルード時に追加するパラメータを指定する。

 .. code-block:: jsp

  <!-- path属性にインクルードするリソースのパスを指定する。 -->
  <n:include path="/app_header.jsp">
      <!--
        paramName属性にパラメータ名、value属性に値を指定する。
        スコープ上に設定された値を使用する場合はname属性を指定する。
        name属性とvalue属性のどちらか一方を指定する。
      -->
      <n:includeParam paramName="title" value="ユーザ情報詳細" />
  </n:include>

ブラウザのキャッシュを防止する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ブラウザのキャッシュを防止することで、ブラウザの戻るボタンが押された場合に、
前画面を表示できないようにすることができる。
これにより、複数ユーザで同じ端末を使用するような環境において、
ブラウザ操作により個人情報や機密情報が漏洩するのを防ぐ。

ブラウザのキャッシュ防止は、 :ref:`tag-no_cache_tag` を使用する。
ブラウザの戻るボタンは、画面表示時にキャッシュしておいた画面を再表示するので、
キャッシュを防止したい画面のJSPで :ref:`tag-no_cache_tag` を使用する。

実装例
 .. code-block:: jsp

  <!-- headタグ内にnoCacheタグを指定する。 -->
  <head>
    <n:noCache/>
    <!-- 以下省略。 -->
  </head>

:ref:`tag-no_cache_tag` を指定すると、以下のレスポンスヘッダとHTMLがブラウザに返る。

レスポンスヘッダ
 .. code-block:: bash

  Expires Thu, 01 Jan 1970 00:00:00 GMT
  Cache-Control no-store, no-cache, must-revalidate, post-check=0, pre-check=0
  Pragma no-cache

HTML
 .. code-block:: html

  <head>
    <meta http-equiv="pragma" content="no-cache">
    <meta http-equiv="cache-control" content="no-cache">
    <meta http-equiv="expires" content="0">
  </head>

.. important::
 :ref:`tag-no_cache_tag` は、 :ref:`tag-include_tag` (<jsp:include>)でincludeされるJSPでは指定できないため、
 必ずforwardされるJSPで指定すること。
 ただし、システム全体でブラウザのキャッシュ防止を使用する場合は、
 各JSPで実装漏れが発生しないように、
 プロジェクトで :ref:`ハンドラ <nablarch_architecture-handler_queue>` を作成し一律設定すること。
 :ref:`ハンドラ <nablarch_architecture-handler_queue>` では、上記のレスポンスヘッダ例の内容をレスポンスヘッダに設定する。

.. tip::
 HTTPの仕様上は、レスポンスヘッダのみを指定すればよいはずであるが、
 この仕様に準拠していない古いブラウザのためにmetaタグも指定している。

.. tip::
 ブラウザのキャッシュ防止は、以下のブラウザでHTTP/1.0かつSSL(https)が適用されない通信において有効にならない。
 このため、ブラウザのキャッシュ防止を使用する画面は、必ずSSL通信を適用するように設計すること。

 問題が発生するブラウザ： IE6, IE7, IE8

静的コンテンツのクライアント側でのキャッシュを強制的に破棄する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
クライアント側(ブラウザ)でキャッシュを有効化している場合、
サーバ上に配置した静的コンテンツを置き換えても、
クライアント側では最新のコンテンツではなくキャッシュされた古いコンテンツが表示される可能性がある。

この問題を回避するため、カスタムタグでは静的コンテンツのURIにパラメータでバージョンを付加し、
静的コンテンツ置き換え時にクライアント側のキャッシュを強制的に破棄する機能を提供する。

パラメータに付加する静的コンテンツのバージョンは、 :ref:`設定ファイル(configファイル)<repository-environment_configuration>` に設定する。
設定ファイルに静的コンテンツのバージョンが設定されていない場合は、この機能は無効化される。

静的コンテンツのバージョンは、 ``static_content_version`` というキー名で指定する。

設定例
 .. code-block:: properties

  # 静的コンテンツのバージョン
  static_content_version=1.0

拡張例
---------------------------------------------------------------------

フォーマッタを追加する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
フォーマットは、
:java:extdoc:`ValueFormatter <nablarch.common.web.tag.ValueFormatter>`
インタフェースを実装したクラスが行う。
実装したクラスをコンポーネント定義に追加することでフォーマットを変更することができる。

コンポーネント定義への追加は、Map型でデータタイプ名をキーに、
:java:extdoc:`ValueFormatter <nablarch.common.web.tag.ValueFormatter>`
を実装したクラスを値に指定する。

フレームワークがデフォルトでサポートしているフォーマットに対する設定例を以下に示す。

フォーマッタのマップは、 ``valueFormatters`` という名前でコンポーネント定義に追加する。

.. code-block:: xml

 <map name="valueFormatters">
   <entry key="yyyymmdd">
     <value-component class="nablarch.common.web.tag.YYYYMMDDFormatter" />
   </entry>
   <entry key="yyyymm">
     <value-component class="nablarch.common.web.tag.YYYYMMFormatter" />
   </entry>
   <entry key="dateTime">
     <value-component class="nablarch.common.web.tag.DateTimeFormatter" />
   </entry>
   <entry key="decimal">
     <value-component class="nablarch.common.web.tag.DecimalFormatter" />
   </entry>
 </map>

.. _`tag-submit_display_control_change`:

ボタン/リンクの表示制御に使う判定処理を変更する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`tag-submit_display_control` に使用する判定処理を変更したい場合は、
:java:extdoc:`DisplayControlChecker <nablarch.common.web.tag.DisplayControlChecker>`
インタフェースを実装することで変更できる。
実装したクラスを :ref:`tag-setting` で
:java:extdoc:`displayControlCheckersプロパティ<nablarch.common.web.tag.CustomTagConfig.setDisplayControlCheckers(java.util.List)>`
に指定する。

設定例
 .. code-block:: xml

  <list name="displayControlCheckers" >
    <!-- サービス提供可否についてはデフォルトのDisplayControlCheckerを指定する -->
    <component class="nablarch.common.web.tag.ServiceAvailabilityDisplayControlChecker" />
    <!-- 認可チェックについてはプロジェクトでカスタマイズしたDisplayControlCheckerを指定する -->
    <component class="com.sample.app.CustomPermissionDisplayControlChecker" />
  </list>

  <component name="customTagConfig"
             class="nablarch.common.web.tag.CustomTagConfig">
     <!-- 判定条件を設定する。 -->
    <property name="displayControlCheckers" ref="displayControlCheckers" />
  </component>

.. _`tag-double_submission_client_side_change`:

クライアント側の二重サブミット防止で、二重サブミット発生時の振る舞いを追加する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`クライアント側の二重サブミット防止 <tag-double_submission_client_side>` を使用していて、
アプリケーションで二重サブミット発生時の振る舞いを追加する場合は、JavaScriptでコールバック関数を実装する。

フレームワークのJavaScript関数は、2回目以降のサブミット要求が発生した場合、
コールバック関数が存在していれば、コールバック関数を呼び出す。
コールバック関数のシグネチャを以下に示す。

.. code-block:: js

 /**
  * @param element 二重サブミットが行われた対象要素(ボタン又はリンク)
  */
 function nablarch_handleDoubleSubmission(element) {
   // ここに処理を記述する。
 }

.. _`tag-double_submission_server_side_change`:

サーバ側の二重サブミット防止で、トークンの発行処理を変更する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:ref:`サーバ側の二重サブミット防止 <tag-double_submission_server_side>` を使用していて、
トークンの発行処理を変更したい場合は、
:java:extdoc:`TokenGenerator <nablarch.common.web.token.TokenGenerator>`
インタフェースを実装することで変更できる。
実装したクラスをコンポーネント定義に ``tokenGenerator`` という名前で追加する。

カスタムタグのルール
---------------------------------------------------------------------

.. _`tag-naming_rule`:

命名ルール
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
カスタムタグでは、CSSのクラス名やJavaScriptの関数名など、カスタムタグが規定する名前については、
個別アプリケーションと重複しないようにプレフィックス ``nablarch_`` を使用する。
そのため、個別アプリケーションでは、 ``nablarch_`` から始まる名前を使用しないこと。

この命名ルールの対象を以下に示す。

* HTMLの属性値
* CSSのクラス名
* JavaScriptの関数名とグローバル変数名
* ページスコープ、リクエストスコープ、セッションスコープの変数名

.. _`tag-access_rule`:

入力/出力データへのアクセスルール
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
入力項目や出力項目を出力するカスタムタグ( :ref:`tag-text_tag` や :ref:`tag-write_tag` など)では、
name属性の値に基づき、出力対象となるデータにアクセスする。

オブジェクトの種類に合わせて、name属性には以下の指定を行う。

* オブジェクト/Mapのプロパティにアクセスする場合は、ドット区切りを指定する。
* List/配列の要素にアクセスする場合は、角括弧(括弧内にインデックス)を指定する。

検索順序は次の通りで、最初に見つかった値を使用する。値が取得できない場合は、空文字列を出力する。

1. Pageスコープ
2. リクエストスコープ
3. リクエストパラメータ
4. セッションスコープ

オブジェクトの実装例
 \

 アクション
  .. code-block:: java

   // オブジェクトをリクエストスコープに設定する。
   PersonForm form = new PersonForm();
   form.setPersonName("名前");
   context.setRequestScopedVar("form", form);
   return new HttpResponse("/WEB-INF/view/sample/accessRuleObject.jsp");

 JSP
  .. code-block:: jsp

   <!-- ドット区切りを使う。 -->
   <n:text name="form.personName" />

Listの実装例
 \

 アクション
  .. code-block:: java

   // Listを持つオブジェクトをリクエストスコープに設定する。
   PersonsForm form = new PersonsForm();
   List<Person> persons = UniversalDao.findAll(Person.class);
   form.setPersons(persons);
   context.setRequestScopedVar("form", form);

 JSP
  .. code-block:: jsp

   <!-- インデックスを取得するためループをまわす。 -->
   <c:forEach items="${form.persons}" varStatus="status">
     <!--
       角括弧を使って要素にアクセスする。
       要素の値はドットを使ってアクセスする。
     -->
     <n:text name="form.persons[${status.index}].personName" />
   </c:forEach>

.. tip::
 検索対象にリクエストパラメータが含まれているのは、
 入力項目のカスタムタグで、入力フォームを再表示した場合に入力値を復元するためである。

 この動きは、NablarchのカスタムタグとJSTL(c:forEachやc:outなど)で異なるので、実装時に注意すること。
 JSTLのタグはリクエストパラメータの値にアクセスできないので、
 JSTLのタグを使用する場合は、アクション側で明示的にリクエストスコープに値を設定するなどの実装が必要になる。

.. tip::
 リクエストパラメータより先にリクエストスコープを検索するのは、
 入力フォームを再表示した場合に入力値を変更できるようにするためである。

 よくある例としては、ユーザが明示的に選択したことをシステム的に保証したいため、
 入力フォームを再表示する際に、ラジオボタンを未選択の状態に戻したい場合がある。

 このような場合は、アクション側でリクエストスコープに空文字を設定すると、
 ラジオボタンを未選択の状態に戻すことができる。

.. _`tag-specify_uri`:

URIの指定方法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
カスタムタグにおいてURIを指定する属性には、次のいずれかの方法で指定する。

 絶対URL
  http/httpsから始まるパス

  .. code-block:: jsp

   <n:a href="https://github.com/coastland">coastland</n:a>

  他システム連携などでアプリケーションとホストが異なるURIを指定する場合に使用する。
  カスタムタグは、指定されたパスをそのまま使用する。

 コンテキストからの相対パス
  /(スラッシュ)から始まるパス

  .. code-block:: jsp

   <n:submit type="submit" uri="/action/person/register" value="登録" />

  アプリケーション内のパスを指定する場合に使用する。
  カスタムタグは、指定されたパスの先頭にコンテキストパスを付加して使用する。

 現在のパスからの相対パス
  /(スラッシュ)から始まらないパス(絶対URLを除く)

  .. code-block:: jsp

   <n:submit type="submit" uri="login" value="ログイン" />

  アプリケーション内のパスを指定する場合に使用する。
  カスタムタグは、指定されたパスをそのまま使用する。

\

httpsとhttpの切り替え
 コンテキストからの相対パスを指定している場合は、カスタムタグのsecure属性を指定することで、
 URIのhttpsとhttpを切り替えることができる。

 secure属性が指定された場合は、カスタムタグの設定値(http用のポート番号、https用のポート番号、ホスト)と
 コンテキストパスを使用してURIを組み立てる。
 そのため、secure属性を使用するアプリケーションでは、
 :ref:`tag-setting` で
 :java:extdoc:`portプロパティ<nablarch.common.web.tag.CustomTagConfig.setPort(int)>` /
 :java:extdoc:`securePortプロパティ<nablarch.common.web.tag.CustomTagConfig.setSecurePort(int)>` /
 :java:extdoc:`hostプロパティ<nablarch.common.web.tag.CustomTagConfig.setHost(java.lang.String)>`
 を指定する。

 .. tip::
  secure属性は、遷移先のプロトコルを切り替えるボタンやリンクのみで使用する。
  遷移先のプロトコルが同じ場合(http→http、https→https)は、secure属性を指定しない。

 実装例
  secure属性の使用例を示す。

  カスタムタグの設定値
   :http用のポート番号: 8080
   :https用のポート番号: 443
   :ホスト: sample.co.jp

  http→httpsに切り替える場合
   \

   .. code-block:: jsp

    <!-- secure属性にtrueを指定する。 -->
    <n:submit type="button" name="login" value="ログイン" uri="/action/login" secure="true" />

   .. code-block:: bash

    # 組み立てられるURI
    https://sample.co.jp:443/<コンテキストパス>/action/login

  https→httpに切り替える場合
   \

   .. code-block:: jsp

    <!-- secure属性にfalseを指定する。 -->
    <n:submitLink name="logout" uri="/action/logout" secure="false">ログアウト</n:submitLink>

   .. code-block:: bash

    # 組み立てられるURI
    https://sample.co.jp:8080/<コンテキストパス>/action/logout

    # カスタムタグの設定でhttp用のポート番号を指定しなかった場合
    # ポート番号が出力されない。
    https://sample.co.jp/<コンテキストパス>/action/logout

.. _`tag-html_escape`:

HTMLエスケープと改行、半角スペース変換
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
HTMLエスケープ
 カスタムタグでは、原則として出力する際に全てのHTMLの属性についてHTMLエスケープを行う。
 以下に変換内容を示す。

 HTMLエスケープの変換内容
  | ``&`` → ``&amp;``
  | ``<`` → ``&lt;``
  | ``>`` → ``&gt;``
  | ``“`` → ``&#034;``
  | ``‘`` → ``&#039;``

 .. important::
  EL式はHTMLエスケープ処理を実施しないため、EL式を使用して値を出力しないこと。
  値を出力する場合は、 :ref:`tag-write_tag` などのカスタムタグを使用する。

  ただし、JSTLのforEachタグやカスタムタグの属性にオブジェクトを設定する場合など、
  直接出力しない箇所ではEL式を使用しても問題ない。

改行、半角スペース変換
 確認画面などに入力データを出力する際には、HTMLエスケープに加えて、改行と半角スペースの変換を行う。
 以下に変換内容を示す。

 改行、半角スペースの変換内容
  | ``改行コード(\n、\r、\r\n)`` → ``<br />``
  | ``半角スペース`` → ``&nbsp;``


:ref:`tag_reference`
---------------------------------------------------------------------
:ref:`tag_reference` を参照。
