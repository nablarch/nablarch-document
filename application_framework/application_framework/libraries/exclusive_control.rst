.. _exclusive_control:

排他制御
=====================================================================

.. contents:: 目次
  :depth: 3
  :local:

この機能では、データベースのデータ更新に対する排他制御を行う。
この機能により、データベースの同一データに対して、
複数のトランザクション（ウェブやバッチ）から同時に更新した場合でも、
データの整合性を保つことができる。

.. _exclusive_control-deprecated:

.. important::
 この機能は、以下の理由により **非推奨** である。
 排他制御には、 :ref:`universal_dao` を使用すること。

 * :ref:`universal_dao` の排他制御は、本機能より簡単に使用できる。
    :ref:`universal_dao_jpa_optimistic_lock` 、 :ref:`universal_dao_jpa_pessimistic_lock` を参照。
 * 主キーを非文字列型で定義した場合、データベースによってはこの機能を使用することができない。
    この機能は、主キーの値を全て文字列型( `java.lang.String` )で保持している。
    主キーのカラム定義が非文字列型(charやvarchar以外)の場合に、
    データベースによっては型の不一致でSQL文の実行時例外が発生する。
    例えば、PostgreSQLのように暗黙の型変換が行われないデータベースの場合、この問題が発生する。

機能概要
---------------------------------------------------------------------

楽観的ロック/悲観的ロックができる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
この機能では、テーブルにバージョン番号カラムを定義することで、楽観的ロック/悲観的ロックを行う。
本フレームワークでは、バージョン番号カラムが定義されたテーブルを **排他制御用テーブル** と呼ぶ。

この機能では以下のことが実現できる。

* :ref:`exclusive_control-optimistic_lock`
* :ref:`exclusive_control-optimistic_lock-bulk`
* :ref:`exclusive_control-pessimistic_lock`

この機能が提供する楽観的ロック/悲観的ロックは、同じ排他制御用テーブルを使用して実現するため、
楽観的ロックと悲観的ロックを並行で使用しても、同一データが同時に更新されるのを防ぐことができる。
たとえば、楽観的ロックを使用するウェブと、悲観的ロックを使用するバッチを並行稼働させても、
データの整合性を保つことができる。

排他制御用テーブルは、排他制御を行う単位ごとに定義し、競合が許容される最大の単位で定義する。
たとえば、「ユーザ」という大きな単位でロックすることが業務的に許容されるならば、
その単位で排他制御用テーブルを定義する。
ただし、単位を大きくすると、競合する可能性が高くなり、
更新失敗(楽観的ロックの場合)や処理遅延(悲観的ロックの場合)を招く点に注意すること。

.. tip::
 通常、排他制御用テーブルの単位は、業務的な観点で定義する。
 たとえば、売上処理と入金処理による更新が同時に行われる場合は、
 それらの処理に関連するテーブルをまとめた単位で排他制御用テーブルを定義する。

 また、テーブル設計の観点からも排他制御用テーブルの単位を定義できる。
 たとえば、ヘッダ部(親)と明細部(子)など、テーブルの親子関係が明確であれば、
 親の単位で排他制御用テーブルを定義する。
 親子関係が明確でない場合は、どちらを親にするのが良いかを判断し、排他制御用テーブルを定義する。

.. important::

 排他制御用テーブルの設計が終わったら、更新順序の設計を行う。
 各テーブルの更新順序を定めることで、デッドロックの防止、及び更新時のデータ整合性の保証を実現する。
 データベースでは、レコードを更新すると行ロックがかかるので、
 更新順序を定めておかなければデッドロックが発生する可能性が非常に高くなる。

モジュール一覧
---------------------------------------------------------------------
.. code-block:: xml

  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-exclusivecontrol</artifactId>
  </dependency>
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-common-exclusivecontrol-jdbc</artifactId>
  </dependency>

  <!-- 楽観的ロックを行う場合のみ -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web-tag</artifactId>
  </dependency>

使用方法
---------------------------------------------------------------------

.. _exclusive_control-optimistic_setting:

排他制御を使うために準備する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
排他制御を使うためには、 **設定** と **排他制御に必要な情報を保持するクラスの作成** を行う。

設定
 :java:extdoc:`BasicExclusiveControlManager <nablarch.common.exclusivecontrol.BasicExclusiveControlManager>` の設定をコンポーネント定義に追加する。

 .. code-block:: xml

  <!-- コンポーネント名は"exclusiveControlManager"で設定する。 -->
  <component name="exclusiveControlManager"
             class="nablarch.common.exclusivecontrol.BasicExclusiveControlManager">
      <!-- 楽観ロックで排他エラーが発生した際に使用するメッセージID -->
      <property name="optimisticLockErrorMessageId" value="CUST0001" />
  </component>

排他制御に必要な情報を保持するクラスの作成
 :java:extdoc:`ExclusiveControlContext <nablarch.common.exclusivecontrol.ExclusiveControlContext>` を継承して作成する。
 このクラスは、排他制御用テーブルごとに作成し、排他制御を行うAPI呼び出しで使用する。

 .. code-block:: sql

  -- 排他制御用テーブル
  CREATE TABLE USERS (
      USER_ID CHAR(6) NOT NULL,
      -- 主キー以外の業務データは省略。
      VERSION NUMBER(10) NOT NULL,
      PRIMARY KEY (USER_ID)
  )

 .. code-block:: java

  // 排他制御用テーブルUSERSに対応するクラス。
  // ExclusiveControlContextを継承する。
  public class UsersExclusiveControl extends ExclusiveControlContext {

      // 排他制御用テーブルの主キーは列挙型で定義する。
      private enum PK { USER_ID }

      // 主キーの値をとるコンストラクタを定義する。
      public UsersExclusiveControl(String userId) {

          // 親クラスのsetTableNameメソッドでテーブル名を設定する。
          setTableName("USERS");

          // 親クラスのsetVersionColumnNameメソッドでバージョン番号カラム名を設定する。
          setVersionColumnName("VERSION");

          // 親クラスのsetPrimaryKeyColumnNamesメソッドで
          // Enumのvaluesメソッドを使用して、主キーの列挙型を全て設定する。
          setPrimaryKeyColumnNames(PK.values());

          // 親クラスのappendConditionメソッドで主キーの値を追加する。
          appendCondition(PK.USER_ID, userId);
      }
  }

.. _exclusive_control-optimistic_lock:

楽観的ロックを行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
楽観的ロックは、更新対象データを取得する時点で、排他制御用テーブルのバージョン番号を取得しておき、
更新を行う時点で、事前に取得した排他制御用テーブルのバージョン番号が更新されていないかをチェックすることで実現する。

楽観的ロックには、 :java:extdoc:`HttpExclusiveControlUtil <nablarch.common.web.exclusivecontrol.HttpExclusiveControlUtil>` を使用する。

入力→確認→完了がある更新機能を例に、楽観的ロックの実装例を示す。

入力画面の初期表示
 .. code-block:: java

  public HttpResponse index(HttpRequest request, ExecutionContext context) {

      // (業務処理)
      // 更新対象データを取得するための主キー条件をリクエストから取得する。
      String userId = getUserId(request);

      // (排他制御)
      // 主キークラスを生成し、バージョン番号を準備する。
      // 取得したバージョン番号は、フレームワークにより、指定されたExecutionContextに設定される。
      HttpExclusiveControlUtil.prepareVersion(context, new UsersExclusiveControl(userId));

      // (業務処理)
      // 更新対象データを取得し、入力画面表示のために、リクエストスコープに設定する。
      context.setRequestScopedVar("user", findUser(userId));

      return new HttpResponse("/input.jsp");
  }

入力画面の確認ボタン（入力→確認）
 .. code-block:: java

  @OnErrors({
      @OnError(type = ApplicationException.class, path = "/input.jsp"),
      @OnError(type = OptimisticLockException.class, path = "/error.jsp")
  })
  public HttpResponse confirm(HttpRequest request, ExecutionContext context) {

      // (排他制御)
      // バージョン番号の更新チェックを行う。
      // バージョン番号は、フレームワークにより、指定されたHttpRequestから取得する。
      // バージョン番号が更新されている場合は、OptimisticLockExceptionが送出されるので、
      // @OnErrorを指定して遷移先を指定する。
      HttpExclusiveControlUtil.checkVersions(request, context);

      // (業務処理)
      // 入力データのチェックを行い、確認画面表示のために、リクエストスコープに設定する。
      context.setRequestScopedVar("user", getUser(request));

      return new HttpResponse("/confirm.jsp");
  }

 .. important::
  バージョン番号のチェック( :java:extdoc:`HttpExclusiveControlUtil.checkVersions <nablarch.common.web.exclusivecontrol.HttpExclusiveControlUtil.checkVersions(nablarch.fw.web.HttpRequest,%20nablarch.fw.ExecutionContext)>` )を行わなければ、
  画面間でバージョン番号が引き継がれない。

確認画面の更新ボタン（確認→完了）
 .. code-block:: java

  @OnErrors({
      @OnError(type = ApplicationException.class, path = "/input.jsp"),
      @OnError(type = OptimisticLockException.class, path = "/error.jsp")
  })
  public HttpResponse update(HttpRequest request, ExecutionContext context) {

      // (排他制御)
      // バージョン番号の更新チェックと更新を行う。
      // バージョン番号は、フレームワークにより、指定されたHttpRequestから取得する。
      // バージョン番号が更新されている場合は、OptimisticLockExceptionが送出されるので、
      // @OnErrorを指定して遷移先を指定する。
      HttpExclusiveControlUtil.updateVersionsWithCheck(request);

      // (業務処理)
      // 入力データのチェックを行い、更新処理を行う。
      // 完了画面表示のために、更新データをリクエストスコープに設定する。
      User user = getUser(request);
      update(user);
      context.setRequestScopedVar("user", user);

      return new HttpResponse("/complete.jsp");
  }

.. _exclusive_control-optimistic_lock-bulk:

一括更新で楽観的ロックを行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
複数のレコードに対し、特定のプロパティ(論理削除フラグなど)を一括更新するような処理では、
選択されたレコードのみに楽観的ロックのチェックを行いたい場合がある。

排他制御用テーブルの主キーが、 **複合主キーでない場合** と **複合主キーの場合** で、
二通りの実装方法がある。

複合主キーでない場合
 ユーザの一括削除を行う画面を例に、複合主キーでない場合の実装例を示す。
 バージョン番号の取得部分は、 :java:extdoc:`HttpExclusiveControlUtil#prepareVersions <nablarch.common.web.exclusivecontrol.HttpExclusiveControlUtil.prepareVersions(nablarch.fw.ExecutionContext,%20java.util.List)>` を呼び出すだけなので、
 実装例を省略する。

 .. code-block:: html

  <!-- 画面の実装（前後は省略） -->
  <tr>
    <th>削除対象</th>
    <th>ユーザ名</th>
  </tr>
  <tr>
    <!-- リクエストパラメータ "user.deactivate" でユーザの主キーを送る。 -->
    <td><checkbox name="user.deactivate" value="user001" /></td>
    <td>ユーザ001</td>
  </tr>
  <tr>
    <td><checkbox name="user.deactivate" value="user002" /></td>
    <td>ユーザ002</td>
  </tr>

 .. code-block:: java

  // (排他制御:チェック)
  // リクエストパラメータ "user.deactivate" に設定されたユーザの主キーのみを
  // チェックの対象とする。
  HttpExclusiveControlUtil.checkVersions(request, context, "user.deactivate");

 .. code-block:: java

  // (排他制御:チェックと更新)
  // リクエストパラメータ "user.deactivate" に設定されたユーザの主キーのみを
  // チェックと更新の対象とする。
  HttpExclusiveControlUtil.updateVersionsWithCheck(request, "user.deactivate");

複合主キーの場合
 ユーザの一括削除を行う画面を例に、複合主キーの場合の実装例を示す。
 バージョン番号の取得部分は、 :java:extdoc:`HttpExclusiveControlUtil#prepareVersions <nablarch.common.web.exclusivecontrol.HttpExclusiveControlUtil.prepareVersions(nablarch.fw.ExecutionContext,%20java.util.List)>` を呼び出すだけなので、
 実装例を省略する。

 .. code-block:: sql

  -- 複合主キーが定義されたテーブル。
  CREATE TABLE USERS (
      USER_ID CHAR(6) NOT NULL,
      PK2     CHAR(6) NOT NULL,
      PK3     CHAR(6) NOT NULL,
      -- 主キー以外の業務データは省略。
      VERSION NUMBER(10) NOT NULL,
      PRIMARY KEY (USER_ID,PK2,PK3)
  )

 .. code-block:: java

  // 排他制御用テーブルUSERSに対応したクラス。
  public class UsersExclusiveControl extends ExclusiveControlContext {

      // 排他制御用テーブルの主キーは列挙型で定義する。
      private enum PK { USER_ID, PK2, PK3 }

      // 主キーの値をとるコンストラクタを定義し、親クラスのメソッドで必要な情報を設定する。
      public UsersExclusiveControl(String userId, String pk2, String pk3) {
          setTableName("USERS");
          setVersionColumnName("VERSION");
          setPrimaryKeyColumnNames(PK.values());
          appendCondition(PK.USER_ID, userId);
          appendCondition(PK.PK2, pk2);
          appendCondition(PK.PK3, pk3);
      }
  }

 .. code-block:: html

  <!-- 画面の実装（前後は省略） -->
  <tr>
    <th>削除対象</th>
    <th>ユーザ名</th>
  </tr>
  <tr>
    <!--
    リクエストパラメータ "user.deactivate" でユーザの主キーを送る。
    複合主キーの場合は、区切り文字(任意、ただし主キーの値にはなり得ないこと)
    で結合した文字列を指定する。
    -->
    <td>
      <input id="checkbox" type="checkbox" name="user.userCompositeKeys"
                                           value="user001,pk2001,pk3001" />
    </td>
    <td>ユーザ001</td>
  </tr>
  <tr>
    <td>
      <input id="checkbox" type="checkbox" name="user.userCompositeKeys"
                                           value="user002,pk2002,pk3002" />
    </td>
    <td>ユーザ002</td>
  </tr>

 .. tip::
  複合主キーに対応したカスタムタグと
  :java:extdoc:`CompositeKey<nablarch.common.web.compositekey.CompositeKey>` を使うと、
  複合主キーをもっと簡単に扱える。詳細は、 :ref:`tag-composite_key` を参照。

 .. code-block:: java

  // (排他制御:チェック)
  // Formには、区切り文字を考慮し、リクエストパラメータから主キーを取り出す処理を実装している。
  User[] deletedUsers = form.getDeletedUsers();

  // チェックをレコードごとに呼び出す。
  for(User deletedUser : deletedUsers) {
      HttpExclusiveControlUtil.checkVersion(
          request, context,
          new UsersExclusiveControl(deletedUser.getUserId(),
                                    deletedUser.getPk2(),
                                    deletedUser.getPk3()));
  }

 .. code-block:: java

  // (排他制御:チェックと更新)
  User[] deletedUsers = form.getDeletedUsers();

  // チェックおよび更新をレコードごとに呼び出す。
  for(User deletedUser : deletedUsers) {
      HttpExclusiveControlUtil.updateVersionWithCheck(
          request, new ExclusiveUserCondition(deletedUser.getUserId(),
                                              deletedUser.getPk2(),
                                              deletedUser.getPk3()));
  }

.. _exclusive_control-pessimistic_lock:

悲観的ロックを行う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
悲観的ロックは、更新対象データを取得する前に、排他制御用テーブルのバージョン番号を更新することで実現する。

更新対象データを取得する前に、排他制御用テーブルのバージョン番号を更新することで、
更新処理のトランザクションがコミット又はロールバックされるまで、排他制御用テーブルの対象行がロックされる。
このため、他のトランザクションの更新処理はロックが解除されるまで待たされる。

悲観的ロックには、 :java:extdoc:`ExclusiveControlUtil#updateVersion <nablarch.common.exclusivecontrol.ExclusiveControlUtil.updateVersion(nablarch.common.exclusivecontrol.ExclusiveControlContext)>` を使用する。

.. code-block:: java

 ExclusiveControlUtil.updateVersion(new UsersExclusiveControl("U00001"));

.. important::
 バッチ処理では、ロックを行うための主キーのみを取得する前処理を設け、
 本処理で1件ずつロックを取得してからデータ取得と更新を行うように実装する。
 理由は以下の通り。

 * データを取得してから更新するまでの間に、他のプロセスによりデータが更新されてしまうことを防ぐため。
 * ロックしている時間をできるだけ短くし、並列処理に与える影響をできるだけ小さくするため。

拡張例
---------------------------------------------------------------------
なし。
