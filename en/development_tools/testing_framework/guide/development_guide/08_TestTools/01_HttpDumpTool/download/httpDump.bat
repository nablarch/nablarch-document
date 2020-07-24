@echo off

cd /d %~dp0


set CP=./lib/*
set JAVA_EXE="%JAVA_HOME%\bin\java"

start "httpDump" %JAVA_EXE% -classpath %CP% nablarch.test.core.http.dump.RequestDumpServer

set TMP_DIR=%~dp1\..\dumptool
mkdir %TMP_DIR%
set TMP_HTML=%TMP_DIR%\%~n1_temp.html
%JAVA_EXE% -classpath %CP% nablarch.test.core.http.dump.HtmlReplacerForRequestUnitTesting %1 %TMP_HTML%

start %TMP_HTML%


