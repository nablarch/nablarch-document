.. _`platform`:

Operating Environment
====================================

.. contents:: Table of contents
   :depth: 3
   :local:

This section describes the operating environment of the Nablarch framework.

.. tip::
 For operating environments concerning contents other than the Nablarch framework (example: Nablarch SQL Executor), 
 see the documentation of each content.

Environment Requirements of the Nablarch Framework
-----------------------------------------------------
The Nablarch framework is built using only the Java standard specifications and requires at least the following for operation.

* Java SE 17
* JDBC 3.0

The following Jakarta EE specifications are required depending on the Nablarch function being used.

* Jakarta Standard Tag Library 3.0
* Jakarta Activation 2.1
* Jakarta Server Pages 3.1
* Jakarta Servlet 6.0
* Jakarta Mail 2.1
* Jakarta Messaging 3.1
* Jakarta Persistence 3.1
* Jakarta Batch 2.1
* Jakarta Bean Validation 3.0
* Jakarta RESTful Web Services 3.1

.. important::
 Although the version number shown here indicates a specific version, a higher than the indicated version number can be used. 
 This is because backward compatibility is basically maintained when the Java standard specifications and Jakarta EE specifications are upgraded.

Test environment of Nablarch framework
-----------------------------------------------------
The Nablarch framework has been tested and verified to operate properly in the following environments.

Java
 * Java SE 17/21 [#java21]_

Database
 * Oracle Database 19c/21c/23ai
 * IBM Db2 11.5/12.1
 * SQL Server 2017/2019/2022
 * PostgreSQL 12.2/13.2/14.0/15.2/16.2/17.4

Application server
 * WebSphere Application Server Liberty 25.0.0.2
 * Open Liberty 25.0.0.2
 * Red Hat JBoss Enterprise Application Platform 8.0.0
 * WildFly 35.0.1.Final
 * Apache Tomcat 10.1.17

Jakarta EE
 * Hibernate Validator 8.0.0.Final
 * JBeret 2.1.1.Final

MOM (Message oriented middleware)
 * IBM MQ 9.3

Browser
 PC
  * Microsoft Edge
  * Mozilla Firefox
  * Google Chrome
  * Safari

.. [#java21] When used with Java21, the configurations are required to be changed separately. For information on how to configure, see :doc:`../blank_project/setup_blankProject/setup_Java21`.
