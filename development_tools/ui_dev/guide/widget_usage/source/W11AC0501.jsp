<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<!-- <%/* --> <script src="js/devtool.js"></script><meta charset="utf-8"><body> <!-- */%> -->
<%@ taglib prefix="t" tagdir="/WEB-INF/tags/template" %>
<%@ taglib prefix="button" tagdir="/WEB-INF/tags/widget/button" %>
<%@ taglib prefix="table" tagdir="/WEB-INF/tags/widget/table" %>
<%@ taglib prefix="column" tagdir="/WEB-INF/tags/widget/column" %>
<%@ taglib prefix="spec" tagdir="/WEB-INF/tags/widget/spec" %>
<%@ taglib prefix="n" uri="http://tis.co.jp/nablarch" %>

<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<n:set var="deleteCount" name="deleteUserCount"></n:set>

<t:page_template title="ユーザ情報一括削除確認">
  <jsp:attribute name="contentHtml">
  <n:form windowScopePrefixes="11AC_W11AC01,W11AC05" useToken="true">
    <spec:layout name="一括削除対象ユーザ情報">
    <table:plain
        title="削除対象 (${deleteCount}件)"
        resultSetName="deleteUsers.userBeans"
        sampleResults="${deleteCount}">

      <column:label
          key="loginId"
          title="ログインID"
          domain="LOGIN_ID"
          dataFrom="SYSTEM_ACCOUNT.LOGIN_ID"
          sample="loginId1">
      </column:label>

      <column:label
          key="kanjiName"
          title="漢字氏名"
          domain="KANJI_NAME"
          dataFrom="USERS.KANJI_NAME"
          sample="なまえ">
      </column:label>

      <column:label
          key="kanaName"
          title="カナ氏名"
          domain="KANA_NAME"
          dataFrom="USERS.KANA_NAME"
          sample="ナマエ">
      </column:label>

      <column:label
          key="effectiveDateFrom"
          title="有効期限（開始）"
          domain="DATE"
          dataFrom="SYSTEM_ACCOUNT.EFFECTIVE_DATE_FROM"
          sample="2010/01/11">
      </column:label>

      <column:label
          key="effectiveDateTo"
          title="有効期限（終了）"
          domain="DATE"
          dataFrom="SYSTEM_ACCOUNT.EFFECTIVE_DATE_TO"
          sample="2015/12/31">
      </column:label>
    </table:plain>
    </spec:layout>

    <button:block>
      <button:cancel
          uri="/action/ss11AC/W11AC01Action/RW11AC0102"
          dummyUri="./W11AC0101.jsp">
      </button:cancel>
      <button:confirm
          uri="/action/ss11AC/W11AC05Action/RW11AC0502"
          allowDoubleSubmission="false"
          dummyUri="./W11AC0502.jsp">
      </button:confirm>
    </button:block>
  </n:form>
  </jsp:attribute>
</t:page_template>


