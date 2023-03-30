.. _mail_sender_thymeleaf_adaptor:

E-mail Thymeleaf Adapter
==================================================

.. contents:: Table of contents
  :depth: 3
  :local:

Provides an adapter for sending an e-mail template using `Thymeleaf (external site) <http://www.thymeleaf.org>`_ .

Module list
--------------------------------------------------
.. code-block:: xml

  <!-- E-mail Thymeleaf adapter -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-mail-sender-thymeleaf-adaptor</artifactId>
  </dependency>
  
.. tip::

  Tests are conducted using Thymeleaf version 3.1.1.RELEASE. 
  When changing the version, test in the project to confirm that there are no problems.

Configuration for using the E-mail Thymeleaf adapter
----------------------------------------------------------------------------------------------------
To use this adapter, configure :java:extdoc:`ThymeleafMailProcessor<nablarch.integration.mail.thymeleaf.ThymeleafMailProcessor>` to :java:extdoc:`MailRequester<nablarch.common.mail.MailRequester>`  in the component configuration file.

``TemplateEngine``  provided by Thymeleaf has to be configured in ``ThymeleafMailProcessor`` .

The configuration example of the component configuration file is shown below.

.. code-block:: xml

  <component name="templateEngine" class="org.thymeleaf.TemplateEngine" autowireType="None">
    <property name="templateResolver">
      <component class="org.thymeleaf.templateresolver.ClassLoaderTemplateResolver" autowireType="None">
        <property name="prefix" value="com/example/template/" />
      </component>
    </property>
  </component>

  <component name="templateEngineMailProcessor"
    class="nablarch.integration.mail.thymeleaf.ThymeleafMailProcessor" autowireType="None">
    <property name="templateEngine" ref="templateEngine" />
  </component>

  <!-- E-mail send request API -->
  <component name="mailRequester" class="nablarch.common.mail.MailRequester">
    <property name="templateEngineMailProcessor" ref="templateEngineMailProcessor"/>
    <!-- Other settings are omitted -->
  </component>

Create an e-mail template
--------------------------------------------------
In standard e-mail process using Thymeleaf, the subject and body are described in one template.


The subject and body are separated by lines called delimiters. The default delimiter is ``---`` (three single-byte hyphens).

An example of the template is shown below.

.. code-block:: none

 [(${Option})] regarding [(${title})]
 ---
 [(${title})] has been submitted with application number [(${requestId})].
 [(${Approver})] should approve [(${title})] promptly. [(${option})]

For more details on subject and body split rules, see :java:extdoc:`TemplateEngineProcessedResult#valueOf<nablarch.common.mail.TemplateEngineProcessedResult.valueOf(java.lang.String)>` .

Where to place the template file depends on the ``TemplateEngine`` configuration. 
For example, in the configuration example shown in the previous section, the template file is loaded from the class path.
Since ``com/example/template/`` is configured in the ``prefix`` of ``ClassLoaderTemplateResolver``, place the template file in ``com/example/template/`` of the class path.

Register an e-mail send request
--------------------------------------------------
Just to register the send request of the standard e-mail. 
See :ref:`mail-request`.
