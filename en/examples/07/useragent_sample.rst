.. _ThreadContextUserAgentSample:

------------------------------------------------------------------
Configuration Sample of UserAgent Information Acquisition Function
------------------------------------------------------------------

In this section, configuration example and specific example of values that can be obtained from various UserAgent values are shown for each use case.

.. tip::

  The patterns shown below do not cover all the patterns in each use case.
  Thoroughly examine the pattern actually used in the project.


Configuration sample of UserAgentParser
=======================================

The following is an example of the configuration that determines the browser from the UserAgent value.
In the following example, three types of browsers are classified into ``MSIE``, ``WebKit`` and ``Gecko``.

.. code-block:: xml

   <!-- Configuration of UserAgentParser -->
   <component name="userAgentParser" class="please.change.me.fw.web.useragent.UserAgentParser">
     <!-- OS pattern mapping configuration
          The OS is not determined in this example, and various properties are not configured. -->
     <property name="osSetting">
       <component class="please.change.me.fw.web.useragent.UserAgentPatternSetting"/>
     </property>
   
     <!-- Browser pattern mapping settings -->
     <property name="browserSetting">
       <component class="please.change.me.fw.web.useragent.UserAgentPatternSetting">
         <!--  -->
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
           <!-- Describes as many patterns as necessary that can be used to determine the user agent to be identified -->
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
 Since typePatternList and itemPatternList are used in the order they are written, they must be written carefully in order.
 For example, if the pattern ``".*Gecko.*"`` is placed at the beginning, Chrome and IE11 will also be determined as Gecko.
 (because the user agent value contains the string ``Gecko``)
 
            
            


Examples of values that can be obtained from various UserAgent values
-------------------------------------------------------------------------

.. list-table::
  :widths: 50 10 10 10
  :header-rows: 1

  * - UserAgent
    - Browser type
    - Browser name
    - Browser version
  
  * - ``Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)``
    - MSIE
    - ie
    - 10.0
  
  * - ``Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36``
    - WebKit
    - chrome
    - 34.0.1847.116
  

The OS can also be determined by making the same configuration.
For specific examples, see the component configuration file attached to the sample project.


Configuration sample of UserAgentValueConvertor implementation class
========================================================================

In the following example, a converter is configured to convert the version number that matches the pattern of IE.

For example, for a user agent called ``Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko`` matches the version number.
``11.0`` matches the version number. This version number is converted to ``_11 __0 ___``
by ``UserAgentValueConvertor``.


.. code-block:: xml

  <!-- UserAgent converter configuration -->
  <component name="browserVersionConvertor" class="please.change.me.fw.web.useragent.UserAgentVersionConvertor">
    <property name="padding" value="_" />
  </component>
  
   <!-- Configuration of UserAgentParser -->
   <component name="userAgentParser" class="please.change.me.fw.web.useragent.UserAgentParser">
     <!-- Middle is omitted -->   
     <!-- Browser pattern mapping settings -->
     <property name="browserSetting">
       <component class="please.change.me.fw.web.useragent.UserAgentPatternSetting">
         <!-- Middle is omitted -->   
         <property name="itemPatternList">
           <list>
             <component class="please.change.me.fw.web.useragent.ItemPattern">
               <property name="name"             value="ie" />
               <property name="pattern"          value="(?i).*(msie\s|trident.+rv:)([\d\.]*).*" />
               <property name="versionIndex"     value="2" />
               <!-- Specify a converter that converts the version number string matching the pattern.-->
               <property name="versionConvertor" ref="browserVersionConvertor" />
             </component>
           <!-- Middle is omitted -->   
           </list>
         </property>
       </component>
     </property>
   </component>
 </component-configuration>

An example when the browser type is specified
==================================================

An example of extracting the browser type and performing processes for each type is shown below.

**Implementation examples**

.. code-block:: java

  public HttpResponse handle(HttpRequest request, ExecutionContext context) {
      // Branch the process according to the browser type
      UserAgent userAgent = request.getUserAgent();
      String browserType = userAgent.getBrowserType();      
      if browserType.equals("MSIE")) {
          ... // Process for "MSIE"
    
      } else if (browserType.equals("WebKit")) {
          ... // Process for "WebKit"
    
      } else if (browserType.equals("Gecko")) {
          ... // Process for "Gecko"
      }
  }


An example of using the obtained information in subsequent processes
======================================================================

An example of extracting the OS (device) and browser name and version information from UserAgent,
setting it in the request scope variable and using it in the JSP is shown below.

**Implementation examples**

.. code-block:: java

  public HttpResponse handle(HttpRequest request, ExecutionContext context) {
      // Configure the OS name and browser name in the request scope variable
      UserAgent userAgent = request.getUserAgent();
      
      context.setRequestScopedVar("deviceName",     userAgent.getOsName());
      context.setRequestScopedVar("deviceVersion",  userAgent.getOsVersion());
      context.setRequestScopedVar("browserName",    userAgent.getBrowserName());
      context.setRequestScopedVar("browserVersion", userAgent.getBrowserVersion());
  }



Examples of values that can be obtained from various UserAgent values
==========================================================================

An example of values that can be obtained when using the component configuration file
attached to the sample project is shown below.


.. list-table::
  :widths: 60 10 10 10 10
  :header-rows: 1

  * - UserAgent
    - Device name
    - Device version
    - Browser name
    - Browser version
  
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

  

When implementing an any analysis/parser class
===============================================

An example of implementing and using an any analysis/parser class is shown below.

**Configuration example**

.. code-block:: xml
 
 <!-- Configuration of UserAgentParser -->
 <component name="userAgentParser" class="please.change.me.common.web.useragent.CustomUserAgentParser">
   <!-- Configuration is the same as for RegexUserAgentParser-->
 </component>

**Implementation examples**

CustomUserAgent inherits UserAgent and adds the following determination method.

* isTablet()
* isSmartPhone()
* isFeaturePhone()

.. code-block:: java

 public class CustomUserAgent extends UserAgent {

     /** Is it a tablet? */
     private boolean isTablet;
  
     /** Is it a smartphone?  */
     private boolean isSmartPhone;
  
     /** Is it a feature phone? */
     private boolean isFeaturePhone;
  
     /**
      * Constructor
      *
      * @param original Parsing results of default parser
      */
     public CustomUserAgent(UserAgent original) {
         super(original);
     }
      
      // Getter and setter methods are omitted }
  }

The CustomUserAgentParser also inherits the RegexUserAgentParser and returns the CustomUserAgent using the parse method.

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
       * Determine if it is a tablet.
       *
       * @param userAgent Parsed {@link UserAgent}
       * @return In the case of tablet, true
       */
      private boolean isTablet(UserAgent userAgent) {
          // Determine by OS name and OS type
          String osName = userAgent.getOsName();
          if (osName.equals("ipad")) {
              return true;
   
          }
          return osName.equals("android") && userAgent.getOsType().equals("tablet");
      }
   
      /**
       * Determine if it is a smartphone.
       *
       * @param userAgent Parsed {@link UserAgent}
       * @return In the case of a smartphone, true
       */
      private boolean isSmartPhone(UserAgent userAgent) {
          // Determine by OS name and OS type
          String osName = userAgent.getOsName();
          if (osName.equals("iphone")) {
              return true;
          }
          return osName.equals("android") && userAgent.getOsType().equals("mobilePhone");
      }
   
      /**
       * Determine if it is a feature phone.
       *
       * @param userAgent Parsed {@link UserAgent}
       * @return In the case of a feature phone, true
       */
      private boolean isFeaturePhone(UserAgent userAgent) {
   
          // When it is not a tablet or a smartphone and it includes the name of the carrier
          if (isTablet(userAgent)) {
              return false;
          }
          if (isSmartPhone(userAgent)) {
              return false;
          }
          // Determine whether a carrier name is included in the UserAgent string
          String uaText = userAgent.getText();
          return uaText.contains("DoCoMo")
                  || uaText.contains("kddi")
                  || uaText.contains("vodafone");
      }
  }

Use as follows in the action class:

.. code-block:: java

 public HttpResponse doUserAgentJudgment(HttpRequest req, ExecutionContext context) {
 
     CustomUserAgent userAgent = req.getUserAgent();
     
     if (userAgent.isTablet()) {
         ... // Process when the client is a Tablet
     } else if (userAgent.isSmartPhone()) {
         ... // Process when the client is a smartphone
     }
 }

**Examples of values that can be obtained from various UserAgent values**

.. list-table::
  :widths: 60 10 10 10 10
  :header-rows: 1

  * - UserAgent
    - isTablet
    - isSmartPhone
    - isFeaturePhone
    - Remarks
  
  * - ``Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)``
    - false
    - false
    - false
    - PC
  
  * - ``Mozilla/5.0 (Linux; U; Android 3.2; ja-jp; SC-01D Build/MASTER) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13``
    - true
    - false
    - false
    - Tablet
  
  * - ``Mozilla/5.0 (Linux; U; Android 2.3.3; ja-jp; SC-02C Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1``
    - false
    - true
    - false
    - Smart phone
  
  * - ``DoCoMo/2.0 N2001(c10)``
    - false
    - false
    - true
    - Feature phone
  
  
