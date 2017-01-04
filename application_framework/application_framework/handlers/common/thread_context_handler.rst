.. _thread_context_handler:

スレッドコンテキスト変数管理ハンドラ
=======================================

.. contents:: 目次
  :depth: 3
  :local:

スレッドコンテキストの各属性値について、リクエスト毎に初期化処理を行うハンドラ。

スレッドコンテキストとは、リクエストIDやユーザIDなど、
同一の処理スレッド内で共有する値をスレッドローカル領域上に保持するための仕組みである。

.. important::
  本ハンドラで設定したスレッドローカル上の値は、 :ref:`thread_context_clear_handler` を使用して、復路処理で削除を行うこと。
  往路処理にて本ハンドラより手前のハンドラでスレッドコンテキストにアクセスした場合、
  値を取得することはできないため本ハンドラより手前ではスレッドコンテキストにアクセスしないよう注意すること。

.. tip::
 スレッドコンテキストの属性値の多くは、本ハンドラによって設定されるが、
 本ハンドラ以外のハンドラや業務アクションから任意の変数を設定することも可能である。

本ハンドラでは、以下の処理を行う。

* :ref:`thread_context_handler-initialization`

処理の流れは以下のとおり。

.. image:: ../images/ThreadContextHandler/ThreadContextHandler_flow.png

ハンドラクラス名
--------------------------------------------------
* :java:extdoc:`nablarch.common.handler.threadcontext.ThreadContextHandler`

モジュール一覧
--------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw</artifactId>
  </dependency>

  <!-- 国際化対応により、言語やタイムゾーンを選択できる画面を作る場合のみ  -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web</artifactId>
  </dependency>

制約
---------------------------------------
なし。

.. _thread_context_handler-initialization:

リクエスト毎にスレッドコンテキストの初期化を行う
-----------------------------------------------------------
スレッドコンテキストの初期化は、
:java:extdoc:`ThreadContextAttributeインタフェース <nablarch.common.handler.threadcontext.ThreadContextAttribute>`
を実装したクラスを使用して行う。

デフォルトで以下のクラスを提供している。

リクエストID、内部リクエストID
 * :java:extdoc:`RequestIdAttribute <nablarch.common.handler.threadcontext.RequestIdAttribute>`
 * :java:extdoc:`InternalRequestIdAttribute <nablarch.common.handler.threadcontext.InternalRequestIdAttribute>`

ユーザID
 * :java:extdoc:`UserIdAttribute <nablarch.common.handler.threadcontext.UserIdAttribute>`

言語
 * :java:extdoc:`LanguageAttribute <nablarch.common.handler.threadcontext.LanguageAttribute>`
 * :java:extdoc:`HttpLanguageAttribute <nablarch.common.web.handler.threadcontext.HttpLanguageAttribute>`
 * :java:extdoc:`LanguageAttributeInHttpCookie <nablarch.common.web.handler.threadcontext.LanguageAttributeInHttpCookie>`
 * :java:extdoc:`LanguageAttributeInHttpSession <nablarch.common.web.handler.threadcontext.LanguageAttributeInHttpSession>`

タイムゾーン
 * :java:extdoc:`TimeZoneAttribute <nablarch.common.handler.threadcontext.TimeZoneAttribute>`
 * :java:extdoc:`TimeZoneAttributeInHttpCookie <nablarch.common.web.handler.threadcontext.TimeZoneAttributeInHttpCookie>`
 * :java:extdoc:`TimeZoneAttributeInHttpSession <nablarch.common.web.handler.threadcontext.TimeZoneAttributeInHttpSession>`

実行時ID
 * :java:extdoc:`ExecutionIdAttribute <nablarch.common.handler.threadcontext.ExecutionIdAttribute>`

これらのクラスは、コンポーネント定義に追加して使用する。

.. code-block:: xml

 <component class="nablarch.common.handler.threadcontext.ThreadContextHandler">
   <property name="attributes">
     <list>

       <!-- リクエストID -->
       <component class="nablarch.common.handler.threadcontext.RequestIdAttribute" />

       <!-- 内部リクエストID -->
       <component class="nablarch.common.handler.threadcontext.InternalRequestIdAttribute" />

       <!-- ユーザID -->
       <component class="nablarch.common.handler.threadcontext.UserIdAttribute">
         <property name="sessionKey"  value="user.id" />
         <property name="anonymousId" value="guest" />
       </component>

       <!-- 言語 -->
       <component class="nablarch.common.handler.threadcontext.LanguageAttribute">
         <property name="defaultLanguage" value="ja" />
       </component>

       <!-- タイムゾーン -->
       <component class="nablarch.common.handler.threadcontext.TimeZoneAttribute">
         <property name="defaultTimeZone" value="Asia/Tokyo" />
       </component>

       <!-- 実行時ID -->
       <component class="nablarch.common.handler.threadcontext.ExecutionIdAttribute" />
     </list>
   </property>
 </component>

.. _thread_context_handler-attribute_access:

スレッドコンテキストの属性値を設定/取得する
-----------------------------------------------------------
スレッドコンテキストへのアクセスは、
:java:extdoc:`ThreadContext <nablarch.core.ThreadContext>` を使用する。

.. code-block:: java

 // リクエストIDの取得
 String requestId = ThreadContext.getRequestId();

.. _thread_context_handler-language_selection:

ユーザが言語を選択する画面を作る
-----------------------------------------------------------
国際化対応などで、ユーザが言語を選択できることが求められることがある。
このような場合、以下のクラスのいずれかと
:java:extdoc:`LanguageAttributeInHttpUtil <nablarch.common.web.handler.threadcontext.LanguageAttributeInHttpUtil>`
を使うことで、ユーザの言語選択を実現できる。

* :java:extdoc:`LanguageAttributeInHttpCookie <nablarch.common.web.handler.threadcontext.LanguageAttributeInHttpCookie>`
* :java:extdoc:`LanguageAttributeInHttpSession <nablarch.common.web.handler.threadcontext.LanguageAttributeInHttpSession>`

ここでは、クッキーに言語を保持し、リンクにより言語を選択させる画面の実装例を示す。

設定例
 .. code-block:: xml

  <!-- LanguageAttributeInHttpUtilを使用するため、
       コンポーネント名を"languageAttribute"にする。-->
  <component name="languageAttribute"
             class="nablarch.common.web.handler.threadcontext.LanguageAttributeInHttpCookie">
    <property name="defaultLanguage" value="ja" />
    <property name="supportedLanguages" value="ja,en" />
  </component>

JSPの実装例
 .. code-block:: jsp

  <%-- n:submitLinkタグを使用しリンクを出力し、
       n:paramタグを使用しリンク毎に別々の言語を送信する。 --%>
  <n:submitLink uri="/action/menu/index" name="switchToEnglish">
    英語
    <n:param paramName="user.language" value="en" />
  </n:submitLink>
  <n:submitLink uri="/action/menu/index" name="switchToJapanese">
    日本語
    <n:param paramName="user.language" value="ja" />
  </n:submitLink>

ハンドラの実装例
 .. code-block:: java

  // ユーザが選択した言語の保持を行うハンドラ。
  // 複数画面でユーザに言語を選択させる場合を想定しハンドラとして実装する。
  public class I18nHandler implements HttpRequestHandler {

      public HttpResponse handle(HttpRequest request, ExecutionContext context) {
          String language = getLanguage(request, "user.language");
          if (StringUtil.hasValue(language)) {

              // LanguageAttributeInHttpUtilのkeepLanguageメソッドを呼び出し、
              // クッキーに選択された言語を設定する。
              // スレッドコンテキストにも言語が設定される。
              // 指定された言語がサポート対象の言語でない場合は、
              // クッキーとスレッドコンテキストへの設定を行わない。
              LanguageAttributeInHttpUtil.keepLanguage(request, context, language);
          }
          return context.handleNext(request);
      }

      private String getLanguage(HttpRequest request, String paramName) {
          if (!request.getParamMap().containsKey(paramName)) {
              return null;
          }
          return request.getParam(paramName)[0];
      }
  }

.. _thread_context_handler-time_zone_selection:

ユーザがタイムゾーンを選択する画面を作る
-----------------------------------------------------------
国際化対応などで、ユーザがタイムゾーンを選択できることが求められることがある。
このような場合、以下のクラスのいずれかと
:java:extdoc:`TimeZoneAttributeInHttpUtil <nablarch.common.web.handler.threadcontext.TimeZoneAttributeInHttpUtil>`
を使うことで、ユーザのタイムゾーン選択を実現できる。

* :java:extdoc:`TimeZoneAttributeInHttpCookie <nablarch.common.web.handler.threadcontext.TimeZoneAttributeInHttpCookie>`
* :java:extdoc:`TimeZoneAttributeInHttpSession <nablarch.common.web.handler.threadcontext.TimeZoneAttributeInHttpSession>`

ここでは、クッキーにタイムゾーンを保持し、リンクによりタイムゾーンを選択させる画面の実装例を示す。

設定例
 .. code-block:: xml

  <!-- TimeZoneAttributeInHttpUtilを使用するため、
       コンポーネント名を"timeZoneAttribute"にする。-->
  <component name="timeZoneAttribute"
             class="nablarch.common.web.handler.threadcontext.TimeZoneAttributeInHttpCookie">
    <property name="defaultTimeZone" value="Asia/Tokyo" />
    <property name="supportedTimeZones" value="Asia/Tokyo,America/New_York" />
  </component>

JSPの実装例
 .. code-block:: jsp

  <%-- n:submitLinkタグを使用しリンクを出力し、
       n:paramタグを使用しリンク毎に別々のタイムゾーンを送信する。 --%>
  <n:submitLink uri="/action/menu/index" name="switchToNewYork">
    ニューヨーク
    <n:param paramName="user.timeZone" value="America/New_York" />
  </n:submitLink>
  <n:submitLink uri="/action/menu/index" name="switchToTokyo">
    東京
    <n:param paramName="user.timeZone" value="Asia/Tokyo" />
  </n:submitLink>

ハンドラの実装例
 .. code-block:: java

  // ユーザが選択したタイムゾーンの保持を行うハンドラ。
  // 複数画面でユーザにタイムゾーンを選択させる場合を想定しハンドラとして実装する。
  public class I18nHandler implements HttpRequestHandler {

      public HttpResponse handle(HttpRequest request, ExecutionContext context) {
          String timeZone = getTimeZone(request, "user.timeZone");
          if (StringUtil.hasValue(timeZone)) {

              // TimeZoneAttributeInHttpUtilのkeepTimeZoneメソッドを呼び出し、
              // クッキーに選択されたタイムゾーンを設定する。
              // スレッドコンテキストにもタイムゾーンが設定される。
              // 指定されたタイムゾーンがサポート対象のタイムゾーンでない場合は、
              // クッキーとスレッドコンテキストへの設定を行わない。
              TimeZoneAttributeInHttpUtil.keepTimeZone(request, context, timeZone);
          }
          return context.handleNext(request);
      }

      private String getTimeZone(HttpRequest request, String paramName) {
          if (!request.getParamMap().containsKey(paramName)) {
              return null;
          }
          return request.getParam(paramName)[0];
      }
  }