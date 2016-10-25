.. _`client_create_3`:

登録内容確認画面から登録画面へ戻る
==============================================
本章では、登録内容確認画面から登録画面へ戻る処理について解説を行う。

:ref:`前へ<client_create_2>`

登録画面へ戻る処理の実装
  `ClientAction` に登録画面へ戻る処理を行うメソッドを追加する。

  ClientAction.java
    .. code-block:: java
      :emphasize-lines: 1,2,3,4,5,6,7,8,9,13

      public HttpResponse back(HttpRequest request, ExecutionContext context) {

          Client client = SessionUtil.get(context, "client");

          ClientForm form = BeanUtil.createAndCopy(ClientForm.class, client);
          context.setRequestScopedVar("form", form);

          return new HttpResponse("forward://input");
      }

      public HttpResponse input(HttpRequest request, ExecutionContext context) {

          SessionUtil.delete(context, "client");

          EntityList<Industry> industries = UniversalDao.findAll(Industry.class);
          context.setRequestScopedVar("industries", industries);

          return new HttpResponse("/WEB-INF/view/client/create.jsp");
      }

  この実装のポイント
    *  :ref:`セッションストア <session_store>` から顧客情報を取得する。
    * 取得した顧客情報を登録画面に表示するため、:java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` を使用して顧客エンティティをフォームに変換し、リクエストスコープに登録する。
    * レスポンスオブジェクトの遷移先を、初期表示処理への内部フォーワードとする
      (登録画面を表示する際、再度プルダウンに表示する業種情報を取得するため)。
    * 初期表示処理で :ref:`セッションストア <session_store>` へ登録したオブジェクトの削除を行う(戻るボタンを押下せずにヘッダメニューから直接登録画面に遷移された場合等を考慮)。

動作確認を行う
  1. 登録画面を表示する。

    .. image:: ../images/client_create/input_display.png

  2. 顧客名に全角文字列、業種に任意の値を選択して「登録」ボタンを押下する。

    .. image:: ../images/client_create/input_valid_value.png

  3. 確認画面にて「入力へ戻る」ボタンを押下する。

    .. image:: ../images/client_create/confirm_display.png

  4. 登録画面が表示され、`2` で入力した値が画面に表示されていることを確認する。

    .. image:: ../images/client_create/input_back.png

:ref:`次へ<client_create_4>`