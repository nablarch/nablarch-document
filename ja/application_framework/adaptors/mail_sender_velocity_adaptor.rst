.. _mail_sender_velocity_adaptor:

E-mail Velocityアダプタ
==================================================

.. contents:: 目次
  :depth: 3
  :local:

`Velocity(外部サイト) <https://velocity.apache.org/>`_ を使用した定型メール送信処理を行うためのアダプタを提供する。

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <!-- E-mail Velocityアダプタ -->
  <dependency>
    <groupId>com.nablarch.integration</groupId>
    <artifactId>nablarch-mail-sender-velocity-adaptor</artifactId>
  </dependency>
  
.. tip::

  Velocityのバージョン2.0を使用してテストを行っている。
  バージョンを変更する場合は、プロジェクト側でテストを行い問題ないことを確認すること。

E-mail Velocityアダプタを使用するための設定を行う
----------------------------------------------------------------------------------------------------
本アダプタを使用するためには、コンポーネント設定ファイルで :java:extdoc:`VelocityMailProcessor<nablarch.integration.mail.velocity.VelocityMailProcessor>` を :java:extdoc:`MailRequester<nablarch.common.mail.MailRequester>` へ設定する。

``VelocityMailProcessor`` にはVelocityが提供する ``VelocityEngine`` を設定する必要がある。
``VelocityEngine`` は以下の理由により :java:extdoc:`ComponentFactory<nablarch.core.repository.di.ComponentFactory>` の実装クラスを作成してコンポーネントを設定することを推奨する。

* ``VelocityEngine`` への設定はコンポーネント設定ファイルよりもJavaコードで行う方がやりやすい
* ``VelocityEngine`` を設定した後に ``init`` メソッドを呼ぶ必要がある

``VelocityEngine`` を作成する ``ComponentFactory`` 実装クラスの例を以下に示す。

.. code-block:: java

  package com.example;

  import org.apache.velocity.app.VelocityEngine;
  import org.apache.velocity.runtime.resource.loader.ClasspathResourceLoader;

  import nablarch.core.repository.di.ComponentFactory;

  public class VelocityEngineFactory implements ComponentFactory<VelocityEngine> {

      @Override
      public VelocityEngine createObject() {
          VelocityEngine velocityEngine = new VelocityEngine();

          velocityEngine.setProperty("resource.loader", "classloader");
          velocityEngine.setProperty("classloader.resource.loader.class",
                  ClasspathResourceLoader.class.getName());

          //必要に応じてVelocityEngineへその他の設定を行う

          velocityEngine.init();

          return velocityEngine;
      }
  }

この ``ConfigurationFactory`` を使用するコンポーネント設定ファイルの設定例を以下に示す。

.. code-block:: xml

  <component name="templateEngineMailProcessor"
             class="nablarch.integration.mail.velocity.VelocityMailProcessor" autowireType="None">
    <property name="velocityEngine">
      <component class="com.example.VelocityEngineFactory"/>
    </property>
  </component>

  <!-- メール送信要求API -->
  <component name="mailRequester" class="nablarch.common.mail.MailRequester">
    <property name="templateEngineMailProcessor" ref="templateEngineMailProcessor"/>
    <!-- その他の設定は省略 -->
  </component>

メールのテンプレートを作成する
--------------------------------------------------
Velocityを使用した定型メール処理では件名と本文を1つのテンプレートに記述する。

件名と本文はデリミタと呼ばれる行で分割される。
デフォルトのデリミタは ``---`` である（半角のハイフンが3つ）。

テンプレートの例を以下に示す。

.. code-block:: none

 $titleについて$option
 ---
 $titleは、申請番号$requestIdで申請されました。
 $approverは速やかに$titleを承認してください。$option

より詳しい件名と本文の分割ルールは :java:extdoc:`TemplateEngineProcessedResult#valueOf<nablarch.common.mail.TemplateEngineProcessedResult.valueOf(java.lang.String)>` を参照。

テンプレートファイルを配置する場所は ``VelocityEngine`` の設定によって異なる。
例えば、前節で示した設定例だとテンプレートファイルはクラスパスからロードされるので、クラスパス上のディレクトリにテンプレートファイルを配置することになる。

メール送信要求を登録する
--------------------------------------------------
単に定型メールの送信要求を登録すればよい。
:ref:`mail-request` を参照。