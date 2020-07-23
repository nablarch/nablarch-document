@echo off
cd /d %~dp0

start "httpDump" mvn exec:java -Dexec.classpathScope="test" -Dexec.mainClass=nablarch.test.core.http.dump.RequestDumpServer

set TMP_DIR=%~dp1\..\dumptool
mkdir %TMP_DIR%
set TMP_HTML=%TMP_DIR%\%~n1_temp.html
call mvn exec:java -Dexec.classpathScope="test" -Dexec.mainClass=nablarch.test.core.http.dump.HtmlReplacerForRequestUnitTesting -Dexec.args="'%1' '%TMP_HTML%'"

start %TMP_HTML%
