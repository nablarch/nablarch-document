====================================================
How to Incorporate the CAPTCHA Function
====================================================

Configure dependent libraries
===================================

Add the definition of the dependent libraries to pom.xml of the web project where the CAPTCHA feature is to be included.

  .. code-block:: xml

    <dependency>
      <groupId>com.github.axet</groupId>
      <artifactId>kaptcha</artifactId>
      <version>0.0.9</version>
    </dependency>

Create table
===================================

Create a table to be used by the CAPTCHA function. (Example for Oracle is given below)

Match the number of digits required for CAPTCHA_TEXT with the value configured in "kaptcha.textproducer.char.length" described later.

  .. code-block:: xml

    CREATE TABLE CAPTCHA_MANAGE (
      CAPTCHA_KEY  VARCHAR2(36) NOT NULL,
      CAPTCHA_TEXT VARCHAR2(4),
      GENERATE_DATE_TIME TIMESTAMP(6) NOT NULL,
      CONSTRAINT PK_CAPTCHA_MANAGE PRIMARY KEY (CAPTCHA_KEY)
    );

Placement of source code for the CAPTCHA function
=========================================================

Place the source code under the following directory in the web project where the CAPTCHA function will be incorporated.

Modify the package name of the package and import statements in the source code according to the destination package.

  `nablarch-biz-sample-all/src/main/java/please/change/me/common/captcha <https://github.com/nablarch/nablarch-biz-sample-all/tree/master/src/main/java/please/change/me/common/captcha>`_


Add the component definition
===================================

(development environment definition file) src/env/dev/resources/{project package}/handler_dev.xml

(production environment definition file) src/main/resources/{project package}/web-component-configuration.xml

The class attribute value in the captchaGenerator definition should match the package in which the captchaGenerator class is located.

  .. code-block:: xml

    <!-- Configuration 1: Component definition of CaptchaGenerator -->
    <component name="captchaGenerator" 
        class="com.nablarch.example.app.web.common.captcha.CaptchaGenerator">
        <property name="imageType" value="jpg"/>
        <property name="configParameters">
          <map>
            <entry key="kaptcha.textproducer.char.string" value="abcdegfynmnpwx" />
            <entry key="kaptcha.textproducer.char.length" value="4" />
          </map>
        </property>
        -->
    </component>


Match the class attribute value of the component definition of captchaGenerateHandler with the package in which the CaptchaGenerateHandler class is placed.

  .. code-block:: xml

    <!-- Configuration 2: Component definition for CaptchaGenerateHandler -->
    <component name="captchaGenerateHandler" 
        class="com.nablarch.example.app.web.common.captcha.CaptchaGenerateHandler"/>


The URL configured in the requestPattern given below must be a URL that does not have a corresponding action class or form class entity.

However, it must match the src attribute of the <img> tag in JSP used to request a Captcha image.

Configuration of the RequestHandlerEntry must be defined after the configuration of the dbConnectionManagementHandler and transactionManagementHandler.

  .. code-block:: xml

    <!-- Configuration 3: Associate a request URL for Captcha image generation and acquisition with a handler for generation and sending of images -->
    <component class="nablarch.fw.RequestHandlerEntry">
            <property name="requestPattern" value="/action/path/to/hoge"/>
            <property name="handler" ref="captchaGenerateHandler"/>
    </component>

Edit Action
===================================

Adds a process to generate a captcha identifier and enable a JSP refer to the generated value of the action method corresponding to a JSP for displaying images that is used with a captcha authentication.

  .. code-block:: java
  
    public HttpResponse method1(HttpRequest request, ExecutionContext context) {
       XxxForm form = new XxxForm();
       form.setCaptchaKey(CaptchaUtil.generateKey()); // Captcha identifier numbering
       context.setRequestScopedVar("form", form);     // Configuring the request scope
       return new HttpResponse("/WEB-INF/view/xxx/xxx.jsp");
    }

Confirm that the method of action called when validating the value entered by the user is configured to be associated with the validation method defined in the form.

  .. code-block:: java
  
    @InjectForm(form = XxxForm.class, prefix = "form", validate = "yyyy")
    public HttpResponse method2(HttpRequest request, ExecutionContext context) {
        // Omitted
    }

Edit Form
===================================

A property and an accessor are added, to retain the information used during the captcha authentication, to the form.

  .. code-block:: java

    private String captchaKey;

    private String captchaValue;

    // Accessor is omitted

Add a method for validation.

  .. code-block:: java

    @ValidateFor("yyyy")

    public static void validateForXxx(ValidationContext<LoginForm> context) {

        // Single item validation

        ValidationUtil.validate(context, new String[] { /*…Middle is omitted…*/, "captchaKey", "captchaValue" });
        if (!context.isValid()) {
            return;
        }
        
        // Captcha string determination

        XxxForm form = context.createObject();
        if (!CaptchaUtil.authenticate(form.getCaptchaKey(), form.getCaptchaValue())) {
            context.addResultMessage("captchaValue", "MSG90001");
        }
    }

Edit jsp
===================================

The following code is added to the JSP corresponding to the screen in which the captcha authentication function is incorporated.

  .. code-block:: jsp

    <%-- Attribute values of n:form are omitted. --%>

    <n:form>
    
      <%--  Omitted  --%>
    
      <%-- Addition of tags for acquisition of captcha image  --%>

      <n:img src="/action/path/to/hoge?captchaKey=${form.captchaKey}" alt=""/>

      <%--  Addition of tags for sending information necessary for captcha authentication  --%>

      <n:plainHidden name="form.captchaKey"></n:plainHidden>
      <n:text name="form.captchaValue" />

    <%-- Omitted  --%>

    </n:form>

