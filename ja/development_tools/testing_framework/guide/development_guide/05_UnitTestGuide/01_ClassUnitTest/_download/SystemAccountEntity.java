package nablarch.sample.ss11.entity;

import java.sql.Timestamp;
import java.util.Map;

import nablarch.core.db.statement.autoproperty.CurrentDateTime;
import nablarch.core.db.statement.autoproperty.UserId;
import nablarch.core.validation.PropertyName;
import nablarch.core.validation.ValidateFor;
import nablarch.core.validation.ValidationContext;
import nablarch.core.validation.ValidationUtil;
import nablarch.core.validation.convertor.Digits;
import nablarch.core.validation.validator.AsciiChar;
import nablarch.core.validation.validator.Length;
import nablarch.core.validation.validator.NumberChar;
import nablarch.core.validation.validator.NumberRange;
import nablarch.core.validation.validator.Required;

/**
 * システムアカウントテーブルの情報を保持するクラス。<br>
 *
 * @author Miki Habu
 * @since 1.0
 */
public class SystemAccountEntity {

    /** 認可単位(権限設定)。 */
    private String[] permissionUnit;

    /** ユーザID。 */
    private String userId;

    /** ログインID。 */
    private String loginId;

    /** パスワード。 */
    private String password;

    /** ユーザIDロック。 */
    private String userIdLocked;

    /** パスワード有効期限。 */
    private String passwordExpirationDate;

    /** 認証失敗回数。 */
    private Integer failedCount;

    /** ユーザ有効期限(FROM)。 */
    private String effectiveDateFrom;

    /** ユーザ有効期限(TO)。 */
    private String effectiveDateTo;

    /** 登録者ID。 */
    @UserId
    private String insertUserId;

    /** 登録日時。 */
    @CurrentDateTime
    private Timestamp insertDate;

    /** 更新者ID。 */
    @UserId
    private String updatedUserId;

    /** 更新日時。 */
    @CurrentDateTime
    private Timestamp updatedDate;
    
    /** バージョン番号 */
    private Long version;

    /**
     * デフォルトコンストラクタ。
     */
    public SystemAccountEntity() {
    }

    /**
     * Mapを引数にとるコンストラクタ。
     *
     * @param params 項目名をキーとし、項目値を値とするMap
     */
    public SystemAccountEntity(Map<String, Object> params) {
        userId = (String) params.get("userId");
        loginId = (String) params.get("loginId");
        password = (String) params.get("password");
        userIdLocked = (String) params.get("userIdLocked");
        passwordExpirationDate = (String) params.get("passwordExpirationDate");
        failedCount = (Integer) params.get("failedCount");
        effectiveDateFrom = (String) params.get("effectiveDateFrom");
        effectiveDateTo = (String) params.get("effectiveDateTo");
        permissionUnit = (String[]) params.get("permissionUnit");
    }


    /**
     * 認可単位(権限設定)を取得する。
     *
     * @return 認可単位
     */
    public String[] getPermissionUnit() {
        return permissionUnit;
    }

    /**
     * 認可単位(権限設定)を設定する。
     *
     * @param permissionUnit 設定する認可単位(権限設定)
     */
    @PropertyName("認可単位ID")
    @NumberChar
    @Length(min = 10, max = 10)
    public void setPermissionUnit(String[] permissionUnit) {
        this.permissionUnit = permissionUnit;
    }

    /** ユーザ登録時にバリデーションを実施するプロパティ。 */
    private static final String[] REGISTER_USER_VALIDATE_PROPS = new String[]{
        "loginId", "permissionUnit"};

    /**
     * ユーザ登録時に実施するバリデーション。
     *
     * @param context バリデーションの実行に必要なコンテキスト
     */
    @ValidateFor("registerUser")
    public static void validateForRegisterUser(
            ValidationContext<SystemAccountEntity> context) {
        // userIdを無視してバリデーションを実行
        ValidationUtil.validate(context, REGISTER_USER_VALIDATE_PROPS);

        // 単項目精査でエラーの場合はここで戻る
        if (!context.isValid()) {
            return;
        }

    }

    /** メッセージ送信によるユーザ登録時にバリデーションを実施するプロパティ。 */
    private static final String[] SEND_USER_VALIDATE_PROPS = new String[]{"loginId"};

    /**
     * メッセージ送信によるユーザ登録時に実施するバリデーション。
     *
     * @param context バリデーションの実行に必要なコンテキスト
     */
    @ValidateFor("sendUser")
    public static void validateForSendUser(ValidationContext<SystemAccountEntity> context) {
        // 権限情報はバリデーション対象外
        ValidationUtil.validate(context, SEND_USER_VALIDATE_PROPS);
    }

    /** ユーザ更新時に実施するバリデーション */
    private static final String[] UPDATE_USER_VALIDATE_PROPS = new String[]{"userId", "loginId", "permissionUnit"};
    
    /**
     * ユーザ更新時に実施するバリデーション。
     * 
     * @param context バリデーションの実行に必要なコンテキスト
     */
    @ValidateFor("updateUser")
    public static void validateForUpdateUser(ValidationContext<SystemAccountEntity> context) {
        ValidationUtil.validate(context, UPDATE_USER_VALIDATE_PROPS);
    }
    
    /** 認可単位ID比較時に実施するバリデーション */
    private static final String[] COMPARE_PERMISSION_VALIDATE_PROPS = new String[]{"permissionUnit"};
    
    /**
     * 認可単位ID比較時に実施するバリデーション。
     * 
     * @param context バリデーションの実行に必要なコンテキスト
     */
    @ValidateFor("comparePermission")
    public static void validateForComparePermission(ValidationContext<SystemAccountEntity> context) {
        // 認可単位のみ精査
        ValidationUtil.validate(context, COMPARE_PERMISSION_VALIDATE_PROPS);
    }

    /** ユーザ情報取得時にバリデーションを実施するプロパティ。 */
    private static final String[] SELECT_USER_INFO_PROPS = new String[]{"userId"};

    /**
     * ユーザ情報取得時に実施するバリデーション。
     *
     * @param context バリデーションの実行に必要なコンテキスト
     */
    @ValidateFor({"selectUserInfo", "deleteUser"})
    public static void validateForSelectUserInfo(ValidationContext<SystemAccountEntity> context) {
        ValidationUtil.validate(context, SELECT_USER_INFO_PROPS);
    }
    
    /**
     * ユーザIDを取得する。
     *
     * @return ユーザID。
     */
    public String getUserId() {
        return userId;
    }

    /**
     * ユーザIDを設定する。
     *
     * @param userId 設定するユーザID。
     */
    @PropertyName("ユーザID")
    @Required
    @Length(min = 10, max = 10)
    @NumberChar
    public void setUserId(String userId) {
        this.userId = userId;
    }

    /**
     * ログインIDを取得する。
     *
     * @return ログインID。
     */
    public String getLoginId() {
        return loginId;
    }

    /**
     * ログインIDを設定する。
     *
     * @param loginId 設定するログインID。
     */
    @PropertyName("ログインID")
    @Required
    @Length(max = 20)
    @AsciiChar
    public void setLoginId(String loginId) {
        this.loginId = loginId;
    }

    /**
     * パスワードを取得する。
     *
     * @return パスワード。
     */
    public String getPassword() {
        return password;
    }

    /**
     * パスワードを設定する。
     *
     * @param password 設定するパスワード。
     */
    @PropertyName("パスワード")
    @Required
    @Length(max = 44)
    @AsciiChar
    public void setPassword(String password) {
        this.password = password;
    }

    /**
     * ユーザIDロックを取得する。
     *
     * @return ユーザIDロック。
     */
    public String getUserIdLocked() {
        return userIdLocked;
    }

    /**
     * ユーザIDロックを設定する。
     *
     * @param userIdLocked 設定するユーザIDロック。
     */
    @PropertyName("ユーザIDロック")
    @Required
    @NumberChar
    @Length(min = 1, max = 1)
    public void setUserIdLocked(String userIdLocked) {
        this.userIdLocked = userIdLocked;
    }

    /**
     * パスワード有効期限を取得する。
     *
     * @return パスワード有効期限。
     */
    public String getPasswordExpirationDate() {
        return passwordExpirationDate;
    }

    /**
     * パスワード有効期限を設定する。
     *
     * @param passwordExpirationDate 設定するパスワード有効期限。
     */
    @PropertyName("パスワード有効期限")
    @Required
    @Length(min = 8, max = 8)
    @NumberChar
    public void setPasswordExpirationDate(String passwordExpirationDate) {
        this.passwordExpirationDate = passwordExpirationDate;
    }

    /**
     * 認証失敗回数を取得する。
     *
     * @return 認証失敗回数。
     */
    public Integer getFailedCount() {
        return failedCount;
    }

    /**
     * 認証失敗回数を設定する。
     *
     * @param failedCount 設定する認証失敗回数。
     */
    @PropertyName("認証失敗回数")
    @Required
    @NumberRange(min = 0, max = 9)
    @Digits(integer = 1, fraction = 0)
    public void setFailedCount(Integer failedCount) {
        this.failedCount = failedCount;
    }

    /**
     * ユーザ有効期限(FROM)を取得する。
     *
     * @return ユーザ有効期限(FROM)。
     */
    public String getEffectiveDateFrom() {
        return effectiveDateFrom;
    }

    /**
     * ユーザ有効期限(FROM)を設定する。
     *
     * @param effectiveDateFrom 設定するユーザ有効期限(FROM)。
     */
    @PropertyName("ユーザ有効期限(FROM)")
    @Required
    @Length(min = 8, max = 8)
    @NumberChar
    public void setEffectiveDateFrom(String effectiveDateFrom) {
        this.effectiveDateFrom = effectiveDateFrom;
    }

    /**
     * ユーザ有効期限(TO)を取得する。
     *
     * @return ユーザ有効期限(TO)。
     */
    public String getEffectiveDateTo() {
        return effectiveDateTo;
    }

    /**
     * ユーザ有効期限(TO)を設定する。
     *
     * @param effectiveDateTo 設定するユーザ有効期限(TO)。
     */
    @PropertyName("ユーザ有効期限(TO)")
    @Required
    @Length(min = 8, max = 8)
    @NumberChar
    public void setEffectiveDateTo(String effectiveDateTo) {
        this.effectiveDateTo = effectiveDateTo;
    }

    /**
     * 登録者IDを取得する。
     *
     * @return 登録者ID。
     */
    public String getInsertUserId() {
        return insertUserId;
    }

    /**
     * 登録者IDを設定する。
     *
     * @param insertUserId 設定する登録者ID。
     */
    @PropertyName("登録者ID")
    @Required
    @Length(min = 10, max = 10)
    @NumberChar
    public void setInsertUserId(String insertUserId) {
        this.insertUserId = insertUserId;
    }

    /**
     * 登録日時を取得する。
     *
     * @return 登録日時。
     */
    public Timestamp getInsertDate() {
        return insertDate;
    }

    /**
     * 登録日時を設定する。
     *
     * @param insertDate 設定する登録日時。
     */
    @PropertyName("登録日時")
    @Required
    public void setInsertDate(Timestamp insertDate) {
        this.insertDate = insertDate;
    }

    /**
     * 更新者IDを取得する。
     *
     * @return 更新者ID。
     */
    public String getUpdatedUserId() {
        return updatedUserId;
    }

    /**
     * 更新者IDを設定する。
     *
     * @param updatedUserId 設定する更新者ID。
     */
    @PropertyName("更新者ID")
    @Required
    @Length(min = 10, max = 10)
    @NumberChar
    public void setUpdatedUserId(String updatedUserId) {
        this.updatedUserId = updatedUserId;
    }

    /**
     * 更新日時を取得する。
     *
     * @return 更新日時。
     */
    public Timestamp getUpdatedDate() {
        return updatedDate;
    }

    /**
     * 更新日時を設定する。
     *
     * @param updatedDate 設定する更新日時。
     */
    @PropertyName("更新日時")
    @Required
    public void setUpdatedDate(Timestamp updatedDate) {
        this.updatedDate = updatedDate;
    }

    /**
     * バージョン番号を取得する。
     * @return バージョン番号
     */
    public Long getVersion() {
        return version;
    }

    /**
     * バージョン番号を設定する。
     * @param version バージョン番号
     */
    @NumberRange(min = 0, max = 999999999)
    @Digits(integer = 10, fraction = 0)
    public void setVersion(Long version) {
        this.version = version;
    }
}

