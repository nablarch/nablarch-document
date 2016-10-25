リソース(アクション)クラスの実装に関して
==================================================


.. _rest_feature_details-method_signature:

リソースクラスのメソッドのシグネチャ
--------------------------------------------------
リソースクラスのメソッドの引数及び戻り値で利用できる型について示す。

メソッド引数
  .. list-table::
    :header-rows: 1
    :class: white-space-normal
    :widths: 30 70

    * - 引数定義
      - 説明

    * - 引数無し
      - パラメータやリクエストボディを必要としない場合には、引数無しとしてメソッドを定義できる。

        例
          .. code-block:: java

            public HttpResponse sample() {
              // 省略
            }

    * - フォーム(Java Beans)
      - リクエストボディから変換したフォームを元に処理を行う場合には、引数としてフォームを定義する。
      
        例
          .. code-block:: java

            public HttpResponse sample(SampleForm form) {
              // 省略
            }

    * - :java:extdoc:`HttpRequest <nablarch.fw.web.HttpRequest>`
      - :ref:`パスパラメータ <rest_feature_details-path_param>` や :ref:`クエリパラメータ <rest_feature_details-query_param>`
        を使う場合やHTTPヘッダの値などを取得したい場合には、引数として :java:extdoc:`HttpRequest <nablarch.fw.web.HttpRequest>` を定義する。

        例
          .. code-block:: java

            public HttpResponse sample(HttpRequest request) {
              // 省略
            }

    * - :java:extdoc:`ExecutionContext <nablarch.fw.ExecutionContext>`
      - :java:extdoc:`ExecutionContext <nablarch.fw.ExecutionContext>` が提供するスコープ変数にアクセスしたい場合は、
        引数として :java:extdoc:`ExecutionContext <nablarch.fw.ExecutionContext>` を定義する。
        
        例
          .. code-block:: java

            public HttpResponse sample(ExecutionContext context) {
              // 省略
            }

    * - 組み合わせ
      - 用途に応じて上記の型を組み合わせることが出来る。
        
        例えば、HTTPヘッダ情報とリクエストボディから変換されたFormを必要とするメソッドでは、以下の定義となる。

        .. code-block:: java

          public HttpResponse sample(SampleForm form, HttpRequest request) {
            // 省略
          }

メソッド戻り値
  .. list-table::
    :header-rows: 1
    :class: white-space-normal
    :widths: 30 70

    * - 戻り値の型
      - 説明

    * - void
      - レスポンスのボディが空であることを示す ``204: NoContent`` をクライアントに返却する。

    * - フォーム(Java Beans)
      - メソッドから戻されたフォームを :ref:`body_convert_handler` で、レスポンスボディに出力する内容に変換しクライアントに返却する。

    * - :java:extdoc:`HttpResponse <nablarch.fw.web.HttpResponse>`
      - メソッドから戻された :java:extdoc:`HttpResponse <nablarch.fw.web.HttpResponse>` の情報を、クライアントに返却する。



.. _rest_feature_details-path_param:

パスパラメータを扱う
--------------------------------------------------
検索や更新、削除対象のリソースを示す値をパスパラメータとして指定する場合の実装方法を示す。

URLの例
  ``GET /users/123`` の ``123`` をパスパラメータとする。

ルーティングの設定
  URLとアクションとのマッピング時にパスパラメータ部に任意の名前を設定する。
  この例では、 ``id`` という名前を設定し、数値のみを許容する設定としている。
  
  詳細は、 :ref:`router_adaptor` を参照。

  .. code-block:: xml

    <routes>
      <get path="users/:id" to="UsersResource#find">
        <requirements>
          <requirement name="id" value="\d+$" />
        </requirements>
      </delete>
    </routes>

リソースクラスのメソッドの実装
  パスパラメータは、 :java:extdoc:`HttpRequest <nablarch.fw.web.HttpRequest>` から取得する。
  このため、リソースのメソッドには、仮引数として :java:extdoc:`HttpRequest <nablarch.fw.web.HttpRequest>` を定義する。

  :java:extdoc:`HttpRequest <nablarch.fw.web.HttpRequest>` に指定するパラメータ名には、
  ルーティングの設定で指定したパスパラメータの名前を使用する。

  .. code-block:: java

    @Produces(MediaType.APPLICATION_JSON)
    public User delete(HttpRequest req) {
      // HttpRequestからパスパラメータの値を取得する
      Long id = Long.valueOf(req.getParam("id")[0]);
      return UniversalDao.findById(User.class, id);
    }

.. important::
  JSRで規定されている :java:extdoc:`PathParam <javax.ws.rs.PathParam>` は使用できないので注意すること。

.. _rest_feature_details-query_param:

クエリーパラメータを扱う
--------------------------------------------------
リソースの検索処理で、検索条件をクエリーパラメータとして指定させたい場合がある。
このような場合の実装方法を以下に示す。

URLの例
  ``GET /users/search?name=Duke``

ルーティングの設定
  ルーティングの設定では、クエリーパラメータを除いたパスを元に、リソースクラスとのマッピングを行う。

  .. code-block:: xml

    <routes>
      <get path="users/search" to="Users#search"/>
    </routes>

リソースクラスのメソッドの実装
  クエリーパラメータは、 :java:extdoc:`HttpRequest <nablarch.fw.web.HttpRequest>` から取得する。
  このため、リソースのメソッドには、仮引数として :java:extdoc:`HttpRequest <nablarch.fw.web.HttpRequest>` を定義する。

  :java:extdoc:`HttpRequest <nablarch.fw.web.HttpRequest>` から取得したパラメータを :java:extdoc:`BeanUtil <nablarch.core.beans.BeanUtil>` を使ってFormクラスにマッピングする。

  .. code-block:: java

    public HttpResponse search(HttpRequest req) {

      // リクエストパラメータをBeanに変換
      UserSearchForm form = BeanUtil.createAndCopy(UserSearchForm.class, req.getParamMap());

      // バリデーションの実行
      ValidatorUtil.validate(form)

      // 業務ロジックを実行する(省略)
    }

    // クエリーパラメータをマッピングするForm
    public UserSearchForm {
      private String name;
      // 省略
    }

.. important::
  JSRで規定されている :java:extdoc:`QueryParam <javax.ws.rs.QueryParam>` は使用できないので注意すること。
