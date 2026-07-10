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
 * {@link UserComponentTest}のテストクラス。
 * 
 * @author Tsuyoshi Kawasaki
 * @since 1.0
 */
public class UserComponentTest extends DbAccessTestSupport {

    /** テスト対象クラス */
    private UserComponent target = new UserComponent();
    

    /**
     * {@link UserComponent#registerUser()}のテスト1。<br>
     * 正常系。
     */
    @Test
    public void testRegisterUser1() {
        String sheetName = "registerUser";
                
        setThreadContextValues(sheetName, "threadContext");
        
        List<Map<String, String>> sysAcctDatas = getListMap(sheetName, "sysAcctEntity");
        List<Map<String, String>> usersDatas = getListMap(sheetName, "usersEntity");
        List<Map<String, String>> grpSysAcctDatas = getListMap(sheetName, "grpSysAcctEntity");
        // エクセルのデータを一時的に受けるMap、List
        Map<String, Object> work = new HashMap<String, Object>();
        List<Map<String, String>> useCaseData = null;
        
        SystemAccountEntity sysAcct = null;
        UsersEntity users = null;
        UgroupSystemAccountEntity grpSysAcct = null;
        for (int i = 0; i < sysAcctDatas.size(); i++) {

            // データベース準備
            setUpDb(sheetName);

            // システムアカウント
            work.clear();
            for (Entry<String, String> e : sysAcctDatas.get(i).entrySet()) {
                work.put(e.getKey(), e.getValue());
            }
            // ユースケースIDの引数作成
            String id = sysAcctDatas.get(i).get("useCaseId");
            useCaseData = getListMap(sheetName, id);
            String[] useCaseId = new String[useCaseData.size()];
            for (int j = 0; j < useCaseData.size(); j++) {
                useCaseId[j] = useCaseData.get(j).get("useCaseId");
            }
            work.put("useCase", useCaseId);
            sysAcct = new SystemAccountEntity(work);
            
            // ユーザ
            work.clear();
            for (Entry<String, String> e : usersDatas.get(i).entrySet()) {
                work.put(e.getKey(), e.getValue());
            }
            users = new UsersEntity(work);

            // グループシステムアカウント
            work.clear();
            for (Entry<String, String> e : grpSysAcctDatas.get(i).entrySet()) {
                work.put(e.getKey(), e.getValue());
            }
            grpSysAcct = new UgroupSystemAccountEntity(work);

            // 実行
            target.registerUser(sysAcct, users, grpSysAcct);
            commitTransactions();

            // 検証
            String expectedGroupId = getListMap(sheetName, "expected").get(i).get("caseNo");
            assertTableEquals(expectedGroupId, sheetName, expectedGroupId);
            
        }
    }
    
    /**
     * {@link UserComponent#registerUser()}のテスト2。<br>
     * 異常系。
     */
    @Test
    public void testRegisterUser2() {
        String sheetName = "registerUser";
                
        setThreadContextValues(sheetName, "threadContext");
        
        List<Map<String, String>> sysAcctDatas = getListMap(sheetName, "sysAcctEntityErr");
        List<Map<String, String>> usersDatas = getListMap(sheetName, "usersEntityErr");
        List<Map<String, String>> grpSysAcctDatas = getListMap(sheetName, "grpSysAcctEntityErr");
        List<Map<String, String>> expected = getListMap(sheetName, "expectedErr");
        // エクセルのデータを一時的に受けるMap、List
        Map<String, Object> work = new HashMap<String, Object>();
        List<Map<String, String>> useCaseData = null;
        
        SystemAccountEntity sysAcct = null;
        UsersEntity users = null;
        UgroupSystemAccountEntity grpSysAcct = null;
        for (int i = 0; i < sysAcctDatas.size(); i++) {

            // データベース準備
            setUpDb(sheetName);

            // システムアカウント
            work.clear();
            for (Entry<String, String> e : sysAcctDatas.get(i).entrySet()) {
                work.put(e.getKey(), e.getValue());
            }
            // ユースケースIDの引数作成
            String id = sysAcctDatas.get(i).get("useCaseId");
            useCaseData = getListMap(sheetName, id);
            String[] useCaseId = new String[useCaseData.size()];
            for (int j = 0; j < useCaseData.size(); j++) {
                useCaseId[j] = useCaseData.get(j).get("useCaseId");
            }
            work.put("useCase", useCaseId);
            sysAcct = new SystemAccountEntity(work);
            
            // ユーザ
            work.clear();
            for (Entry<String, String> e : usersDatas.get(i).entrySet()) {
                work.put(e.getKey(), e.getValue());
            }
            users = new UsersEntity(work);

            // グループシステムアカウント
            work.clear();
            for (Entry<String, String> e : grpSysAcctDatas.get(i).entrySet()) {
                work.put(e.getKey(), e.getValue());
            }
            grpSysAcct = new UgroupSystemAccountEntity(work);

            // 実行
            try {
                target.registerUser(sysAcct, users, grpSysAcct);
                fail();
            } catch (ApplicationException ae) {
                assertEquals(expected.get(i).get("messageId"), ae.getMessages().get(0).getMessageId());
            }
        }
    }
    
}
