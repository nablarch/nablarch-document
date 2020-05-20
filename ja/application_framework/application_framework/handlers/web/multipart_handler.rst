.. _multipart_handler:

マルチパートリクエストハンドラ
==================================================
.. contents:: 目次
  :depth: 3
  :local:


HTTPリクエストがマルチパート形式の場合に、ボディ部を解析しアップロードファイルを一時ファイルとして保存するハンドラ。

本ハンドラでは、以下の処理を行う。

* マリチパートリクエストの解析
* アップロードファイルを一時ファイルとして保存
* 保存した一時ファイルの削除


処理の流れは以下のとおり。

.. image:: ../images/MultipartHandler/flow.png

ハンドラクラス名
--------------------------------------------------
* :java:extdoc:`nablarch.fw.web.upload.MultipartHandler`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

  <!-- 一時保存先を指定する場合のみ -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-core</artifactId>
  </dependency>

.. _multipart_handler-constraint:

制約
--------------------------------------------------
なし。

このハンドラの動作条件
--------------------------------------------------
このハンドラはマルチパート形式のリクエストの場合のみ、リクエストボディの解析を行う。マルチパート形式かどうかは、リクエストヘッダーの ``Content-Type`` で判断する。

``Content-Type`` が ``multipart/form-data`` と一致する場合は、リクエストがマルチパート形式だと判断し、ボディの解析処理を行う。
それ以外の場合には、このハンドラは何もせずに後続のハンドラに処理を委譲する。

アップロードファイルの一時保存先を指定する
--------------------------------------------------
アップロードファイルの一時保存先ディレクトリは、 :ref:`file_path_management` に設定する。

ファイルパス管理に一時保存先ディレクトリの指定がない場合は、デフォルトの保存先としてシステムプロパティの `java.io.tmpdir` の値を使用する。

以下に一時ファイルの保存先ディレクトリの設定例を示す。

ポイント
  * 保存先ディレクトリの論理名は、 ``uploadFileTmpDir`` とすること。

.. code-block:: xml

  <component name="filePathSetting" class="nablarch.core.util.FilePathSetting">
    <!-- ディレクトリの設定 -->
    <property name="basePathSettings">
      <map>
        <!-- アップロードファイルの一時保存ディレクトリ -->
        <entry key="uploadFileTmpDir" value="file:/var/nablarch/uploadTmpDir" />
      </map>
    </property>
  </component>

.. tip::

  上記の例では、保存先ディレクトリを直接指定しているが、この値は環境ごとに異なることが想定される。
  このため、直接コンポーネント設定ファイルに設定するのではなく、環境設定ファイルに設定することを推奨する。

  詳細は、:ref:`repository-environment_configuration` を参照。


.. _multipart_handler-file_limit:

巨大なファイルのアップロードを防ぐ
--------------------------------------------------
巨大なファイルをアップロードされると、ディスクリソースが枯渇するなどが原因でシステムが正常に稼働しなくなる可能性がある。
このため、このハンドラではアップロードサイズの上限を超過した場合には、400(BadRequest)をクライアントに返却する。

アップロードサイズの上限は、バイト数で設定する。設定を省略した場合は、無制限となる。

以下にアップロードサイズの設定例を示す。

.. code-block:: xml

  <component class="nablarch.fw.web.upload.MultipartHandler" name="multipartHandler">
    <property name="uploadSettings">
      <component class="nablarch.fw.web.upload.UploadSettings">
        <!-- アップロードサイズ(Content-Length)の上限(約10M) -->
        <property name="contentLengthLimit" value="1000000" />
      </component>
    </property>
  </component>


.. tip::

  アップロードサイズの上限は、ファイル単位ではなく1リクエストでアップロード出来る上限となる。

  このため、複数のファイルをアップロードした場合には、それらのファイルサイズの合計値(厳密には、Content-Length)により、上限チェックが実施される。

  もし、ファイル単位でサイズチェックをする必要がある場合には、アクション側で実装すること。

一時ファイルの削除（クリーニング）を行う
--------------------------------------------------
保存されたアップロードファイルを以下の条件でクリーニングする。

* ボディの解析中に例外が発生した場合
* ハンドラの復路で自動削除設定が有効な場合

自動削除設定は、デフォルトで有効に設定されている。
この設定は本番環境で安易に無効にすると、大量の一時ファイルがディスク上に残り、最悪の場合ディスクフルの原因となるため注意すること。

設定値を無効にする場合には、 :java:extdoc:`UploadSettings#autoCleaning <nablarch.fw.web.upload.UploadSettings.setAutoCleaning(boolean)>` に `false` を設定する。


マルチパート解析エラー及びファイルサイズ上限超過時の遷移先画面を設定する
----------------------------------------------------------------------------------------------------
このハンドラでは、マルチパート解析エラー [#part_error]_ や :ref:`ファイルサイズの上限超過時 <multipart_handler-file_limit>` に、
不正なリクエストとしてクライアントに `400(BadRequest)` を返却する。

このため、 `400(BadRequest)` に対応したエラーページの設定を `web.xml` に行う必要がある。
`web.xml` へのエラーページ設定を省略した場合は、ウェブアプリケーションサーバが持つデフォルトのページなどがクライアントに返却される。

.. important::

  このハンドラは、:ref:`multipart_handler-constraint` にあるとおり、 :ref:`session_store_handler` より手前に設定する必要がある。
  このため、 :ref:`session_store_handler` の後続に設定される :ref:`http_error_handler` の :ref:`HttpErrorHandler_DefaultPage` は使用することができない。

.. [#part_error]
  マルチパート解析エラーが発生するケース

  * アップロード中にクライアントからの切断要求があり、ボディー部が不完全な場合
  * バウンダリーが存在しない

.. _multipart_handler-read_upload_file:

アップロードしたファイルを読み込む
------------------------------------------------------------
アップロードされたファイル(一時保存されたファイル)は、 :java:extdoc:`HttpRequest <nablarch.fw.web.HttpRequest>` から取得する。

以下に実装例を示す。

ポイント
  * :java:extdoc:`HttpRequest#getPart <nablarch.fw.web.HttpRequest.getPart(java.lang.String)>` を呼び出してアップロードされたファイルを取得する。
  * :java:extdoc:`HttpRequest#getPart <nablarch.fw.web.HttpRequest.getPart(java.lang.String)>` の引数には、パラメータ名を指定する。

.. code-block:: java

  public HttpResponse upload(HttpRequest request, ExecutionContext context) throws IOException {
    // アップロードファイルの取得
    List<PartInfo> partInfoList = request.getPart("uploadFile");

    if (partInfoList.isEmpty()) {
      // アップロードファイルが指定されていなかった場合は業務エラー
    }

    // アップロードされたファイルを処理する
    InputStream file = partInfoList.get(0).getInputStream()

    // 以下アップロードファイルを読み込み処理を行う。
  }

アップロードファイルを処理する詳細な実装方法は、以下のドキュメントを参照。
なお、 :ref:`data_converter` に記載がある通り、 :ref:`data_bind` が推奨となる。
(:ref:`data_bind` で扱うことのできない形式の場合は、 :ref:`data_format` を使用すること。)

* :ref:`データバインドを使ってアップロードファイルを処理する <data_bind-upload_file>`
* :ref:`汎用データフォーマットを使ってアップロードファイルを処理する <data_format-load_upload_file>`

.. tip::

  アップロードされたファイルが画像ファイル等のバイナリファイルの場合は、読み込んだバイナリデータを使用して処理を行うこと。

  Java8であれば以下の様に実装することでアップロードファイルのバイトデータを読み込むことができる。

  .. code-block:: java

    File savedFile = partInfo.getSavedFile();
    try {
        byte[] bytes = Files.readAllBytes(savedFile.toPath());
    } catch (IOException e) {
        throw new RuntimeException(e);
    }
