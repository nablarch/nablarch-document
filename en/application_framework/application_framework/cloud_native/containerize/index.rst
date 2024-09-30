.. _docker_container:

Docker Containerization
==================================================

.. contents:: Table of contents
  :depth: 2
  :local:

This chapter describes how to turn an application created with Nablarch into a Docker container image in a cloud-native manner.

First, we will describe what modifications must be made to a traditional Nablarch application in order to containerize it.
And describe the dedicated archetype, which creates a blank project that includes the configuration for containerization in advance.

.. _requirement_for_cloud_native:

What a suitable system for a cloud environment requires
--------------------------------------------------------------------------------------------------

Cloud native
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Cloud native** refers to a system that was developed from the start to run in a cloud environment such as AWS and is optimized for the cloud environment.

A system suitable for a cloud environment requires a different design than a traditional system that would run in an on-premises environment.
For example, it is necessary to keep the application stateless in order to have scalability.


The Twelve-Factor App
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `The Twelve-Factor App`_ (external site) is a system development methodology proposed by `Heroku <https://www.heroku.com/>`_ (external site) engineers that summarizes the twelve factors to be considered when developing a system suitable for the cloud environment.

The modifications of the Nablarch application needed for containerization described in this chapter are based on the method described in this `The Twelve-Factor App`_ (external site).

.. _modify_nablarch_app_for_cloud_native:

Modifications required for Nablarch web applications
--------------------------------------------------------------------------------------------------

If building a Nablarch web application using :ref:`the standard web application blank project <firstStepGenerateWebBlankProject>` ,
the following points are in violation of `The Twelve-Factor App`_ (external site).

Stateless
  The `VI. Processes <https://12factor.net/processes>`_ (external site) is said that the application must be stateless.
  That is, an individual application must not hold state.

  The standard blank project violates this policy because state management using HTTP sessions is enabled.

  See :ref:`stateless_web_app` for configuration to make a Nablarch web application stateless.

Log output
  The `XI. Logs <https://12factor.net/logs>`_ (external site) is said that all application logs should be written to standard output and not output to a file.

  The standard blank project violates this policy because a file is specified as the output destination for the logger.

  See :ref:`log-basic_setting` for Nablarch's log output configuration.

Configuration using environment variables
  `III. Config <https://12factor.net/config>`_ (external site) is said that configuration (such as configuration for connecting to other services),
  which are switched for each environment, should be configured from environment variables, not from within the application.

  The standard blank project violates this policy because it uses Maven profiles to switch the difference between the development and production environment configurations.

  See :ref:`repository-overwrite_environment_configuration_by_os_env_var` for how to override environment-dependent values using environment variables.

.. _modify_nablarch_batch_for_cloud_native:

Modifications required for Nablarch batch applications
--------------------------------------------------------------------------------------------------

`The Twelve-Factor App`_ (external site) is a methodology for developing SaaS applications, but many of its factor can also be applied when developing batch applications suitable for cloud environments.

If building a Nablarch batch application using :ref:`the standard Nablarch batch application blank project <firstStepGenerateBatchBlankProject>` ,
the points that need to be modified are as follows.

Log output
  (Omitted as it is identical to the Nablarch web application)

Configuration using environment variables
  (Omitted as it is identical to the Nablarch web application)



.. _nablarch_container_archetype:

Archetype for container
--------------------------------------------------------------------------------------------------

Nablarch provides archetypes for web and batch applications that are designed to run on Docker containers.

Blank projects generated using this archetype have the modifications described in such as :ref:`modify_nablarch_app_for_cloud_native` and :ref:`modify_nablarch_batch_for_cloud_native` applied in advance.
Also, a Maven plugin called `Jib`_ (external site) is built in for easy generation of Docker containers, so developers can start developing Nablarch applications for Docker containers soon.

.. tip::
  
  Using Jib, it is possible to create container images without having to write a Dockerfile.

  Dockerfile can describe the most basic instructions for creating Docker container images.
  For this reason, Dockerfile allows to create container images in a flexible way.
  But on the other hand, using Dockerfile also has the following disadvantages.

  * The content can be complex because it is written in basic instructions
  * A high level of knowledge is required, which makes it necessary to write with best practices in mind, such as container image layer structure

  Jib has been specialized in creating Docker container images for Java applications.
  The description of the configuration is abstracted for Java applications and allows to create container images in a way that takes into consideration best practices without any special configuration.

  For these reasons, the Nablarch archetype for container adopts the method of creating container images using Jib instead of writing Dockerfile directly.


See below for a description of the archetype for Docker containers.

* :ref:`Prerequisites <firstStepPreamble>`
* :ref:`Project structure <container_web_project_summary>`
* :ref:`About switching settings for each environment <container_production_config>`
* :ref:`Initial Setup Procedure <first_step_container>`

.. _The Twelve-Factor App: https://12factor.net/
.. _Jib: https://github.com/GoogleContainerTools/jib/tree/master/jib-maven-plugin
