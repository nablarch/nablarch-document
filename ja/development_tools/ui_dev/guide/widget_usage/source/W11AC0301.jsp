<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<!-- <%/* --> <script src="js/devtool.js"></script><meta charset="utf-8"><body> <!-- */%> -->
<%@ taglib prefix="n" uri="http://tis.co.jp/nablarch" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="t" tagdir="/WEB-INF/tags/template" %>
<%@ taglib prefix="field" tagdir="/WEB-INF/tags/widget/field" %>
<%@ taglib prefix="button" tagdir="/WEB-INF/tags/widget/button" %>
<%@ taglib prefix="spec" tagdir="/WEB-INF/tags/widget/spec" %>
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<t:page_template
    title="ユーザ情報更新"
    confirmationPageTitle="ユーザ情報更新確認">
  <jsp:attribute name="contentHtml">
    <n:forInputPage>
      <p class="attention">*は必ず入力してください。</p>
    </n:forInputPage>
    <n:form windowScopePrefixes="11AC_W11AC01,W11AC03">
      <spec:layout name="ユーザ基本情報表示">
      <field:block title="ユーザ基本情報">
        <field:label
            title="ログインID"
            name="W11AC03.loginId"
            domain="LOGIN_ID"
            dataFrom="SYSTEM_ACCOUNT.LOGIN_ID"
            sample="nablarch">
        </field:label>
        <n:hidden name="W11AC03.loginId"></n:hidden>
        <field:text
            title="漢字氏名"
            name="W11AC03.kanjiName"
            required="true"
            maxlength="50"
            hint="全角50文字以内"
            domain="KANJI_NAME"
            dataFrom="USERS.KANJI_NAME"
            sample="名部　楽太郎">
        </field:text>
        <field:text
            title="カナ氏名"
            name="W11AC03.kanaName"
            required="true"
            maxlength="50"
            hint="全角カナ50文字以内"
            domain="KANA_NAME"
            dataFrom="USERS.KANA_NAME"
            sample="ナブ　ラクタロウ">
        </field:text>
        <field:mail
            title="メールアドレス"
            name="W11AC03.mailAddress"
            required="true"
            maxlength="50"
            hint="半角英数記号100文字以内"
            domain="MAIL_ADDRESS"
            dataFrom="USERS.MAIL_ADDRESS"
            sample="nablarch@example.com">
        </field:mail>
        <field:extension_number
            title="内線番号"
            required="true"
            builName="W11AC03.extensionNumberBuilding"
            personalName="W11AC03.extensionNumberPersonal"
            domain="EXT_NUM_BUILDING|EXT_NUM_PERSONAL"
            dataFrom = "USERS.EXTENSION_NUMBER_BUILDING|USERS.EXTENSION_NUMBER_PERSONAL"
            hint="半角数字2文字以内 - 半角数字4文字以内">
        </field:extension_number>
        <field:tel
            title="携帯電話番号"
            areaName="W11AC03.mobilePhoneNumberAreaCode"
            localName="W11AC03.mobilePhoneNumberCityCode"
            subscriberName="W11AC03.mobilePhoneNumberSbscrCode"
            nameAlias="W11AC03.mobilePhoneNumber"
            domain="MOBILE_PHONE_AREA|MOBILE_PHONE_CITY|MOBILE_PHONE_SBSCR"
            dataFrom="USERS.MOBILE_PHONE_NUMBER_AREA_CODE|USERS.MOBILE_PHONE_NUMBER_CITY_CODE|USERS.MOBILE_PHONE_NUMBER_SBSCR_CODE"
            hint="半角数字3文字以内 - 半角数字4文字以内 - 半角数字4文字以内">
        </field:tel>
      </field:block>
      <field:block title="権限情報">
        <field:pulldown
            title="グループ"
            name="W11AC03.ugroupId"
            required="true"
            listName="ugroupList"
            elementLabelProperty="ugroupName"
            elementValueProperty="ugroupId"
            hint="グループを選択してください"
            domain="UGROUP_ID"
            dataFrom="UGROUP.UGROUP_ID|UGROUP.UGROUP_NAME"
            sample="[管理者]|ユーザ">
        </field:pulldown>
      </field:block>
      <field:block title="認可単位情報">
        <field:listbuilder
            title="認可単位"
            name="W11AC03.permissionUnit"
            id="permissionUnitId"
            listName="permissionUnitList"
            elementLabelProperty="permissionUnitName"
            domain="PERMISSION_UNIT_ID"
            dataFrom="PERMISSION_UNIT.PERMISSION_UNIT_ID|PERMISSION_UNIT.PERMISSION_UNIT_NAME"
            elementValueProperty="permissionUnitId"
            sample="ログイン|ユーザ一覧照会|ユーザ情報登録|ユーザ情報更新|ユーザ情報削除|ユーザ情報一括削除|ユーザ情報登録(被仕向)">
         </field:listbuilder>
      </field:block>
      <button:block>
        <n:forInputPage>
          <button:back
              label="検索画面へ"
              uri="/action/ss11AC/W11AC01Action/RW11AC0102"
              dummyUri="./W11AC0101.jsp">
          </button:back>
          <button:back
              label="詳細画面へ"
              uri="/action/ss11AC/W11AC01Action/RW11AC0103"
              dummyUri="./W11AC0102.jsp">
          </button:back>
          <button:check
              uri="/action/ss11AC/W11AC03Action/RW11AC0302"
              dummyUri="W11AC0302.jsp">
          </button:check>
        </n:forInputPage>
        <n:forConfirmationPage>
          <button:cancel
              uri="/action/ss11AC/W11AC03Action/RW11AC0303"
              dummyUri="W11AC0301.jsp">
          </button:cancel>
          <button:confirm
              uri="/action/ss11AC/W11AC03Action/RW11AC0304"
              allowDoubleSubmission="false"
              dummyUri="W11AC0303.jsp">
          </button:confirm>
        </n:forConfirmationPage>
      </button:block>
      </spec:layout>
    </n:form>
  </jsp:attribute>
</t:page_template>

