.. _`client_create_4`:

データベースへの登録
==========================================
本章では、顧客情報をデータベースへ登録する処理について解説を行う。

:ref:`前へ<client_create_3>`

登録処理の実装
  `ClientAction` に顧客情報の登録処理を行うメソッドを追加する。

  ClientAction.java
    .. code-block:: java

      public HttpResponse create(HttpRequest request, ExecutionContext context) {

          Client client = SessionUtil.get(context, "client");

          UniversalDao.insert(client);

          SessionUtil.delete(context, "client");

          return new HttpResponse("redirect://complete");
      }

  この実装のポイント
    * :ref:`セッションストア <session_store>` から顧客エンティティを取り出して、 :ref:`universal_dao` を使用してデータベースに登録する。
    * :ref:`セッションストア <session_store>` から顧客情報を削除する。
    * レスポンスオブジェクトの遷移先として、登録完了画面の表示処理へのリダイレクトを指定する(完了画面でのブラウザの更新ボタン押下による顧客情報の多重登録を防ぐため)。

二重サブミットを防止する
  ボタンをダブルクリックした場合等でリクエストが二重に送信されないように、業務アクションとJSPの二か所に制御を追加する。

  ClientAction.java
    .. code-block:: java

      @OnDoubleSubmission
      public HttpResponse create(HttpRequest request, ExecutionContext context) {

      // 実装は変更なし

      }

  この実装のポイント
    * :java:extdoc:`OnDoubleSubmission <nablarch.common.web.token.OnDoubleSubmission>` を付与して、
      業務アクションメソッドが二重に実行された場合にエラーページへ遷移させる。詳細は :ref:`tag-double_submission` を参照。

  .. tip::

    Exampleアプリケーションでは、二重サブミット時のデフォルトの遷移先画面を設定している。
    デフォルトの遷移先の指定方法は、 :ref:`tag-double_submission` を参照。

  /src/main/webapp/WEB-INF/view/client/create.jsp
    .. code-block:: jsp

      <!-- 修正しない部分は省略 -->
      <!-- 入力へ戻る、確定ボタンは確認画面でのみ表示 -->
        <n:forConfirmationPage>
            <n:button uri="/action/client/back"
                      cssClass="btn btn-raised btn-default">入力へ戻る</n:button>
            <!-- allowDoubleSubmission属性にfalseを指定する -->
            <n:button uri="/action/client/create"
                      allowDoubleSubmission="false"
                      cssClass="btn btn-raised btn-success">確定</n:button>
        </n:forConfirmationPage>

  この実装のポイント
    * :ref:`tag-button_tag` の `allowDoubleSubmission` 属性にfalseを指定することで、二重サブミットを制御するJavaScriptが追加される。
    * ブラウザのJavaScriptが無効になっている場合等を考慮して、サーバサイドでも二重サブミットの制御を行う。

登録完了画面の表示処理を実装する
  登録完了メッセージの設定と、登録完了画面の表示処理の実装を行う。

  完了メッセージを追加する
    messages.propertiesに新規メッセージを追加する。

    messages.properties
      .. code-block:: jproperties

        #その他のメッセージは省略
        success.insert.client=顧客の登録が完了しました。

  業務アクションメソッドを実装する
    登録完了画面の表示処理を実装する。

    ClientAction.java
      .. code-block:: java

        public HttpResponse complete(HttpRequest request, ExecutionContext context) {
            return new HttpResponse("/WEB-INF/view/client/complete.jsp");
        }

  登録完了画面のJSPを作成する
    ひな形となるJSPを `WEB-INF/view/client` 配下に配置する。

     :download:`complete.jsp <../downloads/client_create/complete.jsp>`

  登録完了画面を修正する
    メッセージエリアを追加する。

      /src/main/webapp/WEB-INF/view/client/complete.jsp
        .. code-block:: jsp

          <div class="title-nav">
              <span class="page-title">顧客登録完了画面</span>
          </div>

          <!-- メッセージエリア -->
          <div class="message-area">
              <n:message messageId="success.insert.client"/>
          </div>

    この実装のポイント
      * :ref:`message` を利用し、 :ref:`tag-message_tag` で登録完了メッセージを表示する。
      * :ref:`tag-write_message` を参照。

動作確認を行う
  以下の手順で、登録処理が正しく実装されていることを確認する。

  1. 顧客登録画面を表示する。

    .. image:: ../images/client_create/input_display.png

  2. 顧客名に全角文字列、業種に任意の値を選択して「登録」ボタンを押下する。

    .. image:: ../images/client_create/input_valid_value.png

  3. 登録確認画面が表示され、`2` で入力した顧客名、業種がラベルで表示されることを確認する。

    .. image:: ../images/client_create/confirm_display.png

  4. 「確定」ボタンを押下し、登録完了画面が表示されることを確認する。

    .. image:: ../images/client_create/complete_display.png

  5. サイドメニューの顧客欄の検索ボタンを押下し、顧客検索画面へ遷移する。

    .. image:: ../images/client_create/client_confirm_sidemenu.png

  6. 登録した顧客情報を検索できることを確認する。

    .. image:: ../images/client_create/client_search_result.png


登録機能の解説は以上。

:ref:`Getting Started TOPページへ <getting_started>`
