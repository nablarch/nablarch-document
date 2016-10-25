.. _ThreadContextUserAgentSample:

---------------------------------
UserAgent情報取得機能設定サンプル
---------------------------------

本節では利用ケースごとに、設定例と各種UserAgent値から取得できる値の具体例を示す。

.. tip::

  以下に示すパターンは各利用ケースにおける全てのパターンを網羅しているわけではない。
  利用プロジェクトにて実際に利用するパターンを十分に検討すること。


UserAgentParserの設定サンプル
=============================

UserAgent値からブラウザの判定を行う設定例を以下に示す。
以下の例では、ブラウザの種類を\ ``MSIE``\ 、\ ``WebKit``\ 、\ ``Gecko``\ の3種類に分別している。

.. code-block:: xml

   <!-- UserAgentParserの設定 -->
   <component name="userAgentParser" class="please.change.me.fw.web.useragent.UserAgentParser">
     <!-- OSのパターンマッピング設定
          この例ではOSの判定を行わないので各種プロパティを設定しない。 -->
     <property name="osSetting">
       <component class="please.change.me.fw.web.useragent.UserAgentPatternSetting"/>
     </property>
   
     <!-- ブラウザのパターンマッピング設定 -->
     <property name="browserSetting">
       <component class="please.change.me.fw.web.useragent.UserAgentPatternSetting">
         <!-- ブラウザの種類をMSIE、WebKit、Geckoの3種類に分別 -->
         <property name="typePatternList">
           <list>
             <component class="please.change.me.fw.web.useragent.TypePattern">
               <property name="name"    value="MSIE" />
               <property name="pattern" value=".*MSIE.*" />
             </component>
             <component class="please.change.me.fw.web.useragent.TypePattern">
               <property name="name"    value="MSIE" />
               <property name="pattern" value=".*Trident.+rv:[\d\.]+.*"/>
             </component>
             <component class="please.change.me.fw.web.useragent.TypePattern">
               <property name="name"    value="WebKit" />
               <property name="pattern" value=".*WebKit.*" />
             </component>
             <component class="please.change.me.fw.web.useragent.TypePattern">
               <property name="name"    value="Gecko" />
               <property name="pattern" value=".*Gecko.*" />
             </component>
           </list>
         </property>
         <property name="itemPatternList">
           <!-- 識別対象としたいユーザエージェントを判定できるパターンを必要なだけ記述する -->
           <list>
             <component class="please.change.me.fw.web.useragent.ItemPattern">
               <property name="name"             value="ie" />
               <property name="pattern"          value="(?i).*(msie\s|trident.+rv:)([\d\.]*).*" />
               <property name="versionIndex"     value="2" />
             </component>
             <component class="please.change.me.fw.web.useragent.ItemPattern">
               <property name="name"             value="android_browser" />
               <property name="pattern"          value="(?i).*android.*version/([\d\.]*).+(mobile *?safari).*" />
               <property name="versionIndex"     value="1" />
             </component>
             <component class="please.change.me.fw.web.useragent.ItemPattern">
               <property name="name"             value="mobile_safari" />
               <property name="pattern"          value="(?i).*version/([\d\.]*).+(mobile.*safari).*" />
               <property name="versionIndex"     value="1" />
             </component>
             <component class="please.change.me.fw.web.useragent.ItemPattern">
               <property name="name"             value="firefox_chrome" />
               <property name="pattern"          value="(?i).*(firefox|chrome)[\s/]*([\d\.]*).*" />
               <property name="nameIndex"        value="1" />
               <property name="versionIndex"     value="2" />
             </component>
             <component class="please.change.me.fw.web.useragent.ItemPattern">
               <property name="name"             value="safari" />
               <property name="pattern"          value="(?i).*version/([\d\.]*).+(safari).*" />
               <property name="versionIndex"     value="1" />
             </component>
           </list>
         </property>
       </component>
     </property>
   </component>


.. tip::
 typePatternList、itemPatternListは、記述された順番に使用されるので、 順番に注意して記述すること。
 例えば、 パターン\ ``".*Gecko.*"``\を先頭に配置してしまうと、ChromeやIE11もGeckoと判定されてしまう。
 (ユーザエージェント値に\ ``Gecko``\ という文字列が含まれているため)
 
            
            


各種ユーザエージェント値から取得できる値の例
--------------------------------------------

.. list-table::
  :widths: 50 10 10 10
  :header-rows: 1

  * - UserAgent
    - ブラウザ種別
    - ブラウザ名
    - ブラウザバージョン
  
  * - ``Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)``
    - MSIE
    - ie
    - 10.0
  
  * - ``Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36``
    - WebKit
    - chrome
    - 34.0.1847.116
  

OSの判定についても、同様に設定することで判定が可能となる。
具体例については、サンプルプロジェクト付属のコンポーネント定義ファイルを参照。


UserAgentValueConvertor実装クラスの設定サンプル
===============================================

以下の例では、IEのパターンにマッチしたバージョン番号を変換するコンバータを設定している。

例えば、\ ``Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko``\ というユーザエージェントの場合、
\ ``11.0``\ がバージョン番号としてマッチする。そのバージョン番号が\ ``UserAgentValueConvertor``\ によって
``_11 __0 ___``\ に変換される。


.. code-block:: xml

  <!-- UserAgent用コンバータの設定 -->
  <component name="browserVersionConvertor" class="please.change.me.fw.web.useragent.UserAgentVersionConvertor">
    <property name="padding" value="_" />
  </component>
  
   <!-- UserAgentParserの設定 -->
   <component name="userAgentParser" class="please.change.me.fw.web.useragent.UserAgentParser">
     <!-- 中略 -->   
     <!-- ブラウザのパターンマッピング設定 -->
     <property name="browserSetting">
       <component class="please.change.me.fw.web.useragent.UserAgentPatternSetting">
         <!-- 中略 -->   
         <property name="itemPatternList">
           <list>
             <component class="please.change.me.fw.web.useragent.ItemPattern">
               <property name="name"             value="ie" />
               <property name="pattern"          value="(?i).*(msie\s|trident.+rv:)([\d\.]*).*" />
               <property name="versionIndex"     value="2" />
               <!-- パターンにマッチしたバージョン番号文字列を変換するコンバータを指定する。-->
               <property name="versionConvertor" ref="browserVersionConvertor" />
             </component>
           <!-- 中略 -->   
           </list>
         </property>
       </component>
     </property>
   </component>
 </component-configuration>

ブラウザの種別を特定する場合の例
================================

ブラウザの種別を抽出し、種別毎の処理を行う例を以下に示す。

**実装例**

.. code-block:: java

  public HttpResponse handle(HttpRequest request, ExecutionContext context) {
      // ブラウザ種別により、処理を分岐する
      UserAgent userAgent = request.getUserAgent();
      String browserType = userAgent.getBrowserType();      
      if browserType.equals("MSIE")) {
          ... // "MSIE"の場合の処理
    
      } else if (browserType.equals("WebKit")) {
          ... // "WebKit"の場合の処理
    
      } else if (browserType.equals("Gecko")) {
          ... // "Gecko"の場合の処理
      }
  }


取得した情報を後続処理で使用する場合の例
========================================

UserAgentからOS(デバイス)やブラウザの名称およびバージョン情報を抽出し、\
リクエストスコープ変数に設定してJSPの中で利用する例を以下に示す。

**実装例**

.. code-block:: java

  public HttpResponse handle(HttpRequest request, ExecutionContext context) {
      // OS名、ブラウザ名をリクエストスコープ変数に設定する
      UserAgent userAgent = request.getUserAgent();
      
      context.setRequestScopedVar("deviceName",     userAgent.getOsName());
      context.setRequestScopedVar("deviceVersion",  userAgent.getOsVersion());
      context.setRequestScopedVar("browserName",    userAgent.getBrowserName());
      context.setRequestScopedVar("browserVersion", userAgent.getBrowserVersion());
  }



各種ユーザエージェント値から取得できる値の例
============================================

サンプルプロジェクト付属のコンポーネント定義ファイルを使用した場合に、
取得できる値の例を以下に示す。


.. list-table::
  :widths: 60 10 10 10 10
  :header-rows: 1

  * - UserAgent
    - デバイス名
    - デバイスバージョン
    - ブラウザ名
    - ブラウザバージョン
  
  * - ``Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko``
    - windows
    - -6 --1 ---
    - ie
    - _11 __0 ___
  
  * - ``Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:28.0) Gecko/20100101 Firefox/28.0``
    - mac_os_x
    - -10 --9 ---
    - firefox
    - _28 __0 ___
  
  * - ``Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36``
    - windows
    - -6 --1 ---
    - chrome
    - _34 __0 ___1847
  
  * - ``Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A403 Safari/8536.25``
    - iphone
    - -6 --0 ---
    - mobile_safari
    - _6 __0 ___
  
  * - ``Mozilla/5.0 (iPad; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/8536.25``
    - ipad
    - -6 --0 ---
    - mobile_safari
    - _7 __0 ___
  
  * - ``Mozilla/5.0 (Linux; Android 4.2.2; HTC One Build/JDQ39) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.30 Mobile Safari/537.36``
    - android
    - -4 --2 ---2
    - chrome
    - _30 __0 ___1599
  
  * - ``Mozilla/5.0 (Linux; U; Android 4.3;ja-jp;SC-03E Build/JSS15J) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30``
    - android
    - -4 --3 ---
    - android_browser
    - _4 __0 ___

  

任意の解析クラスを実装する場合
==============================

任意の解析クラスを実装し、利用する例を以下に示す。

**設定例**

.. code-block:: xml
 
 <!-- UserAgentParserの設定 -->
 <component name="userAgentParser" class="please.change.me.common.web.useragent.CustomUserAgentParser">
   <!-- 設定内容はRegexUserAgentParserと同じ -->
 </component>

**実装例**

CustomUserAgentはUserAgentを継承し、以下の判定メソッドを追加することとする。

* isTablet()
* isSmartPhone()
* isFeaturePhone()

.. code-block:: java

 public class CustomUserAgent extends UserAgent {

     /** タブレットであるか */
     private boolean isTablet;
  
     /** スマートフォンであるか */
     private boolean isSmartPhone;
  
     /** フィーチャーフォンであるか */
     private boolean isFeaturePhone;
  
     /**
      * コンストラクタ
      *
      * @param original デフォルトパーサの解析結果
      */
     public CustomUserAgent(UserAgent original) {
         super(original);
     }
      
      // getter, setter メソッドは省略
  }

また、CustomUserAgentParserはRegexUserAgentParserを継承し、parseメソッドでCustomUserAgentを返却する。

.. code-block:: java

  public class CustomUserAgentParser extends RegexUserAgentParser {
  
      /** {@inheritDoc} */
      @Override
      public CustomUserAgent parse(String userAgentText) {
          UserAgent userAgent = super.parse(userAgentText);
          CustomUserAgent custom = new CustomUserAgent(userAgent);
          custom.setTablet(isTablet(userAgent));
          custom.setSmartPhone(isSmartPhone(userAgent));
          custom.setFeaturePhone(isFeaturePhone(userAgent));
          return custom;
      }

      /**
       * タブレットであるかを判定する。
       *
       * @param userAgent 解析済みの{@link UserAgent}
       * @return タブレットの場合、真
       */
      private boolean isTablet(UserAgent userAgent) {
          // OS名およびOSタイプにより判定する
          String osName = userAgent.getOsName();
          if (osName.equals("ipad")) {
              return true;
   
          }
          return osName.equals("android") && userAgent.getOsType().equals("tablet");
      }
   
      /**
       * スマートフォンであるかを判定する。
       *
       * @param userAgent 解析済みの{@link UserAgent}
       * @return スマートフォンの場合、真
       */
      private boolean isSmartPhone(UserAgent userAgent) {
          // OS名およびOSタイプにより判定する
          String osName = userAgent.getOsName();
          if (osName.equals("iphone")) {
              return true;
          }
          return osName.equals("android") && userAgent.getOsType().equals("mobilePhone");
      }
   
      /**
       * フィーチャーフォンであるかを判定する。
       *
       * @param userAgent 解析済みの{@link UserAgent}
       * @return フィーチャーフォンの場合、真
       */
      private boolean isFeaturePhone(UserAgent userAgent) {
   
          // タブレットでもスマートフォンでもなく、キャリア名が含まれる場合
          if (isTablet(userAgent)) {
              return false;
          }
          if (isSmartPhone(userAgent)) {
              return false;
          }
          // UserAgent文字列にキャリア名が含まれるか否かで判定する
          String uaText = userAgent.getText();
          return uaText.contains("DoCoMo")
                  || uaText.contains("kddi")
                  || uaText.contains("vodafone");
      }
  }

アクションクラスでは以下のように利用する。

.. code-block:: java

 public HttpResponse doUserAgentJudgment(HttpRequest req, ExecutionContext context) {
 
     CustomUserAgent userAgent = req.getUserAgent();
     
     if (userAgent.isTablet()) {
         ... // クライアントがタブレットの場合に行う処理
     } else if (userAgent.isSmartPhone()) {
         ... // クライアントがスマートフォンの場合に行う処理
     }
 }

**各種UserAgent値から取得できる値の例**

.. list-table::
  :widths: 60 10 10 10 10
  :header-rows: 1

  * - UserAgent
    - isTablet
    - isSmartPhone
    - isFeaturePhone
    - 備考
  
  * - ``Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)``
    - false
    - false
    - false
    - PC
  
  * - ``Mozilla/5.0 (Linux; U; Android 3.2; ja-jp; SC-01D Build/MASTER) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13``
    - true
    - false
    - false
    - タブレット
  
  * - ``Mozilla/5.0 (Linux; U; Android 2.3.3; ja-jp; SC-02C Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1``
    - false
    - true
    - false
    - スマートフォン
  
  * - ``DoCoMo/2.0 N2001(c10)``
    - false
    - false
    - true
    - フィーチャーフォン
  
  
