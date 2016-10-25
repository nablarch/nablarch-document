.. _`client_popup`:

ポップアップ画面の作成
==========================================
Exampleアプリケーションを元にポップアップ画面の作成方法の解説を行う。

作成する機能の説明
  1. プロジェクト詳細画面の変更ボタンを押下する。

    .. image:: ../images/popup/popup-project_update_btn.png
      :scale: 80

  2. 顧客欄の検索ボタンを押下する。

    .. image:: ../images/popup/popup-project_update.png
      :scale: 80

  3. 顧客検索画面がポップアップで表示される。検索ボタンを押下する。

    .. image:: ../images/popup/popup-popup_init.png
      :scale: 80

  4. 検索結果の顧客IDのリンクを押下する。

    .. image:: ../images/popup/popup-popup_search.png
      :scale: 80

  5. 顧客検索画面が閉じられ、プロジェクト変更画面の顧客ID及び顧客名に選択した値が設定される。

    .. image:: ../images/popup/popup-complete.png
      :scale: 80

ポップアップ画面を表示する
---------------------------------
ポップアップ画面の基本的な実装方法を、以下の順に説明する。

  #. :ref:`ポップアップ画面を表示するボタンの作成<popup-open_popup>`
  #. :ref:`業務アクションメソッドの作成<popup-action>`
  #. :ref:`ポップアップ画面のJSPの作成<popup-popup_jsp>`
  #. :ref:`ポップアップ画面から親ウィンドウへ値を引き渡すJavaScriptの作成<popup-parent_hand_over>`

.. _`popup-open_popup`:

ポップアップ画面を表示するボタンの作成
  プロジェクト変更画面に、顧客検索画面へ遷移するボタンを配置する。

  /src/main/webapp/WEB-INF/view/project/update.jsp
    .. code-block:: jsp
      :emphasize-lines: 17,18,19

      <n:form useToken="true">
          <table class="table">
              <tbody>
                  <!-- 顧客以外の入力欄は省略 -->
                  <tr>
                      <th>
                          顧客名
                      </th>
                      <td>
                          <div class="form-group">
                              <n:text name="form.clientId" maxlength="10" readonly="true"
                                      cssClass="form-control input-label" tabindex="-1" />
                              <n:text name="form.clientName" maxlength="64" readonly="true"
                                      cssClass="form-control  input-label" tabindex="-1" />
                          </div>
                          <n:forInputPage>
                              <n:a href="/action/client/index" id="client_pop">
                                  <img src="/images/glass.png" alt="glass"/>
                              </n:a>
                          </n:forInputPage>
                          <n:error errorCss="message-error" name="form.clientId" />
                          <n:error errorCss="message-error" name="form.clientName" />
                      </td>
                  </tr>
                  <!-- 顧客以外の入力欄は省略 -->
              </tbody>
          </table>
          <div class="title-nav page-footer">
              <div class="button-nav">
                  <!-- ボタン部分は省略 -->
              </div>
          </div>
      </n:form>

  この実装のポイント
    *  :ref:`GETリクエストを行う場合、使用可能なカスタムタグが制限される<tag-using_get>` ため、ポップアップ画面への遷移はaタグ等で実装する。

  ポップアップ画面を開くJavaScript関数の登録
    顧客検索に遷移するボタンのクリックイベントに、ポップアップ画面を開くJavaScript関数を登録する。

    projectInput.js
      .. code-block:: javascript

        $(function() {
            // その他の関数は省略

            $("#client_pop").click(function() {
                window.open(this.href,"clientSearch","width=700,
                    height=500,resizable=yes,scrollbars=yes");
                return false;
              });

            // その他の関数は省略
        }

.. _`popup-action`:

業務アクションメソッドの作成
  顧客を検索し、選択の結果を親画面に引き渡す。

  画面の初期表示処理の作成方法に関しては、 :ref:`登録画面初期表示の作成<client_create_1>` を参照。
  検索処理についても、サーバサイドの実装はプロジェクト検索と同様であるため説明を省略する。作成方法に関しては :ref:`検索機能の作成<project_search>` を参照。

.. _`popup-popup_jsp`:

ポップアップ画面のJSPの作成
  リクエストの送信を介さずにポップアップ画面への入力値を親画面へ反映させるには、JavaScriptを用いて親画面のDOMを
  操作する。

  /src/main/webapp/WEB-INF/view/client/index.jsp
    .. code-block:: jsp
      :emphasize-lines: 16,17,18,19,20,21,22

      <!-- 検索結果の表示部分のみ記載 -->
      <n:form method="GET">
          <!-- listSearchResultの属性指定は省略 -->
          <app:listSearchResult>
              <jsp:attribute name="headerRowFragment">
                  <tr>
                      <th>顧客ID</th>
                      <th>顧客名</th>
                      <th>業種</th>
                  </tr>
              </jsp:attribute>
              <jsp:attribute name="bodyRowFragment">
                  <tr class="list-table x_color_row_table_target">
                      <td>
                          <!-- .clientLinkのonClickイベントによって親画面に値が設定される -->
                          <a href="#" class="clientLink">
                              <input type="hidden" class="clientId"
                                      value="<n:write name='row.clientId' />" />
                              <input type="hidden" class="clientName"
                                      value="<n:write name='row.clientName' />" />
                              <n:write name="row.clientId"/>
                          </a>
                      </td>
                      <td>
                          <n:write name="row.clientName"/>
                      </td>
                      <td>
                          <n:write name="row.industryName" />
                      </td>
                  </tr>
              </jsp:attribute>
          </app:listSearchResult>
          <br/>
          <div class="title-nav">
              <div class="button-nav">
                  <button class="btn btn-raised btn-success clearButton">クリア</button>
                  <button class="btn btn-raised btn-default closeButton">閉じる</button>
              </div>
          </div>
      </n:form>

  この実装のポイント
    * ポップアップ画面で選択した顧客を親ウィンドウへ設定するために、後述のJavaScriptでDOMを操作する関数をクリックイベントとして登録する。

.. _`popup-parent_hand_over`:

ポップアップ画面から親ウィンドウへ値を引き渡すJavaScript関数の作成
  clientList.js
    .. code-block:: javascript

      /**
       * 親ウィンドウの顧客名と顧客IDに、選択された顧客のIDと名前を設定するクリックイベントを登録する。
       * 設定後、ウィンドウを閉じる。
       */
       $(".clientLink").click(function() {
         window.opener.setClientParam($(this).children(".clientId").val(),
             $(this).children(".clientName").val());
         window.close();
       });

  projectInput.js(親画面のjavaScript)
    .. code-block:: javascript

      function setClientParam(clientId, clientName) {
        $("[name='form.clientId']").val(clientId);
        $("[name='form.clientName']").val(clientName);
      }

  この実装のポイント
    * 親画面への参照は、グローバル変数 `window` に `opener` として登録されている。
    * `window.opener` を介して親画面の関数を呼び出し、ポップアップ画面からの入力値を反映する。

  .. tip::

    親画面からポップアップ画面を参照することも可能である。
    詳細は :ref:`オープンしたウィンドウへのアクセス方法<tag-submit_access_open_window>` を参照。

ポップアップ画面の解説は以上。

:ref:`Getting Started TOPページへ <getting_started>`