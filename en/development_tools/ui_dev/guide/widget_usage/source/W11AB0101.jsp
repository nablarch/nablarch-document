<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<!-- <%/* --> <script src="js/devtool.js"></script><meta charset="utf-8"><body> <!-- */%> -->
<%@ taglib prefix="n" uri="http://tis.co.jp/nablarch" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="t" tagdir="/WEB-INF/tags/template" %>
<%@ taglib prefix="link" tagdir="/WEB-INF/tags/widget/link" %>
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<t:page_template title="トップメニュー">
  <jsp:attribute name="contentHtml">
    <n:form>
      <uL>
        <li>
          <link:submit
              uri=""
              label="ユーザ情報一覧照会"
              dummyUri="W11AC0101.jsp">
          </link:submit>
        </li>
        <li>
          <link:submit
              uri=""
              label="ユーザ情報登録"
              dummyUri="W11AC0201.jsp">
          </link:submit>
        </li>
        <li>
          <link:submit
              uri=""
              label="ユーザ情報一括登録"
              dummyUri="W11AC0401.jsp">
          </link:submit>
        </li>
      </uL>
    </n:form>
  </jsp:attribute>
</t:page_template>
