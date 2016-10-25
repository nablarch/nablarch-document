===========================
HTMLメール送信機能サンプル
===========================

概要
====

HTMLメールを送信する機能の実装サンプルを提供する。

`ソースコード <https://github.com/nablarch/nablarch-biz-sample-all>`_

本機能は、Nablarchアプリケーションフレームワークで提供されるメール送信機能(nablarch.common.mail.MailSender)の定型メールを利用してHTMLメールを送信するサンプルである。
なお、本機能はサンプル実装のため、導入プロジェクトで使用する際には、ソースコード(プロダクション、テストコード共に）をプロジェクトに取り込み、使用すること。


.. important::
  
  本サンプルはキャンペーンの通知のようなHTMLメールの一括送信には対応していない。
  下記に当てはまる場合は、プロダクトの利用を推奨する。
  
    * キャンペーン通知やメールマガジンなど、一括で大量のメールを送信する。
    * 配信したメールの開封率、クリックカウントの効果を測定する。
    * メールアドレスからクライアント（例えば、フィーチャーフォンか否か）を判別し、送信するメールを切り替える。
    * 絵文字を利用する。
    * デコメールを送信する。
    * HTMLメールのコンテンツ作成を支援し、顧客がコンテンツを作成する。
      (本サンプルではドローツールやコンテンツ作成機能は存在しないため、開発者がコンテンツを作成する必要がある。)

.. important::

   一部のクライアントでは期待したとおりにHTMLメールが表示されないことにより、ユーザーがメールを参照しない可能性がある。このため、業務要件としてユーザー通知が重要なメールにはHTMLメールを利用しないこと。


.. important::

   **HTMLメールのレイアウト**

    メールクライアントによりHTMLメールの表示に差異があるため、HTMLメール標準を策定し、顧客と合意すること。
    HTMLメール標準では下記のような点を含め、PJにて検討すること。

    * テスト対象とするメールクライアントとデバイス、OS。
    * HTMLタグ、スタイル(CSSのプロパティ)などの使用範囲。
    * フォント、配色などの使用範囲。
    * コンテンツの横幅。(PCのみをサポートする場合でも、メールクライアントのプレビュー機能で確認できる程度のサイズ。)

   **コンテンツ作成時の留意点**

    * <head>タグの内容を無視するメールクライアントがあるため、HTMLメールは、一般的にスタイルをCSSファイルや<style>タグに切り出すことが **推奨されていない** 。

    * 極力シンプルなデザインにすること。

    * メールクライアントによってはメディアクエリをサポートしていないため、極力レスポンシブデザインは採用しないこと。

要求
====

実装済み
--------
* HTMLメール(代替テキストを含む)を送信できる。
* 本文のプレースホルダー部分の文字列に対して、HTMLエスケープを行う。
  これにより、通常のオンライン画面と同様のセキュリティ対策を行うことができる。

取り下げ
--------
* メールクライアント毎の差異を吸収できる。
  (具体的にはCSSなどで定義されたスタイルの差異、JavaScriptの使用可否を含めた実装差異を吸収できる。)

 HTMLメールを送信したいPJにてHTMLのデザインおよび対象クライアントの選定をするため、
 本要求はコンテンツ作成時に対応するものとし、本サンプルでは提供しない。
  

* HTMLメールに画像を埋めこむことができる。
  
  メールに画像を埋めこむとメール容量が増大し、メールクライアントでHTMLを拒否したユーザーでも受信に時間がかかる。また、メールサーバーへの負荷が増大する。
  コンシューマ向けのWebサービスではURL形式の使用が多いため、本サンプルでは画像の埋めこみ機能を提供しない。

構成
============

HTMLメールはコンテンツの内容に応じて、RFC 2557に準拠した下記のパターンのContent-Typeで送信する。

送信するメールのパターンとデータモデルを示す。

メールの形式
------------

本サンプルでは、以下のメールを送信することができる。

+-------------+----------------------------------------+--------------+----------------------+
| メール形式  | 業務Actionが使用するコンテキストクラス | 添付ファイル | メール構造のパターン |
+=============+========================================+==============+======================+
| TEXT        | TemplateMailContext                    | 無し         | 1                    |
|             |                                        +--------------+----------------------+
|             |                                        | 有り         | 2                    |
+-------------+----------------------------------------+--------------+----------------------+
| HTML        | TemplateHtmlMailContext                | 無し         | 3                    |
|             |                                        +--------------+----------------------+
|             |                                        | 有り         | 4                    |
+-------------+----------------------------------------+--------------+----------------------+

**メール構造のパターン１**
 
 .. image:: _images/Mail_Pattern01.jpg
    :scale: 70
 
 
**メール構造のパターン２**

 .. image:: _images/Mail_Pattern02.jpg
    :scale: 70


**メール構造のパターン３**

 .. image:: _images/Mail_Pattern03.jpg
    :scale: 70


**メール構造のパターン４**

 .. image:: _images/Mail_Pattern04.jpg
    :scale: 70

クラス図
--------

 .. image:: _images/HtmlMail_ClassDiagram.png
    :height: 30em
    :width:  60em
 

各クラスの責務
^^^^^^^^^^^^^^^^

  ==============================================================  ==============================================================================================
  クラス名                                                        概要
  ==============================================================  ==============================================================================================
  please.change.me.common.mail.html.HtmlMailRequester             MailRequesterを拡張したHTMLメール送信要求を受け付けるクラス。
  please.change.me.common.mail.html.TemplateHtmlMailContext       TemplateMailContextを拡張し、HTMLメールに必要な情報を保持するクラス。
                                                                  代替テキストを本文に変換することで、HTMLメール用のテンプレートを利用して
                                                                  プレーンテキスト形式のメールを送信する機能を実現する。
  please.change.me.common.mail.html.HtmlMailTable                 HTMLメール用のテーブルにアクセスするクラス。
  please.change.me.common.mail.html.HtmlMailSender                MailSenderを拡張したHTMLメールの送信をサポートするクラス。HTMLメール用の要求でない場合は、
                                                                  親クラスに処理を委譲し、プレーンテキスト形式のメールを送信する。
  please.change.me.common.mail.html.HtmlMailContentCreator        HTMLメール用のコンテンツを生成するクラス。
  ==============================================================  ==============================================================================================

設定の記述
^^^^^^^^^^^

 .. code-block:: xml

    <!-- メール送信要求API -->
    <component name="mailRequester" class="please.change.me.common.mail.html.HtmlMailRequester">
        <property name="mailRequestConfig" ref="mailRequestConfig" />
        <property name="mailRequestIdGenerator" ref="mailRequestIdGenerator" />
        <property name="mailRequestTable" ref="mailRequestTable" />
        <property name="mailRecipientTable" ref="mailRecipientTable" />
        <property name="mailAttachedFileTable" ref="mailAttachedFileTable" />
        <property name="mailTemplateTable" ref="mailTemplateTable" />
        <!-- 拡張したテーブルへのアクセス機能を設定する -->
        <property name="htmlMailTable" ref="htmlMailTable" />
    </component>

    <!-- 
    Nablarchアプリケーションフレームワークのメール送信機能ではスキーマ定義を行うが、
    本ライブラリではソースコードを直接修正すれば良いため、設定ファイルでの定義は行わない。
    ただし、テーブルアクセスの機能はRequester,Senderで共通のため、コンポーネントの定義を行うこと。
    -->
    <component name="htmlMailTable" class="please.change.me.common.mail.html.HtmlMailTable" />



データモデル
------------

メール機能からの拡張部分を示す。

本サンプルではメール関連テーブルにHTML用の拡張テーブルを関連付けることで
TEXT+HTMLメールとして動作させる方式を採用している。

.. tip::

  下記に示すデータモデルのDDLはテスト資源に含まれている。

HTMLメール用代替テキストテンプレートテーブル
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

HTML用定型メールの代替テキストを管理するメールテンプレートの関連テーブル。

  ======================== ================ ==============================================================================================================
  定義                     Javaの型         備考
  ======================== ================ ==============================================================================================================
  メールテンプレートID     java.lang.String | PK
  言語                     java.lang.String | PK
  代替テキスト             java.lang.String | HTMLメールを表示できないメーラーのためのテキスト。
  ======================== ================ ==============================================================================================================


HTMLメール用代替テキストテーブル
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

HTMLメール用の代替テキストを管理するメール送信要求の関連テーブル。

  ======================== ================== ======================================================================================================================
  定義                     Javaの型           備考
  ======================== ================== ======================================================================================================================
  メール送信要求ID         java.lang.String   | PK
  代替テキスト             java.lang.String   | HTMLメールを表示できないメーラーのためのテキスト。
  ======================== ================== ======================================================================================================================

実装例
======

HTMLメールの送信
----------------

本サンプルを利用した実装は、Nablarchアプリケーションフレームワークのメール送信機能の定型メール送信と同様である。

業務アクションで利用するコンテキストクラスが異なるだけなので、実装例は省略する。



コンテンツの動的な切替
-----------------------
HTML用のテンプレートを利用して、業務アクションなどから動的にHTML形式とTEXT形式を切り替える実装のサンプルを提示する。

切替方法
^^^^^^^^^

 メール送信要求時、TemplateHtmlMailContextのcontentTypeに **プレーンテキスト** を指定した場合、
 代替テキストを本文に差し替える。

 +--------------------------+----------------+-------------------------------------------+----------------+
 | コンテキストクラス       | 指定されたType | 本文への移送元                            | Content-Type   |
 +==========================+================+===========================================+================+
 | TemplateMailContext      | \-             | メールテンプレート.本文                   | text/plain     |
 +--------------------------+----------------+-------------------------------------------+----------------+
 | TemplateHtmlMailContext  | *text/plain*   | *代替テキストテンプレート.代替テキスト*   | *text/plain*   |
 +                          +----------------+-------------------------------------------+----------------+
 |                          | text/html      | メールテンプレート.本文                   | text/html      |
 +--------------------------+----------------+-------------------------------------------+----------------+

 .. code-block:: java
 
    public HttpResponse doSendMail(HttpRequest req, ExecutionContext ctx) {
        MailSampleForm form = MailSampleForm.validate(req, "mail");
        TemplateHtmlMailContext mail = new TemplateHtmlMailContext();
        // このとき、ユーザーがContentType.PLAINを選択していれば、代替テキストが本文に切り替わる。
        mail.setContentType(form.getType()); 
        // その他のプロパティを設定し、MailRequesterを呼び出す。
    }


電子署名の併用
---------------

電子署名を利用する場合は、電子署名の拡張サンプルとHTMLメールサンプルを併用する。

  * メール送信要求の登録処理は本サンプルを利用する。
  * メール送信バッチについては、本サンプルが提供するHtmlMailContentCreatorクラスを利用して、HTMLメールのコンテンツを作成できるように電子署名の拡張サンプル(SMIMESignedMailSender)を拡張し、利用する。

実装イメージを下記に示す。

.. code-block:: java

    @Override
    protected void addBodyContent(MimeMessage mimeMessage, MailRequestTable.MailRequest mailRequest,
            List<? extends MailAttachedFileTable.MailAttachedFile> attachedFiles, ExecutionContext context) throws MessagingException {

        String mailSendPatternId = context.getSessionScopedVar("mailSendPatternId");
        Map<String, CertificateWrapper> certificateChain = SystemRepository.get(CERTIFICATE_REPOSITORY_KEY);
        CertificateWrapper certificateWrapper = certificateChain.get(mailSendPatternId);

        try {
            // 電子署名を生成するジェネレータの設定を行う。
            SMIMESignedGenerator smimeSignedGenerator = new SMIMESignedGenerator();
            // ---中略---

            // HTMLメールとの分岐
            MimeBodyPart bodyPart;
            HtmlMailTable htmlTable = SystemRepository.get("htmlMailTable");
            SqlRow alternativeText = htmlTable.findAlternativeText(mailRequest.getMailRequestId());
            if (alternativeText != null) {
                bodyPart = new MimeBodyPart();
                bodyPart.setContent(HtmlMailContentCreator.create(mailRequest.getMailBody(), mailRequest.getCharset(),
                                                                  alternativeText.getString("alternativeText"), attachedFiles));
                mimeMessage.setContent(smimeSignedGenerator.generate(bodyPart));
            } else {
              // SMIMESignedMailSenderの実装
              bodyPart = new MimeBodyPart();
              bodyPart.setText(mailRequest.getMailBody(), mailRequest.getCharset());
              // ---後略---
        } catch (Exception e) {
            MailConfig mailConfig = SystemRepository.get("mailConfig");
            String mailRequestId = mailRequest.getMailRequestId();

            throw new TransactionAbnormalEnd(
                    mailConfig.getAbnormalEndExitCode(), e,
                    mailConfig.getSendFailureCode(), mailRequestId);
        }
    }



タグを埋めこむ
--------------

.. important::

  タグの埋めこみは、下記の点から提供時には実装しておらず、推奨もしていない。
 
    * HTMLメールのレイアウト確認が困難になる
    * セキュリティ対策もPJにて実施する必要がある

  そのため、安易に利用せず、テンプレートを複数用意することで対応できないか検討すること。
  ※テンプレートの作成コストでセキュリティ上のリスクを補填できる点も考慮すること。

Nablarchが提供するサンプルでは、HTMLエスケープを強制するため、動的にHTMLタグをテンプレートに埋めこむことはできない。

動的に埋めこむ必要がある場合は、PJにてTemplateHtmlMailContextを修正し、TemplateMailContext#setReplaceKeyValueを呼び出すAPIを追加すること。

.. code-block:: java

  // HTMLエスケープをせずにタグを埋めこむ。
  public void setReplaceKeyRawValue(String key, String tag) {
      super.setReplaceKeyValue(key, tag);
  }

.. tip::

 HTMLメールのテストは通常のメールと同様のテストを行う。
  
  * HTMLテキストはメール送信要求のテーブルを検証する。
  * 実際のメールクライアントでのレイアウト確認は送信バッチを利用して、メールを送信して確認する。

