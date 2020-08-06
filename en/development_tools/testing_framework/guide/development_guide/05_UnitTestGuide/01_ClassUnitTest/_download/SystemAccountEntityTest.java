package nablarch.sample.management.user;

import org.junit.Test;

import nablarch.test.core.db.EntityTestSupport;

/**
 * Class for testing SystemAccountEntity classes. <br/>
 * Refer to the Excel sheet for details on the content of the test.
 *
 * @author Miki Habu
 * @since 1.0
 */
public class SystemAccountEntityTest extends EntityTestSupport {

    /** Tested entity class */
    private static final Class<SystemAccountEntity> ENTITY_CLASS = SystemAccountEntity.class;

    /** Test of {@link SystemAccountEntity#validateForRegisterUser(nablarch.core.validation.ValidationContext)}. */
    @Test
    public void testValidateForRegisterUser() {
        String sheetName = "testValidateForRegisterUser";
        String validateFor = "registerUser";
        testValidateAndConvert(ENTITY_CLASS, sheetName, validateFor);
    }

    /**
     * Test cases for single-item scanning of character type and character string length
     */
    @Test
    public void testCharsetAndLength() {
        String sheetName = "testCharsetAndLength";
        String id = "charsetAndLength";
        testValidateCharsetAndLength(ENTITY_CLASS, sheetName, id);
    }

    /**
     * Test cases for single-item scanning (other)
     */
    @Test
    public void testSingleValidation() {
        String sheetName = "testSingleValidation";
        String id = "singleValidation";
        testSingleValidation(ENTITY_CLASS, sheetName, id);
    }

    /** setter and getter testing */
    @Test
    public void testSetterAndGetter() {
        String sheetName = "testAccessor";
        String id = "testGetterAndSetter";
        testSetterAndGetter(ENTITY_CLASS, sheetName, id);
    }

    /** Constructor testing */
    @Test
    public void testConstructor() {
        String sheetName = "testAccessor";
        String id = "testConstructor";
        testConstructorAndGetter(ENTITY_CLASS, sheetName, id);
    }

}
