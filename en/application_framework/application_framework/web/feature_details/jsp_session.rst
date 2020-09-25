.. _jsp_session:

How to Prevent JSP from Automatically Creating HTTP Sessions
===========================================================================
The default behavior of JSP is to automatically create an HTTP session when it does not exist.
For example, even when displaying a login screen that does not require an HTTP session,
an HTTP session is automatically created by default wasting the application server memory.

For this reason, it is recommended that JSP should not automatically create an HTTP session.

To disable the automatic creation of an HTTP session in JSP, add the following settings at the beginning of each JSP.

.. code-block:: jsp

  <%@ page session="false" %>


.. important::

  Note that when :ref:`hidden Encryption(deprecated) <tag-hidden_encryption>` is used, the above configuration cannot be used as the HTTP session is used in the hidden encryption process.
  
