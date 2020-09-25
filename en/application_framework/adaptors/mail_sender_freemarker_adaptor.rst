.. _mail_sender_freemarker_adaptor:

E-mail FreeMarker Adapter
==================================================

.. contents:: Table of contents
  :depth: 3
  :local:

Provides an adapter for performing standard e-mail send process using `FreeMarker(external site) <https://freemarker.apache.org/>`_ .

Module list
--------------------------------------------------
.. code-block:: xml

  <!-- E-mail FreeMarker adapter -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-mail-sender-freemarker-adaptor</artifactId>
  </dependency>
  
.. tip::

  Tests are conducted using FreeMarker version 2.3.27-incubating. 
  When changing the version, test in the project to confirm that there are no problems.

Configuration for using the E-mail FreeMarker adapter
----------------------------------------------------------------------------------------------------
To use this adapter, configure :java:extdoc:`FreeMarkerMailProcessor<nablarch.integration.mail.freemarker.FreeMarkerMailProcessor>` to :java:extdoc:`MailRequester<nablarch.common.mail.MailRequester>` in the component configuration file.

``Configuration``  provided by FreeMarker has to be configured in ``FreeMarkerMailProcessor``. 
For ``Configuration``, it is recommended that the component configuration be performed by creating an implementation class of :java:extdoc:`ComponentFactory<nablarch.core.repository.di.ComponentFactory>` for the following reasons.

* Default constructor is deprecated for ``Configuration`` 
* Configuring with Java code is easier than component configuration file for ``Configuration`` 

An example of ``ComponentFactory`` implementation class that creates ``Configuration`` is shown below.

.. code-block:: java

  package com.example;

  import freemarker.template.Configuration;
  import nablarch.core.repository.di.ComponentFactory;

  public class ConfigurationFactory implements ComponentFactory<Configuration> {

      private String basePackagePath;
      private String encoding;

      @Override
      public Configuration createObject() {
          Configuration cfg = new Configuration(Configuration.getVersion());
          ClassLoader classLoader = getClass().getClassLoader();
          cfg.setClassLoaderForTemplateLoading(classLoader, basePackagePath);
          cfg.setDefaultEncoding(encoding);
          // Other configurations are made to Configuration as needed
          return cfg;
      }

      public void setBasePackagePath(String basePackagePath) {
          this.basePackagePath = basePackagePath;
      }

      public void setEncoding(String encoding) {
          this.encoding = encoding;
      }
  }

The setting example of the component configuration file that uses the ``ConfigurationFactory``  is shown below.

.. code-block:: xml

  <component name="templateEngineMailProcessor"
             class="nablarch.integration.mail.freemarker.FreeMarkerMailProcessor" autowireType="None">
    <property name="configuration">
      <component class="com.example.ConfigurationFactory">
        <property name="basePackagePath" value="com/example/template/"/>
        <property name="encoding" value="UTF-8"/>
      </component>
    </property>
  </component>

  <!-- E-mail send request API -->
  <component name="mailRequester" class="nablarch.common.mail.MailRequester">
    <property name="templateEngineMailProcessor" ref="templateEngineMailProcessor"/>
    <!-- Other settings are omitted -->
  </component>

Create an e-mail template
--------------------------------------------------
In standard e-mail process using FreeMarker, the subject and body are described in one template.

The subject and body are separated by lines called delimiters. 
The default delimiter is ``---`` (three single-byte hyphens).

An example of the template is shown below.

.. code-block:: none

 ${option}regarding ${title}
 ---
 ${title} has been submitted with application number ${requestId}.
 ${Approver} should approve ${title} promptly. ${option}

For more details on subject and body split rules, see  :java:extdoc:`TemplateEngineProcessedResult#valueOf<nablarch.common.mail.TemplateEngineProcessedResult.valueOf(java.lang.String)>` .

Where to place the template file depends on the  ``Configuration`` settings. 
For example, in the configuration example shown in the previous section, the template file is loaded from the class path. 
Since  ``com/example/template/``  is configured in  ``basePackagePath`` , template files will be placed in the  ``com/example/template/``  directory of the class path.

Register an e-mail send request
--------------------------------------------------
Just to register the send request of the standard e-mail. 
See :ref:`mail-request` .