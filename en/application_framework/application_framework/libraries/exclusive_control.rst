.. _exclusive_control:

Exclusive Control
=====================================================================

.. contents:: Table of contents
  :depth: 3
  :local:

This function performs exclusive control for updating data in the database.
With this function,
data integrity can be maintained even when the same data in the database is updated
from multiple transactions (web or batch) at the same time.

.. _exclusive_control-deprecated:

.. important::
 This function is **deprecated** because of the following reasons:
 Uses :ref:`universal_dao` for exclusive control.

 * Exclusive control of :ref:`universal_dao` can be used more easily than this function.
    See :ref:`universal_dao_jpa_optimistic_lock` , :ref:`universal_dao_jpa_pessimistic_lock`.
 * If the primary key is defined as a non-string type, this function cannot be used depending on the database.
    This function stores all the primary key values as string type ( `java.lang.String` ).
    When the primary key column definition is a non-string type (other than char or varchar),
    a SQL statement runtime exception occurs due to type mismatch depending on the database.
    For example, this problem occurs in the case of databases such as PostgreSQL where the implicit type conversion is not performed.

Function overview
---------------------------------------------------------------------

Optimistic locking/Pessimistic locking are possible
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This function performs optimistic locking/pessimistic locking by defining the version number column in the table.
In this framework, the table in which the version number column is defined is called the **exclusive control table**.

The following can be realized with this function.

* :ref:`exclusive_control-optimistic_lock`
* :ref:`exclusive_control-optimistic_lock-bulk`
* :ref:`exclusive_control-pessimistic_lock`

Since, the optimistic lock/pessimistic lock provided by this function is realized by using the same exclusive control table,
even if optimistic lock and pessimistic lock are used in parallel, it is possible to prevent the same data from being updated at the same time.
For example, web using optimistic lock and batch using pessimistic lock can run
in parallel and still maintain the data integrity.

The exclusive control table is defined for each unit of exclusive control and the largest unit in which conflicts are allowed.
For example, if the business allows locking in a large unit called "user",
an exclusive control table is defined in that unit.
However, note that the possibility of conflict increases if the unit is increased,
and update failure (in the case of optimistic locking) and processing delay (in the case of pessimistic locking) will occur.

.. tip::
 Normally, the unit of the exclusive control table is defined from a business perspective.
 For example, when the sales and deposit processes are updated at the same time,
 the exclusive control table is defined in a unit of tables related to the processes.

 Also, the unit of the exclusive control table can be defined from the perspective of table design.
 For example, if the parent-child relationship of the table such as the header (parent) and details (child) is clear,
 the exclusive control table is defined in parent units.
 If the parent-child relationship is not clear, determine which one should be the parent and then define the exclusive control table.

.. important::

 Design the update order after designing the exclusive control table.
 Deadlock is prevented by determining the update order of each table, and data integrity during update is guaranteed.
 In a database, since row locks occur when records are updated,
 deadlocks are very likely to occur if the update order is not specified.

Module list
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

  <!-- Only for optimistic locking -->
  <dependency>
    <groupId>com.nablarch.framework</groupId>
    <artifactId>nablarch-fw-web-tag</artifactId>
  </dependency>

How to use
---------------------------------------------------------------------

.. _exclusive_control-optimistic_setting:

Prepare to use exclusive control
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To use exclusive control, **create a class that retains the configuration** and **information required for exclusive control**.

Configuration
 Add the configuration of :java:extdoc:`BasicExclusiveControlManager <nablarch.common.exclusivecontrol.BasicExclusiveControlManager>` to the component definition.

 .. code-block:: xml

  <!-- Configure the component name with "exclusiveControlManager". -->
  <component name="exclusiveControlManager"
             class="nablarch.common.exclusivecontrol.BasicExclusiveControlManager">
      <!-- Message ID used when an exclusive error occurs in optimistic locking -->
      <property name="optimisticLockErrorMessageId" value="CUST0001" />
  </component>

Creating a class that holds the information required for exclusive control
 Create by inheriting :java:extdoc:`ExclusiveControlContext <nablarch.common.exclusivecontrol.ExclusiveControlContext>`.
 This class is created for each exclusive control table and used in the API call that performs exclusive control.

 .. code-block:: sql

  -- Exclusive control table
  CREATE TABLE USERS (
      USER_ID CHAR(6) NOT NULL,
      -- Business data other than the primary key is omitted.
      VERSION NUMBER(10) NOT NULL,
      PRIMARY KEY (USER_ID)
  )

 .. code-block:: java

  // Class corresponding to the exclusive control table USERS.
  // Inherit ExclusiveControlContext.
  public class UsersExclusiveControl extends ExclusiveControlContext {

      // Define the primary key of the exclusive control table with enumeration type.
      private enum PK { USER_ID }

      // Define a constructor that takes the value of the primary key.
      public UsersExclusiveControl(String userId) {

          // Configure the table name with the setTableName method of the parent class.
          setTableName("USERS");

          // Configure the version number column name with the setVersionColumnName method
          // of the parent class.
          setVersionColumnName("VERSION");

          // Use the enum values method for the setPrimaryKeyColumnNames method
          // of parent class to set all primary key enumeration types.
          setPrimaryKeyColumnNames(PK.values());

          // Add the primary key value using the appendCondition method of the parent class.
          appendCondition(PK.USER_ID, userId);
      }
  }

.. _exclusive_control-optimistic_lock:

Optimistic locking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When the data to be updated is acquired, the version number of the table for exclusive control is obtained.
The optimistic lock is achieved by checking whether the version number of the exclusive control table has been updated during the update.

Use :java:extdoc:`HttpExclusiveControlUtil <nablarch.common.web.exclusivecontrol.HttpExclusiveControlUtil>` for optimistic locking.

Using the update function with input → confirmation → completion as an example, an implementation example of optimistic locking is shown below.

Initial display of input screen
 .. code-block:: java

  public HttpResponse index(HttpRequest request, ExecutionContext context) {

      // (Business process)
      // Get the primary key condition to acquire the update target data from the request.
      String userId = getUserId(request);

      // (Exclusive control)
      // Generate the primary key class and prepare the version number.
      // The acquired version number is configured in the ExecutionContext specified
      // by the framework.
      HttpExclusiveControlUtil.prepareVersion(context, new UsersExclusiveControl(userId));

      // (Business process)
      // Acquire the update target data and configure it in the request scope
      // to display the input screen.
      context.setRequestScopedVar("user", findUser(userId));

      return new HttpResponse("/input.jsp");
  }

Confirmation button on the input screen (Input → Confirm)
 .. code-block:: java

  @OnErrors({
      @OnError(type = ApplicationException.class, path = "/input.jsp"),
      @OnError(type = OptimisticLockException.class, path = "/error.jsp")
  })
  public HttpResponse confirm(HttpRequest request, ExecutionContext context) {

      // (Exclusive control)
      // Check the update of version number.
      // Acquire the version number from the HttpRequest specified by the framework.
      // Since the OptimisticLockException will be thrown if the version number has been updated,
      // specify @OnError and the transition destination.
      HttpExclusiveControlUtil.checkVersions(request, context);

      // (Business process)
      // Check the input data and configure in the request scope
      // to display the confirmation screen.
      context.setRequestScopedVar("user", getUser(request));

      return new HttpResponse("/confirm.jsp");
  }

 .. important::
  The version numbers will not be inherited between screens, if ( :java:extdoc:`HttpExclusiveControlUtil.checkVersions <nablarch.common.web.exclusivecontrol.HttpExclusiveControlUtil.checkVersions(nablarch.fw.web.HttpRequest-nablarch.fw.ExecutionContext)>` )
  does not perform the version check.

Update button on the confirmation screen (confirmation → complete)
 .. code-block:: java

  @OnErrors({
      @OnError(type = ApplicationException.class, path = "/input.jsp"),
      @OnError(type = OptimisticLockException.class, path = "/error.jsp")
  })
  public HttpResponse update(HttpRequest request, ExecutionContext context) {

      // (Exclusive control)
      // Perform the update check of the version number and update.
      // Acquire the version number from the HttpRequest specified by the framework.
      // Since the OptimisticLockException will be thrown if the version number has been updated,
      // specify @OnError and the transition destination.
      HttpExclusiveControlUtil.updateVersionsWithCheck(request);

      // (Business process)
      // Check the input data and perform the update process.
      // Configure the updated data in request scope to the display completion screen.
      User user = getUser(request);
      update(user);
      context.setRequestScopedVar("user", user);

      return new HttpResponse("/complete.jsp");
  }

.. _exclusive_control-optimistic_lock-bulk:

Perform optimistic lock with batch update
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In the process of collectively updating specific properties (such as logical deletion flag) for multiple records,
performing optimistic lock check only on selected records may be preferred.

There are two implementation methods depending on whether the primary key of the exclusive control table
is **not a composite primary key** or **a composite primary key**.

Is not a composite primary key
 An implementation example when the primary key is not a composite primary key is shown using the screen for batch deletion of users as an example.
 Since the acquire section of the version number just calls :java:extdoc:`HttpExclusiveControlUtil#prepareVersions <nablarch.common.web.exclusivecontrol.HttpExclusiveControlUtil.prepareVersions(nablarch.fw.ExecutionContext-java.util.List)>`,
 implementation example is omitted.

 .. code-block:: html

  <!-- Implementation of screen (before and after are omitted) -->
  <tr>
    <th>Delete target</th>
    <th>User name</th>
  </tr>
  <tr>
    <!-- Send the primary key of the user with the request parameter "user.deactivate". -->
    <td><checkbox name="user.deactivate" value="user001" /></td>
    <td>User 001</td>
  </tr>
  <tr>
    <td><checkbox name="user.deactivate" value="user002" /></td>
    <td>ユーザ002</td>
  </tr>

 .. code-block:: java

  // (Exclusive control: Check)
  // Only the primary key of the user configured in the request parameter "user.deactivate"
  // is a check target.
  HttpExclusiveControlUtil.checkVersions(request, context, "user.deactivate");

 .. code-block:: java

  // (Exclusive control: Check and update)
  // Only the primary key of the user configured in the request parameter "user.deactivate"
  // is a check target.
  HttpExclusiveControlUtil.updateVersionsWithCheck(request, "user.deactivate");

For composite primary key
 An implementation example when the primary key is a composite primary key is shown using the screen for batch deletion of users as an example.
 Since the acquire section of the version number just calls :java:extdoc:`HttpExclusiveControlUtil#prepareVersions <nablarch.common.web.exclusivecontrol.HttpExclusiveControlUtil.prepareVersions(nablarch.fw.ExecutionContext-java.util.List)>`,
 implementation example is omitted.

 .. code-block:: sql

  -- Table with a composite primary key defined.
  CREATE TABLE USERS (
      USER_ID CHAR(6) NOT NULL,
      PK2     CHAR(6) NOT NULL,
      PK3     CHAR(6) NOT NULL,
      -- Business data other than the primary key is omitted.
      VERSION NUMBER(10) NOT NULL,
      PRIMARY KEY (USER_ID,PK2,PK3)
  )

 .. code-block:: java

  // Class corresponding to the exclusive control table USERS.
  public class UsersExclusiveControl extends ExclusiveControlContext {

      // Define the primary key of the exclusive control table with enumeration type.
      private enum PK { USER_ID, PK2, PK3 }

      // Define a constructor that takes the value of the primary key
      // and set the necessary information in the parent class method.
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

  <!-- Implementation of screen (before and after are omitted) -->
  <tr>
    <th>Delete target</th>
    <th>User name</th>
  </tr>
  <tr>
    <!--
    Send the primary key of the user with the request parameter "user.deactivate".
    In the case of a composite primary key, specify a string that is combined with delimiters
    (arbitrary, it cannot be the primary key value).
    -->
    <td>
      <input id="checkbox" type="checkbox" name="user.userCompositeKeys"
                                           value="user001,pk2001,pk3001" />
    </td>
    <td>User 001</td>
  </tr>
  <tr>
    <td>
      <input id="checkbox" type="checkbox" name="user.userCompositeKeys"
                                           value="user002,pk2002,pk3002" />
    </td>
    <td>ユーザ002</td>
  </tr>

 .. tip::
  Composite primary keys are easier to handle when custom tag corresponding to the composite primary key
  and :java:extdoc:`CompositeKey<nablarch.common.web.compositekey.CompositeKey>` are used.
  For details, see :ref:`tag-composite_key`.

 .. code-block:: java

  // (Exclusive control: Check)
  // Form implements the process of extracting the primary key from the request parameter
  // taking the delimiter into consideration.
  User[] deletedUsers = form.getDeletedUsers();

  // Call the check by record.
  for(User deletedUser : deletedUsers) {
      HttpExclusiveControlUtil.checkVersion(
          request, context,
          new UsersExclusiveControl(deletedUser.getUserId(),
                                    deletedUser.getPk2(),
                                    deletedUser.getPk3()));
  }

 .. code-block:: java

  // (Exclusive control: Check and update)
  User[] deletedUsers = form.getDeletedUsers();

  // Call check and update by record.
  for(User deletedUser : deletedUsers) {
      HttpExclusiveControlUtil.updateVersionWithCheck(
          request, new ExclusiveUserCondition(deletedUser.getUserId(),
                                              deletedUser.getPk2(),
                                              deletedUser.getPk3()));
  }

.. _exclusive_control-pessimistic_lock:

Pessimistic locking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The pessimistic lock is realized by updating the version number of the exclusive control table before acquiring the update target data.

By updating the version number of the exclusive control table before acquiring the update target data,
the target row of the exclusive control table is locked until the transaction of the update process is committed or rolled back.
Therefore, the update process of other transactions is kept on wait until the lock is released.

Use :java:extdoc:`ExclusiveControlUtil#updateVersion <nablarch.common.exclusivecontrol.ExclusiveControlUtil.updateVersion(nablarch.common.exclusivecontrol.ExclusiveControlContext)>` for pessimistic locking.

.. code-block:: java

 ExclusiveControlUtil.updateVersion(new UsersExclusiveControl("U00001"));

.. important::
 In batch process, pre-processing to acquire only the primary key for locking is provided,
 and it is implemented in this process such that data is acquired and updated after acquiring one lock each.
 The reasons are as follows.

 * To prevent other processes from updating the data between the time when the data is acquired and updated.
 * The lock time should be kept as short as possible and keep its impact on parallel processing as small as possible.

Expansion example
---------------------------------------------------------------------
None.
