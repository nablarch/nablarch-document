package nablarch.sample.management.user;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import nablarch.core.db.statement.SqlResultSet;
import nablarch.core.message.ApplicationException;
import nablarch.test.core.db.DbAccessTestSupport;

import org.junit.Test;

/**
 * Test class of {@link UserComponentTest}.
 *
 * @author Tsuyoshi Kawasaki
 * @since 1.0
 */
public class UserComponentTest extends DbAccessTestSupport {

    /** Class to be tested */
    private UserComponent target = new UserComponent();
    

    /**
     * Test 1 of {@link UserComponent#registerUser()}. <br>
     * Normal system.
     */
    @Test
    public void testRegisterUser1() {
        String sheetName = "registerUser";
                
        setThreadContextValues(sheetName, "threadContext");
        
        List<Map<String, String>> sysAcctDatas = getListMap(sheetName, "sysAcctEntity");
        List<Map<String, String>> usersDatas = getListMap(sheetName, "usersEntity");
        List<Map<String, String>> grpSysAcctDatas = getListMap(sheetName, "grpSysAcctEntity");
        // Map and list to temporarily receive Excel data
        Map<String, Object> work = new HashMap<String, Object>();
        List<Map<String, String>> useCaseData = null;
        
        SystemAccountEntity sysAcct = null;
        UsersEntity users = null;
        UgroupSystemAccountEntity grpSysAcct = null;
        for (int i = 0; i < sysAcctDatas.size(); i++) {

            // Database preparation
            setUpDb(sheetName);

            // System account
            work.clear();
            for (Entry<String, String> e : sysAcctDatas.get(i).entrySet()) {
                work.put(e.getKey(), e.getValue());
            }
            // Creation of use case ID arguments
            String id = sysAcctDatas.get(i).get("useCaseId");
            useCaseData = getListMap(sheetName, id);
            String[] useCaseId = new String[useCaseData.size()];
            for (int j = 0; j < useCaseData.size(); j++) {
                useCaseId[j] = useCaseData.get(j).get("useCaseId");
            }
            work.put("useCase", useCaseId);
            sysAcct = new SystemAccountEntity(work);

            // User
            work.clear();
            for (Entry<String, String> e : usersDatas.get(i).entrySet()) {
                work.put(e.getKey(), e.getValue());
            }
            users = new UsersEntity(work);

            // Group system account
            work.clear();
            for (Entry<String, String> e : grpSysAcctDatas.get(i).entrySet()) {
                work.put(e.getKey(), e.getValue());
            }
            grpSysAcct = new UgroupSystemAccountEntity(work);

            // Execution
            target.registerUser(sysAcct, users, grpSysAcct);
            commitTransactions();

            // Verification
            String expectedGroupId = getListMap(sheetName, "expected").get(i).get("caseNo");
            assertTableEquals(expectedGroupId, sheetName, expectedGroupId);
            
        }
    }
    
    /**
     * Test 2 of {@link UserComponent#registerUser()}. <br>
     * Abnormal system.
     */
    @Test
    public void testRegisterUser2() {
        String sheetName = "registerUser";
                
        setThreadContextValues(sheetName, "threadContext");
        
        List<Map<String, String>> sysAcctDatas = getListMap(sheetName, "sysAcctEntityErr");
        List<Map<String, String>> usersDatas = getListMap(sheetName, "usersEntityErr");
        List<Map<String, String>> grpSysAcctDatas = getListMap(sheetName, "grpSysAcctEntityErr");
        List<Map<String, String>> expected = getListMap(sheetName, "expectedErr");
        // Map and list to temporarily receive Excel data
        Map<String, Object> work = new HashMap<String, Object>();
        List<Map<String, String>> useCaseData = null;
        
        SystemAccountEntity sysAcct = null;
        UsersEntity users = null;
        UgroupSystemAccountEntity grpSysAcct = null;
        for (int i = 0; i < sysAcctDatas.size(); i++) {

            // Database preparation
            setUpDb(sheetName);

            // System account
            work.clear();
            for (Entry<String, String> e : sysAcctDatas.get(i).entrySet()) {
                work.put(e.getKey(), e.getValue());
            }
            // Creation of use case ID arguments
            String id = sysAcctDatas.get(i).get("useCaseId");
            useCaseData = getListMap(sheetName, id);
            String[] useCaseId = new String[useCaseData.size()];
            for (int j = 0; j < useCaseData.size(); j++) {
                useCaseId[j] = useCaseData.get(j).get("useCaseId");
            }
            work.put("useCase", useCaseId);
            sysAcct = new SystemAccountEntity(work);

            // User
            work.clear();
            for (Entry<String, String> e : usersDatas.get(i).entrySet()) {
                work.put(e.getKey(), e.getValue());
            }
            users = new UsersEntity(work);

            // Group system account
            work.clear();
            for (Entry<String, String> e : grpSysAcctDatas.get(i).entrySet()) {
                work.put(e.getKey(), e.getValue());
            }
            grpSysAcct = new UgroupSystemAccountEntity(work);

            // Execution
            try {
                target.registerUser(sysAcct, users, grpSysAcct);
                fail();
            } catch (ApplicationException ae) {
                assertEquals(expected.get(i).get("messageId"), ae.getMessages().get(0).getMessageId());
            }
        }
    }
    
}
