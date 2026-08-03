# task-08 Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| mapping.csvのdest_page=テスティングフレームワークとはの全13行が反映されている | OK | **ラウンド2再検証（独立レビューで確認された指摘1-5の修正後）。** `python3 -c "import csv; ..."`でmapping.csvをdest_page=='テスティングフレームワークとは'で再フィルタし13件であることを再確認（current-0162/0163/0164/0165/0166/0175/0176/0180、input-0002/0116/0028、current-0377/0267）。13件全件を再トレースし、いずれも脱落なく反映されていることを確認。<br>1. `current-0162`（01_Abstract.rst:13-20）→「全体像」2段落目（指摘4で全面的に文構造を書き直し。詳細は下記）<br>2. `current-0163`（同:23-27）→「テストデータ」>「テストデータファイルへの外部化」1段落目（指摘4で2文目を書き直し）<br>3. `current-0164`（同:30-135, 生きた文はNablarch特化APIの1文のみ）→「全体像」1段落目（変更なし）<br>4. `current-0165`（同:139-166, 構成図+構成物表）→「アーキテクチャ」simple table＋image（変更なし、既存の正しい変換を維持）<br>5. `current-0166`（同:170-194）→「全体像」3段落目・code-block・tip（変更なし）<br>6. `current-0175`（同:587-612）→「テストデータ」>「テストの独立性」+tip。**指摘1で脱落していたマスタデータ投入タイミング文（テスト実行前に1回、または準備済み前提）と3メリット（プロジェクト全体で再利用/メンテナンス容易化/実行速度向上）を復元**（`grep -n "全テスト実行前に1回\|再利用でき\|メンテナンス\|実行速度" about/index.rst`で存在確認）。tip文も指摘4で書き直し<br>7. `current-0176`（同:615-624）→「テストデータ」>「テストデータファイルへの外部化」箇条書き（指摘4でbullet2-3を書き直し）<br>8. `current-0180`（同:698-739）→「稼動環境」>「モジュール一覧」2つ目のcode-block（変更なし）<br>9. `input-0002`（ntf-doc-terms.md:13-35, 特殊記法・コメント・マーカーカラムの3項目が全データタイプに横断適用される旨）→「テストデータ」>「データブロックの考え方」末尾文。**指摘2で脱落していた「コメント」を復元し、特殊記法・マーカーカラム・コメントの3項目が揃った並列列挙に修正**（`grep -n "コメント" about/index.rst` → `164:...マーカーカラム（読み込み対象外のカラムを示す標識）・コメント`で確認。コメントの定義は`.rn/20260724-ntf-yaml-support/input/ntf-doc-terms.md:102`「セル値の`//`以降はフレームワークが読み込まない」を実測し、括弧書きに反映）<br>10. `input-0116`（ntf-testdata-doc.md:23-48）→「テストデータ」>「データブロックの考え方」表+1段落目（格納階層、指摘4で主語・節順を反転して書き直し）+3段落目（識別方法、変更なし）<br>11. `input-0028`（ntf-doc-terms.md:415-426, テスト種別正式名称8行）→「テストの種類」>「処理方式ごとの正式名称」table。**指摘3(a)で脱落していた「同期応答メッセージ送信処理」（同期応答電文送信の1リクエスト単位のテスト）の事実をMOMによるメッセージング行に統合復元。** 旧3行のうち「メッセージ受信処理」（電文受信1件単位）は現行のMOM行「MOMによる要求電文の受信」に、「同期応答メッセージ送信処理」（同期応答電文送信の1リクエスト単位）は同行「または同期応答電文の送信を1リクエスト単位で行うテスト」に対応させ、両方の事実を1行に統合。glossary.md:156-157で`同期応答メッセージ送信`・`同期応答メッセージ受信`がいずれもMOM系（`FW:libraries/system_messaging/mom_system_messaging.rst`由来）であることを確認済み。HTTPメッセージング行は「HTTP同期応答メッセージ送信処理」（HTTP同期応答電文送信の1リクエスト単位のテスト＝電文送信+応答受信）の事実に近づけて「HTTPによる電文の送信から応答受信までを1リクエスト単位で行うテスト」に書き直し（`grep -n "MOMによる要求電文\|HTTPによる電文" about/index.rst`で確認）。指摘3(b)のテーブルをキュー行は`design.md`§6「テーブルをキューとして使ったメッセージング」の一次資料に基づき「Nablarchバッチアプリケーションと同じ方法で行うテスト」に修正（design.mdの当該箇所を実測: 「Nablarchバッチアプリケーションと同じ方法でテストする」）<br>12. `current-0377`（index.rst:4-27）→「対象範囲」の2つのimportant（変更なし）<br>13. `current-0267`（JUnit5_Extension.rst:37-47）→「稼動環境」>「モジュール一覧」1つ目のcode-block（変更なし）<br><br>**指摘4（逐語的表現の書き直し）の再検証。** 独立レビューが指摘した5箇所すべてについて、base commit `c2419060`（current-*）または作業ツリー（input-*）の実際のソース文を`git show`/`sed`で再実測し、単なる同義語置換ではなく主語・節順・文境界を変えた書き直しであることを確認。<br>a. 全体像2段落目: 元「テスティングフレームワークはJUnit 4をベースとしており、…機能をそのまま利用できる」（原因→結果）→新「アノテーション…機能は、テスティングフレームワーク上でもそのまま利用できる。これは、…JUnit 4を基盤としているためである」（結果→原因、主語をJUnit4機能側に変更）<br>b. テストデータファイルへの外部化1段落目2文目: 元「テストデータファイルを、テスティングフレームワークのAPIを通じて使用できる」（ファイルが主語）→新「テスティングフレームワークは、…このテストデータファイルからAPIを通じて読み込んで使用する」（フレームワークが主語の能動文に変更）<br>c. 同bullet2-3: 元「テストロジックはA、テストデータはBと役割が明確に分かれる」型の並列構文→新「テストソースコードにはロジックだけを残し、データにまつわる関心事は…切り出せる」（並列構文を解消し因果的な言い回しに変更）。bullet3は「Xしておけば/ことでYできる」型→「テストケースを追加する際も、実行の仕組み自体には手を加えず…追記だけで済む」（条件節を解消）<br>d. テストの独立性マスタデータ文: 指摘1の追加内容と合わせて全面書き直し（「共通ファイル化」→「メリット3点」→「タイミング」の順だった原文を、「メリット3点を含む外部化の効果」→「タイミング」の順に圧縮・並べ替え）<br>e. マスタデータ投入tip2-3文目: 元は2文（「これにより」で接続）→新は1文に統合し「ため」の因果節に変更、末尾も「他のテストケースへ影響を与えずに実行できる」→「他のテストケースから独立させたまま実行できる」（テストの独立性という本節のテーマに寄せた言い換え）<br>f. データブロックの考え方「データの格納階層は」文: 元「テストクラス1つ分のデータが読み込み単位に分かれ、その中に複数のデータブロックが共存する」（テストクラス起点のトップダウン）→新「個々のデータブロックは、読み込み単位というまとまりの内側に複数個が共存する形で格納され、その読み込み単位はテストクラス1つ分のデータごとに分かれる」（データブロック起点のボトムアップに反転）<br><br>**指摘5（simple table変換）の再検証。** 「用途/内容/主なデータタイプ」list-tableをsimple table（`====`罫線）に変換。`docutils.utils.column_width()`（東アジア文字を幅2で計算）でカラム幅を算出する専用スクリプトを自作し（`len()`は使わず、既知の落とし穴を回避）、生成した罫線をsphinx-buildで検証（結果は下記）。 | | |
| 4観点のレビューがすべて実施・記録されている | OK | A/B/C/Dそれぞれ独立サブエージェントで3ラウンド実施し、`reviews/page-about_index.md`に全ラウンドの指摘・対応要否・対応内容を記録済み | OK | 3ラウンドとも実測ベースの独立レビューであることを確認（`reviews/page-about_index.md`参照） |
| 未対応の指摘が残っていない、または残す判断とその理由が記録されている | NG | ラウンド3で5件が未解決のまま残っている（R3-B1〜B4、R3-C1、いずれも文体・表記の残課題であり内容・構成には影響しない）。3ラウンド上限のため`steering.md`のRuleどおり4ラウンド目を自己判断で実施せず、`reviews/page-about_index.md`に記録のうえユーザーレビューへ上げる | NG | 未解決5件はいずれも軽微（文体の逐語性3件、表記法の一貫性1件、用語1件）で、内容・網羅性・整合性には影響しないことを確認 |
| make htmlがabout/index.rstについてエラーを出さない | OK | **ラウンド2で再ビルド。** 独立レビューの指摘1-5を適用したrst全体に対し、前回と同じ切り分け方法（`ja/conf.py`をスクラッチにコピーし、(1)`javasphinx`をextensionsから除外、(2)`app.add_javascript`→`app.add_js_file`、(3)`html_theme`を`alabaster`に上書き。リポジトリ内ファイルは無変更）で`sphinx-build -b html -c <scratch_conf> -d <scratch_doctrees> ja <scratch_out>`をフルビルドで実行した。結果は`build succeeded, 3807 warnings`（exit code 0）。ERRORは1901件出ているが、全件`grep "ERROR" build.log`で内訳を確認したところ「Unknown interpreted text role "java:extdoc"」等、javasphinx未適用による既知の環境依存エラーのみで、`grep "ERROR" build.log \| grep -i testing_framework`は0件（本ページ由来のエラーなし）。`grep -n "testing_framework/about/index.rst" build.log`も0件（本ファイルを名指しした警告・エラーなし）。<br>**指摘5のsimple table変換の再検証**: 前回round1で判明した落とし穴（Python `len()`でカラム幅計算すると`ERROR: Malformed table. Text in column margin`になる）を踏まえ、今回は`docutils.utils.column_width()`（東アジア文字を幅2とする表示幅）専用の自作スクリプトでカラム幅・パディングを計算してから罫線を敷いた（検証スクリプトを正解として使わず独立に実装）。ビルド後のHTMLで`grep -c "<table" .../about/index.html` → `4`（アーキテクチャ表・テストの種類表・処理方式ごとの正式名称表・データブロックの考え方表の4つ、malformed tableによる欠落なし）、`grep -c "system-message\|Problem in" .../about/index.html` → `0`。生成HTMLをテキスト抽出して目視確認し、「用途/内容/主なデータタイプ」表の3行が文字化け・列ズレなく描画されていることを確認済み。<br>`:ref:`稼動環境 <testing_framework_about-operating_environment>``は生成HTMLで`href="#testing-framework-about-operating-environment"`として2箇所（全体像からの参照＋ラベル自体）解決されており、undefined label警告は出ていない。画像（`abstract_structure.png`）も引き続きビルドログでコピーが確認できる。 | | |
| testing_framework/index.rstからabout/index.rstへのtoctree導線がある | OK | `ja/development_tools/testing_framework/index.rst`の`.. toctree::`に`about/index`を記載（唯一のエントリ）。ビルドログでも`development_tools/testing_framework/index`から`about/index`への遷移が警告なく解決されている | | |

## QA Expert Review

（本タスクでは steering.md の指示により、Rules の4観点（QA/設計/クラフト/検証）ではなく
ページ作成タスク専用のA〜D観点を用いる。A:網羅性がQAを、B:トンマナがクラフトを、
C:用語とD:整合性が検証を兼ねる。詳細は `reviews/page-about_index.md` 参照）

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Verification approach meaningful to the objective (checks the right thing, not just "passed") | OK | 各ラウンドとも独立サブエージェントに実測（`git show`によるsource取得・grep・docutils/sphinx-buildでの実パース）を義務付け、成果物付属の検証手段に頼らせない運用を徹底した |

## Expert Reviews (axes the task needs)

### A: 網羅性（QA相当）

| ラウンド | Verdict | Evidence / Improvement |
|---|---|---|
| 1 | NG | current-0165構成図欠落、input-0116定義誤り（`reviews/page-about_index.md` R1-A1/A2） |
| 2 | NG | current-0175メリット欠落、input-0002コメント欠落、input-0028事実欠落・出典不明内容（R2-A1〜A3） |
| 3 | **PASS** | 13行全件がOK。未解決の指摘なし |

### B: トンマナ（Craft相当）

| ラウンド | Verdict | Evidence / Improvement |
|---|---|---|
| 1 | NG | 逐語的流用4箇所、S-07表記法、S-08 :ref:欠如（R1-B1〜B3） |
| 2 | NG | ラウンド1修正が不十分な箇所あり、S-07表記法が別表にも該当（R2-B1〜B2） |
| 3 | **NG（未解決のままユーザーレビューへ）** | 3箇所の逐語的言い回し残存（R3-B1〜B3）、処理方式ごとの正式名称表のsimple table化未実施（R3-B4）。3ラウンド上限のため追加の自己判断による修正は実施していない |

### C: 用語（Verification相当・前半）

| ラウンド | Verdict | Evidence / Improvement |
|---|---|---|
| 1 | NG | 処理方式ごとの正式名称の旧名称残存・MOM/テーブルをキュー行欠落（R1-C1） |
| 2 | （未実施。C観点はラウンド1・3のみ実施、ラウンド2はA/B中心の再レビューだったため） | — |
| 3 | **NG（未解決のままユーザーレビューへ）** | MOMによるメッセージング行「同期応答電文」が未定義語かつglossary揺れ表記の残存（R3-C1） |

### D: 整合性（Verification相当・後半）

| ラウンド | Verdict | Evidence / Improvement |
|---|---|---|
| 1 | NG | `:ref:`欠如（R1-D1、B3と同一事象）、マスタデータツール類の未リンク（R1-D2、対応不要・申し送り） |
| 3 | **PASS** | `:ref:`解決、toctree、画像参照、simple table 2件の整形、`make html`相当ビルドとも異常なし |

## Overall Verdict

- Self-check: OK（実装担当による3ラウンド分の自己検証。mapping.csv全13行の再トレース、sphinx-build相当の再ビルドを実施）
- QA (=A 網羅性): PASS（ラウンド3で全13行OK）
- Design expert: N/A（本タスクは既存構造の実装であり、構造・アプローチの新規策定を伴わない）
- Craft expert (=B トンマナ): **NG（未解決5件中4件）** — R3-B1/B2/B3/B4、`reviews/page-about_index.md`参照
- Verification expert (=C+D 用語・整合性): **一部NG** — D（整合性）はPASS、C（用語）はR3-C1が未解決
- Ready to check off: **No** — 3ラウンドのレビューを尽くしたが未解決指摘が5件残っている（いずれも文体・表記レベルで内容・網羅性・整合性には影響しない）。design.md 11.7「3ラウンドで解決しない指摘は、未解決のまま記録してユーザーレビューに上げる」に従い、コーディネーターの判断による4ラウンド目の自己修正は行わず、ユーザーの `/rn:ty`（現状で承認）または `/rn:gm`（追加修正の指示）を仰ぐ

---

## `#8` 差し戻し対応（`ntf-doc-08-rework.md`）後の追記

### A-6: 行数記録の訂正

上記「Overall Verdict」等に至るまでの報告で口頭言及された「6セクション245行」は実測と合わない。
`about/index.rst` の行数は、`#8` 差し戻し対応前（`ef44dfc`時点）で **235行**、差し戻し対応（A-1〜A-4適用、
`wc -l` で実測）後は **225行** である（`テスト種別の正式名称` 表を list-table からsimple tableへ変換し、
`テーブルをキューとして使ったメッセージング` 行を削除したことによる純減）。

### 差し戻し対応で変わった判定

| Criterion | Self-check | Evidence |
|---|---|---|
| 未対応の指摘が残っていない、または残す判断とその理由が記録されている | **OK** | `design.md`§11.7改訂（must/decide/note区分）後、`about/index.rst`を独立サブエージェントで3ラウンド再レビュー。must区分の指摘はすべてラウンド3までに解消（`reviews/page-about_index.md`参照）。残るのは`decide`区分1件（「対象範囲」節の処理方式一覧欠落、D-R2-1/D-R2-2）のみで、`design.md`11.7「3ラウンド上限に達してユーザーレビューに上げてよいのはdecideのみ」に合致する状態でユーザーレビューへ上げる |
| `about/index.rst`に`同期応答電文`が0件 | OK | `grep -c "同期応答電文" ja/development_tools/testing_framework/about/index.rst` → `0` |
| `処理方式ごとの正式名称`の見出しと導入文が表の中身と一致している | OK | 見出しを`テスト種別の正式名称`に変更、導入文を表の実際の中身（クラス単体・リクエスト単体6→5区分・取引単体）に合わせて修正。観点D再レビューでPASS（D-R1-1修正後の再検証、ラウンド2で確認） |
| `make html`相当のビルドがエラー0 | OK | scratch conf（javasphinx除外・`add_js_file`・`alabaster`テーマ）でsphinxをインストールし、`ja`全体を`sphinx-build -b html`でフルビルド。`build succeeded`、exit 0。`grep ERROR build.log \| grep testing_framework`は0件。直近の増分ビルド（about/index.rstのみ再パース）でも新規警告・エラー0件（`html_static_path`の既知の無関係警告1件のみ） |
| `python3 mapping/tools/verify_mapping.py`が`exit 0`、行数・lines合計が不変 | 要最終確認 | `mapping.csv`・`_batch/*.csv`は本ラウンドで一切編集していない（`about/index.rst`と`design.md`のみ変更）ため不変のはず。commit前に実行して確認する |

### 是正後レビューの要約

- 観点A（網羅性）: PASS（must/decide 0件、note 1件）
- 観点B（トンマナ）: 3ラウンドでmust全件解消。ただしR3-B2/R3-B3相当の2箇所は、新基準の機械適用結果とユーザーの
  既存判定（A-5、修正しない）が食い違ったため、**ユーザー判定を優先し原文のまま維持**（`design.md`§11.6に
  「ユーザーの個別判断は本基準より優先する」を追記して再発防止）
- 観点C（用語）: PASS（must/decide 0件、note 1件＝「期待するテスト結果」/「期待値」の表記不統一、対応不要）
- 観点D（整合性）: must 2件（D-R1-1, D-R2-1/D-R3-1）は解消。ただし解消の過程で「対象範囲」節に
  `mapping.csv`に出典のない内容を追加しかけたため取り消し、代わりに`decide`案件として記録（詳細は
  `reviews/page-about_index.md`「新規decide案件」参照）

詳細な全指摘・全ラウンドの記録は `reviews/page-about_index.md` を参照。
