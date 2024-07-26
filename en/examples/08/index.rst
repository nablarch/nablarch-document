=====================================
Sample of HTML Email Send Function
=====================================

Summary
========

Provides the implementation sample of the function that sends the HTML email.

`Source code <https://github.com/nablarch/nablarch-biz-sample-all/tree/master/nablarch-html-mail>`_

This function is a sample to send HTML mail using :ref:`mail` .
Since this function is a sample implementation, the source code (both production and test code) must be imported into the project when using it in an implementation project.


.. important::
  
  This sample does not support the batch send of HTML emails such as campaign notifications.
  Using specialized products is recommended when the following is applicable.
  
    * Sending mass emails such as campaign notifications and email newsletters.
    * Measure the opening rate of the delivered email and effectiveness of click count.
    * The client device (for example, whether it is a feature phone) is identified with the email address and emails sent are switched accordingly.
    * Use emojis.
    * Send a deco-mail.
    * Supports content creation for HTML email, and the content is created by the customer.
      (since there is no draw tool or content creation function in this sample, the developer has to create the content.)

.. important::

   Some clients do not display HTML email as expected, which may prevent the user from viewing the email. For this reason, do not use HTML email for emails where user notifications are important as a business requirement.


.. important::

   **Layout of HTML email**

    Since HTML emails differ in display depending on the email client, establish an HTML email standard with mutual understanding or consent from the customer.
    The following points should be considered with project in the HTML email standard.

    * The email client, device and OS to be tested.
    * The scope of use of HTML tags, styles (CSS properties), etc.
    * Extent to which fonts, color schemes, etc. are used.
    * Width of content. (Even when only PC is supported, the size that can be confirmed by the preview function of the email client.)

   **Points to keep in mind when creating content**

    * Since some email clients ignore the contents of the <head> tag, it is **generally not recommended** to remove styles in CSS files and <style> tags for HTML mail.

    * Try to keep the design as simple as possible.

    * Since some email clients do not support media queries, do not use responsive design as much as possible.


Request
========

Implemented
-------------
* HTML email can be sent (including alternative text).
* Performs HTML escape for the string in the placeholder part of the text.
  This enables the same security measures to be implemented as a normal online screen.

Discontinued
-------------
* It can absorb the differences between different email clients.
  (Specifically, it can absorb differences in style defined by CSS, etc., as well as implementation differences, including whether JavaScript can be used or not.)

 Since the HTML design and target client are selected by the project that wants to send the HTML email,
 this request should be dealt with during content creation and is not provided in this sample.
  

* Images can be embedded in HTML email.
  
  Embedded images in an email increases the size of the email, and it takes a long time to receive them even if the user rejects HTML in the email client.It also increases the load on the email server.
  Since the consumer web services often use the URL format, this sample does not provide the image embedding function.

Structure
============

Depending on the content, HTML emails should be sent with the following Content-Type patterns that conform to RFC 2557.

This shows the pattern and data model of the email to be sent.

Email format
------------

The following emails can be sent in this sample.

+-------------+----------------------------------------+-----------------+------------------------+
| Email format| Context class used by business action  | Attachment files| Mail structure pattern |
+=============+========================================+=================+========================+
| TEXT        | TemplateMailContext                    | No              | 1                      |
|             |                                        +-----------------+------------------------+
|             |                                        | Yes             | 2                      |
+-------------+----------------------------------------+-----------------+------------------------+
| HTML        | TemplateHtmlMailContext                | No              | 3                      |
|             |                                        +-----------------+------------------------+
|             |                                        | Yes             | 4                      |
+-------------+----------------------------------------+-----------------+------------------------+

**Mail structure pattern 1**
 
 .. image:: _images/Mail_Pattern01.jpg
    :scale: 70
 
 
**Mail structure pattern 2**

 .. image:: _images/Mail_Pattern02.jpg
    :scale: 70


**Mail structure pattern 3**

 .. image:: _images/Mail_Pattern03.jpg
    :scale: 70


**Mail structure pattern 4**

 .. image:: _images/Mail_Pattern04.jpg
    :scale: 70

Class diagram
-------------

 .. image:: _images/HtmlMail_ClassDiagram.png
    :width: 100%
 

Responsibilities of each class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  ==============================================================  ==================================================================================================
  Class name                                                      Summary
  ==============================================================  ==================================================================================================
  please.change.me.common.mail.html.HtmlMailRequester             Class that accepts HTML email send request which is an extension of MailRequester
  please.change.me.common.mail.html.TemplateHtmlMailContext       Class that extends TemplateMailContext and retains information required for HTML email.
                                                                  By converting alternative text to the body, it is possible to implement the function
                                                                  which sends email in plain text format using the template for HTML email.
  please.change.me.common.mail.html.HtmlMailTable                 Class that accesses the HTML email table.
  please.change.me.common.mail.html.HtmlMailSender                Class that supports sending HTML emails which is an extension of MailSender. If the request is
                                                                  not for HTML email, delegates the process to parent class and sends email in plain text format.
  please.change.me.common.mail.html.HtmlMailContentCreator        Class that generates content for HTML email.
  ==============================================================  ==================================================================================================

Description of configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 .. code-block:: xml

    <!-- Email send request API -->
    <component name="mailRequester" class="please.change.me.common.mail.html.HtmlMailRequester">
        <property name="mailRequestConfig" ref="mailRequestConfig" />
        <property name="mailRequestIdGenerator" ref="mailRequestIdGenerator" />
        <property name="mailRequestTable" ref="mailRequestTable" />
        <property name="mailRecipientTable" ref="mailRecipientTable" />
        <property name="mailAttachedFileTable" ref="mailAttachedFileTable" />
        <property name="mailTemplateTable" ref="mailTemplateTable" />
        <!-- Configure the access function to extended table -->
        <property name="htmlMailTable" ref="htmlMailTable" />
    </component>

    <!-- 
    Although the schema is defined with the email send function of the Nablarch application framework,
    it is not defined in the configuration file as modifying the source code directly in this library is better
    Since the function of table access is common to Requester and Sender, the component should be defined.
    -->
    <component name="databaseMetaDataExtractor" class=".dao.CustomDatabaseMetaDataExtractor" />



Data model
------------

The extension from the email function is shown.

This sample adopts a architecture to operate as TEXT+HTML email
by associating the extended table for HTML to the email-related table.

.. tip::

  The DDL of the data model shown below is included in the test resource.

Alternative text template table for HTML email
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A relation table of the email template that manages the alternative text of the standard email for HTML.

  ======================== ================ ==============================================================================================================
  Definition               Java type        Remarks
  ======================== ================ ==============================================================================================================
  Email template ID        java.lang.String | PK
  Language                 java.lang.String | PK
  Alternate text           java.lang.String | Text for mailers that cannot display HTML email messages.
  ======================== ================ ==============================================================================================================


Alternative text table for HTML mail
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Relation table for email send requests that manages alternative text for HTML email.

  ======================== ================== ======================================================================================================================
  Definition               Java type          Remarks
  ======================== ================== ======================================================================================================================
  Email send request PK    java.lang.String   | PK
  Alternate text           java.lang.String   | Text for mailers that cannot display HTML email messages.
  ======================== ================== ======================================================================================================================

Implementation examples
========================

Send HTML email
----------------

The implementation using this sample is similar to the standard email send of the email send function of the Nablarch application framework.

As the context class used in business action is different, implementation example is omitted.



Dynamic content switching
----------------------------
A sample implementation, by using an HTML template, that dynamically switches between HTML and TEXT formats from business actions is shown.

Switching method
^^^^^^^^^^^^^^^^^^

 When **plain text** is specified in the contentType of TemplateHtmlMailContext during email send request,
 the body is replaced with the alternate text.

 +--------------------------+----------------+-------------------------------------------+----------------+
 | Context class            | Specified type | Transfer source to body text              | Content-Type   |
 +==========================+================+===========================================+================+
 | TemplateMailContext      | \-             | Email template.Body                       | text/plain     |
 +--------------------------+----------------+-------------------------------------------+----------------+
 | TemplateHtmlMailContext  | *text/plain*   | *Alternate text template.Alternate text*  | *text/plain*   |
 +                          +----------------+-------------------------------------------+----------------+
 |                          | text/html      |  Email template.Body                      | text/html      |
 +--------------------------+----------------+-------------------------------------------+----------------+

 .. code-block:: java
 
    public HttpResponse doSendMail(HttpRequest req, ExecutionContext ctx) {
        MailSampleForm form = MailSampleForm.validate(req, "mail");
        TemplateHtmlMailContext mail = new TemplateHtmlMailContext();
        // If the user has selected ContentType.PLAIN, the alternative text will be switched to the body.
        mail.setContentType(form.getType()); 
        // Configure other properties and call MailRequester.
    }


Combined use of digital signature
----------------------------------

When using a digital signature, use :ref:`the extended sample of digital signature<bouncycastle_mail_sample>` and HTML email sample together.

  * This sample is used for the registration process of the email send request.
  * For email send batch, use the HtmlMailContentCreator class provided by this sample to extend the digital signature extended sample (SMIMESignedMailSender) so that HTML email content can be created and used.

The implementation image is shown below.

.. code-block:: java

    @Override
    protected void addBodyContent(MimeMessage mimeMessage, MailRequestTable.MailRequest mailRequest,
            List<? extends MailAttachedFileTable.MailAttachedFile> attachedFiles, ExecutionContext context) throws MessagingException {

        String mailSendPatternId = context.getSessionScopedVar("mailSendPatternId");
        Map<String, CertificateWrapper> certificateChain = SystemRepository.get(CERTIFICATE_REPOSITORY_KEY);
        CertificateWrapper certificateWrapper = certificateChain.get(mailSendPatternId);

        try {
            // Configure the generator that creates the digital signature.
            SMIMESignedGenerator smimeSignedGenerator = new SMIMESignedGenerator();
            // ---Middle is omitted---

            // Branching with HTML email
            MimeBodyPart bodyPart;
            HtmlMailTable htmlTable = SystemRepository.get("htmlMailTable");
            SqlRow alternativeText = htmlTable.findAlternativeText(mailRequest.getMailRequestId());
            if (alternativeText != null) {
                bodyPart = new MimeBodyPart();
                bodyPart.setContent(HtmlMailContentCreator.create(mailRequest.getMailBody(), mailRequest.getCharset(),
                                                                  alternativeText.getString("alternativeText"), attachedFiles));
                mimeMessage.setContent(smimeSignedGenerator.generate(bodyPart));
            } else {
              // Implementation of SMIMESignedMailSender
              bodyPart = new MimeBodyPart();
              bodyPart.setText(mailRequest.getMailBody(), mailRequest.getCharset());
              // ---Rest is omitted---
        } catch (Exception e) {
            MailConfig mailConfig = SystemRepository.get("mailConfig");
            String mailRequestId = mailRequest.getMailRequestId();

            throw new TransactionAbnormalEnd(
                    mailConfig.getAbnormalEndExitCode(), e,
                    mailConfig.getSendFailureCode(), mailRequestId);
        }
    }



Embed tags
--------------

.. important::

  Embedding of tags is not implemented or recommended at the time of provision because of the following points.
 
    * It becomes difficult to check the layout of HTML email
    * Security measures must be implemented with project

  Therefore, use it carefully after considering whether it can be handled by preparing multiple templates.
  Consider whether template creation cost can compensate for the security risk.

In the sample provided by Nablarch, HTML escape is enforced, so it is not possible to dynamically embed HTML tags in the template.

When it is needed to embed it dynamically, modify TemplateHtmlMailContext in the project and add an API that calls TemplateMailContext#setReplaceKeyValue.

.. code-block:: java

  Embed the tag without doing HTML escape.
  public void setReplaceKeyRawValue(String key, String tag) {
      super.setReplaceKeyValue(key, tag);
  }

.. tip::

 The test for HTML emails is the same as that for regular emails.
  
  * The HTML text validates the table of email send requests.
  * Layout confirmation in the actual email client uses the send batch to send and check the email.

