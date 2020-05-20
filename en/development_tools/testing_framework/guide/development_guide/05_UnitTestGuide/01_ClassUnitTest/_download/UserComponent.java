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
 * ユーザ登録に関するサービスクラス<br/>
 *
 * @author Tsuyoshi Kawasaki
 * @since 1.0
 */
public class UserComponent extends DbAccessSupport {

    /** ユーザーIDロックの状態:アンロック */
    private static final String USER_ID_NOT_LOCKED = "0";

    /** パスワード失敗回数の初期値 */
    private static final int INITIAL_FAILED_COUNT = 0;

    /**
     * ユーザグループの検索を実行する。
     *
     * @return 検索結果
     */
    public SqlResultSet selectUserGroups() {
        SqlPStatement statement = getSqlPStatement("SELECT_ALL_UGROUPS");
        return statement.retrieve();
    }

    /**
     * ユースケーステーブルに登録されている全てのユースケースIDと名称を取得する。
     *
     * @return 検索結果。ユースケースIDの昇順でソート
     */
    public SqlResultSet getAllUseCase() {
        SqlPStatement statement = getSqlPStatement("SELECT_ALL_USE_CASES");
        return statement.retrieve();
    }

    /**
     * ユーザ登録時の入力内容のチェックを行う。<br>
     * チェックOKの場合は、名称も取得する。
     *
     * @param systemAccount チェック対象の情報を保持した{@link SystemAccountEntity}
     * @param ugroupSystemAccount チェック対象の情報を保持した{@link UgroupSystemAccountEntity}
     */
    public void checkForRegisterUser(SystemAccountEntity systemAccount,
            UgroupSystemAccountEntity ugroupSystemAccount) {

        // ログインIDのチェック
        checkLoginId(systemAccount.getLoginId());
        // グループIDのチェック
        checkGroupId(ugroupSystemAccount);
        // ユースケースIDのチェック
        if (systemAccount.getUseCase() != null) {
            checkUseCaseId(systemAccount);
        }
    }

    /**
     * ユーザを登録する。
     *
     * @param systemAccount 画面入力された情報を持つ{@link SystemAccountEntity}
     * @param users 画面入力された情報を持つ{@link UsersEntity}
     * @param ugroupSystemAccount 画面入力された情報を持つ{@link UgroupSystemAccountEntity}
     */
    public void registerUser(SystemAccountEntity systemAccount,
            UsersEntity users,
            UgroupSystemAccountEntity ugroupSystemAccount) {

        // 日付の取得
        // ユーザIDを採番する
        String userId = IdGeneratorUtil.generateUserId();
        // 現在(システム)日付
        String current = BusinessDateUtil.getDate();
        // 1カ月後(パスワードの有効期限)
        String passwordExpirationDate = DateUtil.addMonth(current, 1);
        // 12カ月後(ユーザの有効期限)
        String userEffectiveDateTo = DateUtil.addMonth(current, 12);

        // システムアカウントの登録
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

        // ユーザエンティティの登録
        users.setUserId(userId);
        registerUsers(users);

        // グループシステムアカウントの登録
        ugroupSystemAccount.setUserId(userId);
        ugroupSystemAccount.setEffectiveDateFrom(current);
        ugroupSystemAccount.setEffectiveDateTo(userEffectiveDateTo);
        registerUgroupSystemAccount(ugroupSystemAccount);

        // システムアカウント権限の登録
        if (systemAccount.getUseCase() != null
                && systemAccount.getUseCase().length != 0) {
            registerSystemAccountAuthority(systemAccount);
        }
    }

    /**
     * ログインIDが既に登録されていないかチェックする。
     *
     * @param loginId チェック対象のログインID
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
     * グループIDがシステムに登録されているかチェックする。
     *
     * @param ugroupSystemAccount チェック対象の情報を保持した{@link UgroupSystemAccountEntity}
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
     * ユースケースIDがシステムに登録されているかチェックする。
     *
     * @param systemAccount チェック対象の上方を保持した{@link SystemAccountEntity}
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
     * システムアカウントテーブルに1件登録する。<br>
     *
     * @param systemAccount 登録する情報を保持した{@link SystemAccountEntity}
     */
    private void registerSystemAccount(SystemAccountEntity systemAccount) {
        ParameterizedSqlPStatement statement =
                getParameterizedSqlStatement("INSERT_SYSTEM_ACCOUNT");

        try {
            // システムアカウントに同じログインIDで既に登録されていたら例外を返す。
            statement.executeUpdateByObject(systemAccount);
        } catch (DuplicateStatementException de) {
            throw new ApplicationException(
                    MessageUtil.createMessage(MessageLevel.ERROR, "MSG00001"));
        }
    }


    /**
     * ユーザエンティティに1件登録する。
     *
     * @param users 登録する情報を保持した{@link UsersEntity}
     */
    private void registerUsers(UsersEntity users) {
        ParameterizedSqlPStatement statement = getParameterizedSqlStatement(
                "INSERT_USERS");
        statement.executeUpdateByObject(users);
    }


    /**
     * グループシステムアカウントに1件登録する。
     *
     * @param ugroupSystemAccount 登録内容が設定されたグループシステムアカウントエンティティクラス
     */
    private void registerUgroupSystemAccount(
            UgroupSystemAccountEntity ugroupSystemAccount) {

        ParameterizedSqlPStatement statement = getParameterizedSqlStatement(
                "INSERT_UGROUP_SYSTEM_ACCOUNT");
        statement.executeUpdateByObject(ugroupSystemAccount);
    }


    /**
     * システムアカウント権限に登録する。
     *
     * @param systemAccount システムアカウント
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
