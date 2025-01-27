.. _`session_store`:

セッションストア
=====================================================================

.. contents:: 目次
  :depth: 3
  :local:

HTTPセッションを抽象化した機能を提供する。

本機能では、セッションを識別するためにセッションIDを発行し、
クッキー( ``NABLARCH_SID`` (変更可))を使用して、セッションを追跡する。
そして、セッションIDごとにセッションストアと呼ばれる保存先へ読み書きする機能を提供する。

本機能では、セッションIDごとにセッションストアに読み書きされる値をセッション変数と呼ぶ。

簡単な処理の流れを以下の図に示す。

.. image:: images/session_store/session_store.png

1. :ref:`session_store_handler` の往路処理で、クッキーから取得したセッションIDをもとに、セッションストアからセッション変数をロードする。
2. 業務アクションから :java:extdoc:`SessionUtil <nablarch.common.web.session.SessionUtil>` を通して、セッション変数に対して読み書きする。
3. :ref:`session_store_handler` の復路処理で、セッション変数をセッションストアに保存する。
4. JSPで参照できるように、セッション変数をリクエストスコープに設定する。(既にリクエストスコープに同名の値が存在する場合は設定しない。)

.. important::
  本機能を使用する場合、以下の機能は用途が重複するため非推奨となる。

  * :ref:`hidden暗号化<tag-hidden_encryption>`
  * :ref:`session_concurrent_access_handler`
  * :java:extdoc:`ExecutionContext<nablarch.fw.ExecutionContext>` のセッションスコープにアクセスするAPI

.. tip::
 本機能で使用するクッキー( ``NABLARCH_SID`` )は、HTTPセッションの追跡に使用されるJSESSIONIDとは全く別物である。

.. tip::
 Nablarch 5u16より、セッションストアの有効期間保存先にHTTPセッション以外も選べるようになった。

.. tip::
 クッキーで使用するセッションIDには、:java:extdoc:`UUID<java.util.UUID>` を使用している。

機能概要
---------------------------------------------------------------------

セッション変数の保存先を選択できる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
セッション変数の保存先を、用途に応じて選択できる。

標準では以下の3種類のストアを提供している。

* :ref:`DBストア <session_store-db_store>`
* :ref:`HIDDENストア <session_store-hidden_store>`
* :ref:`HTTPセッションストア <session_store-http_session_store>`

セッションストアの特長や選択基準については、 :ref:`session_store-future_of_store` を参照。

また、 :ref:`redisstore_lettuce_adaptor` を使用することで、Redisを保存先として使用できる。


.. _session_store-serialize:

セッション変数の直列化の仕組みを選択できる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
セッション変数をセッションストアに保存する際の直列化の仕組みを以下から選択できる。
各機能の詳細はリンク先のJavadocを参照。

* :java:extdoc:`Java標準のシリアライズによる直列化(デフォルト) <nablarch.common.web.session.encoder.JavaSerializeStateEncoder>`
* :java:extdoc:`Java標準のシリアライズによる直列化、および暗号化 <nablarch.common.web.session.encoder.JavaSerializeEncryptStateEncoder>`
* :java:extdoc:`Jakarta XML BindingによるXMLベースの直列化 <nablarch.common.web.session.encoder.JaxbStateEncoder>`

モジュール一覧
---------------------------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

  <!-- DBストアを使用する場合のみ -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web-dbstore</artifactId>
  </dependency>

.. _session_store-constraint:

制約
---------------------------------------------------------------------
保存対象はシリアライズ可能なJava Beansオブジェクトであること
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
セッションストアに保存するオブジェクトはシリアライズ可能なJava Beansオブジェクトである必要がある。

オブジェクトが持つプロパティの型は、Javaの基本型もしくはシリアライズ可能なJava Beansオブジェクトである必要がある。
また、プロパティには配列やコレクションを使用できる。

使用方法
---------------------------------------------------------------------

.. _session_store-use_config:

セッションストアを使用するための設定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
セッションストアを使用するためには、 :ref:`session_store_handler` の設定に加えて、
:java:extdoc:`SessionManager <nablarch.common.web.session.SessionManager>` をコンポーネント定義に設定する。

以下に、標準で提供している全ての保存先を使用する場合の設定例を示す。

.. code-block:: xml

  <!-- "sessionManager"というコンポーネント名で設定する -->
  <component name="sessionManager" class="nablarch.common.web.session.SessionManager">

    <!--
      保存先を明示的に指定しなかった場合にデフォルトで使用されるストア名
    -->
    <property name="defaultStoreName" value="db"/>

    <!-- アプリケーションで使用する保存先に合わせてコンポーネントを追加する -->
    <property name="availableStores">
      <list>
        <!-- HIDDENストア -->
        <component class="nablarch.common.web.session.store.HiddenStore">
          <!-- 設定値の詳細はJavadocを参照 -->
        </component>

        <!-- DBストア -->
        <component-ref name="dbStore" />

        <!-- HTTPセッションストア -->
        <component class="nablarch.common.web.session.store.HttpSessionStore">
          <!-- 設定値の詳細はJavadocを参照 -->
        </component>
      </list>
    </property>
  </component>

  <component name="dbStore" class="nablarch.common.web.session.store.DbStore">
    <!-- 設定値の詳細はJavadocを参照 -->
  </component>

  <!-- DBストアの初期化設定 -->
  <component name="initializer"
      class="nablarch.core.repository.initialization.BasicApplicationInitializer">
    <property name="initializeList">
      <list>
        <!-- 他のコンポーネントは省略 -->
        <component-ref name="dbStore" />
      </list>
    </property>
  </component>

なお、DBストアを使用する場合、データベース上にセッション変数を保存するためのテーブルを作成する必要がある。

作成するテーブルの定義を以下に示す。

`USER_SESSION` テーブル
  ==================== ====================
  カラム名             データ型
  ==================== ====================
  SESSION_ID(PK)       `java.lang.String`
  SESSION_OBJECT       `byte[]`
  EXPIRATION_DATETIME  `java.sql.Timestamp`
  ==================== ====================

Oracleで正常に動作しないケースがあるため、 `SESSION_ID` はCHARではなくVARCHARで定義すること。

テーブル名およびカラム名は変更可能である。
変更する場合は、 :java:extdoc:`DbStore.userSessionSchema <nablarch.common.web.session.store.DbStore.setUserSessionSchema(nablarch.common.web.session.store.UserSessionSchema)>` に
:java:extdoc:`UserSessionSchema <nablarch.common.web.session.store.UserSessionSchema>` のコンポーネントを定義する。

.. code-block:: xml

  <property name="userSessionSchema">
    <component class="nablarch.common.web.session.store.UserSessionSchema">
      <!-- 設定値の詳細はJavadocを参照 -->
    </component>
  </property>

.. tip::
  DBストアを使用した場合、ブラウザが閉じられた場合などにテーブル上にセッション情報が残ってしまうことがある。
  そのため、期限切れのセッション情報は定期的に削除する必要がある。

.. _`session_store-input_data`:

入力～確認～完了画面間で入力情報を保持する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
入力～確認～完了画面間で入力情報を保持する場合、
複数タブでの画面操作を許容するか否かでセッションストアを使い分ける。

複数タブでの画面操作を許容しない場合
  DBストアを使用してデータベース上のテーブルにセッション変数を保持する。

複数タブでの画面操作を許容する場合
  HIDDENストアを使用してクライアントサイドにセッション変数を保持する。

  HIDDENストアを使用する場合、以下の様に入力・確認画面のJSPに :ref:`tag-hidden_store_tag` を使用する。

  .. code-block:: jsp

    <n:form>
      <!--
        name属性にはコンポーネント設定ファイルに定義した、
        HiddenStoreのparameterNameプロパティの値を設定
      -->
      <n:hiddenStore name="nablarch_hiddenStore" />
      <!-- その他のタグは省略 -->
    </n:form>

入力～確認～完了画面間でのセッションストアの実装例を以下に示す。

.. toctree::
  :maxdepth: 2

  session_store/create_example

.. toctree::
  :maxdepth: 2

  session_store/update_example

.. _`session_store-form`:

.. tip::
  セッションストアには、Formではなく、業務ロジックを実行するためのオブジェクト(Entity)を格納すること。

  Entityを格納することで、セッションストアから取り出したオブジェクトを使って、すぐに業務ロジックを実行できる。
  これにより、余計な処理が業務ロジックに混入することを防ぎ、ソースの凝集性が高まることが期待できる。

  反対に、Formを格納すると、Formによるデータの受け渡しを誘発し、業務ロジックに不要なデータの変換処理等が入り込み、
  密結合なソースが生まれる可能性が高まる。

  また、Formは外部の入力値を受け付けるため、バリデーション済みであればよいが、バリデーション前であれば信頼できない値を保持した状態となる。
  そのため、セキュリティの観点から、セッションストアに保持するデータは生存期間が長くなるので、
  できるだけ安全なデータを保持しておき、脆弱性を埋め込むリスクを減らすという狙いもある。

.. _`session_store-authentication_data`:

認証情報を保持する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

認証情報を保持する場合は、DBストアを使用する。

ログイン、ログアウト時のセッションストアの実装例を以下に示す。

アプリケーションにログインする
  .. code-block:: java

    // ログイン前にセッションIDを変更する
    SessionUtil.changeId(ctx);

    // CSRFトークンを再生成する（CSRFトークン検証ハンドラを使用している場合）
    CsrfTokenUtil.regenerateCsrfToken(ctx);

    // ログインユーザの情報をセッションストアに保存
    SessionUtil.put(ctx, "user", user, "db");

.. important::
  以下の条件を全て満たす場合、ログインのときにCSRFトークンの再生成が必要になる。

  * :ref:`csrf_token_verification_handler` を使用している
  * ログイン時にセッションIDの変更のみを行う（セッション情報は維持する）

  詳しくは :ref:`csrf_token_verification_handler-regeneration` を参照。

アプリケーションからログアウトする
  .. code-block:: java

    // セッションストア全体を破棄
    SessionUtil.invalidate(ctx);

JSPからセッション変数の値を参照する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
通常のリクエストスコープやセッションスコープと同様の手順で、
JSPからセッションストアで保持しているセッション変数の値を参照できる。

.. important::
  ただし、既にリクエストスコープ上に同名の値が存在する場合は、JSPからセッション変数の値を参照できないため、
  セッション変数にはリクエストスコープと重複しない名前を設定すること。

HIDDENストアの暗号化設定をカスタマイズする
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:ref:`HIDDENストア <session_store-hidden_store>` の暗号化/復号設定のデフォルトは、以下の通りである。

======================= ============================================================
設定項目                設定内容
======================= ============================================================
暗号化アルゴリズム      `AES`
暗号化キー              アプリケーションサーバ内で共通の自動生成されたキーを使用
======================= ============================================================

アプリケーションサーバが冗長化されている場合、アプリケーションサーバごとに異なるキーを生成するため、復号に失敗してしまうケースがある。
このケースでは、明示的に暗号化/復号のキーを設定する。

暗号化アルゴリズムに `AES` を使用し、暗号化/復号のキーを明示的に設定する設定例を以下に示す。

.. code-block:: xml

  <component class="nablarch.common.web.session.store.HiddenStore">
    <!-- 他の設定値は省略 -->
    <property name="encryptor">
      <component class="nablarch.common.encryption.AesEncryptor">
        <property name="base64Key">
          <component class="nablarch.common.encryption.Base64Key">
            <property name="key" value="OwYMOWbnLyYy93P8oIayeg==" />
            <property name="iv" value="NOj5OUN+GlyGYTc6FM0+nw==" />
          </component>
        </property>
      </component>
    </property>
  </component>
  
ポイント
  暗号化の鍵及びIVは、base64でエンコードした値を設定する。
  鍵の強度を高めるためには、以下の機能を使用して生成すると良い。
  
  * :java:extdoc:`KeyGenerator <javax.crypto.KeyGenerator>` を使用して鍵を生成する。
  * :java:extdoc:`SecureRandom <java.security.SecureRandom>` を使用してIVを生成する。
  
  なお、base64エンコードは :java:extdoc:`java.util.Base64.getEncoder()` より取得できる :java:extdoc:`java.util.Base64.Encoder` を使用して行うと良い。

セッション変数に値が存在しない場合の遷移先画面を指定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
正常な画面遷移では必ずセッション変数が存在しているが、ブラウザの戻るボタンを使用され不正な画面遷移が行われることで、
本来存在しているはずのセッション変数にアクセスできない場合がある。
この場合、セッション変数が存在しないことを示す例外( :java:extdoc:`SessionKeyNotFoundException <nablarch.common.web.session.SessionKeyNotFoundException>` )が送出されるので、
この例外を補足することで任意のエラーページに遷移させることが出来る。

以下に実現方法を示す。

システムで共通のエラーページに遷移させる
  システムで共通のエラーページに遷移させる場合は、ハンドラで例外を捕捉し遷移先を指定する。
  
  実装例
    .. code-block:: java

      public class SampleErrorHandler implements Handler<Object, Object> {

        @Override
        public Object handle(Object data, ExecutionContext context) {

          try {
            return context.handleNext(data);
          } catch (SessionKeyNotFoundException e) {
            // セッション変数が存在しないことを示す例外を捕捉し、
            // 不正な画面遷移を表すエラーページを返す
            throw new HttpErrorResponse(HttpResponse.Status.BAD_REQUEST.getStatusCode(),
                    "/WEB-INF/view/errors/BadTransition.jsp", e);
          }
        }
      }


リクエスト毎に遷移先を指定する
  リクエスト毎に遷移先を切り替える場合には、 :ref:`on_error_interceptor` を使用して遷移先を指定する。
  なお、上記のシステムで共通のエラーページに遷移させると併用することで、一部のリクエストのみ遷移先を変更することも出来る。

  実装例
    .. code-block:: java

      // 対象例外にセッション変数が存在しないことを示す例外を指定して、リクエスト毎の遷移先を指定する
      @OnError(type = SessionKeyNotFoundException.class, path = "redirect://error")
      public HttpResponse backToNew(HttpRequest request, ExecutionContext context) {
        Project project = SessionUtil.get(context, "project");
        // 処理は省略
      }


拡張例
---------------------------------------------------------------------

セッション変数の保存先を追加する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
セッション変数の保存先を追加するには以下の手順が必要となる。

#. :java:extdoc:`SessionStore <nablarch.common.web.session.SessionStore>` を継承し、追加したい保存先に対応したクラスを作成する。
#. :java:extdoc:`SessionManager.availableStores <nablarch.common.web.session.SessionManager.setAvailableStores(java.util.List)>` に、作成したクラスのコンポーネント定義を追加する。

.. _session_store-future_of_store:

セッションストアの特長と選択基準
---------------------------------------------------------------------
デフォルトで使用できるセッション変数の保存先は以下の通り。

.. _`session_store-db_store`:

DBストア
  :保存先: | データベース上のテーブル

  :特徴: * ローリングメンテナンス等でアプリケーションサーバが停止した場合でもセッション変数の復元が可能。
          * アプリケーションサーバのヒープ領域を圧迫しない。
          * 同一セッションの処理が複数スレッドで実行された場合後勝ちとなる。(先に保存されたセッションのデータは消失する)


.. _`session_store-hidden_store`:

HIDDENストア
  :保存先: | クライアントサイド
            | ( `hidden` タグを使用して画面間でセッション変数を引き回して実現)

  :特徴: * 複数タブでの画面操作を許容できる。
          * アプリケーションサーバのヒープ領域を圧迫しない。
          * 同一セッションの処理が複数スレッドで実行された場合、セッションのデータはそれぞれのスレッドに紐付けて保存される。

.. _`session_store-http_session_store`:

HTTPセッションストア
  :保存先: | アプリケーションサーバのヒープ領域
            | (アプリケーションサーバの設定によっては、データベースやファイル等に保存される場合がある。)

  :特徴: * 認証情報の様なアプリケーション全体で頻繁に使用する情報の保持に適している。
          * APサーバ毎に情報を保持するため、スケールアウトを行う際に工夫が必要となる。
          * 画面の入力内容の様な大量データを保存すると、ヒープ領域を圧迫する恐れがある。
          * 同一セッションの処理が複数スレッドで実行された場合後勝ちとなる。(先に保存されたセッションのデータは消失する)

            

上記を踏まえ、各セッションストアの選択基準を以下に示す。

======================================================================== ===============================================================
用途                                                                     セッションストア
======================================================================== ===============================================================
入力～確認～完了画面間で入力情報の保持(複数タブでの画面操作を許容しない) :ref:`DBストア <session_store-db_store>`
入力～確認～完了画面間で入力情報の保持(複数タブでの画面操作を許容する)   :ref:`HIDDENストア <session_store-hidden_store>`
認証情報の保持                                                           :ref:`DBストア <session_store-db_store>` または :ref:`HTTPセッションストア <session_store-http_session_store>`
検索条件の保持                                                           使用しない [1]_
検索結果一覧の保持                                                       使用しない [2]_
セレクトボックス等の画面表示項目の保持                                   使用しない [3]_
エラーメッセージの保持                                                   使用しない [3]_
======================================================================== ===============================================================

.. [1] 認証情報を除き、セッションストアでは複数機能に跨るデータの保持は想定していない。
       ブラウザのローカルストレージに検索時のURLを保持するなど、アプリケーションの要件に合わせて設計・実装すること。
.. [2] 一覧情報のような大量データは保存領域を圧迫する可能性があるのでセッションストアには保存しない。
.. [3] 画面表示に使用する値はリクエストスコープを使用して受け渡せばよい。

.. tip::
  :ref:`redisstore_lettuce_adaptor` については、保存先が異なるだけで特徴はDBストアと同じになる。

.. _`session_store_expiration`:
       
有効期間の管理方法
------------------

セッションの有効期間はデフォルトではHTTPセッションに保存されている。
設定を変更することで有効期間の保存先をデータベースに変更できる。

詳細は :ref:`db_managed_expiration` を参照。

また、 :ref:`redisstore_lettuce_adaptor` を使用した場合は有効期限をRedisに保存できる。

.. tip::
  有効期間をデータベースに保存する意義については :ref:`stateless_web_app` 参照。


