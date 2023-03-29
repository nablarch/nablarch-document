.. _`project_upload`:

Create a Batch registration Function Using Upload
===================================================
This section describes the function to upload a CSV file for batch registration based on an example application.

Description of the function to be created
  1. Click "Project batch registration (プロジェクト一括登録)" in the header menu.

    .. image:: ../images/project_upload/project_upload-link.png
      :scale: 80

  2. Download the batch registration sample file which generates the validation error from below

     :download:`batch_project_registration_validation_error.csv <../downloads/project_upload/batch_project_registration_validation_error.csv>` (プロジェクト一括登録_バリデーションエラー.csv)

  3. Upload the sample file and click the "Register(登録)" button.

    .. image:: ../images/project_upload/project_upload-invalid_upload.png
      :scale: 80

  3. Validation error occurs.

    .. image:: ../images/project_upload/project_upload-validate.png
      :scale: 80

  4. Download the batch registration sample file which does not generate validation error from below

    :download:`project_batch_registration.csv <../downloads/project_upload/project_batch_registration.csv>` (プロジェクト一括登録.csv)

  5. Upload the sample file and click the "Register(登録)" button.

    .. image:: ../images/project_upload/project_upload-valid_upload.png
      :scale: 80

  6. The contents of the file are registered in the database and the completion message is displayed.

    .. image:: ../images/project_upload/project_upload-complete.png
      :scale: 80

Overview of the business action method to be created
-----------------------------------------------------

    ProjectUploadAction.java
      .. code-block:: java

        @OnDoubleSubmission
        @OnError(type = ApplicationException.class, path = "/WEB-INF/view/projectUpload/create.jsp")
        public HttpResponse upload(HttpRequest request, ExecutionContext context) {

            // Acquire upload file
            List<PartInfo> partInfoList = request.getPart("uploadFile");
            if (partInfoList.isEmpty()) {
                throw new ApplicationException(
                        MessageUtil.createMessage(MessageLevel.ERROR, "errors.upload"));
            }
            PartInfo partInfo = partInfoList.get(0);

            LoginUserPrincipal userContext = SessionUtil.get(context, "userContext");

            // Loading and validation of upload files
            List<Project> projects = readFileAndValidate(partInfo, userContext);

            // Batch registration to DB
            insertProjects(projects);

            // Add a completion message
            context.setRequestScopedVar("uploadProjectSize", projects.size());

            // Saving a file
            saveFile(partInfo);

            return new HttpResponse("/WEB-INF/view/projectUpload/create.jsp");
        }
  
  The processing flow of the business action method is as follows.
  
  #. :ref:`Acquire a file<project_upload-file_upload_action>`
  #. :ref:`Validate the contents of the CSV file by binding to Bean<project_upload-validation>`
  #. :ref:`Batch registration to DB<project_upload-bulk_insert>`
  #. :ref:`Saving a file<project_upload-file_upload_action>`
  
  The details of each process is described under
  :ref:`Implementation of the file upload function<project_upload-file_upload-impl>` and
  :ref:`Implementation of the batch registration function<project_upload-bulk_insert-impl>`.

.. _`project_upload-file_upload-impl`:

Implementation of the file upload function
-----------------------------------------------------
First, how to create the upload part of the batch registration function using upload is explained

  #. :ref:`Create a file upload screen<project_upload-upload_jsp>`
  #. :ref:`Create a business action method to acquire and save a file<project_upload-file_upload_action>`

  .. _`project_upload-upload_jsp`:

  Create a file upload screen
    Create a screen with a file upload field.

    /src/main/webapp/WEB-INF/view/projectUpload/create.jsp
      .. code-block:: jsp

        <n:form useToken="true" enctype="multipart/form-data">
            <!-- Omitted -->
            <div class="message-area margin-top">
                <!-- Completion message display part -->
                <c:if test="${not empty uploadProjectSize}">
                    <ul><li class="message-info"><n:message messageId="success.upload.project" option0="${uploadProjectSize}" /></li></ul>
                </c:if>
                <!-- Error message display part -->
                <n:errors errorCss="message-error"/>
            </div>
            <!-- Omitted -->
            <h4 class="font-group">Project information file selection</h4>
            <table class="table">
                <!--  Description of screen design is omitted -->
                <tbody>
                    <tr>
                        <th class="item-norequired" colspan="2">Project information file selection</th>
                    </tr>
                    <tr>
                        <th class="width-250 required">Project information file</th>
                        <td >
                            <div class="form-group is-fileinput">
                                <div class="input-group">
                                    <n:file name="uploadFile" id="uploadFile"/>
                                    <!--  Description of screen design is omitted -->
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
                              cssClass="btn btn-raised btn-default">Registration</n:button>
                </div>
            </div>
        </n:form>

    Key points of this implementation
      * Specify `multipart/form-data` as `enctype` attribute of :ref:`tag-form_tag` to send multipart file.
      * Create a file upload field using :ref:`tag-file_tag`. Specify the registration name of the request object in the `name` attribute.
        To acquire the file in a business action, specify this registration name as an argument of
        :java:extdoc:`HttpRequest#getPart<nablarch.fw.web.HttpRequest.getPart(java.lang.String)>`
      * Display upload completed message with :ref:`tag-message_tag`, once the upload is completed.
        In order to include the number of uploads in the completion message, specify the number of uploads configured in the request scope in `option0` attribute.
      * Use :ref:`tag-errors_tag` to create an area to display the list of validation error messages for the target file.
        For the output format of the error message list, refer to :ref:`error message list <tag-write_error_errors_tag>`.

  .. _`project_upload-file_upload_action`:

  Create a business action method
    Describes how to get and save a file in the business action method.

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

            // Batch registration process is omitted as it will be described later

            // Saving a file
            saveFile(partInfo);

            return new HttpResponse("/WEB-INF/view/projectUpload/create.jsp");
        }
        
        /**
         * Save a file
         *
         * @param partInfo Upload file information
         */
        private void saveFile(final PartInfo partInfo) {
            String fileName = generateUniqueFileName(partInfo.getFileName());
            UploadHelper helper = new UploadHelper(partInfo);
            helper.moveFileTo("uploadFiles", fileName);
        }

    Key points of this implementation
      * Acquire the file :java:extdoc:`HttpRequest#getPart<nablarch.fw.web.HttpRequest.getPart(java.lang.String)>`.
      * When the file does not exist (not uploaded), then the size of :java:extdoc:`PartInfo<nablarch.fw.web.upload.PartInfo>` list that is acquired will be zero.
        This value is used to perform control such as throwing a business exception.
      * The uploaded file is stored in a temporary area by the :ref:`multipart request handler<multipart_handler>`.
        Since the temporary area is automatically deleted, if you need to permanently (save) an uploaded file, move the file to an arbitrary directory.
        However, file transfers are possible only when the :ref:`file path management<file_path_management>` is used to manage the input and output of files and directories.
      * Use :java:extdoc:`UploadHelper#moveFileTo<nablarch.fw.web.upload.util.UploadHelper.moveFileTo(java.lang.String-java.lang.String)>` method to transfer files.
        The first argument is the key name of the file storage directory registered in the configuration file.
        In the Example Application, the configuration is described in the following file.

        filepath-for-webui.xml
          .. code-block:: xml

            <!-- File path definition -->
            <component name="filePathSetting"
                    class="nablarch.core.util.FilePathSetting" autowireType="None">
              <property name="basePathSettings">
                <map>
                  <!--Omitted -->
                  <!-- Directory to store the upload file -->
                  <entry key="uploadFiles" value="file:./work/input" />
                </map>
              </property>
              <!-- Omitted -->
            </component>

.. _`project_upload-bulk_insert-impl`:

Implementation of the batch registration function
---------------------------------------------------
This section describes how to create the batch registration part of the batch registration function using uploads.

    #. :ref:`Create a Bean to bind a file<project_upload-create_bean>`
    #. :ref:`Create a business action method for batch registration of files<project_upload-bulk_action>`

.. _`project_upload-create_bean`:

Create a bean to bind the contents of the file
  A bean to bind the contents of the file is created.

  ProjectUploadDto.java
    .. code-block:: java

      @Csv(headers = { /** Describe the header **/},
              properties = { /** Properties to bind **/},
              type = Csv.CsvType.CUSTOM)
      @CsvFormat(charset = "Shift_JIS", fieldSeparator = ',',ignoreEmptyLine = true,
              lineSeparator = "\r\n", quote = '"',
              quoteMode = CsvDataBindConfig.QuoteMode.NORMAL, requiredHeader = true, emptyToNull = true)
      public class ProjectUploadDto implements Serializable {

          // Excerpt of some items only.Getter and setter are omitted

          /** Project name */
          @Required(message = "{nablarch.core.validation.ee.Required.upload}")
          @Domain("projectName")
          private String projectName;

          /** Project type */
          @Required(message = "{nablarch.core.validation.ee.Required.upload}")
          @Domain("projectType")
          private String projectType;

          // Property that holds the line count to process.Setter is omitted.
          /** Line count*/
          private Long lineNumber;

          /**
           * Get line count.
           * @return Line count
           */
          @LineNumber
          public Long getLineNumber() {
              return lineNumber;
          }
      }

  Key points of this implementation
    * Use :java:extdoc:`@Csv<nablarch.common.databind.csv.Csv>` for configuration to link the contents of the uploaded CSV file with the bean property.
      Use  :java:extdoc:`@CsvFormat<nablarch.common.databind.csv.CsvFormat>` to specify the acceptable CSV format.
      （ :java:extdoc:`@CsvFormat<nablarch.common.databind.csv.CsvFormat>` is not required when using the :ref:`default format specification<data_bind-csv_format_set>`）
      For information on how to configure the annotation, refer to :ref:`format specification method when binding the CSV file to the Java Beans class <data_bind-csv_format-beans>`.
    * Perform :ref:`Bean Validation<bean_validation>` by assigning annotations for validation of :java:extdoc:`@Required<nablarch.core.validation.ee.Required>`
      and :java:extdoc:`@Domain<nablarch.core.validation.ee.Domain>` to the property.
    * To accept the values from a file, :ref:`property is defined as string type<bean_validation-form_property>`,
      and conversion to an appropriate type is performed as per the safe value that has passed the validation.
    * By defining the line count property and granting :java:extdoc:`LineNumber<nablarch.common.databind.LineNumber>` to the getter,
      the line of the target data can be configured automatically.

    .. tip::
      The validation error message of a required input item is changed to an appropriate value as per the file upload.
      For information on how to specify a validation message, refer to :ref:`configure the input value check rule<client_create_validation_rule>`.

.. _`project_upload-bulk_action`:

Create a business action method
  Create a business action method to register the contents of the uploaded file in the database.

  .. _`project_upload-validation`:

  Validate the contents of 1 CSV file by binding to Bean
    ProjectUploadAction.java
      .. code-block:: java

        private List<Project> readFileAndValidate(final PartInfo partInfo, final LoginUserPrincipal userContext) {
            List<Message> messages = new ArrayList<>();
            List<Project> projects = new ArrayList<>();

            // Validate the contents of the file by binding it to the bean
            try (final ObjectMapper<ProjectUploadDto> mapper
                     = ObjectMapperFactory.create(
                            ProjectUploadDto.class, partInfo.getInputStream())) {
                ProjectUploadDto projectUploadDto;

                while ((projectUploadDto = mapper.read()) != null) {

                    // Validate and configure the result messages
                    messages.addAll(validate(projectUploadDto));

                    // Create an entity
                    projects.add(createProject(projectUploadDto, userContext.getUserId()));
                }
            } catch (InvalidDataFormatException e) {
                // Parsing ends if there is an invalid line in the file format
                messages.add(
                    MessageUtil.createMessage(
                        MessageLevel.ERROR, "errors.upload.format", e.getLineNumber()));
            }

            // Not registered in the database even if there is one error
            if (!messages.isEmpty()) {
                throw new ApplicationException(messages);
            }
            return projects;
        }
    
        /**
         * Validate the project information and store the result in the message list.
         *
         * @param projectUploadDto Project information Bean generated from CSV
         * @return messages         List of validation result messages
         */
        private List<Message> validate(final ProjectUploadDto projectUploadDto) {

            List<Message> messages = new ArrayList<>();

            // Single item validation.Execute Bean validation based on the annotation defined in Dto
            try {
                ValidatorUtil.validate(projectUploadDto);
            } catch (ApplicationException e) {
                messages.addAll(e.getMessages()
                        .stream()
                        .map(message -> MessageUtil.createMessage(MessageLevel.ERROR,
                                "errors.upload.validate", projectUploadDto.getLineNumber(), message))
                        .collect(Collectors.toList()));
            }

            // Customer existence check
            if (!existsClient(projectUploadDto)) {
                messages.add(MessageUtil.createMessage(MessageLevel.ERROR,
                        "errors.upload.client", projectUploadDto.getLineNumber()));
            }

            return messages;
        }

    Key points of this implementation
      * Use :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` provided by
        :ref:`DataBind<data_bind>` to bind and get the file to the bean.
      * By executing :java:extdoc:`ObjectMapper#read <nablarch.common.databind.ObjectMapper.read()>` for the acquired
        :java:extdoc:`ObjectMapper <nablarch.common.databind.ObjectMapper>` object, the list of bound bean can be obtained.
      * :java:extdoc:`Validator <jakarta.validation.Validator>` object can be created by using
        :java:extdoc:`ValidatorUtil#getValidator <nablarch.core.validation.ee.ValidatorUtil.getValidator()>`, and :ref:`Bean Validation<bean_validation>` can be executed for any Bean.
      * When verification is continued up to the last row and not aborted even when an error occurs,
        error messages for all rows are stored after the verification is completed in :java:extdoc:`Message<nablarch.core.message.Message>` list, by generating and
        throwing :java:extdoc:`ApplicationException<nablarch.core.message.ApplicationException>` with this list as an argument,
        it can be output to the screen with :ref:`tag-errors_tag`.
      * For how to assign a property name to the validation message,
        implement by referring to :ref:`how to include item names in the message when a validation error occurs<bean_validation-property_name>`.
    

  .. _`project_upload-bulk_insert`:

  2.Batch registration to DB
    ProjectUploadAction.java
      .. code-block:: java

        public HttpResponse upload(HttpRequest request,ExecutionContext context)
                throws IOException {

            // Execution of validation is described above

            // Batch registration to DB
            insertProjects(projects);

            // Saving a file is described above
        }

        /**
         * Register multiple project entities to the database in a batch.
         * @param projects List of validated projects
         */
        private void insertProjects(List<Project> projects) {

          List<Project> insertProjects = new ArrayList<Project>();

          for (Project project : projects) {
              insertProjects.add(project);
              // Batch insert every 100 records
              if (insertProjects.size() >= 100) {
                  UniversalDao.batchInsert(insertProjects);
                  insertProjects.clear();
              }
          }

          if (!insertProjects.isEmpty()) {
              UniversalDao.batchInsert(insertProjects);
          }
        }

    Key points of this implementation
      * Batch registration is executed using :java:extdoc:`UniversalDao#batchInsert <nablarch.common.dao.UniversalDao.batchInsert(java.util.List)>`.

      * Set an upper limit on the number of registrations per batch registration, because a large number of registrations at a time may result in a deterioration in performance.

This completes the explanation for the batch registration function using upload.

:ref:`Getting Started To TOP page <getting_started>`