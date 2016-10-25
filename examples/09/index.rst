bouncycastleを使用した電子署名つきメールの送信サンプルの使用方法
============================================================================
本章では、bouncycastle\  [#bouncy]_\ を使用した電子署名付きメール送信機能の使用方法の解説を行う。
なお、本機能はサンプル実装のため、導入プロジェクトで使用する際には、ソースコード(プロダクション、テストコード共に）をプロジェクトに取込使用すること。

`ソースコード <https://github.com/nablarch/nablarch-smime-integration>`_ 

.. [#bouncy]
  bouncycastleとは、暗号化等のセキュリティ関連の機能を提供するオープンソースライブラリである。

  詳細は、bouncycastleのサイト(\ `http://www.bouncycastle.org/ <http://www.bouncycastle.org/>`_\ )を参照


環境準備
-------------

**ライブラリの準備**

 本機能は、オープンソースライブラリのbouncycastleに依存しているため、
 クラスパスにbouncycastleの電子署名に関連するjarファイル(以下の3ファイル)を設定する必要がある。
 
 * bcmail-jdk15on-147.jar
 * bcpkix-jdk15on-147.jar
 * bcprov-jdk15on-147.jar
 
 .. tip::
   
   本機能のテストでは、\ **Release1.47**\ のライブラリを使用してテストを行なっている。

   バグフィックスや脆弱性対応などが行われる可能性があるため、bouncycastleのサイトで最新リリースの有無を必ず確認すること。
   もし、1.47以降のバージョンがリリースされている場合には、最新バージョンのライブラリをプロジェクトに適用すること。

**電子署名用の証明書の準備**

 証明書は、認証局から発行してもらい任意のディレクトリ（メール送信機能（バッチ）からアクセス可能なディレクトリ）に配置すること。
 このディレクトリへのアクセス権限は必要最小限にし、必要のないユーザが証明書にアクセスできないようにすることを推奨する。

電子署名付きメール送信機能の構造
---------------------------------------
本機能は、Nablarchアプリケーションフレームワークで提供されるメール送信機能(\ *nablarch.common.mail.MailSender*\ )の拡張機能である。

送信対象のメール送信パターンIDを元に証明書を特定し、電子署名を付加する仕様としている。
このため、本機能を使用する場合には、必ずメール送信パターンIDを使用できるテーブル設計とすること。

詳細は、Nablarchアプリケーションフレームワークのメール送信機能のガイドを参照すること。


設定ファイルの準備
------------------------
本機能を使用する際に必要となる設定は、証明書に関する設定を除き全てNablarchアプリケーションフレームワークのメール送信機能と同じである。
このため、Nablarchアプリケーションフレームワークのメール送信機能のガイドを参照し、設定ファイルの準備をすること。

証明書に関する設定方法
^^^^^^^^^^^^^^^^^^^^^^
本機能を使用する際に必要となる証明書に関する設定方法を、設定例を元に解説する。

.. code-block:: xml

  <!-- 証明書へアクセスするための設定 -->
  <!--
  証明書へのアクセス設定は証明書のファイル単位で設定を行う。
  この例では、証明書ファイルが２ファイルある場合を例にした設定としている。
  name属性：任意の名前（証明書ファイルを識別出来る名前）を設定する。
  class属性：please.change.me.common.mail.smime.CertificateWrapperを固定で設定する。
  -->
  <component name="certificate_1" class="please.change.me.common.mail.smime.CertificateWrapper">
    <!-- 証明書ファイルへアクセスするためのパスワードを設定する。 -->
    <property name="password" value="password" />
    <!-- 証明書に格納された秘密鍵にアクセスするためのパスワードを設定する。 -->
    <property name="keyPassword" value="password" />
    <!-- 証明書ファイルのパスを設定する。 -->
    <property name="certificateFileName" value="classpath:please/change/me/common/mail/smime/data/certificate_1.p12" />
    <!-- 証明書のキーストアタイプを設定する。 -->
    <property name="keyStoreType" value="PKCS12" />
  </component>
  <component name="certificate_2" class="please.change.me.common.mail.smime.CertificateWrapper">
    <property name="password" value="keystorePass" />
    <property name="keyPassword" value="testAliasPass" />
    <property name="certificateFileName" value="classpath:please/change/me/common/mail/smime/data/certificate_2.p12" />
    <property name="keyStoreType" value="JKS" />
  </component>

  <!-- 電子署名付きメール送信機能用に証明書リストを設定 -->
  <map name="certificateList">
    <!-- メール送信パターンID:01は、certificate_1で設定された証明書を使用して電子署名を付加する。 -->
    <entry key="01" value-name="certificate_1" />
    <!-- メール送信パターンID:02は、certificate_2で設定された証明書を使用して電子署名を付加する。 -->
    <entry key="02" value-name="certificate_2" />
  </map>

実行方法
------------------
実行対象のアクションクラスを、\ **please.change.me.common.mail.smime.SMIMESignedMailSender**\ としてメール送信のバッチプロセスを起動する。
プロセス起動時には、このプロセスが処理すべきメールが特定できるメール送信パターンIDを引数として指定する。

詳細は、Nablarchアプリケーションフレームワークのメール送信機能のガイドを参照すること。

