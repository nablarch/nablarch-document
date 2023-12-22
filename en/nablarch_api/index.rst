============
Nablarch API
============

* :javadoc_url:`Nablarch API Documentation <nablarch-all/NablarchApi/>`
* :javadoc_url:`Nablarch Testing API Documentation <nablarch-testing/NablarchTestingApi/>`

.. tip::
  Up until Nablarch 5, the API documentation provided only the public API for architects and application programmers.
  However, from Nablarch 6, we provide API documentation including non published APIs.
  
  This is because the Java version has been upgraded and the mechanism for extending Javadoc generation has changed, making it impossible to generate Javadoc for only published APIs.

  Whether or not the referenced class or method is a published API can be determined by whether ``@Published`` is described on the target Javadoc.

  For example, :javadoc_url:`DaoContext <nablarch-all/NablarchApi/nablarch/common/dao/DaoContext.html>` is a public API for architects because ``@Published(tag="architect")`` is described at the class.
  On the other hand, the :javadoc_url:`findAll method of BasicDaoContext <nablarch-all/NablarchApi/nablarch/common/dao/BasicDaoContext.html#findAll(java.lang.Class)>` is a non published API because ``@Published`` is not described in either the class or the method.

  Please refer to :ref:`versionup_policy-backward_compatibility_policy` and `README of Unauthorized API Check Tool (external site) <https://github.com/Fintan-contents/coding-standards/blob/main/en/java/staticanalysis/unpublished-api/README.md>`_ for the details of specifications related to public API.
