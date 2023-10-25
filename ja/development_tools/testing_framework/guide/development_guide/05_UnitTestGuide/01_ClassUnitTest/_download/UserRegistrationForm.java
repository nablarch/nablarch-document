package com.nablarch.example.app.web.form;

import nablarch.core.util.StringUtil;
import nablarch.core.validation.ee.DateFormat;
import nablarch.core.validation.ee.Length;
import nablarch.core.validation.ee.Required;
import nablarch.core.validation.ee.SystemChar;

import jakarta.validation.constraints.AssertTrue;
import jakarta.validation.groups.Default;

/**
 * ユーザー登録情報のフォーム。
 * @author Takayuki Uchida
 */
public class UserRegistrationForm {

    /**
     * ユーザー名。
     */
    @Required(groups = {Default.class, ForEnglish.class})
    @Length(min = 5, max = 50, message = "{min}文字以上{max}文字以下で入力してください。", groups = {Default.class, ForEnglish.class})
    @SystemChar(charsetDef = "半角英数", message = "{charsetDef}で入力してください。", groups = {Default.class, ForEnglish.class})
    private String userName;

    /**
     * パスワード。
     */
    @Required(message = "パスワードは入力必須です。", groups = {Default.class, ForEnglish.class})
    @Length(min = 8, groups = {Default.class, ForEnglish.class})
    @SystemChar(charsetDef = "システム許容文字", groups = {Default.class, ForEnglish.class})
    private String newPassword;

    /**
     * 確認用パスワード。
     */
    @Required(message = "パスワードは入力必須です。", groups = {Default.class, ForEnglish.class})
    @Length(min = 8, groups = {Default.class, ForEnglish.class})
    @SystemChar(charsetDef = "システム許容文字", groups = {Default.class, ForEnglish.class})
    private String confirmPassword;

    /**
     * 住所。
     */
    @Length(max = 100, groups = {Default.class, ForEnglish.class})
    @SystemChar.List({
            @SystemChar(charsetDef = "全角文字"),
            @SystemChar(charsetDef = "ASCII文字", groups = ForEnglish.class)
    })
    private String address;

    /**
     * 生年月日。
     */
    @DateFormat.List({
            @DateFormat,
            @DateFormat(value = "MM-dd-yyyy", groups = ForEnglish.class)
    })
    private String birthDay;

    /**
     * パスワードと確認用パスワードが同一であることを検証する。
     * @return {@code true} いずれかが空である場合、パスワードと確認用パスワードが同一である場合
     */
    @AssertTrue(message = "{test.CheckPassword.message}", groups = {Default.class, ForEnglish.class})
    public boolean isValidPassword() {
        if(StringUtil.isNullOrEmpty(newPassword) || StringUtil.isNullOrEmpty(confirmPassword)) {
            return true;
        }
        return confirmPassword.equals(newPassword);
    }

    /**
     * ユーザー名を取得する。
     *
     * @return ユーザー名
     */
    public String getUserName() {
        return userName;
    }

    /**
     * ユーザー名を設定する。
     *
     * @param userName ユーザー名
     */
    public void setUserName(String userName) {
        this.userName = userName;
    }

    /**
     * パスワードを取得する。
     *
     * @return パスワード
     */
    public String getNewPassword() {
        return newPassword;
    }

    /**
     * パスワードを設定する。
     *
     * @param newPassword パスワード
     */
    public void setNewPassword(String newPassword) {
        this.newPassword = newPassword;
    }

    /**
     * 確認用パスワードを取得する。
     *
     * @return 確認用パスワード
     */
    public String getConfirmPassword() {
        return confirmPassword;
    }

    /**
     * 確認用パスワードを設定する。
     * @param confirmPassword 確認用パスワード
     */
    public void setConfirmPassword(String confirmPassword) {
        this.confirmPassword = confirmPassword;
    }

    /**
     * 住所を取得する。
     * @return 住所
     */
    public String getAddress() {
        return address;
    }

    /**
     * 住所を設定する。
     * @param address 住所
     */
    public void setAddress(String address) {
        this.address = address;
    }

    /**
     * 誕生日を取得する。
     * @return 誕生日
     */
    public String getBirthDay() {
        return birthDay;
    }

    /**
     * 誕生日を設定する。
     * @param birthDay 誕生日
     */
    public void setBirthDay(String birthDay) {
        this.birthDay = birthDay;
    }

    /**
     * 英語圏向けであることを示すグループ用インタフェース。
     */
    public interface ForEnglish{}

}
