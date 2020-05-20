<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<!-- <%/* --> <script src="js/devtool.js"></script><meta charset="utf-8"><body> <!-- */%> -->
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="n" uri="http://tis.co.jp/nablarch" %>
<%@ taglib prefix="field" tagdir="/WEB-INF/tags/widget/field" %>
<%@ taglib prefix="button" tagdir="/WEB-INF/tags/widget/button" %>
<%@ taglib prefix="t" tagdir="/WEB-INF/tags/template" %>
<%@ taglib prefix="spec" tagdir="/WEB-INF/tags/widget/spec" %>
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<t:page_template
    title="ユーザ情報登録"
    confirmationPageTitle="ユーザ情報登録確認">
  <jsp:attribute name="contentHtml">
  <n:forInputPage>
    <p class="attention">*は必ず入力してください。</p>
  </n:forInputPage>
  <n:form windowScopePrefixes="W11AC02,11AC_W11AC01">
    <spec:layout name="ユーザ情報の入力画面">
      <field:block title="ユーザ基本情報">
        <field:text title="ログインID"
                    domain="LOGIN_ID"
                    required="true"
                    maxlength="20"
                    hint="半角英数記号20文字以内"
                    name="W11AC02.loginId"
                    dataFrom="SYSTEM_ACCOUNT.LOGIN_ID"
                    sample="test01">
        </field:text>
        <field:password title="パスワード"
                        domain="PASSWORD"
                        dataFrom="SYSTEM_ACCOUNT.PASSWORD"
                        required="true"
                        maxlength="20"
                        name="W11AC02.newPassword"
                        sample="password">
        </field:password>
        <field:password title="パスワード（確認用）"
                        domain="PASSWORD"
                        dataFrom="SYSTEM_ACCOUNT.PASSWORD"
                        required="true"
                        maxlength="20"
                        name="W11AC02.confirmPassword"
                        hint="半角英数記号20文字以内"
                        sample="password">
        </field:password>

        <field:text title="漢字氏名"
                    domain="KANJI_NAME"
                    required="true"
                    maxlength="50"
                    hint="全角50文字以内"
                    dataFrom="USERS.KANJI_NAME"
                    name="W11AC02.kanjiName"
                    sample="名部　楽太郎">
        </field:text>
        <field:text title="カナ氏名"
                    domain="KANA_NAME"
                    required="true"
                    maxlength="50"
                    hint="全角カナ50文字以内"
                    name="W11AC02.kanaName"
                    dataFrom="USERS.KANA_NAME"
                    sample="ナブ　ラクタロウ">
        </field:text>
        <field:text title="メールアドレス"
                    domain="MAIL_ADDRESS"
                    required="true"
                    maxlength="100"
                    hint="半角英数記号100文字以内"
                    name="W11AC02.mailAddress"
                    dataFrom="USERS.MAIL_ADDRESS"
                    sample="nabla@example.com">
        </field:text>
        <field:extension_number
            title="内線番号"
            domain="EXT_NUM_BUILDING|EXT_NUM_PERSONAL"
            dataFrom = "USERS.EXTENSION_NUMBER_BUILDING|USERS.EXTENSION_NUMBER_PERSONAL"
            builName="W11AC02.extensionNumberBuilding"
            personalName="W11AC02.extensionNumberPersonal"
            hint="半角数字2文字以内 - 半角数字4文字以内"
            required="true">
        </field:extension_number>
        <field:tel title="携帯電話番号"
                      domain="MOBILE_PHONE_AREA|MOBILE_PHONE_CITY|MOBILE_PHONE_SBSCR"
                      dataFrom="USERS.MOBILE_PHONE_NUMBER_AREA_CODE|USERS.MOBILE_PHONE_NUMBER_CITY_CODE|USERS.MOBILE_PHONE_NUMBER_SBSCR_CODE"
                      areaName="W11AC02.mobilePhoneNumberAreaCode"
                      localName="W11AC02.mobilePhoneNumberCityCode"
                      subscriberName="W11AC02.mobilePhoneNumberSbscrCode"
                      nameAlias="W11AC02.mobilePhoneNumber"
                      hint="半角数字3文字以内 - 半角数字4文字以内 - 半角数字4文字以内">
        </field:tel>
      </field:block>
      <field:block title="権限情報">
        <field:pulldown title="グループ"
                        required="true"
                        name="W11AC02.ugroupId"
                        listName="allGroup"
                        domain="UGROUP_ID"
                        dataFrom="UGROUP.UGROUP_ID|UGROUP.UGROUP_NAME"
                        elementLabelProperty="ugroupName"
                        elementValueProperty="ugroupId"
                        hint="所属グループを選択してください。"
                        sample="[お客様グループ]|一般グループ">
        </field:pulldown>
      </field:block>
      <field:block title="認可単位情報">
        <field:listbuilder
            title="認可単位"
            name="W11AC02.permissionUnit"
            domain="PERMISSION_UNIT_ID"
            dataFrom="PERMISSION_UNIT.PERMISSION_UNIT_ID|PERMISSION_UNIT.PERMISSION_UNIT_NAME"
            id="permissionUnit"
            listName="allPermissionUnit"
            elementLabelProperty="permissionUnitName"
            elementValueProperty="permissionUnitId"
            sample="ログイン|ユーザ一覧照会|ユーザ情報登録|ユーザ情報更新|ユーザ情報削除|ユーザ情報一括削除|ユーザ情報登録(被仕向)">
        </field:listbuilder>
      </field:block>

      <button:block>
        <n:set var="searchCondition" name="11AC_W11AC01.loginId"></n:set>
        <n:set var="searchRequestId" value="RW11AC0101"></n:set>
        <c:if test="${searchCondition != null}">
          <n:set var="searchRequestId" value="RW11AC0102"></n:set>
        </c:if>
        <n:forInputPage>
          <button:back
              label="検索画面へ"
              uri="/action/ss11AC/W11AC01Action/${searchRequestId}"
              dummyUri="./W11AC0101.jsp">
          </button:back>
          <button:check
              uri="/action/ss11AC/W11AC02Action/RW11AC0202"
              dummyUri="W11AC0202.jsp">
          </button:check>
        </n:forInputPage>
        <n:forConfirmationPage>
          <button:cancel
              uri="/action/ss11AC/W11AC02Action/RW11AC0203"
              dummyUri="W11AC0201.jsp">
          </button:cancel>
          <button:confirm
              uri="/action/ss11AC/W11AC02Action/RW11AC0204"
              allowDoubleSubmission="false"
              dummyUri="W11AC0203.jsp">
          </button:confirm>
          <button:submit
              label="メッセージ送信"
              uri="/action/ss11AC/W11AC02Action/RW11AC0205"
              allowDoubleSubmission="false"
              dummyUri="./W11AC0203.jsp">
          </button:submit>
          <button:submit
              label="Http送信"
              uri="/action/ss11AC/W11AC02Action/RW11AC0206"
              allowDoubleSubmission="false"
              dummyUri="./W11AC0203.jsp">
          </button:submit>
        </n:forConfirmationPage>
      </button:block>
    </spec:layout>
  </n:form>
  </jsp:attribute>
</t:page_template>

