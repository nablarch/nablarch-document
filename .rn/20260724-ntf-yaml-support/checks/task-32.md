# #32 Completion Check

対象コミット: `b3e76fc`（手順1）・`0806ea5`（手順2・3・4・8）・`9031fa6`（手順5・6・7）。ブランチ `ntf-yaml-support`、開始コミット `c2b725d`。push 済み。

是正指示 `ntf-doc-32-fix.md` の処置は `811d1cb`（4観点レビューの有効な指摘11件）。`origin/ntf-yaml-support` も `811d1cb` を指している。

実行日: 2026-08-21。実行環境: Docker イメージ `nablarch-document-build`。

`file:line` は特記のない限り本タスク適用後の作業ツリーを指す。`.rn/` 内の文書どうしの参照は節見出しで指す。

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| `grep -rho 'TODO(NTF-[A-Z0-9-]*)' ja/ \| sort \| uniq -c` の結果が5件・5ID になる（`NTF-MOD-01-2` / `NTF-MOD-01-3` / `NTF-MOD-02-3` / `NTF-MOD-02-4` / `NTF-MOD-03-1` の各1件） | OK | `$ grep -rho 'TODO(NTF-[A-Z0-9-]*)' ja/ \| sort \| uniq -c` → `1 TODO(NTF-MOD-01-2)` / `1 TODO(NTF-MOD-01-3)` / `1 TODO(NTF-MOD-02-3)` / `1 TODO(NTF-MOD-02-4)` / `1 TODO(NTF-MOD-03-1)`。合計5件・5ID で指定と一致 | | |
| `tools/testdata_converter.rst` に「意図のある情報」の行として「無損失で保持する。空欄のレコード種別が該当する」があり、「マーカーカラム」は「意味を持たない情報」の行にだけ現れる。`grep -n 'マーカーカラム' …` のヒットが2件だけになる | 判定文はOK／件数条件はNG（実測3件） | `$ grep -n '無損失で保持する' ja/…/tools/testdata_converter.rst` → `:37     - 無損失で保持する。空欄のレコード種別が該当する` の1件のみ。`$ grep -n 'マーカーカラム' ja/…/tools/testdata_converter.rst` → `:39`（「意味を持たない情報」の行）・`:69`（「前提事項」の新段落）・`:278`（`markerColumnColor` の説明「マーカーカラムの背景色」）の**3件**。`:278` は本タスクの対象外の既存行である（`$ git show c2b725d:…/testdata_converter.rst \| grep -n 'マーカーカラム'` → `37` と `276` の2件。`276` が現 `:278`）。指示書の完了条件2 がこの既存行を数え落としていた。詳細は下の「完了条件2・3 の字義と実測の食い違い」 | | |
| 削除した9ファイルへの参照が `ja/` 配下に残っていない | OK（実質）／指示書の grep 文字列そのままではNG | ファイル名で指す精密なパターンでの実測: `$ grep -rnE 'batch_request_test_class\|real_request_test_class\|send_sync\.(png\|xlsx)\|rest_request_unit_test_structure\|web/request_unit_test_structure\|class_structure\|abstract_structure' ja/ --exclude-dir=_build` → **0件**（exit 1）。指示書の文字列のまま（`send_sync` 単体・`request_unit_test_structure` 単体）だと `images/mom/send_sync_base.png`・`send_sync_online_base.png`・`send_sync_online_mock.png`・`send_sync_test_data_no.png`・`send_sync_response_count_change.png`・`send_sync_test_data_structure.png`・`:ref:` ラベル `testing_framework_common-send_sync_test_data` など、残すべき別ファイル・別ラベル11件にヒットする。詳細は下の「完了条件2・3 の字義と実測の食い違い」 | | |
| `python3 mapping/tools/verify_glossary.py` が `RESULT: OK` | OK | `.rn/20260724-ntf-yaml-support` をカレントにして `$ python3 mapping/tools/verify_glossary.py` → 末尾 `RESULT: OK`（`design_sections 検証 21 件 / 不一致 0 件`、`scheme_names 検証 7 件 / 不一致 0 件`、`reasons 検証 0 件 / 不一致 0 件`）。※`mapping/` はリポジトリルートではなく `.rn/20260724-ntf-yaml-support/` の直下にある | | |
| `python3 mapping/tools/verify_mapping.py` が `OK: no errors` | OK | 同上のカレントで `$ python3 mapping/tools/verify_mapping.py` → 末尾 `OK: no errors` | | |
| `python3 -m pytest mapping/tools -q` が `183 passed, 96 subtests passed` | OK | 同上のカレントで `$ python3 -m pytest mapping/tools -q` → `183 passed, 96 subtests passed in 2.69s` | | |
| Docker でフルビルドし、`grep -cE 'WARNING:\|ERROR:\|SEVERE:' build.log` が 0。ビルド直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を必ず実行する | OK | `$ docker run --rm -v /home/tie303177/work/nablarch/nablarch-document:/root/document nablarch-document-build /bin/bash -c "cd /root/document; rm -rf _build; sphinx-build -d _build/.doctrees/ja -b html ja _build/html" > build.log 2>&1` → `rc=0`、末尾 `build succeeded.`。直後に `$ git -C /home/tie303177/work/nablarch/nablarch-document checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行済み。`$ grep -cE 'WARNING:\|ERROR:\|SEVERE:' build.log` → `0`。※直前の増分ビルドでは `WARNING: unsupported build info format in '/root/document/_build/html/.buildinfo', building all` が1件出た。これは前回ビルドの残骸 `.buildinfo` の形式不一致によるもので、本タスクの変更とは無関係である。`_build` を消してからビルドし直して0件になることを確認した。`build.log` と `_build/` はコミットしない | | |
| `checks/task-32.md` に、手順1-3・2-2・3-2・4-3 の記録と、手順9の台帳がある | OK | 本ファイルの「手順1-3 …」「手順2-2 …」「手順3-2 …」「手順4-3 …」「手順9 TODO台帳」の各節 | | |
| `#31` が check-off されている（手順0。調整役が `1618faf` で完了済み） | OK | `$ git log --oneline -6` に `1618faf docs: complete task #31 — 記録の誤記5件を削って直し、未解決9件の送り先を記す` がある。`steering.md` の `#31` の節見出しが `— DONE` で終わり、`#32` の Steps の手順0 が `- [x] 0. …— 1618faf で完了` になっている。`checks/task-31.md` はブランチに入っている（`$ git status --porcelain` に未追跡として出ない） | | |

## Completion Criteria（是正指示 `ntf-doc-32-fix.md`）

上の `## Completion Criteria` は `#32` の当初の完了条件（対象は `b3e76fc`・`0806ea5`・`9031fa6`）。以下は是正指示 `ntf-doc-32-fix.md` §「完了条件」の1〜14（対象は `811d1cb`）。Self-check はすべて本ファイルの書き手が自分でコマンドを実行して判定した。`ja/…/` は `ja/development_tools/testing_framework/` からの相対、`.rn/…/` は `.rn/20260724-ntf-yaml-support/` からの相対を表す。

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| 1. `grep -n '空エントリ' ja/…/tools/testdata_converter.rst` が0件 | OK | `$ grep -n '空エントリ' ja/…/tools/testdata_converter.rst` → 出力なし（exit 1）。`$ grep -c '空エントリ' …` → `0` | | |
| 2. `grep -n 'マーカーカラム' ja/…/tools/testdata_converter.rst` が `:39`・`:69`・`:278` の3件（`:37` に無い） | OK | `$ grep -n 'マーカーカラム' ja/…/tools/testdata_converter.rst` → `:39`（「意味を持たない情報」の行）・`:69`（前提事項の段落）・`:278`（`markerColumnColor` の説明）の3件のみ。`:37` は `- 無損失で保持する。空欄のレコード種別が該当する` でヒットしない | | |
| 3. `grep -n 'testing_framework_setup' ja/…/about/index.rst` が1件 | OK | `$ grep -n 'testing_framework_setup' ja/…/about/index.rst` → `:106` の1件（本文2文目の直後に挿入した参照。段落は1行のまま） | | |
| 4. `grep -c 'AbstractHttpRequestTestTemplate' ja/…/implementation/request_unit_test/web.rst` が0 | OK | `$ grep -c 'AbstractHttpRequestTestTemplate' ja/…/implementation/request_unit_test/web.rst` → `0` | | |
| 5. `_batch/*.csv` を昇順に連結した結果が `mapping/mapping.csv` とバイト一致する。`csv.DictReader` の行数が編集前と同じ597行 | OK | `.rn/…/mapping` をカレントにして `_batch/*.csv` 30ファイルを昇順連結（先頭のみヘッダ込み、2つ目以降はヘッダ除く）→ `byte-identical: True`、`rows: 597`。編集前の `$ git show 811d1cb^:.rn/…/mapping/mapping.csv` を `csv.DictReader` に流して数えた結果も `597`。編集した7ファイルの行数も編集前後で不変。詳細は下の「是正§3-3 マッピング台帳7行への追記」 | | |
| 6. `design.md` に `### 利用側ページに内部構造の構成図を置かない` が存在し、`:137` の見出しが `### 「アーキテクチャ」は本文のみとし、図も構成物一覧の表も置かない` になっている | OK | `$ grep -n '^### ' .rn/…/design.md` → `137:### 利用側ページに内部構造の構成図を置かない`（新設）と `149:### 「アーキテクチャ」は本文のみとし、図も構成物一覧の表も置かない`（差し替え後）。**指示書は後者を `:137` と書いているが、これは新節を直前に挿入する前の行番号である。**現物では新節が `:137`、差し替えた既存節が `:149`。要求の内容（新節が存在し、既存節の見出しが差し替わっている）は満たしている | | |
| 7. `steering.md` に `#33` のエントリが存在する | OK | `$ grep -n '#33' .rn/…/steering.md` → `921:### #33: 記法の適用順序の明文化と、残置図の禁止語点検`（ほかに `#32` の Steps 16 と当該完了条件の行がヒットする） | | |
| 8. `python3 mapping/tools/verify_glossary.py` が `RESULT: OK` | OK | `.rn/20260724-ntf-yaml-support` をカレントにして `$ python3 mapping/tools/verify_glossary.py` → 末尾 `RESULT: OK`（`population 検証 331 件 / 不一致 0 件`、`design_sections 21 件 / 0 件`、`scheme_names 7 件 / 0 件`、`reasons 0 件 / 0 件`） | | |
| 9. `python3 mapping/tools/verify_mapping.py` が `OK: no errors` | OK | 同上のカレントで `$ python3 mapping/tools/verify_mapping.py` → 末尾 `OK: no errors` | | |
| 10. `python3 -m pytest mapping/tools -q` が `183 passed, 96 subtests passed` | OK | 同上のカレントで `$ python3 -m pytest mapping/tools -q` → `183 passed, 96 subtests passed in 1.59s` | | |
| 11. Docker フルビルドで `grep -cE 'WARNING:\|ERROR:\|SEVERE:' build.log` が 0 | 調整役が実施 | 本ファイルの書き手は判定していない | | |
| 12. 禁止事項（`ja/conf.py`・`mapping/glossary.md` §5.15・`mapping.csv` 直接編集・`en/`・`locales/` の `.gitignore` 追加）に触れていない | OK | `$ git diff --name-only 811d1cb^..811d1cb` → 16ファイル。`$ … \| grep -E 'ja/conf\.py\|glossary\.md\|^en/\|^locales/\|\.gitignore'` → 0件（exit 1）。`cf2ef3f` は `811d1cb^` と同一コミットのため `$ git diff --stat cf2ef3f..HEAD` も同じ16ファイルを返す。`mapping/mapping.csv` は一覧に含まれるが、`_batch/*.csv` の連結とバイト一致する（完了条件5）ため直接編集ではなく `_batch/` からの再生成である | | |
| 13. `checks/task-32.md` に §1-3（`:278`）・§3-3（台帳7行）・§5（jar の実測）の記録がある | OK | §1-3 は本ファイル「気づいた点（本タスクでは処置していない）」の項目2、§3-3 は本ファイル「是正§3-3 マッピング台帳7行への追記」、§5 は本ファイル「手順2-2 NTF-MOD-02-2 を外した根拠」の3つ目の箇条書き | | |
| 14. `#32` が check-off されている | 調整役が実施 | 本ファイルの書き手は判定していない | | |

## 完了条件2・3 の字義と実測の食い違い

**完了条件2** — 指示書が挙げた2件（「意味を持たない情報」の行・「前提事項」の新段落）に加えて、`tools/testdata_converter.rst:278` に「マーカーカラム」がもう1件ある。「Excel形式の出力を整形する」節の設定項目表にある `markerColumnColor` の説明「マーカーカラムの背景色」で、本タスクが触る箇所ではなく、開始コミット `c2b725d` の時点で既に存在していた（当時は `:276`）。したがって件数は3件になる。判定の本体（「意図のある情報」の行が「無損失で保持する。空欄のレコード種別が該当する」であること、中間モデルの扱いの表では「マーカーカラム」が「意味を持たない情報」の行にだけ現れること）は満たしている。

**完了条件3** — 指示書の grep 文字列は `send_sync`・`request_unit_test_structure` を部分一致で指しているため、削除対象ではない別ファイルにもヒットする。実測11件の内訳は次のとおりで、いずれも残すべきものである。

| ヒット箇所 | 中身 |
|---|---|
| `implementation/deal_unit_test/mom.rst:21`・`:26`・`:80`・`:89` | `images/mom/send_sync_online_base.png`・`send_sync_online_mock.png`・`send_sync_test_data_no.png`・`send_sync_response_count_change.png`（いずれも現存し参照されている画像） |
| `implementation/request_unit_test/mom.rst:39` | `images/mom/send_sync_base.png`（現存し参照されている画像。削除した `send_sync.png` とは別ファイル） |
| `setup/common.rst:183` | `images/common/send_sync_test_data_structure.png`（同上） |
| `setup/common.rst:118`、`setup/deal_unit_test/mom.rst:33`、`setup/deal_unit_test/http_messaging.rst:35`、`implementation/deal_unit_test/http_messaging.rst:26` | `:ref:` ラベル `testing_framework_common-send_sync_test_data` の定義と参照3件 |

削除した9ファイルをファイル名で指すパターンに直すと0件になる（上の Evidence 参照）。なお `ja/_build/` はビルド成果物のディレクトリで `.gitignore:2` の `_build/` により追跡対象外である（`$ git check-ignore -v ja/_build` → `.gitignore:2:_build/	ja/_build`）。追跡ファイルだけを見る `git grep` でも結果は同じであることを確認した。

## 手順1-3 中間モデルの表の書き換えの根拠

指示書 `ntf-doc-32.md` §1-1 が逐語で与えたものをそのまま引く（出典は `nablarch-testing-converter` のコミット `229201f`。モジュール側リポジトリは本作業ディレクトリの外にあるため、指示書の逐語引用を出典として扱う）。

**(a) マーカーカラムは中間モデルに入らない** — `:39` へ移した根拠。

- `src/main/java/nablarch/test/core/reader/TestCoreReaderAdapter.java:129`

  ```
  return Arrays.asList(header.getEffectiveColumnNames());
  ```

  `getEffectiveColumnNames` はマーカーカラムを除いたカラム名を返す。
- `.rn/ntf-test-data-converter/steering.md:475`（完了条件）

  ```
  - マーカーカラム（`[no]` 等）が変換後のYAML / Excelに含まれない（除外が機能している）
  ```

**(b) 空エントリは中間モデルに入らない** — `:39` へ加えた根拠。

- `src/main/java/nablarch/test/tool/converter/xls/XlsFormatReader.java:566`

  ```
  private static List<List<String>> dropEmptyEntries(List<List<String>> rows) {
  ```
- 同 `:583`

  ```
  private static boolean isEmptyEntry(List<String> row) {
  ```
- 呼び出しは同ファイルの `:162` と `:193`。

**(c) 空欄のレコード種別は中間モデルに保持される** — `:37` に残した根拠。

- `src/main/java/nablarch/test/tool/converter/xls/XlsFormatReader.java:308`

  ```
  String recordType = emptyToNull(bodyLines.get(idx).get(0));
  ```
- 同 `:327-329`

  ```
  private static String emptyToNull(String recordType) {
      return recordType == null || recordType.isEmpty() ? null : recordType;
  }
  ```
- `src/main/java/nablarch/test/tool/converter/model/RecordLayout.java:66`

  ```
  /** @return レコード種別（省略時は {@code null}） */
  ```

  空セルは中間モデルで `null` として保持される。

これにより `checks/task-31.md`「申し送り」1（`:39` の「外側」の限定）と3（表に残した「マーカーカラム」「空欄のレコード種別」の検証）は解消となる。「外側」の語は `:39` にそのまま残っているが、対になる「内側」が `#31` で外されて宙に浮いていた問題は、同じ行に「マーカーカラム、空エントリ」が並んだことで「外側」がデータブロックの外の空行だけを指す限定として読めるようになった。

## 手順2-2 NTF-MOD-02-2 を外した根拠

指示書 `ntf-doc-32.md` §2-2 が逐語で与えた実測をそのまま引く。ただし3つ目の箇条書きは誤りだったため、是正指示 `ntf-doc-32-fix.md` §5 の実測に差し替えた（本タスクで再実測して一致を確認した）。

計測対象: `~/.m2/repository/com/nablarch/framework/nablarch-testing-jetty12/1.1.0/nablarch-testing-jetty12-1.1.0.jar`

- 含まれるクラスは12件のみ。
  - `nablarch/test/core/http/dump/` … `SimpleReplacer`、`RequestDumpServlet`、`RequestDumpAgent`、`RequestDumpServerShutdownFilter`、`RequestDumpServer`、`RequestDumpServer$1`、`HtmlReplacerForRequestUnitTesting`（7件）
  - `nablarch/fw/web/httpserver/` … `HttpServerFactoryJetty12`、`HttpServerJetty12`、`LazySessionInvalidationFilter`、`LazySessionInvalidationFilter$RequestWrapper`、`LazySessionInvalidationFilter$SessionWrapper`（5件）
- コンポーネント定義ファイル（`.xml` / `.config`）は同梱されていない（`META-INF/maven` 配下の `pom.xml` と `pom.properties` のみ）。
- `nablarch-testing` の jar 側（是正指示 `ntf-doc-32-fix.md` §5 の実測。本タスクで `unzip -l` により再実測し一致を確認した）: `nablarch/test/core/http/dump/template.xls`（15872 バイト）は 1.2.0・1.3.0・1.4.0・1.7.0・2.0.0・6u3・6-NEXT-SNAPSHOT のいずれにも存在する。1.3.0 以降で消えたのは同パッケージの `.class` 7件（`RequestDumpAgent`・`SimpleReplacer`・`RequestDumpServlet`・`HtmlReplacerForRequestUnitTesting`・`RequestDumpServerShutdownFilter`・`RequestDumpServer`・`RequestDumpServer$1`）だけである。1.2.0 は dump 配下9エントリ（`.class` 7件＋`template.xls`＋ディレクトリ）、1.3.0 以降は2エントリ（`template.xls`＋ディレクトリ）。
  - 消えたのはクラスであり、`.. important::` が言う「提供するのは…クラスだけ」の結論は倒れない。残る `template.xls` はクラスではなくリソースで、`nablarch-testing-jetty12` が提供する12クラスとコンポーネント定義非同梱という上の2点は変わらない。

これにより `setup/request_unit_test/rest.rst` の `.. important::`（「``nablarch-testing-jetty12`` が提供するのは、内蔵サーバとリクエスト単体データ作成ツールのクラスだけである。コンポーネントの登録は行わないため…」）は裏付けられた。**上の jar の訂正によっても `.. important::` の結論は倒れない。**`.. important::` の本文は `#32`・是正のいずれでも変えていない（`$ git diff c2b725d..811d1cb -- ja/…/setup/request_unit_test/rest.rst` の差分は TODOブロック3行と直後の空行1行の削除だけ。是正コミットでは当該ファイル自体が無変更）。

## 手順3-2 NTF-SRC-01 を外した根拠

指示書 `ntf-doc-32.md` §3-2 が逐語で与えた出典をそのまま引く。

- JUnit 5.3.0 リリースノート https://docs.junit.org/5.3.0/release-notes/index.html 節「Deprecations and Breaking Changes」より逐語:

  ```
  The JUnit Platform Surefire Provider (`junit-platform-surefire-provider`) is now
  deprecated in favor of the native support for the JUnit Platform provided by
  Maven Surefire 2.22.0 and later versions.
  ```
- Apache Maven Surefire Plugin 2.22.0 リリース告知（2018-06-17） https://blogs.apache.org/maven/entry/apache-maven-surefire-plugin-2 New Features より逐語:

  ```
  SUREFIRE-1330 – JUnit 5 surefire-provider code donation
  ```

これで `setup/junit5_extension.rst` の「JUnit 5を使用するには、``maven-surefire-plugin`` が2.22.0以上である必要がある。」の下限値に一次出典が付いた。本文は変えず、TODOブロック4行だけを削除した。

## 手順4-3 NTF-SRC-02 を外した根拠と「Open With」の扱い

**UI項目名の英語名の出典**（本リポジトリ内、コミット `65a1756`。逐語は本タスクで現物を開いて確認した）:

`en/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/02_RequestUnitTest.rst`

| 行 | 逐語 |
|---|---|
| `:499` | `* Select "Run(実行)" > "Run Configuration(実行構成)" from the menu bar.` |
| `:501` | `* In the "Run Configuration(実行構成)" window, click on the "Arguments(引数)" tab and specify the above options in the "VM Arguments(VM引数)" field.` |
| `:507` | `* Select "Window(ウィンドウ)" > "Settings(設定)" from the menu bar. In the "Settings(設定)" window that is displayed, select "Installed JREs(インストール済みのJRE)".` |
| `:509` | `* Select the JRE you want to use from the list of installed JREs that is displayed, and click the "Edit(編集)" button.` |

「デフォルトの VM 引数」だけは en 側 `:513` が `* Specify the above-mentioned option in the "VM argument(VM引数)" field.` となっており、`setup/request_unit_test/web.rst` の画面ショット `images/web/edit_jre.png` に写っている「デフォルトの VM 引数(V):」と一致しないため、en を根拠にしない。Eclipse公式ヘルプを出典とする。

- https://help.eclipse.org/latest/topic/org.eclipse.jdt.doc.user/tasks/task-add_new_jre.htm
- 逐語: `In the Default VM Arguments field, you can add/edit the default arguments that will be passed to the VM when launching.`

**「Open With」の扱い** — `tools/request_data_tool.rst` の「HTMLダンプからツールを起動する」節にあった「Open With」は、日本語名の一次情報が本作業環境で取得できなかった。そのため項目名を書かない言い回しに変え、「Eclipseのパッケージエクスプローラなどから、生成されたHTMLダンプを右クリックし、``httpDump`` で開くとツールが起動する。」とした。直後の画面ショット `images/request_data_tool/04_Eclipse_OpenWith.png` は残してある。

これにより `checks/task-last.md` §5-5 の「S-12 規約4 未達9件」は解消となる。

## 手順9 TODO台帳

行番号では指さず、TODO が置かれている節見出しで指す。

| ID | ページ | 節（上位 > 下位） | 内容と外す条件 |
|---|---|---|---|
| `NTF-MOD-01-2` | `tools/testdata_converter.rst` | テストデータ変換ツール > 使用方法（冒頭の「あらかじめ導入の手順を済ませておく。」の直後） | 同名で拡張子違いのExcelブックが同居したときの変換対象の扱い。`nablarch-testing-converter` で `XLS-28`（同居を検出してエラーで止める）として要対応と確定・実装済み（`5ab13d8`、main 未マージ）。依頼書 `ntf-mod-01-nablarch-testing-converter.md` §3。`XLS-28` の対応がマージされたら外す。本文の書き直しは不要 |
| `NTF-MOD-01-3` | `tools/testdata_converter.rst` | テストデータ変換ツール > 機能概要 > 前提事項 | 0件テーブル（YAMLの `rows: []` を持つテーブル系エントリ）を含むYAML形式のテストデータをExcel形式へ変換できない。`nablarch-testing-converter` の `XLS-27` の当面の対応による制約。本体側は `nablarch-testing` の `#23`・`#24` として起票済み・未着手。`#23`・`#24` がマージされ `XLS-27` の2段目へ切り替わったら外す。本文の書き直しは不要 |
| `NTF-MOD-02-3` | `implementation/deal_unit_test/mom.rst` | 取引単体テスト（MOMによるメッセージング） > 使用方法 > テストを実行する | YAML形式で同期応答メッセージのモックアップの再読み込みが働かない。不具合と判定済みで、`nablarch-testing` の `#21` で対応予定・未着手 |
| `NTF-MOD-02-4` | `tools/master_data_tool.rst` | マスタデータ投入ツール > 機能概要 | YAML形式のマスタデータファイルへの対応は `nablarch-testing` の `#22` で対応予定・未着手。Excel形式のマスタデータファイルにYAML形式用のパーサを設定すると無言で0件になる点は仕様と判定済みで、直後の `.. important::` に記載済み。逆向き（YAML形式のファイル＋Excel形式用のパーサ）は未確認 |
| `NTF-MOD-03-1` | `setup/junit5_extension.rst` | JUnit 5用拡張機能 > 拡張例 > 事前処理・事後処理を実装する（節の末尾。直後の「JUnit 4のTestRuleを再現する」節の直前） | `resolveTestRules()` に登録したTimeoutがテスト本体に効かない。不具合と判定済みで、`nablarch-testing-junit5` 側で修正予定・未着手。依頼書 `ntf-mod-03-nablarch-testing-junit5.md` §2。修正後に本文へ反映する |

**実測**

```
$ grep -rho 'TODO(NTF-[A-Z0-9-]*)' ja/ | sort | uniq -c
      1 TODO(NTF-MOD-01-2)
      1 TODO(NTF-MOD-01-3)
      1 TODO(NTF-MOD-02-3)
      1 TODO(NTF-MOD-02-4)
      1 TODO(NTF-MOD-03-1)
```

本タスクで外したのは `NTF-MOD-02-2`・`NTF-SRC-01`・`NTF-SRC-02`（2箇所）・`NTF-FIG-01`〜`04` の7ID・8件。開始時（`c2b725d`）は13件・12ID だった。

## 是正§3-3 マッピング台帳7行への追記

是正指示 `ntf-doc-32-fix.md` §3-3 の処置（`811d1cb`）。`mapping.csv` の直接編集は禁止事項なので、`_batch/*.csv` の `note` 末尾へ追記してから連結で `mapping.csv` を作り直した。既存の `note` は消していない。`current-0322` は是正指示 §3-3 が全走査で追加特定した7行目である。

| mapping_id | ファイル | disposition | 追記した文面 |
|---|---|---|---|
| `current-0165` | `_batch/batch-03.csv` | `MOVE`（変更なし） | (B) |
| `current-0182` | `_batch/batch-09.csv` | `MOVE`（変更なし） | (C) |
| `current-0200` | `_batch/batch-13.csv` | `MOVE`（変更なし） | (A) |
| `current-0281` | `_batch/batch-19.csv` | `MOVE`（変更なし） | (A) |
| `current-0295` | `_batch/batch-21.csv` | `MOVE`（変更なし） | (A) |
| `current-0308` | `_batch/batch-17.csv` | `MOVE`（変更なし） | (A) |
| `current-0322` | `_batch/batch-28.csv` | `MOVE`（変更なし） | (D) |

追記した文面は4種類。いずれも編集後の `_batch/*.csv` を `csv.DictReader` で読み出して逐語を確認した。

- (A) `current-0200`・`0281`・`0295`・`0308`

  ```
  【#32・2026-08-21】この図は削除した。本行の内容は図のみのため、移送先に対応する記述は無い。disposition は割当の履歴として MOVE のまま残す。理由は design.md「利用側ページに内部構造の構成図を置かない」。
  ```
- (B) `current-0165`

  ```
  【#32・2026-08-21】図 abstract_structure.png は削除した。図が示していた関係は about/index.rst の「アーキテクチャ」節の本文に統合済み。disposition は MOVE のまま。理由は design.md「利用側ページに内部構造の構成図を置かない」。
  ```
- (C) `current-0182`

  ```
  【#32・2026-08-21】図 class_structure.png は削除した。「主なクラスとリソース」の表は implementation/class_unit_test/component.rst に存在する。disposition は MOVE のまま。理由は design.md「利用側ページに内部構造の構成図を置かない」。
  ```
- (D) `current-0322`

  ```
  【#32・2026-08-21】図 send_sync.png は削除した。テストクラスのスーパクラスに関する tip は implementation/request_unit_test/mom.rst の「テストクラスを作成する」に存在する。disposition は MOVE のまま。理由は design.md「利用側ページに内部構造の構成図を置かない」。
  ```

**実測**（カレントは `.rn/20260724-ntf-yaml-support/mapping`。編集前は `git show 811d1cb^:.rn/20260724-ntf-yaml-support/mapping/_batch/batch-NN.csv` を `csv.DictReader` に流して数えた）

- `disposition` は7行とも編集前後で `MOVE`。編集前の `mapping.csv` を `csv.DictReader` で読み、7つの `mapping_id` すべてが `MOVE` であることを確認済み。
- `csv.DictReader` の行数（編集前 → 編集後）: `batch-03` 20 → 20、`batch-09` 22 → 22、`batch-13` 20 → 20、`batch-17` 20 → 20、`batch-19` 20 → 20、`batch-21` 20 → 20、`batch-28` 20 → 20。7ファイルとも不変。
- `_batch/*.csv`（30ファイル）をファイル名の昇順に連結（先頭のみヘッダ込み、2つ目以降はヘッダ除く）した結果は `mapping.csv` とバイト一致する。
- `mapping.csv` の `csv.DictReader` 行数は597行。編集前も597行。

```
$ python3 -c "
import glob,io,csv
fs=sorted(glob.glob('_batch/*.csv'))
out=[]
for i,f in enumerate(fs):
    ls=io.open(f,encoding='utf-8').read().splitlines(True)
    out += ls if i==0 else ls[1:]
print('byte-identical:', ''.join(out)==io.open('mapping.csv',encoding='utf-8').read())
print('rows:', len(list(csv.DictReader(io.open('mapping.csv',encoding='utf-8')))))
"
byte-identical: True
rows: 597
```

## Method（作りながら検証した記録）

**指示書が示した「変更前」の文面は、書き換える前にすべて現物を開いて逐語一致を確認した。** 置換は Python の文字列一致で行い、対象文字列の出現回数が1であることを `assert` で確かめてから置換している（0件・複数件ならその場で止まる作りにした）。文字列一致で処置した32箇所（本文の置換・挿入16、行ブロックの削除16）はすべて1件ずつ一致した。残る2箇所（`setup/request_unit_test/rest.rst:51-54`、`setup/junit5_extension.rst:73-76` の削除）は行範囲指定で消したため、消す前に該当行を表示して逐語一致を確認している。

| 主張 | 当てた出典 | 結果 |
|---|---|---|
| `testdata_converter.rst:37`・`:39` の変更前の文面 | 現物（`grep -n ''` で行番号つきに表示） | 逐語一致 |
| `:67` の段落が「ただし Excel 形式のクォート記法…」で終わる | 現物 | 逐語一致。その直後に空行1行を挟んで新段落を挿入した |
| マーカーカラム／空エントリが中間モデルに入らないこと、空欄のレコード種別が保持されること | 指示書 §1-1 の逐語引用（`nablarch-testing-converter` `229201f`） | 上の「手順1-3」節に転記。モジュール側リポジトリは作業ディレクトリの外にあるため見に行っていない |
| `setup/request_unit_test/rest.rst:51-54` が TODOブロック3行＋空行1行であること | 現物 | 一致。`:55` の `.. important::` は変更していない |
| `setup/junit5_extension.rst:73-76` が TODOブロック4行であること | 現物 | 一致。`:77` の空行と `:78` の本文は指示書のとおり残した |
| `setup/request_unit_test/web.rst` の `:190`・`:191`・`:198`・`:202`・`:222` の変更前の文面 | 現物 | 5行とも逐語一致 |
| UI項目名の英語名 | `en/…/02_RequestUnitTest.rst:499`・`:501`・`:507`・`:509`（本リポジトリ内。**現物を開いて逐語を確認した**） | 4行とも指示書の引用と一致 |
| en `:513` が "VM argument(VM引数)" であること（「デフォルトの VM 引数」に en を使わない理由） | 同ファイル `:513` の現物 | 一致（`* Specify the above-mentioned option in the "VM argument(VM引数)" field.`） |
| `tools/request_data_tool.rst:100` の変更前の文面 | 現物 | 逐語一致 |
| `NTF-FIG-01`〜`04` の4ブロックの範囲（`rest.rst:17-22`・`batch.rst:17-22`・`mom.rst:17-21`・`mom.rst:35-40`） | 現物 | 4件とも一致。同一ファイル内の2件（mom.rst）は行番号がずれないよう下（`:35-40`）から処置した |
| 残る `.. image::` 3件と、図に言及する本文2箇所 | 現物（`implementation/request_unit_test/web.rst:17-18`、`implementation/class_unit_test/component.rst:15`・`:17-18`、`about/index.rst:106`・`:108-110`） | 一致。`component.rst:15` の「全体像を次に示す。」と `about/index.rst:106` の「構成物どうしの関係は、次の図のとおり。」を削り、宙に浮いた導入が残らないことを diff で確認した |
| 削除する9ファイルが `ja/` のどこからも参照されなくなること | 手順5の適用後に `grep -rn` で実測 | 削除前に0件を確認してから `git rm` した |
| 「主なクラスとリソース」から削る7行の逐語 | 現物（`web.rst:40-42`・`rest.rst:46-48`・`batch.rst:57-59`・`:51-53`・`mom.rst:93-95`・`:84-86`・`:81-83`） | 7行とも一致。同一ファイル内の複数削除（batch.rst 2件、mom.rst 3件）は文字列一致で処置したため行番号のずれは生じない |
| 本文4箇所（`rest.rst:23`・`batch.rst:23`・`mom.rst:22`・`mom.rst:41`）の変更前の文面 | 現物 | 4箇所とも逐語一致。変更後の文面は指示書の与えたものをそのまま使い、言い換えていない |
| `NTF-MOD-03-1` の変更前3行 | 現物（`setup/junit5_extension.rst`。手順3の削除で `:400-402` → `:396-398` へ4行分ずれていた） | 逐語一致 |
| 段落を途中で改行していないこと | 追加・書き換えた段落はいずれも1行 | `git diff` の追加行が1行ずつであることで確認 |
| 「自動テストフレームワーク」を書いていないこと | `$ git diff \| grep -c '自動テストフレームワーク'` → `0` | OK |
| `en/` を触っていないこと | `$ git status --porcelain` に `en/` の行が無い | OK |
| `list-table` の整合 | 行を削った4つの表を diff で確認 | 削除はいずれも `* - 名称` / `- 役割` / `- 作成単位` の3行1組。列数・`:widths:` は変えていない |

**Docker フルビルドの副産物** — ビルド直後に `git -C /home/tie303177/work/nablarch/nablarch-document checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を毎回実行した（2回のビルドとも）。`git status --porcelain` に `locales/` の行が出ないことを確認済み。

## 気づいた点（本タスクでは処置していない）

1. **`setup/junit5_extension.rst`「前提事項」の直後に空行が1行残る。** 指示書 §3-1 が「`:77` の空行と `:78` の本文は残す」と明示しているためそのままにした。ただし同ファイルの他の `~` 見出しはいずれも下線の次の行から本文が始まっており（`:27-28`・`:80-81`・`:100-101` ほか）、この節だけ体裁が異なる。HTML出力は変わらない。
2. **`tools/testdata_converter.rst:278` の `markerColumnColor`。** 是正指示 `ntf-doc-32-fix.md` §1-3 が一次情報を与えて解決した。`markerColumnColor` が効く対象は、書き手が合成する `XlsFormatWriter.EMPTY_BLOCK_MARKER_COLUMN`（`XlsFormatWriter.java:543`。値は `"[EMPTY]"`）だけである。※本ファイル §「調整役が実測で裏を取った事項」の表はこの定数を `"[空]"` と記録しているが、§1-3 が値を `"[EMPTY]"` と訂正している。したがって読み込んだマーカーカラムに背景色が付くわけではなく、`#32` がこのページに矛盾を新規に作ったのではない。誤っていたのは `#32` 適用前の `:37`「無損失で保持する。マーカーカラム、空欄のレコード種別が該当する」のほうである（`$ git show c2b725d:ja/…/tools/testdata_converter.rst \| grep -n 'マーカーカラム'` → `37` と `276` の2件で現物を確認。`:37` は手順1（`b3e76fc`）で外した）。`:278` が背景色の対象を書いていない点は独立した別件で、本文は `#32`・是正のいずれでも変更していない。
3. **完了条件2・3 の検査コマンド。** 上の「完了条件2・3 の字義と実測の食い違い」のとおり、指示書の grep 文字列では判定できない。次回以降の指示書ではファイル名で指すパターン（`send_sync\.(png|xlsx)` など）にするのがよい。

## QA Expert Review

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| 検証の方法が目的にかみ合っているか（正しいものを測っているか） | NG | (1) 完了条件2 が締めるべき `:278` を数え落としていたため、本変更が同ページ内に作った矛盾（下の三角1）を素通りさせた。(2) 完了条件7 は `WARNING` 行数しか見ず、ビルドが途中で落ちた場合も0を返すため「ビルドが壊れていないこと」を測れない（QA観点が `-a -E` で 49% で異常終了したログに対し `grep -c` が0を返すことを実測）。(3) 手順5・7・8（図3件・表7行・本文3箇所の削除、`NTF-MOD-03-1` の文言差し替え）に対応する完了条件が存在せず、完了条件を全部満たしても目的3 を達したことにならない |

## Expert Reviews (axes the task needs)

### Design Expert

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| 方針・構造が適切か | NG | (1) 図の導入文の処置が1箇所漏れ（`implementation/request_unit_test/mom.rst:28`「…構成を次に示す。」の指す先が無い）。指示書 §5-2 が他2箇所で処置した型と同じ。(2) `about/index.rst` から、削除図が持っていた「Nablarch Application Framework →コンポーネント設定ファイル/環境設定ファイル（読み取る）」の関係が失われた（`design.md` の当該節が図の内容として列挙している逐語と、`:106` の本文を突き合わせて確認）。(3) 表のリード文が2種類に割れている（`web.rst:17`・`rest.rst:19` は「テストを構成する主な」、他4ページは「このページで扱う主な」）。新しい採否基準と整合するのは後者。(4) `rest.rst` の表に `SimpleRestTestSupport` が無い（本文 `:17`・`:52` は利用者が継承するクラスとして示す。変更前からの欠落） |
| 体系全体の整合 | NG | `mapping/mapping.csv` の `disposition=MOVE` の6行（`current-0165`・`0182`・`0200`・`0281`・`0295`・`0308`）が、今回削除した図を移送先の内容としている。うち4行は `note` が「…pngの構成図**のみ**」で、行の内容がまるごと消えた。`verify_mapping.py` は節の存在と行数しか見ないため `OK: no errors` を返すが、台帳の不変条件は破れている。あわせて `design.md` の節見出し「「アーキテクチャ」は図のみとし、構成物一覧の表は置かない」と本文「内容もすでに図と導入文のみという最小限に絞られている」が、図を落とした現物と矛盾する。`:ref:`・`toctree`・画像参照の解決性は OK（削除9ファイルへの参照0件、`.. image::` の指す先はすべて実在） |

### Craft Expert (writing)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| 日本語技術文書としての明快さ・正確さ | NG | (1) `mom.rst:28` の宙に浮いた導入文（Design と重複）。文を消すだけでは「Nablarchバッチアプリケーションから…行う場合」の限定が失われるため、`:30` の冒頭へ移して1文に統合するのが正しい。(2) `implementation/request_unit_test/web.rst:48`「これらのクラスは、内蔵サーバも含めてすべて同一の\ JVM\ 上で動作する。」— 表から `HttpServer`（「内蔵サーバ。…」）の行を落としたため、「これらのクラス」に内蔵サーバが含まれなくなり係り受けが崩れた。(3) `tools/testdata_converter.rst:69` の新段落が同ページ `:278` と矛盾（下の三角1）。(4) `mom.rst:22` の「スーパクラス」が、直前の文が別の継承関係を述べているため指示対象を決められない（同じ書き換えを受けた `batch.rst:17`・`mom.rst:30` は隣接しており曖昧でない） |
| 既存の体裁・声・用語との一貫性 | NG | (1) `setup/junit5_extension.rst:73` — `~` 下線の直後に空行が入る。`ja/development_tools/testing_framework/` 配下（`guide/` を除く）で下線の次行が本文のものが163件、空行のものはこの1件だけ。この空行は TODO と本文の区切りとして存在していたもので、TODO を消した以上残す理由が無い。(2) `setup/request_unit_test/web.rst:186`「実行構成(Run Configuration)」が Eclipse の実UI名と違う（下の三角2）。(3) 併記の省略記号の扱いが既存2件（`tools/request_data_tool.rst:74`「追加(Add...)」・`:78`「参照(Browse...)」）と不揃い。OK側: 1段落1行・二重空行0・行末空白0、`list-table` の列数と `:widths:` 不変、`\ ` エスケープ、`en/` 無変更、`自動テストフレームワーク` が**本文には**0件 |

### Verification Expert (fact-check)

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| 主張が出典に当たって確かめられているか | NG | (1) 本ファイル §手順2-2 の3つ目「`nablarch.test.core.http.dump` は…1.3.0・1.4.0・1.7.0・2.0.0・6u3・6-NEXT-SNAPSHOT の jar には存在しない」が再現しない。**調整役が `unzip -l` で全版を実測**したところ、全版に `nablarch/test/core/http/dump/template.xls`（15872 bytes）が存在し、消えているのは `.class` 7件だけである（1.2.0: dump配下9・class 7／他の全版: dump配下2・class 0・xls 1）。`.. important::` の結論（jetty12 が12クラスのみを提供、コンポーネント定義は非同梱）は調整役の実測と一致し倒れないが、根拠の1行が誤り。この jar は `~/.m2` にあり「作業ディレクトリの外のモジュール側リポジトリ」ではなく、検証可能だった。(2) `tools/testdata_converter.rst:69` の「テストの実行結果は変わらない」に出典が無く、出典は逆を示す（下の三角1）。(3) `setup/request_unit_test/web.rst:186` の英語名（下の三角2） |
| 網羅性（未確認の主張が残っていないか） | NG | `:69` の新段落の3文のうち、本ファイルの Method 表が拾っているのは「中間モデルに入らない」だけで、「テストの実行結果は変わらない」と、空エントリ側の主語（`dropEmptyEntries` は `nablarch.test.tool.converter.xls.XlsFormatReader` すなわち**変換ツール自身**のコードで、テスティングフレームワークではない。呼び出しは `229201f` 全体で `:162`（TableDataBlock）と `:193`（ListMapBlock）の2箇所のみ。FileDataBlock・MessageDataBlock には掛かっていない）は拾われていない。「本ファイル §気づいた点2」が `markerColumnColor` を「未確認」と正しく書いているのに、同じ厳しさが `:69` の本文には適用されていない。あわせて本ファイル §完了条件2・3 の内訳表が11件のうち10件しか説明しておらず（`implementation/deal_unit_test/mom.rst:72` が欠落）、「`:ref:` ラベルの定義と参照3件」も実際は定義1件＋参照4件 |

## 調整役が実測で裏を取った事項

すべて調整役が自分で実行・自分で開いて確認した。

| 事項 | 実測 |
|---|---|
| 完了条件4・5・6 | `RESULT: OK` / `OK: no errors` / `183 passed, 96 subtests passed in 0.72s` |
| 完了条件7 | クリーンなフルビルドを実行。`loading pickled environment... not yet created`・`building [html]: targets for 325 source files that are out of date`・`updating environment: 325 added, 0 changed, 0 removed`・末尾 `build succeeded.`・exit 0。`grep -cE 'WARNING:\|ERROR:\|SEVERE:'` → `0`。直後に `git -C <repo> checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行し、`git status --porcelain` が `?? checks/task-32.md` の1行だけであることを確認 |
| 削除9ファイル | `git ls-files ja/` に9件とも残っていない。9つのファイル名それぞれで追跡ファイルを走査し、参照は全件0。`en/` の同名ファイル16件は無傷 |
| `markerColumnColor` の矛盾 | `nablarch-testing-converter` `229201f` の `xls/XlsFormatWriter.java:258` `if (isMarkerColumn(columns.get(c)))`、同 `:543` `static final String EMPTY_BLOCK_MARKER_COLUMN = "[空]";`、同 `:556` `return columnName != null && columnName.startsWith("[") && columnName.endsWith("]");` |
| `XLS-08`（本体と変換ツールで規則の順序が違う） | 同 `xls/XlsFormatReader.java:549-560` 逐語。「本体 `PoiXlsReader#readLine` は除外前の生の行で空エントリを判定するため、マーカーカラムだけを持つ行は本体では空エントリにならず」「記法は 2 つの規則の前後関係を定めていない。「除外 → 空エントリ判定」を前提とする（ユーザー確定・2026-08-18。**解説書側へ明文化を申し送る**）。課題は `coverage/issues.md` の XLS-08 に記録している」 |
| `dropEmptyEntries` の帰属と適用範囲 | `git -C <converter> grep -n 'dropEmptyEntries' 229201f -- src/main/java` → 定義 `:566`、呼び出しは `:162` と `:193` の2箇所のみ |
| Eclipse の実UI名 | Eclipse公式ヘルプ `tasks-executionArgs.htm` 逐語 `"Run > Run Configurations..."`（**複数形＋省略記号**）。`task-add_new_jre.htm` は `"Default VM Arguments"`・`"Java > Installed JREs"` を確認。「編集」ボタンの英語名は同ヘルプに記載が無く**未確認** |
| `en/` が Eclipse の一次情報にならないこと | `en/…/02_RequestUnitTest.rst:507` は `"Settings(設定)"`、対応する `ja/…/setup/request_unit_test/web.rst:193`（本タスク未変更）は「設定(Preferences)」。同一の出典ファイルが少なくとも1語で誤っている |
| jar の実測 | 上の Verification Expert の行に記載 |
| `mapping.csv` の MOVE 6行 | `csv.DictReader` で `src_section_id` を突合し6行とも実在・`disposition=MOVE` を確認。`note` は `current-0200`・`0281`・`0295`・`0308` が「…pngの構成図のみ。」、`0182` が「class_structure.png（全体像図）と…表。」、`0165` が「自動テストフレームワークの構成図と、…表。」 |
| `design.md` の当該節 | 節見出し「### 「アーキテクチャ」は図のみとし、構成物一覧の表は置かない」と、本文「内容もすでに図と導入文のみという最小限に絞られている（直上の改訂参照）ため、本節は第1部に残し変更しない。」、および図の関係を列挙した「…Nablarch Application Framework→コンポーネント設定ファイル/環境設定ファイル（読み取る）という関係を確認した上で」を現物で確認 |
| `send_sync_base.png` の禁止語 | 調整役が画像を開いて確認。「自動テストフレームワーク」のノードが2つ（左端の起点と右端の「④要求電文のアサート／⑤応答電文の生成」）ある。`mapping/glossary.md:515` が `自動テストフレームワーク` → `テスティングフレームワーク`（無条件）と定める |
| `AbstractHttpRequestTestTemplate` を web.rst に残した根拠 | 指示書 §7-1 の「web.rst:78・88 で継承する」は誤り。`implementation/request_unit_test/web.rst:83`・`:116` はいずれも `BasicHttpRequestTestTemplate` で、`AbstractHttpRequestTestTemplate` は同ファイルで表の `:41` 以外に出現しない。`setup/request_unit_test/web.rst:229` は「アプリケーションプログラマが直接使用することはなく、テスティングフレームワークを拡張する際に用いる」と明言 |

## 是正ラウンドの4観点レビュー（2026-08-21、コミット `811d1cb`）

対象は是正指示 `ntf-doc-32-fix.md` の完了条件1〜14。完了条件11・13・14 は調整役が担当したためレビューには渡していない。**4観点とも、判定可能な完了条件（1〜10・12）はすべて OK。**4観点は独立に `_batch` 連結のバイト一致（538530 バイト）・597行・`note` 列のみの差分を確認しており、台帳の不変条件は破れていない。fail の理由はいずれも完了条件の外にある。

### QA Expert（是正ラウンド）

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| 検証の方法が目的にかみ合っているか | NG | (1) 完了条件4 が `web.rst` の1シンボルの grep のため、判断4の採否基準に照らして落ちるはずの `implementation/request_unit_test/mom.rst:91` の `TestDataConverter`（表以外の出現0件）が通過する。落とした `AbstractHttpRequestTestTemplate` と同型。(2) 指示書 §4-2 の前提「`mom.rst:143` の独自拡張用スーパクラスの一覧」が現物と違う（`:103`「使用方法 > テストクラスを作成する」節の中で、利用者が継承するクラスを指示している箇所）。(3) 完了条件6 の `:137` は指示書 §3-1 の「`:137` の直前に新設」と両立しない。(4)「判断なしで直す6件」に対応する完了条件が1つも無い |

### Design Expert（是正ラウンド）

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| 方針・構造が適切か | NG | (1) 台帳への `#32` ポインタが図の7行にしか付いていない。`design.md` の新節は「同じ理由で『主なクラスとリソース』の表からも…落とした」と書いているのに、表から落ちたクラスを内容に持つ `current-0201`・`0282`・`0296`・`0309`・`0323`・`input-0184` の6行が素通り。指示書 §3-3 の走査条件が `heading_path` の「全体像」「構成」だけだったため。(2) `design.md` §「出典と実装が食い違う場合」が求める `reviews/page-*.md` への記録が無い（`reviews/page-testdata_converter.md` は `7f5659e` から未変更）。出典 `input-0184`（`input/testdata-converter-design.md:31`「意図ある情報は無損失（マーカーカラム、空エントリ…を保持）」）に反してマーカーカラムを除去側へ動かしている |
| 体系全体の整合 | NG | (1) 空エントリの削除が、一次情報付きで決着済みの過去判断を覆している（下の「判断待ち1」）。(2) `mapping/style.md` S-12 の実測が `#32` で陳腐化 → `f8f74f2` で追記済み。(3) `:278` の既知の欠陥に追跡先が無い（`grep -n 'markerColumnColor\|EMPTY' steering.md` → 0件）。(4) `design.md` 新節が `## 2. 第1部` の内部にあるが、決定の適用範囲は第1部〜第3部 |

### Craft Expert (writing)（是正ラウンド）

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| 日本語技術文書としての明快さ・正確さ | NG | (1) `mom.rst` の同一ページ内矛盾（`9031fa6` の退行。下の「判断待ち3」）。(2) `rest.rst:41` の「``RestTestSupport``\ は、**これ**に…」の「これ」が、直前の文の主語が `RestTestSupport`・`SimpleRestTestSupport` の対であるため一意に決まらない（指示書 §4-3 の逐語文面）。(3) `web.rst:48`「これらのクラス」の指示語は依然として対象が定まらない（表に `テストデータ` 行を含むため）—— 現状でも読めるため見送り |
| 既存の体裁・声・用語との一貫性 | NG → 一部 `f8f74f2` で是正 | (1) `mom.rst:30` の行頭 `\ ` は既存6箇所と揃わない（他はすべて直後がインラインマークアップ）→ `f8f74f2` で削除。(2) 表からクラスを落とした理由（利用者が名前を書かない）が `mom.rst:141-143` の現物と矛盾（判断待ち3）。OK側: リード文は6ページ完全統一（「テストを構成する主な」0件）、`list-table` の列数・`:widths:` 不変、段落内改行0、行末空白0、`glossary.md` の揺れ表記157〜162語の独自走査でヒット0、docutils での parse エラー0 |

### Verification Expert (fact-check)（是正ラウンド）

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| 主張が出典に当たって確かめられているか | NG → 1件 `f8f74f2` で是正 | 裏が取れたもの: `about/index.rst` の `:ref:` 先（`setup/index.rst:1` にラベル実在、内容も `setup/common.rst:45`・`setup/request_unit_test/web.rst:15`・`setup/class_unit_test.rst:10` で成立）／削除画像9件が `git show --diff-filter=D --name-only 9031fa6` と完全一致／`design.md` §11.8 が `:838` に実在し引用が `:848` に逐語で存在／台帳7行の追記文が指示書と逐語一致・既存 `note` 保全／`current-0182`・`0322` の「表・tip は…に存在する」が現物で確認できる／`rest.rst:41` の説明が同ページ `:17`・`:53` と整合。NG: `design.md` の「残る3つは同節の本文が既に述べている」が過剰主張（テスティングフレームワーク→NAF の側が `about/index.rst` の本文に無い）→ `f8f74f2` で書き分けに是正 |
| 網羅性 | NG | `tools/testdata_converter.rst:39` に残る `行末の空セル` が未確認の主張。`implementation/testdata_notation.rst:1545` が「\ Excel\ 形式のみ。\ YAML\ 形式では ``rows:``\ の各要素をそのまま読み込む」と明記しており、指示書 §1-1 が `空エントリ` を落とした理由（形式を問わない中間モデルの表に非対称な扱いを無条件に書けない）がそのまま当てはまる。同行の `データブロックの外側にある空行` は `ja/` 配下に出典が無い（`grep` で `:39` の1件のみ）。`コメント`（`testdata_notation.rst:1512`）と `マーカーカラム`（同 `:1549`、但し書き無し）は対称で問題なし |

## 調整役が実測で裏を取った事項（是正ラウンド）

すべて調整役が自分で実行・自分で確認した。

| 事項 | 実測 |
|---|---|
| 完了条件1〜10・12 | 4観点と独立に全件実行して一致。`_batch` 30ファイル昇順連結が `mapping.csv` とバイト一致、`csv.DictReader` 597行、各 `_batch` の行数は編集前と同一（20/22/20/20/20/20/20）、7行とも `disposition=MOVE` |
| 完了条件11 | クリーンなフルビルド。`loading pickled environment... not yet created`・`building [html]: targets for 325 source files that are out of date`・`updating environment: 325 added, 0 changed, 0 removed`・末尾 `build succeeded.`。913行のログに `Exception`・`Traceback` 0件。`grep -cE 'WARNING:\|ERROR:\|SEVERE:'` → `0`。直後に `git -C <repo> checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行し、`git status --porcelain` が `?? checks/task-32.md` の1行だけであることを確認。**ただし当日の `docker build` は `pip install -r requirements.txt` が exit 1 で失敗し、7日前にビルド済みの既存イメージ `nablarch-document-build`（`a974e0c8ac60`）でビルドした。**イメージ自体は当日作り直せていない |
| jar（是正指示 §5 の再実測） | `unzip -l` で7版を実測。1.2.0 は `nablarch/test/core/http/dump/` に `template.xls`（15872）＋`.class` 7件。1.3.0・1.4.0・1.7.0・2.0.0・6u3・6-NEXT-SNAPSHOT はいずれも `template.xls`（15872）のみ。2.2.0 は jar 自体が無い。消えたのは `.class` だけで `.. important::` の結論は倒れない |
| 空エントリの3コミットの遷移 | `git show <commit>:<path>` で確認。`c650039`（`#30`まで）保持側＝「マーカーカラム、データブロックの内側にある空エントリ、空欄のレコード種別」／`69334be`（`#31`）保持側から空エントリが消失／`b3e76fc`（`#32`）マーカーカラムを除去側へ移し空エントリを除去側へ追加／`811d1cb`（是正）除去側から空エントリを削除 |
| 保持側にあった根拠 | `reviews/page-testdata_converter.md:116` 逐語: 「「空エントリ」と「完全な空行」が同一物に見えるのに保持と除去に分かれている｜クラフト｜「データブロックの内側にある空エントリ」「データブロックの外側にある空行」に書き分け（`model/ListMapBlock.java:12`「空マッピング由来の空行も空リストとして保持」による）」 |
| `mom.rst` の退行 | `git show 9031fa6 -- <mom.rst>` で確認。`:30` が「テストクラスは、\ ``StandaloneTestSupportTemplate``\ を継承した\ :java:extdoc:`BatchRequestTestSupport`\ を継承して作成する。」から `StandaloneTestSupportTemplate` を失い、`:141-143` の箇条書きとの接続が切れた |
| `mom.rst:91` の `TestDataConverter` | `grep -n 'TestDataConverter' mom.rst` → `91:` の1件のみ（表のセル） |
| `mom.rst:141-143` の所在 | `:103`「使用方法 > テストクラスを作成する」節の中。`:141`「テストクラスは、テスト対象の処理方式に合わせて次のどちらかのスーパクラスを継承する。」独自拡張用の一覧ではない |
| 台帳の適用漏れ6行 | `csv.DictReader` で `note` を確認。`current-0201`（`AbstractHttpReqestTestSupport,BasicHttpReqestTestSupport`・`HttpServer`）・`0282`（`StandaloneTestSupportTemplate`・`TestShot`）・`0296`（同）・`0309`（`HttpServer`）・`0323`（`StandaloneTestSupportTemplate`・`AbstractHttpRequestTestTemplate`）・`input-0184`（「マーカーカラム・空エントリ・空欄レコード種別は保持」）。いずれも `#32` のポインタ無し |
| `style.md` S-12 の陳腐化 | `git grep -h '^\.\. image::' <commit> -- <dir>` で `a380740^`=34・`a380740`=30・`d8d6114`=30・`0806ea5`=30・`9031fa6`=27・`HEAD`=27。S-12 の「33件」はどの時点でも再現しない。`grep -rn 'NTF-SRC-02' ja/` → 0件 |
| `f8f74f2` の是正3件 | `design.md` の書き分け・`mom.rst:30` の行頭 `\ ` 削除・`style.md` S-12 への 2026-08-21 追記。過去の実測ブロックは無改変。`verify_glossary.py` `RESULT: OK`／`verify_mapping.py` `OK: no errors`／`pytest` `183 passed, 96 subtests passed` |

## user 判断待ち6件（2026-08-21、是正ラウンド後）

**回答なしに `ja/`・`mapping/`・`reviews/` を触らないこと。**根拠はすべて上の「調整役が実測で裏を取った事項（是正ラウンド）」にある。

1. **空エントリの帰属**（最重要）。保持側 →（`#31`で消失）→ 除去側（`#32`）→ 完全消滅（是正）と動いた。是正指示 §1 の根拠（`XlsFormatReader#dropEmptyEntries` が Excel 起点のみ）は「除去側に無条件に書けない」ことを示すが、「保持側にも書けない」ことは示していない。保持側の根拠 `model/ListMapBlock.java:12`（保持）は是正指示が触れていない。副作用として `:39` に「データブロック**の外側にある**空行」だけが残り、対語が消えて限定の意味が読者に伝わらない。**調整役の推奨: `ListMapBlock.java:12` を再確認したうえで保持側へ戻す**
2. **`:39` の `行末の空セル`**。`testdata_notation.rst:1545` が Excel 限定と明記。判断1と同型。**推奨: 落とす**（§1-1 の `変更後` は逐語指定だったため字面を越える）
3. **`mom.rst:140-143` の継承クラス**。3観点が独立に指摘。`web.rst:73`（web は `BasicHttpRequestTestTemplate`）とも `setup/request_unit_test/web.rst:229`（`AbstractHttpRequestTestTemplate` は直接使用しない）とも矛盾。**推奨: `#33` へ送る**（正しい継承関係の確定にモジュール側の一次情報が要る）
4. **表の採否基準の適用漏れ**。(a) `mom.rst:91` の `TestDataConverter`（**推奨: 落とす**）、(b) 台帳6行への `#32` ポインタ（**推奨: 図7行と同じ形で足す**）
5. **`design.md` §「出典と実装が食い違う場合」が求める `reviews/page-testdata_converter.md` への記録**。**推奨: 判断1の結論が出てから1回で書く**
6. **`:278` の追跡先**。`#32` を閉じると台帳から消える。**推奨: `#33` の3項目目として足す**

**採用しなかった指摘**: (a) `:69` に Excel 限定で空エントリの挙動を書き戻す案（クラフト）—— 判断1で「両方から落とす」と明示的に決まった件の蒸し返し。判断1を見直す場合は連動する。(b) 完了条件6 の `:137` —— 指示書 §3-1 が「`:137` の直前に新設せよ」と定めている以上、実行後に `:137` が新節になるのは必然。実装の欠陥ではない。(c) `web.rst:48`「これらのクラス」の指示語 —— 指示どおり直した行への追加の詰めで、現状でも読める

## Overall Verdict

- Self-check: OK（是正の完了条件1〜10・12・13 は実装担当が実行して OK。11・14 は調整役が実施。完了条件6 の `:137` は指示書が新節挿入前の行番号を書いたもので、現物は新節 `:137`・差し替えた既存節 `:149`。当初の完了条件2・3 は指示書の検査コマンドの文字列そのままでは満たせない。判定の本体はいずれも満たしている）
- QA: NG（是正ラウンド。判定可能な完了条件は全件 OK。fail の理由は完了条件の外 —— 上の「user 判断待ち6件」の1・3・4）
- Design expert: NG（是正ラウンド。同上 —— 判断待ち1・4・5・6）
- Craft expert: NG（是正ラウンド。うち `mom.rst:30` の行頭 `\ ` は `f8f74f2` で是正済み。残りは判断待ち3）
- Verification expert: NG（是正ラウンド。うち `design.md` の過剰主張は `f8f74f2` で是正済み。残りは判断待ち2）
- Ready to check off: No。**user 判断待ち6件の回答待ち。**判断が要らない3件（`design.md` の過剰主張・`mom.rst:30` の行頭 `\ `・`style.md` S-12 の実測の陳腐化）は `f8f74f2` で処置済み。当初ラウンドの4観点の判定は上の `## QA Expert Review`・`## Expert Reviews` に、是正ラウンドの判定は `## 是正ラウンドの4観点レビュー` にある

---

## 是正2（user 判断待ち6件の回答。指示書 `ntf-doc-32-fix2.md`）

実行日: 2026-08-21。開始コミット `1355984`。ブランチ `ntf-yaml-support`。

`ja/` の `file:line` は是正2 適用後の作業ツリーを指す。`.rn/` 内の文書どうしの参照は節見出しで指す。モジュール側リポジトリは作業ディレクトリの外にあるため開いていない。モジュール側の逐語はすべて指示書 `ntf-doc-32-fix2.md` が引用したものであり、出典として指示書を明示する。

### Completion Criteria（是正2）

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| 1. `grep -n '行末の空セル' ja/development_tools/testing_framework/tools/testdata_converter.rst` が `:39` を含まず、前提事項の新段落1件のみ | OK | 実行結果は1件のみ: `71:行末の空セルも、\ Excel\ 形式から読み込むときだけ取り除かれる。…` （`:39` は「保持しない。コメント、マーカーカラム、データブロックの外側にある空行は除去する」に変わり、`行末の空セル` を含まない） | | |
| 2. `grep -n '空エントリ' ja/development_tools/testing_framework/tools/testdata_converter.rst` が0件 | OK | `grep -c '空エントリ' …` → `0` | | |
| 3. `grep -c 'StandaloneTestSupportTemplate\|AbstractHttpRequestTestTemplate' ja/…/implementation/request_unit_test/mom.rst` が0 | OK | 実行結果 `0`。2行の箇条書き（差し替え後は `:130`・`:131`）を `BatchRequestTestSupport`・`BasicHttpRequestTestTemplate` へ差し替えた。指示書の `:142-143` は文面で照合した（`f8f74f2` 時点の実物では `:141-142`） | | |
| 4. §4-2 の10行が6ページの表から消えており、`grep -c 'TestDataConverter' mom.rst` が1、`grep -c 'RequestTestingMessagingProvider' mom.rst` が3、`grep -c 'TestCaseInfo' web.rst` が削除前と同じ。`component.rst`・`entity.rst` に差分が無い | OK | 10行の削除は削除スクリプトが1件ずつ `  * - ``クラス名``` の完全一致を1件だけ検出して3行ずつ削除（実際に削除した行番号: web `:35`・`:35`、rest `:37`、batch `:48`・`:48`・`:48`、mom `:76`・`:76`・`:76`・`:79`。指示書 §4-2 の行番号と、先行削除ぶんのずれを込みで一致）。`grep -cE '^  \* - ``(DbAccessTestSupport\|HttpRequestTestSupport\|MainForRequestTesting\|FileSupport\|MQSupport\|MessageSender)``$'` は web/rest/batch/mom すべて `0`。`grep -c 'TestDataConverter' mom.rst` → `1`、`grep -c 'RequestTestingMessagingProvider' mom.rst` → `3`、`grep -c 'TestCaseInfo' web.rst` → `13`、`git show HEAD:…/web.rst \| grep -c 'TestCaseInfo'` → `13`（同数）。`git diff --stat HEAD -- …/class_unit_test/component.rst …/entity.rst` → 出力0行 | | |
| 5. 各ページの `list-table` の行が3行構成を保ち、docutils の parse エラーが0 | OK | 6ページを独自スクリプトで走査。`:header-rows: 1`・`:widths: 30,45,25` はいずれも不変、データ行はすべて `* - ` ＋ `- ` 2行の3セル構成（web 6行／rest 5行／batch 4行／mom 7行／component 5行／entity 5行、いずれもヘッダ行を含む。表が空になったページは無い）。parse エラーは Sphinx フルビルドで確認 —— `grep -cE 'WARNING:\|ERROR:\|SEVERE:' build.log` → `0`、末尾 `build succeeded.` | | |
| 6. `_batch/*.csv` を昇順に連結（先頭のみヘッダ込み）した結果が `mapping/mapping.csv` とバイト一致し、`csv.DictReader` が597行。6行の `note` に `【#32` があり、`disposition` は編集前と同一 | OK | 連結規則を先に検証: HEAD の `_batch/*.csv` 30件を昇順連結した結果が HEAD の `mapping.csv` と**バイト一致**（`True`）。編集後も同じ手順で `mapping.csv` を作り直した。`csv.DictReader` → `597`。**`_batch/batch-25.csv` だけ改行が LF、他29件は CRLF** のため、`\r\n` での機械的分割は使えず、各ファイルの生テキストから先頭行だけを落として連結した。各 `_batch` の `csv.DictReader` 行数は編集前後で全30件一致。6行の `note` はいずれも `【#32` を含み（`mapping.csv` 全体では図7行と合わせて13行）、`disposition` は `current-0201`=`MERGE`、`current-0282`・`0296`・`0309`・`0323`・`input-0184`=`MOVE` で編集前と同一。追記後の `note` セルは6行とも `"` で囲んだ | | |
| 7. `design.md:139` の節に判定基準の2項目と適用範囲（6ページ）が書かれている | OK | `design.md` §「利用側ページに内部構造の構成図を置かない」の第1段落（`:139`）の直後に段落を新設。(1) 利用者が作成する成果物は載せる、(2) 利用者が名前を書くクラスだけ載せる、の2項目と、落とす対象・落としたクラスの役割の残し先・適用範囲（表を持つ6ページ全部、2026-08-21）を書いた。既存節の文体（太字リード＋地の文1段落）に揃えた | | |
| 8. `reviews/page-testdata_converter.md` に §5-1 の3件が記録されている | OK | 既存の `## 出典から変えた点` の表（4列: 箇所／出典の記述／ページの記述／変えた理由）に3行を追記（マーカーカラムの保持・空エントリの保持・行末の空セルの除去）。実装のファイル名・行番号と参照コミット `nablarch-testing-converter` `e977824` を、表直後の1段落に明記した | | |
| 9. `steering.md` の `#33` に (c) が足され、見出しが改まっている | OK | 見出しは `### #33: 記法の適用順序の明文化、markerColumnColor の説明不足、残置図の禁止語点検`（指示書 §6 の逐語）。`**Purpose**` の「2件」を「3件」に直し (c) を追加。背景の箇条書きに (c) を3項目目として追加した | | |
| 10. `python3 mapping/tools/verify_glossary.py` が `RESULT: OK` | OK | 末尾 `RESULT: OK`、`exit=0` | | |
| 11. `python3 mapping/tools/verify_mapping.py` が `OK: no errors` | OK | 末尾 `OK: no errors`、`exit=0` | | |
| 12. `python3 -m pytest mapping/tools -q` が `183 passed, 96 subtests passed` | OK | `183 passed, 96 subtests passed in 0.59s` | | |
| 13. Docker フルビルドで `grep -cE 'WARNING:\|ERROR:\|SEVERE:' build.log` が 0。直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行する。**`docker build` から作り直すこと。** | **NG（`docker build` が失敗。ビルド自体は既存イメージで実行し警告0）** | `docker build -t nablarch-document-build .` は **exit 1**。下の「`docker build` の失敗ログ」に逐語。やむを得ず既存イメージ `nablarch-document-build`（`a974e0c8ac60`、7日前）で `_build` を消してからフルビルドした結果は、`loading pickled environment... not yet created`／`building [html]: targets for 325 source files that are out of date`／末尾 `build succeeded.`、913行のログに `Exception\|Traceback` 0件、`grep -cE 'WARNING:\|ERROR:\|SEVERE:' build.log` → `0`。直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行し、`build.log` は作業ツリーから退避して削除。`git status --porcelain` に `build.log`・`sphinx.mo` は残っていない。**イメージ自体は2回続けて未検証であり、これを「成功」とは報告しない。`#33` へ (d) として送った** | | |
| 14. 禁止事項（`ja/conf.py`・`mapping/glossary.md` §5.15・`mapping.csv` 直接編集・`en/`・`locales/` の `.gitignore` 追加）に触れていない | OK | `git status --porcelain -- ja/conf.py .rn/20260724-ntf-yaml-support/mapping/glossary.md en/ locales/` → 0行。`mapping.csv` は `_batch/*.csv` を直してから連結し直して生成（直接編集していない）。`.gitignore` は未変更 | | |
| 15. `checks/task-32.md` に §4-2 の「落とさない行」の判定根拠と、§1・§3 で推奨を採らなかった理由が記録されている | OK | 本節の下記4小節（「§1 で推奨を採らなかった理由」「§3 で `#33` へ送らなかった理由と jar 実測の逐語」「§4-2 の『落とさない行』4件の判定根拠」「§4-2 で落とした10クラスの役割の残存確認」） | | |

### §1 で推奨（保持側へ戻す）を採らなかった理由

是正ラウンドの調整役推奨は「`ListMapBlock.java:12` を再確認したうえで保持側へ戻す」だったが、user はこれを採らなかった。理由は、根拠 `model/ListMapBlock.java:12`（「空マッピング由来の空行も空リストとして保持」）が **YAML 経路の話**であり、Excel 経路には当てはまらないことである。Excel 経路で読み飛ばしを実行するのは変換ツールではなく NTF 本体であり、変換ツールに判断の余地が無い。`nablarch-testing-converter` `e977824` の `.rn/ntf-test-data-converter/coverage/issues.md:299-300` 逐語（指示書 `ntf-doc-32-fix2.md` §1 が引用したもの）:

> 読み飛ばしを実行するのも本体 `PoiXlsReader#isBlankLine`（L140-147）であり、
> converter に判断の余地は無い。

したがって Excel 起点では「無損失で保持する」が成り立たず、保持側にも書けない。中間モデルの表は形式を問わない記述であるため、片方の経路でしか成り立たない扱いをどちらの欄にも無条件には書けない。`tools/testdata_converter.rst:39` は現状（空エントリの記載なし）のままとした。

「データブロックの外側にある」も残した。対語が消えて限定の意味が伝わらないという是正ラウンドの指摘は成り立つが、この書き分けは `reviews/page-testdata_converter.md` の「是正した指摘」表が「「空エントリ」と「完全な空行」が同一物に見えるのに保持と除去に分かれている」を是正して入れたものであり、「完全な空行」へ戻すと同じ曖昧さが戻る。

### §3 で `#33` へ送らなかった理由と jar 実測の逐語

是正ラウンドの調整役推奨は「`#33` へ送る（正しい継承関係の確定にモジュール側の一次情報が要る）」だったが、user はこれを採らなかった。理由は、モジュール側の一次情報が jar から確定できたことである。`~/.m2/repository/com/nablarch/framework/nablarch-testing/2.0.0/nablarch-testing-2.0.0.jar` を展開して `javap` で実測（2026-08-21、user 実施）。逐語（指示書 `ntf-doc-32-fix2.md` §3 が引用したもの）:

```
public abstract class nablarch.test.core.http.BasicHttpRequestTestTemplate
    extends nablarch.test.core.http.AbstractHttpRequestTestTemplate<nablarch.test.core.http.TestCaseInfo>
public class nablarch.test.core.batch.BatchRequestTestSupport
    extends nablarch.test.core.standalone.StandaloneTestSupportTemplate
```

`StandaloneTestSupportTemplate` の直接のサブクラスは `BatchRequestTestSupport` と `MessagingRequestTestSupport` の2つ、`AbstractHttpRequestTestTemplate` の直接のサブクラスは `BasicHttpRequestTestTemplate` の1つだけである（同 jar の全クラスを `javap` で走査）。

差し替えの妥当性は、作業ディレクトリ内でも裏が取れる。`mom.rst:128`（是正2 適用後。指示書が挙げる `:140` は表から12行を削る前の行番号）は「テスト対象の処理方式に合わせて次のどちらかのスーパクラスを継承する。」と述べ、ウェブとバッチの2ページを `:ref:` で参照している。参照先の2ページが挙げるクラスは `batch.rst:17`「テストクラスは、\ ``BatchRequestTestSupport``\ を継承して作成する。」と `web.rst` の `BasicHttpRequestTestTemplate`（表 `:35`、本文 `:67`「\ :java:extdoc:`BasicHttpRequestTestTemplate <…>`\ を継承する。」・`:77`「`public class UserSearchActionRequestTest extends BasicHttpRequestTestTemplate {`」）であり、差し替え後の2行（`mom.rst:130`・`:131`）はこれに揃う。

### §4-2 の「落とさない行」4件の判定根拠

いずれも「利用者がテストコード・テストデータ・コンポーネント設定のいずれかに名前を書く」に該当するため残した。4件とも現物を開いて確認した。

| 残した行 | 判定根拠（自分で開いて確認した文面） |
|---|---|
| `mom.rst` の `TestDataConverter` | 利用者（アーキテクト）が実装し、コンポーネント設定にクラス名を書く。`setup/request_unit_test/mom.rst:72`「拡張するには\ :java:extdoc:`TestDataConverter <nablarch.test.core.file.TestDataConverter>`\ を実装する。XMLやJSONといったデータ形式ごとに、必要に応じてアーキテクトが用意する。」、同 `:91`「`class="com.example.test.core.file.FormUrlEncodedTestDataConverter"/>`」。`AbstractHttpRequestTestTemplate` と同型ではない（後者は `setup/request_unit_test/web.rst:229`「アプリケーションプログラマが直接使用することはなく、テスティングフレームワークを拡張する際に用いる。」と一次情報が直接使用を否定している） |
| `mom.rst` の `RequestTestingMessagingProvider` | コンポーネント設定に書く。`setup/request_unit_test/mom.rst:44`「`class="nablarch.test.core.messaging.RequestTestingMessagingProvider"/>`」 |
| `web.rst` の `TestCaseInfo` | テストコードに書く。`web.rst:199`・`:200` のメソッドシグネチャ `void beforeExecute(TestCaseInfo testCaseInfo, ExecutionContext context)`／`void afterExecute(TestCaseInfo testCaseInfo, ExecutionContext context)` と、`:211`・`:218` のサンプルコード `public void beforeExecute(TestCaseInfo testCaseInfo,`／`public void afterExecute(TestCaseInfo testCaseInfo,`（指示書 §4-2 は `:217`・`:224` と書いているが、これは同ページから6行を削る前の行番号。削除後は `:211`・`:218`） |
| `component.rst`・`entity.rst`（変更なし） | 表はどちらも5行（ヘッダ1＋データ4）。`DbAccessTestSupport` は `component.rst:69`「:java:extdoc:`DbAccessTestSupport <nablarch.test.core.db.DbAccessTestSupport>`\ を継承する。」・`:81`「`public class UserComponentTest extends DbAccessTestSupport {`」、`EntityTestSupport` は `entity.rst:86`「:java:extdoc:`EntityTestSupport <nablarch.test.core.db.EntityTestSupport>`\ を継承する。」・`:95`「`public class UserRegistrationFormTest extends EntityTestSupport {`」で、いずれも利用者がテストコードに名前を書いて継承するクラスである。指示書 §4-2 は `entity.rst:35` を挙げているが、`:35` は表のセルそのものであり、継承の根拠は `:15`・`:86`・`:95` にある |

### §4-2 で落とした10クラスの役割が本文に残っていることの確認

10件それぞれについて、指示書 §4-2 の「根拠」欄が指す本文を実際に開いて残存を確認した。行番号は削除後の作業ツリーのもの。

| ページ | 落としたクラス | 役割が残っている本文（確認した文面） |
|---|---|---|
| `web.rst` | `DbAccessTestSupport` | `:102` の `tip`「データベースを使用するテストに必要な機能は、\ ``HttpRequestTestSupport``\ が\ :java:extdoc:`DbAccessTestSupport <nablarch.test.core.db.DbAccessTestSupport>`\ へ処理を委譲することで実現している。このため、準備データの投入やテーブルの検証は\ :ref:`コンポーネント単体テスト <component_unit_test>`\ と同じように行える。」 |
| `web.rst` | `HttpRequestTestSupport` | 同上（同じ `tip` が委譲元として `HttpRequestTestSupport` を挙げている）。内蔵サーバの起動という役割は `:10`「テスティングフレームワークが起動する内蔵サーバにリクエストを送信し」と `:330`「内蔵サーバの起動とリクエストの送信は、スーパクラスが行う。」に残る |
| `rest.rst` | `DbAccessTestSupport` | `:93`「データベース関連機能は、\ ``RestTestSupport``\ から\ ``DbAccessTestSupport``\ に処理を委譲することで実現している。\ ``DbAccessTestSupport``\ の詳細は\ :ref:`コンポーネント単体テスト <component_unit_test>`\ を参照。」 |
| `batch.rst` | `MainForRequestTesting` | `:171`「メインクラスには、テスト用の\ ``MainForRequestTesting``\ を使用する。このクラスは、テスト用のコンポーネント設定ファイルからシステムリポジトリを初期化し、テスト対象の実行後に元のリポジトリへ戻す。」（削除した表セルと同じ説明が本文にある） |
| `batch.rst` | `DbAccessTestSupport` | `:17`「準備データの投入とテスト結果の確認は、テーブルについては\ ``DbAccessTestSupport``\ が、ファイルについては\ ``FileSupport``\ が行う。」 |
| `batch.rst` | `FileSupport` | 同上 `:17` に加え、表の直後の `:49`「``FileSupport``\ が提供するファイルの操作は、ファイルダウンロードのテストなど\ Nablarch\ バッチアプリケーション以外のテストでも必要になる。このため、独立したクラスとして提供されている。」 |
| `mom.rst` | `MainForRequestTesting` | `:178`「メインクラスには、テスト用の\ ``MainForRequestTesting``\ を使用する。このクラスは、テスト用のコンポーネント設定ファイルからシステムリポジトリを初期化し、テスト対象の実行後に元のリポジトリへ戻す。」 |
| `mom.rst` | `DbAccessTestSupport` | `:17`「準備データの投入とテスト結果の確認は、データベースについては\ ``DbAccessTestSupport``\ が、キューについては\ ``MQSupport``\ が行う。」 |
| `mom.rst` | `MQSupport` | 同上 `:17` |
| `mom.rst` | `MessageSender` | `:30`「テスト対象のアプリケーションが\ ``MessageSender``\ を使って同期応答メッセージ送信を行う。\ ``MessageSender``\ が生成した要求電文は\ ``RequestTestingMessagingProvider``\ が受け取り、…」 |

削除箇所の前後は通しで読み直した。壊れは無い。

- `web.rst:42`「これらのクラスと内蔵サーバは、すべて同一の\ JVM\ 上で動作する。」—— 「これらのクラス」は直前の表を指し、表は空になっていない（データ行5件）。「内蔵サーバ」は `:10` で既に導入済みであるため、`HttpRequestTestSupport` の行が消えても指示対象は失われない。なお「これらのクラス」に表の `テストデータ` 行が含まれてしまう点は `#32` 以前からの既存事象であり、是正ラウンドで「現状でも読める」として見送られたもの。是正2 でも触っていない。
- `batch.rst:49` の `FileSupport` 段落 —— 表の直後に残るが、`FileSupport` は `:17` で導入済みであり、指示書 §4-2 自身がこの段落（旧 `:58`）を「役割が残る場所」として指定している。段落は変更していない。
- `mom.rst`・`rest.rst` —— 表の直後は `使用方法` 見出しであり、削除の影響を受ける地の文は無い。

### 指示書と実物が食い違った点（是正2 で実測して確かめたもの）

指示書の記述をそのまま使わず、実物を開いて確かめた結果、次の3点で行番号が食い違った。いずれも**文面は一致した**ため、文面で照合して作業した。

| 指示書の記述 | 実物 | 扱い |
|---|---|---|
| §5-1「出典 `input/testdata-converter-design.md:7` 逐語: - 意図ある情報は無損失（…）」 | 実物は `:31`。`:32` が「無意味な情報は持たない（コメント、完全な空行、行末の空セルを除去）」。`:7` は「本体の読み込み機構は [ntf-testdata-loading.md] を参照。」 | `reviews/` には実測どおり `:31`・`:32` と書いた。逐語は一致 |
| §5-1「（出典 `:8`）行末の空セルを除去」 | 同上（実物は `:32`） | 同上 |
| §4-2「`web.rst:217`・`:224` のメソッドシグネチャ」 | 削除後は `:211`・`:218`（同ページから6行削ったぶんのずれ）。文面は一致 | 上の「落とさない行」表に実測の行番号で記録 |

あわせて、`current-0201` の `note` に書いた「落としたクラス名」について1点申し送る。指示書 §5-2 は「`current-0201` は `#32`（`9031fa6`）で落とした `AbstractHttpRequestTestTemplate` も含めて書く」としており、そのとおりに書いた。ただし `git show 9031fa6 -- …/web.rst` を実測したところ、`9031fa6` が `web.rst` の表から落としたのは `HttpServer`（行ごと）と、`AbstractHttpRequestTestTemplate`（`` `AbstractHttpRequestTestTemplate`・`BasicHttpRequestTestTemplate` `` という1セルからの片方）の2つである。`HttpServer` は `current-0201` の `note` の内容にも入っているが、指示書が列挙を指定していないため書き足していない。同様に `9031fa6` は `mom.rst` の表から `StandaloneTestSupportTemplate`・`AbstractHttpRequestTestTemplate`・`TestShot` を落としており、これらは `current-0296`・`current-0323` の `note` の内容に含まれる。追記の要否は user 判断。

### `docker build` の失敗ログ（完了条件13）

`docker build -t nablarch-document-build .` → **exit 1**。失敗箇所は `Dockerfile:19`。逐語（末尾抜粋）:

```
#10 10.85 Could not fetch URL https://pypi.org/simple/setuptools/: There was a problem confirming the ssl certificate: HTTPSConnectionPool(host='pypi.org', port=443): Max retries exceeded with url: /simple/setuptools/ (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1017)'))) - skipping
#10 10.86 ERROR: Could not find a version that satisfies the requirement setuptools==57.5.0 (from versions: none)
#10 10.86 ERROR: No matching distribution found for setuptools==57.5.0
#10 11.11 Could not fetch URL https://pypi.org/simple/pip/: There was a problem confirming the ssl certificate: HTTPSConnectionPool(host='pypi.org', port=443): Max retries exceeded with url: /simple/pip/ (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1017)'))) - skipping
#10 ERROR: process "/bin/sh -c pip install --no-cache-dir setuptools==57.5.0 wheel     && pip install --no-cache-dir --no-build-isolation -r requirements.txt" did not complete successfully: exit code: 1
------
Dockerfile:19
--------------------
  18 |     # Python はツールチェーンを更新しない限り 3.10 系が上限である。
  19 | >>> RUN pip install --no-cache-dir setuptools==57.5.0 wheel \
  20 | >>>     && pip install --no-cache-dir --no-build-isolation -r requirements.txt
  21 |
--------------------
ERROR: failed to build: failed to solve: process "/bin/sh -c pip install --no-cache-dir setuptools==57.5.0 wheel     && pip install --no-cache-dir --no-build-isolation -r requirements.txt" did not complete successfully: exit code: 1
```

原因は前回（`pip install` の失敗としか記録されていなかったもの）と同じ層にあり、実測で特定できた。社内 TLS 傍受の自己署名 CA をコンテナ内の `pip` が検証できない。ホスト側には CA が `/usr/local/share/ca-certificates/ca.crt` として置かれ、`SSL_CERT_FILE`・`UV_CA_BUNDLE`・`NODE_EXTRA_CA_CERTS` がこれを指しているが、`Dockerfile` はこの CA をイメージへ入れていない。`Dockerfile` は `#32` の作業範囲外のため触っていない。

**`#33` へ送った**（`steering.md` の `#33` に `(d)` として追加。見出しは指示書 §6 が逐語で指定した3項目のままとし、`(d)` は環境課題として本文にのみ置いた）。

フルビルドは既存イメージ `nablarch-document-build`（`a974e0c8ac60`、7日前）で実行した。**イメージ自体は2回続けて未検証であり、これを「成功」とは報告しない。**

### Method の適用記録（すべて自分で実行して確かめた）

- **行番号ではなく文面で照合した。** `sed -n` で編集前の実物を開き、指示書の「変更前」と一致することを確認してから直した。表の10行の削除は、`  * - ``クラス名``` の完全一致がファイル内で1件だけであることを毎回 assert し、続く `    - ` 行が2行（＝3行構成）であることも assert したうえで削除した。削除ごとに以降の行番号がずれる点は、文面一致で吸収した。
- **10件の本文残存確認**は上の表のとおり、10件それぞれ `sed -n`／`grep -n` で本文を開いて文面を確認した。
- **削除箇所の前後を通しで読み直した**（上の3点）。
- **モジュール側リポジトリは開いていない。** 逐語はすべて指示書 `ntf-doc-32-fix2.md` からの引用であり、その旨を出典として明記した。
- **CSV は `csv.DictReader` でカウントした**（`wc -l` は使っていない）。連結規則は HEAD の `_batch` と HEAD の `mapping.csv` でバイト一致を先に検証してから適用した。
- **`mapping/tools/build_mapping.sh` は使っていない。** 実装を読んだところ、このスクリプトが作るのは `sections-current.csv`・`sections-input.csv` であって `mapping.csv` ではない（`OUT_CURRENT`・`OUT_INPUT` の2つだけを出力する）。`mapping.csv` の生成は含まれていない。

## Overall Verdict（是正2）

- Self-check: OK（完了条件1〜12・14・15 は実行して OK。13 は **NG** —— `docker build` が社内 TLS 傍受の自己署名 CA により失敗し、既存イメージでフルビルドした。ビルドそのものは警告0・`build succeeded.` だが、イメージは未検証。`#33` へ (d) として送った。16 は調整役が実施）

---

## レビュー指摘の是正（2026-08-21、コミット `5c2c26f` への4観点レビューで有効と判定された9件）

### V1 `design.md` の部番号

「第2部」を「第3部」に直し、6ページのパスを本文に書いて別ファイル（`setup/request_unit_test/{web,rest,batch,mom}.rst`）と読み違えられないようにした。実測: `grep -rn '主なクラスとリソース' ja/development_tools/testing_framework/ --include=*.rst` のヒットは6件で、すべて `implementation/` 配下（`implementation/request_unit_test/{web,rest,batch,mom}.rst`・`implementation/class_unit_test/{component,entity}.rst`）。`design.md` §1 の構成図（`:18`）は「テストの実装方法　第3部・アプリ開発者向け」。`mapping.csv` を `csv.DictReader` で読み、この6ページに対応する `dest_page` 6種の `dest_part` はいずれも `第3部 テストの実装方法` の1種類だけだった。「リクエスト単体テスト4ページとクラス単体テスト2ページ」という数え方は上のヒット6件と一致するため、そのまま残した。

### V2 「6ページ全部へ適用した」の過剰主張

`design.md` の該当文を「既存行へ (2) の判定を当て、該当する10行を落とした。当てたのは (2) の落とす側だけであり、(1) の側は既存の記載を変えていない。表に行を足していないため、(1) に該当する成果物が表に無いページはそのままである」と書き直した。実測: `grep -c '^  \* - テスト対象クラス' <6ページ>` → web 1・rest 1・batch 0・mom 0・component 1・entity 1。batch・mom の表にテスト対象クラスの行が無いことを確認したうえで、行は足していない（是正2 指示書 §4-2「表の他の行・列数・`:widths:` は変えない」に従う）。

### V3 `web.rst` から消えた `HttpRequestTestSupport` の役割

`:102` の `.. tip::` の文に修飾を足し、「内蔵サーバの起動やリクエスト単体テストで必要となるアサートの機能を提供する\ ``HttpRequestTestSupport``\ が…委譲することで実現している」とした。役割の文言は、落とした行の逐語（`git show 5c2c26f -- .../web.rst` の削除行「内蔵サーバの起動や、リクエスト単体テストで必要となるアサートの機能を提供する」）から採った。ページの他の段落と同じく1段落1行で書いた。

### V4 `batch.rst` の宙に浮いた段落（選んだ方針と理由）

**方針: 段落を残したまま、`FileSupport` を名指ししているリード文の直後（現 `:19`）へ移し、「独立したクラス」を「``BatchRequestTestSupport``\ とは別のクラス」に書き換えた。落とさなかった。** 理由: この段落の出典は `mapping.csv` の `current-0287`（`csv.DictReader` で読み、`src_file` が `06_TestFWGuide/RequestUnitTest_batch.rst`・`src_body_start=123`・`src_body_end=133`・`dest_page` が「リクエスト単体テスト（Nablarchバッチアプリケーション）」・`disposition=MOVE`）であり、`note` が「ファイル操作はバッチ処理以外（例：ファイルダウンロード）でも必要なため独立したクラスとして提供している旨」を移送対象として明示している。今回の是正では `mapping.csv` を変更しないため、`MOVE` の割当が求める内容を落とすことはできないと判断した。「独立した」が表の他行との対比を含意していた点だけを、比較対象を明示する語に置き換えて解消した。

### V5〜V8 `reviews/page-testdata_converter.md`

- **V5**: 追記3行の出典表記 `design.md:31`・`design.md:32` を `input/testdata-converter-design.md:31`・`:32` に直した。実測: `sed -n '31,32p' input/testdata-converter-design.md` → `- 意図ある情報は無損失（マーカーカラム、空エントリ、空欄のレコード種別を保持）` / `- 無意味な情報は持たない（コメント、完全な空行、行末の空セルを除去）`。同じ行番号でプロジェクトの `design.md` を開くと `:31` は空行・`:32` は表のヘッダ行だった。
- **V6**: 末尾段落を「作業指示が引用したもの」から、自分で照合した記録へ書き直した。`nablarch-testing-converter` を `e977824` で `git show <commit>:<path>` により開き、`src/main/java/nablarch/test/core/reader/TestCoreReaderAdapter.java:129`（`return Arrays.asList(header.getEffectiveColumnNames());`）・`:254`（`{@link NablarchTestUtils#trimTailCopy(List)} で行末の空セルを除去済みである。`）・`:410`（`{@link NablarchTestUtils#trimTailCopy(List)}で行末の空セルを除去して返す。`）・`src/main/java/nablarch/test/tool/converter/yaml/YamlFormatReader.java:491`（`エントリ先頭行のキー（YAML 記述順）からマーカーカラム（{@code [COL]}）を除いたカラム名を返す。`）を確認した。`grep -n 'trimTail' yaml/YamlFormatReader.java` は0件、`grep -rn 'dropEmptyEntries\|isEmptyEntry' src/main/java/` は `xls/XlsFormatReader.java` の5件のみだった。**指示書の文面と実測が食い違った2点は実測に合わせた**: マーカーカラムの Javadoc は `` `[COL]` `` ではなく `{@code [COL]}`、`:254` の Javadoc は `` `NablarchTestUtils#trimTailCopy(List)` `` ではなく `{@link NablarchTestUtils#trimTailCopy(List)}`。空エントリの根拠は、二次情報（converter の `coverage/issues.md`）を捨て、一次情報へ差し替えた。`nablarch-testing` を `e21bf67` で開き、`src/main/java/nablarch/test/core/reader/PoiXlsReader.java:140-147` の `private boolean isBlankLine(List<String> line)` が全要素空のとき `true` を返し、同 `:93` の `if (isBlankLine(list)) {` の直後の `continue;` で行が読み飛ばされることを確認した。
- **V7**: 参照リポジトリ表の `nablarch-testing-converter` 行に「`#32` の是正2 の追記分のみ `e977824`」を、`nablarch-testing` 行に「`e21bf67`（`#32` の是正2 の追記分で参照）」を足し、宣言文を「『出典から変えた点』の末尾3件を除く本ページの事実は、すべて `2f21bce` で再確認済みである」に限定したうえで、末尾3件の参照コミットと `2f21bce` での成否を書いた。実測: `git rev-list --count 2f21bce..e977824` → `140`。`git show 2f21bce:src/main/java/nablarch/test/tool/converter/yaml/YamlFormatReader.java | sed -n '491p'` → `                result.add(entry);`（Javadoc ではない）。一方 `git show 2f21bce:src/main/java/nablarch/test/core/reader/TestCoreReaderAdapter.java | sed -n '129p;254p;410p'` は `e977824` と同一の3行を返したため、この3箇所は `2f21bce` でも成立する旨を書き分けた。
- **V8**: `TestCoreReaderAdapter.java` の2箇所を、節冒頭の相対パス宣言（`src/main/java/nablarch/test/tool/converter/`）に依存しないフルパス `src/main/java/nablarch/test/core/reader/TestCoreReaderAdapter.java` に直した。実測: `git ls-tree -r --name-only e977824 | grep TestCoreReaderAdapter` → `src/main/java/nablarch/test/core/reader/TestCoreReaderAdapter.java`（と同名のテスト）。あわせて `YamlFormatReader.java` は宣言どおりの相対表記になるよう `yaml/` を付けた。

### V9 `steering.md` の `#33` の件数矛盾（選んだ方針と理由）

**方針: (d) を `#33` の箇条書きから外し、見出し `### #34` 「ビルド用 Docker イメージを `docker build` から作り直せない（環境課題）」として独立させた。`Purpose` は「記述課題3件」と明示した。** 理由: `#33` の3項目 (a)(b)(c) はいずれも解説書の記述をどう直すかの課題で、着手すれば `ja/` または `.rn/` の文書が変わる。(d) は `Dockerfile` と社内 CA の課題で、解決しても解説書の記述は変わらない。系統が違うものを1タスクに束ねると着手単位も完了条件も混ざるため、`Purpose` を広げるより分ける方を採った。(d) が記録していた失敗ログ（`pip install` の TLS 検証失敗、CA の所在、既存イメージ流用の経緯）は、逐語のまま `#34` の「背景と未決点」へ移した。あわせて `#33` (c) の `XlsFormatWriter.java:543` の引用に参照コミット `e977824` を書き足した（実測: `git show 2f21bce:src/main/java/nablarch/test/tool/converter/xls/XlsFormatWriter.java | sed -n '543p'` は空行で、この行は `2f21bce` には無い）。なお上の「Overall Verdict（是正2）」が「`#33` へ (d) として送った」と書いているが、この是正で送り先は `#34` に変わった。

### 元の作業指示の完了条件の再実行（是正後）

| # | 条件 | 実測 | 判定 |
|---|---|---|---|
| 1 | `grep -n '行末の空セル' tools/testdata_converter.rst` が `:39` を含まず新段落1件のみ | ヒット1件・`:71`（前提事項の段落）。`:39` は含まない | OK |
| 2 | `grep -n '空エントリ' tools/testdata_converter.rst` が0件 | `grep -c` → `0` | OK |
| 3 | `grep -c 'StandaloneTestSupportTemplate\|AbstractHttpRequestTestTemplate' mom.rst` が0 | `0` | OK |
| 4 | 10行が6ページの表から消え、`TestDataConverter` が1・`RequestTestingMessagingProvider` が3・`TestCaseInfo` が削除前と同じ。`component.rst`・`entity.rst` に差分が無い | `grep -c` → 1 / 3 / 13。削除前の `TestCaseInfo` も `git show 5c2c26f^:.../web.rst \| grep -c` で 13。落とした10クラスは4ページの `^  \* - ``` 行に1件も現れない。`git diff --stat HEAD -- implementation/class_unit_test/` は空 | OK |
| 5 | `list-table` の行が3行構成を保ち、docutils の parse エラーが0 | 6ページを機械判定し、`:header-rows: 1`・`:widths: 30,45,25` が保たれ、全行が3セル（web 6行／rest 5行／batch 4行／mom 7行／component 5行／entity 5行、ヘッダ込み）。変更した `web.rst`・`batch.rst` を `docutils.core.publish_doctree`（`report_level=2`）に通すと WARNING 以上は web 34件・batch 14件で、**すべて Sphinx 専用の `Unknown directive type`／`Unknown interpreted text role`**。それ以外は0件 | OK |
| 6 | `_batch/*.csv` 連結が `mapping.csv` とバイト一致、`csv.DictReader` が597行、6行の `note` に `【#32`、`disposition` が編集前と同一 | 30ファイルを昇順連結（先頭のみヘッダ込み）した結果が `mapping.csv` とバイト一致（`True`）。`csv.DictReader` の行数 `597`。`current-0201`（MERGE）・`current-0282`・`current-0296`・`current-0309`・`current-0323`・`input-0184`（すべて MOVE）の6行に `【#32` あり。`git diff --stat HEAD -- mapping/` は空で、この是正で台帳は1バイトも触っていない | OK |
| 10 | `verify_glossary.py` が `RESULT: OK` | `RESULT: OK` | OK |
| 11 | `verify_mapping.py` が `OK: no errors` | `OK: no errors` | OK |
| 12 | `pytest mapping/tools -q` が `183 passed, 96 subtests passed` | `183 passed, 96 subtests passed in 1.09s` | OK |
| 14 | 禁止事項に触れていない | `git diff --stat HEAD -- ja/conf.py mapping/glossary.md mapping/mapping.csv en/ locales/` が空。`locales/` に `.gitignore` を足していない。`tools/testdata_converter.rst`（user 判断中の `:71` を含む）にも差分なし | OK |

完了条件13（Docker フルビルド）は指示により実行していない。変更した `.rst` の docutils parse で代替した（条件5 の欄のとおり）。

### Method（レビュー是正で自分で確かめたこと）

- **モジュール側リポジトリを自分で開いた。** 是正2 では指示書からの引用で済ませたが、今回は `nablarch-testing-converter` の `e977824` と `nablarch-testing` の `e21bf67` を `git show <commit>:<path>` で開き、6箇所の逐語と行番号を照合した。2箇所で指示書の文面と実測が食い違い、実測へ合わせた（V6 のとおり）。
- **同じ引用が別コミットでも成立するかを確かめた。** `2f21bce` でも同じ `git show` を実行し、`TestCoreReaderAdapter` の3箇所は成立、`YamlFormatReader.java:491` と `XlsFormatWriter.java:543` は不成立であることを1件ずつ確かめてから、ページ冒頭の宣言文を書き分けた。
- **出典を二次情報から一次情報へ差し替えた。** 空エントリの根拠だった converter リポジトリの `coverage/issues.md`（作業記録）を、NTF 本体 `PoiXlsReader.java` の実装そのものへ置き換えた。
- **編集は文面一致で行い、件数を毎回 assert した。** 置換は Python で `count(old)==1` を assert してから適用した。`batch.rst` の段落移動は、移動元の前後が空行であること・移動先のリード文が `FileSupport` を名指ししていることを assert してから行った。

---

## レビュー指摘の是正（2巡目）（2026-08-21、コミット `72275f2` への4観点レビューで有効と判定された9件）

### F1 `design.md` の採否基準の「落とす側」が実態より広い

**やったこと**: 該当段落を4段落に分け、(1) 落とす側の定義を「そのページが説明するテストにおいて (2) を満たさないクラス」に変えて委譲構造・直接使用の否定という限定を外し、(2) 適用範囲と10行の数え方（是正1 の1行を含まない旨）を書き、(3) 落とした10行の4類型を実態から起こし、(4) (C)・(D) が委譲構造にも直接使用の否定にも当たらないことと `MessageSender` の直接使用を一次情報が肯定していることを明記した。`AbstractHttpRequestTestTemplate` の例は「是正1（`811d1cb`）で落とした1行であり、上の10行には含まれない」と書き添えて残した。

**落とした10行の再分類**（`git show 5c2c26f -- ja/` の削除行10件を1行ずつ判定。パスは `ja/development_tools/testing_framework/` からの相対）:

| # | ページ | クラス | 類型 | 判定の根拠（自分で開いて確認） |
|---|---|---|---|---|
| 1 | `implementation/request_unit_test/web.rst` | `DbAccessTestSupport` | (A) 準備・確認を担うサポートクラス | 同 `:102`「…へ処理を委譲することで実現している」 |
| 2 | `implementation/request_unit_test/rest.rst` | `DbAccessTestSupport` | (A) | 同 `:93`「``RestTestSupport``\ から\ ``DbAccessTestSupport``\ に処理を委譲することで実現している」 |
| 3 | `implementation/request_unit_test/batch.rst` | `DbAccessTestSupport` | (A) | 同 `:17`「テーブルについては\ ``DbAccessTestSupport``\ が…行う」 |
| 4 | `implementation/request_unit_test/mom.rst` | `DbAccessTestSupport` | (A) | 同 `:17`「データベースについては\ ``DbAccessTestSupport``\ が…行う」 |
| 5 | `implementation/request_unit_test/batch.rst` | `FileSupport` | (A) | 同 `:17`「ファイルについては\ ``FileSupport``\ が行う」 |
| 6 | `implementation/request_unit_test/mom.rst` | `MQSupport` | (A) | 同 `:17`「キューについては\ ``MQSupport``\ が行う」 |
| 7 | `implementation/request_unit_test/web.rst` | `HttpRequestTestSupport` | (B) 利用者が継承するスーパクラスのさらに上位 | `javap -cp nablarch-testing-2.0.0.jar` 実測: `BasicHttpRequestTestTemplate extends AbstractHttpRequestTestTemplate<TestCaseInfo>`、`AbstractHttpRequestTestTemplate extends HttpRequestTestSupport`。利用者が継承する `BasicHttpRequestTestTemplate` は表に残っている |
| 8 | `implementation/request_unit_test/batch.rst` | `MainForRequestTesting` | (C) テスティングフレームワークが起動するメインクラス | 同 `:17`・`:173`「テスト用のメインクラス\ ``MainForRequestTesting``\ を通じて…起動され」 |
| 9 | `implementation/request_unit_test/mom.rst` | `MainForRequestTesting` | (C) | 同 `:17`・`:178` |
| 10 | `implementation/request_unit_test/mom.rst` | `MessageSender` | (D) テスト対象のアプリケーションが呼ぶ本番のクラス | 同 `:30`「テスト対象のアプリケーションが\ ``MessageSender``\ を使って同期応答メッセージ送信を行う」。一次情報は直接使用を**肯定**（`ja/application_framework/application_framework/libraries/system_messaging/mom_system_messaging.rst:425` `responseMessage = MessageSender.sendSync(`、同 `http_system_messaging.rst:145`「メッセージ送信には ``MessageSender#sendSync`` を使用する」。いずれも `sed -n` で開いて確認） |

内訳: (A) 6行・(B) 1行・(C) 2行・(D) 1行 = 10行。旧文が挙げていた「委譲構造」に当たるのは (A) の6行だけで、(B)（1行）は委譲元、(C)（2行）はメインクラス、(D)（1行）は本番クラスである。旧文の「一次情報が直接使用を否定しているクラス」に当たる行は10行中0行だった。

**「利用者がどこにも名前を書かない」と書かなかった理由（自分で当て直した結果）**: 最初の草稿は「利用者がどこにも名前を書かないクラス」と書いたが、`grep -rn 'FileSupport' ja/development_tools/testing_framework --include=*.rst` を当てたところ `implementation/request_unit_test/web.rst:512` に `private FileSupport fileSupport = new FileSupport(getClass());` があり、利用者が名前を書く箇所が実在した。落としたのは `batch.rst` の行であって `web.rst` の話ではないため、判定がページ単位であることを本文に明記し、「どこにも」を外した。あわせて `component.rst`（`:81` `public class UserComponentTest extends DbAccessTestSupport {`）で `DbAccessTestSupport` を表に残していることを例として書いた。

**`MessageSender` の役割の残存（選んだ方針と理由）**: **`mom.rst` 側に1文足す方を選んだ。** 落とした行の役割は「``Action``\ から受け取ったパラメータを要求電文に変換し、応答電文をパースして返す」で、`grep -n '応答電文' mom.rst` の全ヒット（`:28`・`:30`・`:49`・`:53`・`:68`・`:77`・`:163`・`:167`・`:180`・`:188`・`:192`・`:194`）を開いたところ、後半の「応答電文をパースして返す」に対応する記述はどこにも無かった。`design.md` 側の書き方を緩めると、他の9行では成立している「役割は本文に残す」という規約を10行のうち1行のために弱めることになる。役割は台帳 `current-0323` が移送対象としている出典の内容でもあるため、ページ側に戻すのが筋と判断した。`mom.rst:30` の末尾に「\ ``MessageSender``\ は、受け取った応答電文をパースして\ Action\ へ返す。」を足した。

### F2 `web.rst:102` の多義・重複（選んだ方針と理由）

**方針: レビューの代案をそのまま採り、`.. tip::` の中に置いたままにした。** 役割を独立した1文に分けたため、読点の有無に依存せず (a) の読み（〔内蔵サーバの起動〕と〔リクエスト単体テストで必要となるアサート〕）だけが残る。「機能」の重複も解消した。

**tip に置いたままとした理由**: `design.md`「利用側ページに内部構造の構成図を置かない」が求めるのは「落としたクラスの役割をリード文または本文に残す」ことであり、`.. tip::` は本文の一部である。委譲構造は利用者がテストを書くのに要らない情報なので、地の文へ昇格させると同節の「利用者は内部の作りを知らなくてもテストを書ける」という方針に逆行する。`web.rst` のリード文 `:15` は `#32` の範囲外のため触っていない。

**実測**: 変更後の `web.rst:102` は1行の段落。`docutils.core.publish_doctree`（`report_level=2`）で WARNING 以上34件、うち `Unknown directive type`／`Unknown interpreted text role`（Sphinx 専用）以外は**0件**。

### F3 `batch.rst:19` の結論部重複と扱いの割れ（選んだ方針と理由）

**方針: `:19` の段落を `.. tip::` にして `:17` の直後（現 `:19`〜`:21`）に置き、結論部を主題化して重複を解消した。** 変更後の文は「\ ``FileSupport``\ が独立したクラスとして提供されているのは、ファイルの操作が、ファイルダウンロードのテストなど\ Nablarch\ バッチアプリケーション以外のテストでも必要になるためである。」

**残さなければならないものの確認**: `mapping/mapping.csv` を `csv.DictReader` で読み `current-0287` を開いた。`note` は「ファイルに関する操作を提供するクラスであり、『テストデータから入力ファイルを作成する』『テストデータの期待値と実際に出力されたファイルの内容を比較する』の2機能を提供する旨、ファイル操作はバッチ処理以外（例：ファイルダウンロード）でも必要なため独立したクラスとして提供している旨。」であり、**「独立したクラスとして提供している旨」が移送対象**である。変更後の文はこの語をそのまま含んでいるため出典の内容は落ちていない。2機能の側は `:17`「準備データの投入とテスト結果の確認は、…ファイルについては\ ``FileSupport``\ が行う」が受けている。

**理由**: `:17` が `FileSupport` を `BatchRequestTestSupport` とは別のクラスとして名指ししているため、「別のクラスとして提供されている」を結論として述べ直すと直前の言い直しになる。独立していることを主題（既知）に回し、理由だけを述語に置いた。`.. tip::` にしたのは、内部構造の理由づけを地の文から補足へ落とすため、および `web.rst` の同種の処置（`.. tip::`）と扱いを揃えるためである。

### F4 参照リポジトリ表の列の意味

第3列「執筆・検証時の HEAD」を1巡目より前の値に戻し（`nablarch-testing` は `—`）、**第4列「`#32` の是正2 の追記分の参照コミット」を新設**して `e977824` / `—` / `e21bf67` を移した。表の直後に、自分で実測した HEAD と実測日を書いた段落を足した。

**実測（2026-08-21、`git -C <repo> log -1`）**: `nablarch-testing-converter` → `6d12021`（ブランチ `ntf-test-data-converter`）、`nablarch-testing` → `f41cc64`（ブランチ `convert-testdata-excel-to-text`）、`nablarch-testing-yaml` → `0197071`（ブランチ `feature/ntf-yaml`）。レビューが挙げた `f0435c6`・`832a700` からもさらに進んでおり、HEAD が動く値であることを本文に明記した。

### F5 `design.md` が2つの別文書を指す状態

「出典から変えた点」の表と直後の段落の `design.md` 全7件を、1件ずつ実物を開いて判定した。

| 表記 | 実物で確認した内容 | 指していた文書 | 直した先 |
|---|---|---|---|
| `design.md:114` | 「YAML の値は…書き出し時に**全値をダブルクォートで囲む**」 | 出典 | `input/testdata-converter-design.md:114` |
| `design.md:295` | 「`YamlTestDataValidator`（`ValidationError` と対）は YAML OUT 後にスキーマ検証を行うリンター」 | 出典 | `input/testdata-converter-design.md:295` |
| `:291` | `YamlFormatWriter --> YamlTestDataValidator : 出力後スキーマ検証` | 出典 | 同 `:291`（直前を明示したうえで「同」） |
| `design.md:155-171` | 整形設定の表。既定色が `[要確認] 見やすい配色を調査して決定` | 出典 | `input/testdata-converter-design.md:155-171` |
| 出典 `:110-112` | Excel／YAML のクォート記法の担い手 | 出典 | `input/testdata-converter-design.md:110-112` |
| `design.md:346-348` | 章構成設計の当該行は「それぞれ1ページにまとめ、ページを跨がせない」で、**「使用方法＝操作手順」ではなかった**。出典 `:346-348` は「開発とリポジトリ分割の手順」でこちらでもない。「使用方法＝操作手順」を実際に述べているのは章構成設計 §5「第4部 ツール」の「ページのアウトライン」（`└── 使用方法` の下に `<操作手順>する`） | 章構成設計 | `.rn/20260724-ntf-yaml-support/design.md` §5「第4部 ツール」の「ページのアウトライン」（`steering.md` Rules の「`.rn/` 内の相互参照は節見出しで指す」に合わせ、行番号をやめた） |
| 直後の段落 `design.md`「出典と実装が食い違う場合」 | 章構成設計に `### 出典と実装が食い違う場合` が実在（`## 8. トンマナ` 配下） | 章構成設計 | `.rn/20260724-ntf-yaml-support/design.md` §8「トンマナ」の「出典と実装が食い違う場合」 |

**F5 の範囲外だが同種の表記が残っている箇所**（指摘が「表と直後の段落」に範囲を切っているため触っていない。指す先は確認済み）: 同ファイル `:125` の `design.md:346-348`（表と同じ誤り。章構成設計 §5 が正）、`:146` の `design.md:29-33`（出典の4項目。出典側）、`:173` の `design.md:25-30`（出典の可逆性の定義。出典側）、`:177` の `design.md:330-360`（章構成設計側だが、現在の §5 は「テストデータ変換ツールは『導入』を持つ」と改まっており記述自体が古い）。

### F6 パス表記の不揃い

「出典から変えた点」の表の `yaml/YamlFormatReader.java:491` と `yaml/YamlFormatReader.java` を、同じ表の `TestCoreReaderAdapter.java` と同じフルパス `src/main/java/nablarch/test/tool/converter/yaml/YamlFormatReader.java` に揃えた。参照リポジトリ表の直後の段落にあった同じ短縮形1件も揃えた。**実測**: `grep -c '`yaml/YamlFormatReader' reviews/page-testdata_converter.md` → `0`。

### F7 Docker の `#34` 分離が steering に記録されていない

`#32` の是正2 Steps の Step 24 から「**`docker build` から作り直した**」の強調を外し、イメージ再作成を `#34` へ分離した旨・是正2指示 完了条件13 が定めた逃げ道（失敗ログを記録して送る）に沿った処置である旨・**`#32` は既存イメージでのフルビルド（警告0・`build succeeded.`）をもって完了条件13 の代替とする**旨を書いた。`#34` 側にも「`#32` の完了判定との関係」の項目を足し、同じ内容を `#34` の視点から書いた（送り先を記述課題の `#33` ではなく環境課題として独立させた `#34` にしたこと、イメージ再作成の検証は `#34` で行うこと）。

### F8 `#33` (a) の参照2件

- `issues.md` —— `nablarch-testing-converter@e977824` で `git show e977824:.rn/ntf-test-data-converter/coverage/issues.md | sed -n '488,500p'` を実行し、「**原因は適用順序である。** 現状は…」が **`:493`**、続く括弧書きが `:494` であることを確認した。`:499` → `nablarch-testing-converter@e977824` の `:493-494` に直し、1巡目までの `:499` が作業ツリーを行番号で指した誤りであることを書き添えた
- `XlsFormatReader.java` —— `git show 45194f9:…/XlsFormatReader.java | sed -n '555,562p'` は `deduplicateColumnNames` の実装で逐語が無く、`git show e977824:…` では `:558-560` に逐語があり `:557` は `<p>` であることを確認した。`:557-560` → `nablarch-testing-converter@e977824` の `:558-560` に直し、ピン `45194f9` では成立しない旨を書き添えた
- Assumptions の参照リポジトリ表に `nablarch-testing-converter`（`#32` のみ）の行を1行足し、参照コミット `e977824` が `#32` の作業指示 `ntf-doc-32-fix2.md` §5-1 の指定である旨と、**上のピン `45194f9` を書き換えるものではない**旨を書いた。実測: `git rev-list --count 45194f9..e977824` → `131`

### F9 `design.md` の書き方2点

- ブレース記法 `…/{web,rest,batch,mom}.rst`・`{component,entity}.rst` を個別列挙に改めた。**実測**: 改修後、`grep -rn '{web,rest,batch,mom}\|{component,entity}' .rn/` のヒットは本ファイル（未追跡の `checks/task-32.md`、1巡目の記録）1件のみで、`design.md` からは消えた（`grep -n '{[a-z_]*,' design.md` → 0件）
- 末尾2文の言い直しを「当てたのは (2) の落とす側だけで、(1) の側は既存の記載も表の行数も変えていない（…）」の1文に畳んだ
- 10行と台帳11行の差を「是正1（`811d1cb`）で `implementation/request_unit_test/web.rst` から落とした `AbstractHttpRequestTestTemplate` の1行は含まない（マッピング台帳の `note` に `【#32】` として記録された削除行が計11行あるのは、この1行を加えた数である）」と書いた。**実測**: 台帳の `【#32` を含む5行（`current-0201` 3クラス・`current-0282` 3・`current-0296` 3・`current-0309` 1・`current-0323` 1）が挙げるクラス名は計11件

### 元の作業指示の完了条件の再実行（2巡目の是正後、2026-08-21）

| # | 条件 | 実測 | 判定 |
|---|---|---|---|
| 1 | `grep -n '行末の空セル' tools/testdata_converter.rst` が `:39` を含まず新段落1件のみ | ヒット1件・`:71` | OK |
| 2 | `grep -c '空エントリ' tools/testdata_converter.rst` が0 | `0` | OK |
| 3 | `grep -c 'StandaloneTestSupportTemplate\|AbstractHttpRequestTestTemplate' mom.rst` が0 | `0` | OK |
| 4 | 10行が6ページの表から消え、`TestDataConverter` 1・`RequestTestingMessagingProvider` 3・`TestCaseInfo` が削除前と同じ・`component.rst`／`entity.rst` に差分なし | 表の行頭 `^  \* - ``<クラス>``` を6ページに当て、`MainForRequestTesting`／`FileSupport`／`MQSupport`／`MessageSender`／`HttpRequestTestSupport` は0件、`DbAccessTestSupport` は `component.rst` の1件のみ（意図どおり）。`TestDataConverter` → `1`、`RequestTestingMessagingProvider` → `3`、`TestCaseInfo` → `13`（`f8f74f2` でも `13`）。`git diff --stat f8f74f2 -- implementation/class_unit_test/` → 空 | OK |
| 5 | `list-table` の行が3行構成を保ち、docutils の parse エラーが0 | 6ページを `docutils.core.publish_doctree`（`report_level=2`）に通し、WARNING 以上は web 34／rest 11／batch 14／mom 20／component 15／entity 28 件。**うち `Unknown directive type`／`Unknown interpreted text role`（Sphinx 専用）以外は全ページ0件** | OK |
| 6 | `_batch/*.csv` 連結が `mapping.csv` とバイト一致、`csv.DictReader` が597行、6行の `note` に `【#32`、`disposition` が編集前と同一 | 昇順連結（先頭のみヘッダ込み）が 287,149 バイトでバイト一致。`csv.DictReader` → `597` 行。`current-0201`／`0282`／`0296`／`0309`／`0323`／`input-0184` の6行すべてに `【#32` あり。`f8f74f2` の `mapping.csv` と `disposition` を全597行で突き合わせて差分0 | OK |
| 7 | `design.md` の節に判定基準の2項目と適用範囲（6ページ） | (1)(2) の2項目と、6ページを個別列挙した適用範囲の段落がある | OK |
| 8 | `reviews/page-testdata_converter.md` に §5-1 の3件 | マーカーカラム・空エントリ・行末の空セルの3行が「出典から変えた点」の表にある | OK |
| 9 | `steering.md` の `#33` に (c) が足され、見出しが改まっている | 見出しは `### #33: 記法の適用順序の明文化、markerColumnColor の説明不足、残置図の禁止語点検`、箇条書きに (c) がある | OK |
| 10 | `verify_glossary.py` が `RESULT: OK` | `RESULT: OK` | OK |
| 11 | `verify_mapping.py` が `OK: no errors` | `OK: no errors` | OK |
| 12 | `pytest mapping/tools -q` が `183 passed, 96 subtests passed` | `183 passed, 96 subtests passed in 0.69s` | OK |
| 14 | 禁止事項に触れていない | `git status --porcelain` は変更6ファイル（`design.md`・`reviews/page-testdata_converter.md`・`steering.md`・`batch.rst`・`mom.rst`・`web.rst`）と未追跡の `checks/task-32.md` のみ。`ja/conf.py`・`mapping/glossary.md`・`mapping/mapping.csv`・`en/`・`locales/` はいずれも未変更。`.gitignore` に `locales` は0件。`tools/testdata_converter.rst` も未変更 | OK |

完了条件13（Docker フルビルド）は指示により実行していない（`docker build`／`sphinx-build` の実行禁止）。変更した `.rst` の docutils parse で代替した（条件5 の欄のとおり）。完了条件15 は本節と1巡目の節が満たしている。

### Method（2巡目の是正で自分で確かめたこと）

- **F1 は書いた直後に自分で当て直した。** 草稿の「利用者がどこにも名前を書かないクラス」を `grep -rn` で6ページ以外にも当てたところ `web.rst:512` の `new FileSupport(getClass())` に当たったため、判定がページ単位であることを明記して範囲を実態に合わせた。旧文が挙げていた2条項が10行のどれに当たるかも1行ずつ数え、(A) 6行・(B) 1行・(C) 2行・(D) 1行、旧文の「直接使用の否定」に当たるのは0行であることを確認してから書いた
- **モジュール側の一次情報を自分で開いた。** `MessageSender` の直接使用の肯定は `sed -n '420,430p'` と `sed -n '140,150p'` で2箇所とも開いた。継承関係は `javap -cp ~/.m2/…/nablarch-testing-2.0.0.jar` を4クラスに実行した。`issues.md` と `XlsFormatReader.java` の行番号は `git show <commit>:<path> | sed -n` で `45194f9` と `e977824` の両方を開いて突き合わせた
- **HEAD は自分で `git -C <repo> log -1` を実行した値だけを書いた。** レビューが挙げた `f0435c6`・`832a700` はそのまま写さず、実測値と実測日で置き換え、HEAD が動く値であることを本文に書いた
- **編集は文面一致で行い、毎回 assert した。** 置換は Python で `old in s` を assert してから適用し、行番号は編集で動いた分（`batch.rst` の `MainForRequestTesting` が `:171` → `:173`）を再 grep して直した
- **`docker build`／`sphinx-build` は実行していない。** `locales/ja/LC_MESSAGES/sphinx.mo` は未変更（`git status --porcelain` に現れない）

## Overall Verdict（レビュー是正2巡目）

- Self-check: OK（F1〜F9 の9件をすべて是正し、元の作業指示の完了条件1〜12・14 を再実行して全 OK。13 は指示により未実行で、変更した `.rst` の docutils parse で代替した。F1・F2・F3 で選んだ方針とその理由、F1 の10行の再分類は本節に記録した）

## レビュー指摘の是正（3巡目）（2026-08-21、コミット `14053b5` への4観点レビューで有効と判定された9件）

### G1 `design.md` の採否基準にまた入っていた過剰主張（1文ずつ実測で当て直した）

**直した内容**: `design.md`「利用側ページに内部構造の構成図を置かない」の3段落目のうち、「(1) に該当する成果物の行が無い `implementation/request_unit_test/batch.rst`・同 `mom.rst` の表もそのままである」を「`implementation/request_unit_test/batch.rst`・同 `mom.rst` の表は (1) のうちテストクラスとテストデータの2行を持ち、テスト対象クラスの行を持たない。これは基準を当てる前からそうであり、この2ページから (1) の行を落としたわけではない」に戻した。あわせて同じ段落の「1行」「`【#32】`」を実測に合わせた。

**書き換えた文が主張している範囲を、1文ずつ当て直した実測**:

| 書いた文 | 主張の範囲 | 実測コマンド | 出力 | 判定 |
|---|---|---|---|---|
| 「(1) に該当する行は6ページとも1文字も変えていない」 | 6ページ全部・(1) の行の全文（役割・作成単位のセルを含む） | 6ページそれぞれについて `git show 9031fa6~1:<path>` と現物から、1つ目の `list-table` の先頭行から最初の ``` * - `` ``` 行の直前までを切り出して `diff` | 6ページとも差分0（`web.rst`／`rest.rst`／`batch.rst`／`mom.rst`／`component.rst`／`entity.rst` すべて `identical`） | 成立 |
| 「`batch.rst`・同 `mom.rst` の表は (1) のうちテストクラスとテストデータの2行を持ち、テスト対象クラスの行を持たない」 | この2ページの表の全行 | `awk '/^\.\. list-table::/{n++} n==1 && /^  \* - /{print}'` を6ページに実行 | `batch.rst` は 名称／リクエスト単体テストクラス／テストデータ／`` `BatchRequestTestSupport` `` の4行、`mom.rst` は 名称／リクエスト単体テストクラス／テストデータ／`MessagingRequestTestSupport`／`MessagingReceiveTestSupport`／`RequestTestingMessagingProvider`／`TestDataConverter` の7行。テスト対象クラスの行は両ページとも0件。他4ページ（`web.rst:32`・`rest.rst:34`・`component.rst:32`・`entity.rst:32`）にはある | 成立。**「(1) に該当する成果物の行が無い」は反例2件（テストクラス・テストデータ）で不成立** |
| 「これは基準を当てる前からそうであり」 | `#32` 着手前の状態 | `git show 9031fa6~1:<path>` の同じ awk | `batch.rst` 9行・`mom.rst` 14行のいずれにもテスト対象クラスの行なし | 成立 |
| 「見出し行を除く表の行数は7行のまま動いていない」 | `811d1cb` の前後の `web.rst` の表 | `git show 811d1cb~1:…/web.rst` と `git show 811d1cb:…/web.rst` に同じ awk | 前後とも見出し行＋7行。変わったのは ``` * - ``AbstractHttpRequestTestTemplate``\ ・\ ``BasicHttpRequestTestTemplate`` ``` → ``` * - ``BasicHttpRequestTestTemplate`` ``` のセル1つだけ | 成立。**「1行」は不成立** |
| 「マッピング台帳の `note` に `【#32・2026-08-21】` として記録された、落としたクラスの名前が計11件」 | 台帳の該当5行の `note` | `grep -c '【#32】' mapping/mapping.csv` → `0`。`grep -o '【#32[^】]*】' mapping/mapping.csv \| sort \| uniq -c` → `13 【#32・2026-08-21】`。`csv.DictReader` で `current-0201`／`0282`／`0296`／`0309`／`0323` の `note` を出力 | 列挙されたクラス名は 3＋3＋3＋1＋1＝11件 | 成立（マーカーは `【#32・2026-08-21】`。`【#32】` では検索できない） |

### G2 `batch.rst:21` の「独立したクラス」（選んだ方針と理由）

**方針: `72275f2` の「``BatchRequestTestSupport``\ とは別のクラスとして提供されている」に戻した。** 理由は2つ。(1) 「独立したクラス」は `ja/` 配下で本件1件だけで（実測: `grep -rn '独立したクラス' ja/ --include='*.rst' \| grep -v _build \| wc -l` → 是正前 `1`、是正後 `0`）、「何から独立か」が文だけでは決まらない。(2) `.. tip::` は本文から切り離して読まれる独立したブロックであり、直前の `:17` が比較対象を与えているという読み方に頼れない。`72275f2` はこの点を是正したものであり、`14053b5` の `.. tip::` 化はそれを理由なく巻き戻していた。是正後の `:21` は「\ ``FileSupport``\ が\ ``BatchRequestTestSupport``\ とは別のクラスとして提供されているのは、…」。

### G3 `reviews/page-testdata_converter.md` の誤った参照（1件ずつ実物を開いて判定した）

| 箇所 | 直す前 | 実測 | 直した後 |
|---|---|---|---|
| `:125` | `design.md:346-348` | `.rn/20260724-ntf-yaml-support/design.md:345` は `### テストデータの2ページ`、`:347-348` はその表のヘッダと区切り。「使用方法＝操作手順」は `:386` の `<操作手順>する`（`grep -n '操作手順' design.md` → `386` の1件のみ） | 章構成設計 `.rn/20260724-ntf-yaml-support/design.md` §5「第4部 ツール」の「ページのアウトライン」 |
| `:177` | `design.md:330-360`（未解決事項） | 同 `:393`「**テストデータ変換ツールは「導入」を持つ**（`#28` §3-16 確定。`#6` の「導入を持たない」を改める）」。`grep -n 'testdata_converter-setup\|^導入' tools/testdata_converter.rst` → `75:.. _testdata_converter-setup:`／`77:導入` | 【解消済み】として、指摘の内容と解消の経緯だけを残した |
| `:146` | 素の `design.md:29-33` | `input/testdata-converter-design.md` の4項目は `:29`〜`:32`（`:33` は空行） | `input/testdata-converter-design.md:29-32` |
| `:173` | 素の `design.md:25-30` | 可逆性の定義は `input/testdata-converter-design.md:25`、「意図ある情報は無損失」は同 `:31`（`:25-30` は後者を含まない） | `input/testdata-converter-design.md:25`（可逆性の定義）・同 `:31`（意図ある情報は無損失） |
| `:78` | `implementation/testdata_notation.rst:1430` | `sed -n '1429,1431p'` → `:1429` が見出し「YAML形式の場合」、`:1430` がアンダーライン、`:1431` が本文 | `:1431` |
| `:79` | 同 `:291` のクラス図 | `sed -n '291,292p' input/testdata-converter-design.md` → `:291` は `XlsFormatWriter --> ExcelFormatConfig : 整形設定を参照`、`:292` が `YamlFormatWriter --> YamlTestDataValidator : 出力後スキーマ検証` | `:292`（逐語を併記） |

**ファイル全体を通しで読んで見つけた、指摘に無い行番号のずれ6件も直した。** `.rn/` 内の文書（`style.md`・`glossary.md`）への参照は、`steering.md` Rules に従って行番号ではなく節見出しへ改めた。行番号のままでは規約ファイルが動くたびに同じずれが起きるためである。

| 箇所 | 直す前 | 実測 | 直した後 |
|---|---|---|---|
| `:4` | `mapping/style.md:347` | `:347` は空行。ページラベルの表は S-08（`grep -n '^### S-' style.md` → `442:### S-08`、当該行は `:490`） | `mapping/style.md` S-08「`:ref:` ラベルの命名規則」のページラベル表 |
| `:103` | `setup/request_unit_test/mom.rst:35` | `:35` は空行。`grep -n 'TestDataConverter'` → `:72` が `:java:extdoc:` 付きの解説 | `:72` |
| `:126` | `style.md:232-234` | `:232-234` は見出しレベルの表。`grep -n '読者が必ず守るべき'` → `:342`（S-06 内） | `mapping/style.md` S-06「アドミニション（tip / note / important）の使い分け」 |
| `:128` | `testdata_notation.rst:124, 879, 881, 904, 1107` | `grep -n 'レコード定義' testdata_notation.rst \| cut -d: -f1` → `124 881 883 906 1109` | `implementation/testdata_notation.rst:124`・`:881`・`:883`・`:906`・`:1109` |
| `:129` | `glossary.md:212, 215` | `:212` は `テストデータ`、`:215` は `YAML形式`。`データブロック` は `:217`、`テストショット一覧` は `:220`。いずれも §5.8 テストデータ（`:208`〜） | `mapping/glossary.md` §5.8「テストデータ」 |
| `:86`・`:136` | `testdata_notation.rst:1164` | `:1164` は `.. important::` ディレクティブ行。レコード種別の本文は `:1166` | `implementation/testdata_notation.rst:1166` |
| `:144`・`:145` | `style.md:155-156`／`:127-182`／`:273` | 「〜する」形式規約は S-03（`:159`〜`:227`。禁止語は `:187`）、全 `list-table` 例外は S-07（`:364`〜。例外条項は `:370`） | S-03「セクションタイトルの形式（「〜する」形式）」／S-07「表の記法」 |
| `:101` | `ja/conf.py:299-323` | `grep -n 'javadoc_url_map' ja/conf.py` → `:304`。辞書は `:304`〜`:318` | `ja/conf.py:304-318` |

`design.md`／`testdata-converter-design.md` の取り違えは、`grep -n '\`design\.md' reviews/page-testdata_converter.md` が0件になったことで残っていないことを確認した。

**直していない1件（報告のみ）**: `mapping/style.md:401` が `reviews/page-testdata_converter.md:94` を指しているが、`:94` は空行で、当該記述は `:101`（「クラス名の表記」節）である。`style.md` は本タスクの9件の対象外のため触っていない。

### G4 `steering.md` Step 24 と `#34` の理由づけの二重記載

**直した内容**: `steering.md` Rules「1件のフィードバック対応につき、詳細な理由づけを書く場所を1箇所に決め、他の場所は1〜2行のポインタにとどめる」（`steering.md` Rules の該当項）に従い、詳細は `#34`「`#32` の完了判定との関係」に残し、Step 24 は「**`docker build` からのイメージ再作成は `#34` へ分離し、既存イメージでのフルビルドを完了条件13 の代替とする**（`#32` のレビュー是正、2026-08-21）。理由と失敗ログの所在は `steering.md` `#34`「`#32` の完了判定との関係」。」の2文に落とした（約520字→約110字）。

### G5 `web.rst:102` の「起動を提供」（選んだ方針と理由）

**方針: 「内蔵サーバの起動機能と、リクエスト単体テストで必要となるアサートを提供する。」に直した。** 「起動を提供」は `ja/` 配下で0件（実測: `grep -rn '起動を提供' ja/ --include='*.rst' | grep -v _build | wc -l` → `0`）で目的語が宙に浮く。「〈動作〉機能を提供する」は同じ第3部に先例があり、`implementation/request_unit_test/mom.rst:77`「同期応答メッセージ送信のリクエスト単体テストで、要求電文のアサート機能および応答電文の生成・返却機能を提供する。」がそれにあたる。

**主語 `HttpRequestTestSupport` は据え置いた。** 「スーパクラス」に置き換えると、この文が `HttpRequestTestSupport` を `DbAccessTestSupport` への委譲元として名指しできなくなり、`design.md`「利用側ページに内部構造の構成図を置かない」が定める「落としたクラスの役割は、各ページのリード文または本文に残す」が再び不成立になるためである。

### G6 `mom.rst:30` の「返す。」の連続と段落長

**直した内容**: 末尾の「\ ``MessageSender``\ は、受け取った応答電文をパースして\ Action\ へ返す。」を「\ ``MessageSender``\ はこれをパースし、\ Action\ へ引き渡す。」に置き換えた。`MessageSender` の役割の後半（応答電文をパースして返すこと）はページに残っている。

実測（マークアップを除いた文字数を数えた）: 「返す。」は段落内 `2` → `1` 件。段落長は `387` → `381` 字（比較対象の `rest.rst:189` は `298` 字）。「引き渡す」は `ja/` 配下に14件の先例がある。

### G7 参照リポジトリ表の直後の実測 HEAD

**直した内容**: 揮発する HEAD の列挙を落とし、不変条件だけを残した。あわせて `:19` の現在形を、執筆・検証時点の記録であると分かる書き方に直した。

陳腐化の実測（2026-08-21、`git -C <repo> log -1`）: `nablarch-testing-converter` は記録の `6d12021` から `f27fb8d` へ、`nablarch-testing` は `f41cc64` から `cf81162` へ動いていた。`nablarch-testing-yaml` は `0197071` のままだが、`:19` は同じリポジトリの作業ツリーを `b91abc1` と現在形で書いており、同じファイル内で矛盾していた。

なお指示は「不変条件＝第2列のピンと第4列の参照コミット」としているが、**実物を読むと converter は第2列が「ピンなし」で、本ページの事実の大半は第3列に記録された `2f21bce` に依存している**（同ファイル `:17`「「出典から変えた点」の末尾3件を除く本ページの事実は、すべて `2f21bce` で再確認済みである」、同 `:36`「`nablarch-testing-converter@2f21bce`」）。そのため「第2列と第4列」とは書かず、依存先のコミットを `2f21bce`／`e977824`／`e21bf67`／`190cc9a` と名指しで書いた。

### G8 `design.md` の採否基準の段落の書き方2点

- **言い直し**: 5段落目末尾の「これは是正1（`811d1cb`）で落とした1行であり、上の10行には含まれない」を「（上の10行に含まれない理由は本節の3段落目に書いた）」に縮めた。`AbstractHttpRequestTestTemplate`／是正1 `811d1cb`／10行に含まれない の3命題を全文で書くのは3段落目の1箇所だけにした。
- **主題と本文の不一致**: (C) の根拠を1文足す方を採った。「(C) の `MainForRequestTesting` は、テスティングフレームワークがテスト対象を起動するために使うメインクラスである。落としたのは、利用者がテストコード・テストデータ・コンポーネント設定のいずれにもこの名前を書かず (2) を満たさないためである（…）」。主題を (D) に絞ると、(C) を落とした根拠が `design.md` のどこにも無くなるため。

(C) に添えた括弧内の実測: `grep -rn 'MainForRequestTesting' ja/ | grep -v '/_build/'` → 5件（`implementation/request_unit_test/batch.rst:17`・`:173`、同 `mom.rst:17`・`:30`・`:178`）。5件とも地の文で、コード例・テストデータ例・コンポーネント設定例には現れない（`.rst` 以外のファイルを含めて走査した）。

### G9 細かい事実のずれ4件

| 件 | 実測コマンド | 出力 | 直した後 |
|---|---|---|---|
| 台帳のマーカー | `grep -c '【#32】' mapping/mapping.csv` ／ `grep -o '【#32[^】]*】' mapping/mapping.csv \| sort \| uniq -c` | `0` ／ `13 【#32・2026-08-21】` | `【#32・2026-08-21】` |
| 「`AbstractHttpRequestTestTemplate` の1行」 | `git show 811d1cb -- …/web.rst` | 表の行数は前後とも見出し行＋7行。差分はセル1つの中身（2クラス併記→1クラス） | 「同コミットが変えたのは2クラスを併記していたセルの中身だけで、見出し行を除く表の行数は7行のまま動いていない」 |
| `http_system_messaging.rst:145` の逐語 | `sed -n '145p' ja/application_framework/application_framework/libraries/system_messaging/http_system_messaging.rst` | ``   * メッセージ送信には、 :java:extdoc:`MessageSender#sendSync<nablarch.fw.messaging.MessageSender.sendSync(nablarch.fw.messaging.SyncMessage)>` を使用する。`` | 読点と句点を戻し、ロールも含めた形にした（参照先の完全修飾名は `<…>` で省略） |
| 類型 (B) の行番号 | `grep -n 'HttpRequestTestSupport' …/web.rst` | `102` の1件のみ | 同 `web.rst:102` |

### 元の作業指示の完了条件の再実行（3巡目の是正後、2026-08-21）

| # | 条件 | 実測 | 判定 |
|---|---|---|---|
| 1 | `grep -n '行末の空セル' tools/testdata_converter.rst` が `:39` を含まず新段落1件のみ | ヒット1件・`:71` | OK |
| 2 | `grep -c '空エントリ' tools/testdata_converter.rst` が0 | `0` | OK |
| 3 | `grep -c 'StandaloneTestSupportTemplate\|AbstractHttpRequestTestTemplate' mom.rst` が0 | `0` | OK |
| 4 | 10行が6ページの表から消え、`TestDataConverter` 1・`RequestTestingMessagingProvider` 3・`TestCaseInfo` が削除前と同じ・`component.rst`／`entity.rst` に差分なし | 表の行頭 `^  \* - ``<クラス>``` を6ページに当て、`MainForRequestTesting`／`FileSupport`／`MQSupport`／`MessageSender`／`HttpRequestTestSupport` は0件、`DbAccessTestSupport` は `component.rst:35` の1件のみ。`TestDataConverter` → `1`、`RequestTestingMessagingProvider` → `3`、`TestCaseInfo` → `13`。`git diff --stat 14053b5 -- implementation/class_unit_test/` → 空 | OK |
| 5 | `list-table` の行が3行構成を保ち、docutils の parse エラーが0 | 6ページを `docutils.core.publish_doctree`（`report_level=2`・`source_path` 指定）に通し、当該ファイル発のメッセージは web 34／rest 11／batch 14／mom 20／component 15／entity 28 件。**`Unknown directive type`／`Unknown interpreted text role`（Sphinx 専用）以外は全ページ0件** | OK |
| 6 | `_batch/*.csv` 連結が `mapping.csv` とバイト一致、`csv.DictReader` が597行、6行の `note` に `【#32`、`disposition` が編集前と同一 | 昇順連結（先頭のみヘッダ込み）がバイト一致（`True`、541,037 バイト）。`csv.DictReader` → `597` 行。`note` に `【#32` を含む行は13行（うち是正2 の6行を含む）。`mapping.csv` は今回未変更（`git status --porcelain` に現れない）ため `disposition` も不変 | OK |
| 7 | `design.md` の節に判定基準の2項目と適用範囲（6ページ） | `design.md:141` に (1)(2) の2項目、`:143` に6ページを個別列挙した適用範囲 | OK |
| 8 | `reviews/page-testdata_converter.md` に §5-1 の3件 | マーカーカラム・空エントリ・行末の空セルの3行が「出典から変えた点」の表（`:87`〜`:89`）にある | OK |
| 9 | `steering.md` の `#33` に (c) が足され、見出しが改まっている | 見出しは `:936` `### #33: 記法の適用順序の明文化、markerColumnColor の説明不足、残置図の禁止語点検`、(c) は `:956` | OK |
| 10 | `verify_glossary.py` が `RESULT: OK` | `RESULT: OK` | OK |
| 11 | `verify_mapping.py` が `OK: no errors` | `OK: no errors` | OK |
| 12 | `pytest mapping/tools -q` が `183 passed, 96 subtests passed` | `183 passed, 96 subtests passed in 0.63s` | OK |
| 14 | 禁止事項に触れていない | `git status --porcelain` は変更6ファイル（`design.md`・`reviews/page-testdata_converter.md`・`steering.md`・`batch.rst`・`mom.rst`・`web.rst`）と未追跡の `checks/task-32.md` のみ。`ja/conf.py`・`mapping/glossary.md`・`mapping/mapping.csv`・`en/`・`locales/` はいずれも未変更。`.gitignore` に `locales` は0件。`tools/testdata_converter.rst` も未変更 | OK |

完了条件13（Docker フルビルド）は指示により実行していない（`docker build`／`sphinx-build` の実行禁止）。変更した `.rst` の docutils parse で代替した（条件5 の欄のとおり）。

### 参考記録: `14053b5` のコミットメッセージの事実誤り

`14053b5` のコミットメッセージは「`batch.rst` の `FileSupport` の段落は tip にして**リード文の直後へ移し**」と書いているが、**位置は動いていない**。`72275f2` がこの段落を `:19` に置いてから `14053b5` が `.. tip::` で包むまで、段落は一貫して `:17` の直後（`:19`〜`:21`）にある。またこのページのリード文は `:10`（「Nablarch\ バッチアプリケーションのリクエスト単体テストでは、…」）であり、段落はその直後にはない。コミットメッセージは書き換えられないため、ここに記録する。

### Method（3巡目の是正で自分で確かめたこと）

- **G1 は書いた文を1文ずつ実測で当て直した。** 全称・限定の表現（「6ページとも」「持たない」「7行のまま」「計11件」）を書いた文それぞれについて、反例が出ないかを走査してから確定した。「(1) に該当する成果物の行が無い」は、`batch.rst`／`mom.rst` の表の全行を列挙して反例2件（テストクラス・テストデータ）を自分で見つけたうえで落とした
- **HEAD は自分で `git -C <repo> log -1` を実行した。** 3リポジトリとも実行し、2つが記録から動いていることを確認したうえで、値そのものは恒久記録に書かないことにした
- **指示の前提もそのまま写さず実物で確かめた。** G7 の「不変条件＝第2列のピンと第4列の参照コミット」は、実物の表と `:17`／`:36` を読むと converter に第2列のピンが無く成り立たないため、依存先のコミットを名指しする書き方に変えた
- **編集は文面一致で行い、毎回 assert した。** 置換はすべて Python で `s.count(old) == 1` を assert してから適用し、いずれも1行内の置換に留めたため、6ファイルとも行数は変わっていない（`git diff --numstat` の追加行数＝削除行数）。他ファイルからの `file:line` 参照がずれないことも確認した
- **`docker build`／`sphinx-build` は実行していない。** `locales/ja/LC_MESSAGES/sphinx.mo` は未変更

## Overall Verdict（レビュー是正3巡目）

- Self-check: OK（G1〜G9 の9件をすべて是正し、あわせてファイル通読で見つけた行番号のずれ6件も直した。元の作業指示の完了条件1〜12・14 を再実行して全 OK。13 は指示により未実行で、変更した `.rst` の docutils parse で代替した。G1 の当て直しの実測、G2・G5 で選んだ方針とその理由、`14053b5` のコミットメッセージの誤りは本節に記録した）

---

## 4観点レビューの判定（是正2。調整役が記入。2026-08-21）

実装エキスパートはこの節を書かない。以下は調整役が収集した各観点の判定と、その triage の結果である。

### ラウンド構成

| ラウンド | 対象コミット | QA | 設計 | クラフト | 検証 |
|---|---|---|---|---|---|
| 1回目 | `5c2c26f` | fail | fail | fail | fail |
| 2回目（是正1） | `72275f2` | **pass** | fail | fail | **pass** |
| 3回目（是正2） | `14053b5` | 実施せず（2回目 pass、変更は fail 2観点の指摘由来） | fail | fail | 実施せず（同左） |
| 4回目（是正3） | `456544e` | — | — | — | — |

是正は `task-verify-workflow.md` の上限3回に達した（`72275f2`・`14053b5`・`456544e`）。4回目の観点レビューは回していない。`456544e` は調整役が自分で全件を実測照合した（下記「調整役の独立レビュー」）。

### QA Expert Review

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Verification approach meaningful to the objective (checks the right thing, not just "passed") | OK（2回目以降） | 1回目は fail。「grep が 0 になった」の先にある読み物としての正しさで実害5件を検出（`design.md` の基準(1)の未適用、`:71` の因果の誤り、空エントリの根拠、`web.rst` の役割消失、`batch.rst` の浮いた段落）。2回目に pass。独立検証として jar の `javap` 走査、converter リポジトリの直接参照、CSV の自作連結スクリプト、リポジトリを複製したうえでのフルビルドを実施しており、付属検証スクリプトに依存していない |

### Expert Reviews

#### Design Expert

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Approach/structure fits | OK（`456544e` 時点） | 採否基準の4類型 (A)6・(B)1・(C)2・(D)1 が落とした10行と過不足なく一致することを、3回目のレビューが独立に当て直して確認。残存行に基準を当てても、落ちるはずなのに残っている行は0件 |
| System-wide integrity (interfaces, cross-doc consistency) | OK（`456544e` 時点） | 1〜3回目でいずれも fail。指摘の中心は `design.md` の過剰主張（第2部/第3部の取り違え、「6ページ全部へ適用」、「委譲構造と直接使用の否定」の2条項、「(1) に該当する成果物の行が無い」）で、**4回連続で別の過剰主張が混入した**。`456544e` で解消。`#32`↔`#34` の宙ぶらりん、`#33` (a) の参照コミット欠落も解消済み |

#### Craft Expert（writing）

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Medium-specific best practice | OK（`456544e` 時点） | 1〜3回目とも fail。`web.rst:102` の二義（読点の脱落）・「機能」の重複・120字、`batch.rst` の結論部重複、`mom.rst:30` の「返す。」の連続と段落長、`reviews/` の表の列の意味。いずれも `456544e` で解消。段落1行・禁止語0件・S-13 エスケープ・docutils parse は全ラウンドで OK |
| Consistency with existing style | OK（`456544e` 時点） | `.. tip::` の書き出し・「〜のは、〜ためである」の構文とも既存の先例に一致することを実測で確認。`web.rst`（tip）と `batch.rst`（tip）で扱いが揃った |

#### Verification Expert（fact-check）

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Artifact actually checked (claims verified) | OK（2回目以降） | 1回目は fail。**2回目は「自ら `git show` で照合した」という宣言そのものを疑わせる形で12件の参照を検証させ、不一致0件**（`TestCoreReaderAdapter.java:254` と `:410` の読点の有無の違いまで引用どおり）。1回目に見つかった「実装の逐語は作業指示が引用したもの」という二次情報依拠の記述は是正済み |
| Coverage (claims) | OK | 1回目は新規主張51件、2回目は29件を分解して全件を出典に照合。いずれも確かめ漏れ0件 |

### Triage の結果

- **Valid → 是正した**: 1回目9件（V1〜V9）、2回目9件（F1〜F9）、3回目9件（G1〜G9）。計27件
- **Invalid → 却下した**: 2件
  - 設計1回目「`locales/ja/LC_MESSAGES/sphinx.mo` が dirty で `git checkout` が未実行」—— 誤帰属。`5c2c26f` 直後の `git status` は `?? checks/task-32.md` のみで、dirty 化させたのは調整役が並行で走らせた検証観点エージェントの Docker ビルドだった（クラフト観点が復元済み。現在クリーン）
  - QA/クラフト「`checks/task-32.md` が未追跡でコミットに含まれていない」—— 意図的な運用。`#31`・`#32` と同じく `#32` の check-off コミットで調整役が staging する
  - クラフト3回目 M-1「`web.rst:102` の主語 `HttpRequestTestSupport` を『スーパクラス』に置き換える」—— 採らない。`design.md` が定める「落としたクラスの役割は本文に残す」が再び不成立になる。この文はそもそも `HttpRequestTestSupport` が委譲元であることを述べる文である
- **Escalation → user へ上げた（未回答）**: 判断A〜E の5件（下記）

### 調整役の独立レビュー（`456544e`。2026-08-21）

4回目の観点レビューは回していないため、調整役が全件を自分で実測した。

| 確認項目 | 結果 | 実測 |
|---|---|---|
| `batch.rst`・`mom.rst` の表の (1) の行 | 一致 | 両表とも「リクエスト単体テストクラス」「テストデータ」を持ち、テスト対象クラスの行のみ無い |
| `811d1cb` が変えたのはセル1つ | 一致 | `811d1cb~1`・`811d1cb` とも web.rst の表は `* - ` 8行（見出し行込み）。差分は `` `AbstractHttpRequestTestTemplate`・`BasicHttpRequestTestTemplate` `` → `` `BasicHttpRequestTestTemplate` `` のセル1つ |
| `MainForRequestTesting` の出現5件 | 一致 | `grep -rn 'MainForRequestTesting' ja/ --include=*.rst` → `mom.rst:17`・`:30`・`:178`、`batch.rst:17`・`:173` の5件 |
| `MessageSender` の一次情報 | 一致 | `mom_system_messaging.rst:425` に `responseMessage = MessageSender.sendSync(`、`http_system_messaging.rst:145`「メッセージ送信には、 :java:extdoc:`MessageSender#sendSync<…>` を使用する。」 |
| `PoiXlsReader#isBlankLine` | 一致 | `nablarch-testing@e21bf67` の `:93` `if (isBlankLine(list)) {`、`:140-147` に定義 |
| `XlsFormatReader#dropEmptyEntries` | 存在 | `converter@e977824` の `:566`（呼出は `:162`・`:193`）。Javadoc は「マーカーカラムだけを持つ行は本体では空エントリにならず…ここで落とす」 |
| `issues.md` の逐語 | `:493` | `#33` (a) が指していた `:499` は誤り。`456544e` で是正済み |
| `XlsFormatReader.java` の申し送り逐語 | `e977824` の `:558-560` | ピン `45194f9` では同じ行が `deduplicateColumnNames` の実装で不成立 |
| 台帳 | 一致 | `_batch` 30ファイルの昇順連結が `mapping.csv` とバイト一致。`csv.DictReader` 597行。`f8f74f2` との差分は指定6行の `note` のみで、`disposition` を含む他列は全行不変 |
| 検証器3本 | OK | `RESULT: OK` / `OK: no errors` / `183 passed, 96 subtests passed` |

### 3回の上限に達した時点で残る未解決の指摘

いずれも `456544e` の時点で有効なまま残っている。

1. **`mapping/style.md:401` が `reviews/page-testdata_converter.md:94` を指しているが `:94` は空行**（当該記述は `:101`）。`#32` の是正で `reviews/` が伸びたことによって生じたずれである。`.rn/` 内の相互参照を節見出しで指す Rules にも反する。**次のラウンド（user 判断A〜E の反映）に含めて直す**
2. **落としたクラスの役割の置き場所が4ページで揃っていない** —— `batch.rst`・`mom.rst` は機能概要のリード段落の本文、`web.rst` は使用方法配下の `.. tip::`、`rest.rst` は使用方法配下の本文。`design.md` が「リード文または本文」を許すため規約違反ではないが、揃ってはいない。`web.rst` のリード文（`:15`）が他3ページと違ってサポートクラスを名指ししないことに由来し、`#32` の範囲外
3. **完了条件13（Docker フルビルド）** —— `docker build` は3回連続で失敗し、イメージ自体は未検証のまま。`#34` へ分離済み。フルビルド自体は既存イメージで警告0・`build succeeded.` を独立に2回確認している

### user 判断待ち（判断A〜E。未回答のため `#32` は check-off できない）

- **A**: `tools/testdata_converter.rst:71` の段落（作業指示 §2-2 の逐語）に、因果のねじれと適用範囲（`testdata_notation.rst:1544-1545` はファイル・メッセージ限定）の書き漏れがある
- **B**: 判断1（空エントリ）の前提。`XlsFormatReader#dropEmptyEntries` は converter 側の判断だが、対象はマーカーカラムだけの行という残差に限られる。調整役の推奨は「判断1 は維持し、`#33` (a) の背景に1行足す」
- **C**: 採否基準の「載せる側」が6ページで揃っていない（`batch.rst`・`mom.rst` にテスト対象クラスの行が無い、`mom.rst` の表にスーパクラスが無い）。表への行追加は作業指示が禁じているため未実施。推奨は `#33` へ (e) として送る
- **D**: 台帳 `note` の列挙範囲。`9031fa6` で落ちた7行（`StandaloneTestSupportTemplate`×2・`TestShot`×2・`HttpServer`×2・`AbstractHttpRequestTestTemplate`）が台帳のどこにも記録されていない。推奨は `#33` で補う
- **E**: `Dockerfile` に社内 CA を入れる恒久対処（`#34`）

## Overall Verdict（是正2 全体）

- Self-check: OK（実装エキスパートが各ラウンドで記入）
- QA: OK（2回目以降）
- Design expert: OK（`456544e` 時点。1〜3回目は fail）
- Craft expert: OK（`456544e` 時点。1〜3回目は fail）
- Verification expert: OK（2回目以降）
- Ready to check off: **No** —— user 判断A〜E が未回答であり、判断A は `tools/testdata_converter.rst` を、判断C は6ページの表を動かしうる

---

## Completion Criteria（是正3指示 `ntf-doc-32-fix3.md`）

対象は判断A〜E の回答を反映した是正3。実行日 2026-08-21、開始コミット `6f828d3`。是正3 の成果物 `4d0a48a` に対する4観点レビューで有効と判定された17件も、同じ日に同じ節へ反映した（以降「是正3-2」）。`file:line` は特記のない限り現在の作業ツリーを指す。`.rn/` 内の文書どうしの相互参照は `steering.md` `# Rules` に従い節見出しで指す。

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| 1. `tools/testdata_converter.rst` の該当段落が §1 の変更後の文と一致し、`grep -c '行末の空セル' …` が 1 | OK | 置換は Python で `s.count(old) == 1` を assert してから実施。適用後 `$ grep -c '行末の空セル' ja/development_tools/testing_framework/tools/testdata_converter.rst` → `1`、`$ grep -n` の位置は `:71`。段落は指示書 §1「変更後」と一致 | | |
| 2. `reviews/page-testdata_converter.md` の空エントリの行に `XlsFormatReader.java:566` の残差処理が、行末の空セルの行に適用範囲（ファイル・メッセージ）が書かれている | OK | `reviews/page-testdata_converter.md` §「出典から変えた点」の表で、「空エントリの保持」の行の「変えた理由」欄に `dropEmptyEntries`（`XlsFormatReader.java:566`、呼び出しは同 `:162`・`:193`）と同 `:550-554` の Javadoc に基づく残差の説明を追記。「行末の空セルの除去」の行の「ページの記述」欄に適用範囲（`implementation/testdata_notation.rst:1544-1545` の表行が対象を「ファイル・メッセージ」としている）を追記。同節の表の直後の段落に是正3 の照合記録を追記した。是正3-2 で同節をさらに2点直した。(1) 実処理の係り受けが取れなかった箇所を「実処理は同 `:413` の `BodyLineCollector` にあり、行末の空セルを落としているのは同 `:464` `bodyLines.add(NablarchTestUtils.trimTailCopy(line));` である」に書き換え、`:413` が `private static final class BodyLineCollector` であることを `git show e977824:…/TestCoreReaderAdapter.java` で確認した。(2) 「Excel 形式」の半角空白を詰めた（`$ grep -c 'Excel 形式' reviews/page-testdata_converter.md` → 0件、`Excel形式` は5件）。是正3-3 でさらに2点直した。(1) 「行末の空セルの除去」行の「ページの記述」列が229字と同列の他11セル（10〜82字）から突出し、理由と日付スタンプが混ざっていたため、同列を65字に縮めて理由と日付スタンプを「変えた理由」列の末尾へ移した。(2) 適用範囲の根拠が converter 側と成果物だけで NTF 本体を走査していなかったため、`nablarch-testing@e21bf67` の実測を「変えた理由」列に足した（`src/main/java/nablarch/test/core/reader/HeaderLine.java:33` `List<String> keys = trimTailCopy(headerLine);` がヘッダ行を持つブロック全般で走り、`ListMapParser.java:64`・`TableDataParser.java:93` が `HeaderLine` を生成するため、テーブル系と `LIST_MAP` のカラム名行でも行末の空セルは詰められる）。**是正3-4**: 4列目の後半（NTF 本体側の反証）を2文に落とし、詳細は下の「4観点レビューの判定（是正3。調整役が記入。2026-08-21）」節を指す形にした。`:89` の閉じパイプの欠落と `:88` のコードスパン中のパイプ文字（`grep` の交替）も、パイプを使わない2つの `git grep` に置き換えて直し、全表の全行が同じセル数であることをスクリプトで数えて確かめた | | |
| 3. `steering.md` の `#33` に (d) が足され、見出しにも反映されている。(d) に「`mom.rst` の表にスーパクラスが無い」という誤った記述が含まれていない | OK | `steering.md` §「#33: 記法の適用順序の明文化、markerColumnColor の説明不足、残置図の禁止語点検、「主なクラスとリソース」の表の載せる側の不揃い」の見出し末尾に該当句を追加し、同節の Purpose を「記述課題3件」→「4件」に直して (d) を追記、同節の「背景と未決点」に (d) の項を足した。是正3-2 で (d) を2点直した。(1) `mom.rst` の表に無いスーパクラスは2つあり、同 `:130` の `BatchRequestTestSupport` と同 `:131` の `BasicHttpRequestTestTemplate` の両方を挙げた（`BasicHttpRequestTestTemplate` は `web.rst:35` の表にはあるが、採否の判定はページ単位のため `mom.rst` 側は独立に未処理である旨も書いた）。(2) 表の記述を「`mom.rst` の表にあるスーパクラスは `MessagingRequestTestSupport`（同 `:70`）と `MessagingReceiveTestSupport`（同 `:73`）の2つ」と主語を限定し、表全体が見出し行を除いて6行あること（同 `:64`・`:67`・`:70`・`:73`・`:76`・`:79`）を併記して、表に2行しか無いとは読めないようにした。指示書が誤りとした「`mom.rst` の表にスーパクラスが無い」は書いていない | | |
| 4. `design.md` の §「利用側ページに内部構造の構成図を置かない」に §4-1 の段落があり、`:141` の文は変わっていない | OK（内訳は指示と異なる内容にした。下の「§4-1 の内容を実測に合わせて変えた点」を参照） | 新段落は `design.md` §「利用側ページに内部構造の構成図を置かない」の5段落目で、是正3-2 でもこの1段落のまま（分割していない）。`$ git diff --numstat 6f828d3 -- .rn/20260724-ntf-yaml-support/design.md` → `3 1`（新段落＋空行の追加2行と、同節3段落目の1行の書き換え）。`:141` は同節2段落目の「落としたクラスの役割は、各ページのリード文または本文に残す。」を含む行で、`$ diff <(git show 6f828d3:….md \| sed -n '141p') <(sed -n '141p' design.md)` が差分なし。是正3-3 で同じ段落を書き直した（レビュー指摘14件のうち8件）。事実の誤り1件（「残った動作の記述は、帰属先が表に残したクラスへ移っている。」）を反例2件の実測により削除し、`(1)`〜`(5)` のラベル・太字1スパン・「計7行」の単位明記・一般名の書き分け・段落序数指しの解消・台帳8件と7行のずれの括弧書き・規範違反2行の処置を反映した。段落は1つのままで、`$ git diff --numstat 1ccfc53 -- .rn/20260724-ntf-yaml-support/design.md` → `1 1`（`:141` を含む他の段落は1文字も動いていない）。詳細は下の「是正3-3（レビュー指摘14件）の記録」節。**是正3-4**: 同段落の件数の主張に母集団の限定語を足し、「一般名は行ごとに違う」を「3種である」に直し、重複2か所を削った。`:149` の「本節の3段落目」も内容指しに直した。`$ git diff -U0` の変更行は `:147` と `:149` の2行だけで、`:141` は動いていない | | |
| 5. `steering.md` の `#34` 未決点に §5 の方針が書かれている | OK | `steering.md` §「#34: ビルド用 Docker イメージを `docker build` から作り直せない（環境課題）」の「未決点」。「`Dockerfile` は変更しない方向」「CA は環境固有で焼き込むと他環境が壊れる」「`--build-arg` またはビルドコンテキストへの一時配置とビルド後の削除を `steering.md` の手順として残す方向で検討」「`ca.crt`・`Dockerfile.ca` を作業ツリーに残さない」の4点を記載 | | |
| 6. `mapping/style.md` に `reviews/page-testdata_converter.md:94` が残っていない。§6 の `grep -nE` が0件 | OK | 4件すべてを節見出し方式に是正した。`mapping/style.md` §S-07「表の記法」の3件を `` `reviews/page-class_unit_test.md` §「`#15` 以降への申し送り」``・`` `reviews/page-testdata_converter.md` §「クラス名の表記」``・`` `reviews/page-request_unit_test_batch.md` §7「判断待ち（decide）」`` に、`mapping/glossary.md` §5.4「メッセージング方式」の1件を `` `S:reviews/page-request_unit_test_http_messaging.md` §3「出典より実装を優先した点」`` に直した。`$ grep -nE '(reviews\|design\|steering\|checks)/[a-z0-9_-]+\.md:[0-9]+' mapping/style.md mapping/glossary.md mapping/vocabulary.md` → ヒット0件（exit 1）。参照先の見出しは4件とも各ファイル内で一意（`$ grep -n '^#' <file>` で確認）。なお本行の Criterion 列に残る `reviews/page-testdata_converter.md:94` は、指示書 `ntf-doc-32-fix3.md` の完了条件6 の逐語であり、Criterion 列は本ファイルで書き換えを禁じられているためそのままにした（是正3-2）。**是正3-3 で、この grep の範囲の限界を明記する。** パターン `(reviews\|design\|steering\|checks)/[a-z0-9_-]+\.md:[0-9]+` はディレクトリ接頭辞付きのパスしか拾わず、ベアファイル名の `.rn/` 内参照を検出できない。実際に `mapping/style.md` には `ntf-doc-27-small-3rd.md:26`・`:28`（同ファイルの `:58`）と `ntf-doc-27-small-3rd.md:129-132`（同 `:224`）が残っている（`$ grep -nE '[a-z0-9_-]+\.md:[0-9]+' mapping/style.md` → 2行）。したがって0件という出力は「指示書 §6 が指定したパターンに一致する参照が無い」ことの証拠であって、「`.rn/` 内を行番号で指す参照が無くなった」ことの証拠ではない | | |
| 7. `_batch/*.csv` 連結が `mapping.csv` とバイト一致し `csv.DictReader` が597行。`456544e` との差分が指定5行の `note` のみ | OK | `mapping/` をカレントに昇順連結（先頭のみヘッダ込み） → `identical: True` / `rows: 597`。`456544e` の `mapping.csv` を `git show` で取り出し、`csv.DictReader` で全597行・全14列を突き合わせた結果、値が変わったフィールドは5件のみで、いずれも `note` 列かつ旧値を接頭辞として保持（`b[note].startswith(a[note])` が真）。`disposition` を含む他の列は全行一致。`$ git diff --numstat 456544e -- .rn/…/mapping/` → `mapping.csv` は `5 5`、`_batch/batch-13,17,19,21,28.csv` が各 `1 1` | | |
| 8. `verify_glossary.py` が `RESULT: OK` | OK | `.rn/20260724-ntf-yaml-support` をカレントに `$ python3 mapping/tools/verify_glossary.py` → 末尾 `RESULT: OK`（`design_sections 21件/不一致0`・`scheme_names 7件/不一致0`）。是正3-3 で `mapping/glossary.md` §1 の `:18` を書き換えた（免除の範囲を `design.md` 1本から `.rn/` 内の自分たちの文書へ広げ、`steering.md` の `# Rules` の 2026-08-18 の決定を書き写した）のち再実行し、`RESULT: OK`。是正3-4 で同じ `:18` から Rules の逐語2文を落とし、暫定の扱いであることを明記して再実行し、`RESULT: OK` | | |
| 9. `verify_mapping.py` が `OK: no errors` | OK | 同上のカレントで `$ python3 mapping/tools/verify_mapping.py` → 末尾 `OK: no errors` | | |
| 10. `pytest mapping/tools -q` が `183 passed, 96 subtests passed` | OK | 同上のカレントで `$ python3 -m pytest mapping/tools -q` → `183 passed, 96 subtests passed in 0.64s` | | |
| 11. 既存イメージでのフルビルドで警告0。直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` | OK | 下の「Docker フルビルド（完了条件11）」節のとおり。是正3-2 で `-E` を付けて再実行し、`updating environment: 325 added, 0 changed, 0 removed` と `build succeeded.`、`grep -cE 'WARNING:\|ERROR:\|SEVERE:' build.log` → `0` を確認した。是正3-3 でも `-E` 付きで再実行し、`updating environment: 325 added, 0 changed, 0 removed`・`build succeeded.`・`$ grep -cE 'WARNING:\|ERROR:\|SEVERE:' <scratchpad>/build.log` → `0` を確認した。直後に `$ git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行し、生成された `_build/` は docker 内の `rm -rf` で消した（`$ ls -d _build` → `No such file or directory`）。**是正3-4** でも完了条件11 の再確認として同じコマンドを実行し、`updating environment: 325 added, 0 changed, 0 removed`・`build succeeded.`・`$ grep -cE 'WARNING:\|ERROR:\|SEVERE:' build.log` → `0`（`build.log` はリポジトリ外のスクラッチに出力）。直後に `$ git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行し、`_build/` は docker 経由で削除（`$ ls -d _build` → `No such file or directory`） | | |
| 12. 禁止事項に触れていない | OK | `$ git status --porcelain` は変更12ファイル（是正3-2 後も同じ）（`design.md`・`steering.md`・`reviews/page-testdata_converter.md`・`mapping/style.md`・`mapping/glossary.md`・`mapping/mapping.csv`・`mapping/_batch/batch-13,17,19,21,28.csv`・`tools/testdata_converter.rst`）と未追跡の `checks/task-32.md` のみ。`ja/conf.py` は未変更。`mapping/glossary.md` の変更は §5.4「メッセージング方式」の1行のみで §5.15 には触れていない（`$ git diff --numstat 6f828d3 -- …/mapping/glossary.md` → `1 1`。変更行が §5.4 の配下にあることは `$ grep -n '^### 5\.' mapping/glossary.md` で前後の見出し位置を取って確認した）。`mapping.csv` は直接編集せず `_batch/*.csv` からの昇順連結で作り直した。`en/` 配下・`locales/` の `.gitignore` は未変更。是正3-3 の時点で `$ git status --porcelain` は変更3ファイル（`design.md`・`mapping/glossary.md`・`reviews/page-testdata_converter.md`）と未追跡の `checks/task-32.md`、および調整役が別途扱う `steering.md` のみ。`$ git diff --stat 1ccfc53 -- ja/` と `$ git diff --stat 1ccfc53 -- .rn/20260724-ntf-yaml-support/mapping/mapping.csv .rn/20260724-ntf-yaml-support/mapping/_batch/` はいずれも空。`mapping/glossary.md` §5.15 は未変更。**是正3-4 後**は変更3ファイル（`design.md`・`reviews/page-testdata_converter.md`・`mapping/glossary.md`）と未追跡の `checks/task-32.md`、および調整役が編集中の `steering.md`（ステージにもコミットにも含めない）。`$ git diff --stat 6946fa1 -- ja/ mapping/mapping.csv mapping/_batch/` は空 | | |
| 13. 「〜が無い」「すべて」「〜だけ」を書いた文それぞれについて反例走査してから確定したことを記録する | OK | 下の「完了条件13 の走査記録」節に、是正3 の9文と是正3-2 で新しく書いた7文の計16文について、走査コマンドと結果を記載。**是正3-3 で走査の対象を広げた。** 語（「〜が無い」「すべて」「〜だけ」）で網を掛ける方式は、`design.md` 5段落目の「残った動作の記述は、帰属先が表に残したクラスへ移っている。」——主語が無く全称語も含まない一般則——を取りこぼしていた。対象を「主語を明示しない一般則として読める断定文」まで広げ、今回新しく書いた文を1文ずつ走査し直した（下の「是正3-3（レビュー指摘14件）の記録」節の `#17`〜`#25`）。**是正3-4** で `#17`・`#20` の判定が誤りだったことを是正し、走査の手順に「自分の括弧書き・直後の列挙が反例になっていないか」を足した（下の「完了条件13 の走査（是正3-4。E-1〜E-3）」節の `#17`（再）〜`#28`） | | |
| 14. `checks/task-32.md` を staging して `#32` を check-off する | 実装エキスパートは未実施（指示により本ファイルをコミットしない） | 本ファイルは作業ツリーに残す。staging と check-off は調整役が行う | | |

### §4-1 の内容を実測に合わせて変えた点（要相談）

指示書 §4-1 の2点目は「**この7行のうち6行は、落としたクラスの役割が本文に残っていない。**」としていたが、実測すると成り立たない。**そのままは書かず、実測どおりの内容にした。**なお是正3 の1巡目では「6行は残っている／残らないのは1行」と書いたが、これも実測すると誤りだった。是正3-2 で **5行／2行** に直した。

- 消えているのは**クラス名**であって役割ではない。`$ grep -rn 'StandaloneTestSupportTemplate\|HttpServer\|AbstractHttpRequestTestTemplate\|TestShot' ja/development_tools/testing_framework/implementation/request_unit_test/` → 0件（指示書 §4-1 の実測と一致）。
- **役割の一部が本文に残っているのは5行、セルの内容が残っていないのは2行である。** 分類の基準は段落自身が使っているもの（表のセルの文が本文にあるか）を全行に当てた。`mom.rst` の `StandaloneTestSupportTemplate` のセルは「バッチやメッセージング処理などコンテナ外で動作する処理のテスト実行環境を提供する。」の1文だけで、`batch.rst` 側が持つ動作の1文（「テストデータを読み取り、テストショットを1件ずつ実行する。」）を持たない（`$ git show 9031fa6~1:…/mom.rst` の `:81`-`:83` と同 `batch.rst` の `:51`-`:53` を突き合わせて実測）。したがって `AbstractHttpRequestTestTemplate` と同じく「残っていない」側であり、1巡目の6行／1行は誤りだった。
- **残っている5行も、残ったのは役割の一部である。** `batch.rst` の `StandaloneTestSupportTemplate` は動作の1文だけが同 `:17` に残り、位置づけの1文は落ちた。`batch.rst`・`mom.rst` の `TestShot` は実行の側だけが残り、「1件分の情報を保持し」に対応する記述は無い（`$ grep -n '情報を保持\|1件分' …/batch.rst …/mom.rst` → 0件）。`rest.rst`・`web.rst` の `HttpServer` は「内蔵サーバ」という名称が残り、「サーブレットコンテナとして動作する」に対応する記述は無い。ただし `web.rst` はセルの3つ目の要素（「\ HTTP\ レスポンスをファイルへ出力する機能を持つ」）に対応する記述を同 `:44`「内蔵サーバを使用して\ HTML\ ダンプを出力する」として持つため、`rest.rst` と同じ「名称だけ」とは書かなかった。
- **残った動作の記述は、帰属先が表に残したクラスへ移っている。** `batch.rst:17` は直前で「``BatchRequestTestSupport``\ を継承して作成する」と書いており、続く「スーパクラスが…」の指示対象は表に残した `BatchRequestTestSupport` である（`mom.rst:17` も同様）。`9031fa6~1` の同 `mom.rst:22` は同じ動作を `StandaloneTestSupportTemplate` に帰属させていた。この付け替えは `mom.rst:130`-`:131`（`9031fa6~1` では同 `:162`-`:163`）でも起きている。
- したがって指示書 §4-1 の3点目「`:141` 末尾の…この7行には当てはまらないことを明記する」も、そのままでは事実に反する。**7行のうち5行については役割の一部が当てはまり、残り方（クラス名ではなく一般名、かつ帰属先の付け替え）が10行と違う**と書いた。

`:141` の文そのものは書き換えていない（完了条件4 の Evidence のとおり、`$ diff` で1行単位に照合した）。

### 完了条件13 の走査記録（2026-08-21）

今回の変更で全称・限定・排他・不在を主張した文と、確定前に実行した反例走査。`#1`〜`#9` は是正3、`#10`〜`#16` は是正3-2 で新しく書いた文。`ja/` 配下のパスは特記のない限りリポジトリルートからの相対、`.rn/` 内の文書は節見出しで指す。

| # | 書いた文（要旨・掲載先） | 走査コマンド | 結果 | 判定 |
|---|---|---|---|---|
| 1 | 「\ YAML\ 形式から読み込むときは ``rows:``\ の各要素をそのまま扱うため、この整形は行われない。」（`tools/testdata_converter.rst:71`） | `git -C …/nablarch-testing-converter grep -n 'trimTail' e977824 -- src/main/` | ヒット3件（`TestCoreReaderAdapter.java:254`・`:410`・`:464`）。`yaml/YamlFormatReader.java` は0件 | 反例なし |
| 2 | 「converter が落とすのはこの残差である（一般の空エントリは本体が落とす）。」（`reviews/page-testdata_converter.md` §「出典から変えた点」） | `git show e977824:…/xls/XlsFormatReader.java` の `:547-565` を通読。`git grep -n 'dropEmptyEntries' e977824 -- src/main/` | 定義 `:566`、呼び出しは `:162`（`readTableBlocks`）・`:193`（`readListMapBlock`）の2か所。Javadoc `:550-554` が残差である旨を述べている | 反例なし |
| 3 | 「`XlsFormatReader` からの呼び出しはファイル（`:212`）・メッセージ（`:240`）・同期応答電文（`:274`）の3か所である」（`reviews/page-testdata_converter.md` §「出典から変えた点」） | `git grep -n 'readBlockBodyLines' e977824 -- src/main/` | `XlsFormatReader.java` は `:55`（Javadoc）・`:212`・`:240`・`:274`。**`TestCoreReaderAdapter.java:124`（`readListMapColumnNames`）からも呼ばれる**反例を発見 | 反例あり。「3か所」は `XlsFormatReader` からの呼び出しに限定して書き、`:124` の存在と「ファイルとメッセージだけで起きるとは書いていない」ことを同じ文に明記した |
| 4 | 「この7行のクラス名は、`implementation/request_unit_test/` 配下に1件も残っていない」（`design.md` §「利用側ページに内部構造の構成図を置かない」5段落目） | `grep -rn 'StandaloneTestSupportTemplate\|HttpServer\|AbstractHttpRequestTestTemplate\|TestShot' ja/development_tools/testing_framework/implementation/request_unit_test/` | 0件（exit 1） | 反例なし |
| 5 | 「「サーブレットコンテナとして動作する」に対応する記述は本文に無い」（同5段落目） | `grep -rn 'サーブレットコンテナ' ja/development_tools/testing_framework/implementation/request_unit_test/` | `web.rst:48` の1件のみ | 反例1件（`web.rst:48`）。実物を開くとビューテクノロジについての注記で `HttpServer` の説明ではないため、その旨を文中に明記した |
| 6 | 「「実行環境を提供する」に対応する記述は `mom.rst` の本文に無い」（同5段落目） | `grep -rn '実行環境' ja/development_tools/testing_framework/implementation/request_unit_test/`、`grep -n 'ウェブ' mom.rst` | 「実行環境」0件。「ウェブ」は `:35`・`:86`・`:128`・`:131`・`:157` の5件で、うち **`:131`「``BasicHttpRequestTestTemplate``\ ：ウェブアプリケーションのテストで使用する。」は役割の記述である** | 反例1件（`mom.rst:131`）。是正3 の1巡目は「いずれも役割の説明ではない」と断定して取りこぼしていた。実物を開くと `:131` が説明しているのは `BasicHttpRequestTestTemplate` であり、落とした `AbstractHttpRequestTestTemplate` の役割ではない。是正3-2 で段落にこの事実（`9031fa6~1` の同 `:162`-`:163` からサブクラスへの付け替えが起きていること）を書き足した。**是正3-3 で裏付けを補強した。**文字列 `grep` だけでは言い換えを取りこぼすため（この行がまさに1巡目に `mom.rst:131` を取りこぼした実例である）、`grep` に加えて `mom.rst` の全199行を通読した。読んだ範囲と、言い換えの候補として検討した2件の判定は、下の「是正3-3（レビュー指摘14件）の記録」節の「走査 #6 の裏付けの補強」に書いた |
| 7 | 「`batch.rst`・同 `mom.rst` の表はテスト対象クラスの行を持たない（残る4ページは持つ）」（`steering.md` §「#33: 記法の適用順序の明文化、markerColumnColor の説明不足、残置図の禁止語点検、「主なクラスとリソース」の表の載せる側の不揃い」 の (d)） | 6ページの `grep -n '^  \* - '` で表の第1列を全行列挙 | `web.rst:32`・`rest.rst:34`・`component.rst:32`・`entity.rst:32` にテスト対象クラスの行があり、`batch.rst`（`:43`・`:46`・`:49`）と `mom.rst`（`:64`・`:67`・`:70`・`:73`・`:76`・`:79`）には無い | 反例なし |
| 8 | 「基準 (2) を満たすスーパクラスが2つ、`mom.rst` の表に無い」（同 (d)） | `grep -n '^  \* - ' mom.rst` の全行列挙、`grep -n 'BatchRequestTestSupport\|BasicHttpRequestTestTemplate' mom.rst`、`grep -n '^  \* - ' web.rst` | 表の行は `:64`・`:67`・`:70`・`:73`・`:76`・`:79` の6行で、どちらの名前も無い。本文は `:30`・`:130` に `BatchRequestTestSupport`、`:131` に `BasicHttpRequestTestTemplate` を持つ。`BasicHttpRequestTestTemplate` は `web.rst:35` の表にある | 反例なし。指示書 §3 が誤りとした「`mom.rst` の表にスーパクラスが無い」も、`:70`・`:73` の2件が反例であることを再確認した |
| 9 | 「台帳 `current-0282`・`current-0296`・`current-0323` の出典表にも該当行が無い」（同 (d)） | `note` 欄ではなく出典の実物を開いた。`git show 6bf8cfb~1:ja/…/06_TestFWGuide/RequestUnitTest_batch.rst`（`:26-54`）・同 `RequestUnitTest_real.rst`（`:25-62`）・同 `RequestUnitTest_send_sync.rst`（`:39-67`） | 3表とも第1列は「リクエスト単体テストクラス」「Excelファイル（テストデータ）」とクラス名のみで、テスト対象クラスの行は無い | 反例なし |
| 10 | 「表のセルにあった役割のうち一部が本文に残っているのは5行、セルの内容が本文に残っていないのは2行である。」（`design.md` §「利用側ページに内部構造の構成図を置かない」5段落目） | 7行それぞれについて、`git show 9031fa6~1:…` で落としたセルの全文を取り出し、その各文に対応する記述を現在の本文で探した（`grep -n 'テストショット\|情報を保持\|1件分\|内蔵サーバ\|サーブレットコンテナ\|実行環境\|ダンプ' batch.rst mom.rst rest.rst web.rst`） | 残る5行＝`batch.rst` の `StandaloneTestSupportTemplate`・`TestShot`、`mom.rst` の `TestShot`、`rest.rst`・`web.rst` の `HttpServer`。残らない2行＝`mom.rst` の `StandaloneTestSupportTemplate`・`AbstractHttpRequestTestTemplate` | 反例なし。1巡目の「6行／1行」は `mom.rst` の `StandaloneTestSupportTemplate` のセルが `batch.rst` 側と同一だと見なした誤りで、実物では `mom.rst` 側は1文のみだった |
| 11 | 「「1件分の情報を保持し」に対応する記述は無い」（同5段落目） | `grep -n '情報を保持\|1件分' ja/development_tools/testing_framework/implementation/request_unit_test/batch.rst ja/development_tools/testing_framework/implementation/request_unit_test/mom.rst` | 0件（exit 1）。`9031fa6~1` では同 `batch.rst:23`「テストショット1件分の情報を保持する\ ``TestShot``\ を1件ずつ実行する」・同 `mom.rst:22`「1件のテストショットの情報は\ ``TestShot``\ が保持し」として存在した | 反例なし |
| 12 | 「`rest.rst` の `HttpServer` は…「内蔵サーバ」という名称だけが残る」（同5段落目） | `grep -c '内蔵サーバ' rest.rst`（7件）、`grep -c 'サーブレット' rest.rst` | 「内蔵サーバ」7件、「サーブレット」0件。セルの2文目に対応する記述は `rest.rst` に無い | 反例なし。`web.rst` は同じセル構成ではなく3つ目の要素（`HTTP` レスポンスのファイル出力）を持ち、それに対応する記述が同 `:44` にあるため、`web.rst` は「名称だけ」と書かず別に記述した |
| 13 | 「同 `:130`-`:131` は…`BatchRequestTestSupport`・`BasicHttpRequestTestTemplate` を挙げるが、`9031fa6~1` の同じ箇所（同 `:162`-`:163`）は `StandaloneTestSupportTemplate`・`AbstractHttpRequestTestTemplate` を挙げていた」（同5段落目） | `sed -n '128,131p' mom.rst` と `git show 9031fa6~1:…/mom.rst \| sed -n '160,163p'` | 導入文（「次のどちらかのスーパクラスを継承する。」）は同一で、箇条書き2件のクラス名だけがサブクラスへ入れ替わっている | 反例なし |
| 14 | 「表の採否基準を当てて落とした名前が計11件」「同じマーカーの配下には `9031fa6` が落とした行の名前も書いてあるが、それはこの11件に含まない」（`design.md` §「利用側ページに内部構造の構成図を置かない」3段落目） | `grep -o '【#32・2026-08-21】[^"]*' mapping/mapping.csv` で `note` の全マーカー配下を列挙し、採否基準を当てて落とした名前を数え直した | 採否基準の適用は5行（`current-0201` 3件・`current-0282` 3件・`current-0296` 3件・`current-0309` 1件・`current-0323` 1件）で計11件。同じマーカーの配下にある「なお同じ基準で 9031fa6 が…落としている」の名前は別勘定 | 反例なし。1巡目は「記録された、落としたクラスの名前が計11件」と書いており、`9031fa6` 分の追記後は数え方が定まらなくなっていたため、数える対象を限定する語を足した（数そのものは変えていない） |
| 15 | 「`mom.rst` の表にあるスーパクラスは `MessagingRequestTestSupport`…と `MessagingReceiveTestSupport`…の2つ」（`steering.md` §「#33: 記法の適用順序の明文化、markerColumnColor の説明不足、残置図の禁止語点検、「主なクラスとリソース」の表の載せる側の不揃い」 の (d)） | `grep -n '^  \* - ' mom.rst` | `:61`（見出し行）・`:64`・`:67`・`:70`・`:73`・`:76`・`:79` の7件。データ行は6行 | 反例なし。ただし1巡目の「表にあるのは…の2つ」は主語が無く、表全体が2行しか無いと読める。是正3-2 で「表にあるスーパクラスは」と主語を補い、データ行が6行であることを併記した |
| 16 | 「`BasicHttpRequestTestTemplate` は `web.rst:35` の表にはあるが、…`mom.rst` 側は独立に未処理である」（同 (d)） | `grep -n '^  \* - ' web.rst` と `grep -n 'BasicHttpRequestTestTemplate' mom.rst web.rst` | `web.rst:35` が表の行。`mom.rst` は `:131` の本文のみ。判定をページ単位とする根拠は `design.md` §「利用側ページに内部構造の構成図を置かない」2段落目「判定はページ単位で行う」 | 反例なし |

### `XlsFormatReader.java` の照合記録（コミット `e977824`、2026-08-21）

`git -C /home/tie303177/work/nablarch/nablarch-testing-converter show e977824:src/main/java/nablarch/test/tool/converter/xls/XlsFormatReader.java` を `grep -n ''` に通して行番号付きで開き、指示書 §2 の逐語と突き合わせた。

- **指示書 §2 の「`:551-555` 逐語」は行番号が1つずれている。** 引用文の先頭「{@code notation:1535}「全要素が null または空文字のエントリは読み飛ばされる」を、」は `:550`、末尾「残ってしまう。」は `:554` にある。`:555` は「カラム名とデータ行を持つ構成である）なので、ここで落とす。」で引用に含まれない。**`reviews/` には実測どおり `:550-554` と書いた。**
- `:566` は `private static List<List<String>> dropEmptyEntries(List<List<String>> rows) {` で、指示書のとおり。呼び出しは `:162`（`readTableBlocks`）・`:193`（`readListMapBlock`）の2か所。
- あわせて `src/main/java/nablarch/test/core/reader/TestCoreReaderAdapter.java` も開き、`:264` `readBlockBodyLines`、`:410` `BodyLineCollector` の Javadoc、`:464` `bodyLines.add(NablarchTestUtils.trimTailCopy(line));` を確認した。

### Docker フルビルド（完了条件11）

既存イメージ `nablarch-document-build` を使用（`docker build` からのイメージ再作成は `#34` へ分離済みのため実施していない）。

**是正3 の1巡目は `-E` も `-a` も付けずに実行しており、`_build/.doctrees` が残っていればソースを1ファイルも読まずに `build succeeded.`・警告0 になる。フルビルドの証跡になっていなかった。是正3-2 で `-E` を付けて実行し直した。** 以下は再実行のログ本文（`build.log` はリポジトリ外の scratchpad に置いた）。

```
$ docker run --rm -v /home/tie303177/work/nablarch/nablarch-document:/root/document \
    nablarch-document-build /bin/bash -c \
    "cd /root/document; sphinx-build -E -d _build/.doctrees/ja -b html ja _build/html" 2>&1 | tee <scratchpad>/build.log
Running Sphinx v1.3.6
loading translations [ja]... done
building [mo]: targets for 0 po files that are out of date
building [html]: targets for 325 source files that are out of date
updating environment: 325 added, 0 changed, 0 removed
reading sources... [  0%] about_nablarch/concept
…
copying static files... done
copying extra files... done
dumping search index in Japanese (code: ja) ... done
dumping object inventory... done
build succeeded.

$ grep -cE 'WARNING:|ERROR:|SEVERE:' <scratchpad>/build.log
0

$ git checkout -- locales/ja/LC_MESSAGES/sphinx.mo
```

`updating environment: 325 added` が全325ファイルを読み直したことを示す（1巡目のログにこの行は無い）。ビルド後の `git status --porcelain` に `locales/ja/LC_MESSAGES/sphinx.mo` は現れず（今回の再実行では `.mo` が書き換わらなかったが、指示どおり `git checkout` は実行した）、生成された `_build/`（55MB、docker が root 所有で作るためホストからは消せない）は同じイメージのコンテナ内から `rm -rf` して消した。`_build/` は `.gitignore:2` で除外されている。

### Method（是正3 で自分で確かめたこと）

- **指示書の逐語をそのまま信用せず、実物を `git show` で開いて行番号ごと突き合わせた。** その結果、指示書 §2 の `:551-555` が実測 `:550-554` であること、§4-1 の「6行は役割が本文に残っていない」が成り立たないことの2件を見つけ、いずれも実測どおりに書いた。**是正3-2 では、自分が1巡目に書いた「6行／1行」も同じやり方で潰し、`git show 9031fa6~1` のセル全文を7行分すべて取り出して 5行／2行 に直した。**
- **`9031fa6` の7行は `git show 9031fa6~1` と `git show 9031fa6` の表を突き合わせて自分で数えた。** `batch.rst` 2行・`mom.rst` 3行・`rest.rst` 1行・`web.rst` 1行の計7行で、指示書 §4 の内訳と一致する。
- **台帳の根拠は `note` 欄ではなく出典の実物で確かめた。** `guide/` 配下の現行解説書は `6bf8cfb` で削除済みのため `6bf8cfb~1` から取り出して読んだ。
- **編集はすべて Python で `s.count(old) == 1` を assert してから適用した。** `mapping.csv` は直接編集せず `_batch/*.csv` を直してから昇順連結で作り直し、`456544e` との全597行・全14列の突き合わせで `note` 5件以外に差分が無いことを確認した。
- **`design.md` の変更は同節の3段落目と5段落目の2行だけ**で（`$ git diff --numstat 6f828d3 -- …/design.md` → `3 1`）、`:141` を含む2段落目は `diff` で1行単位に照合して未変更であることを確かめた。
- **是正3-2 では、`.rn/` 内の文書を行番号で指していた本節の記述をすべて節見出し方式に直した。** `steering.md` `# Rules` の相互参照規約に従う。`ja/` と参照リポジトリの実物を指す `file:line` はそのまま残した。

### 是正3-3（レビュー指摘14件）の記録（2026-08-21）

`1ccfc53` の作業ツリーに対する是正ラウンド2。指摘14件の内訳は `design.md` 8件（A-1〜A-9 のうち A-1 が事実の誤り）・`reviews/page-testdata_converter.md` 2件・`mapping/glossary.md` 1件・本ファイル 3件（D-1〜D-3。D-4 は反映作業）。触ったのは `design.md` の新段落1行・`reviews/page-testdata_converter.md` の1行・`mapping/glossary.md` の `:18`・本ファイルだけで、`ja/` 配下と `steering.md`・`mapping/mapping.csv`・`mapping/_batch/` は1文字も触っていない。

#### `design.md` §「利用側ページに内部構造の構成図を置かない」の新段落

- **A-1（事実の誤り）** 「残った動作の記述は、帰属先が表に残したクラスへ移っている。」を削った。反例2件を自分で確かめた。(a) 同じ段落が挙げた `web.rst:44`「内蔵サーバを使用して\ HTML\ ダンプを出力する」が名指しするのは「内蔵サーバ」という一般名で、`web.rst` の表にこの機能を帰属させたクラスは無い（`$ grep -n '^  \* - ' ja/development_tools/testing_framework/implementation/request_unit_test/web.rst` → `:23` が見出し行、データ行は `:26`・`:29`・`:32`・`:35`・`:38` で `HttpServer` を継ぐ行が無い）。(b) 根拠に引いていた `9031fa6~1` の `mom.rst:22` の逐語の主語は `MessagingRequestTestSupport` であり、このクラスは `9031fa6` の前後とも表にある（旧 `:87`／新 `:70`。`$ git show 9031fa6~1:….rst \| grep -n '^  \* - '` と `$ git show 9031fa6:….rst \| grep -n '^  \* - '` で確認）。つまり `mom.rst` では「移った」という変化自体が起きていない。(c) `batch.rst` 側（`$ git show 9031fa6~1:….../batch.rst \| sed -n '23p'`）の第2文「テストデータを読み取り、テストショット1件分の情報を保持する ``TestShot``\ を1件ずつ実行する。」は主語が明示されておらず、落とした側への帰属とは読めない。代わりに、(1) と (3) の中で `batch.rst:17`・`mom.rst:17` の「スーパクラス」の指示対象が表に残したクラスであることを、行ごとに主語つきで書いた。新しい断定文は作っていない。
- **A-2** `(1)`〜`(5)` のラベルを振り、読者が5を数えられるようにした。同節の4類型の段落（`(A)…6行` `(B)…1行` `(C)…2行` `(D)…1行`）と同じ型。段落は1つのまま。
- **A-3** 太字を冒頭の1文だけにした（`**` の対を数えて 4→1。同節の他9段落は各1）。
- **A-4** 5点を削った。(i) 「パスは `ja/development_tools/testing_framework/` からの相対。」（`$ grep -n 'からの相対' design.md` → 同節の `:145`・`:151` が同じ宣言を持つ）、(ii) 「テストショット」の語の分布、(iii) `9031fa6~1` の `mom.rst:22` の逐語、(iv) `mom.rst` の `StandaloneTestSupportTemplate` のセルの再引用、(v) 末尾の `:128` の文。
- **A-5** 単位を「行」と明記し、列挙を先頭3行にそろえた。自分で数え直した結果は `$ grep -c '内蔵サーバ' …/rest.rst` → `7`、同 `…/web.rst` → `7`。`rest.rst` は出現数が9・行数が7で単位が食い違うため、行数に統一した。列挙は `rest.rst` が `:10`・`:15`・`:17`、`web.rst` が `:10`・`:42`・`:44`。
- **A-6** 一般名を行ごとに書き分けた（(1)「スーパクラス」、(2) と (3)「テストショット」、(4) と (5)「内蔵サーバ」）。「残っている5行も、残るのは」の同語の重なりも解消した。
- **A-7** 段落序数の指し2件（「本節の4段落目」「本節の2段落目」）を内容指し（「本節の「落とした10行を実態から分類すると」の段落」「本節の採否基準の段落」）に替えた。新段落に `段落目` は0件。参照先の文言は `design.md` の実物で確認した。
- **A-8** 台帳の名前8件と7行のずれを、同節3段落目と同じ括弧書きの形で解消した。`mapping.csv` の `note` を自分で読み直して数えた結果は `current-0201` 1件・`current-0282` 2件・`current-0296` 2件・`current-0309` 1件・`current-0323` 2件の計8件。`mom.rst` の表は1つで、落ちたのは `9031fa6~1` の `:81`（`StandaloneTestSupportTemplate`）・`:84`（`AbstractHttpRequestTestTemplate`）・`:93`（`TestShot`）の3行。出典が `current-0296`（現行 `06_TestFWGuide/RequestUnitTest_real.rst`、メッセージ受信処理）と `current-0323`（同 `RequestUnitTest_send_sync.rst`、同期応答メッセージ送信処理）の2表に分かれているため、`StandaloneTestSupportTemplate` が両方の `note` に入る。
- **A-9** 規範違反2行の処置を書いた。前後関係は自分で確かめた。`$ git log --format='%h %ad %s' --date=iso -S'落としたクラスの役割は、各ページのリード文または本文に残す。' -- .rn/20260724-ntf-yaml-support/design.md` の最古が `5c2c26f`（2026-08-21 13:50:02 +0900、`#32` の是正2）、`$ git log --format='%h %ad %s' --date=iso -1 9031fa6` が 2026-08-21 10:04:52 +0900。したがって `9031fa6` は規範の明文化より前である。7行は明文化前の判断であり、規範を遡って当てるかどうかは別の判断であることを書き、判断は `steering.md` の `#33` へ送ると明記した（`#33` への追記は調整役が行う。本ラウンドでは `steering.md` を触っていない）。

#### `reviews/page-testdata_converter.md`

- **B-1** 「行末の空セルの除去」行の「ページの記述」列を229字から65字に縮め、混ざっていた理由（「…としているため」）と日付スタンプを「変えた理由」列の末尾へ移した。同表の「ページの記述」列12セルの長さを実測すると、見出しを除き 10〜82字で、本行だけが突出していた。移動後は 65字で範囲内。
- **B-2** 適用範囲の根拠に NTF 本体側の実測を足した。`$ git grep -n 'trimTailCopy' e21bf67 -- src/main/`（`nablarch-testing`）→ `NablarchTestUtils.java:273`（定義）・`DataFileParser.java:68`・`HeaderLine.java:33`。`HeaderLine.java:33` は `List<String> keys = trimTailCopy(headerLine);` で、コンストラクタの先頭でヘッダ行に当たる。`$ git grep -ln HeaderLine e21bf67 -- src/main/` → `HeaderLine.java`・`ListMapParser.java`・`TableDataParser.java` の3ファイル。生成箇所は `ListMapParser.java:64` `header = new HeaderLine(firstLine);` と `TableDataParser.java:93` `header = new HeaderLine(readLine());`。したがってテーブル系と `LIST_MAP` のカラム名行でも行末の空セルは詰められ、行末の空セルの除去はファイル・メッセージに閉じない。逐語はすべて `git show` で開いて照合した。

#### `mapping/glossary.md` §1（`:18`）

- **C-1** 免除の範囲を `design.md` 1本から `.rn/` 内の自分たちの文書へ広げ、`steering.md` の `# Rules` が 2026-08-18 に定めた文（「`.rn/` 内の文書どうしの相互参照は、行番号ではなく節見出し（`ファイル名` §番号「見出し」）で指す。`ja/` や他リポジトリの実物を出典として示す `file:line` は対象外で、そのまま使う。」）と、その区別の基準（「指す先が `.rn/` 内の自分たちの文書か、実物か」）を書き写した。**ここで「`input/` 配下の出典資料と、受領後に書き換えていない作業指示は実物の側」とした線引きは、Rules の書き写しではなく `#32` での拡張である**（Rules は `.rn/` 内の文書どうしの相互参照を節見出しで指すと述べるだけで、作業指示を例外にしていない。`ntf-doc-*.md` は `.rn/` 内の文書である）。是正3-4 で、確定した規約ではなく `#32` 時点の暫定の扱いであることが分かる書き方に改め、`.rn/` 全体の規約として追認するかは `steering.md` の `#33` (e-1) で決めると明記した（`ntf-doc-terminology.md` は `$ git log --oneline --follow` が受領コミット `11ec3a1` の1件のみ）。§5.15 は触っていない。`$ python3 mapping/tools/verify_glossary.py` → `RESULT: OK`。

#### 走査 #6 の裏付けの補強（D-3）

走査 #6「「実行環境を提供する」に対応する記述は `mom.rst` の本文に無い」は、是正3-2 まで文字列 `grep` だけを裏付けにしていた。逐語 `grep` は言い換えを取りこぼす（この行自体が1巡目に `mom.rst:131` を取りこぼした実例）。2026-08-21、`$ grep -rn '実行環境' ja/development_tools/testing_framework/implementation/request_unit_test/` が0件（exit 1）であることに加えて、`mom.rst` の全199行を通読した。読んだ範囲は、リード文 `:10`、「機能概要」`:12`-`:81`（表 `:57`-`:80` を含む）、「使用方法」`:83`-`:199` の全体である。言い換えの候補として検討したのは2件。`:10`「いずれもテスティングフレームワークが提供するスーパクラスとテストデータを使うことで、テストコードをほとんど書かずにテストを実施できる。」は、表に残したスーパクラス（`MessagingRequestTestSupport`・`MessagingReceiveTestSupport`）を一般名で指す記述である。`:131`「ウェブアプリケーションのテストで使用する。」は、残ったサブクラス `BasicHttpRequestTestTemplate` の用途である。表の `:70`-`:79` が使う「…機能を提供する。」も、いずれも表に残したクラスについての記述である。どれも落とした `StandaloneTestSupportTemplate`・`AbstractHttpRequestTestTemplate` の役割の説明ではない。

#### 完了条件13 の走査（対象を広げて再実施。D-2）

走査の対象を「「〜が無い」「すべて」「〜だけ」等の語を含む文」から「主語を明示しない一般則として読める断定文」まで広げた。是正3-2 までの語ベースの走査は、`design.md` 5段落目の「残った動作の記述は、帰属先が表に残したクラスへ移っている。」を取りこぼしていた。この文は全称語を含まず、主語も無く、語では引っかからない。今回は新しく書いた文（`design.md` の新段落・`reviews/page-testdata_converter.md` の第3列と第4列・`mapping/glossary.md` `:18`）を1文ずつ読み、主語の有無と適用範囲を判定した。**主語を明示しない断定文は0件である。**下表の9文はいずれも「この7行」「この5行」「(5) の…文」「`HttpServer` の2行」「この2クラス」のように範囲を主語で限定している。

| # | 書いた文（要旨・掲載先） | 主語 | 走査・裏付け | 判定 |
|---|---|---|---|---|
| 17 | 「マッピング台帳の `note` にこの7行の名前は8件現れるが、`mom.rst` の表は1つで、落ちたのは…3行である。」（`design.md` §「利用側ページに内部構造の構成図を置かない」5段落目） | 台帳の `note` ／ `mom.rst` の表 | `mapping.csv` の該当5行の `note` を `csv.DictReader` で読み出して名前を数え、`git show 9031fa6~1` と `git show 9031fa6` の `mom.rst` の表の行を突き合わせた | **是正3-4 で是正。この判定は誤り**（下の「完了条件13 の走査（是正3-4。E-1〜E-3）」の `#17`（再）を参照）。文が言っている数え方では8件にならない |
| 18 | 「この7行のクラス名は、`implementation/request_unit_test/` 配下に1件も残っていない」（同5段落目） | この7行のクラス名 | `grep -rn 'StandaloneTestSupportTemplate\|HttpServer\|AbstractHttpRequestTestTemplate\|TestShot' ja/development_tools/testing_framework/implementation/request_unit_test/` を再実行 | 反例なし（0件、exit 1） |
| 19 | 「表のセルにあった役割の一部が本文に残っているのは次の5行である。」（同5段落目） | 「…のは」で5行に限定し、`(1)`〜`(5)` で列挙 | 7行それぞれのセル全文（`git show 9031fa6~1`）と現在の本文を突き合わせ。走査 #10 の判定を再確認した | 反例なし |
| 20 | 「この5行で本文に残っているのはクラス名ではなく一般名であり、その一般名は行ごとに違う」（同5段落目） | この5行 | クラス名が0件であること（#18）に加え、行ごとに残った一般名を特定した。(1)「スーパクラス」（`batch.rst:17`）、(2)(3)「テストショット」（同 `:17`・`mom.rst:17`）、(4)(5)「内蔵サーバ」（`rest.rst`・`web.rst` 各7行） | **是正3-4 で是正。この判定は誤り**（下の「完了条件13 の走査（是正3-4。E-1〜E-3）」の `#20`（再）を参照）。同じ文の括弧書きが反例だった |
| 21 | 「(5) の出力機能の文が名指しするのも「内蔵サーバ」という一般名であって、表に残したクラスではない。」（同5段落目） | (5) の出力機能の文 | `web.rst:44` を開いて名指し先を確認。`grep -n '^  \* - ' …/web.rst` で表のデータ行が `:26`・`:29`・`:32`・`:35`・`:38` であることを確認 | 反例なし。この確認が A-1 の削除の根拠 |
| 22 | 「`HttpServer` の2行に共通して、「サーブレットコンテナとして動作する」に対応する記述は本文に無い」（同5段落目） | `HttpServer` の2行 | `grep -rn 'サーブレットコンテナ' ja/development_tools/testing_framework/implementation/request_unit_test/` を再実行 → `web.rst:48` の1件 | 反例1件を実物で確認。ビューテクノロジについての注記であり `HttpServer` の説明ではないため、括弧内にその旨を明記して残した |
| 23 | 「この2クラスについても帰属先の付け替えは起きている。」（同5段落目） | この2クラス（`mom.rst` の `StandaloneTestSupportTemplate`・`AbstractHttpRequestTestTemplate`） | `sed -n '126,132p' …/mom.rst` と `git show 9031fa6~1:…/mom.rst \| sed -n '158,164p'` | 反例なし。導入文は同一で、箇条書き2件のクラス名だけがサブクラスへ入れ替わっている |
| 24 | 「ただし NTF 本体側では、行末の空セルの除去はファイル・メッセージに閉じない。」（`reviews/page-testdata_converter.md` §「出典から変えた点」） | 行末の空セルの除去 | `git grep -n 'trimTailCopy' e21bf67 -- src/main/`、`git grep -ln HeaderLine e21bf67 -- src/main/`、`HeaderLine.java:33`・`ListMapParser.java:64`・`TableDataParser.java:93` の逐語を `git show` で確認 | 反例なし。文は是正3-4 で書き直した（「全般」が過剰主張だった。下の「完了条件13 の走査（是正3-4。E-1〜E-3）」の `#27`） |
| 25 | 「`input/` 配下の出典資料と、受領後に書き換えていない作業指示は実物の側であり、`file:line` のまま指す。」（`mapping/glossary.md` §1） | `input/` 配下の出典資料と作業指示 | `steering.md` の `# Rules` が示す区別の基準（「指す先が `.rn/` 内の自分たちの文書か、実物か」）を実物で確認。`ntf-doc-terminology.md` は `git log --oneline --follow` が受領コミット `11ec3a1` の1件のみで、受領後に書き換えていない | 反例なし。文は是正3-4 で書き直した（Rules の書き写しではなく拡張だった。下の「完了条件13 の走査（是正3-4。E-1〜E-3）」の `#28`） |

#### 完了条件13 の走査（是正3-4。E-1〜E-3）

**走査の手順に1つ足した（E-3）。** 文の外を探すだけでなく、**その文自身の括弧書きと直後の列挙が、その文の反例になっていないか**を確かめる。是正3-4 で判定を是正した2件（`#17`・`#20`）は、どちらも反例が同じ文の中にあり、外向きの走査では出なかった。あわせて、件数を書いた文は**何を母集団として数えたかが文の中で限定されているか**を確かめる（`#17` はこの限定を欠いていた）。

| # | 書いた文（要旨・掲載先） | 走査・裏付け | 判定 |
|---|---|---|---|
| 17（再） | 「マッピング台帳の `note` 末尾に `9031fa6` の分として書き足した「なお同じ基準で…落としている」の一文だけを数えると、この7行の名前は8件現れる」（`design.md` §「利用側ページに内部構造の構成図を置かない」5段落目） | `csv.DictReader` で `mapping.csv` の `note` 列を読み、4クラス名（`StandaloneTestSupportTemplate`・`AbstractHttpRequestTestTemplate`・`TestShot`・`HttpServer`）の出現を数え直した。`note` 列全体で45件（23行）、書き足した `current-0201`・`current-0282`・`current-0296`・`current-0309`・`current-0323` の5行の `note` 全体で19件、`なお同じ基準で` で始まる一文に限ると8件 | **是正3-3 の判定「反例なし（8件／3行を再現）」は誤り。**再現したのは書き手が意図した数え方であって、文が字義どおりに言っている数え方ではない。母集団を `note` 列全体とすれば45件、5行の `note` としても19件で、8件にはならない。限定語（数える一文と5行の明示）を足した現行文で走査し直し、反例なし |
| 20（再） | 「その一般名は「スーパクラス」（(1)）・「テストショット」（(2) と (3)）・「内蔵サーバ」（(4) と (5)）の3種である」（同5段落目） | 同じ文の括弧書きを反例として当てた。(2) と (3)、(4) と (5) はそれぞれ同じ語であり、5行で3種である | **是正3-3 の判定「反例なし」は誤り。**旧文「その一般名は行ごとに違う」の反例は、同じ文の括弧書きそのものだった。「3種である」に書き換えて走査し直し、反例なし |
| 26 | 「(4)…「内蔵サーバ」という名称だけが残る（同ファイルの7行に現れる…）」「(5)…名称（同ファイルの7行に現れる…）」（同5段落目） | `$ grep -c '内蔵サーバ'` が `rest.rst` 7・`web.rst` 7。`$ grep -o '内蔵サーバ'` の出現数は `rest.rst` 9・`web.rst` 7 | 反例なし。旧文の「計7行」は、同じ段落の「10行」「7行」「5行」「2行」（いずれも表の行）と単位が違い、表の行と読めた。「同ファイルの7行」と単位を明示した。`rest.rst` は1行に2回現れる行があるため出現数9・行数7 |
| 27 | 「`HeaderLine.java:33` `List<String> keys = trimTailCopy(headerLine);` が、テーブル系（同 `TableDataParser.java:93`）と `LIST_MAP`（同 `ListMapParser.java:64`）のカラム名行でも走る。」（`reviews/page-testdata_converter.md` §「出典から変えた点」） | `$ git grep -ln HeaderLine e21bf67 -- src/main/` → `HeaderLine.java`・`ListMapParser.java`・`TableDataParser.java` の3ファイル。`$ git grep -n 'trimTailCopy' e21bf67 -- src/main/` → `NablarchTestUtils.java:273`（定義）・`DataFileParser.java:68`・`HeaderLine.java:33`。いずれも `nablarch-testing@e21bf67` を `git show` で開いて照合 | **`#24` の旧文「ヘッダ行を持つブロック全般で走り」は反例あり。**`HeaderLine` を生成するのはこの2か所だけで、ファイル系のフィールド名称行は `HeaderLine` を通らず `DataFileParser.java:68` の別経路で `trimTailCopy` が当たる。範囲をこの2つに限定した現行文で走査し直し、反例なし。結論（テーブル系と `LIST_MAP` のカラム名行でも詰められる）は変えていない |
| 28 | 「`input/` 配下の出典資料と、受領後に書き換えていない作業指示を実物の側として `file:line` のまま指すのは `#32` 時点の暫定の扱いで、`.rn/` 全体の規約として追認するかは `steering.md` の `#33` (e-1) で決める。」（`mapping/glossary.md` §1） | `steering.md` の `# Rules` を開き直した。Rules は `.rn/` 内の文書どうしの相互参照を節見出しで指すと述べるだけで、作業指示を例外にしていない。`ntf-doc-*.md` は `.rn/` 内の文書である。`steering.md` の `#33` (e-1) も、この線引きを `.rn/` 全体の規約として追認するかどうかを未決としている | **`#25` の旧文「…実物の側であり、`file:line` のまま指す。」は Rules の書き写しではなく `#32` での拡張だった。**確定した規約と読めない書き方に改めた。反例なし |

## Overall Verdict（是正3）

- Self-check: OK（完了条件1〜13 を実行して全 OK。14 は指示により調整役へ引き継ぐ。是正3-2 でレビュー指摘17件を反映し、そのうち自分の誤り3件——`design.md` 5段落目の「6行／1行」（正しくは 5行／2行）、走査記録 `#6` の取りこぼし（`mom.rst:131`）、完了条件11 の証跡が `-E` 無しでフルビルドを立証していなかった点——を実測で潰した。指示書 §4-1 の内訳は指示の文言ではなく実測どおりの内容にしてある。上の「§4-1 の内容を実測に合わせて変えた点」を参照。是正3-3 でさらにレビュー指摘14件を反映し、そのうち自分の事実誤り1件——`design.md` 5段落目の「残った動作の記述は、帰属先が表に残したクラスへ移っている。」——を反例2件の実測により削除した。この文は主語が無く全称語も含まないため語ベースの走査をすり抜けていたので、完了条件13 の走査対象を「主語を明示しない一般則として読める断定文」まで広げ、今回書いた文9件を走査し直した（主語を明示しない断定文は0件）。完了条件6 の grep がベアファイル名の `.rn/` 内参照を拾わないことも Evidence に明記した。内訳は下の「是正3-3（レビュー指摘14件）の記録」節を参照） 是正3-4 でさらにレビュー指摘10件（A-1〜A-4・B-1・C-1〜C-4・D-1〜D-2・E-1〜E-4）を反映した。そのうち自分の判定の誤り2件——走査記録 `#17`（文が字義どおりに言っている数え方ではなく、書き手が意図した数え方で走査していた。母集団は `note` 列全体で45件・対象5行で19件）と `#20`（同じ文の括弧書きが反例だった。一般名は5行で3種）——を是正し、走査の手順に「自分の括弧書き・直後の列挙が、その文の反例になっていないか」を足した。`reviews/page-testdata_converter.md` の表の破れ2件（閉じパイプの欠落・コードスパン中のパイプ）も直し、全表の全行が同じセル数であることをスクリプトで確かめた。内訳は上の「完了条件13 の走査（是正3-4。E-1〜E-3）」節を参照。

## 4観点レビューの判定（是正3。調整役が記入。2026-08-21）

実装エキスパートはこの節を書かない。以下は調整役が収集した各観点の判定と、その triage の結果である。

### ラウンド構成

| ラウンド | 対象 | QA | 設計 | クラフト | 検証 |
|---|---|---|---|---|---|
| 1回目 | `4d0a48a` | pass（条件付き） | fail | fail | pass（条件付き） |
| 2回目（是正1） | `1ccfc53` ＋ 未コミットの `steering.md`・`checks/task-32.md` | 実施せず（1回目 pass、変更は fail 2観点と検証観点の指摘由来） | fail | fail | pass（条件付き） |
| 3回目（是正2） | `6946fa1` ＋ 未コミットの `steering.md`・`checks/task-32.md` | — | — | — | — |

是正は `task-verify-workflow.md` の上限3回のうち2回を使った（`1ccfc53`・`6946fa1`）。

### QA Expert Review

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Verification approach meaningful to the objective | OK | 完了条件1〜13 を独立に再現。加えて完了条件そのものの穴を2件指摘した。(1) 完了条件13 の走査が「〜が無い」「すべて」「〜だけ」という**語**で切られているため、肯定形の範囲限定（「ファイルとメッセージのテストデータでは」）が対象から外れた。(2) 完了条件6 が `mapping/` の3ファイルに限定されているため、`.rn/` 全体の行番号参照は残る。どちらも是正3-3 で Evidence と走査記録に反映し、`#33` (e-1) へ送った |

### Expert Reviews

#### Design Expert

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Approach/structure fits | OK（是正後） | 1回目・2回目とも fail。7行の内訳を `design.md` に置き台帳の `note` からポインタで指す approach 自体は妥当と判定された。2回目に、規範違反2行の処置が決まっていない点（F3）と、`steering.md` `#32` の是正3 Steps に置いた8行の理由づけが Rules「詳細な理由づけは1箇所、他は1〜2行のポインタ」に反する点（F4）を指摘。前者は `design.md` に事実を書いたうえで `#33` (e-2) へ、後者は調整役が1〜2行に圧縮して是正 |
| System-wide integrity | OK（是正後） | 2回目に、`steering.md` の是正3ブロックが存在しない節 §「4観点レビューの判定（是正3）」を2回指している点（F1）を指摘。本節を起こすことで解消した。台帳の名前8件と7行のずれ（F5）は `design.md` の括弧書きで解消。段落序数指し（F6）は内容指しに置換 |

#### Craft Expert（writing）

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Medium-specific best practice | OK（是正後） | 1回目・2回目とも fail。2回目の指摘のうち、`design.md` 5段落目で「5行」を読者が数えられない点（列挙が4文）・強調が同節で1段落だけ4スパンである点・約400字が削れる点・「計7件」の単位が再現できない点を是正。`(1)`〜`(5)` のラベルは同節の4類型の段落と同じ型にそろえた |
| Consistency with existing style | OK（是正後） | `reviews/page-testdata_converter.md` の「ページの記述」列が229字（同列の他11セルは10〜82字）で、かつ理由と日付スタンプという右隣の列の内容を抱えていた点を是正（65字）。`mapping/style.md` §「クラス名の表記」の規約（`#28` 確定）の3件——全角括弧直後の半角空白、引用の非逐語（「コードリテラル」→ 実文 `` ``literal`` ``）、鉤括弧の連続——も是正。`steering.md` のダッシュの割れは調整役が既存 Steps の形にそろえた |

#### Verification Expert（fact-check）

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Artifact actually checked | OK | 1回目・2回目とも、照合した約60件の `file:line`・逐語・grep 件数・コミット差分の内訳・台帳の全597行×14列がすべて独立に再現した。2回目に事実の誤り1件を検出（下記） |
| Coverage | OK（是正後） | 2回目に「残った動作の記述は、帰属先が表に残したクラスへ移っている。」が全称の主張でありながら全称語を含まないため、完了条件13 の語ベースの走査をすり抜けたことを指摘。反例2件（`web.rst:44` の帰属先が一般名であること、根拠に引いた `9031fa6~1` の `mom.rst:22` の主語が表に残るクラスであること）を実測で示した。是正3-3 で当該文を削除し、走査対象を「主語を明示しない一般則として読める断定文」まで広げた |

### Triage の結果

- **Valid → 是正した**: 1回目17件（`1ccfc53`）、2回目14件（`6946fa1` ＋ 調整役による `steering.md` の是正）。計31件
- **Invalid → 却下した**: 4件
  - クラフト3回目「`reviews/page-testdata_converter.md:59`・`:161` の `\|` も `:88` と同じ形に揃える」—— 採らない。GFM では表のセル内の `\|` は正しいエスケープであり、セル区切りにならない。実際、この2行を含めて同ファイルの全表がセル数のそろった状態である（GFM のエスケープ規則で判定するスクリプトで実測。`:77`〜`:89` の13行がすべて4セル）。`:88` を2つのコードスパンに分けたのは指摘に沿った措置だが、必要ではなかった
  - クラフト3回目「`design.md` 5段落目をさらに約400字削る」—— 一部のみ採った。指摘のうち2か所（重複した1文と末尾の重複2文）は削ったが、同じラウンドの過剰主張の指摘（件数の限定語欠落）を直すために母集団の限定と実測値を書き足す必要があり、正味では 3652字→3722字 と増えた。作業指示 `ntf-doc-32-fix3.md` §4-1 が段落の分割を禁じているため、分量と限定の精度が二律背反になっている。分量は `#32` では下げきらないと判断した
  - 設計1回目 F4「`design.md` の新段落を `:149` の後へ移す」—— 作業指示 `ntf-doc-32-fix3.md` §4-1 が挿入位置を「`:145`（4類型の段落）と `:147` の間」と定めている。完了条件4 の scope boundary の内側であるため採らない
  - クラフト1回目 指摘7「`design.md` の新段落を3段落に割る」—— 同 §4-1 が「1段落足す」と定めている。同じ理由で採らない。長さは削除で下げる方向のみ採った
- **`#33` へ送った**: 4件（(d) は指示書 §3 による。(e-1)〜(e-3) は本ラウンドのレビュー由来）
  - **(e-1)** `.rn/` 内の相互参照の節見出し化が3ファイルで止まっている（生きている文書だけで、ディレクトリ接頭辞付き141件・ベアファイル名271件が残る。完了条件6 の grep は後者を拾わない）。`mapping/glossary.md` §1 が `#32` の是正3 で置いた「`input/` 配下と受領後未編集の作業指示は実物の側」という暫定の線引きを追認するかどうかも含む
  - **(e-2)** 「落としたクラスの役割は、各ページのリード文または本文に残す。」を、明文化前の7行へ遡って当てるか
  - **(e-3)** 落としたクラスの役割の置き場所が4ページで揃っていない（是正2 が範囲外として持ち越し、どこにも引き継がれていなかったもの）
- **Escalation → user へ上げた**: 5件（下記）

### 調整役の独立レビュー（`6946fa1` ＋ 未コミット分。2026-08-21）

各観点の指摘のうち、成果物の内容を動かすものは調整役が自分で実測して裏を取ってから是正に回した。

| 確認項目 | 結果 | 実測 |
|---|---|---|
| `:71` が指示書 §1「変更後」と一致 | 一致 | `sed -n '71p'` を指示書の文と突き合わせ。`grep -c '行末の空セル'` → 1 |
| `9031fa6` の7行と各セルの文面 | 一致 | `git show 9031fa6~1` / `git show 9031fa6`。`mom.rst` の `StandaloneTestSupportTemplate` のセルが位置づけ1文だけであることも確認（5行/2行 の根拠） |
| `web.rst:44` の帰属先 | 一般名 | `grep -n '^  \* - ' …/web.rst` → データ行は `:26`・`:29`・`:32`・`:35`・`:38`。`HttpServer` を継ぐ行が無い |
| `9031fa6~1` の `mom.rst:22` の主語 | `MessagingRequestTestSupport` | 同クラスは `9031fa6` で削除されていない。「移った」という変化が起きていない |
| `HeaderLine` 経由の行末の空セル除去 | 実在 | `nablarch-testing@e21bf67` の `HeaderLine.java:33` `trimTailCopy(headerLine)`。利用者は `ListMapParser`・`TableDataParser`（`git grep -ln HeaderLine e21bf67 -- src/main/`） |
| `readBlockBodyLines` の呼び出し元 | 4か所 | `XlsFormatReader.java:212`・`:240`・`:274` と `TestCoreReaderAdapter.java:124` |
| `XlsFormatReader.java` の Javadoc の行 | `:550-554` | 指示書 §2 の `:551-555` は1行ずれ。`dropEmptyEntries` が `:566` は指示どおり |
| `mom.rst` が継承するスーパクラス | 2つ | `:130` `BatchRequestTestSupport`・`:131` `BasicHttpRequestTestTemplate`。どちらも `mom.rst` の表に無い |
| 規範の初出と `9031fa6` の前後 | 規範が後 | 規範の文は `5c2c26f`（是正2）で入り、`9031fa6` はそれより前 |
| 台帳 | 一致 | `_batch` 30ファイルの昇順連結が `mapping.csv` とバイト一致。`csv.DictReader` 597行。`456544e` との差分は指定5行の `note` のみで、いずれも旧値を接頭辞として保持 |
| 検証器3本 | OK | `RESULT: OK` / `OK: no errors` / `183 passed, 96 subtests passed` |
| Docker フルビルド | 警告0 | `-E` 付きで `updating environment: 325 added, 0 changed, 0 removed` → `build succeeded.`。325 は `ja/` 配下の `.rst` 実数と一致 |

### user へ上げた5件（判断A〜E の回答に対する再エスカレーション）

いずれも指示書 `ntf-doc-32-fix3.md` が逐語で指定した文に関わるため、調整役の判断では動かせない。

1. **`:71` の適用範囲が実装より狭い** —— テーブル系と `LIST_MAP` のカラム名行でも行末の空セルは詰められる（`nablarch-testing@e21bf67` の `HeaderLine.java:33`）。判断A が辿った3か所は `TestCoreReaderAdapter:264` の呼び出し元であり、本体側のこの経路が漏れている
2. **`:71` の「メッセージのテストデータ」に前例が無い** —— `ja/` で1件（この段落のみ）。「電文のテストデータ」は8件あり、同ページ `:73` も「電文のレコード種別」
3. **`:71` の「この整形」が同ページの別義と衝突する** —— このページの「整形」は `:63`・`:247`・`:249` で書き出し時の装飾に固定されている
4. **台帳5行の `note` を足すと8件になり `design.md` の7行と合わない** —— `#32` では `design.md` 側の括弧書きで解消したが、`note` の文面は指示書の逐語のまま
5. **指示書 §4-1 の「7行のうち6行は落としたクラスの役割が本文に残っていない」は成り立たない** —— 残っていないのはクラス名であって役割ではない。実測は 5行/2行

## Overall Verdict（是正3 全体）

- Self-check: OK（実装エキスパートが各ラウンドで記入）
- QA: OK
- Design expert: OK（是正後）
- Craft expert: OK（是正後）
- Verification expert: OK（是正後）
- Ready to check off: Yes（完了条件1〜13 は調整役が独立に再現して全 OK。14 は本コミットで実施する。上の5件は user への申し送りであり、`#32` の完了条件を満たすことを妨げない）
