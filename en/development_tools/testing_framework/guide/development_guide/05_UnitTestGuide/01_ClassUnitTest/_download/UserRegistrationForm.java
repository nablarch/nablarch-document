package com.nablarch.example.app.web.form;

import nablarch.core.util.StringUtil;
import nablarch.core.validation.ee.DateFormat;
import nablarch.core.validation.ee.Length;
import nablarch.core.validation.ee.Required;
import nablarch.core.validation.ee.SystemChar;

import javax.validation.constraints.AssertTrue;
import javax.validation.groups.Default;

/**
 * User Registration Information Form.
 * @author Takayuki Uchida
 */
public class UserRegistrationForm {

    /**
     * User name.
     */
    @Required(groups = {Default.class, ForEnglish.class})
    @Length(min = 5, max = 50, message = "{min}文字以上{max}文字以下で入力してください。", groups = {Default.class, ForEnglish.class})
    @SystemChar(charsetDef = "半角英数", message = "{charsetDef}で入力してください。", groups = {Default.class, ForEnglish.class})
    private String userName;

    /**
     * Password.
     */
    @Required(message = "パスワードは入力必須です。", groups = {Default.class, ForEnglish.class})
    @Length(min = 8, groups = {Default.class, ForEnglish.class})
    @SystemChar(charsetDef = "システム許容文字", groups = {Default.class, ForEnglish.class})
    private String newPassword;

    /**
     * Confirm password.
     */
    @Required(message = "パスワードは入力必須です。", groups = {Default.class, ForEnglish.class})
    @Length(min = 8, groups = {Default.class, ForEnglish.class})
    @SystemChar(charsetDef = "システム許容文字", groups = {Default.class, ForEnglish.class})
    private String confirmPassword;

    /**
     * Address.
     */
    @Length(max = 100, groups = {Default.class, ForEnglish.class})
    @SystemChar.List({
            @SystemChar(charsetDef = "全角文字"),
            @SystemChar(charsetDef = "ASCII文字", groups = ForEnglish.class)
    })
    private String address;

    /**
     * Birthday
     */
    @DateFormat.List({
            @DateFormat,
            @DateFormat(value = "MM-dd-yyyy", groups = ForEnglish.class)
    })
    private String birthDay;

    /**
     * Verify that the password and confirmation password are identical.
     * @return {@code true} If either is empty, or if the password and confirmation password are the same
     */
    @AssertTrue(message = "{test.CheckPassword.message}", groups = {Default.class, ForEnglish.class})
    public boolean isValidPassword() {
        if(StringUtil.isNullOrEmpty(newPassword) || StringUtil.isNullOrEmpty(confirmPassword)) {
            return true;
        }
        return confirmPassword.equals(newPassword);
    }

    /**
     * Get the user name.
     *
     * @return user name
     */
    public String getUserName() {
        return userName;
    }

    /**
     * Set the user name.
     *
     * @param userName user name
     */
    public void setUserName(String userName) {
        this.userName = userName;
    }

    /**
     * Get the password.
     *
     * @return password
     */
    public String getNewPassword() {
        return newPassword;
    }

    /**
     * Set the password.
     *
     * @param newPassword password
     */
    public void setNewPassword(String newPassword) {
        this.newPassword = newPassword;
    }

    /**
     * Get the confirm password.
     *
     * @return confirm password
     */
    public String getConfirmPassword() {
        return confirmPassword;
    }

    /**
     * Set the confirm password.
     *
     * @param confirmPassword confirm password
     */
    public void setConfirmPassword(String confirmPassword) {
        this.confirmPassword = confirmPassword;
    }

    /**
     * Get the address.
     *
     * @return address address
     */
    public String getAddress() {
        return address;
    }

    /**
     * Set the address.
     *
     * @param address address.
     */
    public void setAddress(String address) {
        this.address = address;
    }

    /**
     * Get the birthday.
     * @return birthday
     */
    public String getBirthDay() {
        return birthDay;
    }

    /**
     * Set the birthday
     *
     * @param birthDay birthday
     */
    public void setBirthDay(String birthDay) {
        this.birthDay = birthDay;
    }

    /**
     * An interface for groups indicating that it is intended for English-speaking countries.
     */
    public interface ForEnglish{}

}
