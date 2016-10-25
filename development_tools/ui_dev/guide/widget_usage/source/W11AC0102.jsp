<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<!-- <%/* --> <script src="js/devtool.js"></script><meta charset="utf-8"><body> <!-- */%> -->
<%@ taglib prefix="n" uri="http://tis.co.jp/nablarch" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="t" tagdir="/WEB-INF/tags/template" %>
<%@ taglib prefix="button" tagdir="/WEB-INF/tags/widget/button" %>
<%@ taglib prefix="field" tagdir="/WEB-INF/tags/widget/field" %>
<%@ taglib prefix="spec" tagdir="/WEB-INF/tags/widget/spec" %>
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<t:page_template title="ユーザ情報詳細" confirmationPageTitle="ユーザ情報詳細">
  <jsp:attribute name="contentHtml">
  <spec:layout name="ユーザー基本情報">
  <field:block title="ユーザ基本情報">
    <field:label
        title="ログインID"
        name="userDetailedInfo.loginId"
        domain="LOGIN_ID"
        dataFrom="SYSTEM_ACCOUNT.LOGIN_ID"
        sample="login-id">
    </field:label>
    <field:label
        title="漢字氏名"
        name="userDetailedInfo.kanjiName"
        domain="KANJI_NAME"
        dataFrom="USERS.KANJI_NAME"
        sample="てすと ゆーざ">
    </field:label>
    <field:label
        title="カナ氏名"
        name="userDetailedInfo.kanaName"
        domain="KANA_NAME"
        dataFrom="USERS.KANA_NAME"
        sample="テスト ユーザ">
    </field:label>
    <field:label
        title="メールアドレス"
        name="userDetailedInfo.mailAddress"
        domain="MAIL_ADDRESS"
        dataFrom="USERS.MAIL_ADDRESS"
        sample="test@mail.com">
    </field:label>
    <field:label_extension_number
        title="内線番号"
        builName="userDetailedInfo.extensionNumberBuilding"
        personalName="userDetailedInfo.extensionNumberPersonal"
        domain="EXT_NUM_BUILDING|EXT_NUM_PERSONAL"
        dataFrom="USERS.EXTENSION_NUMBER_BUILDING|USERS.EXTENSION_NUMBER_PERSONAL"
        sample="01-1111">
    </field:label_extension_number>
    <field:label_tel
        title="携帯電話番号"
        areaName="userDetailedInfo.mobilePhoneNumberAreaCode"
        localName="userDetailedInfo.mobilePhoneNumberCityCode"
        subscriberName="userDetailedInfo.mobilePhoneNumberSbscrCode"
        domain="MOBILE_PHONE_CITY|MOBILE_PHONE_AREA|MOBILE_PHONE_SBSCR"
        dataFrom="USERS.MOBILE_PHONE_NUMBER_CITY_CODE|USERS.MOBILE_PHONE_NUMBER_AREA_CODE|USERS.MOBILE_PHONE_NUMBER_SBSCR_CODE"
        sample="090-1234-1234">
    </field:label_tel>
  </field:block>
  <field:block title="権限情報">
    <field:label_id_value
        title="グループ"
        idName="ugroupInfo.ugroupId"
        valueName="ugroupInfo.ugroupName"
        domain="UGROUP_ID"
        dataFrom="UGROUP.UGROUP_ID|UGROUP.UGROUP_NAME"
        sample="0000000000: お客様グループ">
    </field:label_id_value>
  </field:block>
  <field:block title="認可単位情報">
    <field:label_block
        title="認可単位"
        dataFrom="PERMISSION_UNIT.PERMISSION_UNIT_ID|PERMISSION_UNIT.PERMISSION_UNIT_NAME">
      <c:if test="${empty permissionUnitInfo}">-</c:if>
      <c:if test="${not empty permissionUnitInfo}">
        <c:forEach var="unit" items="${permissionUnitInfo}">
          <n:write name="unit.permissionUnitId"/>:<n:write name="unit.permissionUnitName"/><br />
        </c:forEach>
      </c:if>
    </field:label_block>
  </field:block>
  <n:form windowScopePrefixes="11AC_W11AC01">
    <button:block>
      <n:set var="loginId" name="11AC_W11AC01.loginId"></n:set>
      <n:set var="kanjiName" name="11AC_W11AC01.kanjiName"></n:set>
      <n:set var="kanaName" name="11AC_W11AC01.kanaName"></n:set>
      <n:set var="ugroupId" name="11AC_W11AC01.ugroupId"></n:set>
      <n:set var="userIdLocked" name="11AC_W11AC01.userIdLocked"></n:set>
      <c:if test="${empty loginId and empty kanjiName  and empty kanaName and empty ugroupId and empty userIdLocked}">
        <n:set var="searchRequestId" value="RW11AC0101"></n:set>
      </c:if>
      <c:if test="${not empty loginId or not empty kanjiName or not empty kanaName or not empty ugroupId or not empty userIdLocked}">
        <n:set var="searchRequestId" value="RW11AC0102"></n:set>
      </c:if>
      <button:back uri="/action/ss11AC/W11AC01Action/${searchRequestId}"  dummyUri="./W11AC0101.jsp" label="検索画面へ">
      </button:back>
      <button:delete uri="/action/ss11AC/W11AC04Action/RW11AC0401" dummyUri="./W11AC0401.jsp">
        <n:param paramName="W11AC04.userId" name="userDetailedInfo.userId"></n:param>
      </button:delete>
      <button:update
          uri="/action/ss11AC/W11AC03Action/RW11AC0301" dummyUri="./W11AC0301.jsp">
        <n:param paramName="W11AC03.userId" name="userDetailedInfo.userId"></n:param>
      </button:update>
    </button:block>
  </n:form>
  </spec:layout>
  </jsp:attribute>
</t:page_template>

