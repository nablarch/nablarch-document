.. _hot_deploy_handler:

Hot Deploy Handler
========================================

.. contents:: Table of contents
  :depth: 3
  :local:

This handler hot deploys the application during development.

By using this handler, changes to action class, form class, etc. can be updated immediately without restarting the application server.
This saves the trouble of restarting the application server every time the source code is modified and allows the work to proceed efficiently.

The process flow is as follows.

.. image:: ../images/HotDeployHandler/flow.png

.. important::

  Since this handler reloads the class for each request, it may lead to a decrease in response speed.
  for use in the development environment and **should never be used in the production environment.**

.. important::

  When this handler is used, the request unit test may not operate normally. Therefore, do not use this handler during the request unit test.

.. tip::

  When using this handler, disable the hot deploy function of the server.

Handler class name
--------------------------------------------------
* :java:extdoc:`nablarch.fw.hotdeploy.HotDeployHandler`

Module list
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web-hotdeploy</artifactId>
  </dependency>
  
Constraints
------------------------------
None.

Specify the package to be hot-deployed
--------------------------------------------------------------
Packages to be hot-deployed are configured in the :java:extdoc:`targetPackages <nablarch.fw.hotdeploy.HotDeployHandler.setTargetPackages(java.util.List)>` property.

The configuration example is shown below.

.. code-block:: xml

  <component class="nablarch.fw.hotdeploy.HotDeployHandler">
    <property name="targetPackages">
      <list>
        <value>please.change.me.web.action</value>
        <value>please.change.me.web.form</value>
      </list>
    </property>
  </component>

.. important::

  Entity classes should not be hot-deployed for the following reasons.

  * Since all the classes in the target package are reloaded for each request,
    the response speed may decrease if a class that does not change frequently, such as an entity class, is subject to hot deployment.
  * Since the class loader changes for each request, cast of entity class may fail when :ref:`session_store` is used.
