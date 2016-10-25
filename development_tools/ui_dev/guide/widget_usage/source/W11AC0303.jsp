<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<!-- <%/* --> <script src="js/devtool.js"></script><meta charset="utf-8"><body> <!-- */%> -->
<%@ taglib prefix="n" uri="http://tis.co.jp/nablarch" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="t" tagdir="/WEB-INF/tags/template" %>
<%@ taglib prefix="button" tagdir="/WEB-INF/tags/widget/button" %>
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<t:page_template title="ユーザ情報更新完了">
  <jsp:attribute name="contentHtml">
    <n:form windowScopePrefixes="11AC_W11AC01">
      <p class="completedMessage">ユーザ情報の更新が完了しました。</p>

      <n:set var="searchCondition" name="11AC_W11AC01.loginId"></n:set>
      <n:set var="searchRequestId" value="RW11AC0101"></n:set>
      <c:if test="${searchCondition != null}">
        <n:set var="searchRequestId" value="RW11AC0102"></n:set>
      </c:if>
      <button:block>
        <button:submit
            label="検索画面へ"
            uri="/action/ss11AC/W11AC01Action/${searchRequestId}"
            dummyUri="./W11AC0101.jsp">
        </button:submit>
        <button:submit
            label="詳細画面へ"
            uri="/action/ss11AC/W11AC01Action/RW11AC0103"
            dummyUri="./W11AC0102.jsp">
        </button:submit>
      </button:block>
    </n:form>
  </jsp:attribute>
</t:page_template>

