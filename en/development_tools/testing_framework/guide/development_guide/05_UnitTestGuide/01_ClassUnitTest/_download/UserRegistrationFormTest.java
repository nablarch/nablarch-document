package com.nablarch.example.app.web.form;

import nablarch.test.core.db.EntityTestSupport;
import org.junit.Test;

/**
 * Class that executes tests for the {@link UserRegistrationForm} class. <br/>
 * Refer to the Excel sheet for test content.
 *
 * @author Takayuki Uchida
 * @since 1.0
 */
public class UserRegistrationFormTest extends EntityTestSupport {

    /**
     * Form class to be tested
     */
    private static final Class<?> TARGET_CLASS = UserRegistrationForm.class;

    /**
     * Test cases for character type and string length
     */
    @Test
    public void testCharsetAndLength() {

        String sheetName = "testCharsetAndLength";

        String id = "charsetAndLength";

        testValidateCharsetAndLength(TARGET_CLASS, sheetName, id);
    }

    /**
     * Test cases for single item validation (not listed above)
     */
    @Test
    public void testSingleValidation() {

        String sheetName = "testSingleValidation";

        String id = "singleValidation";

        testSingleValidation(TARGET_CLASS, sheetName, id);
    }

    /**
     * Test cases for validation between items
     */
    @Test
    public void testWholeFormValidation() {

        String sheetName = "testWholeFormValidation";

        testBeanValidation(TARGET_CLASS, sheetName);
    }

    /**
     * test case for setter and getter
     */
    @Test
    public void testSetterAndGetter() {

        String sheetName = "testSetterAndGetter";

        String id = "setterAndGetter";

        testSetterAndGetter(TARGET_CLASS, sheetName, id);
    }
}
