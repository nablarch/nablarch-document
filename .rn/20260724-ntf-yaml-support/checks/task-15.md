# `#15` self-check — リクエスト単体テストの設定（ウェブアプリケーション）

対象: `ja/development_tools/testing_framework/setup/request_unit_test/web.rst`
ページ先頭ラベル: `request_unit_test_setting_web`（`style.md` S-08 の一覧から引いた）

## 1. マッピング行の反映対応表（全件）

母集合は `mapping.csv` を `dest_page` で機械的に抽出した**6行全件**であり、ホワイトリストで切り出していない（`#10b` の申し送り）。
`DROP` は0件のため、6行すべてが反映対象である。

```
python3 -c "import csv;[print(r['mapping_id'],r['disposition'],r['dest_section'],r['lines']) for r in csv.DictReader(open('.rn/20260724-ntf-yaml-support/mapping/mapping.csv')) if r['dest_page']=='リクエスト単体テストの設定（ウェブアプリケーション）']"
→ current-0204 MOVE 拡張例 4 / current-0205 MOVE 拡張例 5 / current-0210 MOVE 使用方法 4
  current-0211 MOVE 使用方法 104 / current-0212 MOVE 使用方法 54 / current-0213 MOVE 使用方法 79
  （6行・250 lines・DROP 0件）
```

| mapping_id | 出典（`02_RequestUnitTest.rst`） | lines | 反映先（`web.rst`） | 反映内容 |
|---|---|---|---|---|
| current-0204 | `:93-96` | 4 | `:224` 拡張例 > テストデータの書き方を拡張する | `AbstractHttpRequestTestTemplate` を直接使用しないこと・拡張時に用いること |
| current-0205 | `:99-103` | 5 | `:224` 拡張例 > テストデータの書き方を拡張する | `TestCaseInfo` の役割と、両クラスを継承するという手順 |
| current-0210 | `:306-309` | 4 | `:15` 使用方法 > コンポーネント設定ファイルに設定項目を登録する（導入文） | 実行環境に依存する設定値をコンポーネント設定ファイルで変更できること |
| current-0211 | `:312-415` | 104 | `:17-101` 同上（設定項目一覧の表・`important` 1件・`tip` 2件・脚注2件の地の文） | 19項目の設定項目名・説明・デフォルト値、脚注2件、`ignoreHtmlResourceDirectory` と `tempDirectory` の補足 |
| current-0212 | `:418-471` | 54 | `:103-155` 同上（`sessionInfo` のキー表とXML記述例） | `sessionInfo` の2キーの表、コンポーネント設定ファイルの記述例（XML全文） |
| current-0213 | `:474-552` | 79 | `:157-219` 使用方法 > テストの実行速度を上げる（L4 2件） | JVMオプション2種・Eclipseでの設定手順（画像3件）、HTMLリソースコピー抑止のシステムプロパティ・`important`・`tip`・Eclipseでの設定手順（画像1件） |

**未反映0件。** 落とした具体は D-4（CPUの製品名2件）のみで、`reviews/page-request_unit_test_setting_web.md` に `decide` として記録した。

## 2. 出典の要素別の突合（`current-0211`〜`current-0213`）

### 2-1 設定項目一覧（`:313-393`）の19項目

出典の表のデータ行を機械的に数え、本文の `list-table` のデータ行と突き合わせた。

| # | 設定項目名 | 本文に有り |
|---|---|---|
| 1 | `htmlDumpDir` | ○ |
| 2 | `webBaseDir` | ○ |
| 3 | `xmlComponentFile` | ○ |
| 4 | `userIdSessionKey` | ○ |
| 5 | `exceptionRequestVarKey` | ○ |
| 6 | `dumpFileExtension` | ○ |
| 7 | `httpHeader` | ○ |
| 8 | `sessionInfo` | ○ |
| 9 | `htmlResourcesExtensionList` | ○ |
| 10 | `jsTestResourceDir` | ○ |
| 11 | `backup` | ○ |
| 12 | `htmlResourcesCharset` | ○ |
| 13 | `checkHtml` | ○ |
| 14 | `htmlChecker` | ○ |
| 15 | `htmlCheckerConfig` | ○ |
| 16 | `ignoreHtmlResourceDirectory` | ○ |
| 17 | `tempDirectory` | ○ |
| 18 | `uploadTmpDirectory` | ○ |
| 19 | `dumpVariableItem` | ○ |

出典に無く実装にのみ存在する `htmlResourcesRoot`（`HttpTestConfiguration.java:144`、既定値 `htmlResources`）は**追加していない**（「マッピングにない内容を追加しない」）。

### 2-2 出典のセル内補足の行き先

| 出典 | 内容 | 反映先 |
|---|---|---|
| `:356-358` | `ignoreHtmlResourceDirectory` の `tip`（`.svn`/`.git` を除外するとパフォーマンス向上） | 表の直後の `tip`（`:95-97`） |
| `:362-368` | `tempDirectory` の `tip`（jettyの既定は `./work`、無い場合はTempフォルダ） | 表の直後の `tip`（`:99-101`）。「Windowsの場合はユーザのホームディレクトリ/Local Settings/Temp」はOS依存の具体を「OSの一時ディレクトリ」に一般化した |
| `:372-376` | `uploadTmpDirectory` の説明（コピー後に処理するため実体が移動されない） | 説明セル内（`:77`） |
| `:380-392` | `dumpVariableItem` の説明（可変項目＝JSESSIONIDと二重サブミット防止用トークン、毎回同じ結果にしたい場合の値） | 説明セル内（`:80`。プロパティ名と逆の意味である旨の注意を含む）。**指定すべき値は出典の `false` ではなく `true` である**（ラウンド1 R1-M1 で是正。`HttpServer.java:427-430`） |

### 2-3 `current-0213` の要素

| 出典 | 内容 | 反映先 |
|---|---|---|
| `:475-476` | 実行速度を向上させたい場合の導入 | `:159` L3導入文 |
| `:478-480` | CPUに関する `tip` | `:161-163`（製品名2件は落とした。D-4。ラウンド1 R1-8 で1文に絞った） |
| `:486-489` | `-Xms256m -Xmx256m` | `:167-171` |
| `:492-494` | `-Xverify:none` | `:173-181`（非推奨の `important` を追加。D-5） |
| `:497-503` | 実行構成での指定手順＋`vmoptions.png` | `:183-188` |
| `:505-515` | インストール済みのJREでの指定手順＋`installed_jre.png`・`edit_jre.png` | `:190-199` |
| `:520-522` | `-Dnablarch.test.skip-resource-copy=true` | `:203-207` |
| `:527-529` | 頻繁に編集しない場合は設定してよい旨 | `:203`（同じ段落に統合） |
| `:532-534` | `important`（編集してもHTMLダンプに反映されない） | `:209-211` |
| `:537-539` | `tip`（ディレクトリが無ければコピーされる） | `:213-215`（ラウンド1 R1-7 で「ダンプディレクトリ配下の `htmlResources` ディレクトリ」と referent を明示） |
| `:542-548` | 実行構成での指定手順＋`skip_resource_copy.png` | `:217-219`（ラウンド1 R1-9 で、手順を繰り返さず「JVMオプションと同じ実行構成の「VM 引数」欄」の1文＋画像に縮めた） |

## 3. ゲート

| # | ゲート | 結果 | 実行内容 |
|---|---|---|---|
| 1 | `dest_page` の6行**全件**の反映先が記録されている（母集合をホワイトリストで切り出さない） | OK | §1 の表。`csv.DictReader` で抽出した6行と表の行数が一致 |
| 2 | ページ先頭ラベルが `style.md` S-08 の一覧どおり | OK | S-08:320 の `request_unit_test_setting_web` と `web.rst:1` が一致 |
| 3 | 第2部の記載範囲を守っている（テストソースコードの実装例・テストデータの記述例を置かない） | OK | 本ページの `code-block` は `xml` 2件・`bash` 3件のみ（`grep -c` で実測）。`java` 0件、テストデータの記述例0件 |
| 4 | 出典の文面をそのまま流用していない | OK | 表のセル・地の文とも書き直した。XML記述例とJVMオプションは設定値そのものであり流用に当たらない |
| 5 | 用語が `glossary.md` の正表記 | OK（ラウンド1で是正） | `テストケース` 0件・`データシート` 0件・`HTML ダンプ` 0件・`Webアプリケーション` 0件。**ラウンド1で `オーバヘッド`→`オーバーヘッド`・`基底クラス`→`スーパクラス`・`セッション`→`セッションスコープ`・`Jetty`→`内蔵サーバ（Jetty）` を是正**（いずれも §8 の置換表の左辺には無く、FW解説書の用法・§5.12・§5.14 に照らして判明した）。是正後の再測定で `オーバヘッド` 0件・`基底クラス` 0件 |
| 6 | 段落内で改行していない（1段落1行） | OK | 空行を挟まず日本語の本文行が連続する箇所0件 |
| 7 | `.. contents::` を置いている（S-09） | OK | `web.rst:6-8` |
| 8 | 新規ラベルが `ja/` 全体で衝突していない | OK | `request_unit_test_setting_web` / `request_unit_test_web` / `html_check_tool` の3件とも、`ja/` 配下の既存ラベル定義に同名なし |
| 9 | 作成したページが `toctree` に載っている | OK | `setup/index.rst` に `request_unit_test/web`、`implementation/index.rst` に `request_unit_test/web`、`tools/index.rst` に `html_check_tool` |
| 10 | Docker フルビルドが `build succeeded`・新規警告0件 | OK | `docker run --rm -v <repo>:/root/document nablarch-document-build /bin/bash -c "cd /root/document; sphinx-build -E -a -d _build/.doctrees/ja -b html ja _build/html"` → `build succeeded, 1 warning.`。警告は既知の `db_double_submit.rst:108: undefined label: how_to_set_token_in_request_unit_test` 1件のみ。生成HTMLで画像4件の `src` と `:ref:` の解決を確認。ビルドが再生成した `locales/ja/LC_MESSAGES/sphinx.mo` は `git checkout -- locales/` で復元 |
| 11 | `mapping/`・`design.md`・`style.md`・`glossary.md`・`ja/conf.py` に差分が無い | OK | `git status --short` に当該パスの変更なし |

**初回ビルドで1件の新規警告**（`web.rst:6: WARNING: Title underline too short.`）が出たため是正した。原因はタイトル26文字（表示幅52）に対し下線が50文字だったことで、docutils の下線長チェックが表示幅基準であることによる。下線を52文字にして解消（`steering.md` Rules の「表示幅で揃える」が見出し下線にも効くことの実例）。

## 4. ラウンド1の是正（4観点レビュー）

4観点それぞれを別のサブエージェントで実施した結果、**A pass / B pass / C fail（`must` 3）/ D fail（`must` 1）**。`must` は重複を除いて3件で、いずれも是正した（コミット `f4c9fad`、`web.rst` のみ）。

| # | 区分 | 内容 |
|---|---|---|
| R1-M1 | `must` | `dumpVariableItem` の説明が**実装と逆**（実装は `true` のとき可変項目を除去する。`HttpServer.java:427-430`）。出典もフィールドのjavadocも同じ誤りを持つ |
| R1-M2 | `must` | `オーバヘッド` → `オーバーヘッド` |
| R1-M3 | `must` | `基底クラス` → `スーパクラス` |

`should`/`note` の是正13件・対応しない判断7件（うちレビュアー間で割れた2件を含む）の全件は `reviews/page-request_unit_test_setting_web.md`「ラウンド1」に記録した。

是正後の Docker フルビルドは `build succeeded, 1 warning.`（既知の `db_double_submit.rst` 1件のみ・新規0件）。段落内改行0件・`テストケース` 0件も再測定した。

## 5. ラウンド2（是正差分限定の検証）

`#10b` の申し送りに従い、ラウンド1の是正差分（`ae89097..f4c9fad`）だけを対象に、**「是正が指示範囲に収まっているか」「是正が新しい欠陥を生んでいないか」の2点のみ**を1つのサブエージェントで検証した。ページ全体の再レビューはしていない。

**判定: pass（`must` 0件）。指摘は `should` 3件・`note` 6件。**

| # | 区分 | 指摘 | 対応 |
|---|---|---|---|
| R2-1 | `should` | ラウンド1で追加した `dumpVariableItem` の `tip` が直上の表セルの言い換えになっており、**ラウンド1で削らせた欠陥（`tip` が直前の文の言い換え）を別の場所で再生産している**。かつ `tip` の新設自体が指示範囲外 | `tip` を削除し、「プロパティ名から受ける印象とは逆の意味である点に注意する」を表セルに畳んだ |
| R2-2 | `should` | `tip` が `htmlResources` というディレクトリ名をリテラルで名指ししているが、それを決める `htmlResourcesRoot` はページに無く（R1-6 で表への追加を見送ったため）、変更可能である事実を読者が知る手段がない | 表に項目を足さず、`tip` を「ダンプディレクトリ配下のHTMLリソースのコピー先ディレクトリ（デフォルトは `htmlResources`）」に書き換えた |
| R2-3 | `should` | R1-1 で `htmlResourcesCharset` に `template` を挙げた結果、直上の `htmlResourcesExtensionList`（`css`・`js`・`jpg`）との間に、ページ上で説明されない不整合が生じた。実装上 `.css`・`.js`・`.template` は拡張子リストと無関係に書き換え対象になる（`HttpRequestTestSupport.java` の `HtmlResourceExtensionFilter#accept`） | `htmlResourcesCharset` の説明に「`htmlResourcesExtensionList` の指定によらず書き換えの対象になる」を足した |
| R2-4 | `note` | 距離のある後方参照は「上記」より「前述」が本解説書の用法 | 2箇所目（`:199`）を「前述のオプション」に戻した |
| R2-5 | `note` | `:203` が1文中で「リクエスト単体テスト」を2回繰り返している（リンク文言を参照先タイトルに合わせた副作用） | 前半を「テストの実行時に」に改めた |
| R2-6 | `note` | `sessionInfo` の実体は `null` ではなく空の `Map`（`HttpTestConfiguration.java:133`）で、「該当なし」とわずかにずれる | **対応しない。** 他5項目は `null` 初期化で「該当なし」が正しく、読者にとっての意味（初期状態で格納される値は無い）は空の `Map` でも同じ。表記を1項目だけ変えると列内が不揃いになる |

ラウンド2の検証は、差分の各箇所を実コードまで辿って再検証しており、**新たな事実誤りは検出されなかった**（`dumpVariableItem` の反転是正・`checkHtml` の `important`・`htmlResources` ディレクトリの `tip`・セッションスコープ・拡張子の並び・記述例の導入文・スーパクラスと型引数の記述が、いずれも実装と一致することを確認）。

ラウンド2の是正後、Docker フルビルドは `build succeeded, 1 warning.`（既知の1件のみ・新規0件）。段落内改行0件を再測定。

## 6. Overall Verdict

- 6行全件を反映。未反映0件
- 出典と実装の食い違いは、作成時に4件（C-1〜C-4）、ラウンド1でさらに2件（`dumpVariableItem` の反転・`htmlResourcesCharset` の範囲）を検出し、いずれも実装を優先した
- user review に上げる `decide` 3件: 画像の配置規約（D-1）／CPU製品名の削除（D-4）／`-Xverify:none` の非推奨追記（D-5）
- 4観点レビュー ラウンド1（`must` 3件を是正）→ ラウンド2の是正差分限定の検証で **pass**（`must` 0件）→ ラウンド2の `should` 3件も是正済み
- Ready to check off: **user review 承認待ち**（`steering.md` Rules「user review の承認を受けるまで次タスクに着手しない」）
