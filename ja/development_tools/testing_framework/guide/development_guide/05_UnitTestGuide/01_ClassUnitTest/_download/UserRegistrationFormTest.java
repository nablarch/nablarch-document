package com.nablarch.example.app.web.form;

import nablarch.test.core.db.EntityTestSupport;
import nablarch.test.junit5.extension.db.EntityTest;
import org.junit.jupiter.api.Test;

/**
 * {@link UserRegistrationForm}に対するテストを実行するクラス。
 * テスト内容はExcelシート参照のこと。
 *
 * @author Takayuki Uchida
 * @since 1.0
 */
@EntityTest
class UserRegistrationFormTest {

    /**
     * テスト対象Formクラス。
     */
    private static final Class<?> TARGET_CLASS = UserRegistrationForm.class;

    /** テストサポートクラス（インスタンスは拡張機能がインジェクションする）。 */
    EntityTestSupport support;

    /**
     * 文字種および文字列長の単項目精査テストケース
     */
    @Test
    void testCharsetAndLength() {

        String sheetName = "testCharsetAndLength";

        String id = "charsetAndLength";

        support.testValidateCharsetAndLength(TARGET_CLASS, sheetName, id);
    }

    /**
     * 単項目精査のテストケース（上記以外）
     */
    @Test
    void testSingleValidation() {

        String sheetName = "testSingleValidation";

        String id = "singleValidation";

        support.testSingleValidation(TARGET_CLASS, sheetName, id);
    }

    /**
     * 項目間精査のテストケース
     */
    @Test
    void testWholeFormValidation() {

        String sheetName = "testWholeFormValidation";

        support.testBeanValidation(TARGET_CLASS, sheetName);
    }

    /**
     * setter、getterのテストケース
     */
    @Test
    void testSetterAndGetter() {

        String sheetName = "testSetterAndGetter";

        String id = "setterAndGetter";

        support.testSetterAndGetter(TARGET_CLASS, sheetName, id);
    }
}
