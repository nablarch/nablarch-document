package com.nablarch.example.app.web.form;

import nablarch.test.core.db.EntityTestSupport;
import org.junit.Test;

/**
 * {@link UserRegistrationForm}に対するテストを実行するクラス。
 * テスト内容はExcelシート参照のこと。
 *
 * @author Takayuki Uchida
 * @since 1.0
 */
public class UserRegistrationFormTest extends EntityTestSupport {

    /**
     * テスト対象Formクラス。
     */
    private static final Class<?> TARGET_CLASS = UserRegistrationForm.class;

    /**
     * 文字種および文字列長の単項目精査テストケース
     */
    @Test
    public void testCharsetAndLength() {

        String sheetName = "testCharsetAndLength";

        String id = "charsetAndLength";

        testValidateCharsetAndLength(TARGET_CLASS, sheetName, id);
    }

    /**
     * 単項目精査のテストケース（上記以外）
     */
    @Test
    public void testSingleValidation() {

        String sheetName = "testSingleValidation";

        String id = "singleValidation";

        testSingleValidation(TARGET_CLASS, sheetName, id);
    }

    /**
     * 項目間精査のテストケース
     */
    @Test
    public void testWholeFormValidation() {

        String sheetName = "testWholeFormValidation";

        testBeanValidation(TARGET_CLASS, sheetName);
    }

    /**
     * setter、getterのテストケース
     */
    @Test
    public void testSetterAndGetter() {

        String sheetName = "testSetterAndGetter";

        String id = "setterAndGetter";

        testSetterAndGetter(TARGET_CLASS, sheetName, id);
    }
}
