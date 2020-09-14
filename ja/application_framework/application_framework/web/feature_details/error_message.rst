バリデーションエラーのメッセージを画面表示する
==================================================
サーバサイドで行ったバリデーションのエラーメッセージは、 :ref:`http_error_handler` でリクエストスコープに格納される。
テンプレートエンジンでは、リクエストスコープに格納された :java:extdoc:`ErrorMessages <nablarch.fw.web.message.ErrorMessages>` にアクセスすることでエラーメッセージを表示できる。
リクエストスコープの変数名は、:ref:`エラーメッセージのリクエストスコープへの設定 <http_error_handler-error_messages>` を参照。

.. tip::

  JSPを使用した場合、 :ref:`カスタムタグを使用したエラー表示 <tag-write_error>` を使用することでエラーメッセージの表示ができるが、
  カスタムタグが出力するDOM構造の制約によりCSSフレームワークとの相性が悪い問題がある。

  リクエストスコープ上のオブジェクトを使用した場合、DOM構造の制約がなくなるためJSPでも直接リクエストスコープ上のオブジェクトにアクセスしエラーメッセージを表示しても良い。
  

以下に :ref:`Thymeleaf <web_thymeleaf_adaptor>` を使った場合の実装例を示す。

特定のプロパティに対応したメッセージを表示したい
  :java:extdoc:`ErrorMessages#hasError <nablarch.fw.web.message.ErrorMessages.hasError(java.lang.String)>` や
  :java:extdoc:`ErrorMessages#getMessage <nablarch.fw.web.message.ErrorMessages.getMessage(java.lang.String)>`
  を使用することでプロパティ(入力項目のname属性の値)に対応したエラー有無やメッセージの表示ができる。

  この例では、 ``form.userName`` プロパティに対応したエラーメッセージがリクエストスコープにある場合にメッセージが表示される。

  .. code-block:: html

    <input type='text' name='form.txt' />
    <span class="error" th:if="${errors.hasError('form.userName')}"
        th:text="${errors.getMessage('form.userName')}">入力してください。</span>

グローバルメッセージ(プロパティに紐付かないメッセージ)を表示したい
  :java:extdoc:`ErrorMessages#getGlobalMessages() <nablarch.fw.web.message.ErrorMessages.getGlobalMessages()>` を使用して
  グローバルメッセージが表示できる。

  .. code-block:: html

    <ul>
      <li th:each="message : ${errors.globalMessages}" th:text="${message}"></li>
    </ul>

全てのメッセージを表示したい
  :java:extdoc:`ErrorMessages#getAllMessages() <nablarch.fw.web.message.ErrorMessages.getAllMessages()>` を使用して
  全てのメッセージが表示できる。
  
  .. code-block:: html

    <ul>
      <li th:each="message : ${errors.allMessages}" th:text="${message}">エラーメッセージ</li>
    </ul>

