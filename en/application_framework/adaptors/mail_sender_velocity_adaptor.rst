.. _mail_sender_velocity_adaptor:

E-mail Velocity Adapter
==================================================

.. contents:: Table of contents
  :depth: 3
  :local:

Provides an adapter for sending an e-mail template using `Velocity(external site) <https://velocity.apache.org/>`_ .

Module list
--------------------------------------------------
.. code-block:: xml

  <!-- E-mail Velocity adapter -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-mail-sender-velocity-adaptor</artifactId>
  </dependency>
  
.. tip::

  Tests are conducted using Velocity version 2.0. 
  When changing the version, test in the project to confirm that there are no problems.

Configuration for using the E-mail Velocity adapter
----------------------------------------------------------------------------------------------------
To use this adapter, configure :java:extdoc:`VelocityMailProcessor<nablarch.integration.mail.velocity.VelocityMailProcessor>` to :java:extdoc:`MailRequester<nablarch.common.mail.MailRequester>` in the component configuration file.

``VelocityEngine``  provided by Velocity has to be configured in ``VelocityMailProcessor`` . 
For ``VelocityEngine`` , it is recommended that the component configuration be performed by creating an implementation class of  :java:extdoc:`ComponentFactory<nablarch.core.repository.di.ComponentFactory>` for the following reasons.

* Configuring ``VelocityEngine`` with Java code is easier than component configuration file.
* init method is required to be called after configuring ``VelocityEngine``.

An example of ``ComponentFactory`` implementation class that creates ``VelocityEngine`` is shown below.

.. code-block:: java

  package com.example;

  import org.apache.velocity.app.VelocityEngine;
  import org.apache.velocity.runtime.resource.loader.ClasspathResourceLoader;

  import nablarch.core.repository.di.ComponentFactory;

  public class VelocityEngineFactory implements ComponentFactory<VelocityEngine> {

      @Override
      public VelocityEngine createObject() {
          VelocityEngine velocityEngine = new VelocityEngine();

          velocityEngine.setProperty("resource.loader", "classloader");
          velocityEngine.setProperty("classloader.resource.loader.class",
                  ClasspathResourceLoader.class.getName());

          // Other configurations are made to VelocityEngine as needed

          velocityEngine.init();

          return velocityEngine;
      }
  }

The setting example of the component configuration file that uses the ``ConfigurationFactory`` is shown below.

.. code-block:: xml

  <component name="templateEngineMailProcessor"
             class="nablarch.integration.mail.velocity.VelocityMailProcessor" autowireType="None">
    <property name="velocityEngine">
      <component class="com.example.VelocityEngineFactory"/>
    </property>
  </component>

  <!-- E-mail send request API -->
  <component name="mailRequester" class="nablarch.common.mail.MailRequester">
    <property name="templateEngineMailProcessor" ref="templateEngineMailProcessor"/>
    <!-- Other settings are omitted -->
  </component>

Create an e-mail template
--------------------------------------------------
In standard e-mail process using Velocity, the subject and body are described in one template.

In standard e-mail process using Velocity, the subject and body are described in one template.
The subject and body are separated by lines called delimiters. The default delimiter is ``---`` (three single-byte hyphens).

An example of the template is shown below.

.. code-block:: none

 $Option regarding $title$option
 ---
 $title has been submitted with application number $requestId.
 $Approver should approve $title promptly. $option

For more details on subject and body split rules, see :java:extdoc:`TemplateEngineProcessedResult#valueOf<nablarch.common.mail.TemplateEngineProcessedResult.valueOf(java.lang.String)>` .

Where to place the template file depends on the ``VelocityEngine`` configuration. 
For example, since the template file is loaded from the class path in the configuration example shown in the previous section, place the template file in a directory of the class path.

Register an e-mail send request
--------------------------------------------------
Just to register the send request of the standard e-mail. 
See :ref:`mail-request`.