.. _`role_check`:

アノテーションによる認可チェック
=====================================================================

.. contents:: 目次
  :depth: 3
  :local:

この機能は、 :doc:`permission_check` と同様にアプリケーションが提供する機能に対して認可チェックを行う。


機能概要
---------------------------------------------------------------------

煩雑なデータ管理をせずに認可チェックができる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: images/role_check/conceptual_model.jpg

アノテーションによる認可チェックでは、ユーザに対してロール(役割)を割り当てる。
また、認可チェックを行いたい機能に対しても、その機能を実行するのに必要なロールを割り当てる。
そして、現在のユーザが実行対象の機能に割り当てられたロールを有するかどうかで、認可の判定を行う。

機能とロールの割り当ては、基本的にアノテーションを用いてJavaのプログラム上で行う。
また、ユーザとロールの割り当てについては、フレームワークでは特に方法を規定しておらず自由な方法を選択できるようにしている。

このようにアノテーションによる認可チェックでは、 :doc:`permission_check` よりも単純なデータ構造で権限を管理できるようになっている。


アノテーションで認可チェックができる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: java

  @CheckRole("ADMIN")
  public HttpResponse index(HttpRequest request, ExecutionContext context) {

アノテーションによる認可チェックでは、アクションクラスのメソッドに対してアノテーションを使ってロールを割り当てることができる。
上記例では、 ``index`` メソッドを実行するために ``ADMIN`` ロールが必要であることを定義している。


ハンドラによる認可チェックとの使い分け
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

本認可チェックと :doc:`permission_check` を使い分ける基準について説明する。

アノテーションによる認可チェックは、前述のとおりロール単位で権限を管理する。
また、ロールと機能の割り当てはJavaのアノテーションで行う仕組みとなっている。
したがって、本認可チェックを用いることが適しているのは、ロール自体の増減やロールに割り当てる機能の変更が頻繁に発生しない場合となる。

例えば、権限管理が必要なロールの種類と機能の組み合わせが決まっており今後それらが大きく変化する予定がない場合は、本認可チェックを用いることで簡単に認可チェックを実現できる。

一方で、ユーザが所属する部署によって権限を制御したいようなシステムでは、組織変更で部署の構成や利用できる機能の組み合わせも大きく変わることが予想される。このようなシステムで本認可チェックを用いると、変更のたびにアノテーションの書き換えが必要になり大きな修正工数が必要となる。
このようなシステムでは、 :doc:`permission_check` を用いて権限の組み合わせをデータで管理することを推奨する。


モジュール一覧
---------------------------------------------------------------------

.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-auth</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-auth-session</artifactId>
  </dependency>
  <!-- デフォルトコンフィグレーションを利用する場合 -->
  <dependency>
    <groupId>com.nablarch.configuration</groupId>
    <artifactId>nablarch-main-default-configuration</artifactId>
  </dependency>


使用方法
---------------------------------------------------------------------

事前準備
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

コンポーネントを定義する
*********************************************************************

.. code-block:: xml

  <component name="roleEvaluator"
             class="nablarch.common.authorization.role.BasicRoleEvaluator">
      <property name="userRoleResolver" ref="userRoleResolver" />
  </component>

  <component name="userRoleResolver"
             class="nablarch.common.authorization.role.session.SessionStoreUserRoleResolver" />

アノテーションによる認可チェックを使用するためには、まず :java:extdoc:`BasicRoleEvaluator <nablarch.common.authorization.role.BasicRoleEvaluator>` のコンポーネントを定義する。
また、このとき ``userRoleResolver`` プロパティには :java:extdoc:`SessionStoreUserRoleResolver <nablarch.common.authorization.role.session.SessionStoreUserRoleResolver>` を設定する。

なお、この設定はデフォルトコンフィグレーションとしても提供している。
デフォルトコンフィグレーションを使う場合は、以下のようにファイルをインポートすることで同様の設定となる。

.. code-block:: xml

  <import file="nablarch/common/authorization/role/session/authorization-session.xml" />

interceptorsOrderに追加する
*********************************************************************

アノテーションによるチェックは、Nablarchの :java:extdoc:`インターセプタ <nablarch.fw.Interceptor>` の仕組みを用いて実現している。
したがって、既にコンポーネント定義にて ``interceptorsOrder`` を定義している場合は、 :java:extdoc:`CheckRole <nablarch.common.authorization.role.CheckRole>` を追加する必要がある。

.. code-block:: xml

  <!-- インターセプタの実行順定義 -->
  <list name="interceptorsOrder">
    <!-- CheckRole を追加する -->
    <value>nablarch.common.authorization.role.CheckRole</value>
    <!-- 他のインターセプターの記述は省略 -->
  </list>


``interceptorsOrder`` を定義していない場合は、この対応は不要である。

また、デフォルトコンフィグレーションの ``nablarch/webui/interceptors.xml`` を読み込んでいる場合も特に対応は必要ない。


ロールを定義する
*********************************************************************

.. code-block:: java

  public class Roles {
      /** システム管理者のロール。 */
      public static final String ROLE_ADMIN = "ADMIN";
      /** プロジェクト管理者のロール。 */
      public static final String ROLE_PROJECT_MANAGER = "PROJECT_MANAGER";
  }

アノテーションなどで指定するロールを定義する。

ロールは任意の文字列として定義する。
システムで扱えるのであれば文字種やフォーマットに制限はないが、管理しやすいように何のロールか理解しやすい値にすることを推奨する。

また、アノテーションで指定する際は定数ではなく文字列リテラルを直接指定することも可能だが、修正が容易になるように定数で管理することを推奨する。
なお、上記例では専用の定数クラスを用意しているが、より適切なクラスがある場合はプロジェクトの事情に合わせて変更して構わない。


ユーザのロールを保存する
*********************************************************************

アノテーションによる認可チェックでは、ユーザに割り当てられたロールをセッションストアに保存する実装をデフォルトで提供している。
ログイン時に、ユーザに割り当てられたロールを解決してセッションストアに保存しておくことで、その後の認可チェックはセッションストアに保存されたロールの情報を用いて行われるようになる。

以下に、ログイン時にロールをセッションストアに保存する実装例を記載する。

.. code-block:: java

  List<String> userRoles = resolveUserRoles(loginId);
  SessionStoreUserRoleUtil.save(userRoles, executionContext);

ここでは、ログインIDを元にユーザに割り当てられたロールの一覧を解決し、それを :java:extdoc:`SessionStoreUserRoleUtil <nablarch.common.authorization.role.session.SessionStoreUserRoleUtil>` の ``save`` メソッドでセッションストアに保存している。

.. tip::
  ``resolveUserRoles`` メソッドが行う、ユーザからロールを解決する方法については、フレームワークでは特に規定していない。
  したがって、プロジェクトごとの事情に合わせてロールを解決する実装を作りこむことになる。
  
  多くの場合はデータベースから解決することが想定される。
  例えば、ロールが「管理者」だけのようなシステムでは、ユーザの情報を管理するテーブルの「管理者フラグ」の値を見て解決するような方法が考えられる。
  また、ユーザにいくつかのロールを割り当てるようなシステムでは、ユーザとロールを関連付けるテーブルを検索することで解決するような方法が考えられる。


アクションのメソッドにアノテーションでロールを割り当てる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: java

  @CheckRole(Roles.ROLE_ADMIN)
  public HttpResponse index(HttpRequest request, ExecutionContext context) {

:java:extdoc:`CheckRole <nablarch.common.authorization.role.CheckRole>` アノテーションをアクションメソッドに設定し ``value`` にロールを指定することで、アクションメソッドにロールを割り当てることができる。
上記例では、 ``index`` メソッドに対して ``ADMIN`` ロールを割り当てている。
これにより、 ``index`` メソッドは ``ADMIN`` ロールを持つユーザだけが実行できるようになる。
もし ``ADMIN`` ロールを持たないユーザがメソッドを実行しようとした場合は、 :java:extdoc:`Forbidden <nablarch.fw.results.Forbidden>` がスローされる。

複数のロールを割り当てたい場合は、配列で指定できる。
以下に実装例を示す。

.. code-block:: java

  @CheckRole({Roles.ROLE_ADMIN, Roles.ROLE_PROJECT_MANAGER})
  public HttpResponse index(HttpRequest request, ExecutionContext context) {

この場合、 ``index`` メソッドを実行するためには ``ADMIN`` と ``PROJECT_MANAGER`` の両方のロールを保有している必要がある(AND条件)。

OR条件にしたい場合は、 ``anyOf`` に ``true`` を設定する。
以下に実装例を示す。

.. code-block:: java

  @CheckRole(
      value = {Roles.ROLE_ADMIN, Roles.ROLE_PROJECT_MANAGER},
      anyOf = true
  )
  public HttpResponse index(HttpRequest request, ExecutionContext context) {

上記例では、 ``index`` メソッドを実行するためには ``ADMIN`` か ``PROJECT_MANAGER`` のいずれかのロールを保有していれば良いということになる。


アノテーションに割り当てた CheckRole の設定を一覧で確認する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

アクションメソッドに設定した :java:extdoc:`CheckRole <nablarch.common.authorization.role.CheckRole>` アノテーションに誤りがないかチェックするために、アノテーションの設定状況を一覧表示する機能を提供している。
本機能を利用することで、アノテーションの設定に漏れが無いか、設定されている内容に過不足がないかをチェックできるようになる。

本機能は、システム起動時にアノテーションの設定情報を収集して、デバッグレベルでログに出力するという方法で実現している。
以下で、設定方法について説明する。

まず、 :java:extdoc:`CheckRoleLogger <nablarch.common.authorization.role.CheckRoleLogger>` のコンポーネントを以下のように定義する。

.. code-block:: xml

  <!-- 初期化が必要なコンポーネント -->
  <component name="initializer"
             class="nablarch.core.repository.initialization.BasicApplicationInitializer">
    <property name="initializeList">
      <list>
        <!-- 他の初期化が必要なコンポーネントの記述は省略 -->

        <component class="nablarch.common.authorization.role.CheckRoleLogger">
          <property name="targetPackage" value="com.nablarch.example.app.web.action" />
        </component>
      </list>
    </property>
  </component>

:java:extdoc:`CheckRoleLogger <nablarch.common.authorization.role.CheckRoleLogger>` は、初期化が必要なコンポーネントとして :java:extdoc:`BasicApplicationInitializer <nablarch.core.repository.initialization.BasicApplicationInitializer>` の ``initializeList`` に設定する。
またこのとき、 ``targetPackage`` プロパティにアクションクラスが存在するパッケージを指定する(サブパッケージも対象となる)。

なお、デフォルトでは末尾が ``Action`` で終わる名前のクラスが処理の対象となる。
この設定は ``targetClassPattern`` プロパティに任意の正規表現を指定することで変更できる。
詳細は :java:extdoc:`CheckRoleLogger <nablarch.common.authorization.role.CheckRoleLogger>` のJavadocを参照のこと。

上記設定が完了したら、ログレベルをデバッグレベルにしてシステムを起動する。
これにより、システム起動時に以下のようなログが出力されるようになる。

.. code-block:: text

  2023-01-11 14:29:31.643 -DEBUG- nablarch.common.authorization.role.CheckRoleLogger [null] boot_proc = [] proc_sys = [nablarch-example-web] req_id = [null] usr_id = [null] CheckRole Annotation Settings
  class	signature	role	anyOf
  com.nablarch.example.app.web.action.AuthenticationAction	index(nablarch.fw.web.HttpRequest, nablarch.fw.ExecutionContext)		
  (中略)
  com.nablarch.example.app.web.action.ProjectBulkAction	update(nablarch.fw.web.HttpRequest, nablarch.fw.ExecutionContext)		
  com.nablarch.example.app.web.action.ProjectUploadAction	index(nablarch.fw.web.HttpRequest, nablarch.fw.ExecutionContext)	ADMIN	true
  com.nablarch.example.app.web.action.ProjectUploadAction	index(nablarch.fw.web.HttpRequest, nablarch.fw.ExecutionContext)	PROJECT_MANAGER	true

ログには、以下の要素がタブ区切りで出力されるようになっている。

.. list-table:: ログ出力要素
   :widths: 1, 5, 10
   :header-rows: 1
   :stub-columns: 0

   * - 要素
     - 説明
     - 出力例
   * - ``class``
     - クラスの完全修飾名
     - ``com.nablarch.example.app.web.action.ProjectUploadAction``
   * - ``signature``
     - メソッドのシグネチャ
     - ``upload(nablarch.fw.web.HttpRequest, nablarch.fw.ExecutionContext)``
   * - ``role``
     - 割り当てられているロール(アノテーション未設定の場合は空)
     - ``ADMIN``
   * - ``anyOf``
     - ``@CheckRole`` の ``anyOf`` に設定された値(アノテーション未設定の場合は空)
     - ``false``

複数のロールが割り当てられている場合、それぞれのロールは別の行に分けて出力される。
例えば上記出力例では、 ``ProjectUploadAction`` の ``index`` メソッドには ``ADMIN`` と ``PROJECT_MANAGER`` の2つのロールが割り当てられていることが分かる。
実装に置き換えると、以下のように設定されていることになる。

.. code-block:: java

  @CheckRole(
      value = {Roles.ROLE_ADMIN, Roles.ROLE_PROJECT_MANAGER},
      anyOf = true
  )
  public HttpResponse index(HttpRequest request, ExecutionContext context) {


プログラムで判定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ロールの有無を、プログラム上の任意の場所で判定できる。

.. code-block:: java

  if (CheckRoleUtil.checkRole(Roles.ROLE_ADMIN, executionContext)) {
      // ADMIN ロールを持つ場合の処理
  }

プログラムでロールの有無を判定する場合は、 :java:extdoc:`CheckRoleUtil <nablarch.common.authorization.role.CheckRoleUtil>` を使用する。
上記例では、 ``checkRole`` メソッドを使って現在のユーザが ``ADMIN`` ロールを持っているかどうかを判定している。

複数のロールを指定する場合は、 ``checkRoleAllOf`` メソッドか ``checkRoleAnyOf`` メソッドを使用して判定できる。


JSPで判定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:doc:`permission_check` では、JSPのカスタムタグで認可チェックを行い自動的にボタンの表示・非表示を切り替えるような仕組みが提供されている。
しかし本認可チェックでは、このような仕組みは提供していない。

そこでここでは、本認可チェックを採用したうえでJSPの表示・非表示をロールの有無で制御する方法について説明する。

ロールによる表示の制御は、サーバー側で判定した結果をセッションストアなどに保存することで実現する。
実装例を以下に示す。

.. code-block:: java

  UserContext userContext = new UserContext();
  userContext.setAdmin(CheckRoleUtil.checkRole(Roles.ROLE_ADMIN, executionContext));
  userContext.setProjectManager(CheckRoleUtil.checkRole(Roles.ROLE_PROJECT_MANAGER, executionContext));

  SessionUtil.put(executionContext, "userContext", userContext);

この例では、ログイン時にユーザのロールを判定した結果を ``UserContext`` クラスに保存してセッションストアに格納している(``UserContext`` はただのJava Beansで、プロジェクトごとに必要に応じて作成する)。
これにより、JSPではEL式やJSTLを使うことで以下のように表示を制御できるようになる。

.. code-block:: jsp

  <c:if test="${userContext.admin}">
    <%-- ADMIN ロールを持つ場合に表示する --%>
  </c:if>
  <c:if test="${userContext.projectManager}">
    <%-- PROJECT_MANAGER ロールを持つ場合に表示する  --%>
  </c:if>


仕組み
---------------------------------------------------------------------

ここでは、アノテーションによる認可チェックの仕組みについて説明する。

.. image:: images/role_check/architecture.png

アノテーションを用いたチェック処理の実行は、Nablarchの :java:extdoc:`インターセプタ <nablarch.fw.Interceptor>` の仕組みを利用して実現している。
:java:extdoc:`CheckRole <nablarch.common.authorization.role.CheckRole>` アノテーションは、このインターセプタを実装したものとなっている。

:java:extdoc:`CheckRole <nablarch.common.authorization.role.CheckRole>` と :java:extdoc:`CheckRoleUtil <nablarch.common.authorization.role.CheckRoleUtil>` 自体は直接認可チェックは行わず、 :java:extdoc:`RoleEvaluator <nablarch.common.authorization.role.RoleEvaluator>` に処理を委譲する。
このとき、 :java:extdoc:`RoleEvaluator <nablarch.common.authorization.role.RoleEvaluator>` のインスタンスは :java:extdoc:`SystemRepository <nablarch.core.repository.SystemRepository>` から ``roleEvaluator`` という名前で取得したものを使用する。
また、チェック処理に渡すユーザIDは、 :java:extdoc:`ThreadContext <nablarch.core.ThreadContext>` の ``getUserId`` メソッドで取得したものを使用する。

:java:extdoc:`RoleEvaluator <nablarch.common.authorization.role.RoleEvaluator>` のデフォルトの実装クラスとして、本認可チェックでは :java:extdoc:`BasicRoleEvaluator <nablarch.common.authorization.role.BasicRoleEvaluator>` というクラスを提供している。
このクラスは、ユーザに紐づくロールと引数で渡されたロールとを比較し、条件を満たすかどうかを判定するシンプルな作りとなっている。
なお、ユーザに紐づくロールの解決は :java:extdoc:`UserRoleResolver <nablarch.common.authorization.role.UserRoleResolver>` に委譲している。

:java:extdoc:`UserRoleResolver <nablarch.common.authorization.role.UserRoleResolver>` のデフォルト実装としては、　:java:extdoc:`SessionStoreUserRoleResolver <nablarch.common.authorization.role.session.SessionStoreUserRoleResolver>` を提供している。
このクラスは、セッションストアに保存された情報でユーザのロールを解決する仕組みとなっている。


拡張方法
---------------------------------------------------------------------

前述の仕組みの説明から、 :java:extdoc:`RoleEvaluator <nablarch.common.authorization.role.RoleEvaluator>` または :java:extdoc:`UserRoleResolver <nablarch.common.authorization.role.UserRoleResolver>` の実体を差し替えることで任意の処理に拡張できることがわかる。

:java:extdoc:`RoleEvaluator <nablarch.common.authorization.role.RoleEvaluator>` の実体の差し替えは、 :java:extdoc:`RoleEvaluator <nablarch.common.authorization.role.RoleEvaluator>` を実装した独自クラスを作成し、そのクラスを ``roleEvaluator`` という名前でコンポーネント登録することで実現できる。

.. code-block:: xml

  <component name="roleEvaluator" class="com.example.CustomRoleEvaluator" />

:java:extdoc:`RoleEvaluator <nablarch.common.authorization.role.RoleEvaluator>` の実体には :java:extdoc:`BasicRoleEvaluator <nablarch.common.authorization.role.BasicRoleEvaluator>` を使いつつ、 :java:extdoc:`UserRoleResolver <nablarch.common.authorization.role.UserRoleResolver>` の実体だけを差し替えたい場合は、 :java:extdoc:`BasicRoleEvaluator <nablarch.common.authorization.role.BasicRoleEvaluator>` の ``userRoleResolver`` プロパティに設定するコンポーネントを差し替えればいい。
デフォルトコンフィグレーションを利用している場合は、 ``userRoleResolver`` という名前のコンポーネントを設定するように定義されているので、同じ名前で独自クラスのコンポーネントを定義することで差し替えができる。

.. code-block:: xml

  <component name="userRoleResolver" class="com.example.CustomUserRoleResolver" />
