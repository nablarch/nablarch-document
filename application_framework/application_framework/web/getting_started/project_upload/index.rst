.. _`project_upload`:

アップロードを用いた一括登録機能の作成
==========================================
Exampleアプリケーションを元に、CSVファイルをアップロードして一括登録する機能の解説を行う。

作成する機能の説明
  1. ヘッダメニューの「プロジェクト一括登録」を押下する。

    .. image:: ../images/project_upload/project_upload-link.png
      :scale: 80

  2. バリデーションエラーが発生する一括登録サンプルファイルを、下記からダウンロードする。

     :download:`プロジェクト一括登録_バリデーションエラー.csv<../downloads/project_upload/プロジェクト一括登録_バリデーションエラー.csv>`

  3. サンプルファイルをアップロードし、登録ボタンを押下する。

    .. image:: ../images/project_upload/project_upload-invalid_upload.png
      :scale: 80

  3. バリデーションエラーが発生する。

    .. image:: ../images/project_upload/project_upload-validate.png
      :scale: 80

  4. バリデーションエラーが発生しない一括登録サンプルファイルを、下記からダウンロードする。

    :download:`プロジェクト一括登録.csv<../downloads/project_upload/プロジェクト一括登録.csv>`

  5. サンプルファイルをアップロードし、登録ボタンを押下する。

    .. image:: ../images/project_upload/project_upload-valid_upload.png
      :scale: 80

  6. ファイルの内容がデータベースに登録され、完了メッセージが表示される。

    .. image:: ../images/project_upload/project_upload-complete.png
      :scale: 80

作成する業務アクションメソッドの全体像
-----------------------------------------------------

    ProjectUploadAction.java
      .. code-block:: java

        @OnDoubleSubmission
        @OnError(type = ApplicationException.class, path = "/WEB-INF/view/projectUpload/create.jsp")
        public HttpResponse upload(HttpRequest request, ExecutionContext context) {

            // アップロードファイルの取得
            List<PartInfo> partInfoList = request.getPart("uploadFile");
            if (partInfoList.isEmpty()) {
                throw new ApplicationException(
                        MessageUtil.createMessage(MessageLevel.ERROR, "errors.upload"));
            }
            PartInfo partInfo = partInfoList.get(0);

            LoginUserPrincipal userContext = SessionUtil.get(context, "userContext");

            // アップロードファイルの読み込みとバリデーション
            List<Project> projects = readFileAndValidate(partInfo, userContext);

            // DBへ一括登録する
            insertProjects(projects);

            // 完了メッセージの追加
            WebUtil.notifyMessages(context, MessageUtil.createMessage(
                    MessageLevel.INFO, "success.upload.project", projects.size()));

            // ファイルの保存
            saveFile(partInfo);

            return new HttpResponse("/WEB-INF/view/projectUpload/create.jsp");
        }
  
  業務アクションメソッドの処理の流れは次のようになっている。
  
  #. :ref:`ファイルを取得する<project_upload-file_upload_action>`
  #. :ref:`CSVファイルの内容をBeanにバインドしてバリデーションする<project_upload-validation>`
  #. :ref:`DBへ一括登録する<project_upload-bulk_insert>`
  #. :ref:`ファイルを保存する<project_upload-file_upload_action>`
  
  それぞれの処理の詳細は次節以降の
  :ref:`ファイルアップロード機能の実装<project_upload-file_upload-impl>` と
  :ref:`一括登録機能の実装<project_upload-bulk_insert-impl>` で説明する。

.. _`project_upload-file_upload-impl`:

ファイルアップロード機能の実装
-----------------------------------------------------
まず、アップロードを用いた一括登録機能のうち、アップロード部分の作成方法に関して説明する。

  #. :ref:`ファイルアップロード画面の作成<project_upload-upload_jsp>`
  #. :ref:`ファイルの取得と保存を行う業務アクションメソッドの作成<project_upload-file_upload_action>`

  .. _`project_upload-upload_jsp`:

  ファイルアップロード画面の作成
    ファイルアップロード欄をもつ画面を作成する。

    /src/main/webapp/WEB-INF/view/projectUpload/create.jsp
      .. code-block:: jsp

        <n:form useToken="true" enctype="multipart/form-data">
            <!-- 省略 -->
            <div class="message-area margin-top">
                <!-- エラーメッセージ表示部分 -->
                <n:errors errorCss="message-error"/>
            </div>
            <!-- 省略 -->
            <h4 class="font-group">プロジェクト情報ファイル選択</h4>
            <table class="table">
                <!-- 画面デザインに関する記述は省略 -->
                <tbody>
                    <tr>
                        <th class="item-norequired" colspan="2">プロジェクト情報ファイル選択</th>
                    </tr>
                    <tr>
                        <th class="width-250 required">プロジェクト情報ファイル</th>
                        <td >
                            <div class="form-group is-fileinput">
                                <div class="input-group">
                                    <n:file name="uploadFile" id="uploadFile"/>
                                    <!-- 画面デザインに関する記述は省略 -->
                                </div>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
            <div class="title-nav">
                <div class="button-nav">
                    <n:button uri="/action/projectUpload/upload"
                              allowDoubleSubmission="false"
                              cssClass="btn btn-raised btn-default">登録</n:button>
                </div>
            </div>
        </n:form>

    この実装のポイント
      * マルチパートファイルを送信するため、 :ref:`tag-form_tag` の `enctype` 属性を `multipart/form-data` と指定する。
      * :ref:`tag-file_tag` を用いてファイルアップロード欄を作成する。 `name` 属性にはリクエストオブジェクトへの登録名を指定する。
        業務アクションでファイルを取得するには、 :java:extdoc:`HttpRequest#getPart<nablarch.fw.web.HttpRequest.getPart(java.lang.String)>`
        の引数にこの登録名を指定する。
      * :ref:`tag-errors_tag` を用いて、対象ファイルに対するバリデーションエラーメッセージを一覧表示する領域を作成する。
        エラーメッセージ一覧の出力形式については :ref:`エラーメッセージの一覧表示 <tag-write_error_errors_tag>` を参照。

  .. _`project_upload-file_upload_action`:

  業務アクションメソッドの作成
    業務アクションメソッドでの、ファイルの取得及び保存方法を説明する。

    ProjectUploadAction.java
      .. code-block:: java

        public HttpResponse upload(HttpRequest request, ExecutionContext context)
                throws IOException {

            List<PartInfo> partInfoList = request.getPart("uploadFile");
            if (partInfoList.isEmpty()) {
                throw new ApplicationException(MessageUtil.createMessage(MessageLevel.ERROR,
                         "errors.upload"));
            }
            PartInfo partInfo = partInfoList.get(0);

            // 一括登録処理は後述するので省略

            // ファイルの保存
            saveFile(partInfo);

            return new HttpResponse("/WEB-INF/view/projectUpload/create.jsp");
        }
        
        /**
         * ファイルを保存する。
         *
         * @param partInfo アップロードファイルの情報
         */
        private void saveFile(final PartInfo partInfo) {
            String fileName = generateUniqueFileName(partInfo.getFileName());
            UploadHelper helper = new UploadHelper(partInfo);
            helper.moveFileTo("uploadFiles", fileName);
        }

    この実装のポイント
      * :java:extdoc:`HttpRequest#getPart<nablarch.fw.web.HttpRequest.getPart(java.lang.String)>` を使用してファイルを取得する。
      * ファイルが存在しない(アップロードされていない)場合は、取得した :java:extdoc:`PartInfo<nablarch.fw.web.upload.PartInfo>` リストのサイズは0となる。
        この値を使用して業務例外を送出するなどの制御を行う。
      * アップロードされたファイルは :ref:`マルチパートリクエストハンドラ<multipart_handler>` によって一時領域に保存される。
        一時領域は自動で削除されるため、アップロードファイルを永続化（保存）する必要がある場合は、ファイルを任意のディレクトリへ移送する。
        ただし、ファイルの移送は :ref:`ファイルパス管理<file_path_management>` を使用してファイルやディレクトリの入出力を管理している場合のみ可能である。
      * ファイルの移送には :java:extdoc:`UploadHelper#moveFileTo<nablarch.fw.web.upload.util.UploadHelper.moveFileTo(java.lang.String, java.lang.String)>` メソッドを使用する。
        第一引数には、設定ファイルに登録されたファイル格納ディレクトリのキー名を指定する。
        Exampleアプリケーションでは下記ファイルに設定が記載されている。

        filepath-for-webui.xml
          .. code-block:: xml

            <!-- ファイルパス定義 -->
            <component name="filePathSetting"
                    class="nablarch.core.util.FilePathSetting" autowireType="None">
              <property name="basePathSettings">
                <map>
                  <!--省略 -->
                  <!--アップロードファイルの格納ディレクトリ-->
                  <entry key="uploadFiles" value="file:./work/input" />
                </map>
              </property>
              <!-- 省略 -->
            </component>

.. _`project_upload-bulk_insert-impl`:

一括登録機能の実装
----------------------------
アップロードを用いた一括登録機能のうち、一括登録部分の作成方法に関して説明する。

    #. :ref:`ファイルをバインドするBeanの作成<project_upload-create_bean>`
    #. :ref:`ファイルを一括登録する業務アクションメソッドの作成<project_upload-bulk_action>`

.. _`project_upload-create_bean`:

ファイルの内容をバインドするBeanの作成
  ファイルの内容をバインドするBeanを作成する。

  ProjectUploadDto.java
    .. code-block:: java

      @Csv(headers = { /** ヘッダーを記述 **/},
              properties = { /** バインド対象のプロパティ **/},
              type = Csv.CsvType.CUSTOM)
      @CsvFormat(charset = "Shift_JIS", fieldSeparator = ',',ignoreEmptyLine = true,
              lineSeparator = "\r\n", quote = '"',
              quoteMode = CsvDataBindConfig.QuoteMode.NORMAL, requiredHeader = true)
      public class ProjectUploadDto implements Serializable {

          // 一部項目のみ抜粋。ゲッタ及びセッタは省略

          /** プロジェクト名 */
          @Required(message = "{nablarch.core.validation.ee.Required.upload}")
          @Domain("projectName")
          private String projectName;

          /** プロジェクト種別 */
          @Required(message = "{nablarch.core.validation.ee.Required.upload}")
          @Domain("projectType")
          private String projectType;

          // 処理対象行の行数を保持するプロパティ。セッタは省略。
          /** 行数 */
          private Long lineNumber;

          /**
           * 行数を取得する。
           * @return 行数
           */
          @LineNumber
          public Long getLineNumber() {
              return lineNumber;
          }
      }

  この実装のポイント
    * アップロードされたCSVファイルの内容と、Beanのプロパティとの紐付けの設定は、 :java:extdoc:`@Csv<nablarch.common.databind.csv.Csv>` を使用する。
      受け付けるCSVのフォーマットの指定は、 :java:extdoc:`@CsvFormat<nablarch.common.databind.csv.CsvFormat>` を使用する。
      （ :ref:`デフォルトのフォーマットの指定<data_bind-csv_format_set>` を利用する場合は、 :java:extdoc:`@CsvFormat<nablarch.common.databind.csv.CsvFormat>` は不要）
      アノテーションの設定方法の詳細は、 :ref:`CSVファイルをJava Beansクラスにバインドする場合のフォーマット指定方法 <data_bind-csv_format-beans>` を参照。
    * プロパティに :java:extdoc:`@Required<nablarch.core.validation.ee.Required>` や :java:extdoc:`@Domain<nablarch.core.validation.ee.Domain>`
      などのバリデーション用のアノテーションを付与して :ref:`Bean Validation<bean_validation>` を行う。
    * ファイルからの入力値を受け付けるため、 :ref:`プロパティはString型で定義し<bean_validation-form_property>`、
      適切な型への変換はバリデーションを通過した安全な値に対して行う。
    * 行数プロパティを定義し、ゲッタに :java:extdoc:`LineNumber<nablarch.common.databind.LineNumber>` を付与することで、
      対象データが何行目のデータであるかを自動的に設定できる。

    .. tip::
      入力必須項目のバリデーションエラーメッセージを、ファイルアップロードに対するメッセージとして適切なものに変更している。
      バリデーションメッセージの指定方法については、 :ref:`入力値のチェックルールを設定する<client_create_validation_rule>` を参照。

.. _`project_upload-bulk_action`:

業務アクションメソッドの作成
  アップロードされたファイルの内容をデータベースに登録する業務アクションメソッドを作成する。

  .. _`project_upload-validation`:

  1.CSVファイルの内容をBeanにバインドしてバリデーションする
    ProjectUploadAction.java
      .. code-block:: java

        private List<Project> readFileAndValidate(final PartInfo partInfo, final LoginUserPrincipal userContext) {
            List<Message> messages = new ArrayList<>();
            List<Project> projects = new ArrayList<>();

            // ファイルの内容をBeanにバインドしてバリデーションする
            try (final ObjectMapper<ProjectUploadDto> mapper
                     = ObjectMapperFactory.create(
                            ProjectUploadDto.class, partInfo.getInputStream())) {
                ProjectUploadDto projectUploadDto;

                while ((projectUploadDto = mapper.read()) != null) {

                    // 検証して結果メッセージを設定する
                    messages.addAll(validate(projectUploadDto));

                    // エンティティを作成
                    projects.add(createProject(projectUploadDto, userContext.getUserId()));
                }
            } catch (InvalidDataFormatException e) {
                // ファイルフォーマットが不正な行がある場合はその時点で解析終了
                messages.add(
                    MessageUtil.createMessage(
                        MessageLevel.ERROR, "errors.upload.format", e.getLineNumber()));
            }

            // 一件でもエラーがある場合はデータベースに登録しない
            if (!messages.isEmpty()) {
                throw new ApplicationException(messages);
            }
            return projects;
        }
    
        /**
         * プロジェクト情報をバリデーションして、結果をメッセージリストに格納する。
         *
         * @param projectUploadDto CSVから生成したプロジェクト情報Bean
         * @return messages         バリデーション結果のメッセージのリスト
         */
        private List<Message> validate(final ProjectUploadDto projectUploadDto) {

            List<Message> messages = new ArrayList<>();

            // 単項目バリデーション。Dtoに定義したアノテーションを元にBean Validationを実行する
            try {
                ValidatorUtil.validate(projectUploadDto);
            } catch (ApplicationException e) {
                messages.addAll(e.getMessages()
                        .stream()
                        .map(message -> MessageUtil.createMessage(MessageLevel.ERROR,
                                "errors.upload.validate", projectUploadDto.getLineNumber(), message))
                        .collect(Collectors.toList()));
            }

            // 顧客存在チェック
            if (!existsClient(projectUploadDto)) {
                messages.add(MessageUtil.createMessage(MessageLevel.ERROR,
                        "errors.upload.client", projectUploadDto.getLineNumber()));
            }

            return messages;
        }

    この実装のポイント
      * ファイルをBeanにバインドして取得するには、 :ref:`データバインド<data_bind>` が提供する、
        :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` を使用する。
      * 取得した :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` オブジェクトに対して、
        :java:extdoc:`ObjectMapper#read <nablarch.common.databind.ObjectMapper.read()>` を実行することで、バインド済みBeanのリストを取得できる。
      * :java:extdoc:`ValidatorUtil#getValidator <nablarch.core.validation.ee.ValidatorUtil.getValidator()>` を使用して
        :java:extdoc:`Validator <javax.validation.Validator>` オブジェクトを生成することで、任意のBeanに対して :ref:`Bean Validation<bean_validation>` を実行することができる。
      * エラーが発生した時点でバリデーションを中止せず、最終行まで検証を行う場合、
        バリデーション終了後に全行分のエラーメッセージを格納した :java:extdoc:`Message<nablarch.core.message.Message>` のリスト
        を引数に :java:extdoc:`ApplicationException<nablarch.core.message.ApplicationException>` を生成して送出することで、
        :ref:`tag-errors_tag` で画面に出力できる。
      * バリデーションメッセージにプロパティ名を付与する方法については
        :ref:`バリデーションエラー時のメッセージに項目名を含めたい<bean_validation-property_name>` を参照し実装する。
    

  .. _`project_upload-bulk_insert`:

  2.DBへ一括登録する
    ProjectUploadAction.java
      .. code-block:: java

        public HttpResponse upload(HttpRequest request,ExecutionContext context)
                throws IOException {

            // バリデーションの実行は前述

            // DBへ一括登録する
            insertProjects(projects);

            // ファイル保存は前述
        }

        /**
         * 複数のプロジェクトエンティティを一括でデータベースに登録する。
         * @param projects 検証済みのプロジェクトリスト
         */
        private void insertProjects(List<Project> projects) {

          List<Project> insertProjects = new ArrayList<Project>();

          for (Project project : projects) {
              insertProjects.add(project);
              // 100件ごとにbatchInsertする
              if (insertProjects.size() >= 100) {
                  UniversalDao.batchInsert(insertProjects);
                  insertProjects.clear();
              }
          }

          if (!insertProjects.isEmpty()) {
              UniversalDao.batchInsert(insertProjects);
          }
        }

    この実装のポイント
      * 一括登録は、 :java:extdoc:`UniversalDao#batchInsert <nablarch.common.dao.UniversalDao.batchInsert(java.util.List)>`
        を使用して実行する。
      * 一度に登録する件数が膨大になるとパフォーマンスの低下を招く可能性があるため、一括登録一回ごとの件数に上限を設定する。

アップロードを用いた一括登録機能の解説は以上。

:ref:`Getting Started TOPページへ <getting_started>`