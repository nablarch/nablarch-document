.. _bouncycastle_mail_sample:

How to Use a Sample to Send a Digitally Signed Email Using Bouncycastle
============================================================================

This chapter describes how to use the digitally signed send mail feature using bouncycastle. [#bouncy]_
Since this function is a sample implementation, the source code (both production and test code) must be imported into the project when using it in an implementation project.

`Source code <https://github.com/nablarch/nablarch-biz-sample-all/tree/master/nablarch-smime-integration>`_

.. [#bouncy]
  Bouncycastle is an open source library that provides security-related functions such as encryption.

  For more information, see site of bouncycastle (\ `https://www.bouncycastle.org/ <https://www.bouncycastle.org/>`_\ ).


Environment preparation
-----------------------

**Preparing the library**

 Add the following to your pom.xml.

 .. code-block:: xml

   <dependency>
     <groupId>org.bouncycastle</groupId>
     <artifactId>bcjmail-jdk18on</artifactId>
     <version>1.78.1</version>
   </dependency>

 .. tip::

   The library of **Release1.78.1** is used for the test of this function.

   Check the bouncycastle site for the latest release, as bug and vulnerability fixes may have been addressed.
   If a version after 1.78.1 has been released, the latest version of the library should be used in the project.

**Prepare a certificate for digital signature**

 The certificate must be issued by the certification authority and placed in an any directory (a directory accessible by the email send function (batch)).
 It is recommended that access privileges to this directory are kept to a minimum to prevent users for whom it is not required from accessing the certificate.

Structure of digitally signed email send function
--------------------------------------------------
This function is an extension of the email send function (\ *nablarch.common.mail.MailSender*\ ) provided by the Nablarch application framework.

A certificate is identified based on the target email send pattern ID and a digital signature is added to the certificate.
Therefore, when this function is used, ensure to design a table that can use the mail transmission pattern ID.

For more information, see the guide to :ref:`mail`.


Preparation of configuration file
----------------------------------
The configuration required to use this function are all the same as the email send function of Nablarch Application Framework, except for the certificate configuration.
For this reason, refer to the guide to email send functions of the Nablarch application framework to prepare the configuration file.

How to configure certificates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This section describes how to configure the certificates required to use this function using an example configuration.

.. code-block:: xml

  <!-- Configuring access to certificates -->
  <!--
  The access configuration to the certificate is configured for each certificate file.
  In this example, the configuration is based on two certificate files.
  Name attribute: Configure an any name (name that can identify the certificate file).
  Class attribute: Configure tplease.change.me.common.mail.smime.CertificateWrapper to a fixed value.
  -->
  <component name="certificate_1" class="please.change.me.common.mail.smime.CertificateWrapper">
    <!-- Configure the password to access the certificate file. -->
    <property name="password" value="password" />
    <!-- Configure the password to access the private key stored in the certificate. -->
    <property name="keyPassword" value="password" />
    <!-- Configure the path of the certificate file. -->
    <property name="certificateFileName" value="classpath:please/change/me/common/mail/smime/data/certificate_1.p12" />
    <!-- Configure the keystore type of the certificate. -->
    <property name="keyStoreType" value="PKCS12" />
  </component>
  <component name="certificate_2" class="please.change.me.common.mail.smime.CertificateWrapper">
    <property name="password" value="keystorePass" />
    <property name="keyPassword" value="testAliasPass" />
    <property name="certificateFileName" value="classpath:please/change/me/common/mail/smime/data/certificate_2.p12" />
    <property name="keyStoreType" value="JKS" />
  </component>

  <!-- Configure a certificate list for send function of digitally signed emails -->
  <map name="certificateList">
    <!-- The mail send pattern ID:01 is a digital signature that is added using the certificate set in certificate_1. -->
    <entry key="01" value-name="certificate_1" />
    <!-- The mail send pattern ID:02 is a digital signature that is added using the certificate set in certificate_2. -->
    <entry key="02" value-name="certificate_2" />
  </map>

Execution
------------------
Launch a process of email send batch with the target action class as **please.change.me.common.mail.smime.SMIMESignedMailSender**.
When a process is launched, an email send pattern ID that can identify the mail to be processed by this process is specified as an argument.

For more information, see the guide to email send functions of the Nablarch application framework.

