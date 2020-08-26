.. _`stateless_web_app`:

Making Web Applications Stateless
=====================================================================

.. contents:: Table of contents
  :depth: 3

Basic concept
--------------------------------------------------

The HTTP session provided by the servlet API cannot be scaled out as it is because the AP server has its own state.
Normally, you need to take the following measures to scale out the AP server.

1. Enable sticky sessions in the load balancer
2. use the session replication function of the AP server
3. set the AP server's HTTP session destination to NoSQL

1 and 2 are inferior in terms of ease of disposability, as referred to in the `Twelve-Factor App <https://12factor.net/ja/>`_, while 2 and 3 are dependent on the AP server.

Although some of the features used by Nablarch depend on HTTP sessions,
they are by switching these features to HTTP session-independent ones, the
The AP server can be made stateless.

.. _http-session-dependence:

Features that depend on HTTP sessions
--------------------------------------------------

The following features depend on the HTTP session by default.

* :ref:`session_store`
* :ref:`Double submission prevention<tag-double_submission>`
* :ref:`thread_context_handler`
* :ref:`http_rewrite_handler`
* :ref:`Hidden encryption<tag-hidden_encryption>`

How to implement the HTTP session-independent feature
--------------------------------------------------------------------

You can remove dependence on HTTP sessions by configuring each function of :ref:`http-session-dependence` as follows.

Session store
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`db_managed_expiration`

Double submission prevention
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`db_double_submit` 

Thread context cariable management handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Do not use the following components in :ref:`thread context initialization<thread_context_handler-initialization>`.

* :java:extdoc:`LanguageAttributeInHttpSession <nablarch.common.web.handler.threadcontext.LanguageAttributeInHttpSession>`
* :java:extdoc:`TimeZoneAttributeInHttpSession <nablarch.common.web.handler.threadcontext.TimeZoneAttributeInHttpSession>`
* :java:extdoc:`UserIdAttribute <nablarch.common.handler.threadcontext.UserIdAttribute>`

Each of the following components can be substituted as implementations that do not use HTTP sessions.

* :java:extdoc:`LanguageAttributeInHttpCookie <nablarch.common.web.handler.threadcontext.LanguageAttributeInHttpCookie>`
* :java:extdoc:`TimeZoneAttributeInHttpCookie <nablarch.common.web.handler.threadcontext.TimeZoneAttributeInHttpCookie>`
* :java:extdoc:`UserIdAttributeInSessionStore <nablarch.common.web.handler.threadcontext.UserIdAttributeInSessionStore>`

HTTP rewrite handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Do not use :ref:`http_rewrite_handler`.
If it is used, configure it so that the session scope is not accessed.

Hidden encryption
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Nablarch provides the feature of :ref:`hidden encryption<tag-hidden_encryption>`.
Since this feature is HTTP session dependent, set :ref:`useHiddenEncryption <tag-use_hidden_encryption>` to ``false`` to not use it.

Using the local file system
--------------------------------------------------
If you store uploaded files and so on locally on the AP server, they will have state.
In such a case, you need to prepare a shared storage space so that the AP server does not have files locally.

Detecting accidental creation of HTTP sessions
--------------------------------------------------
To prevent accidental creation of HTTP sessions due to a misconfiguration or an implementation error, a feature to detect the creation of HTTP sessions is provided.
When this feature is enabled, an exception is sent when an attempt to create an HTTP session is made.

This feature can be enabled by setting the ``preventSessionCreation`` property of the
:java:extdoc:`WebFrontController <nablarch.fw.web.servlet.WebFrontController>` to ``true`` (disabled by default at ``false``).

Specifically, the detection function can be enabled by writing the following in the configuration file that defines the components of :java:extdoc:`WebFrontController <nablarch.fw.web.servlet.WebFrontController>`.

.. code-block:: xml

  <!-- handler queue configuration -->
  <component name="webFrontController"
             class="nablarch.fw.web.servlet.WebFrontController">

    <!-- Detecting accidental creation of HTTP sessions -->
    <property name="preventSessionCreation" value="true" />
