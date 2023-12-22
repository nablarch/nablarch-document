.. _view_other:

その他のテンプレートエンジンを使用した画面開発
==================================================
:ref:`web_thymeleaf_adaptor` 以外のテンプレートエンジンを使用したい場合の対応方法を説明する。

使用するテンプレートエンジンが、Servlet forwardを使用してクライアントにレスポンスを返すためのServletを提供している場合には、
``web.xml`` にServletを登録するだけで対応できる。

Servletを提供していないテンプレートエンジンの場合には、
:ref:`web_thymeleaf_adaptor` と同じように :java:extdoc:`CustomResponseWriter <nablarch.fw.web.handler.responsewriter.CustomResponseWriter>` の実装クラスを作成することで対応できる。

実装方法や設定方法などの詳細は、以下の解説書やソースコードを参照すること。

* :ref:`web_thymeleaf_adaptor` 
* `ウェブアプリケーション Thymeleafアダプタのソースコード <https://github.com/nablarch/nablarch-web-thymeleaf-adaptor>`_
