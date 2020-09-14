.. _`client_create_2`:

登録内容の確認
==========================================
本章では、登録した内容を確認する処理について解説を行う。

:ref:`前へ<client_create_1>`

登録画面へ入力項目を追加する
  登録確認画面への遷移を行うにあたり、まず顧客情報の登録に必要な以下の入力項目を登録画面に追加する。

  フォームの作成
    登録画面に入力された値を受け付けるため、 `ClientForm` クラスを新規作成する。

    ClientForm.java
      .. code-block:: java

        package com.nablarch.example.app.web.form;

        public class ClientForm implements Serializable {

            // 顧客名
            private String clientName;

            // 業種コード
            private String industryCode;

            // getter、setterは省略
        }

    この実装のポイント
      * フォームクラスには必ずセッタ及びゲッタを作成する。
      * :java:extdoc:`@InjectForm <nablarch.common.web.interceptor.InjectForm>` を使用してバリデーションを実行する( :ref:`後述<client_create-setup_validation>` )ために、フォームは `Serializable` インタフェースを実装する。
      * 入力値を受け付けるプロパティは全てString型で宣言する。詳細は :ref:`バリデーションルールの設定方法 <bean_validation-form_property>` を参照。

  登録画面のJSPを修正する
    登録画面のJSPに以下の項目を追加する。

    * :ref:`tag-text_tag` の `name` 属性に、顧客名を受け付けるフォームのプロパティ名を追加する。
    * :ref:`tag-select_tag` の `name` 属性に、業種コードを受け付けるフォームのプロパティ名を追加する。
    * 各タグの `name` 属性の指定方法は、 :ref:`tag-access_rule` を参照。
    * :ref:`tag-text_tag` 、 :ref:`tag-select_tag` に入力エラー発生時のCSSクラスを追加する。
    * 登録ボタン( :ref:`tag-button_tag` )の `uri` 属性に、登録確認画面へ遷移するURIを追加する。
      `uri` 属性の指定方法は、 :ref:`tag-specify_uri` を参照。
    * 入力エラー発生時のエラーメッセージ表示領域を追加する。

    /src/main/webapp/WEB-INF/view/client/create.jsp
      .. code-block:: jsp
        :emphasize-lines: 5,6,8,17,20,22,27

        <n:form>
            <div class="form-group label-static is-empty">
                <label class="control-label">顧客名</label>
                <!-- 顧客名のテキストボックス -->
                <n:text name="form.clientName"
                        cssClass="form-control input-text" errorCss="form-control input-error" />
                <!-- 顧客名の入力エラー時のエラーメッセージ -->
                <n:error errorCss="message-error" name="form.clientName" />
            </div>
            <div class="form-group label-static is-empty">
                <label class="control-label">業種</label>
                <!-- 業種のプルダウン -->
                <n:select
                        listName="industries"
                        elementValueProperty="industryCode"
                        elementLabelProperty="industryName"
                        name="form.industryCode"
                        withNoneOption="true"
                        cssClass="btn dropdown-toggle"
                        errorCss="btn dropdown-toggle input-error" />
                <!-- 業種の入力エラー時のエラーメッセージ -->
                <n:error errorCss="message-error" name="form.industryCode" />
            </div>
            <div class="button-nav">
                <!-- 登録ボタン -->
                <n:button
                        uri="/action/client/confirm"
                        cssClass="btn btn-raised btn-success">登録</n:button>
            </div>
        </n:form>

.. _`client_create_validation_rule`:

入力値のチェックルールを設定する
  :ref:`bean_validation` を使用して、入力値のチェックルールを設定する。

  ClientForm.java
    .. code-block:: java

      @Required
      @Domain("clientName")
      private String clientName;

      @Required(message = "{nablarch.core.validation.ee.Required.select.message}")
      @Domain("industryCode")
      private String industryCode;

   messages.properties
    .. code-block:: jproperties

      #その他のメッセージは省略
      #プルダウンに適した入力必須メッセージを追加する
      nablarch.core.validation.ee.Required.select.message=選択してください。

  この実装のポイント
    * :ref:`bean_validation` を行うためには、`nablarch.core.validation.ee` 配下のアノテーションを付与する
      ( `nablarch.core.validation.validator` 配下に同名アノテーションが存在する場合があるので注意)。
    * :ref:`ドメインバリデーション <bean_validation-domain_validation>` を使用して、`ClientForm` クラスのプロパティにバリデーションルールを定義する。
    * 対象項目に適したメッセージを表示するために、 :java:extdoc:`Required <nablarch.core.validation.ee.Required>` の `message` 属性に独自に定義したメッセージを指定する。
      メッセージ定義の詳細は :ref:`message-property_definition` を参照。

.. _`client_create-setup_validation`:

confirmメソッドを作成し、バリデーションが行われるように設定する
  実行前に入力値のチェックが行われるように設定したメソッドを作成する。

  ClientAction.java
    .. code-block:: java

      @InjectForm(form = ClientForm.class, prefix = "form")
      @OnError(type = ApplicationException.class, path = "forward://input")
      public HttpResponse confirm(HttpRequest request, ExecutionContext context) {

          // バリデーション済みオブジェクトを取得
          ClientForm form = context.getRequestScopedVar("form");

          // 実装内容については後述
      }

  この実装のポイント
      * 業務アクションメソッドに :java:extdoc:`InjectForm <nablarch.common.web.interceptor.InjectForm>` を付与して :ref:`bean_validation` を実行する。
      * :java:extdoc:`OnError <nablarch.fw.web.interceptor.OnError>` の `path` 属性で、バリデーションエラー発生時にinputメソッドへ内部フォーワードするよう設定する
        (登録画面を再表示するためには、業種リストを設定する必要があるため)。
      * バリデーションエラーが発生しなかった場合は、リクエストスコープからバリデーション済みオブジェクトが取得出来る。

登録確認画面の表示処理を実装する
  後続の登録処理に使用する顧客情報を :ref:`session_store` に保存し、登録確認画面を表示する。

  ClientAction.java
    .. code-block:: java

      @InjectForm(form = ClientForm.class, prefix = "form")
      @OnError(type = ApplicationException.class, path = "forward://input")
      public HttpResponse confirm(HttpRequest request, ExecutionContext context) {
          ClientForm form = context.getRequestScopedVar("form");

          Client client = BeanUtil.createAndCopy(Client.class, form);
          SessionUtil.put(context, "client", client);

          EntityList<Industry> industries = UniversalDao.findAll(Industry.class);
          context.setRequestScopedVar("industries", industries);

          return new HttpResponse("/WEB-INF/view/client/confirm.jsp");
      }

  この実装のポイント
    * 登録画面の表示処理時と同様、業種情報をデータベースから取得してリクエストスコープに設定する。
    *  :ref:`セッションストア <session_store>` への保存は、:java:extdoc:`SessionUtil <nablarch.common.web.session.SessionUtil>` を使用する。
    * :ref:`セッションストアにフォームは格納しない <session_store-form>` ため、
      :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` を使用してフォームをエンティティに変換した上で :ref:`セッションストア <session_store>` に登録する。
    * :ref:`セッションストア <session_store>` を利用する際の詳しい実装例は :ref:`create_example` を参照。

.. _`client_create_forConfirmationPage`:

登録確認画面のJSPを作成する
  登録確認画面のJSPを新規作成する。

  /src/main/webapp/WEB-INF/view/client/confirm.jsp
    .. code-block:: jsp

      <%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
      <%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
      <%@ taglib prefix="n" uri="http://tis.co.jp/nablarch" %>
      <!-- 登録画面を確認画面に変換して表示する -->
      <n:confirmationPage path="./create.jsp" ></n:confirmationPage>

  この実装のポイント
    * :ref:`tag-confirmation_page_tag` を使用することで、登録画面のJSPを流用して確認画面を作成できる。詳細は :ref:`tag-make_common` を参照。

登録画面を修正する
  登録画面のJSPを修正し、登録画面のみで表示する項目、確認画面でのみ表示する項目を出し分けられるようにする。

  /src/main/webapp/WEB-INF/view/client/create.jsp
    .. code-block:: jsp

      <div class="button-nav">
          <!-- 登録ボタンは登録画面でのみ表示 -->
          <n:forInputPage>
              <n:button uri="/action/client/confirm"
                        cssClass="btn btn-raised btn-success">登録</n:button>
          </n:forInputPage>
          <!-- 入力へ戻る、確定ボタンは確認画面でのみ表示 -->
          <n:forConfirmationPage>
              <n:button uri="/action/client/back"
                        cssClass="btn btn-raised btn-default">入力へ戻る</n:button>
              <n:button uri="/action/client/create"
                        cssClass="btn btn-raised btn-success">確定</n:button>
          </n:forConfirmationPage>
      </div>

  この実装のポイント
    * 登録画面のみで表示する項目は :ref:`tag-for_input_page_tag` の内部に記述する。
    * 確認画面でのみ表示する項目は :ref:`tag-for_confirmation_page_tag` の内部に記述する。

動作確認を行う
  登録確認処理が正しく実装されていることを確認するため、以下の手順で動作確認を実施する。

バリデーションエラーが発生しないケース
  1. 顧客登録画面を表示する。

    .. image:: ../images/client_create/input_display.png

  2. 顧客名に全角文字列、業種に任意の値を選択して確認ボタンを押下する。

    .. image:: ../images/client_create/input_valid_value.png

  3. 登録確認画面が表示され、`2` で入力した顧客名、業種がラベルで表示されることを確認する。

    .. image:: ../images/client_create/confirm_display.png

バリデーションエラーが発生するケース
  1. 顧客登録画面を表示する。

    .. image:: ../images/client_create/input_display.png

  2. 顧客名に半角文字列、業種を未選択にして確認ボタンを押下する。

    .. image:: ../images/client_create/input_invalid_value.png

  3. 登録画面が再度表示され、エラーメッセージが表示されていることを確認する。

    .. image:: ../images/client_create/input_invalid_display.png

:ref:`次へ<client_create_3>`
