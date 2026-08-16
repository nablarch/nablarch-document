# 作業依頼: テスティングフレームワーク本体の事象4件の仕様判定と対応

宛先: `nablarch-testing` の担当

## 0. この依頼の位置づけ

NTF解説書（`nablarch/nablarch-document` の `ntf-yaml-support` ブランチ）を全面的に作り直している。その過程で、テスティングフレームワーク本体に4つの事象を確認した。**解説書にどう書くかがこの判定に依存する**ため、判定をいただきたい。

**この依頼は「不具合を直してください」ではない。** まず**NTF仕様として、この挙動が意図されたものかどうかを判定していただきたい**。仕様であれば、そう判定していただければそれでよい（解説書側に仕様として書く）。不具合であれば、§6 の方針で対応をお願いしたい。

以下はすべて**実行して観測した事実、またはコードを読んで確認した事実**であって、正誤の判断を含まない。「未確認」と書いた箇所は、依頼者が確認できなかったものである。

**急ぎではない。** YAML対応も解説書の刷新もいずれも開発中で、まだリリースしない。利用者はいないため、期限より**判定の正しさを優先していただきたい**。

## 1. 検証環境

| 項目 | 値 |
| --- | --- |
| `nablarch-testing` | `e21bf67`（読み取りはすべて `git show e21bf67:<path>` で行った） |
| `nablarch-core` | `~/.m2` の `6-NEXT-SNAPSHOT` sources jar（`nablarch-core-6-NEXT-20260717.011251-20-sources.jar`） |
| 解説書 | `nablarch/nablarch-document` `ntf-yaml-support` の `7e19f68`。削除前の現行解説書は `2e501ad` |
| OS | Linux（WSL2）、JDK Temurin 21.0.11+10 |

---

## 2. 事象1: リクエストデータ作成ツールに Linux 用の起動スクリプトが配布されていない

### 2-1. 観測した事実

解説書が配布しているリクエストデータ作成ツールの配布物は、**`httpDump.bat` の1ファイルだけ**である。

- 現行解説書（`2e501ad`）: `ja/development_tools/testing_framework/guide/development_guide/08_TestTools/01_HttpDumpTool/download/httpDump.bat`
- 作り直し中の解説書（`7e19f68`）: `ja/development_tools/testing_framework/tools/downloads/request_data_tool/httpDump.bat`（内容は上と完全に同一。パスを移しただけ）

`.sh` は**どちらにも存在しない**（`git ls-tree -r --name-only <ref> | grep -i httpdump` で確認）。

一方、現行解説書の本文には Linux 向けの記述がある。

```
「Linuxの場合はシェルスクリプト(httpDump.sh)を選択する」
```

配布されていないファイルを選択するよう案内している状態になっている。

なお `nablarch-testing` 側には `src/main/script/httpDump.sh` が存在するが、これは配布物とは別物である（事象2を参照）。

### 2-2. 判定していただきたいこと

1. **リクエストデータ作成ツールは Windows 専用か。** 専用であれば、解説書には「Windowsでのみ使用できる」と書く
2. Windows 専用でない場合、**Linux 用の起動スクリプトを配布物に含めるべきか**

---

## 3. 事象2: `src/main/script/httpDump.{bat,sh}` が配布物と乖離し、そのままでは動かない

### 3-1. 観測した事実

`nablarch-testing@e21bf67` の `src/main/script/` に2つのスクリプトがある。

**`src/main/script/httpDump.bat`**

```bat
set LIB_DIR=../lib
set NTF_JAR=%LIB_DIR%/nablarch-tfw.jar
set POI_JAR=%LIB_DIR%//poi-3.2-FINAL-20081019.jar
set JETTY_JAR=%LIB_DIR%//jetty.jar;../lib/jetty-util.jar;
set SERVLET_JAR=%LIB_DIR%//servlet-api.jar
set CP=%NTF_JAR%;%POI_JAR%;%JETTY_JAR%;%SERVLET_JAR%
set JAVA_EXE=%JAVA_HOME%\bin\java\java.exe
```

- 参照している `nablarch-tfw.jar` は Nablarch 1.x 時代の成果物名である
- `poi-3.2-FINAL-20081019.jar` は 2008年10月版の POI を指している
- `%JAVA_HOME%\bin\java\java.exe` は**存在しないパス**である（正しくは `%JAVA_HOME%\bin\java.exe`）

**`src/main/script/httpDump.sh`**

```sh
CP=http-dump-1.0-jar-with-dependencies.jar
java -classpath ${CP} nablarch.test.core.http.dump.RequestDumpServer &
...
firefox ${TMP_FILE}
```

- 参照している `http-dump-1.0-jar-with-dependencies.jar` は配布物に含まれていない
- 末尾でブラウザを `firefox` に決め打ちしている

**配布物側（解説書の `httpDump.bat`）はこうなっている。**

```bat
set CP=./lib/*
set JAVA_EXE="%JAVA_HOME%\bin\java"
```

配布物のほうは現行の構成に追随しており、`src/main/script/` 側だけが取り残されている。

### 3-2. 判定していただきたいこと

1. **`src/main/script/httpDump.{bat,sh}` は現在も使われているか。** 使われていない（配布物が正で、こちらは残骸）のであれば、削除すべきか
2. 使われているのであれば、**現行の構成に合わせて更新すべきか**

### 3-3. あわせて教えていただきたいこと（依頼者が特定できなかった）

`nablarch.test.core.http.dump.RequestDumpServer` と `nablarch.test.core.http.dump.HtmlReplacerForRequestUnitTesting` の**実装がどのモジュールにあるのかを特定できなかった**。`nablarch-testing@e21bf67` を探した範囲では、`src/main/resources/nablarch/test/core/http/dump/template.xls` があるだけで、Java の実装は見つからない。

解説書の第2部に「`nablarch-testing-jetty12` は内蔵サーバの実装を提供するだけで、コンポーネントの登録までは行わない」という記述があり、この記述が正しいかどうかを判断するのに必要である。**どのモジュールが `nablarch.test.core.http.dump` の実装を持つかを教えていただきたい。**

---

## 4. 事象3: YAML形式のテストデータで、同期応答メッセージのモックアップの再読み込みが働かない

### 4-1. 観測した事実

**解説書（および現行解説書の出典 `send_sync.rst:176-177,187`）の記述**

> テストデータのタイムスタンプが更新されると、モックアップクラスはテストデータを読み込み直し、次に返す応答電文を1件目に戻す

**実装**

`src/main/java/nablarch/test/core/messaging/SendSyncSupport.java` の `createTestDataInfo`。

```java
File file = filePathSetting.getFileIfExists(SEND_SYNC_TEST_DATA_BASE_PATH, requestId);   // :348
...
if (fileCache.containsKey(cacheKey)) {
    TestDataInfo cachedTestDataInfo = fileCache.get(cacheKey);
    // 読み込むテストデータファイルのタイムスタンプが変更された場合、再読み込みを行う
    if (file.lastModified() != cachedTestDataInfo.lastModified) {                        // :360
```

**`getFileIfExists` が返すもの**

`nablarch-core` の `FilePathSetting`。

```java
public File getFileIfExists(String basePathName, String fileName) {
    File resolved = resolvePath(basePathName, fileName, false);
    return resolved.exists() ? resolved : null;
}

protected File resolvePath(String basePathName, String fileName, boolean createNew) {
    URL basePathUrl = getBasePathUrl(basePathName);
    // ベースパスに対応する拡張子が存在するならば、引数のファイル名に拡張子を結合する
    String fileNameJoinExtension = getFileNameJoinExtension(basePathName, fileName);
    File file = new File(basePathUrl.getFile(), fileNameJoinExtension);
    ...
}
```

拡張子は、そのベースパスに拡張子が設定されている場合にだけ結合される。

**YAML形式では `sendSyncTestData` に拡張子を設定しない。** したがって `new File(base, requestId)` となり、これは**リクエストIDと同じ名前のディレクトリ**を指す。ディレクトリも `exists()` は `true` を返すので、`getFileIfExists` はそのディレクトリを返す。

**ディレクトリの最終更新日時は、配下のファイルを上書き編集しても変わらない。** この環境で実測した。

```
$ mkdir -p RM21AA0101 && echo a > RM21AA0101/message.yaml
$ stat -c %Y RM21AA0101          → 1786796772
（1.2秒待って）
$ echo b > RM21AA0101/message.yaml
$ stat -c %Y RM21AA0101          → 1786796772   （変わらない）
$ stat -c %Y RM21AA0101/message.yaml → 1786796774   （ファイル側は更新されている）
```

結果として、YAML形式では `:360` の比較が常に等しくなり、**再読み込みの分岐に入らない**と読める。

Excel形式では `sendSyncTestData` に拡張子を設定するため、`getFileIfExists` はブックファイル自体を返し、上書き編集で `lastModified()` が変わる。**この非対称は実測ではなくコードからの帰結である。**

### 4-2. 判定していただきたいこと

1. **YAML形式でも再読み込みが働くべきか。** 働くべきであれば不具合、Excel形式限定の機能であれば仕様と判定していただきたい
2. 仕様と判定する場合、**解説書にはどう書くのが正しいか**（「Excel形式でのみ再読み込みされる」でよいか）

---

## 5. 事象4: マスタデータ投入ツールが、YAML形式のパーサ設定下で無言で0件になる

### 5-1. 観測した事実

`src/main/java/nablarch/test/core/db/MasterDataSetUpper.java:188` が、システムリポジトリから `testDataParser` を取得している。

```java
TestDataParser parser = SystemRepository.get("testDataParser");
```

マスタデータファイルは Excel 形式で記述する前提だが、YAML形式を採用したプロジェクトはコンポーネント設定ファイルの `testDataParser` に YAML 用のパーサを設定している。この状態で Excel 形式のマスタデータファイルを指定すると、**投入対象が0件になり、例外も警告も出ない**。

これは作り直し中の解説書がすでに本文に書いている（`ja/development_tools/testing_framework/tools/master_data_tool.rst:28`）。**この記述が正しいかどうかの確認を含めて判定いただきたい。**

### 5-2. 判定していただきたいこと

1. **この記述は正しいか。** YAML形式を採用したプロジェクトではマスタデータ投入ツールを使えない、という理解でよいか
2. **無言で0件になってよいか。** 利用者が投入されたと誤認する。検出してエラーにすべきか
3. YAML形式のマスタデータファイルに対応する予定はあるか

---

## 6. 不具合と判定した場合の対応方針

**テスト駆動で対応をお願いしたい。** 手順は次のとおり。

1. **先に、失敗する再現テストを書く。** 期待する挙動をアサートするテストを追加し、この時点でテストが**失敗すること**を確認して、テストだけをコミットする（コミットメッセージに「再現テストを追加する」旨を書く）
2. **実装を直す。** 直したうえで、1のテストが通ることを確認する
3. **既存テストが壊れていないことを確認する**

事象ごとに原因が異なるため、**同じコミットにまとめず、事象ごとに再現テスト → 修正の単位で進めていただきたい。**

事象3の再現テストは、YAML形式のテストデータ（リクエストIDと同名のディレクトリ配下の `message.yaml`）を用意し、モックアップから1回読ませたあとに配下のファイルだけを上書き編集して、2回目の読み出しで応答電文が1件目に戻ることをアサートする形になると考える。

事象1・2はスクリプトと配布物の問題なので、自動テストで縛れるかどうかを含めて判断していただきたい。

## 7. 回答していただきたい形式

事象ごとに次を返していただきたい。

- **判定**: 仕様 / 不具合 / 判断保留（保留の場合は何が決まれば判定できるか）
- **仕様と判定した場合**: そう言える根拠。解説書にそのまま書けるだけの説明があると助かる
- **不具合と判定した場合**: 対応する版と、おおよその見込み時期

あわせて §3-3（`nablarch.test.core.http.dump` の実装がどのモジュールにあるか）にも回答をお願いしたい。

解説書側は、**判定が出るまで該当箇所に TODO を残し、不具合が直る前提で本文を書く**方針で進める。仕様と判定された場合は本文を仕様に合わせて書き直すので、その旨をお知らせいただきたい。

## 8. 禁止事項

- 依頼者は不具合と断定していない。**まず仕様かどうかを判定すること**
- 判定より先に実装を直さないこと
- 再現テストを書く前に実装を直さないこと
