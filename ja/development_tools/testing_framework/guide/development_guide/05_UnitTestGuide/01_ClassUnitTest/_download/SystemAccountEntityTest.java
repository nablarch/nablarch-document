package nablarch.sample.management.user;

import org.junit.Test;

import nablarch.test.core.db.EntityTestSupport;

/**
 * SystemAccountEntityクラスに対するテストを実行するクラス。<br/>
 * テスト内容はエクセルシート参照のこと。
 *
 * @author Miki Habu
 * @since 1.0
 */
public class SystemAccountEntityTest extends EntityTestSupport {

    /** テスト対象エンティティクラス */
    private static final Class<SystemAccountEntity> ENTITY_CLASS = SystemAccountEntity.class;

    /** {@link SystemAccountEntity#validateForRegisterUser(nablarch.core.validation.ValidationContext)} のテスト。 */
    @Test
    public void testValidateForRegisterUser() {
        String sheetName = "testValidateForRegisterUser";
        String validateFor = "registerUser";
        testValidateAndConvert(ENTITY_CLASS, sheetName, validateFor);
    }

    /**
     * 文字種および文字列長の単項目精査テストケース
     */
    @Test
    public void testCharsetAndLength() {
        String sheetName = "testCharsetAndLength";
        String id = "charsetAndLength";
        testValidateCharsetAndLength(ENTITY_CLASS, sheetName, id);
    }

    /**
     * 単項目精査のテストケース（上記以外）
     */
    @Test
    public void testSingleValidation() {
        String sheetName = "testSingleValidation";
        String id = "singleValidation";
        testSingleValidation(ENTITY_CLASS, sheetName, id);
    }

    /** setter、getterのテスト */
    @Test
    public void testSetterAndGetter() {
        String sheetName = "testAccessor";
        String id = "testGetterAndSetter";
        testSetterAndGetter(ENTITY_CLASS, sheetName, id);
    }

    /** コンストラクタのテスト */
    @Test
    public void testConstructor() {
        String sheetName = "testAccessor";
        String id = "testConstructor";
        testConstructorAndGetter(ENTITY_CLASS, sheetName, id);
    }

}
