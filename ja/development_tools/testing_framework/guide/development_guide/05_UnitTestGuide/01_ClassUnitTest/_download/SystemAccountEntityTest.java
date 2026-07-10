package nablarch.sample.management.user;

import org.junit.jupiter.api.Test;

import nablarch.test.core.db.EntityTestSupport;
import nablarch.test.junit5.extension.db.EntityTest;

/**
 * SystemAccountEntityクラスに対するテストを実行するクラス。<br/>
 * テスト内容はエクセルシート参照のこと。
 *
 * @author Miki Habu
 * @since 1.0
 */
@EntityTest
class SystemAccountEntityTest {

    /** テスト対象エンティティクラス */
    private static final Class<SystemAccountEntity> ENTITY_CLASS = SystemAccountEntity.class;

    /** テストサポートクラス（インスタンスは拡張機能がインジェクションする）。 */
    EntityTestSupport support;

    /** {@link SystemAccountEntity#validateForRegisterUser(nablarch.core.validation.ValidationContext)} のテスト。 */
    @Test
    void testValidateForRegisterUser() {
        String sheetName = "testValidateForRegisterUser";
        String validateFor = "registerUser";
        support.testValidateAndConvert(ENTITY_CLASS, sheetName, validateFor);
    }

    /**
     * 文字種および文字列長の単項目精査テストケース
     */
    @Test
    void testCharsetAndLength() {
        String sheetName = "testCharsetAndLength";
        String id = "charsetAndLength";
        support.testValidateCharsetAndLength(ENTITY_CLASS, sheetName, id);
    }

    /**
     * 単項目精査のテストケース（上記以外）
     */
    @Test
    void testSingleValidation() {
        String sheetName = "testSingleValidation";
        String id = "singleValidation";
        support.testSingleValidation(ENTITY_CLASS, sheetName, id);
    }

    /** setter、getterのテスト */
    @Test
    void testSetterAndGetter() {
        String sheetName = "testAccessor";
        String id = "testGetterAndSetter";
        support.testSetterAndGetter(ENTITY_CLASS, sheetName, id);
    }

    /** コンストラクタのテスト */
    @Test
    void testConstructor() {
        String sheetName = "testAccessor";
        String id = "testConstructor";
        support.testConstructorAndGetter(ENTITY_CLASS, sheetName, id);
    }

}
