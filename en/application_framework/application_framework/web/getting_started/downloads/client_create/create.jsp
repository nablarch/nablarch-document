<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="n" uri="http://tis.co.jp/nablarch" %>
<%@ page session="false" %>

<!DOCTYPE html>
<html>
    <head>
        <title>顧客登録画面</title>
    </head>
    <body>
        <n:include path="/WEB-INF/view/common/menu.jsp" />
        <n:include path="/WEB-INF/view/common/header.jsp" />
        <div class="container-fluid mainContents">
            <section class="row">
                <div class="title-nav">
                    <span class="page-title">顧客登録画面</span>
                </div>
            </section>
        </div>
        
        <!-- ここに登録画面の初期表示部分を実装する -->
        
        <n:include path="/WEB-INF/view/common/footer.jsp" />
    </body>
</html>