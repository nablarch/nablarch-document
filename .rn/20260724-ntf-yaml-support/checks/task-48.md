# `#48` 図の作成（PlantUML 21枚）・既存画像の処置・README「図の作成方法」— 実測記録

指示書: `ntf-doc-48-figures.md`（§12 まで反映）。参照点: 解説書 `a6da1f6`／`nablarch-testing@3c4bd2a`／`nablarch-testing-rest@ec718a2`／`nablarch-testing-junit5@c06ebe8`／`nablarch-testing-converter@d611bec`。
生成環境: PlantUML 1.2025.4（`~/.local/share/plantuml/plantuml-1.2025.4.jar`）、Java `temurin-17-jdk-amd64`、フォント `Noto Sans JP`（`~/.fonts/NotoSansJP-Regular.ttf`。`fc-list :lang=ja family` が `Noto Sans JP` を返す）。

## 1. 図ごとの記録

`file:line` はすべて `a6da1f6` 時点のもの。パスは `ja/development_tools/testing_framework/` からの相対。

| # | ファイル | 本文の行 | 実装の `file:line`＋ピン | 生成サイズ | `:scale:` |
|---|---|---|---|---|---|
| 1 | `about/images/index/architecture_components` | `about/index.rst:106` | — | 577x538 | 無し |
| 2 | `about/images/index/test_support_class` | `about/index.rst:106`、継承先の対応は `implementation/request_unit_test/web.rst:35`・`rest.rst:17`・`batch.rst:17`・`mom.rst:17`、`implementation/class_unit_test/component.rst:15`・`entity.rst:15` | `nablarch-testing@3c4bd2a`: `src/main/java/nablarch/test/event/TestEventDispatcher.java:22`（`abstract`）・`TestSupport.java:27`・`core/db/DbAccessTestSupport.java:36`・`core/db/EntityTestSupport.java:48`・`core/http/HttpRequestTestSupport.java:72`・`core/http/AbstractHttpRequestTestTemplate.java:62`・`core/http/BasicHttpRequestTestTemplate.java:15`・`core/standalone/StandaloneTestSupportTemplate.java:21`・`core/batch/BatchRequestTestSupport.java:26`・`core/messaging/MessagingRequestTestSupport.java:48`・`core/messaging/MessagingReceiveTestSupport.java:13`・`core/integration/IntegrationTestSupport.java:16`／`nablarch-testing-rest@ec718a2`: `src/main/java/nablarch/test/core/http/SimpleRestTestSupport.java:39`・`RestTestSupport.java:26`（いずれも `extends` 句を `git show <pin>:<path>` で実測） | 1128x457 | `70` |
| 3 | `setup/images/common/send_sync_testdata_layout` | `setup/common.rst:166`-`:170`・`:219`・`:264`、`implementation/deal_unit_test/mom.rst:72` | — | 508x406 | 無し |
| 4 | `setup/images/junit5_extension/extension_class` | `setup/junit5_extension.rst:16`-`:20`・`:227`-`:231`・`:241`・`:262`・`:271` | `nablarch-testing-junit5@c06ebe8`: `src/main/java/nablarch/test/junit5/extension/TestSupportExtension.java:14`（`extends TestEventDispatcherExtension`） | 491x403 | 無し |
| 5 | `setup/images/master_data_restore/restore_flow` | `setup/master_data_restore.rst:26`-`:32` | — | 485x459 | 無し |
| 6 | `implementation/class_unit_test/images/component/select_sequence` | `implementation/class_unit_test/component.rst:147`-`:153`・`:157`-`:171` | — | 725x485 | 無し |
| 7 | `implementation/class_unit_test/images/component/update_sequence` | `implementation/class_unit_test/component.rst:176`-`:191`・`:195`-`:213` | — | 766x530 | 無し |
| 8 | `implementation/request_unit_test/images/web/request_test_components` | `implementation/request_unit_test/web.rst:13`-`:44`。`Nablarch Application Framework` の出典は `about/index.rst:106`・`implementation/request_unit_test/rest.rst:17`（指示書 §12 (3) の判断による） | — | 431x500 | 無し |
| 9 | `implementation/request_unit_test/images/web/execute_sequence` | `implementation/request_unit_test/web.rst:87`-`:98`・`:191`-`:200` | — | 767x625 | 無し |
| 10 | `implementation/request_unit_test/images/web/mail_request_components` | `implementation/request_unit_test/web.rst:529`-`:533` | — | 609x463 | 無し |
| 11 | `implementation/request_unit_test/images/web/html_dump_layout` | `implementation/request_unit_test/web.rst:541`-`:543` | — | 686x311 | 無し |
| 12 | `implementation/request_unit_test/images/rest/request_test_components` | `implementation/request_unit_test/rest.rst:13`-`:17`・`:93` | — | 742x599 | 無し |
| 13 | `implementation/request_unit_test/images/batch/request_test_components` | `implementation/request_unit_test/batch.rst:13`-`:21` | — | 674x500 | 無し |
| 14 | `implementation/request_unit_test/images/batch/execute_sequence` | `implementation/request_unit_test/batch.rst:167`-`:173`・`:177`-`:184` | — | 863x702 | 無し |
| 15 | `implementation/request_unit_test/images/mom/request_test_components` | `implementation/request_unit_test/mom.rst:13`-`:17` | — | 673x533 | 無し |
| 16 | `implementation/request_unit_test/images/mom/execute_sequence` | `implementation/request_unit_test/mom.rst:178`・`:186`-`:194` | — | 886x531 | 無し |
| 17 | `implementation/request_unit_test/images/mom/send_sync_sequence` | `implementation/request_unit_test/mom.rst:30`・`:37`-`:51` | — | 780x534 | 無し |
| 18 | `implementation/deal_unit_test/images/mom/send_sync_mock_components` | `implementation/deal_unit_test/mom.rst:17`・`:31`・`:35` | — | 707x410 | 無し |
| 19 | `implementation/images/testdata_notation/testdata_layout` | `implementation/testdata_notation.rst:26`-`:28`・`:44`-`:51`・`:83`-`:90`・`:98`・`:117`-`:124` | — | 539x512 | 無し |
| 20 | `tools/images/request_data_tool/tool_components` | `tools/request_data_tool.rst:88`-`:118` | — | 330x569 | 無し |
| 21 | `tools/images/testdata_converter/converter_components` | `tools/testdata_converter.rst:14`-`:16`・`:22`-`:39` | — | 586x216 | 無し |

`:scale:` を付けたのは図2 の1枚だけである。生成幅 1128px が本文幅を超えるため `70` を指定した（既存の `tools/html_check_tool.rst:193`（1124px）が同じ `70` を使っている前例に合わせた）。他20枚は 886px 以下で、`:scale:` 無しの既存画像の最大（`tools/images/request_data_tool/03_Eclipse_OpenFile.png` 1056px）を下回る。

## 2. 削除した既存画像（13件）

`git rm` で削除した。実行結果は各コミットの `git diff --numstat`（削除は `-  -  <path>`）で確認できる。

| ディレクトリ | ファイル | コミット |
|---|---|---|
| `setup/images/common/` | `send_sync_test_data_structure.png` | `49c90098` |
| `setup/images/master_data_restore/` | `modification_detected.png`・`copy_from_backup.png` | `a2473cdc` |
| `implementation/request_unit_test/images/web/` | `mail_overview.jpg`・`htmlDumpDir.png` | `620311a2` |
| `implementation/request_unit_test/images/mom/` | `send_sync_base.png`・`hanrei.png` | `e8163455` |
| `implementation/deal_unit_test/images/mom/` | `send_sync_online_base.png`・`send_sync_online_mock.png`・`send_sync_test_data_no.png`・`send_sync_response_count_change.png` | `f73e4d89` |
| `tools/images/request_data_tool/` | `requestDumpToolAbstract.png`・`image.xlsx` | `2887060e` |

上書き2件（`implementation/class_unit_test/images/component/select_sequence.png`・`update_sequence.png`）は `d71b139c` で PlantUML 生成物に差し替えた。画面キャプチャ13件は触っていない。

## 3. `.rst` の差分の全件表（完了条件8）

`git diff -U0 a6da1f6..HEAD -- 'ja/**/*.rst'` の hunk は27件（下表の行数）で、すべて §3 の挿入・§4 の削除・§6 の (a)〜(i) に分類される。§3・§4・§6 以外の hunk は0件。

| ファイル | hunk | 分類 |
|---|---|---|
| `about/index.rst` | `@@ -107,0 +108,7 @@` | §3 図1・図2 の挿入 ＋ §6 (f) |
| `implementation/deal_unit_test/mom.rst` | `@@ -19 +19 @@` | §6 (a)（導入文） |
| `implementation/deal_unit_test/mom.rst` | `@@ -21,7 +21 @@` | §6 (a)（画像2枚→図18） |
| `implementation/deal_unit_test/mom.rst` | `@@ -78,6 +72 @@` | §6 (b) ＋ §4（`send_sync_test_data_no.png`） |
| `implementation/deal_unit_test/mom.rst` | `@@ -85,2 +74 @@` | §6 (c) ＋ §4（`send_sync_response_count_change.png`） |
| `implementation/request_unit_test/batch.rst` | `@@ -18,0 +19,2 @@` | §3 図13 の挿入 |
| `implementation/request_unit_test/batch.rst` | `@@ -174,0 +177,2 @@` | §3 図14 の挿入 |
| `implementation/request_unit_test/mom.rst` | `@@ -18,0 +19,2 @@` | §3 図15 の挿入 |
| `implementation/request_unit_test/mom.rst` | `@@ -39,5 +41 @@` | §3 図17 への差し替え ＋ §6 (d) ＋ §4（`send_sync_base.png`・`hanrei.png`） |
| `implementation/request_unit_test/mom.rst` | `@@ -179,0 +178,2 @@` | §3 図16 の挿入 |
| `implementation/request_unit_test/rest.rst` | `@@ -18,0 +19,2 @@` | §3 図12 の挿入 |
| `implementation/request_unit_test/web.rst` | `@@ -43,0 +44,2 @@` | §3 図8 の挿入 |
| `implementation/request_unit_test/web.rst` | `@@ -99,0 +102,2 @@` | §3 図9 の挿入 |
| `implementation/request_unit_test/web.rst` | `@@ -531 +535 @@` | §3 図10 への差し替え ＋ §4（`mail_overview.jpg`） |
| `implementation/request_unit_test/web.rst` | `@@ -539 +543 @@` | §3 図11 への差し替え ＋ §4（`htmlDumpDir.png`） |
| `implementation/testdata_examples.rst` | `@@ -1923,0 +1924,2 @@` | §6 (b)（参照ラベルの追加） |
| `implementation/testdata_notation.rst` | `@@ -29,0 +30,2 @@` | §3 図19 の挿入 |
| `implementation/testdata_notation.rst` | `@@ -44,8 +46 @@` | §6 (e)（`code-block` 削除） ＋ §6 (i)（`:46` の末尾の一文を削除） |
| `implementation/testdata_notation.rst` | `@@ -83,8 +78 @@` | §6 (e)（`code-block` 削除） ＋ §6 (i)（`:78` の末尾の一文を削除） |
| `implementation/testdata_notation.rst` | `@@ -117,8 +105 @@` | §6 (e)（`:117` の差し替えと `code-block` 削除） |
| `setup/common.rst` | `@@ -171,0 +172,4 @@` | §3 図3 の挿入 ＋ §6 (g) |
| `setup/common.rst` | `@@ -219,3 +223 @@` | §6 (h) ＋ §4（`send_sync_test_data_structure.png`） |
| `setup/junit5_extension.rst` | `@@ -21,0 +22,2 @@` | §3 図4 の挿入 |
| `setup/master_data_restore.rst` | `@@ -28,2 +27,0 @@` | §4（`modification_detected.png`） |
| `setup/master_data_restore.rst` | `@@ -32 +30 @@` | §3 図5 への差し替え ＋ §4（`copy_from_backup.png`） |
| `tools/request_data_tool.rst` | `@@ -90 +90 @@` | §3 図20 への差し替え ＋ §4（`requestDumpToolAbstract.png`） |
| `tools/testdata_converter.rst` | `@@ -17,0 +18,2 @@` | §3 図21 の挿入 |

## 4. 完了条件1〜11 の実測

**1. 画像ファイル 55件（`.puml` 21・`.png` 34）。`.jpg`・`.xlsx` は0件。**

```
$ find ja/development_tools/testing_framework -path '*/images/*' -type f | wc -l
55
$ find ja/development_tools/testing_framework -path '*/images/*' -name '*.puml' | wc -l
21
$ find ja/development_tools/testing_framework -path '*/images/*' -name '*.png' | wc -l
34
$ find ja/development_tools/testing_framework -path '*/images/*' -type f ! -name '*.png' ! -name '*.puml'
（出力なし）
```

21組の `.puml`／`.png` のパスは §1 の表のとおりで、§3 の「ページ」「ファイル名」と一致する。

**2. `.. image::` 34件、参照先はすべて実在。削除13件への参照0件。**

`.rst` を走査して `.. image::` の相対パスを `os.path.normpath` で解決し、`os.path.exists` で突き合わせた（独立に組んだスクリプト。成果物付属の検証スクリプトは使っていない）。

```
image directives: 34
missing targets: []
references to deleted: []
```

**3. 同名の図のパス。**

```
$ ls ja/development_tools/testing_framework/implementation/request_unit_test/images/*/request_test_components.png
.../images/batch/request_test_components.png
.../images/mom/request_test_components.png
.../images/rest/request_test_components.png
.../images/web/request_test_components.png
$ ls ja/development_tools/testing_framework/implementation/request_unit_test/images/*/execute_sequence.png
.../images/batch/execute_sequence.png
.../images/mom/execute_sequence.png
.../images/web/execute_sequence.png
```

**4. 21枚とも `.puml` から別ディレクトリへ再生成して `cmp` でバイト一致。**

`.puml` をスクラッチディレクトリへコピーし、指示書 §5 のコマンド（是正 (k) 後）で再生成して `cmp -s` した。21枚すべて `OK`、`DIFF` は0件。

使った java の実体は `/usr/lib/jvm/temurin-17-jdk-amd64/bin/java -version` の1行目が `openjdk version "17.0.19" 2026-04-21`。README「図の作成方法」の前提 `Java 17` と一致する。

同名の `.puml` が複数ディレクトリにあるため（`execute_sequence` 3件・`request_test_components` 4件）、再生成先は `.puml` 1本ごとに別ディレクトリを切って突き合わせた。

**5. 禁止語0件・解説書参照0件。**

`mapping/glossary.md` §8「対応表」の左列を機械抽出（97語）し、全 `.puml` に対して突き合わせた。ヒットした12件はいずれも適用条件に照らして置換対象外である。

- `単体テスト` 10件 — すべて `リクエスト単体テスト`・`取引単体テスト`・`コンポーネント単体テスト`・`エンティティ単体テスト` の一部。対応表の条件（「`リクエスト単体テスト` などの一部でなく…クラス単体テストを指すことが文脈から確定できる場合に限る」）に該当しない
- `バッチアプリケーション` 2件 — いずれも既に正表記 `Nablarchバッチアプリケーション` の一部

`NTF` は当初 `architecture_components.puml` の PlantUML エイリアス（`as NTF`）として1件ヒットしたため、`757344ea` で `FW` に改めた。現在は0件である。

```
$ grep -rn 'nablarch-document\|\.rst\|:[0-9][0-9]*\b' --include=*.puml ja/
（解説書参照に当たるものは0件）
```

**6. Docker フルビルド。**

```
$ docker run --rm -v /home/tie303177/work/nablarch/nablarch-document:/root/document nablarch-document-build \
    /bin/bash -c "cd /root/document; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"
build succeeded.
exit=0
$ grep -cE 'WARNING:|ERROR:|SEVERE:' build.log
0
```

ビルド直後に `git -C /home/tie303177/work/nablarch/nablarch-document checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行し、`build.log` を削除した。

出力の確認: **Sphinx は画像を `_build/html/_images/` に集約するため、完了条件6 の文言（`_build/html/development_tools/testing_framework/` 配下に21枚）は指示書の誤りである**（指示書 §13（`c98d887c`）でディレクターが確認）。判定は「21枚が `_images/` に出力され、`<img src>` 34件にリンク切れ0」とする。実測は次のとおりで、21枚すべてが出力されている。同名の図は Sphinx が連番を付けて区別する。

```
$ ls _build/html/_images/ | grep -E 'execute_sequence|request_test_components'
execute_sequence.png / execute_sequence1.png / execute_sequence2.png
request_test_components.png / request_test_components1.png / request_test_components2.png / request_test_components3.png
```

ビルドした HTML の `<img src>` を走査したところ、`_images` を指す参照は34件で、リンク切れは0件であった。

**7. 検証スクリプトと不変対象の差分。**

```
$ python3 mapping/tools/verify_mapping.py
Loaded 597 rows from mapping.csv
lines total (all rows): 12986
lines total (excluding DROP): 11983
OK: no errors
$ python3 mapping/tools/verify_glossary.py
population 検証  331 件 / 不一致   0 件
design_sections 検証   21 件 / 不一致   0 件
scheme_names 検証    7 件 / 不一致   0 件
reasons    検証    0 件 / 不一致   0 件
RESULT: OK
$ git diff --numstat a6da1f6..HEAD -- .rn/20260724-ntf-yaml-support/mapping.csv .rn/20260724-ntf-yaml-support/_batch/ ja/conf.py en/ Dockerfile .rn/20260724-ntf-yaml-support/mapping/glossary.md
（出力なし＝0行）
```

`glossary.md` は §5.15 を含めてファイル全体で差分0行である。

**8. 差分の分類** — 上の §3 のとおり。§3・§4・§6 (a)〜(i) 以外の hunk は0件。

**9. `README.md`。** `## 図の作成方法` を指示書 §2 の逐語で挿入した。位置は `## ドキュメントのビルド方法`（36行目）と `## textlintの実行方法`（79行目）の間（57〜77行目）。コミット `e40f091b`。

**10. 記録。** `design.md` 2箇所（§「「アーキテクチャ」は本文のみとし、図も構成物一覧の表も置かない」冒頭の上書き段落、§「画像の配置」末尾の1文）、`steering.md` の `#33` (b)・`#48`・State、本ファイル。

**11. `git status --porcelain` が空、全コミットが push 済み。** 報告時点で実測して記載する。

## 5. 指示書の穴として報告した件

**`implementation/testdata_notation.rst` の2文が、§6 (e) の `code-block` 削除で指す先を失う。** §6 は `:117` だけを扱っており、次の2文は扱っていない。§9「本文の追記・言い換え（§6 の (a)〜(h) 以外）」に当たるため、報告時点では処置していなかった。

- `:44`（現 `:46`）「同名の1つのExcelファイル（`.xls` または `.xlsx`）がテストクラスに対応し、1シートが読み込み単位に対応する。**ディレクトリ構成の対応は、以下のとおりである。**」— 直後に続いていた `.. code-block:: text`（`:46`-`:51`）を削除したため、「以下」が指す先が無い
- `:83`（現 `:78`）「同名の1つのディレクトリがテストクラスに対応し、1つのYAMLファイルが読み込み単位に対応する。**ディレクトリ構成の対応は、以下のとおりである。**」— 同じく `:85`-`:90` の削除により「以下」が指す先が無い

いずれも図19（`:30` に置いた `testdata_layout`）が同じ内容を両形式の対比として示しているため、`:117` と同じ形（`:ref:` で図を指す）か、末尾の一文を落とす形のどちらかで詰められる。

**処置**: 指示書 §13（`c98d887c`）で **(i)** として「末尾の一文を落とす」形が指示され、`:46`・`:78` の各末尾の一文「ディレクトリ構成の対応は、以下のとおりである。」を削除した。前の文はそのまま。実測は次のとおりで、当該ページに残る「以下のとおりである」は本件の2文とは無関係な箇所（`:186` ほか）だけである。

```
$ grep -n 'ディレクトリ構成の対応は、以下のとおりである。' ja/development_tools/testing_framework/implementation/testdata_notation.rst
（出力なし）
```
