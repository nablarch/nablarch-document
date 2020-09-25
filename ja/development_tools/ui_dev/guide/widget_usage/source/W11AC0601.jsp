<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<!-- <%/* --> <script src="js/devtool.js"></script><meta charset="utf-8"><body> <!-- */%> -->
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="n" uri="http://tis.co.jp/nablarch" %>
<%@ taglib prefix="t" tagdir="/WEB-INF/tags/template" %>
<%@ taglib prefix="field" tagdir="/WEB-INF/tags/widget/field" %>
<%@ taglib prefix="button" tagdir="/WEB-INF/tags/widget/button" %>
<%@ taglib prefix="spec" tagdir="/WEB-INF/tags/widget/spec" %>
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<t:page_template title="ユーザ情報一括登録">
  <jsp:attribute name="localCss">
    div.item-list > ol {
      list-style: decimal inside;
      margin: 10px 0 20px 20px;
    }

    div.item-list > ul {
      list-style: none;
      margin: 10px 0 20px 20px;
    }
  </jsp:attribute>
  <jsp:attribute name="contentHtml">
  <n:form enctype="multipart/form-data">
  <spec:layout name="ユーザ登録">
    <field:block title="ユーザ登録情報ファイル">
      <field:file title="登録対象ファイル" name="userList"></field:file>
    </field:block>

    <button:block>
      <button:submit
        label="アップロード"
        uri="/action/ss11AC/W11AC06Action/RW11AC0602"
        dummyUri="./W11AC0602.jsp">
      </button:submit>
    </button:block>
  </spec:layout>


    <div class="title">
      <h2>ファイルのフォーマット</h2>
    </div>

    <div>
      <h4>本画面でアップロードするファイルは以下の形式としてください。</h4>
    </div>
    <div class="item-list">
      <ul>
        <li>ファイルの形式：CSVファイル</li>
        <li>文字コード：Windows-31J</li>
        <li>改行コード：CRLF</li>
      </ul>
    </div>

    <div>
      <h4>ファイルに必要な項目</h4>
    </div>
    <div class="item-list">
      <ol>
        <li>ログインID</li>
        <li>漢字氏名</li>
        <li>カナ氏名</li>
        <li>メールアドレス</li>
        <li>内線番号（ビル番号）</li>
        <li>内線番号（個人番号）</li>
        <li>携帯電話番号（市外）</li>
        <li>携帯電話番号（市内）</li>
        <li>携帯電話番号（加入）</li>
      </ol>
    </div>
  </n:form>
  </jsp:attribute>
</t:page_template>

