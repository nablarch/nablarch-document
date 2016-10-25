<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<!-- <%/* --> <script src="js/devtool.js"></script><meta charset="utf-8"><body> <!-- */%> -->
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="n" uri="http://tis.co.jp/nablarch" %>
<%@ taglib prefix="t" tagdir="/WEB-INF/tags/template" %>
<%@ taglib prefix="field" tagdir="/WEB-INF/tags/widget/field" %>
<%@ taglib prefix="button" tagdir="/WEB-INF/tags/widget/button" %>
<%@ taglib prefix="spec" tagdir="/WEB-INF/tags/widget/spec" %>
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<t:page_template title="ユーザ情報削除確認">
  <jsp:attribute name="contentHtml">
    <spec:layout name="削除対象ユーザ情報">
    <field:block title="ユーザ基本情報">
      <field:label
          title="ログインID"
          name="deleteUserInfo.loginId"
          domain="LOGIN_ID"
          dataFrom="SYSTEM_ACCOUNT.LOGIN_ID"
          sample="test01">
      </field:label>
      <field:label
          title="漢字氏名"
          name="deleteUserInfo.kanjiName"
          domain="KANJI_NAME"
          dataFrom="USERS.KANJI_NAME"
          sample="名部　楽太郎">
      </field:label>
      <field:label
          title="カナ氏名"
          name="deleteUserInfo.kanaName"
          domain="KANA_NAME"
          dataFrom="USERS.KANA_NAME"
          sample="ナブ　ラクタロウ">
      </field:label>
      <field:label
          title="メールアドレス"
          name="deleteUserInfo.mailAddress"
          domain="MAIL_ADDRESS"
          dataFrom="USERS.MAIL_ADDRESS"
          sample="nabla@example.com">
      </field:label>
      <field:label_extension_number
          title="内線番号"
          builName="deleteUserInfo.extensionNumberBuilding"
          personalName="deleteUserInfo.extensionNumberPersonal"
          domain="EXT_NUM_BUILDING|EXT_NUM_PERSONAL"
          dataFrom = "USERS.EXTENSION_NUMBER_BUILDING|USERS.EXTENSION_NUMBER_PERSONAL"
          sample="01-1234">
      </field:label_extension_number>
      <field:label_tel
          title="携帯電話番号"
          areaName="deleteUserInfo.mobilePhoneNumberAreaCode"
          localName="deleteUserInfo.mobilePhoneNumberCityCode"
          subscriberName="deleteUserInfo.mobilePhoneNumberSbscrCode"
          domain="MOBILE_PHONE_CITY|MOBILE_PHONE_AREA|MOBILE_PHONE_SBSCR"
          dataFrom="USERS.MOBILE_PHONE_NUMBER_CITY_CODE|USERS.MOBILE_PHONE_NUMBER_AREA_CODE|USERS.MOBILE_PHONE_NUMBER_SBSCR_CODE"
          sample="090-1111-2222">
      </field:label_tel>
    </field:block>
    </spec:layout>
    <n:form windowScopePrefixes="11AC_W11AC01,W11AC04" useToken="true">
      <button:block>
        <n:set var="searchCondition" name="11AC_W11AC01.loginId"></n:set>
        <n:set var="searchRequestId" value="RW11AC0101"></n:set>
        <c:if test="${searchCondition != null}">
          <n:set var="searchRequestId" value="RW11AC0102"></n:set>
        </c:if>
        <button:back
            label="検索画面へ"
            uri="/action/ss11AC/W11AC01Action/${searchRequestId}"
            dummyUri="./W11AC0101.jsp">
        </button:back>
        <button:back
            label="詳細画面へ"
            uri="/action/ss11AC/W11AC01Action/RW11AC0103"
            dummyUri="./W11AC0102.jsp">
        </button:back>
        <button:confirm
            uri="/action/ss11AC/W11AC04Action/RW11AC0403"
            dummyUri="./W11AC0402.jsp"
            allowDoubleSubmission="false">
        </button:confirm>
      </button:block>
    </n:form>
  </jsp:attribute>
</t:page_template>

