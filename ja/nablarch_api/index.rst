============
Nablarch API
============

* :javadoc_url:`Nablarch APIドキュメント <nablarch-all/NablarchApi/>`
* :javadoc_url:`Nablarch Testing APIドキュメント <nablarch-testing/NablarchTestingApi/>`

.. tip::
  Nablarch 5までのAPIドキュメントは、アーキテクトとアプリケーションプログラマ向けの公開APIだけに絞ったものを提供していた。
  しかし、Nablarch 6からは非公開APIも含めた形でAPIドキュメントを提供している。
  
  これは、Javaのバージョンが上がってJavadocの生成を拡張する仕組みが変わり、公開APIだけに絞ったJavadoc生成ができなくなったためである。

  参照したクラスやメソッドが公開APIであるかどうかは、対象のJavadoc上に ``@Published`` が記載されているかどうかで判断できる。

  例えば、 :javadoc_url:`DaoContext <nablarch-all/NablarchApi/nablarch/common/dao/DaoContext.html>` はクラスに ``@Published(tag="architect")`` が記載されているためアーキテクト向けの公開APIであることが分かる。
  一方で、 :javadoc_url:`BasicDaoContextのfindAllメソッド <nablarch-all/NablarchApi/nablarch/common/dao/BasicDaoContext.html#findAll(java.lang.Class)>` はクラスにもメソッドにも ``@Published`` が記載されていないことから非公開APIであることが分かる。

  なお、公開APIに関する仕様の詳細は :ref:`versionup_policy-backward_compatibility_policy` および `使用不許可APIチェックツールのREADME (外部サイト) <https://github.com/Fintan-contents/coding-standards/blob/main/java/staticanalysis/unpublished-api/README.md>`_ を参照すること。
