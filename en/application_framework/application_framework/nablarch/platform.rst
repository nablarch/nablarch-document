.. _`platform`:

Operating Environment
====================================

.. contents:: Table of contents
   :depth: 3
   :local:

This section describes the operating environment of the Nablarch framework.

.. tip::
 For operating environments concerning contents other than the Nablarch framework (example: UI development platform), 
 see the documentation of each content.

Environment Requirements of the Nablarch Framework
-----------------------------------------------------
The Nablarch framework is built using only the Java standard specifications and requires at least the following for operation.

* Java SE 6
* JDBC 3.0

The following Java standard specifications are required depending on the Nablarch function being used.

* JavaServer Pages Standard Tag Library 1.1
* JavaBeans Activation Framework 1.1
* JavaServer Pages 2.1
* Java Servlet 2.5
* JavaMail API 1.4
* Java Message Service API 1.1-rev-1
* Java Persistence 2.0
* Batch Applications for the Java Platform 1.0
* Bean Validation 1.1
* Java API for RESTful Web Services (JAX-RS) 2.0

.. important::
 Although the version number shown here indicates a specific version, a higher than the indicated version number can be used. 
 This is because backward compatibility is basically maintained when the Java standard specifications are upgraded.

Test environment of Nablarch framework
-----------------------------------------------------
The Nablarch framework has been tested and verified to operate properly in the following environments.

Java
 * Java SE 6/8/11 [#java11]_/17 [#java17]_

Database
 * Oracle Database 12c/19c/21c
 * IBM Db2 10.5/11.5
 * SQL Server 2017/2019
 * PostgreSQL 10.0/11.5/12.2/13.2/14.0

Application server
 * Oracle Weblogic Server 14.1.1
 * WebSphere Application Server 9.0.5.8
 * WildFly 26.0.1.Final
 * Apache Tomcat 9.0.54

Java EE
 * Hibernate Validator 5.3.6.Final
 * JBeret 1.3.4.Final

MOM (Message oriented middleware)
 * WebSphere MQ 7

Browser
 PC
  * Internet Explorer 11
  * Microsoft Edge
  * Mozilla Firefox
  * Google Chrome
  * Safari
 Smart phone
  * Safari(iOS)
  * Google Chrome(Android)

Operational results of Nablarch framework
-----------------------------------------------------
The operation results of February 2016 are shown below.

OS
 * RedHat Enterprise Linux 5/6
 * WindowsServer 2008
 * AIX 7

Java
 * Java SE 6/7/8

Database
 * Oracle Database 11g/12c
 * DB2 10
 * SQLServer 2008
 * PostgreSQL 9

Application server
 * Oracle Weblogic Server 11g/12c
 * WebSphere Application Server 7/8
 * JBoss Application Server 7
 * Apache Tomcat 6/7/8

MOM (Message oriented middleware)
 * WebSphere MQ 7

.. [#java11] When used with Java11, the configurations are required to be changed separately. For information on how to configure, see :doc:`../blank_project/setup_blankProject/setup_Java11`.
.. [#java17] When used with Java17, the configurations are required to be changed separately. For information on how to configure, see :doc:`../blank_project/setup_blankProject/setup_Java17`.
