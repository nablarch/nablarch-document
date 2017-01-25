.. _`getting_started_http_massaging-save`:

登録機能の作成
==========================================================
リクエストされた情報(JSON形式)をDBに登録する機能の解説を行う。

作成する機能の概要
  .. image:: ../images/overview.png

動作確認手順
  1. 事前にDBの状態を確認

     H2のコンソールから下記SQLを実行し、レコードが存在しないことを確認する。

     .. code-block:: sql

       SELECT * FROM PROJECT WHERE PROJECT_NAME = 'プロジェクト９９９';

  2. プロジェクト情報の登録

    任意のRESTクライアントを使用して、以下のリクエストを送信する。

    URL
      http://localhost:9080/ProjectSaveAction
    HTTPメソッド
      POST
    HTTPヘッダ
      Content-Type: application/json |br|
      X-Message-Id: 1
    リクエストボディ
      .. code-block:: json

        {
            "projectName": "プロジェクト９９９",
            "projectType": "development",
            "projectClass": "ss",
            "projectManager": "山田",
            "projectLeader": "田中",
            "clientId": 10,
            "projectStartDate": "20160101",
            "projectEndDate": "20161231",
            "note": "備考９９９",
            "sales": 10000,
            "costOfGoodsSold": 20000,
            "sga": 30000,
            "allocationOfCorpExpenses": 40000
        }

  3. 動作確認

    H2のコンソールから下記SQLを実行し、レコードが1件取得できることを確認する。

    .. code-block:: sql

      SELECT * FROM PROJECT WHERE PROJECT_NAME = 'プロジェクト９９９';

登録を行う
----------------------

#. :ref:`フォーマットファイルの作成<getting_started_http_messaging-format>`
#. :ref:`フォームの作成<getting_started_http_messaging-form>`
#. :ref:`業務アクションの作成<getting_started_http_messaging-action>`

.. _`getting_started_http_messaging-format`:

フォーマットファイルの作成
  HTTPメッセージングでは、リクエストされたHTTPメッセージを :ref:`data_format` を使用して解析する。

  ProjectSaveAction_RECEIVE.fmt
    .. code-block:: bash

      file-type:        "JSON"
      text-encoding:    "UTF-8"

      [project]
      1  projectName                       N
      2  projectType                       N
      3  projectClass                      N
      4  projectStartDate[0..1]            N
      5  projectEndDate[0..1]              N
      6  clientId                          X9
      7  projectManager[0..1]              N
      8  projectLeader[0..1]               N
      9  note[0..1]                        N
      10 sales[0..1]                       X9
      11 costOfGoodsSold[0..1]             X9
      12 sga[0..1]                         X9
      13 allocationOfCorpExpenses[0..1]    X9
      14 userId[0..1]                      X9

  この実装のポイント
    * フォーマットファイルの名称は、「リクエストID + "_RECEIVE"」という形式にする。
    * フォーマットファイルの記述方法は :ref:`data_format-definition` を参照。

.. _`getting_started_http_messaging-form`:

フォームの作成
  リクエストボディの内容をバインドするフォームを作成する。

  ProjectForm.java
    .. code-block:: java

      public class ProjectForm {

          // 一部項目のみ抜粋

          /** プロジェクト名 */
          @Required
          @Domain("projectName")
          private String projectName;

          /**
           * プロジェクト名を取得する。
           *
           * @return プロジェクト名
           */
          public String getProjectName() {
              return projectName;
          }

          /**
           * プロジェクト名を設定する。
           *
           * @param projectName 設定するプロジェクト名
           *
           */
          public void setProjectName(String projectName) {
              this.projectName = projectName;
          }
      }

  この実装のポイント
    * :ref:`bean_validation` を用いてバリデーションを行うため、バリデーション用のアノテーションを設定する。

.. _`getting_started_http_messaging-action`:

業務アクションの作成
  プロジェクトをDBに登録する業務アクションを作成する。

  ProjectSaveAction.java
    .. code-block:: java

      public class ProjectSaveAction extends MessagingAction {

          /**
           * 電文を受信した際に実行される業務処理。
           * <p>
           * プロジェクト情報をバリデーションし、DBに登録する。
           * このメソッドは、一つのプロジェクトを登録するための処理である。
           * (汎用フォーマットによる形式チェックにより単独プロジェクトであることが保証される)
           * </p>
           * 登録が完了した場合は、レスポンスコードを記載した応答電文を設定する。
           * 例外が発生した場合は、{@link ProjectSaveAction#onError(Throwable, RequestMessage, ExecutionContext)}
           * にて応答電文を設定する。
           * 
           * @param requestMessage   受信したメッセージ
           * @param executionContext 実行コンテキスト
           * @return 応答電文
           */
          @Override
          protected ResponseMessage onReceive(RequestMessage requestMessage,
                                              ExecutionContext executionContext) {

              // 入力値をフォームにバインドする
              ProjectForm form = BeanUtil.createAndCopy(ProjectForm.class,
                      requestMessage.getParamMap());

              // バリデーションエラーがある場合は業務例外を送出
              ValidatorUtil.validate(form);

              UniversalDao.insert(BeanUtil.createAndCopy(Project.class, form));

              // 応答電文のフォーマッタを作成する
              requestMessage.setFormatterOfReply(createFormatter());

              // 応答電文に記載するステータスコードを設定する
              Map<String, String> map = new HashMap<>();
              map.put("statusCode", String.valueOf(HttpResponse.Status.CREATED.getStatusCode()));

              // 応答データ返却
              return requestMessage.reply()
                     .setStatusCodeHeader(String.valueOf(HttpResponse.Status.CREATED.getStatusCode()))
                     .addRecord("data", map);
          }
      }


  この実装のポイント
    * :java:extdoc:`MessagingAction <nablarch.fw.messaging.action.MessagingAction>` を継承し、業務メソッドを作成する。
    * :java:extdoc:`MessagingAction#onReceive <nablarch.fw.messaging.action.MessagingAction.onReceive(nablarch.fw.messaging.RequestMessage, nablarch.fw.ExecutionContext)>`
      に、リクエスト受信時に実行する処理を実装する。
    * リクエストボディの値は、 :ref:`data_format` を使用して解析された状態で引数の :java:extdoc:`RequestMessage <nablarch.fw.messaging.RequestMessage>` オブジェクト
      が保持している。 `getParamMap` メソッドを使用してリクエストボディの値を取得する。
    * :ref:`bean_validation` を使用してリクエスト値のバリデーションを行う。
    * :java:extdoc:`UniversalDao <nablarch.common.dao.UniversalDao>` を用いてプロジェクトをDBに登録する。
    * 処理結果を表すレスポンスコードを :java:extdoc:`ResponseMessage <nablarch.fw.messaging.RequestMessage>` に設定して返却する。

  .. tip::
    業務例外が送出された場合は、 :ref:`http_messaging_error_handler` の処理によってレスポンスコード「400」が設定される。

.. |br| raw:: html

  <br />