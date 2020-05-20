<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<!-- <%/* --> <script src="js/devtool.js"></script><meta charset="utf-8"><body> <!-- */%> -->
<%@ taglib prefix="n" uri="http://tis.co.jp/nablarch" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="t" tagdir="/WEB-INF/tags/template" %>
<%@ taglib prefix="button" tagdir="/WEB-INF/tags/widget/button" %>
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<t:page_template title="ユーザ情報削除完了">
  <jsp:attribute name="contentHtml">
    <p>ユーザの削除が完了しました。</p>

    <button:block>
      <n:set var="searchCondition" name="11AC_W11AC01.loginId"></n:set>
      <n:set var="searchRequestId" value="RW11AC0101"></n:set>
      <c:if test="${searchCondition != null}">
        <n:set var="searchRequestId" value="RW11AC0102"></n:set>
      </c:if>
      <n:form windowScopePrefixes="11AC_W11AC01">
        <button:submit
            label="検索画面へ"
            uri="/action/ss11AC/W11AC01Action/${searchRequestId}"
            dummyUri="./W11AC0101.jsp">
        </button:submit>
      </n:form>
    </button:block>
  </jsp:attribute>
</t:page_template>

