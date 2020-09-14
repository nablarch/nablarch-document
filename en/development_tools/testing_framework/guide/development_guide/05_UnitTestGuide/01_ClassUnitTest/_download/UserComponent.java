package nablarch.sample.management.user;

import nablarch.common.date.DateUtil;
import nablarch.core.date.BusinessDateUtil;
import nablarch.core.db.statement.ParameterizedSqlPStatement;
import nablarch.core.db.statement.SqlPStatement;
import nablarch.core.db.statement.SqlResultSet;
import nablarch.core.db.statement.exception.DuplicateStatementException;
import nablarch.core.db.support.DbAccessSupport;
import nablarch.core.message.ApplicationException;
import nablarch.core.message.MessageLevel;
import nablarch.core.message.MessageUtil;

import nablarch.sample.util.AuthenticationUtil;
import nablarch.sample.util.IdGeneratorUtil;

/**
 * Service class for user registration<br/>
 *
 * @author Tsuyoshi Kawasaki
 * @since 1.0
 */
public class UserComponent extends DbAccessSupport {

    /** User ID lock status: unlocked */
    private static final String USER_ID_NOT_LOCKED = "0";

    /** Default number of password failures */
    private static final int INITIAL_FAILED_COUNT = 0;

    /**
     * Search user group.
     *
     * @return Search results
     */
    public SqlResultSet selectUserGroups() {
        SqlPStatement statement = getSqlPStatement("SELECT_ALL_UGROUPS");
        return statement.retrieve();
    }

    /**
     * Acquires all use test IDs and names registered in the use test table.
     *
     * @return Search results. Sort by use test ID
     */
    public SqlResultSet getAllUseCase() {
        SqlPStatement statement = getSqlPStatement("SELECT_ALL_USE_CASES");
        return statement.retrieve();
    }

    /**
     * Checks input information on user registration. <br>
     * The name is also acquired if the information passes the check.
     *
     * @param systemAccount {@link SystemAccountEntity} containing the information to be checked
     * @param ugroupSystemAccount {@link UgroupSystemAccountEntity} containing the information to be checked
     */
    public void checkForRegisterUser(SystemAccountEntity systemAccount,
            UgroupSystemAccountEntity ugroupSystemAccount) {

        // Login ID check
        checkLoginId(systemAccount.getLoginId());
        // Group ID check
        checkGroupId(ugroupSystemAccount);
        // Use case ID check
        if (systemAccount.getUseCase() != null) {
            checkUseCaseId(systemAccount);
        }
    }

    /**
     * Registers user.
     *
     * @param systemAccount {@link SystemAccountEntity} containing information input in the screen
     * @param users {@link UsersEntity} containing information input in the screen
     * @param ugroupSystemAccount {@link UgroupSystemAccountEntity} containing information input in the screen
     */
    public void registerUser(SystemAccountEntity systemAccount,
            UsersEntity users,
            UgroupSystemAccountEntity ugroupSystemAccount) {

        // Acquires date
        // Assigns user ID
        String userId = IdGeneratorUtil.generateUserId();
        // Current (system) date
        String current = BusinessDateUtil.getDate();
        // After 1 month (expiration of password)
        String passwordExpirationDate = DateUtil.addMonth(current, 1);
        // After 12 months (expiration of user)
        String userEffectiveDateTo = DateUtil.addMonth(current, 12);

        // System account registration
        systemAccount.setPasswordExpirationDate(passwordExpirationDate);
        systemAccount.setEffectiveDateFrom(current);
        systemAccount.setEffectiveDateTo(userEffectiveDateTo);
        systemAccount.setUserId(userId);
        systemAccount.setUserIdLocked(USER_ID_NOT_LOCKED);
        systemAccount.setFailedCount(INITIAL_FAILED_COUNT);
        systemAccount.setPassword(AuthenticationUtil.encryptPassword(
                systemAccount.getUserId(),
                systemAccount.getNewPassword()));

        registerSystemAccount(systemAccount);

        // User entity registration
        users.setUserId(userId);
        registerUsers(users);

        // Group system account registration
        ugroupSystemAccount.setUserId(userId);
        ugroupSystemAccount.setEffectiveDateFrom(current);
        ugroupSystemAccount.setEffectiveDateTo(userEffectiveDateTo);
        registerUgroupSystemAccount(ugroupSystemAccount);

        // System account authority registration
        if (systemAccount.getUseCase() != null
                && systemAccount.getUseCase().length != 0) {
            registerSystemAccountAuthority(systemAccount);
        }
    }

    /**
     * Checks whether the login ID is already registered.
     *
     * @param loginId Login ID to be checked
     */
    private void checkLoginId(String loginId) {
        SqlPStatement statement = getSqlPStatement("SELECT_SYSTEM_ACCOUNT");
        statement.setString(1, loginId);

        if (!statement.retrieve().isEmpty()) {
            throw new ApplicationException(
                    MessageUtil.createMessage(MessageLevel.ERROR, "MSG00001"));
        }
    }

    /**
     * Checks whether the group ID is registered in the system.
     *
     * @param ugroupSystemAccount {@link UgroupSystemAccountEntity} containing the information to be checked
     */
    private void checkGroupId(
            UgroupSystemAccountEntity ugroupSystemAccount) {

        SqlPStatement statement = getSqlPStatement("SELECT_UGROUP");
        statement.setString(1, ugroupSystemAccount.getUgroupId());
        SqlResultSet result = statement.retrieve();
        if (result.isEmpty()) {
            throw new ApplicationException(
                    MessageUtil.createMessage(MessageLevel.ERROR, "MSG00002",
                            MessageUtil.getStringResource("S0020001")));
        }
    }

    /**
     * Checks whether the use case ID is registered in the system.
     *
     * @param systemAccount {@link SystemAccountEntity} containing the information to be checked
     */
    private void checkUseCaseId(SystemAccountEntity systemAccount) {
        SqlPStatement statement = getSqlPStatement("SELECT_USE_CASE");
        for (String useCaseId : systemAccount.getUseCase()) {
            statement.setString(1, useCaseId);
            SqlResultSet result = statement.retrieve();
            if (result.isEmpty()) {
                throw new ApplicationException(
                        MessageUtil.createMessage(MessageLevel.ERROR,
                                "MSG00002", MessageUtil.getStringResource(
                                "S0030001")));
            }
        }
    }


    /**
     * One registration is made in the system account table. <br>
     *
     * @param systemAccount {@link SystemAccountEntity} containing the information to be checked
     */
    private void registerSystemAccount(SystemAccountEntity systemAccount) {
        ParameterizedSqlPStatement statement =
                getParameterizedSqlStatement("INSERT_SYSTEM_ACCOUNT");

        try {
            // An exception is returned if the same login ID is already registered as a system account.
            statement.executeUpdateByObject(systemAccount);
        } catch (DuplicateStatementException de) {
            throw new ApplicationException(
                    MessageUtil.createMessage(MessageLevel.ERROR, "MSG00001"));
        }
    }


    /**
     * One user entity registration is made.
     *
     * @param users {@link UsersEntity} containing the information to be checked
     */
    private void registerUsers(UsersEntity users) {
        ParameterizedSqlPStatement statement = getParameterizedSqlStatement(
                "INSERT_USERS");
        statement.executeUpdateByObject(users);
    }


    /**
     * One group system account registration is made.
     *
     * @param ugroupSystemAccount Group system account entity class in which registration details are set
     */
    private void registerUgroupSystemAccount(
            UgroupSystemAccountEntity ugroupSystemAccount) {

        ParameterizedSqlPStatement statement = getParameterizedSqlStatement(
                "INSERT_UGROUP_SYSTEM_ACCOUNT");
        statement.executeUpdateByObject(ugroupSystemAccount);
    }


    /**
     * Registered as system account authority.
     *
     * @param systemAccount System account
     */
    private void registerSystemAccountAuthority(
            SystemAccountEntity systemAccount) {

        SystemAccountAuthorityEntity sysAcctAuthEntity =
                new SystemAccountAuthorityEntity();
        systemAccount.setUserId(systemAccount.getUserId());

        ParameterizedSqlPStatement statement = getParameterizedSqlStatement(
                "INSERT_SYSTEM_ACCOUNT_AUTHORITY");

        for (String useCase : systemAccount.getUseCase()) {
            sysAcctAuthEntity.setUseCaseId(useCase);
            statement.addBatchObject(sysAcctAuthEntity);
        }
        statement.executeBatch();
    }
}
