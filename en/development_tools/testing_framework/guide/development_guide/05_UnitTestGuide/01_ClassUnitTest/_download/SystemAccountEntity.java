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
 * Class to retain information from the system account table. <br>
 *
 * @author Miki Habu
 * @since 1.0
 */
public class SystemAccountEntity {

    /** Certification unit (authority setting). */
    private String[] permissionUnit;

    /** User ID. */
    private String userId;

    /** Login ID. */
    private String loginId;

    /** Password. */
    private String password;

    /** User ID lock. */
    private String userIdLocked;

    /** Expiration date of password. */
    private String passwordExpirationDate;

    /** Number of authentication failures. */
    private Integer failedCount;

    /** User validity period (FROM). */
    private String effectiveDateFrom;

    /** User validity period (TO). */
    private String effectiveDateTo;

    /** Registration ID. */
    @UserId
    private String insertUserId;

    /** Registration date/time. */
    @CurrentDateTime
    private Timestamp insertDate;

    /** ID of updated user. */
    @UserId
    private String updatedUserId;

    /** Date/time of update. */
    @CurrentDateTime
    private Timestamp updatedDate;

    /** Version number */
    private Long version;

    /**
     * Default constructor.
     */
    public SystemAccountEntity() {
    }

    /**
     * Constructor to take maps as arguments.
     *
     * @param params Map using the item name as the key and the item value as the value
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
     * Acquires certification unit (authority setting).
     *
     * @return Certification unit
     */
    public String[] getPermissionUnit() {
        return permissionUnit;
    }

    /**
     * Set certification unit (authority setting).
     *
     * @param permissionUnit Certification unit to be set (authority setting)
     */
    @PropertyName("認可単位ID") // Certification unit ID
    @NumberChar
    @Length(min = 10, max = 10)
    public void setPermissionUnit(String[] permissionUnit) {
        this.permissionUnit = permissionUnit;
    }

    /** Property to be validated during user registration. */
    private static final String[] REGISTER_USER_VALIDATE_PROPS = new String[]{ "loginId", "permissionUnit" };

    /**
     * Validation performed during user registration.
     *
     * @param context Context required for validation
     */
    @ValidateFor("registerUser")
    public static void validateForRegisterUser(
            ValidationContext<SystemAccountEntity> context) {
        // Ignores userId and performs validation
        ValidationUtil.validate(context, REGISTER_USER_VALIDATE_PROPS);

        // Goes back at this point if an error occurs when scanning an item
        if (!context.isValid()) {
            return;
        }

    }

    /** Property to be validated by sending a message during user registration. */
    private static final String[] SEND_USER_VALIDATE_PROPS = new String[]{"loginId"};

    /**
     /** Validation performed by sending a message during user registration.
     *
     * @param context Context required for validation
     */
    @ValidateFor("sendUser")
    public static void validateForSendUser(ValidationContext<SystemAccountEntity> context) {
        // Authority information is not subject to validation
        ValidationUtil.validate(context, SEND_USER_VALIDATE_PROPS);
    }

    /** Validation performed during user update */
    private static final String[] UPDATE_USER_VALIDATE_PROPS = new String[]{"userId", "loginId", "permissionUnit"};
    
    /**
     * Validation performed during user update.
     *
     * @param context Context required for validation
     */
    @ValidateFor("updateUser")
    public static void validateForUpdateUser(ValidationContext<SystemAccountEntity> context) {
        ValidationUtil.validate(context, UPDATE_USER_VALIDATE_PROPS);
    }

    /** Validation performed during comparison of certification unit IDs */
    private static final String[] COMPARE_PERMISSION_VALIDATE_PROPS = new String[]{"permissionUnit"};
    
    /**
     * Validation performed during comparison of certification unit IDs.
     *
     * @param context Context required for validation
     */
    @ValidateFor("comparePermission")
    public static void validateForComparePermission(ValidationContext<SystemAccountEntity> context) {
        // Only certification units are scanned
        ValidationUtil.validate(context, COMPARE_PERMISSION_VALIDATE_PROPS);
    }

    /** Property to be validated when acquiring user information. */
    private static final String[] SELECT_USER_INFO_PROPS = new String[]{"userId"};

    /**
     * Validation performed when acquiring user information.
     *
     * @param context Context required for validation
     */
    @ValidateFor({"selectUserInfo", "deleteUser"})
    public static void validateForSelectUserInfo(ValidationContext<SystemAccountEntity> context) {
        ValidationUtil.validate(context, SELECT_USER_INFO_PROPS);
    }
    
    /**
     * Acquires user ID.
     *
     * @return User ID.
     */
    public String getUserId() {
        return userId;
    }

    /**
     * Set user ID.
     *
     * @param userId User ID to be set.
     */
    @PropertyName("ユーザID") // User ID
    @Required
    @Length(min = 10, max = 10)
    @NumberChar
    public void setUserId(String userId) {
        this.userId = userId;
    }

    /**
     * Acquires login ID.
     *
     * @return Login ID.
     */
    public String getLoginId() {
        return loginId;
    }

    /**
     * Set login ID.
     *
     * @param loginId Login ID to be set.
     */
    @PropertyName("ログインID") // Login ID
    @Required
    @Length(max = 20)
    @AsciiChar
    public void setLoginId(String loginId) {
        this.loginId = loginId;
    }

    /**
     * Acquires password.
     *
     * @return Password.
     */
    public String getPassword() {
        return password;
    }

    /**
     * Set password.
     *
     * @param password Password to be set.
     */
    @PropertyName("パスワード") // Password
    @Required
    @Length(max = 44)
    @AsciiChar
    public void setPassword(String password) {
        this.password = password;
    }

    /**
     * Acquires user ID lock.
     *
     * @return User ID lock.
     */
    public String getUserIdLocked() {
        return userIdLocked;
    }

    /**
     * Set user ID lock.
     *
     * @param userIdLocked User ID lock to be set.
     */
    @PropertyName("ユーザIDロック") // User ID lock
    @Required
    @NumberChar
    @Length(min = 1, max = 1)
    public void setUserIdLocked(String userIdLocked) {
        this.userIdLocked = userIdLocked;
    }

    /**
     * Acquires expiry date of password.
     *
     * @return Expiration date of password.
     */
    public String getPasswordExpirationDate() {
        return passwordExpirationDate;
    }

    /**
     * Set expiration date of password.
     *
     * @param passwordExpirationDate Password expiration date to be set.
     */
    @PropertyName("パスワード有効期限") // Expiration date of password
    @Required
    @Length(min = 8, max = 8)
    @NumberChar
    public void setPasswordExpirationDate(String passwordExpirationDate) {
        this.passwordExpirationDate = passwordExpirationDate;
    }

    /**
     * Acquires number of authentication failures.
     *
     * @return Number of authentication failures.
     */
    public Integer getFailedCount() {
        return failedCount;
    }

    /**
     * Set number of authentication failures.
     *
     * @param failedCount Number of authentication failures to be set.
     */
    @PropertyName("認証失敗回数") // Number of authentication failures
    @Required
    @NumberRange(min = 0, max = 9)
    @Digits(integer = 1, fraction = 0)
    public void setFailedCount(Integer failedCount) {
        this.failedCount = failedCount;
    }

    /**
     * Acquires user validity period (FROM).
     *
     * @return User validity period (FROM).
     */
    public String getEffectiveDateFrom() {
        return effectiveDateFrom;
    }

    /**
     * Set user validity period (FROM).
     *
     * @param effectiveDateFrom User validity period (FROM) to be set.
     */
    @PropertyName("ユーザ有効期限(FROM)") // User validity period (FROM)
    @Required
    @Length(min = 8, max = 8)
    @NumberChar
    public void setEffectiveDateFrom(String effectiveDateFrom) {
        this.effectiveDateFrom = effectiveDateFrom;
    }

    /**
     * Acquires user validity period (TO).
     *
     * @return User validity period (TO).
     */
    public String getEffectiveDateTo() {
        return effectiveDateTo;
    }

    /**
     * Set user validity period (TO).
     *
     * @param effectiveDateTo User validity period (TO) to be set.
     */
    @PropertyName("ユーザ有効期限(TO)") // User validity period (TO)
    @Required
    @Length(min = 8, max = 8)
    @NumberChar
    public void setEffectiveDateTo(String effectiveDateTo) {
        this.effectiveDateTo = effectiveDateTo;
    }

    /**
     * Acquires ID of registered user.
     *
     * @return Registered user ID.
     */
    public String getInsertUserId() {
        return insertUserId;
    }

    /**
     * Sets ID of registered user.
     *
     * @param insertUserId ID of registered user.
     */
    @PropertyName("登録者ID") // Registered user ID
    @Required
    @Length(min = 10, max = 10)
    @NumberChar
    public void setInsertUserId(String insertUserId) {
        this.insertUserId = insertUserId;
    }

    /**
     * Acquires registration date/time.
     *
     * @return Registration date/time.
     */
    public Timestamp getInsertDate() {
        return insertDate;
    }

    /**
     * Set registration date/time.
     *
     * @param insertDate Registration date/time to be set.
     */
    @PropertyName("登録日時") // Registration date/time
    @Required
    public void setInsertDate(Timestamp insertDate) {
        this.insertDate = insertDate;
    }

    /**
     * Acquires ID of updated user.
     *
     * @return ID of updated user.
     */
    public String getUpdatedUserId() {
        return updatedUserId;
    }

    /**
     * Set ID of updated user.
     *
     * @param updatedUserId Updated user ID to be set.
     */
    @PropertyName("更新者ID") // ID of updated user
    @Required
    @Length(min = 10, max = 10)
    @NumberChar
    public void setUpdatedUserId(String updatedUserId) {
        this.updatedUserId = updatedUserId;
    }

    /**
     * Acquires date/time of update.
     *
     * @return Date/time of update.
     */
    public Timestamp getUpdatedDate() {
        return updatedDate;
    }

    /**
     * Set date/time of update.
     *
     * @param updatedDate Update date/time to be set.
     */
    @PropertyName("更新日時") // Date/time of update
    @Required
    public void setUpdatedDate(Timestamp updatedDate) {
        this.updatedDate = updatedDate;
    }

    /**
     * Acquires version number.
     * @return Version number
     */
    public Long getVersion() {
        return version;
    }

    /**
     * Sets version number.
     * @param version Version number
     */
    @NumberRange(min = 0, max = 999999999)
    @Digits(integer = 10, fraction = 0)
    public void setVersion(Long version) {
        this.version = version;
    }
}

