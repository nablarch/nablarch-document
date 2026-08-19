# page-request_data_tool — リクエスト単体データ作成ツール（`#27-04`）

対象ファイル: `ja/development_tools/testing_framework/tools/request_data_tool.rst`
ラベル: `request_data_tool`（`mapping/style.md:391`）
部: 第4部 ツール

## 参照リポジトリ

| リポジトリ | 作業指示のピン | 参照方法 |
|---|---|---|
| `nablarch-testing` | `e21bf67` | ピンは作業ツリー HEAD（`fdf55d4`）の祖先ではない。`git merge-base --is-ancestor e21bf67 HEAD` は rc=1。すべて `git show e21bf67:<path>` で読んだ |
| `nablarch-testing-jetty12` | ピンなし | `/home/tie303177/work/nablarch/` 配下にソースが無い。下記「ローカル Maven リポジトリの参照」を参照 |

### ローカル Maven リポジトリの参照（Rule §1-9 からの逸脱）

Rule §1-9 は「出典・実装・規約はすべてこのリポジトリと `/home/tie303177/work/nablarch/` 配下にある」としているが、本ページの主題である `nablarch-testing-jetty12` はそこに無い。モジュール名の記載が正しいかを事実で確認するため、`~/.m2/repository/com/nablarch/framework/` 配下の jar を読み取り専用で参照した。参照したのは次の2件である。

| jar | `nablarch/test/core/http/dump/` の内容 |
|---|---|
| `nablarch-testing-jetty12/6-NEXT-SNAPSHOT/nablarch-testing-jetty12-6-NEXT-SNAPSHOT.jar` | `RequestDumpServer.class`・`RequestDumpServer$1.class`・`RequestDumpAgent.class`・`RequestDumpServlet.class`・`RequestDumpServerShutdownFilter.class`・`HtmlReplacerForRequestUnitTesting.class`・`SimpleReplacer.class`（`template.xls` は無い） |
| `nablarch-testing/6u3/nablarch-testing-6u3.jar` | `template.xls` のみ（クラスは無い） |

`nablarch-testing-jetty12/1.1.0/nablarch-testing-jetty12-1.1.0-sources.jar` も展開して読んだ。`RequestDumpAgent.java:129-131` の `getTemplateBook` は `RequestDumpAgent.class.getResourceAsStream("template.xls")` でクラスパスから読む。`RequestDumpAgent` は `nablarch.test.core.http.dump` パッケージにあるため、解決先は `nablarch/test/core/http/dump/template.xls`、すなわち `nablarch-testing` 側の資源である。**2つのモジュールが両方とも必要であることを、この2点で確認した。**

## 出典行の消化（G10）

`mapping.csv` を `csv.DictReader` で読み `dest_page == 'リクエスト単体データ作成ツール'` を抽出した全17行・163行分。すべて `MOVE`。DROP なし。出典は削除済みのため `git show 2e501ad:<path>` で読んだ。

| mapping_id | 出典 | ページ上の反映先 | 判定 |
|---|---|---|---|
| current-0334 | `01_HttpDumpTool.rst:9-22` | リード文、機能概要1〜2段落目、`:19` の `:ref:` | 消化。脚注の飛び先 `request_test_req_params` は削除済みのため `testdata_notation-test_shots` に付け替え |
| current-0335 | `:25-30` | 機能概要2段落目（Excel形式で取得できる／直感的に作成できる） | 消化 |
| current-0336 | `:33-39` | 使用方法のリード＋全体図 | 消化 |
| current-0337 | `:42-46` | 使用方法リードの「導入の手順を済ませておく」 | 消化。「開発環境構築ガイド」の1行は落とした（下記） |
| current-0338 | `:49-60` | 「入力となるHTMLダンプを生成する」 | 消化＋実装で補強（出力先の構成） |
| current-0339 | `:63-73` | 「HTMLダンプからツールを起動する」＋tip | 消化 |
| current-0340 | `:76-78` | 「画面を操作してリクエストを送信する」 | 消化 |
| current-0341 | `:81-86` | 「Excelファイルをダウンロードする」 | 消化 |
| current-0342 | `:89-93` | 「リクエストパラメータをテストデータにコピーする」 | 消化 |
| current-0343 | `02_SetUpHttpDumpTool.rst:4-8` | 導入のリード文 | 消化。旧ラベル `http_dump_tool_prerequisite` は `request_data_tool-setup` に置き換え |
| current-0344 | `:11-22` | 「前提事項」 | 消化＋実装で補強（`JAVA_HOME`） |
| current-0345 | `:25-61` | 「依存関係を確認して起動用スクリプトを配置する」 | 消化。jar名の列挙（`nablarch-testing-XXX.jar` 等）はpomの記述に統合した |
| current-0346 | `:64-67` | 「Eclipseから起動できるように設定する」のリード | 消化 |
| current-0347 | `:70-78` | 同節の手順1〜3＋1枚目の画像 | 消化。画像の実物に合わせてラベルを補正（下記） |
| current-0348 | `:81-87` | 同節の手順4＋2枚目の画像 | 消化 |
| current-0349 | `:90-99` | 同節の手順5＋3枚目の画像 | 消化。`httpDump.sh` の記述は一度落としたが、`#28` §7 で取り消して戻した（下記・`decide` 1）。**判定（2026-08-19、`#29`）**: 事象1は仕様（解説書側対応のみ）と判定済みで、本文は据え置き、`TODO(NTF-MOD-02-1)` は削除した。詳細と出典は本書「判断待ち（`decide`）」の 1。**user 判断（2026-08-19、`#30`）**: `httpDump.sh` の案内を再度落とし、`httpDump.bat` だけを示す形にした。詳細と根拠は本書「判断待ち（`decide`）」の 1。 |
| current-0350 | `:102-111` | 「HTMLダンプからツールを起動する」＋4枚目の画像 | 消化。旧ラベル `howToExecuteFromEclipse` は不要になったため起こしていない |

### 意図して落とした出典

| 出典 | 落とした理由 |
|---|---|
| `01_HttpDumpTool.rst:43`「開発環境構築ガイドに従って開発環境を構築済みであること。」 | `git grep '開発環境構築ガイド' 2e501ad -- ja/` のヒットはこの1件のみで、リンクターゲットも該当ページも存在しない。参照先の無い前提条件になるため落とした |
| `02_SetUpHttpDumpTool.rst:91-92`「Linuxの場合はシェルスクリプト(httpDump.sh)を選択する。」 | `httpDump.sh` が配布されていない（`decide` 1）。**この判断は `#28` §7 で取り消した。** `ntf-doc-28-decide-disposition.md:703`・`:709` の決定により、Windows・Linuxの双方で使えることを前提に本文を書き、`tools/request_data_tool.rst:82` で `httpDump.bat` / `httpDump.sh` の双方を示す形に戻した（`#28` 時点は `:86`。この状態の実物は `561c1ab:ja/development_tools/testing_framework/tools/request_data_tool.rst:82`。`#29` が `TODO(NTF-MOD-02-1)` の3行と直後の空行1行を削除したため4行ずれた。2026-08-19 実測）。`.sh` が配布物に無いことは同ファイルの `TODO(NTF-MOD-02-1)`（`#28` 時点は `:60`）で判定待ちとして記録していたが、**この TODO は判定が返ったため `#29` で削除済みである**（下記の判定を参照）。依頼書は `ntf-mod-02-nablarch-testing.md` §2。`:download:` は `httpDump.bat` の1件のままとした。存在しないファイルを `:download:` で指すとビルドが WARNING を出し、ゲート7（WARNING 0件）に反するためである。**判定（2026-08-19、`#29`）**: 事象1は仕様（解説書側対応のみ）と判定済みで、本文は据え置き、`TODO(NTF-MOD-02-1)` は削除した。詳細と出典は本書「判断待ち（`decide`）」の 1。戻した本文（`561c1ab:ja/development_tools/testing_framework/tools/request_data_tool.rst:82`）と `:download:` 1件（同 `:62`。いずれも 2026-08-19 実測）は、現行解説書 `2e501ad:ja/.../02_SetUpHttpDumpTool.rst:59`・`:91-92` と同じ形であり、`#29` 時点では意図した状態であった。**その後 user 判断（2026-08-19、`#30`）により、本文からは再び `httpDump.sh` の案内を落とした**（`:download:` は `httpDump.bat` の1件のまま）。詳細と根拠は本書「判断待ち（`decide`）」の 1 |
| `02_SetUpHttpDumpTool.rst:33-48` のpomスニペットの `<dependencies>` と `<!-- 中略 -->` | 抜粋であることを示すだけの行。既存ページ `setup/request_unit_test/rest.rst:20-37` は `<dependency>` 要素のみを示す形なので合わせた |

## 実装で確認した事実（出典に無い追記）

`design.md:509`・`design.md:521` に従い、`file:line` とコミットで記録する。

| 記載内容 | 出典 |
|---|---|
| 出力先はダンプディレクトリの下のテストクラス名のディレクトリ | `nablarch-testing@e21bf67` `src/main/java/nablarch/test/core/http/HttpRequestTestSupport.java:243`（`testClass.getSimpleName()`）・`:409-411`（`new File(config.getHtmlDumpDir() + fileSeparator + className)`）。既定値は `HttpTestConfiguration.java:24` の `./tmp/html_dump`。画像 `04_Eclipse_OpenWith.png` にも `UserRegisterActionRequestTest` フォルダとして写っている |
| `:68-70` の tip（起動用スクリプトの動作と配置場所の理由） | `ja/development_tools/testing_framework/tools/downloads/request_data_tool/httpDump.bat:3`（`cd /d %~dp0`）・`:6`（`set CP=./lib/*`） |
| 前提事項の `JAVA_HOME` | 同 `httpDump.bat:7`（`set JAVA_EXE="%JAVA_HOME%\bin\java"`） |
| 初期画面表示でもテストショット番号の列だけの `requestParams` が要る | `implementation/testdata_notation.rst:451` の tip。実装の裏付けは `nablarch-testing@e21bf67` `src/main/java/nablarch/test/core/http/TestCaseInfo.java:342-351`（行数が足りないと `IllegalArgumentException`） |
| pomのコメントを「リクエスト単体データ作成ツールの実装」にした | `nablarch-testing-jetty12` の `RequestDumpServer` は `org.eclipse.jetty.server.Server` を直接組み立てており、Nablarchの内蔵サーバ（`HttpServerJetty12`）を経由しない（`nablarch-testing-jetty12-1.1.0-sources.jar` の `RequestDumpServer.java:10-14,87`）。jetty12 を足す理由は内蔵サーバではなく本ツールの実装が入っていることである |
| Eclipse手順のGUIラベル | `images/request_data_tool/01_Eclipse_Preference.png`・`02_Eclipse_EditorSelection.png`・`03_Eclipse_OpenFile.png`・`04_Eclipse_OpenWith.png` を実際に開いて読み取った。出典は `Preference`・`External program`（単数形）と書いていたが、実物は `Preferences`・`External programs`。押すべき `Add...` は画面右上ではなく `Associated editors` の側（赤枠が指しているのも下側） |

## 移送したアセット（G13）

`design.md:897`・`:907` に従い `git mv` した。移動元ディレクトリ `guide/development_guide/08_TestTools/01_HttpDumpTool/` は空になったので削除した。

| 移動元 | 移動先 |
|---|---|
| `_image/{requestDumpToolAbstract,01_Eclipse_Preference,02_Eclipse_EditorSelection,03_Eclipse_OpenFile,04_Eclipse_OpenWith}.png` | `tools/images/request_data_tool/` |
| `_image/image.xlsx` | `tools/images/request_data_tool/image.xlsx` |
| `download/httpDump.bat` | `tools/downloads/request_data_tool/httpDump.bat` |

`image.xlsx` は画像の作図元で、`grep -rn 'image.xlsx' ja/ en/ --include=*.rst` のヒットは0件である。`guide/` 配下は順次消えるため、作図元を失わないよう画像と同じディレクトリへ移した（`guide/` 内の他ページも `images.xlsx`・`mail_image.xlsx` のように作図元を画像と同居させている）。`en/` 側は対象外のため触っていない。

`:download:` の置き場所は `design.md` に規定が無いため、FW解説書の先例 `web/getting_started/downloads/client_create/` に倣って `tools/downloads/<ページのラベル>/` とした。

## 4観点レビュー

QA・設計・クラフト・検証の4観点を、それぞれ別のサブエージェントで1巡した。指摘は延べ42件。**是正26件・不採用9件・記録のみ7件。** 是正はすべて push 前の1巡で畳んだ。

### 是正した指摘

| # | 指摘 | 対応 |
|---|---|---|
| 1 | HTML系の語が `HTMLダンプ`／`HTML`／`HTMLファイル`／`htmlファイル` の4通りに割れている（`glossary.md:287` の正表記は `HTMLダンプ`） | ダンプ出力を指す箇所はすべて `HTMLダンプ` に統一。OSのファイル種別を指す2箇所（前提事項・Eclipse設定のリード）は `HTMLファイル` にした |
| 2 | 見出し下線の直後に空行を入れている（11箇所） | 全削除。新規16ページの実測は「直後に本文」203件対「空行あり」4件 |
| 3 | `code-block:: text` でコマンドを示している | `bash` にした。既存の `mvn` コマンド例 `testdata_converter.rst:105` が `bash` |
| 4 | Eclipse設定を番号付きリストで書いており、承認済みページと揃わない | `setup/request_unit_test/web.rst:186-198` に倣い、`*` の箇条書き＋画像をリスト外に置く形にした |
| 5 | 「追加(Add)ボタン」がどちらの Add か特定できない | 画像を開いて確認し、「関連付けられたエディター(Associated editors)」の「追加(Add...)」と特定した |
| 6 | GUIラベルの英語表記が実物と違う（`Preference`／`External program`） | `Preferences`／`External programs`／`Browse...`／`Add...` に補正 |
| 7 | 「導入」をセクションタイトルの直書きで指している | `.. _request_data_tool-setup:` を追加し `:ref:` にした。使わなくなった `request_data_tool-prerequisite` は削除（被参照0件を確認） |
| 8 | 図の後に前提が来る | 使用方法のリードを「導入を済ませておく」＋「全体の流れは次のとおり」の2文にし、図を後ろに置いた |
| 9 | 使用方法のリードが機能概要の言い換えになっている | 1文に削った |
| 10 | `:101` の参照が本文の根拠になっていない（飛び先に「テストクラス名」の記述が無い） | 「`htmlDumpDir` で指定したダンプディレクトリ」までを参照の対象とし、テストクラス名のディレクトリは実装で確認した事実として記載（上表） |
| 11 | 見出し「テストデータにコピーする」だけでは中身が分からない（`style.md:150`） | 「リクエストパラメータをテストデータにコピーする」にした |
| 12 | `httpDump.sh` を案内しているが配布していない | Linux／`httpDump.sh` の記述を落とし、「配置した起動用スクリプト(httpDump.bat)を選ぶ。」にした（`decide` 1）。この是正は `#28` §7 で取り消し、双方を示す形に戻してある。**判定（2026-08-19、`#29`）**: 事象1は仕様（解説書側対応のみ）と判定済みで、本文は据え置き、`TODO(NTF-MOD-02-1)` は削除した。詳細と出典は本書「判断待ち（`decide`）」の 1。**user 判断（2026-08-19、`#30`）で本指摘の是正を再適用した**: 本文は「配置した起動用スクリプト(httpDump.bat)を選ぶ。」に戻り、本指摘は解消済みである。詳細と根拠は本書「判断待ち（`decide`）」の 1。 |
| 13 | pomのコメント `<!-- 内蔵サーバの実装 -->` が理由を取り違えている | 「リクエスト単体データ作成ツールの実装」にした |
| 14 | リード文の主語がねじれている（ツールがブラウザを操作することになる） | 「ブラウザで表示するツールである。画面に値を入力してサブミットすると〜」に分割 |
| 15 | 機能概要1段落目の「これを」の指す先が一意でない | 「キーと値を人手で書き写すと」に書き換え |
| 16 | 「サブミットで発生したHTTPリクエストが〜ダウンロードできる」の主述がねじれている | 「〜パラメータを記載したExcelファイルを、ダウンロードできる。」にした |
| 17 | 「ExcelやOpenOfficeで起動すればよい」は「起動」の誤用 | 「開けばよい」にした |
| 18 | 「HTMLファイルがブラウザで起動される」も同じ誤用 | 「HTMLダンプがブラウザで開かれる」にした |
| 19 | 「画面上で入力して」の目的語が無い | 「画面に値を入力して」にした |
| 20 | 見出し「依存関係を**追加**して」と本文「記述されていることを**確認**する」が食い違う | 見出しと導入リードを「確認して」に統一 |
| 21 | 「本ツールは…2つのモジュールが提供する」が二重主語 | 「本ツールの実体は、〜2つのモジュールに含まれる。」にした |
| 22 | 「関連付けされて」は誤用 | 「関連付けられて」にした |
| 23 | 前提事項に `JAVA_HOME` が抜けている | 追記（上表） |
| 24 | ディレクトリの指し方が「プロジェクトのディレクトリ」「pom.xmlと同じディレクトリ」で揺れている | 「pom.xmlと同じディレクトリ」に統一 |
| 25 | tip の「上のコマンド」が指示語のまま | ``mvn dependency:copy-dependencies`` と書いた |
| 26 | 「HTMLファイルを右クリックし、httpDumpで開く」では `Open With` サブメニューが読み取れない | 画像を確認し「右クリックし、「Open With」→「httpDump」を選ぶとツールが起動する」にした |

### 採らなかった指摘

| # | 指摘 | 採らなかった理由 |
|---|---|---|
| 1 | 「`nablarch-testing` と `nablarch-testing-jetty12` の2つが提供する」は誤り。`nablarch-testing@e21bf67` にダンプ関連クラスは1つも無く、`7c545e5`（2019-09-06）で削除されている | 削除の事実はそのとおりだが、結論は成り立たない。jar の実測（上記「ローカル Maven リポジトリの参照」）で、クラスは jetty12 に、`RequestDumpAgent` が読む `template.xls` は `nablarch-testing` にあり、**両方必要**であることを確認した |
| 2 | `nablarch-testing` は他モジュールから推移的に入るため「明示不要」の旨を書き足すべき（`nablarch-example-web/pom.xml:197-200`） | 出典（`02_SetUpHttpDumpTool.rst:31-32`）は2つのjarを必要物として挙げており、推移的取り込みの話は出典にも実装上の必須設定にも当たらない。プロジェクト構成次第の話をこのページに書くと、かえって判断を要求することになる |
| 3 | `:19` の `:ref:` は `testShots` の節ではなく `requestParams` の説明（`testdata_notation.rst:447`）を指すべき | `:447` が属する L4 見出し「ウェブアプリケーションのカラムを記述する」（`:397`）にラベルが無い。ラベルの追加は別ページの改変であり本ページの範囲外。ラベルを持つ直近の上位節が `testdata_notation-test_shots` であり、リンク文字列も見出しと一致している |
| 4 | `Excelファイル` を `\ Excelファイル` にそろえるべき | 逆。`/guide/` を除く既存ページの実測は `Excelファイル` が非エスケープ10件・エスケープ0件。`\ Excel\ 形式` の形（複合語でない場合）だけがエスケープされている |
| 5 | `\ Excel\ やOpenOfficeで` は表示上そろわないので `\ OpenOffice\ ` も付けるべき | `\ ` は空白のエスケープで、描画には出ない。ビルド後の HTML は `直接ExcelやOpenOfficeで起動すればよい。` であり、表示差は無い。エスケープの対象語は実測に基づき `Excel`・`YAML`・`Java` に限っている |
| 6 | tip の「本ツールが内部で起動するサーバ」は用語集の `内蔵サーバ` に置き換えるべき（QA・クラフトの2観点から） | `glossary.md:286` は `内蔵サーバ` を「リクエスト単体テスト（ウェブアプリケーション・RESTfulウェブサービス）で使用するサーブレットコンテナ」と定義している。本ツールが起動するのは `RequestDumpServer`（`org.eclipse.jetty.server.Server` を直接生成、`HttpServerJetty12` を経由しない）で、テスト実行時の内蔵サーバとは別のプロセス・別のサーバである。同じ語を当てると読者に別物を指し示すことになる。設計観点のレビューも同じ結論（`:51` のコメント側を直すべき）に達しており、そちらは是正13で対応した |
| 7 | 「Linuxで使用する場合は同等のシェルスクリプトをプロジェクトで用意する」旨の tip を足す | 指摘者自身が「出典を確認していない（未確認）」と付記している。裏付けの無い運用をドキュメントに書けない（`decide` 1 に上げる） |
| 8 | 初期画面表示の説明に「本ツールは既存のHTMLダンプを入力とするが、初期画面には元となる画面が無いためである」を足す | 同上。指摘者が未確認と明記している |
| 9 | 「導入」配下の見出しが体言止め（前提事項）と動詞終止形で混在している | `style.md` S-03 の「〜する」形式は「使用方法」「拡張例」配下に限られており、「導入」配下は規約対象外。承認済みの `tools/testdata_converter.rst:57` も「前提事項」を体言止めで置いている |

## ゲート

| | 結果 | 実測 |
|---|---|---|
| G1 | PASS | `git status --porcelain` の全件は `R` 7件（画像5・`image.xlsx`・`httpDump.bat`）と ` M` 1件（`request_data_tool.rst`）のみ |
| G2 | PASS | 禁止6対象を `git status --porcelain` で指定して差分0件 |
| G3 | PASS | ビルド直後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行。`git status` に現れない |
| G4 | PASS | `python3 mapping/tools/verify_mapping.py` が exit 0。`mapping.csv` は変更していない |
| G5 | PASS | Docker フルビルドが `build succeeded, 1 warning.`。warning は既知の `db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test` 1件のみ。新規warning 0件 |
| G6 | PASS | `grep -cE '不具合\|バグ\|将来\|修正され'` が 0 |
| G7 | PASS | ページ先頭ラベル `request_data_tool` が `mapping/style.md:391` と一致 |
| G8 | PASS | 見出し12件、下線はすべて50。`east_asian_width` による表示幅の最大は46（「リクエストパラメータをテストデータにコピーする」）。NG 0件 |
| G9 | PASS | 本文の `:ref:` 4件がビルド後HTMLで解決し、リンク文字列も飛び先の見出しと一致（「テストショット一覧（testShots）を記述する」×2・「導入」・「リクエスト単体テストの設定（ウェブアプリケーション）」） |
| G10 | PASS | 上表のとおり17行すべてを分類。落とした3件は理由付きで記載 |
| G11 | N/A | `REFERENCE` の行なし |
| G12 | PASS | 枝分かれ（`-a`／`-b`）の `mapping_id` なし。`src_file` 2本は本ページ専用 |
| G13 | PASS | `.. image::` 5件のファイルが実在し、ビルド後に `_build/html/_images/` へコピーされている。`git ls-files .../01_HttpDumpTool/` は0件、ディレクトリも削除済み |

## 判断待ち（`decide`）

1. **`httpDump.sh` が配布されていない。Linuxでは本ツールを使えない。** 出典 `02_SetUpHttpDumpTool.rst:91-92` は「Linuxの場合はシェルスクリプト(httpDump.sh)を選択する」と書くが、`git ls-files | grep -i httpDump` の結果、この解説書リポジトリに `.sh` は ja/en とも存在しない。`nablarch-testing@e21bf67` の `src/main/script/httpDump.sh` はクラスパスに `http-dump-1.0-jar-with-dependencies.jar` を指定しており、本ページが案内する `-DoutputDirectory=lib`（`./lib/*`）では動かない。加えて同 `pom.xml` の `<build>` は `<testResources>` しか定義しておらず `src/main/script` は jar に入らない（親POM `nablarch-parent` は `/home/tie303177/work/nablarch/` 配下に無いため、親側での追加は未確認）。**本ページはWindows前提の記述に寄せた。** `.sh` を v6 対応版で新規提供するか、Windows専用と明記するかの判断を求める。

   **判定が返った（2026-08-19、`#29`）。クローズ。** 事象1は**仕様（解説書側の対応のみ）**と判定済み（`nablarch-testing` `8530497:docs/pr75/steering.md`。user が作業指示に引用した文面による）。`httpDump.sh` は配布物に含まれない。本文は現行解説書に合わせて据え置くという **user 判断**により変更しない。`TODO(NTF-MOD-02-1)` は削除した。本ページはWindows専用とは明記せず、`561c1ab:ja/development_tools/testing_framework/tools/request_data_tool.rst:82`（2026-08-19 実測）で `httpDump.bat` / `httpDump.sh` の双方を示す現行解説書どおりの形を保つ（この判断は下記のとおり `#30` で上書きされた）。経緯は `checks/task-28.md` §7「本文の書き換えを伴った箇所」。

   **user 判断で本文を変更した（2026-08-19、`#30`）。** `tools/request_data_tool.rst:82` を「`* 配置した起動用スクリプト(httpDump.bat)を選ぶ。`」に改め、Windows・Linux の場合分けと `httpDump.sh` の案内を落とした（2026-08-19 実測。この変更後も `httpDump.sh` は追跡下の `ja/` に0件。`git ls-files ja/ | xargs grep -l` で確認した。`grep -rn ... ja/` だと `.gitignore` 対象の `ja/_build/` に残る旧ガイドのビルド成果物に2件当たるため、測定範囲を追跡ファイルに限る）。**これは現行解説書（`2e501ad:ja/development_tools/testing_framework/guide/development_guide/08_TestTools/01_HttpDumpTool/02_SetUpHttpDumpTool.rst:91-92`「Windowsの場合はバッチファイル(httpDump.bat)を、」「Linuxの場合はシェルスクリプト(httpDump.sh)を選択する。」）にある記述を落とす変更である。** 判断したのは **user**（日付 2026-08-19、タスク `#30`）であり、`#29` の「現行解説書に合わせて据え置く」という判断を上書きする。根拠は（いずれも `nablarch-testing` `65911f5`。本作業ディレクトリからは参照できないため、user が作業指示に引用した文面による）、`src/main/script/httpDump.sh` は存在するが、`pom.xml` に `src/main/script` を成果物へ取り込む設定が無く配布物に入らないこと、および解説書側の配布物も `httpDump.bat` の1件のみ（`tools/downloads/request_data_tool/httpDump.bat`）で、読者が `httpDump.sh` を入手する手段が無いことである。**「Windows専用」「Windowsでのみ使用できる」の趣旨は書かない**（そう断定できる一次情報が無いという user 判断による）。`:download:` は `httpDump.bat` の1件のまま変更しない（`tools/request_data_tool.rst:62`。2026-08-19 実測）。

2. **`nablarch-testing` 本体の `src/main/script/httpDump.{bat,sh}` が Nablarch 1.x 時代のまま残っている。** `e21bf67` の `httpDump.bat` は `nablarch-tfw.jar`・`poi-3.2-FINAL-20081019.jar`・`jetty.jar` を `../lib` から個別指定し、`set JAVA_EXE=%JAVA_HOME%\bin\java\java.exe`（`bin\java\java.exe` は存在しないパス）になっている。この解説書が配布している `httpDump.bat` とは別物で、そのままでは起動しない。かつ jar にも入らない。削除するか v6 対応版に更新するかは本体側の判断であり、ドキュメントでは扱えない。

   **判定が返った（2026-08-19、`#29`）。クローズ。** 事象2は**現状維持**と確定した（出典: `nablarch-testing` `8530497:docs/pr75/steering.md`。本作業ディレクトリからは参照できないため、user が作業指示に引用した文面による）。`src/main/script/httpDump.{bat,sh}` は削除も更新もされない。よって解説書側で反映すべき変更は無く、**本文・`:download:` とも変更しない**（`:download:` は `tools/request_data_tool.rst:62` の `httpDump.bat` 1件のまま。2026-08-19 実測）。なお `TODO(NTF-MOD-02-2)`（`setup/request_unit_test/rest.rst:51`）は依頼書 `ntf-mod-02-nablarch-testing.md` §3-3「あわせて教えていただきたいこと」の照会であり、本判定とは別件のため**回答待ちのまま据え置く**。

3. **`setup/request_unit_test/rest.rst:53` の記述が実装より狭い。** 「``nablarch-testing-jetty12``\ は内蔵サーバの実装を提供するだけで」とあるが、実測では本ツールの実装（`nablarch.test.core.http.dump.*`）も同モジュールに含まれる。承認済みページのため本コミットでは触っていない。

4. **`setup/request_unit_test/web.rst:31` の `webBaseDir` の既定値が実装と食い違う。** ドキュメントは `src/main/webapp`、実装は `nablarch-testing@e21bf67` `HttpTestConfiguration.java:29` の `../main/web`。本ページの範囲外だが、`htmlDumpDir`（一致）を検証する過程で見つけた。

5. **第3部から本ページへの導線が無い。** 旧 `05_UnitTestGuide/02_RequestUnitTest/index.rst:249-250` には「:ref:`http_dump_tool` を使用して、リクエストパラメータのデータを作成する」という逆方向のリンクがあった。`grep -rn 'request_data_tool' ja/ --include=*.rst` の結果、本ページを指しているのは `tools/index.rst:9` の toctree だけである。`design.md:360`「第2部・第3部からツールに言及する場合は `:ref:` で参照する」に照らすと、`implementation/request_unit_test/web.rst`（`#27-19` 以降で作成）に導線を置く必要がある。

6. **規約側の手当ての提案（設計観点から）。** いずれもページは変更していない。
   - `glossary.md:309` の `前提事項` は「機能概要の下位セクション」と定義されているが、第4部では `mapping.csv`（`current-0344`）に従って「導入」配下に置いている。定義を広げるか、第4部の例外を明記するか。
   - `style.md` に「見出し下線の直後に空行を置かない」を明文化する（実測 203/207）。明文が無いため本ページで揺れた。
   - `style.md` S-05 にコマンド例の言語指定（`text` ではなく `bash`）を明記する。
   - キャプチャのUI言語と本文のGUIラベル表記の対応規則（本ページのキャプチャは英語ロケール、`setup/request_unit_test/web.rst` は日本語ロケール）。本ページは出典に倣って「日本語(English)」の併記とした。
