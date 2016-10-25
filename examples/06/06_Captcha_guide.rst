====================================================
CAPTCHA機能の組み込み手順
====================================================

依存ライブラリの設定
===================================

CAPTCHA機能を組み込む先のウェブプロジェクトのpom.xmlに、依存ライブラリの定義を追記してください。

  .. code-block:: xml

    <dependency>
      <groupId>com.github.axet</groupId>
      <artifactId>kaptcha</artifactId>
      <version>0.0.9</version>
    </dependency>

テーブルの作成
===================================

CAPTCHA機能が使用するテーブルを作成してください。(下例はOracleの場合)

CAPTCHA_TEXTに必要な桁数は、後述の「kaptcha.textproducer.char.length」で設定した値に合わせてください。

  .. code-block:: xml

    CREATE TABLE CAPTCHA_MANAGE (
      CAPTCHA_KEY  VARCHAR2(36) NOT NULL,
      CAPTCHA_TEXT VARCHAR2(4),
      GENERATE_DATE_TIME TIMESTAMP(6) NOT NULL,
      CONSTRAINT PK_CAPTCHA_MANAGE PRIMARY KEY (CAPTCHA_KEY)
    );

CAPTCHA機能のソースコードの配置
===================================

下記ディレクトリ配下のソースコードを、CAPTCHA機能を組み込む先のウェブプロジェクトに配置してください。

ソースコードのpackage文、import文のパッケージ名は、配置先のパッケージに合わせて修正してください。

  `nablarch-biz-sample-all/main/java/please/change/me/common/captcha <https://github.com/nablarch/nablarch-biz-sample-all/tree/master/main/java/please/change/me/common/captcha>`_


コンポーネント定義の追記
===================================

(開発環境用定義ファイル) src/env/dev/resources/{プロジェクトのパッケージ}/handler_dev.xml

(本番環境用定義ファイル) src/main/resources/{プロジェクトのパッケージ}/web-component-configuration.xml

captchaGeneratorの定義のclass属性の値は、CaptchaGeneratorクラスを配置したパッケージに合わせてください。

  .. code-block:: xml

    <!-- 設定１：CaptchaGeneratorのコンポーネント定義 -->
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


captchaGenerateHandlerのコンポーネント定義のclass属性の値も、
CaptchaGenerateHandlerクラスを配置したパッケージに合わせてください。

  .. code-block:: xml

    <!-- 設定２：CaptchaGenerateHandlerのコンポーネント定義 -->
    <component name="captchaGenerateHandler" 
        class="com.nablarch.example.app.web.common.captcha.CaptchaGenerateHandler"/>


下記のrequestPatternに設定するＵＲＬについては、対応するActionクラスやFormクラスの実体が存在しないＵＲＬを指定します。

ただし、Captcha画像をリクエストするためのＪＳＰ内の<img>タグのsrc属性とは揃っている必要があります。

RequestHandlerEntryの設定は、dbConnectionManagementHandler、transactionManagementHandler の設定よりも後に定義する必要があります。

  .. code-block:: xml

    <!-- 設定３： Captcha画像の生成・取得のためのリクエストＵＲＬと画像生成・送信を実行するハンドラを関連付ける -->
    <component class="nablarch.fw.RequestHandlerEntry">
            <property name="requestPattern" value="/action/path/to/hoge"/>
            <property name="handler" ref="captchaGenerateHandler"/>
    </component>

Actionの編集
===================================

Captcha認証用の画像を表示するためのJSPに対応する、Actionのメソッドに、
Captcha識別子の生成、および、生成した値をJSPが参照できるようにするための処理を追加します。

  .. code-block:: java
  
    public HttpResponse method1(HttpRequest request, ExecutionContext context) {
       XxxForm form = new XxxForm();
       form.setCaptchaKey(CaptchaUtil.generateKey()); // Captcha識別子の採番
       context.setRequestScopedVar("form", form);     // リクエストスコープへの設定
       return new HttpResponse("/WEB-INF/view/xxx/xxx.jsp");
    }

ユーザーが入力した値をバリデーションするタイミングで呼び出されるActionのメソッドに、
Formに定義するバリデーション用のメソッドとの関連付けが設定されていることを確認します。

  .. code-block:: java
  
    @InjectForm(form = XxxForm.class, prefix = "form", validate = "yyyy")
    public HttpResponse method2(HttpRequest request, ExecutionContext context) {
        // 中略
    }

Formの編集
===================================

Captcha認証時に使用する情報を保持するためのプロパティおよびアクセッサをFormに追加します。

  .. code-block:: java

    private String captchaKey;

    private String captchaValue;

    // アクセッサは省略

バリデーション用のメソッドを追加します。

  .. code-block:: java

    @ValidateFor("yyyy")
    public static void validateForXxx(ValidationContext<LoginForm> context) {

        // 単項目精査
        ValidationUtil.validate(context, new String[] { …中略…, "captchaKey", "captchaValue" });
        if (!context.isValid()) {
            return;
        }
        
        // Captcha文字列判定
        XxxForm form = context.createObject();
        if (!CaptchaUtil.authenticate(form.getCaptchaKey(), form.getCaptchaValue())) {
            context.addResultMessage("captchaValue", "MSG90001");
        }
    }

jspの編集
===================================

Captcha認証機能を組み込む画面に対応するJSPに下記のコードを追加します。

  .. code-block:: xml

    <n:form …省略…>
    
    // 中略
    
    // Captcha認証用画像を取得するためのタグを追加
    <n:img src="/action/path/to/hoge?captchaKey=${form.captchaKey}" alt=""/>

    // Captcha認証時に必要な情報を送信するためのタグを追加
    <n:plainHidden name="form.captchaKey"></n:plainHidden>
    <n:text name="form.captchaValue" />

    // 中略
    </n:form>

