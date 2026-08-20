# #28 Completion Check

作業指示は `ntf-doc-28-decide-disposition.md`。節は着手順に並べてあり、指示書の節番号順ではない。

| 節 | 内容 | 本ファイル内の位置 |
|---|---|---|
| §1 | 判定不要24件のクローズ | 直下 |
| §3 | 規約ファイルの是正（22件） | `## §3` |
| §2 | 本文の是正（32件） | `## §2` |
| §6 | 判断済み10件の実施 | `## §6` |
| §7 | モジュール判定待ちの TODO（7件） | `## §7` |
| §4 | 記録の是正・未確認の解消（15件） | `## §4` |
| §5 | 残骸の整理（4件） | `## §5` |
| — | ゲート1〜11 の判定 | `## ゲート1〜11` |

## §1 判定不要としてクローズする24件

**§1 の24件は `ntf-doc-28-decide-disposition.md` `:39-96` の理由により閉じた**（ゲート1）。指示書 `:41` のとおり作業は無い。内訳は 1-1 飛び先スタブ6件（`#27` 完了により実体化）・1-2 S-02 適用2件（§3-1 に統合）・1-3 `webBaseDir`（`#18` で決着済み）ほか、指示書 `:43-96` に記載のとおり。

## §3 規約ファイルの是正

作業指示: `ntf-doc-28-decide-disposition.md` §3（`:326-447`）。変更してよいファイルは
`mapping/style.md`・`mapping/glossary.md`・`design.md` の3つのみ。`ja/` 配下の `.rst` は1行も変更していない。

### コミット

| コミット | 内容 |
|---|---|
| `62294c3` | 3-19〜3-22（本書の判断に伴う規約改定4件） |
| `55581b4` | 3-3・3-6・3-11・3-12（実測が要る4件） |
| `18fb782` | 3-1・3-2・3-4・3-5・3-7・3-8・3-9・3-10・3-18 |
| `ef40fb9` | 3-13・3-14・3-15・3-16・3-17 ＋ §6-2-3 に伴う `design.md` §8 の追記 |
| `cee5b4d` | 3-11 の実測内訳の自己訂正（下記「自己訂正」参照） |

いずれも `ntf-yaml-support` へ push 済み（`18fb782..ef40fb9..cee5b4d`）。

### 22件の実施結果

行番号は特記なき限り実施後の現在値。「根拠確認結果」は、作業指示が挙げた `file:line` を
すべて自分で開いて確かめた結果である。

| 項番 | 対象ファイル | 実施内容 | 根拠確認結果 |
|---|---|---|---|
| 3-1 | `mapping/style.md` S-02（`:51-58`） | 第3部にも「機能概要は出典が無ければ見出しを置かない」を明文化。第3部で必須なのは「使用方法」だけとし、`design.md` §4 の5節が「標準的な手順の並びであって全ページに5つ揃えることを求めるものではない」を併記 | 一致。`design.md:281-296` は第3部アウトライン（`:281` が「### ページのアウトライン」）。`ntf-doc-27-small-3rd.md:26`・`:28` も一致 |
| 3-2 | `mapping/style.md` S-04（`:235`・`:237-247`） | 見出し記号表に L5 = `"` の行を追加し、`^` の上下線で代用しない理由を規約化 | 一致。着手時の `style.md:189-193` は L1〜L4 の4行のみ（`62bb33a` で確認）。`ja/biz_samples/12/index.rst:85-87` は `^` の上下線で「インタフェース」を書いている |
| 3-3 | `mapping/style.md` S-04（`:234`・`:249-262`） | L4 の使用条件を「同じL3の配下に2本以上並べる場合にだけ使う」に改め、旧条文「用例が薄いページでのみ使う」を撤回。実測を併記 | 一致（`style.md:193` の旧条文を `62bb33a` で確認）。ただし条件は指示の例示「3つ以上」ではなく「2本以上」とした。理由は下記「判断が割れた点」1 |
| 3-4 | `mapping/style.md` S-08 | ラベル一覧の「（スタブ）」を除去 | 一致（着手時 `:343`「JUnit 5用拡張機能（スタブ）」・`:344`「マスタデータ復旧機能（スタブ）」）。ただし該当は2行ではなく4行あった。下記「判断が割れた点」2 |
| 3-5 | `mapping/style.md` S-09（`:541-549`）・S-02（`:43-46`） | S-09 の適用外を「L2セクションを1つも持たないページ」と定義し直し、導線のみ3ページを追加（計7ページ）。S-02 のリード文にも同じ3ページの例外を明記 | 一致。着手時 `:413-417` は4件のみ。3ページはいずれも実測6行（`wc -l` で確認） |
| 3-6 | `mapping/style.md` S-04（`:283-292`） | 「L3・L4は下線の直後に空行を置かない」を明文化。L1は空行を置く、L2は実測が割れているため定めない | **不一致（再計測で値が変わった）**。`#27-04` の 203/207 は `reviews/page-request_data_tool.md:93`・`:165` にあり、当時の新規16ページのみを数えたもの。38ページ全体の再計測では 308/384。下記「実測4件」参照 |
| 3-7 | `mapping/style.md` S-05（`:302-309`） | コマンド例は `text` ではなく `bash` を指定する旨を明記 | 一致（`#27-04 decide-6` の2つ目） |
| 3-8 | `mapping/style.md` S-12（`:706-748`） | キャプチャのUIロケール規約を新設。既存のキャプチャは撮り直さない／同一ページ内でアプリのUIロケールを混在させない／新規は日本語ロケール／本文のUI項目名は「日本語(English)」併記 | 一致。`tools/request_data_tool.rst` のキャプチャは英語、`setup/request_unit_test/web.rst` は日本語。画像33件をすべて開いて分類した（下記「実測4件」の補足） |
| 3-9 | `mapping/style.md` S-13（`:750-777`） | インラインマークアップの直前・直後が全角文字（全角の約物を含む）のとき `\ ` を置く、を明文化 | 一致（規範が無いこと自体を確認） |
| 3-10 | `mapping/style.md` S-07（`:379-425`） | 表の中のクラス名を コードリテラル と `:java:extdoc:` のどちらで書くかを4条で規約化。第3部47件対2件・第2部0件対41件の実測を併記 | 一致（`#27-14 decide-5`） |
| 3-11 | `mapping/style.md` S-04（`:264-276`） | 下線長を「レベルごとの既定値（L1・L2=50、L3・L4=49）とタイトルの表示幅の大きい方」に固定 | 一致（着手時 `style.md:195` は「タイトル文字列と同じ長さ以上」のみ）。ただし「50文字固定」ではなくレベル別とした。下記「判断が割れた点」3 |
| 3-12 | `mapping/style.md` S-02（`:64-71`・`:104-116`） | 第4部のセクション構成を「機能概要 → 導入 → 使用方法」と規約化。`tools/` の実在4ページを実測して根拠に記載 | 一致（第4部が未定義であることを確認）。実測は下記「実測4件」 |
| 3-13 | `mapping/glossary.md` §5.13（`:314`） | 「前提事項」の意味を「機能概要または導入の下位セクション」に広げ、第4部の実配置を根拠として追記 | **不一致（行番号）**。指示は `glossary.md:309` だが、`:309` は「モジュール一覧」の行で、「前提事項」は `:312`（着手時。`62bb33a` で確認） |
| 3-14 | `mapping/glossary.md` §5.7（`:206`）・§8（`:562`） | 「NTF解説書の本文に現れない」の断定を「新規作成したページ本文には現れない。ただし出典の手動テスト手順には実例がある」に緩めた。置換ルールは変えていない | **不一致（行番号）**。指示は `:201`・`:556` だが、`:201` は「テストクラス」・`:556` は「DBアクセステスト」の行。該当は `:204`・`:560`（着手時）。反例 `NTF:05_UnitTestGuide/03_DealUnitTest/index.rst:12`・`:27` は一致。手動テストである旨は指示の `:7-8` ではなく `:8` にある |
| 3-15 | `mapping/glossary.md` §5.4 | 「通信先」は出典の読み替え指示を書き写す文脈でのみ使い、それ以外は「外部システム」を使う、を明文化。§5 の表・§8 の対応表には載せない | 一致。読み替え指示は `NTF:05_UnitTestGuide/02_RequestUnitTest/http_send_sync.rst:9` と `NTF:05_UnitTestGuide/03_DealUnitTest/http_send_sync.rst:11` |
| 3-16 | `design.md` §5（`:371-381`） | 「テストデータ変換ツールは『導入』を持つ」に改め、`#6` の判断を改める理由と移動対象を明記。`.rst` の節移動は §2 の担当へ申し送り | 一致。`design.md:330-360` の範囲に該当記述あり（`:356`）。出典 `input/testdata-converter-design.md` は362行で、`pom.xml`・`dependency`・`plugin`・`artifactId`・「導入」・「インストール」いずれも0件 |
| 3-17 | `design.md` §3「記載範囲」（`:250-264`） | 第3部から設定に言及するときの線引きを明文化。設定項目名＋`:ref:` は可、値・デフォルト値・設定ファイルの記述例は不可。判定手順と例外を併記 | 一致（`:239`「### 記載範囲」を確認）。指示の例示より例外を1つ増やしている。下記「判断が割れた点」4 |
| 3-18 | `mapping/style.md` S-03 例外3（`:213-223`） | ページ単位の作業指示がセクションタイトルを名指しした場合はその指示を優先する、を1条追加。優先条件と記録義務つき | 一致。`style.md:155-156` は S-03 の内容条件（着手時）。`ntf-doc-27-small-3rd.md:129-132` は4本のL3の文言を名指ししている |
| 3-19 | `design.md` §8（`:540-549`） | 「記載例についても同じ基準（無いと読者が書けない）で追記してよい」を追加。`ef40fb9` で判定手順・記録義務まで書き下ろした（§6-2-3 の指定） | 一致（着手時 `design.md:504-517` が当該節） |
| 3-20 | `design.md` §5（`:387`） | §5「第2部・第3部との切り分け」と §8 が両方該当する場合の優先順位を1文追加（設定値はツールページ、他ページからは `:ref:` のみ） | 一致（着手時 `:358-362` が当該節、`:360` が該当文） |
| 3-21 | `mapping/style.md` S-10 規約5 | 「Excel形式の図しか無い場合は、図の直前の本文で『Excel形式で示す』と明示する」を1条追加 | 一致（`#27-09 decide-2`） |
| 3-22 | `design.md` §9 | 「`en/` は本刷新では変更せず、`ja/` 確定後に別タスクで同じ章構成へ揃える」を理由つきで追加 | 一致（着手時 `:546-556` が §9） |

### 別立て: §6-2-3 に伴う `design.md` §8 の追記

`ntf-doc-28-decide-disposition.md:613`（§6-2-3）の指定により、`design.md` §8「出典が欠いている、
実装上必須の設定の追記」に記載例の条項を置いた（`design.md:540-549`、コミット `ef40fb9`）。
`#18` 確定分の条項（`:533-539`）の文言は変更していない。追記は次の3点を満たす。

- 「無いと読者が書けない」を、実物を開いて判定する3条件に分解した（出典に記載例が0件／読者が書くべき
  ファイルの項目名・カラム構成が当該ページのどこにも無い／書き足す内容を実装またはテストコードの
  `file:line` で示せる）
- 記載例の追記にも `reviews/page-*.md` への根拠記録義務が**掛かる**ことを明示した
- 記録の確認は `design.md` §11.9「ページ作成」のゲートが求める4観点レビューで行うとした。作業指示の
  言う「ゲート8」という番号は `design.md` §11.9 には存在しないため、実在する行に読み替えた

なお §3 の表の 3-19 は同じ節を対象としており、本件は 3-19 の書き直しにあたる（別の追記ではない）。

### 実測4件（コマンドと値）

対象は `ja/development_tools/testing_framework/` 配下の `guide/` を除く38ページ。見出しは
「タイトル行＋下線行」で抽出し、下線がタイトルより短いもの・直前行が空でも下線でもないものを除いた。
走査スクリプトはセッション用の一時ファイル（`scratchpad/measure*.py`）で、リポジトリには置いていない。
抽出条件は上記のとおりで、再現できる。

**3-3（L4の分布）**

```
L3 総数 158 / うち L4 を持つ L3 48
L4 を持つ L3 の配下のL4の本数: 2本=40件, 3本=1件, 5本=1件, 6本=4件, 7本=1件, 1本=1件
L4 総数 120 / L4 を持つファイル数 9
（内訳）testdata_examples.rst 58本, testdata_notation.rst 27本, request_unit_test/web.rst 15本,
       class_unit_test/component.rst 6本, class_unit_test/entity.rst 6本,
       deal_unit_test/batch.rst 2本, request_unit_test/rest.rst 2本, setup/common.rst 2本,
       setup/request_unit_test/web.rst 2本
1本だけの1件: implementation/request_unit_test/web.rst:305「テストデータを作成する」
```

**3-6（見出し下線の直後の空行）**

```
見出し総数 384 / 直後が空行でない 308 / 直後が空行 76
  L1: 空行なし  1 / 空行あり 37
  L2: 空行なし 30 / 空行あり 38
  L3: 空行なし 158 / 空行あり  0
  L4: 空行なし 119 / 空行あり  1
L4 の例外1件: implementation/testdata_notation.rst:1379「Excel形式の場合」
L1 の例外1件: index.rst:1（S-09 適用外で `.. contents::` を持たない）
```

`#27-04` の「203/207」は当時の新規16ページを対象にした値（出典 `reviews/page-request_data_tool.md:93`・
`:165`）であり、38ページ全体では 308/384 である。L2が30対38で割れているため、規約は L3・L4（と L1）に
限定した。

**3-11（見出し下線の長さ）**

判定式は「下線長 == max(レベル既定値, タイトルの表示幅)」。表示幅は East Asian Width が W/F/A の文字を
2、それ以外を1として数える。既定値は L1・L2=50、L3・L4=49。

```
一致 290 / 総数 384
  L1: 38/38   L2: 68/68   L3: 122/158   L4: 62/120
不一致 94（すべて「49とすべき箇所を50にしている」型）
  implementation/testdata_examples.rst  L3 22件・L4 58件（計80件）
  tools/request_data_tool.rst           L3  8件
  tools/master_data_tool.rst            L3  6件
L3またはL4を持つページ 31 のうち、不一致を含むのは上記3ページのみ（残り28ページは不一致0件）
```

**3-12（第4部 `tools/` の構成）**

```
master_data_tool.rst   :12 機能概要 → :32 導入 → :118 使用方法   前提事項は :36（導入配下の先頭のL3）
request_data_tool.rst  :12 機能概要 → :22 導入 → :86  使用方法   前提事項は :26（導入配下の先頭のL3）
html_check_tool.rst    :12 機能概要 →           :69  使用方法   前提事項は :65（機能概要配下の末尾のL3）
testdata_converter.rst :12 機能概要 →           :67  使用方法   前提事項は :57（機能概要配下の末尾のL3）
4ページとも「拡張例」「モジュール一覧」のL2見出しは0件。tools/index.rst は toctree のみの表題ページ
```

**補足の実測（3-8・3-9・3-10 で規約の根拠にしたもの）**

- 3-8: `.. image::` の実体33件をすべて画像として開いて分類した。UIキャプチャ13件（英語ロケール3件＝
  `tools/request_data_tool.rst`、日本語ロケール8件、ロケールの判る文字が無いもの2件）、図20件。
  同一ページ内でロケールが混在するページは0件。本文のUI項目名が併記になっていない箇所は11件
- 3-9: インラインマークアップ2,159件の境界を数え、規約に反する箇所は186件（直前が全角の約物で `\ ` 無し
  185件 ＋ `index.rst:13` の1件）
- 3-10: 表のセル内のクラス名は、第3部が コードリテラル47件対 `:java:extdoc:` 2件、第2部が0件対41件。
  第3部の `:java:extdoc:` 2件は `implementation/class_unit_test/entity.rst:35`・
  `implementation/class_unit_test/component.rst:35`

### 自己訂正

`55581b4` で 3-11 の内訳を「`testdata_examples.rst` L3 24件」と書いていたが、再計測すると22件だった
（下線50のL3のうち2件はタイトルの表示幅が50で、規約に一致する）。`cee5b4d` で訂正した。合計94件・
不一致ゼロ28ページという他の数値は再計測でも変わらない。

### 検証結果

```
$ python3 mapping/tools/verify_glossary.py
refs 290/0  counts 118/0  sections 86/0  terms 201/0  applies 96/0
population 331/0  design_sections 21/0  scheme_names 7/0  reasons 0/0
RESULT: OK                       ← 不一致は着手時の0件から増えていない（refs は283→290に増加）

$ python3 mapping/tools/verify_mapping.py ; echo $?
OK: no errors
0

$ python3 -m pytest mapping/tools/ -q
183 passed, 96 subtests passed in 0.57s
```

`git diff --stat`（`ef40fb9` の直前まで累積、`62bb33a..cee5b4d`）は次の3ファイルに限られる。

```
.rn/20260724-ntf-yaml-support/design.md
.rn/20260724-ntf-yaml-support/mapping/glossary.md
.rn/20260724-ntf-yaml-support/mapping/style.md
```

`ja/` 配下の `.rst`・`ja/conf.py`・`en/` 配下・`ntf-mod-01〜03*.md`・`mapping/mapping.csv`・
`mapping/_batch/` は1行も変更していない。

### `glossary.md` §5.15 が0行変更であることの証明

```
$ git diff -U0 -- .rn/20260724-ntf-yaml-support/mapping/glossary.md | grep "^@@"
@@ -154,0 +155,2 @@
@@ -204 +206 @@
@@ -312 +314 @@
@@ -560 +562 @@
```

変更は旧154・204・312・560行の4箇所のみで、いずれも §5.15 の範囲外である。範囲そのものの一致も
確認した（作業指示が挙げた `:331-456` と、実測した §5.15 の見出し範囲 335-460 の両方を含む
旧325-465行が、作業ツリーの327-467行とバイト単位で完全一致）。

```
HEAD 325-465 と 作業ツリー 327-467 が完全一致: True
```

### 判断が割れた点

1. **3-3**: 指示の例示は「L3が3つ以上の独立した操作に分かれる場合」だが、条件を**「同じL3の配下に
   L4を2本以上並べる場合」**とした。実測でL4を持つL3 48件のうち40件が配下2本であり、「3つ以上」に
   すると40件が違反になる。既存の構成をほぼ全否定する規約は採らず、判定できない例外（1本だけの
   `request_unit_test/web.rst:305`）だけを違反として残した
2. **3-4**: 指示は `:343`・`:344` の2行を挙げるが、「（スタブ）」は実際には4箇所あり、4箇所とも
   除去した（2行だけ直すと同一ファイル内で表記が割れるため）
3. **3-11**: 指示の例示は「50文字固定」だが、実測ではL3・L4の既定が49（L3 112件・L4 62件）で、
   50に固定すると174件が違反になる。**レベル別の既定値（L1・L2=50、L3・L4=49）**とし、
   タイトルの表示幅がそれを超える場合のみ伸ばす形にした。この形での違反は94件で、3ページに集中する
4. **3-17**: 指示の例示は「設定項目名を挙げて `:ref:` で送るのはよい。値・既定値・記述例を第3部に
   書かない」だが、そのままでは既存の承認済みページ3箇所が違反になる。判定を「その設定項目名が
   第2部（ツールは第4部）に現れるか」の `grep` で行う形にし、**現れない場合で、テストの実装手順の
   中でしか意味を持たない設定は第3部に置いてよい**という例外を足した。この形での違反は0件
5. **3-6**: `#27-04` の 203/207 を再計測したところ 308/384 で、対象範囲が異なることが分かった
   （上記「実測4件」）。L2が割れているため、L2は規約で定めないことにした

### `ja/` 配下の本文是正への申し送り（§2 の担当へ）

`.rst` は1行も変更していない。規約を確定した結果、次が是正対象になる。

| 規約 | 対象 | 件数 |
|---|---|---|
| S-04（下線長） | `implementation/testdata_examples.rst`（80件）・`tools/request_data_tool.rst`（8件）・`tools/master_data_tool.rst`（6件） | 94件 |
| S-04（下線の直後） | `implementation/testdata_notation.rst:1379`「Excel形式の場合」の直後の空行 | 1件 |
| S-04（L4の条件） | `implementation/request_unit_test/web.rst:305`「テストデータを作成する」の配下のL4が1本だけ | 1件 |
| S-12（UI項目名の併記） | 本文のUI項目名が「日本語(English)」併記になっていない箇所 | 11件 |
| S-13（`\ ` エスケープ） | 直前が全角の約物で `\ ` が無い箇所185件 ＋ `index.rst:13` | 186件 |
| S-07（表内のクラス名） | `implementation/class_unit_test/entity.rst:35`・`implementation/class_unit_test/component.rst:35` の `:java:extdoc:` をコードリテラルへ | 2件 |
| `design.md` §5（3-16） | `tools/testdata_converter.rst` の `:89-101`（`<plugin>`）と `:174-183`（`<dependency>`）を、新設する「導入」（L2）へ移す。「前提事項」（`:57-65`）は機能概要配下のまま動かさない | 1ページ |

## §2 本文の是正

担当は §2 の 2-1〜2-32 のみ。§1・§3〜§7 は触れていない。

### コミット

| SHA | 範囲 | 対象 |
|---|---|---|
| `24896d8` | (A) | 2-1・2-15・2-16・2-17（`implementation/deal_unit_test/batch.rst`、`reviews/page-deal_unit_test_batch.md`） |
| `6fc3000` | (B) | 2-3〜2-6・2-8〜2-10・2-12〜2-14（マスタデータ・設定系） |
| `0ddc0e4` | (C) | 2-2・2-20・2-21・2-22（テストデータ記法系） |
| `601a6d6` | (D) | 2-7・2-18・2-19・2-23〜2-32（導線・追記系、`reviews/page-*.md` 3件を含む） |

いずれも `git add` でファイルを明示して作成した。`git add -A`・`git commit -a` は使っていない。`sphinx-build` は実行していない。本ファイル（`checks/task-28.md`）は `git add` していない。

### 32件の実施結果（ゲート2）

「確認した実体」は、着手前に自分で開いて確認した位置である。行番号は着手前（`24896d8^`）の状態のもの。

| # | 確認した実体（`file:line`） | 確認結果 | 実施内容 |
|---|---|---|---|
| 2-1 | `implementation/deal_unit_test/batch.rst:350`・`:360`・`:370`・`:400`・`:416`・`:432`・`:450`・`:460`・`:470`・`:480`（YAML、`expectedStatusCode: "100"` 10件）、`:117`・`:122`・`:127`・`:192`・`:221`・`:250`・`:277`・`:282`・`:287`・`:292`（Excel 形式の表のセル `100` 10件）。根拠 `ja/application_framework/application_framework/handlers/standalone/status_code_convert_handler.rst:39-41`・`:44-56`、`implementation/testdata_examples.rst:561`・`:568` | 一致（ただし指示書は Excel 側を「`:112`・`:184`・`:213`・`:242`・`:272` の表」としており、実際に `100` を持つセルは上記10行） | YAML 10件・Excel セル 10件をすべて `0` に直した |
| 2-2 | `implementation/testdata_notation.rst:531`（`requestPath`（必須））・`:534`（`userId`（必須））・`:528`（`diConfig`（必須）＝正しい） | 一致 | 「（必須）」を外し、説明欄に「カラムを記述しない場合は ``test`` が使われる」を書いた。実装は `MessagingRequestTestSupport.java:89-91`（`putIfAbsent`）・`StandaloneTestSupportTemplate.java:164`・`:166`・`TestShot.java:73-74`。**`TestShot.java:332-336` の `putIfAbsent` は `containsKey` 判定であり、空セルは補完されない**ため、「空の場合」欄には書かず説明欄に書いた |
| 2-3 | `implementation/testdata_notation.rst:63`（`` `<PROJECT_ROOT>/test/jp/co/tis/example/db/` ``）、`:48-51` の `code-block` | 一致 | 表側を `src/test/java/com/example/db/` に直した |
| 2-4 | `setup/request_unit_test/web.rst:154-155`（`htmlCheckerConfig` の記述例）、同 `:68`（表のデフォルト値） | 一致 | 値を `src/test/resources/nablarch/test/http-request-test/html-check-config.csv` に直した |
| 2-5 | `about/index.rst:20`（「経路に起因する不具合を早期に見つけられる」） | 一致 | 「不具合」→「問題」（1語） |
| 2-6 | `implementation/class_unit_test/component.rst:89`（設定手順）・`:91-93`（`code-block:: properties`） | 一致（指示書は `code-block` を `:91-92` としているが実体は `:91-93`） | 記述と `code-block` を `setup/class_unit_test.rst` へ移し、新設ラベル `class_unit_test_setting-db_transaction` を置いた。第3部からは `:ref:` で送る |
| 2-7 | `setup/request_unit_test/rest.rst:53`。実体は `nablarch-testing-jetty12@646c3d9`（scratchpad に clone）の `src/main/java` | **不一致（指示書の前提が誤り）** | 「内蔵サーバの実装を提供するだけで」を実態に改めた。**実体は `src/main/java/nablarch/test/core/http/dump/` に7クラス、内蔵サーバ関連が3クラス（`HttpServerFactoryJetty12`・`HttpServerJetty12`・`LazySessionInvalidationFilter`）、`src/main/resources` は存在しない。** 現在の不具合の挙動・回避策は書いていない |
| 2-8 | `setup/master_data_restore.rst:91`（`value="nablarch_test_master"`）。配布物 zip 展開結果 `master_data-build.properties:26`、`tools/master_data_tool.rst:94` | 一致（ただし**是正理由は指示書と異なる**） | `NABLARCH_TEST_MASTER` に直した。理由は配布物と綴りを揃えるため。**小文字での実動作は未確認**であり、そう読める記述はしていない |
| 2-9 | `setup/master_data_restore.rst:61`（tip）。実装は `nablarch-testing@e21bf67` `MasterDataSetUpper.java`（`setUpMasterData` が全テーブルを `tablesFinished` に入れ `copyDataToBackUpSchema` へ渡す）・`MasterDataRestorer.java:283`（`TableDuplicator`） | 一致（**`TableDuplicator` は独立クラスではなく `MasterDataRestorer.java:283` の `static class`**） | 投入ツール併用時はマスタデータファイルに記述した全テーブルがバックアップ用スキーマに必要である旨を tip に追記した |
| 2-10 | `implementation/testdata_notation.rst:40`（gsp の tip）。出典 `2e501ad` の `01_Abstract.rst:607-610` | 一致（**出典の範囲は `:607-609` ではなく `:607-610`**。gsp への言及は無い） | gsp の一文を落とし、マスタデータ投入ツールへの `:ref:` に寄せた |
| 2-11 | `tools/master_data_tool.rst` 全体。`grep -c protect` = 0、`grep -c 'build/classes'` = 0 | **不一致（指示書の前提が誤り）** | **是正対象なし。** `.rst` に誤記は0件で、誤記は配布物 zip 側にある。配布物の是正は本タスクの範囲外のため、本項は記録のみで閉じる |
| 2-12 | `implementation/deal_unit_test/mom.rst:62`（1文目・2文目）、`:58-62` | 一致 | 1文目を削除し2文目だけ残した |
| 2-13 | `implementation/request_unit_test/batch.rst:183`、`setup/request_unit_test/batch.rst:16-17` | 一致 | 条件節の帰属を直し、メインクラスの使用は無条件、ループ制御ハンドラの置き換えはハンドラ構成に含まれる場合と書き分けた |
| 2-14 | `setup/request_unit_test/batch.rst:10`・`:15`・`:17`。FW解説書 `batch/nablarch_batch/architecture.rst`（`request_thread_loop_handler` 0件）・`messaging/db/architecture.rst:49`・`messaging/mom/architecture.rst:95` | **不一致（指示書の前提が誤り）** | 「常駐バッチ」の条件付けを3箇所すべてから外し、「ハンドラ構成にリクエストスレッド内ループ制御ハンドラが含まれる場合」に改めた。L3見出しの下線は S-04 に合わせて 62 → 50 に直した（`awk 'length($0)'` で実測） |
| 2-15 | `implementation/deal_unit_test/batch.rst`（記載例の `setUpTable: default`）。実装 `TestShot.java:149-162` | 一致 | 「テストショットごとに準備データが再投入される」旨を1文足した |
| 2-16 | 実装 `TestShot.java:198-213` | **不一致（指示書の前提が誤り）** | **根拠の範囲は `:193-213` ではなく `:198-213`。** 分割例と非分割例の検証範囲の違いを1文足した |
| 2-17 | `implementation/deal_unit_test/batch.rst:376`（`expectedTable: "fileInputBatch"`）。対応するデータブロックが本ページにも出典にも無いことを確認 | 一致 | 当該セルを空にした（データブロックは創作しない） |
| 2-18 | `nablarch-testing@e21bf67` `src/main/java/nablarch/test/core/messaging/MockMessagingContext.java`（`receiveMessage(String,String,long)` が `throw new UnsupportedOperationException`、`close()` は空実装、`send(SendingMessage)` はログ出力後 `return "messageId"`、`sendMessage` は `send` へ委譲） | 一致（ただし**`send`・`sendMessage` は `throws UnsupportedOperationException` を宣言するが実際には投げない**） | `.. important::` で制約を書いた。「投げる」とは書いていない。同クラスは `@Published` を持たないため `:java:extdoc:` では参照せず ``literal`` で書いた |
| 2-19 | `implementation/request_unit_test/http_messaging.rst:15`（「同じ方法で実施する」2箇所） | 一致（ただし**根拠に挙がった `implementation/deal_unit_test/batch.rst:20`・`rest.rst:22` の文言は「同じ方法で行う」ではなく「同じである」**。実際の同型は `implementation/request_unit_test/db_queue.rst:6`・`implementation/deal_unit_test/db_queue.rst:6`） | 2箇所を「同じ方法で行う」に統一した |
| 2-20 | `implementation/testdata_notation.rst:1240`・`:1253`。実装 `MockMessagingContext`（MOM）・`MockMessagingClient`（HTTP、`bodyBytes == null` で `HttpMessagingTimeoutException`）・`SendSyncSupport.java:346`・`:348` | 一致（**MOM 限定にすべき文は `:1240` と `:1253` の2つ**） | `:1240` は「取引単体テストのモックアップクラスは例外を送出せず `sendSync` の戻り値として `null` を返す」を MOM 同期応答送信に限定した。`:1253` は要求電文の扱いを MOM と HTTP で書き分けた |
| 2-21 | `implementation/testdata_notation.rst:1156`（`sendSyncTestData` の段落）、`implementation/testdata_examples.rst:1802`。実装 `SendSyncSupport.java:49`（`SEND_SYNC_TEST_DATA_BASE_PATH = "sendSyncTestData"`）・`TestShot.java` | **不一致（指示書の前提が誤り）** | **対象は `:1154` ではなく `:1156`**（`:1154` は節のリード文）。取引単体テストのモックアップクラスの話であることを明示し、リクエスト単体テストでは `sendSyncTestData` を使わない旨を足した。`testdata_examples.rst:1802` も同様に限定した |
| 2-22 | `implementation/testdata_notation.rst:392`。実装 `TestCaseInfo.java` の `getTestCaseName()`（`sheetName + "_Shot" + no + "_" + description`）、`HttpRequestTestSupport.java:260-261` | 一致 | ファイル名が `<読み込み単位の名前>_Shot<テストショット番号>_<descriptionの値>.html` である旨を足した |
| 2-23 | `implementation/deal_unit_test/mom.rst:72-73` と `implementation/request_unit_test/mom.rst:39-40` が逐語同一であることを確認 | 一致 | 記述量の少ない `deal_unit_test/mom.rst` 側を `:ref:` に置き換えた（飛び先は 2-24 で新設した `request_unit_test_mom-request_id`） |
| 2-24 | `implementation/request_unit_test/mom.rst` に節ラベルが無いこと、`style.md` S-08 の命名規則、`ja/` 全体で衝突が無いこと（`grep`） | 一致 | 6つ足した（`-request_id`・`-test_class`・`-test_method`・`-test_data`・`-execute`・`-assertion`） |
| 2-25 | `nablarch-testing-rest@9ada31e` `src/main/java/nablarch/fw/web/RestMockHttpRequest.java:61-67`（`setBody(Object)`）・`:272-283`（`convertBody`）、`StringBodyConverter.java:9-16`、`JacksonBodyConverter.java:12`・`:29-31`、`RestMockHttpRequestBuilder.java:17`（`defaultContentType = "application/json"`） | 一致（**実ファイルは `nablarch/fw/web/` 配下。`nablarch/test/core/http/` ではない**） | `implementation/request_unit_test/rest.rst` に `setBody` の説明を足した |
| 2-26 | `implementation/request_unit_test/web.rst`（`request_data_tool` への参照0件）、`tools/request_data_tool.rst:1`・`:10` | 一致 | 「テストデータを作成する」に `:ref:` の tip を足した |
| 2-27 | `setup/deal_unit_test/rest.rst:10`（第3部への導線0件）、`implementation/deal_unit_test/rest.rst:1`（`deal_unit_test_rest`） | 一致 | リード文の末尾に `:ref:` を足した |
| 2-28 | `setup/request_unit_test/http_messaging.rst:10`、`implementation/request_unit_test/http_messaging.rst:1` | 一致 | 同じ文型で `:ref:` を足した |
| 2-29 | `reviews/page-request_unit_test_batch.md:193`、`implementation/request_unit_test/mom.rst:10`、`implementation/request_unit_test/batch.rst:10` | **不一致（指示書の追加箇所欄が出典と食い違う）** | **指示書の追加箇所欄は `implementation/deal_unit_test/mom.rst` だが、出典が指摘しているのは `implementation/request_unit_test/mom.rst:10`（応答不要メッセージ**送信**に触れていない）であるため、そちらに足した。** |
| 2-30 | `implementation/request_unit_test/rest.rst`・`mom.rst`・`batch.rst`（JUnit 5 への参照0件）、承認済みの文型 `implementation/request_unit_test/web.rst:96`・`implementation/class_unit_test/component.rst:141`・`entity.rst:105` | 一致 | 3ページの「テストクラスを作成する」節末に、承認済みと同一の文型の tip を足した |
| 2-31 | `implementation/deal_unit_test/db_queue.rst:6`（全6行）、`implementation/deal_unit_test/batch.rst:20`、`setup/request_unit_test/batch.rst:19`（`OneShotLoopHandler`）、`ntf-doc-27-db-queue.md:52` | 一致 | **`db_queue.rst` は1文字も変えていない**（個別指示「『同じ方法で行う』以上のことを書かない」に抵触するため）。中継点の `implementation/deal_unit_test/batch.rst:20` にコンポーネント設定への `:ref:` を足し、3ホップを2ホップにした |
| 2-32 | `implementation/request_unit_test/rest.rst:61`。実装 `BasicTestDataParser.java:41`・`:221-222`・`:194`、`TestSupport.java:404`。デフォルト設定 `nablarch-testing-default-configuration-6u2.jar` の `nablarch/test/test-data.xml`（`testDataParser` に `<property name="dbInfo" ref="dbInfo"/>`）と `nablarch/test/rest-request-test.xml`（`test-data.xml` を `import` していない） | 一致 | tip を `testDataParser`（`dbInfo` はそのプロパティ）に改め、`setup/request_unit_test/rest.rst` から `class_unit_test_setting-column_default_values` へ導線を張り、`setup/class_unit_test.rst` の記述例に `<property name="dbInfo" ref="dbInfo"/>` を補った。`reviews/page-request_unit_test_rest.md` に D-19 として追記した |

内訳: 一致 25件 / 不一致 6件（2-7・2-11・2-14・2-16・2-21・2-29） / 未確認 0件。2-8・2-19 は根拠の一部が指示書と食い違ったが、是正対象そのものは一致していたため「一致」に数え、相違を備考に書いた。**本文に書けなかった「未確認」の事実は0件**（2-8 の小文字の実動作は未確認のままとし、本文にその旨を書いていない）。

### ゲート3 の実測値

`ja/development_tools/testing_framework/implementation/deal_unit_test/batch.rst` に対して実行した（2026-08-16、コミット `601a6d6` 時点）。

```
$ grep -c '"100"' implementation/deal_unit_test/batch.rst
0
$ grep -c '100' implementation/deal_unit_test/batch.rst
0
$ grep -c '"0"' implementation/deal_unit_test/batch.rst
10
$ grep -c '^    - 0$' implementation/deal_unit_test/batch.rst
10
$ grep -c 'expectedStatusCode' implementation/deal_unit_test/batch.rst
16
```

`"100"` 0件、`"0"` 10件（YAML）＋ Excel 形式の表のセル `0` 10件。ゲート3（`"100"` 0件・`"0"` 10件以上）を満たす。`expectedStatusCode` の16件の内訳は、YAML 10件＋表の見出しセル5件＋本文の必須カラムの説明1件である。

### 指示書の前提が誤っていた6件

| # | 指示書の前提 | 実際 |
|---|---|---|
| 2-7 | `nablarch-testing-jetty12` が何を持つかは未確認 | `nablarch-testing-jetty12@646c3d9` の `src/main/java` に `nablarch/test/core/http/dump/` の7クラスと内蔵サーバ関連3クラスがある。`src/main/resources` は無い |
| 2-11 | `tools/master_data_tool.rst` に `protect.main.resources` の誤記と存在しない `build/classes` の記述がある | `.rst` にはどちらも0件。誤記は配布物 zip 側にある。**是正対象なし** |
| 2-14 | リクエストスレッド内ループ制御ハンドラは常駐バッチのもの | `batch/nablarch_batch/architecture.rst` に `request_thread_loop_handler` は0件。`messaging/db/architecture.rst:49`・`messaging/mom/architecture.rst:95` ほかに属する。条件は `:10`・`:15`・`:17` の3箇所に掛かっていた |
| 2-16 | 根拠は `TestShot.java:193-213` | `:198-213` |
| 2-21 | 対象は `implementation/testdata_notation.rst:1154` | `:1156`（`:1154` は節のリード文） |
| 2-29 | 追加箇所は `implementation/deal_unit_test/mom.rst` | 出典 `reviews/page-request_unit_test_batch.md:193` が指摘しているのは `implementation/request_unit_test/mom.rst:10` |

このほか、根拠の側にずれがあったもの: 2-10（出典は `01_Abstract.rst:607-609` ではなく `:607-610`）、2-9（`TableDuplicator` は `MasterDataRestorer.java:283` の `static class`）、2-8（是正理由は「小文字だと動かないから」ではなく配布物と綴りを揃えるため。小文字の実動作は**未確認**）、2-19（根拠に挙がった2行の文言は「同じである」であり、同型は `db_queue.rst:6` の2ページ）、2-6（`code-block` は `:91-92` ではなく `:91-93`）、2-25（実ファイルは `nablarch/fw/web/` 配下）。

### 指示書から外れた判断

1. **2-29 の追加箇所を変えた。** 指示書の表は `implementation/deal_unit_test/mom.rst` を挙げるが、出典 `reviews/page-request_unit_test_batch.md:193` が指摘しているのは `implementation/request_unit_test/mom.rst:10` の欠落である。出典を優先した。
2. **2-31 で `db_queue.rst` を変えなかった。** 個別指示 `ntf-doc-27-db-queue.md:52`「『同じ方法で行う』以上のことを書かない」に抵触するため、中継点の `implementation/deal_unit_test/batch.rst:20` に `:ref:` を足してホップを減らした。
3. **2-13 で新しいラベルを作らなかった。** 節ラベル `request_unit_test_setting_batch-loop_handler` は存在しないため、既存のページ先頭ラベル `request_unit_test_setting_batch` を使った。
4. **2-2 で「空の場合」欄に書かなかった。** `TestShot.java:332-336` の `putIfAbsent` が `containsKey` 判定であり、空のカラムがあっても補完されないため、説明欄に「カラムを記述しない場合は」と条件を明示して書いた。
5. **2-18 で `:java:extdoc:` を使わなかった。** `MockMessagingContext` は `@Published` を持たず、リンクが解決しないおそれがあるため ``literal`` にした。

### レビュー記録への追記

- `reviews/page-deal_unit_test_batch.md` — D-10・D-11 と D-7 への追記（2-1・2-15・2-16・2-17）
- `reviews/page-request_unit_test_rest.md` — D-19（2-32）・D-20（2-25）・D-21（2-30）
- `reviews/page-request_unit_test_mom.md` — D-13（2-24）・D-14（2-29）・D-15（2-30）
- `reviews/page-deal_unit_test_mom.md` — D-12（2-18）・D-13（2-12）・D-14（2-23）

`page-request_unit_test_batch.md`・`page-request_unit_test_web.md`・`page-request_unit_test_http_messaging.md`・`page-deal_unit_test_setting_rest.md`・`page-request_unit_test_setting_http_messaging.md` には「出典から変えた点」の節が無い。2-19・2-26・2-28・2-30（batch）・2-31 の追記先が無いため、これらは追記していない。

### 他の担当への申し送り

- **§7（`TODO(NTF-MOD-*)`）の担当へ。** 2-7 の本文は `setup/request_unit_test/rest.rst:51-53` に「あるべき姿」で書いてある（`nablarch-testing-jetty12` が提供するのは内蔵サーバとリクエスト単体データ作成ツールのクラスだけで、コンポーネントの登録は行わない）。現在の不具合の挙動・回避策・注意書きは書いていない。`NTF-MOD-02-2` の判定が出たら、この段落にコメントを入れること。
- **§6-5（図）の担当へ。** `.. image::` には触れていない。`implementation/deal_unit_test/mom.rst` は 2-18 の `.. important::` を `:37-39` に挿入したため、`images/mom/send_sync_online_base.png`（`:21`）・`send_sync_online_mock.png`（`:26`）の行番号が下にずれている。
- **§4（規約の全面適用）の担当へ。** 2-14 で `setup/request_unit_test/batch.rst:16` の L3 下線を 62 → 50 に直した以外、S-04 の下線長は触っていない。今回新設・改変した見出しは `setup/class_unit_test.rst` の「デフォルト以外のトランザクションを使用する」（L3）と `setup/request_unit_test/batch.rst` の「リクエストスレッド内ループ制御ハンドラを置き換える」（L3）の2つ。どちらも下線50で書いた。
- **調整役へ。** `python3 mapping/tools/verify_glossary.py` は `RESULT: OK`（不一致0件）、`python3 mapping/tools/verify_mapping.py` は `OK: no errors` を確認した（`601a6d6` 時点）。フルビルドは実行していない。新設ラベルは `class_unit_test_setting-db_transaction` と `request_unit_test_mom-` の6件の計7件で、`ja/` 全体で衝突が無いことを確認済み。

## §6 判断済み10件の実施

担当範囲は §6-2・§6-4・§6-5・§6-6 の4節。§6-1・§6-3 は担当外。

### コミット

| # | SHA | 内容 |
|---|-----|------|
| A | `b29b68d` | §6-2-1・§6-2-2（`setup/request_unit_test/mom.rst`） |
| B1 | `c2a1ae9` | §6-2-3・§6-2-4・§6-2-5（`implementation/testdata_examples.rst`・`setup/request_unit_test/batch.rst`・`setup/class_unit_test.rst`） |
| B2 | `10c2567` | `reviews/page-*.md` 4件への根拠記録 |
| C | `a380740` | §6-5 の図4件の削除と `TODO(NTF-FIG-01..04)` の挿入 |
| D | `4b0b4dc` | §6-6（`implementation/deal_unit_test/web.rst`） |
| E | `7553b81` | 自己点検で見つけた下線長の是正2件（下記「§4 の担当へ」） |

指示書は B を1コミットとしていたが、B1・B2 に分けた。`reviews/page-*.md` には本文を入れたコミットの SHA を書く必要があり、同一コミット内に自分の SHA を書けないため。

### §6-2 実装上必須の設定の追記（5件）

いずれも出典（NTF 解説書・`nablarch-testing` のソースおよびテストリソース）を自分で開いて確認した。行番号は確認時点の実測値。

| 項番 | 追記先（現在の行） | 追記した内容 | 自分で確認した出典 | 記録先 |
|------|--------------------|--------------|--------------------|--------|
| 6-2-1 | `setup/request_unit_test/mom.rst:15` L3「メッセージ受信用のメッセージングプロバイダを登録する」 | `EmbeddedMessagingProvider` を `messagingProvider` という名前で登録する。キュー名は `TEST.REQUEST`・`TEST.RESPONSE` 固定 | `MessagingRequestTestSupport.java:108-109`（`ConfigurationBrowser.require(diConfig, "messagingProvider", false)`）・`repository/ConfigurationBrowser.java:49-56`（未登録時に `IllegalArgumentException`）・`:185-186`・`:197`（キュー名のリテラル）・`:96-97`（`stopServer()` の無条件呼び出し）・`EmbeddedMessagingProvider.java:33`・`:86` | `reviews/page-request_unit_test_setting_mom.md` §7.1 |
| 6-2-2 | 同 `:36` L3「同期応答メッセージ送信用のメッセージングプロバイダに差し替える」 | 本番と同じコンポーネント名で `RequestTestingMessagingProvider` を登録して差し替える | `RequestTestingMessagingProvider.java:130`・`:149`・`:230`・`:331-338`・`TestShot.java:167`・`setup/deal_unit_test/mom.rst:29`（同名で置き換える書き方の前例） | 同 §7.2 |
| 6-2-3 | `implementation/testdata_examples.rst:1859` L3「応答不要メッセージ送信の要求電文の期待値を記述する」 | 記載例（Excel形式・YAML形式の両方）。`design.md` §8 の3条件を満たすことを確認したうえで追加 | `DataType.java:47`・`:50`・`YamlSection.java:36-37`・`schemaFullCoverage.yaml:213-223`・`AsyncMessageSendActionForUtTest.java:26-31`・`AsyncMessageSendActionForUt.java:27-28`・`:35-37`・`TestShot.java:167`・`RequestTestingMessagingProvider.java:230`・`:245-253` | `reviews/page-testdata_examples.md` |
| 6-2-4 | `setup/request_unit_test/batch.rst:39` L3「応答不要メッセージ送信用のメッセージングプロバイダに差し替える」 | 本番と同じコンポーネント名で `RequestTestingMessagingProvider` を登録して差し替える | `batch-test-component-configuration.xml:61-63`・`RequestTestingMessagingProvider.java:464-474`（`send()` はキャッシュするだけ）・`:478-481`・`TestShot.java:167`・`:257`・`:331-338` | `reviews/page-request_unit_test_setting_batch.md` §6 |
| 6-2-5 | `setup/class_unit_test.rst:104` L3「テストデータの投入に使用するトランザクションを登録する」 | `testTran` という固定名で `SimpleDbTransactionManager` を登録する | `DbAccessTestSupport.java:42`・`:188`・`:45`・`TableData.java:103`・`:349`・`MasterDataRestorer.java:322`・`db/TransactionTemplate.java:43-50`・`framework.xml:8-12` | `reviews/page-class_unit_test.md` |

自己訂正（コミット前に出典を開き直して見つけた引用行の誤り、4件）: `RequestTestingMessagingProvider.java:329-336`→`:331-338`、`MessagingRequestTestSupport.java:106-109`→`:108-109`、`RequestTestingMessagingProvider.java:464-472`→`:464-474`、`AsyncMessageSendActionForUt.java:26-30`→`:27-28`・`:35-37`。

`testFwTran` はマスタデータ復元ツール側の設定であり、6-2-5 の対象外と判断した。

### §6-4 `htmlCheckerConfig` → `.rst` の変更なし

`design.md:387`（設定値そのものはツールページに置き、他ページからは `:ref:` で制約だけ残す）の状態に既になっていることを確認した。よって変更もコミットも行っていない。

- 設定値と記載例: `tools/html_check_tool.rst:114`・`:120`
- 制約と相互参照: 同 `:138` の `.. important::`（「どちらか一方を設定する（`:ref:`request_unit_test_setting_web``\ 参照）」）・同 `:187`
- 参照側: `setup/request_unit_test/web.rst:67-68`・`:86`・`:154`

`#27-05`（`setup/master_data_restore.rst` の tip の但し書き）は §2-9 で処理済みであることを確認した。当該 tip（`:59-61` 付近）に `:ref:`マスタデータ投入ツール <master_data_tool>`` を伴う但し書きが入っている。

### §6-5 本文と食い違う図の削除（4件・ゲート11）

png ファイルは4件とも削除していない（`ls` で存在を確認済み）。TODO に `guide/` のパスは1件も含まれていない（実測0件）。

| TODO | 削除した図 | 図が伝えていた構造 | 補った本文（現在の行） |
|------|-----------|--------------------|------------------------|
| `NTF-FIG-01` | `implementation/request_unit_test/rest.rst` の `images/rest/rest_request_unit_test_structure.png` | テストクラスと内蔵サーバ・Nablarch AF・Action・テーブルの関係 | 同 `:23` に散文で追加（`RestTestSupport`／`SimpleRestTestSupport` の継承関係、内蔵サーバの保持、リクエストの流れ、期待値との照合） |
| `NTF-FIG-02` | `implementation/request_unit_test/mom.rst` の `images/mom/send_sync.png` | 同期応答メッセージ送信の構成（テストクラス・`MessageSender`・プロバイダ・テストデータ） | 同 `:41` に散文で追加（`BatchRequestTestSupport` 継承、`TestShot`、`MainForRequestTesting`、`MessageSender`、`RequestTestingMessagingProvider` によるアサートと応答電文の生成） |
| `NTF-FIG-03` | 同ページの `images/mom/real_request_test_class.png` | メッセージ受信のテストクラス構成 | 同 `:22` に散文で追加（`StandaloneTestSupportTemplate`←`MessagingRequestTestSupport`←`MessagingReceiveTestSupport` の継承、`TestShot`、`MainForRequestTesting`、`DbAccessTestSupport`／`MQSupport`） |
| `NTF-FIG-04` | `implementation/request_unit_test/batch.rst` の `images/batch/batch_request_test_class.png` | バッチのテストクラス構成 | 同 `:23` に散文で追加（`BatchRequestTestSupport` 継承、`TestShot`、`MainForRequestTesting`、`DbAccessTestSupport`／`FileSupport`） |

図と一緒に、`send_sync.png` の誤ったクラス名だけを説明していた `.. tip::` を削除した（図が無くなると意味を成さないため）。その tip が持っていた事実（`BatchRequestTestSupport` を使う）は上記の散文に残してある。

作図元ファイル: `NTF-FIG-01` は `images/rest/rest_request_unit_test_structure.xlsx`、`NTF-FIG-02` は `images/mom/send_sync.xlsx`（§5-3 での退避後のパス。TODO 本文にもその旨を書いた）。`NTF-FIG-03`・`NTF-FIG-04` には作図元ファイルが存在しない旨を TODO に書いた。

`grep -rn 'TODO(NTF-FIG-' ja/` の実測結果（4件、ゲート10の前半）:

```
ja/development_tools/testing_framework/implementation/request_unit_test/mom.rst:17:.. TODO(NTF-FIG-03)
ja/development_tools/testing_framework/implementation/request_unit_test/mom.rst:35:.. TODO(NTF-FIG-02)
ja/development_tools/testing_framework/implementation/request_unit_test/batch.rst:17:.. TODO(NTF-FIG-04)
ja/development_tools/testing_framework/implementation/request_unit_test/rest.rst:17:.. TODO(NTF-FIG-01)
```

#### `#27-09 decide-2`（S-10 規約5）の確認 → 変更なし

`implementation/deal_unit_test/mom.rst` の `.. image::` は4件（`:21`・`:26`・`:80`・`:85`）。このうち記載例は `:80` の `send_sync_test_data_no.png` だけで、直前の `:78` に「応答電文を2件記述した場合の例を Excel 形式で示す」がある（S-10 規約5 の由来となった文そのもの）。残る3件は記載例ではなく処理フロー図・動作説明図であり、規約5 の対象外と判断した。`:85` の `send_sync_response_count_change.png` は png を開いて内容を確認したうえでの判断で、打鍵→Excelファイルの書き換え→再打鍵という手順の流れを示す図である。よってこのページに変更は不要。

#### `#27-10 decide-2` の確認のみ

`implementation/deal_unit_test/http_messaging.rst` に `.. image::` は0件、「Excel」の出現も0件（実測）。食い違う図が残っていないことを確認した。TODO の対象外という指示書の判断のとおり、何も行っていない。

### §6-6 「現在検討中」の tip の削除 → ディレクティブごと削除

`implementation/deal_unit_test/web.rst` の `:44-45` にあった次の tip を、ディレクティブごと削除した（コミット `4b0b4dc`）。

```rst
.. tip::
  画面ハードコピー取得ツール、DBダンプ取得ツール等のテスト補助ツールについては現在検討中。
```

削除単位の判断根拠: tip の本文がこの1文だけで、削除すると空のディレクティブが残るため。前後（`* DBダンプ（テスト実行前および実行後）` の箇条書きと L3「二重サブミット防止機能を確認する」）は tip を参照しておらず、削除しても文のつながりは崩れない。

### 他の担当への申し送り

- **§5-3（画像の退避）の担当へ。** `TODO(NTF-FIG-02)` の本文に、作図元として `images/mom/send_sync.xlsx` という退避後のパスを書いてある。退避先がこのパスと異なる場合は、`implementation/request_unit_test/mom.rst:35-39` の TODO を直すこと。
- **§7（`TODO(NTF-MOD-*)`）の担当へ。** `implementation/request_unit_test/` の3ページ（`rest.rst`・`mom.rst`・`batch.rst`）は、いずれも `:17` に `TODO(NTF-FIG-*)` を入れたため、`:17` 以降の行番号が下にずれている。`mom.rst` は `:35` にもう1件入れたため、そこから下はさらにずれる。
- **§4（規約の全面適用）の担当へ。** §6-2 で新設した L3 見出しは4件（`setup/request_unit_test/mom.rst:15`・`:36`、`setup/request_unit_test/batch.rst:39`、`setup/class_unit_test.rst:104`）と、`implementation/testdata_examples.rst:1859` の L3（配下に L4「Excel形式の場合」「YAML形式の場合」の対を持つ）。下線長は S-04（既定値 L3・L4 は 49、タイトルの表示幅が超えるときだけ表示幅まで伸ばす）に照らして自分で実測し、表示幅より1文字長かった2件をコミット `7553b81` で是正した（`setup/request_unit_test/mom.rst:15` の下線 53→52、`setup/class_unit_test.rst:104` の下線 55→54）。新設 L3 5件の現在値は 52・62・62・54・50 で、いずれも表示幅と一致する。ただし新設した L4 2件は下線 50 で書いており、既定値 49 と一致しない。`implementation/testdata_examples.rst` の既存の L4 は 60 件すべてが 50（実測）であり、同一ページ内で揃える方を採ったためである。S-04 が挙げる「49 とすべき箇所を 50 にしている」不一致 94 件と同じ性質なので、全面適用の際にまとめて直すこと。
- **調整役へ。** `sphinx-build` によるフルビルドは実行していない（指示による）。

## §7 モジュール判定待ちの TODO

`ntf-doc-28-decide-disposition.md:671-721` による。7件すべてを reST コメントとして本文の直前に置いた。`sphinx.ext.todo` は使っていない（`ja/conf.py` 未変更）。

コミットは2本。`db738c0`（本文の書き換えを伴う2件＋`reviews/` の追記）、`daa101c`（残り5件の TODO 配置）。

### 7-3. 入れた TODO の一覧

| 識別子 | ファイル（`ja/development_tools/testing_framework/` 配下） | 依頼書 | 節 |
|---|---|---|---|
| `NTF-MOD-01-2` | `tools/testdata_converter.rst` | `ntf-mod-01-nablarch-testing-converter.md` | §3（事象2: 同名で拡張子違いの Excel ブックが同居すると、片方の変換結果が無言で失われる） |
| `NTF-MOD-02-2` | `setup/request_unit_test/rest.rst` | `ntf-mod-02-nablarch-testing.md` | §3-3（`nablarch.test.core.http.dump` の実装がどのモジュールにあるか） |
| `NTF-MOD-02-3` | `implementation/deal_unit_test/mom.rst` | `ntf-mod-02-nablarch-testing.md` | §4（事象3: YAML形式のテストデータで、同期応答メッセージのモックアップの再読み込みが働かない） |
| `NTF-MOD-02-4` | `tools/master_data_tool.rst` | `ntf-mod-02-nablarch-testing.md` | §5（事象4: マスタデータ投入ツールが、YAML形式のパーサ設定下で無言で0件になる） |
| `NTF-MOD-03-1` | `setup/junit5_extension.rst` | `ntf-mod-03-nablarch-testing-junit5.md` | §2（観測した事実。`resolveTestRules()` に登録した `TestRule` はテスト本体を包めない） |

行番号は本表でも統合表（`checks/task-last.md` §8「TODO 台帳（統合）」）でも持たない。以後の加筆で動くためで、現在地は `grep -rn 'TODO(NTF-' ja/` で取る。

`#28` の §7 で入れた `TODO(NTF-MOD-*)` は7件だが、本表は現在5行である（`#28` が入れた TODO は §7 の `NTF-MOD-*` 7件だけではなく、§6-5 の `TODO(NTF-FIG-01..04)` 4件を含めて計11件である）。`NTF-MOD-02-1` は判定（事象1=仕様・解説書側対応）と user 判断（本文は据え置く）を受けて `#29` で削除したため、本表から外した（下の「本文の書き換えを伴った箇所」の `NTF-MOD-02-1` の項に追記した2026-08-19 の段落を参照）。`NTF-MOD-01-1` も、依頼書 §2 の3事象の判定がすべて返って `#31` で削除したため、同じ扱いで本表から外した（`checks/task-last.md` §8「TODO 台帳（統合）」の削除記録の段落と、`checks/task-31.md`「判定の内訳（3事象）」を参照）。

節番号は3つの依頼書を実際に開いて確認した（指示書 `:699-707` の表を写していない）。指示書の表は「事象1」「事象2」といった事象番号で書かれており、依頼書の節番号は事象番号と1対1に対応する（`ntf-mod-01` は事象1=§2・事象2=§3、`ntf-mod-02` は事象1=§2・事象3=§4・事象4=§5）。

置いた位置の判断（`:693`「本文の直前に置く」）:

- `01-1` — L3「意味を変えずに往復できる」の直前。判定に依存するのはこの節の主張そのもののため、節ごと指す位置にした。見出しの下線と本文の間にコメントを挟むと S-04「L3・L4の見出しは下線の直後に空行を置かない」に反するため、見出しの前に置いた。`01-2`・`03-1` も同じ理由で見出しの前
- `01-2` — 「使用方法」のリードの次、`.xls` と `.xlsx` をどちらも変換対象とすると書いた段落の直前
- `02-1` — 起動用スクリプトを配置する段落の直前
- `02-2` — `nablarch-testing-jetty12` の提供範囲を書いた `.. important::` の直前
- `02-3` — テストデータのタイムスタンプ更新による再読み込みを書いた段落の直前
- `02-4` — 削除した `.. important::` の跡地（「機能概要」の末尾、`.. _master_data_tool-setup:` の直前）
- `03-1` — L3「JUnit 4のTestRuleを再現する」の直前

### 本文の書き換えを伴った箇所

**`NTF-MOD-02-1` — `tools/request_data_tool.rst`（`#27` の判断の巻き戻し）**

- `grep -n 'httpDump'` で全件（`:62`・`:82`・`:100`。追記前の行番号）を洗い出したうえで、`:82` の「配置した起動用スクリプト(httpDump.bat)を選ぶ。」を「配置した起動用スクリプトを選ぶ。Windowsの場合はバッチファイル(httpDump.bat)を、Linuxの場合はシェルスクリプト(httpDump.sh)を選ぶ。」に戻した（現在は `:86`）。出典 `2e501ad:.../02_SetUpHttpDumpTool.rst:91-92` の「Windowsの場合はバッチファイル(httpDump.bat)を、Linuxの場合はシェルスクリプト(httpDump.sh)を選択する。」に対応する。`git show 2e501ad:<path>` で出典を開いて確認した
- `:60`（追記前）の「次のファイルを、pom.xmlと同じディレクトリに配置する。」は「次の起動用スクリプトを、」に改めた。`:66` の `:download:` は `httpDump.bat` の1件のままとした。**指示書 `:703`「起動スクリプト名は `httpDump.bat` / `httpDump.sh` の双方を示す」に対する判断**: 存在しないファイルを `:download:` で指すと `sphinx-build` が WARNING を出し、ゲート7（WARNING・ERROR 0件）に反する。`ja/.../tools/downloads/request_data_tool/` にあるのは `httpDump.bat` の1ファイルだけである（`ls` で実測）。`httpDump.sh` を新規に作って配布物に足すことは、依頼書 `ntf-mod-02` §2-2 の2「Linux 用の起動スクリプトを配布物に含めるべきか」がまさに判定を求めている事項であり、解説書側で先に決めない。したがって双方の名前は本文（`:86`）で示し、`:download:` は判定が返るまで増やさない
- `:104` の「Windows上で本ツールを起動するとコマンドプロンプトが現れる」は出典（`01_HttpDumpTool.rst` の tip）どおりであり、「Windowsのみ」とは書いていないため触っていない
- `reviews/page-request_data_tool.md` の「意図して落とした出典」表の `02_SetUpHttpDumpTool.rst:91-92` の行に、取り消した旨・戻した先・`:download:` を増やさない理由を追記した。あわせて同ファイルの `current-0349` の行（「`httpDump.sh` の記述は落とした」）も実態に合わせた

**判定（2026-08-19、`#29` で追記）**: 事象1は**仕様（解説書側の対応のみ）**と判定された（`nablarch-testing` `8530497:docs/pr75/steering.md`。本作業ディレクトリからは参照できないため user が作業指示に引用した文面による）。`httpDump.sh` は配布物に含まれない。そのうえで **user 判断により、本文は現行解説書に合わせて据え置く**（「Windowsの場合はバッチファイル(httpDump.bat)を、Linuxの場合はシェルスクリプト(httpDump.sh)を選ぶ。」の1文と `:download:` 1件を変えない。TODO 3行の削除で行番号が動き、2026-08-19 時点ではそれぞれ `:82`・`:62`）。現行解説書 `2e501ad:ja/.../01_HttpDumpTool/02_SetUpHttpDumpTool.rst:59`・`:91-92` と同じ形であり、意図した状態である。待つものが無くなったため `TODO(NTF-MOD-02-1)` の3行を削除した。**上の3項目の記述はそのまま有効で、本文への追加の書き換えは行っていない。**

**`NTF-MOD-02-4` — `tools/master_data_tool.rst`（`.. important::` の削除）**

- 削除したのは `:26-28` の `.. important::` ブロック全体である。本文は「マスタデータファイルは Excel 形式で記述する。コンポーネント設定ファイルの `testDataParser` に YAML 形式用のパーサを設定しているプロジェクトでは、本ツールを使用できない（共通設定 参照）。この場合、Excel 形式のマスタデータファイルを指定しても投入の対象が0件になり、エラーにもならない。」の3文だった
- **削除範囲の判断理由**: 指示書 `:706` は「「本ツールを使用できない」以下の記述を落とす」と指定している。2文目は「YAML 形式用のパーサを設定しているプロジェクトでは」という条件節と「本ツールを使用できない」という帰結で1文をなしており、帰結だけを落とすと文が成立しない。したがって2文目・3文目は文ごと落とす。残るのは1文目の「マスタデータファイルは Excel 形式で記述する。」だけになるが、(1) 同じ事実はリード文 `:10`「投入するデータは、自動テストのテストデータと同じ書式で Excel ファイルに記述する。」と「使用方法」の「マスタデータを記述する」（`MASTER_DATA.xls` に記述する／`masterdata.file` の既定値 `MASTER_DATA*.xls`）に既に書かれており、(2) `style.md` S-06 は `important` を「無視すると不具合・非推奨機能の誤用・データ不整合につながる、読者が必ず守るべき注意事項」に限っている。帰結を失った1文だけを `important` として残すと、既出の事実に不相応な重みが付く。よってブロックごと削除した
- このブロックは出典由来ではなく、`#27-05` のレビュー（`reviews/page-master_data_tool.md` の「設計 M-2」）で新設したものである。出典行の消化には影響しない。削除した旨は同ファイルの該当行に追記した
- 削除で参照が失われるものは無い。`:ref:`共通設定 <testing_framework_common>`` は同ページ `:41`（前提事項）にも残っている

**`NTF-MOD-02-4` の波及（他ページの同趣旨の記述）**

- `grep -rn 'マスタデータ投入ツール\|master_data_tool' ja/ --include=*.rst` の結果、`master_data_tool.rst` 以外のヒットは `tools/index.rst:11`（toctree）・`setup/master_data_restore.rst:61`・`:175`・`implementation/testdata_notation.rst:40` の4件。いずれもバックアップ用スキーマへの投入範囲・依存関係の解析順・導線の話であり、形式（Excel/YAML）による使用可否には触れていない
- `grep -rn '使用できない\|使えない\|利用できない' ja/development_tools/testing_framework/ --include=*.rst` のヒットは4件（`implementation/class_unit_test/entity.rst:119`・`:287` は入れ子 Form、`implementation/testdata_notation.rst:962` はデータ型名称、`tools/html_check_tool.rst:36` は HTML5）。いずれもマスタデータ投入ツールとは無関係である
- **したがって波及して処理した箇所は無い。**

### 指示書から外れた判断

1. **`:download:` に `httpDump.sh` を足さなかった**（上記 `NTF-MOD-02-1`）。ビルド WARNING とゲート7、および依頼書 `ntf-mod-02` §2-2 の判定範囲に触れるため
2. **`NTF-MOD-02-2` の TODO の1行目・3行目の文言を変えた。** 他の6件は「…。判定待ち。」「仕様と判定された場合は本文を書き直す。」で揃えたが、02-2 は仕様かどうかの判定ではなく「`nablarch.test.core.http.dump` の実装がどのモジュールにあるか」という事実の照会（依頼書 §3-3）である。「回答待ち。」「回答の内容に応じて本文を書き直す。」とした。書式（3行・1行目に事象・2行目に依頼書のパスと節・3行目に扱い）は指示書 `:685-693` のとおり保っている

### `grep -rn 'TODO(NTF-MOD-' ja/` の実測（2026-08-16、`daa101c` 時点。ゲート10 の前半）

行番号は当時のもの。現在地は `grep -rn 'TODO(NTF-' ja/` で取る。下のブロックは当時の証拠としてそのまま残す。

「ゲート10 の前半」としているのは、当初「ゲート9」と書いていたのが誤りで、ゲート9 は §5-2 直前の `guide/development_guide` の残存確認であるため。

当時（`daa101c` 時点）に入れた TODO は7件で、当時の 7-3 の表と完全に一致していた。`#29` で `NTF-MOD-02-1` を削除したため、現在の 7-3 の表（6行）とは `NTF-MOD-02-1` の1件だけずれる。下のブロックは当時の証拠としてそのまま残す。

```
ja/development_tools/testing_framework/implementation/deal_unit_test/mom.rst:83:.. TODO(NTF-MOD-02-3): YAML形式で同期応答メッセージのモックアップの再読み込みが働かない。判定待ち。
ja/development_tools/testing_framework/setup/junit5_extension.rst:395:.. TODO(NTF-MOD-03-1): resolveTestRules() に登録したTimeoutがテスト本体に効かない。判定待ち。
ja/development_tools/testing_framework/setup/request_unit_test/rest.rst:51:.. TODO(NTF-MOD-02-2): nablarch.test.core.http.dump の実装を持つモジュールが未特定。回答待ち。
ja/development_tools/testing_framework/tools/master_data_tool.rst:26:.. TODO(NTF-MOD-02-4): マスタデータ投入ツールがYAML形式用のパーサ設定下で無言で0件になる。判定待ち。
ja/development_tools/testing_framework/tools/request_data_tool.rst:60:.. TODO(NTF-MOD-02-1): リクエスト単体データ作成ツールのLinux用起動スクリプトが配布物に無い。判定待ち。
ja/development_tools/testing_framework/tools/testdata_converter.rst:22:.. TODO(NTF-MOD-01-1): テストデータ変換ツールの往復非可逆。判定待ち。
ja/development_tools/testing_framework/tools/testdata_converter.rst:75:.. TODO(NTF-MOD-01-2): 同名で拡張子違いのExcelブックが同居したときの変換対象の扱い。判定待ち。
```

ゲート10（ビルド出力 `_build/html` に `TODO(NTF-MOD-` が0件）は未実施。フルビルドは調整役がまとめて行うため（指示による）。

### 他の担当への申し送り

- **調整役へ。** `sphinx-build` は実行していない。ゲート10 の確認とあわせて、`tools/master_data_tool.rst` の `important` を1件削除したことによる差分（`reviews/page-master_data_tool.md` の G6 の実測「`tip` 2件・`important` 3件」は現在 `important` 2件）を、必要なら是正すること
- **調整役へ。** §7 の着手時点で、`implementation/request_unit_test/` の3ページと `implementation/deal_unit_test/mom.rst` などは §2・§6 担当の変更で行番号がずれていた。行番号は動き続けるため、7-3 の表からも統合表（`checks/task-last.md` §8）からも外した。現在地は `grep -rn 'TODO(NTF-' ja/` で取る
- **判定が返ったときの担当へ。** `NTF-MOD-02-1` が「不具合（Linux 用スクリプトを配布物に含める）」と判定された場合は、`tools/downloads/request_data_tool/` に `httpDump.sh` を置き、`tools/request_data_tool.rst:66` の `:download:` を2件にすること。`NTF-MOD-02-4` が「仕様」と判定された場合は、`tools/master_data_tool.rst:26` の跡地に制約を書き戻すことになる
- **上の申し送りは `#29` で消化済み（2026-08-19 追記）。** `NTF-MOD-02-1` は「仕様」と判定されたため `:download:` は1件のまま据え置き、TODO を削除した（上の「本文の書き換えを伴った箇所」の判定の段落）。`NTF-MOD-02-4` は前半だけが「仕様」と確定したため、跡地には前半の制約1文だけを `.. important::` で書いた。**上に全文を記録した3文のうち「マスタデータファイルは Excel 形式で記述する。」と「…本ツールを使用できない（共通設定 参照）。」の2文は書き戻さない。** 後半（YAML形式のマスタデータファイルへの対応）が `nablarch-testing` の #22 で対応予定であり、#22 の完了後にこの2文は誤りになるためである（`checks/task-last.md` §8「TODO 台帳（統合）」の `NTF-MOD-02-4` の行）

## §4 記録の是正・未確認の解消

15件すべてを一次情報で確認した。**実際に書き換えたファイルは `steering.md` 1件のみ**（4-7）。`ja/` 配下の `.rst` と `mapping.csv`・`_batch/` は1バイトも変更していない。

| 項番 | 判定 | 実施 |
|---|---|---|
| 4-1 | 不一致（`mapping.csv` 側が誤り） | 記録のみ（直さない。理由は後述の共通判断） |
| 4-2 | 不一致（`mapping.csv` 側が誤り） | 記録のみ（**直すとゲート5が `exit 1` になる**） |
| 4-3 | 不一致（本文が1行落としている） | 記録のみ（`mapping.csv` に表す欄が無い） |
| 4-4 | 不一致（1行が2箇所に分割配置） | 記録のみ（忠実な是正は行の分割＝構造変更） |
| 4-5 | 不一致（`note` が出典どおりで実装と食い違う） | 記録のみ（`#27-03` が「出典に戻すな」と明記） |
| 4-6 | 粒度を決定 | 記録のみ（既存ラベルで足りる。`mapping.csv` 変更不要） |
| 4-7 | 表そのものが存在しなかった | **`steering.md` に参照リポジトリ表を新設し4件をピン** |
| 4-8 | 不一致＋一部未確認 | 記録＋申し送り（本文の変更はしない） |
| 4-9 | 一致（是正不要） | 記録のみ |
| 4-10 | 一致（是正不要） | 記録のみ |
| 4-11 | 不一致（前提に出典が無い） | 記録＋**申し送り**（§2 は当該文を直していない） |
| 4-12 | 飛び先は妥当だが読者は無関係な記述を読む | 記録＋申し送り |
| 4-13 | 飛び先の6例すべてが別の題材 | 記録＋申し送り |
| 4-14 | **指示書の前提が誤り**（3件中2件もDBキューに効く） | 記録のみ（是正不要） |
| 4-15 | 2ページで件数表がずれ | 記録のみ（指示書は履歴として残す） |

内訳: **是正した 1件**（4-7）／**記録のみ 10件**（4-1〜4-6・4-9・4-10・4-14・4-15）／**申し送りを含む 4件**（4-8・4-11・4-12・4-13）。

### 着手時点の実測値（ベースライン）

```
$ cd .rn/20260724-ntf-yaml-support && python3 mapping/tools/verify_mapping.py
Loaded 597 rows from mapping.csv
lines total (all rows): 12986
lines total (excluding DROP): 11983
candidate duplicate destinations: 43 / reference-only sections: 2
intro section split advisories: 5 / part2 optional: 18
OK: no errors      exit=0
```

`csv.DictReader` によるレコード数 597。**§4 完了時点で再実行し、上記と完全に同一・`exit=0`・597行であることを確認した**（`mapping.csv` を触っていないため当然だが、実測して記録する）。

---

### 4-1〜4-5 共通の判断 — 5件とも「直さずに逸脱として記録する」を選ぶ

指示書 `ntf-doc-28-decide-disposition.md:456` が「`_batch/` 経由の正規の手順で直すか、直さずに `checks/task-28.md` に逸脱として記録するかを CC が選び、選んだ理由を書くこと」と選択を明示的に委ねている。**5件とも後者を選んだ。**

#### まず `_batch/` 経由の手順が何をするかを実物で確認した

- `mapping/tools/build_mapping.sh`（92行、全文を読んだ）が生成するのは `sections-current.csv` と `sections-input.csv` の2つだけである（`:20-21` `OUT_CURRENT`・`OUT_INPUT`）。**このスクリプトは `mapping.csv` を生成しない。**
- `mapping.csv` の再生成手順は `checks/task-20.md:520`・`checks/task-26.md:69` に記録されている次の形である。すなわち `_batch/batch-*.csv` を編集し、連結して `mapping.csv` を作り直し、md5 が一致することを確かめる。

  ```
  { head -1 _batch/batch-01.csv; for f in _batch/batch-*.csv; do tail -n +2 "$f"; done; } > /tmp/regen.csv
  md5sum mapping/mapping.csv /tmp/regen.csv
  ```
- `mapping/tools/verify_mapping.py`（645行）の `load_rows()` は `mapping.csv` があればそれを、無ければ `_batch/batch-*.csv` の連結を読む。`check_intro_section_split` は `heading_path` の末尾が `(L2直下)` の行について `dest_section` が兄弟行の `dest_section` 集合に無ければ **ERROR（`exit 1`）**、`(L1直下)`・`(冒頭)` なら advisory（`note` に `[セクション境界]` を要求）という判定である。

#### 実際に `_batch/` を書き換えてシミュレーションした（作業ツリー外の複製で実施）

`mapping/` 一式を scratchpad へ複製し、`verify_mapping.py` の `REPO_ROOT` 解決だけを固定値に置き換えて（複製先では `git rev-parse --show-toplevel` が `fatal: not a git repository` で落ちるため。**実ファイルは変更していない**）、2通り試した。

| 試行 | 変更内容 | 結果 |
|---|---|---|
| 1 | 4-1・4-2・4-4 の3件を是正 | **`exit 1`**。`1 error(s): current-0269 ((L2直下)): dest_section='機能概要' not among sibling dest_section values ['使用方法']` |
| 2 | 4-1・4-4 の2件のみ是正 | `exit 0`。差分は advisory 1件のみ（`[第3部 … リクエスト単体テスト（HTTPメッセージング） > 機能概要]: 2 row(s) → 1 row(s)`）。行数・総行数は不変 |

#### 選んだ理由（5件を一括で「記録のみ」にする根拠）

1. **4-2 は正規の手順で直すとゲート5（`verify_mapping.py` が `exit 0`）を破る。** `current-0269` の兄弟は `current-0270` 1件だけで、その `dest_section` は `使用方法`。`current-0269` を `機能概要` にすると兄弟集合に無くなり `(L2直下)` の ERROR になる。回避するには `current-0270` も `機能概要` に変えるしかないが、`current-0270`（`JUnit5_Extension.rst:147-168`、22行）の実際の配置は `setup/junit5_extension.rst:129` 「BasicHttpRequestTestTemplateを使用する」＝ `使用方法`（`:75`）配下であり、**正しい行を誤りに変えることになる。** これは `#5d` STEP7 が解消したのと同型の ERROR（`checks/task-05d.md:141`）で、そこへ戻すことになる。
2. **一部だけ直すと台帳の信頼性が下がる。** 4-2 を直せない以上、直せる分だけ直すと「印の無い行は正しい」と読めなくなる。5件すべてを未是正のまま1箇所に列挙するほうが、次に読む人が漏れなく拾える。
3. **4-3 は `mapping.csv` に表す欄が無い。** 行単位の部分不採用を記録する列が存在しない（`reviews/page-request_unit_test_http_messaging.md:133` が同じ理由で記録に留めている）。
4. **4-4 の忠実な是正は行の分割**（1行→2行、597→598行）であり、§4 が授権していない構造変更になる。
5. **4-5 は「出典に戻すな」と既に決まっている。** `reviews/page-testdata_converter.md:77` が「`mapping.csv` の `note` 列は出典どおりのままなので、後続で『出典に戻す』是正をしないこと」と明記している。
6. `dest_section` を動かすと `volume.md` の `dest_section` 別集計（第2部 機能概要 96／使用方法 1334 → 4-1・4-2 の両方を当てた場合 122／1308）が古くなるが、`volume.md` は §4 の変更対象に入っていない。

**選ばなかった方（＝正規の手順で直す）の不利益**: 上記1のとおりゲート5を破る、または `current-0270` を誤りにする。加えて `volume.md` の再集計が §4 の範囲外で必要になる。

**この選択の不利益（明記する）**: `mapping.csv` に既知の誤りが5セル残る。`#last` で `mapping.csv` から配置を再導出すると、この5件は誤ったまま再現する。**緩和として、各項に「正しい値」を1行で書いておく。** 直す判断が出たときはこの値をそのまま当てればよい。

---

### 4-1. `current-0178` の `dest_section`

- **台帳**: `mapping/_batch/batch-03.csv` の `current-0178`。出典 `05_UnitTestGuide/…/01_Abstract.rst:671-688`（18行）、`disposition=MOVE`、`dest_page=JUnit 5用拡張機能`、**`dest_section=機能概要`**
- **実際の配置**: `ja/development_tools/testing_framework/setup/junit5_extension.rst:180` 「JUnit 4で書いたテストをJUnit 5上で実行する」。同ファイルの L2 見出しは `:14` 機能概要／`:75` 使用方法／`:225` 拡張例 であり、`:180` は **`使用方法` 配下**
- **結論**: 台帳が誤り。正しい値は `dest_section=使用方法`
- **波及**: `current-0178` の兄弟は `current-0179`（機能概要）・`current-0180`（使用方法）で、`使用方法` は既に兄弟集合にある。単独で直せば `exit 0` のまま（シミュレーション試行2で実測）
- **実施**: 記録のみ。理由は上記の共通判断（特に2・6）

### 4-2. `current-0269` の `dest_section`

- **台帳**: `mapping/_batch/batch-14.csv` の `current-0269`。出典 `06_TestFWGuide/JUnit5_Extension.rst:101-144`（44行）、`disposition=MOVE`、**`dest_section=使用方法`**
- **実際の配置**: `setup/junit5_extension.rst:26` 「Extensionクラスと合成アノテーションの一覧」＝ **`機能概要`（`:14`）配下**
- **結論**: 台帳が誤り。正しい値は `dest_section=機能概要`
- **波及**: **直すと `verify_mapping.py` が `exit 1`**（試行1で実測）。兄弟は `current-0270` の1件のみで `使用方法`。回避には `current-0270`（実配置は `:129` 「BasicHttpRequestTestTemplateを使用する」＝ `使用方法`）を誤らせるしかない
- **実施**: 記録のみ。**5件を一括で記録のみにした最大の理由がこの行である**

### 4-3. `input-0027` の1行が本文に載っていない

- **台帳**: `mapping/_batch/batch-10.csv` の `input-0027`。出典 `.rn/20260724-ntf-yaml-support/input/ntf-doc-terms.md:399-411`（13行）、`disposition=MERGE`、`dest_page=リクエスト単体テスト（HTTPメッセージング）`、`dest_section=使用方法`
- **実際の本文**: `ja/development_tools/testing_framework/implementation/request_unit_test/http_messaging.rst`（全42行）の `:29-42` の `list-table` は3行（`同期応答メッセージ送信`／`送信キュー・受信キュー`→`通信先`／`RequestTestingMessagingProvider`→`RequestTestingMessagingClient`）。出典にある `MockMessagingContext`→`MockMessagingClient` の行は**無い**
- **結論**: 本文が出典の1行を落としている（`reviews/page-request_unit_test_http_messaging.md:133` が既に記録済み）
- **実施**: 記録のみ。`mapping.csv` は行単位の部分不採用を表せない（`disposition` は行全体にしか付かない）。**本文に足すかどうかは `ja/` の変更になるため申し送り対象だが、`#27-15` のレビューが「読み替え表に載せる語を絞る」判断として意図的に落としたものであり、是正を推奨しない**

### 4-4. `current-0069` の `dest_section`

- **台帳**: `mapping/_batch/batch-21.csv` の `current-0069`。出典 `06_TestFWGuide/http_send_sync.rst:6-15`（10行）、`disposition=REFERENCE`、**`dest_section=機能概要`**
- **実際の配置**: `implementation/request_unit_test/http_messaging.rst:15`（機能概要）と `:36-37`（使用方法 > 用語を読み替える、`:24`）の**2箇所に分かれている**（`reviews/page-request_unit_test_http_messaging.md:94` D-4 が記録）
- **結論**: 台帳の1行では実配置を表せない。忠実に直すなら `current-0069-a`／`-b` への分割（597→598行）
- **波及**: `dest_section` を `使用方法` に変えるだけなら兄弟が居ないため `exit 0`（試行2で実測）。ただし `[第3部 … リクエスト単体テスト（HTTPメッセージング） > 機能概要]` の reference-only advisory が 2 row(s) → 1 row(s) に変わる
- **実施**: 記録のみ。行分割は §4 が授権していない構造変更で、`#5c`（`DROP` 全件レビュー）や `#5d` のような専用タスクの範疇である

### 4-5. `input-0198-b` の `note`

- **台帳**: `mapping/_batch/batch-02.csv` の `input-0198-b`。出典 `.rn/20260724-ntf-yaml-support/input/testdata-converter-design.md:295`（1行）、`disposition=MERGE`、`dest_page=テストデータ変換ツール`
- **食い違い**: 出典は変換ツールがリンタを通す前提で書かれているが、実装ではリンタが変換の処理経路に組み込まれていない（`reviews/page-testdata_converter.md:67` — `grep -rn 'YamlTestDataValidator' src/main/` の該当が自クラスの3行のみ）
- **結論**: 本文は実装に合わせて既に書かれており（`design.md` §8「出典と実装が食い違う場合は実装を優先する」）、`note` だけが出典どおりの文言で残っている
- **実施**: 記録のみ。`reviews/page-testdata_converter.md:77` が「`note` 列は出典どおりのままなので、後続で『出典に戻す』是正をしないこと」と明示的に決めており、`:176` に逸脱として記録済み。**`note` を実装側に書き換えると、この既決の判断と衝突する**

---

### 4-6. `current-0196` の飛び先の粒度

- **現状の本文**: `ja/development_tools/testing_framework/implementation/class_unit_test/component.rst:313`

  > 外部キーが設定されたテーブルに準備データを登録する場合は、テーブルの親子関係を判断して削除と登録が行われる。詳細は\ :ref:`マスタデータ復旧機能 <master_data_restore>`\ を参照。

  飛び先 `master_data_restore` は `setup/master_data_restore.rst:1` の**ページ先頭ラベル**である（`reviews/page-component_unit_test.md:143` `decide-2`）
- **出典**: `2e501ad:…/06_TestFWGuide/02_DbAccessTest.rst:547` が「詳細は :ref:`MasterDataRestore-fk_key` を参照。」。このラベルは `2e501ad:…/04_MasterDataRestore.rst:92` に定義され、節題は「外部キーが設定されたテーブルを使用する場合について」
- **候補となる粒度を実物で確認した**。`setup/master_data_restore.rst` に実在するラベルは4つ — `:1 master_data_restore`／`:53 master_data_restore-backup_schema`／`:63 master_data_restore-watched_tables`／`:159 master_data_restore-suppress_table_sort`。見出しは `:3` マスタデータ復旧機能／`:12` 機能概要／`:24` マスタデータを復旧する流れ／`:34` 必要となるスキーマ／`:49` 使用方法／`:55` バックアップ用スキーマを作成する／`:65` 監視対象テーブルを登録する／`:117` SQLログを出力する／`:161` テーブルの依存関係の解析を抑止する
- **旧 `MasterDataRestore-fk_key` の内容の行き先を特定した**: `setup/master_data_restore.rst:165` の1文目が旧 fk_key 節の内容そのもので、`:174-178` の `.. important::` が準備データの投入に触れている。つまり旧ラベルの後継は `:159` の `master_data_restore-suppress_table_sort`（見出し `:161` 「テーブルの依存関係の解析を抑止する」）である
- **結論**: **`master_data_restore-suppress_table_sort` を飛び先にするのが出典の粒度に一致する。** 新しいラベルを作る必要は無い。ただし現状のページ先頭 `master_data_restore` でも読者は迷子にならない（当該節は同じページ内）
- **`mapping.csv` の変更**: **不要**。`current-0196`（`mapping/_batch/batch-09.csv`、出典 `02_DbAccessTest.rst:546-548`、3行、`REFERENCE`、`dest_page=コンポーネント単体テスト`・`dest_section=使用方法`）の各列は実配置と一致しており、`:ref:` の飛び先の粒度は `mapping.csv` が表現する情報ではない
- **実施**: 記録のみ。**`component.rst:313` の `:ref:` を `master_data_restore-suppress_table_sort` に変えるかは `ja/` の変更なので申し送り**（後述）

---

### 4-7. 参照コミットのピン（**唯一、実際に書き換えた項目**）

- **指示書の前提が誤っていた**: 「`steering.md` の参照リポジトリ表に足す」とあるが、**`steering.md` に参照リポジトリ表は存在しなかった**。`grep -n "参照リポジトリ" steering.md` は0件。リポジトリ名の言及は `steering.md:291`（`#27` 以降の共通 Steps のチェック項目。`nablarch/nablarch-testing` と `nablarch/nablarch-testing-yaml` を挙げるのみでコミットは書いていない）だけである
- **ピン値の実体は別ファイルにあった**: `ntf-doc-weekend-queue.md:187` 「`nablarch-testing` は `e21bf67`、`nablarch-testing-yaml` は `190cc9a`。」。これは `#27` 限定の作業指示であり、`#28`・`#last` の担当が読むとは限らない
- **実測コマンドと出力**（2026-08-16、`git -C <repo> log -1 --format='%H %ad %s' --date=short`）:

  ```
  nablarch-testing            fdf55d4b3149f0bd6181819b88c1008cfc4970cb 2026-08-05 chore: jacoco.exec を .gitignore に追加
                              （ブランチ convert-testdata-excel-to-text）
  nablarch-testing-yaml       e69b69f124246d6658f810e9e625bf96cf79b4f1 2026-08-14 docs(steering): #14 Acceptance criteria 実行結果を記録
                              （ブランチ feature/ntf-yaml）
  nablarch-testing-converter  45194f9780f65758d8804062bd53608244293c2a 2026-08-14 docs(coverage): レビュー指摘を台帳へ反映し、実測と食い違う数値を直す
                              （ブランチ ntf-test-data-converter）
  nablarch-testing-rest       9ada31e2f6a859580d925bc63b9540b524c33b8b 2026-06-25 chore: suspend session — fix-testdataparser-usage
                              （ブランチ fix-testdataparser-usage）
  ```

  4リポジトリとも `/home/tie303177/work/nablarch/` 配下に clone 済み。**clone が無いリポジトリは無かった。** `nablarch-testing-converter` と `nablarch-testing-yaml` の実測値はレビュー役の報告値（`45194f9`・`e69b69f`）と一致し、そこから先へは動いていない
- **もっとも重要な発見**: `git -C nablarch-testing merge-base --is-ancestor e21bf67 HEAD` が**偽**。`merge-base` は `6aa6989` で、HEAD 側に14コミット・`e21bf67` 側に16コミットある。**`nablarch-testing` の作業ツリーはピン `e21bf67` の内容ではない。** 作業ツリーを直接 `grep` すると別の内容を読む（`git show e21bf67:<path>` を使う必要がある）。`nablarch-testing-yaml` は `190cc9a` が HEAD の祖先で、12コミット前進しているだけ
- **実施**: `steering.md` の `# Assumptions` 節の末尾（`:37` の直後、`# Rules` の直前）に**参照リポジトリ表を新設し、4件の行を足した**（+8行）。表が存在しなかったため「行を足すだけ」を最も近い形で満たす置き方として、既存の箇条書き（作業指示・IN側資料・トンマナ基準の並び）の末尾に追加した。**他の節は1行も変更していない**（`git diff` で確認済み。差分は `@@ -35,6 +35,14 @@` の1ハンクのみ）
- 表は「参照コミット（本刷新が根拠に使う）」と「実測 HEAD（2026-08-16）」を分けた。`nablarch-testing` は `e21bf67`、`nablarch-testing-yaml` は `190cc9a` を参照コミットとして残した（既存ページはこの2つで検証済みで、HEAD に付け替えると過去の検証記録の再現性が失われるため）。`nablarch-testing-converter` と `nablarch-testing-rest` は既存のピンが無いので実測値をそのままピンにした

---

### 4-8. surefire 2.22.0 の一次情報（別担当が一次情報で検証済み・そのまま記録）

- **現状の本文**: `ja/development_tools/testing_framework/setup/junit5_extension.rst:73` 「JUnit 5を使用するには、\ ``maven-surefire-plugin``\ が2.22.0以上である必要がある。」（`:71` 「前提事項」配下）
- **観測した事実**:
  - `nablarch-testing@e21bf67:pom.xml` — `<version>2.2.0</version>`、親は `com.nablarch:nablarch-parent:6u2`。`maven-surefire-plugin` は `:195-203` に宣言があるが `<version>` を持たず親から継承する
  - `~/.m2/repository/com/nablarch/nablarch-parent/6u2/nablarch-parent-6u2.pom:52` — `<surefire.plugin.version>2.22.2</surefire.plugin.version>`（`:91`・`:370` で使用）
  - `~/.m2/repository/com/nablarch/nablarch-parent/6-NEXT-SNAPSHOT/nablarch-parent-6-NEXT-SNAPSHOT.pom:52` — 同じく `2.22.2`（`:91`・`:399` で使用）
- **指示書の前提が誤っていた**: 指示書は「親POM は本作業環境に無い」としているが、**`~/.m2/repository/com/nablarch/nablarch-parent/` に `6u2` と `6-NEXT-SNAPSHOT` の両方が実在した**
- **結論**: 不一致（部分的）。Nablarch の親POM が実際にピンしているのは **2.22.2** であって 2.22.0 ではない。「2.22.0 **以上**」という下限値の根拠は Nablarch 側の一次情報に見当たらない。JUnit 5 側の要件と思われるが、その一次情報は本作業環境（オフライン）では取得できず**未確認**
- **実施**: 記録のみ（本文は変更しない）。**申し送り**は後述

### 4-9. HTTPメッセージ受信の実行経路（別担当が一次情報で検証済み・そのまま記録）

- **現状の本文**: `implementation/request_unit_test/http_messaging.rst:15`（`:12` 機能概要 配下）「HTTPメッセージ受信のリクエスト単体テストは、\ :ref:`リクエスト単体テスト（MOMによるメッセージング） <request_unit_test_mom>`\ の同期応答メッセージ受信と同じ方法で行う。…」
- **実装（`nablarch-testing@e21bf67`）**:
  - `MessagingRequestTestSupport.java:106-111` — `ConfigurationBrowser.require(diConfig, "messagingProvider", false)` → `messagingProvider.createContext()`
  - 同 `:185-188` — `msg.setDestination("TEST.REQUEST").setReplyTo("TEST.RESPONSE"); context.send(msg);`／`:197` — `context.receiveSync("TEST.RESPONSE", 10000)`
  - キュー名は `MQSupport.java:17 RECEIVE_QUEUE_NAME = "TEST.REQUEST"`・`:20 SEND_QUEUE_NAME = "TEST.RESPONSE"` の固定値
  - `EmbeddedMessagingProvider.java:33` — `extends JmsMessagingProvider`（組み込み ActiveMQ Artemis、`vm://0`）
- **結論**: 一致。HTTPメッセージ受信のテストは HTTP のトランスポートを一切通らず、MOM とまったく同一の経路で起動される。**本文の是正は不要**
- **副産物**: 旧解説書 `2e501ad:…/05_UnitTestGuide/02_RequestUnitTest/real.rst:15` の FQCN `nablarch.test.core.http.MessagingRequestTestSupport` は誤り（`nablarch.test.core.http` パッケージに当該クラスは無い。正しくは `nablarch.test.core.messaging.MessagingRequestTestSupport`）。**新解説書への引き写しは0件**（`git grep -c "nablarch.test.core.http.MessagingRequestTestSupport" -- ja/` が0件。自分で再実行して確認した）
- **実施**: 記録のみ

### 4-10. `implementation/class_unit_test/component.rst` の `@BeforeClass` の原因（別担当が一次情報で検証済み・そのまま記録）

- **現状の本文**: **`:121`**（`#28` §2 のコミット後に行番号が移動。指示書と `28-facts.md` が挙げる `:125` は `7e19f68` 時点の値）「``@BeforeClass``\ ・\ ``@AfterClass``\ を使用する場合、サブクラスにスーパクラスと同名で同じアノテーションを付けたメソッドを作成しない。同名のメソッドに同種のアノテーションを付けると、スーパクラスのメソッドが起動されなくなる。…」
- **実装（JUnit 4.13.1 のバイトコードを `javap` で確認。`nablarch-testing@e21bf67:pom.xml:151-154` が `junit:junit:4.13.1` を宣言）**:
  - `TestClass.getSuperClasses(Class)` — 引数のクラスを先頭に置き `getSuperclass()` を辿る（**サブクラスが先**）
  - `TestClass.addToAnnotationLists(T, Map)` — **アノテーションごとに**専用リストを取り `FrameworkMember.handlePossibleBridgeMethod(list)` を呼ぶ。戻り値が `null` なら追加しない
  - `FrameworkMethod.isShadowedBy(FrameworkMethod)` — 比較するのは名前と引数型のみで、**アノテーションは比較していない**
- **結論**: 一致。原因は Java の static メソッド隠蔽ではなく **JUnit 自身のシャドウ判定**である。ただし判定の土俵がアノテーション別のリストであるため、「同名（かつ同一引数型）」と「同種のアノテーション」の**両方**が条件になる。本文の書き方は実装と一致する。**是正不要・§2 への移動も不要**
- **実施**: 記録のみ

### 4-11. `implementation/deal_unit_test/batch.rst:10`・`:15` の前提（別担当が一次情報で検証済み・そのまま記録＋申し送り）

- **現状の本文**（作業ツリーで自分で確認）:
  - `:10` 「Nablarchバッチアプリケーションの取引単体テストは、1つの取引を構成する複数のバッチ処理を1つのテストメソッドの中で順に動かし、取引全体が想定どおりに処理されることを検証する。」
  - **`:15` 「バッチアプリケーションでは、1つの取引が複数のバッチ処理に分かれることが多い。テスティングフレームワークは、…」**
- **出典**: `2e501ad:…/05_UnitTestGuide/03_DealUnitTest/batch.rst:5-6` は「バッチ処理の取引単体テストは、自動テストフレームワークを使用してテストを行う。／リクエスト単体テストを連続実行することにより、取引単位でのテストを行う。」のみ。**「複数のバッチ処理に分かれることが多い」という頻度の主張は出典に無い**
- **FW解説書**: `ja/application_framework/application_framework/messaging/db/` 配下で「取引」は0件、`batch/` 配下でも0件。`messaging/db/application_design.rst:3-4` と `messaging/db/architecture.rst:17`・`:23`・`:30` は、責務配置・構成・処理の流れがすべて Nablarchバッチと同じであると明記している
- **結論**: 不一致（前提に出典が無い）。ただし**DBキューで「成立しない」と言える根拠も無い**ため、`implementation/deal_unit_test/db_queue.rst:6` の「同じ方法で行う」という導線に矛盾は生じない。**是正するとすれば飛び先ではなく `batch.rst:15` の側**
- **§2 の実施状況を確認した**: `git log --oneline 62bb33a..HEAD -- ja/…/implementation/deal_unit_test/batch.rst` は `24896d8`（`#28` §2 (A) 是正4件）と `601a6d6`（§2 導線・追記系）の2件を返す。両コミットの差分を `git log -p` で確認したところ、変更は `:19` の導線追記、`:59-63` のグループID・準備データ・期待値の追記、および Excel/YAML 記述例の `100`→`0`・`fileInputBatch`→空欄 の是正であり、**`:15` の「複数のバッチ処理に分かれることが多い」には手が入っていない**（作業ツリーの `:15` に当該文が現存することも自分で確認した）
- **実施**: **申し送り**（後述）。`.rst` は自分では触らない

---

### 4-12. `implementation/request_unit_test/db_queue.rst` の飛び先の妥当性

- **当該ページ（全6行、全文を読んだ）**: `:1` `.. _request_unit_test_db_queue:`／`:3-4` タイトル「リクエスト単体テスト（テーブルをキューとして使ったメッセージング）」／`:6` 「テーブルをキューとして使ったメッセージングのリクエスト単体テストは、\ :ref:`リクエスト単体テスト（Nablarchバッチアプリケーション） <request_unit_test_batch>`\ と同じ方法で行う。」
- **読者が実際に見るもの** — 飛び先 `implementation/request_unit_test/batch.rst`（200行）を開いて数えた:
  - 見出しは `:3` タイトル／`:12` 機能概要／`:67` 使用方法／`:72` テストクラスを作成する／`:114` テストメソッドを作成する／`:141` テストデータを作成する／`:179` テストを実行する／`:189` テスト結果を確認する
  - **「応答不要」が9箇所**（`:10`・`:20`・`:29`・`:92`・`:145`・`:147`・`:152`・`:158`・`:164`）。冒頭のリード文 `:10` から応答不要メッセージ送信の話が始まる
  - `.. code-block::` は**6件**（`:82`・`:100`・`:125`・`:134`・`:160`・`:171`）。うち**3件が応答不要メッセージ送信に固有**（`:100` 応答不要のテストクラス、`:160`・`:171` ディスパッチハンドラ差し替え）＝**50%**
  - **「テーブルをキュー」「db_messaging」「db_queue」の出現は0件。** 飛び先のページは、飛んできた読者にひとことも触れていない
- **指示書の数値との照合**: 指示書は「8割が該当しない」としているが、**自分で数えた結果は 6件中3件（50%）** であり一致しない。「応答不要」の言及9箇所という別指標なら印象は指示書寄りだが、コードブロック基準では50%である
- **結論**: 飛び先自体は妥当（`ntf-doc-27-db-queue.md:53` が「『同じ方法で行う』以上のことを書かない」と規定しており、`#27` の判断として正しい）。ただし**読者は、自分に関係のない「応答不要メッセージ送信」の説明を半分ほど読まされる。** 飛び先に「テーブルをキューとして使ったメッセージングのテストもこのページの方法で行う」という受け側の一言が無いことが実害の中心である
- **実施**: 記録＋**申し送り**（後述）

### 4-13. `implementation/deal_unit_test/db_queue.rst` の飛び先の妥当性

- **当該ページ（全6行）**: `:6` 「テーブルをキューとして使ったメッセージングの取引単体テストは、\ :ref:`取引単体テスト（Nablarchバッチアプリケーション） <deal_unit_test_batch>`\ と同じ方法で行う。」
- **読者が実際に見るもの** — 飛び先 `implementation/deal_unit_test/batch.rst`（491行）を開いて数えた:
  - 見出しは `:3` タイトル／`:12` 機能概要／`:17` 使用方法／`:22` テストクラスを作成する／`:43` テストメソッドを作成する／`:81` テストデータを作成する／`:99` Excel形式の場合／`:341` YAML形式の場合
  - **記述例は6件**（`:101`・`:170`・`:261` が Excel、`:343`・`:383`・`:443` が YAML。3つの書き方 × 2形式）
  - **6件すべてが同じ題材**「ファイル入力・ユーザ削除・ファイル出力」（`:89-91`）で、`setUpFile`／`expectedFile` を使う**ファイル入出力バッチ**である
  - **`SqlRow` の出現は0件**。`setUpTable` 17件・`expectedTable` 13件
  - 一方 DBキューの入力は `SqlRow` である（`ja/application_framework/application_framework/messaging/db/getting_started/table_queue.rst:94` `public class ProjectCreationServiceAction extends BatchAction<SqlRow>`、同 `:100`・`:194`）
- **結論**: 飛び先自体は妥当（テストの**方法**は同じ）。ただし**6つの記述例すべてがファイル入出力バッチの題材で、DBキュー（`SqlRow` 入力）の読者は自分のケースに直接あてはまる例を1つも見られない。** 4-12 と同じく、飛び先に受け側の一言が無い
- **実施**: 記録＋**申し送り**（後述）

### 4-14. `setup/request_unit_test/db_queue.rst` の飛び先の妥当性 — **指示書の前提が誤っている**

- **当該ページ（全6行）**: 飛び先は `setup/request_unit_test/batch.rst`（119行）
- **飛び先の設定項目は3件**: `:15` リクエストスレッド内ループ制御ハンドラを置き換える／`:39` ディレクティブのデフォルト値を設定する／`:80` 符号無数値・符号付数値のテスト用のデータ型を登録する
- **指示書の前提**: 「DBキューに該当するのは1件のみ（残り2件はファイルデータ用）」
- **反証を一次情報で得た**:
  - 飛び先ページ自身のリード文 `:10` が「後の2つは…ファイルデータ**や電文**のテストデータを扱うテストで使用する」と書いており、電文を含めている
  - 実装でも電文のテストデータは固定長ファイルの経路を通る:
    - `nablarch-testing@e21bf67 src/main/java/nablarch/test/core/reader/MessageParser.java:58` — `return new FixedLengthFileParser(...)`
    - `FixedLengthFileParser.java:31` — `return new FixedLengthFile(filePath);`
    - `FixedLengthFile.java:17` — `private static final String DEFAULT_DIRECTIVES = "fixedLengthDirectives";`、`:24-27` のコンストラクタが `super(path); prepareDefaultDirectives(DEFAULT_DIRECTIVES);`
    - `DataFile.java:60` — `DEFAULT_DIRECTIVES = "defaultDirectives"`、`:89-92` のコンストラクタが `prepareDefaultDirectives(DEFAULT_DIRECTIVES)`
  - すなわち `defaultDirectives`／`fixedLengthDirectives`（設定項目2）は、DBキューのテストが扱う電文テストデータにも効く
- **1件目の分量**: `:15-38`（24行）／本文 `:10-119`（110行）＝ **約22%**
- **結論**: **3件中2件がDBキューに関係する**（1件目のループ制御ハンドラは `:17` が「このハンドラは :ref:`テーブルをキューとして使ったメッセージング <db_messaging>` のハンドラ構成に含まれる」と明記しており直接該当、2件目のディレクティブも上記のとおり該当）。関係しないと確実に言えるのは3件目（符号無数値・符号付数値のデータ型）だけである。**指示書が想定した「該当は1件のみ」という是正の動機は成立しない。是正不要**
- **実施**: 記録のみ

---

### 4-15. 個別指示の件数表の再計算

**使った集計コマンド**（`disposition != 'DROP'` で絞り、`src_file` 別に集計）:

```bash
cd .rn/20260724-ntf-yaml-support/mapping
python3 - <<'PY'
import csv, collections
rows=[r for r in csv.DictReader(open('mapping.csv',newline='',encoding='utf-8'))
      if r['disposition']!='DROP']
for page in ['コンポーネント単体テスト','リクエスト単体テスト（ウェブアプリケーション）','エンティティ単体テスト']:
    sub=[r for r in rows if r['dest_page']==page]
    print(f"## {page}: {len(sub)}件 / {sum(int(r['lines']) for r in sub)}行")
    agg=collections.Counter(); ln=collections.Counter()
    for r in sub:
        agg[r['src_file']]+=1; ln[r['src_file']]+=int(r['lines'])
    for f,c in agg.most_common():
        print(f"   {f}  {c}件 {ln[f]}行")
PY
```

#### `ntf-doc-27-large-pages.md` — **ずれ2箇所（いずれも表の側が誤り。見出しの合計値は正しい）**

| 箇所 | 指示書 | `mapping.csv` 実測 |
|---|---|---|
| `:36` 見出し（コンポーネント単体テスト 合計） | 出典770行・26件 | **26件・770行（一致）** |
| `:40` §2-1 表 `03_Tips.rst` | 12件・270行 | **14件**・270行（**件数が2件少ない**） |
| `:78` 見出し（リクエスト単体テスト（ウェブ） 合計） | 出典914行・33件 | **33件・914行（一致）** |
| `:92` §3-2 表 `02_RequestUnitTest/index.rst` | 12件・455行 | **13件・461行** |
| `:92` §3-2 表 `02_RequestUnitTest.rst` | 8件・213行 | **9件・260行** |
| `:114` 見出し（エンティティ単体テスト 合計） | 出典1,344行・17件 | **17件・1344行（一致）** |
| `:118` §4-1 表（17行すべて） | — | **17件すべて行数一致。合計1344行も一致** |

**指示書は自分自身と食い違っている**（見出しの合計と表の合計が合わない）。

- §2-1 表の合計 = 4+8+12 = **24件**（見出しは26件）／343+157+270 = 770行（見出しと一致）
- §3-2 表の合計 = 12+8+3+2+2+2+2 = **31件**／455+213+90+39+18+15+31 = **861行**（見出しは33件・914行）

`mapping.csv` の実測は**見出しの側と完全に一致する**。したがって**誤っているのは表の側**である。実測の内訳:

- コンポーネント単体テスト 26件/770行 — `03_Tips.rst` **14件**/270行、`02_DbAccessTest.rst` 8件/157行、`01_ClassUnitTest/02_componentUnitTest.rst` 4件/343行
- リクエスト単体テスト（ウェブ） 33件/914行 — `02_RequestUnitTest/index.rst` **13件/461行**、`06_TestFWGuide/02_RequestUnitTest.rst` **9件/260行**、`fileupload.rst` 3件/90行、`03_Tips.rst` 2件/39行、`mail.rst` 2件/18行、`input/ntf-doc-terms.md` 2件/31行、`double_transmission.rst` 2件/15行
- エンティティ単体テスト 17件/1344行 — `02_entityUnitTestWithNablarchValidation.rst` 9件/663行、`01_entityUnitTestWithBeanValidation.rst` 8件/681行

補足: §2-3（`:65` 「`03_Tips.rst` の12件の扱い」）が挙げる「溶かし先の目安」の `mapping_id` を数えると、`current-0216`・`0218`〜`0220`・`0222`・`0230`・`0231`・`0233`〜`0239`（`0232` は無い）の **14件**で、`mapping.csv` が返す14件と過不足なく一致する。**実害は見出しと本文の「12件」という数え間違いだけで、対象行の取りこぼしは無い。**

#### `ntf-doc-27-small-3rd.md` — **ずれ0件**

§0 の一覧表（32行/33行/48行/28行）も、各ページの個別表（`:56-57`・`:81`・`:114-118`・`:151-155`）も、`mapping.csv` と完全に一致した。取引単体テスト（RESTful）2件/32行、取引単体テスト（HTTPメッセージング）2件/33行、取引単体テスト（ウェブ）5件/48行、リクエスト単体テスト（HTTPメッセージング）3件/28行。

#### `ntf-doc-27-db-queue.md` — **出典件数表を持たない**

全71行を読んだ。数値を含む表はゲート表（DQ1〜DQ5）だけで、出典件数表は存在しない。同ファイルは3ページとも出典0行だと述べており、`mapping.csv` で3つの `dest_page` を引いてもいずれも**0件/0行**で一致した。

**実施**: 記録のみ。指示書本体は履歴として残すため書き換えていない。

---

### 申し送り

宛先を分けて書く。いずれも自分では実施していない。

#### （A）`ja/` 配下の `.rst` を編集する担当へ

1. **`setup/junit5_extension.rst:73`（4-8）** — 現状「``maven-surefire-plugin``\ が2.22.0以上である必要がある」。Nablarch の一次情報で裏が取れる値は **2.22.2**（親POM `6u2`・`6-NEXT-SNAPSHOT` とも `:52` が `<surefire.plugin.version>2.22.2</surefire.plugin.version>`）であり、「2.22.0以上」という下限の Nablarch 側根拠は無い。**推奨は「Nablarch の親POM は ``maven-surefire-plugin`` 2.22.2 を使用する」に寄せるか、下限値を書くこと自体をやめること。** 2.22.0 を残す場合は JUnit 5 側の出典を明示する必要があるが、その出典は本作業環境（オフライン）で取得できず**未確認**である。この点は判断をユーザーに上げるべき論点として残る。
2. **`implementation/deal_unit_test/batch.rst:15`（4-11）** — 「バッチアプリケーションでは、1つの取引が複数のバッチ処理に分かれることが多い。」は出典（`2e501ad:…/03_DealUnitTest/batch.rst:5-6`）にも FW解説書（`batch/`・`messaging/db/` とも「取引」0件）にも根拠が無い加筆である。**§2 の2コミット（`24896d8`・`601a6d6`）はこの文に手を入れていない。** 出典どおりに「テスティングフレームワークは、リクエスト単体テストと同じ仕組みでバッチを起動する機能を提供している。この機能を1つのテストメソッドの中で連続して呼び出すことで、取引単位のテストになる。」だけを残す形へ寄せると、DBキューから飛んできた読者にも成立する。
3. **`implementation/class_unit_test/component.rst:313`（4-6）** — `:ref:`マスタデータ復旧機能 <master_data_restore>`` の飛び先を、出典と同じ粒度の **`master_data_restore-suppress_table_sort`**（`setup/master_data_restore.rst:159`、見出し `:161` 「テーブルの依存関係の解析を抑止する」）に変えるかを判断してほしい。ラベルは既に存在するので新設は不要。**現状のページ先頭ラベルのままでも誤りではない**（同一ページ内の節であり読者は迷わない）。
4. **`implementation/request_unit_test/batch.rst`（4-12）と `implementation/deal_unit_test/batch.rst`（4-13）に受け側の一言を置くか** — どちらの飛び先も、飛んでくる「テーブルをキューとして使ったメッセージング」に一言も触れていない（`request_unit_test/batch.rst` では「テーブルをキュー」「db_messaging」「db_queue」がいずれも0件）。読者は `request_unit_test/batch.rst` では6件のコードブロックのうち3件（50%）が応答不要メッセージ送信固有の記述を、`deal_unit_test/batch.rst` では6件の記述例すべてがファイル入出力バッチ（`SqlRow` は0件）の題材を読むことになる。**`#27` の縛り（`ntf-doc-27-db-queue.md:53` 「『同じ方法で行う』以上のことを書かない」）は飛び元ページに対するものなので、飛び先に受け側の一言を置くことはこの縛りに反しない。**

#### （B）調整役へ

1. **`checks/task-28.md` への取り込み**: 本節をそのまま貼れる。私は `checks/task-28.md` を編集していない。
2. **私が変更したファイルは `.rn/20260724-ntf-yaml-support/steering.md` の1件のみ**（`# Assumptions` に +8行。`git diff --stat` で `1 file changed, 8 insertions(+)`）。§4 完了時点の `git status --short` は `M .rn/20260724-ntf-yaml-support/steering.md` と `?? .rn/20260724-ntf-yaml-support/checks/task-28.md` の2行で、後者は他の担当が作成した未追跡ファイルであり私は触っていない。作業中に一時的に見えた `ja/…/setup/class_unit_test.rst`・`ja/…/setup/request_unit_test/batch.rst` の2件は他の担当の変更で、いずれも既にコミット済みである。
3. **`mapping.csv`・`_batch/`・`volume.md` は変更していない。** `verify_mapping.py` は `exit 0`、`csv.DictReader` によるレコード数 597 で着手時から不変。
4. **4-1〜4-5 の5件は既知の誤りとして `mapping.csv` に残る。** `#last` で `mapping.csv` から配置を再導出する場合、本節を読まないと5件を誤って再現する。正しい値は各項に書いた（4-1: `current-0178` → `使用方法`／4-2: `current-0269` → `機能概要`（**ただし直すと `verify_mapping.py` が `exit 1`**）／4-3: 表せる列が無い／4-4: `current-0069` は2行への分割が必要／4-5: `note` は現状維持が既決）。
5. **指示書の前提が誤っていた箇所が3つある**（履歴として残すため指示書は書き換えていない）。(a) 4-7 — `steering.md` に参照リポジトリ表は存在しなかった。ピン値の実体は `ntf-doc-weekend-queue.md:187` にあった。(b) 4-8 — 親POM は「本作業環境に無い」とされていたが `~/.m2/repository/com/nablarch/nablarch-parent/` に実在した。(c) 4-14 — 「DBキューに該当するのは1件のみ」という前提が実装で否定され、3件中2件が該当する。
6. **数値が実測と合わない箇所が2つある。** 4-12 の「8割が該当しない」は、コードブロック基準で数えると6件中3件（50%）だった。4-15 の `ntf-doc-27-large-pages.md` は見出しの合計と表の合計が自分自身で食い違っており、`mapping.csv` と一致するのは見出しの側である。

---

## §5 残骸の整理 4件

作業指示: `ntf-doc-28-decide-disposition.md` §5（`:526-577`）。「順序の指定」（`:740-746`）に従い、§1〜§4・§6・§7 をすべて終えてから 5-1 → 5-3 → ゲート9 → 5-4 の順に行い、5-2（削除）を最後の単独コミットとした。調整役が自分で実施した（不可逆な削除を含むため委譲していない）。

### コミット

| コミット | 内容 |
|---|---|
| `ef40fb9` | §5-4（`design.md` §9 への追記。§3-22 と同じコミットに入っている） |
| （§5-1・§5-3） | 画像の移設と作図元の退避 |
| （§5-2） | `guide/` の削除（単独コミット） |

### 5-1. `about/index.rst` の画像を移した

- `git mv ja/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/_images/abstract_structure.png ja/development_tools/testing_framework/about/images/index/abstract_structure.png`
- `about/index.rst:108` の `.. image::` を `../guide/development_guide/06_TestFWGuide/_images/abstract_structure.png` から `images/index/abstract_structure.png` に書き換えた（`:scale: 80` はそのまま）
- 配置規約は `design.md` §13（`ja/development_tools/testing_framework/<部>/images/<ページ名>/<図名>`）。`about/images/` は存在しなかったため `about/images/index/` を新規に作った

### 5-3. 作図元の `.xlsx` を退避した

- `git mv ja/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/_image/images.xlsx ja/development_tools/testing_framework/implementation/request_unit_test/images/mom/send_sync.xlsx`
- 退避先は `TODO(NTF-FIG-02)`（`implementation/request_unit_test/mom.rst:35-39`）が作図元として示すパスと一致する。§6 担当の申し送り（本ファイル §6「他の担当への申し送り」）が求めた照合を満たすため、TODO 側の書き換えは不要だった
- 指示書 `:565` のとおり、残る `.xlsx` 6件（`http_send_sync_ok_pattern.xlsx`・`send_sync_ok_pattern.xlsx`・`mail_image.xlsx`・`01_ClassUnitTest/_download/` の3件）と日本語ファイル名の1件は作図元ではないため退避していない。5-2 の削除で失われる

### 5-4. `en/` を後続作業として明示記録した

`design.md:594`（§9「対象外とするもの」の末尾）に追記済み。コミット `ef40fb9`（§3-22 と同一）。本文は次のとおり。

> **`en/` 配下は本刷新では変更せず、`ja/` 確定後に別タスクで同じ章構成へ揃える**（`#28` 確定）。対象外にするのではなく、順序を後ろに置く。`en/development_tools/testing_framework/` は独立した `en/conf.py` を持ち `ja/` を参照しない（`grep -rn "/ja/" --include=*.rst en/development_tools/` が0件）ため、`ja/` の刷新によって壊れることはない。したがって `ja/` を先に確定させてから着手できる。

根拠の grep は調整役が再実測した（`0` 件）。**本タスクで `en/` 配下のファイルは1件も変更していない**（`git diff --name-only <着手コミット>..HEAD -- en/` が0件）。

### 5-2. `guide/` をディレクトリごと削除した

削除直前の実測（`git ls-files ja/development_tools/testing_framework/guide`）:

| 項目 | 値 |
|---|---|
| 追跡ファイル数 | **86**（指示書 `:532` の88件から、5-1・5-3 で移した2件を差し引いた数） |
| 内訳 | png 70・xlsx 7（うち1件は日本語ファイル名）・java 6・jpg 2・JPG 1 |
| `.rst` の数 | **0** |

**このディレクトリの削除がビルド出力に影響しないことの根拠**（削除前にフルビルドを行い、その結果をゲート7に記録したため、根拠を示す）:

1. `guide/` 配下に `.rst` は0件である（上表）。したがって toctree にも `sphinx-build` の読み取り対象にも入らない
2. `guide/` を参照する `.rst` は0件である（ゲート9）
3. `ja/conf.py:144` の `html_static_path` は `['../_static']` のみで、`html_extra_path` は `:150` でコメントアウトされている。Sphinx は参照されていない画像を `_build/html` へ複写しない

---

## ゲート1〜11

`ntf-doc-28-decide-disposition.md:724-738`。調整役が実測した。フルビルドは §5-2 の削除より前に実行しており、削除がビルド出力に影響しない根拠は §5-2 に記した。

| # | 内容 | 判定 | 実測値・根拠 |
|---|---|---|---|
| 1 | §1 の24件を閉じた記録が1行ある | **PASS** | 本ファイル `## §1` |
| 2 | §2 の32件それぞれの根拠 `file:line` 確認と結果、「未確認」項目の可否 | **PASS** | 本ファイル §2「32件の実施結果（ゲート2）」。17件の「未確認」はすべて可否を明記。確認できなかった1件（`maven-surefire-plugin` 2.22.0 の一次情報）は本文を変えずに記録した（禁止事項 `:753` に従う） |
| 3 | `implementation/deal_unit_test/batch.rst` の `expectedStatusCode` が `"100"` 0件・`"0"` 10件以上 | **PASS** | `grep -c '"100"'` = **0**、`grep -c '"0"'` = **10** |
| 4 | §3 の18件が3ファイルに反映され、`glossary.md` §5.15 に差分0行 | **PASS** | 反映は本ファイル §3「22件の実施結果」。§5.15 は `084dd28`（`#28` 着手前）と HEAD で **126行が完全一致**（`awk` で §5.15 の節を抜き出して `diff` → 差分0行。126行は指示書の `:331-456` と同じ長さ） |
| 5 | `verify_mapping.py` が exit 0 | **PASS** | `exit 0`、`OK: no errors` |
| 6 | `verify_glossary.py` の不一致が `#pre-last` から増えていない | **PASS** | `#pre-last` 完了時点 **0件**（`checks/task-pre-last.md:87`）→ 現在 **0件**（`RESULT: OK`。refs 290・counts 118・sections 86・terms 201・applies 96・population 331・design_sections 21・scheme_names 7・reasons 0） |
| 7 | Docker フルビルドで WARNING・ERROR ともに0件 | **PASS** | `build succeeded.`（exit 0）。`grep -c -i WARNING` = **0**。`grep -c -i error` は17件ヒットするが、**17件すべてファイル名・ページ名に `error` を含む進捗行**（`global_error_handler`・`HttpErrorHandler`・`errors_all.png` など）で、ビルドのエラーではない。ビルド後に `git checkout -- locales/ja/LC_MESSAGES/sphinx.mo` を実行済み |
| 8 | §6-2 の5件の根拠 `file:line` とコミットハッシュが `reviews/page-*.md` にある | **PASS** | コミット `10c2567`。本ファイル §6「§6-2 実装上必須の設定の追記（5件）」 |
| 9 | §5-2 の直前に `grep -rn "guide/development_guide" --include=*.rst ja/` が0件 | **PASS** | **0件**（5-1 の書き換え後に実測） |
| 10 | `TODO(NTF-FIG-01〜04)` が `grep` の実測と一致し、`_build/html` に0件 | **条件付き PASS**（下記参照） | `.rst` 側は `TODO(NTF-FIG-` **4件**・`TODO(NTF-MOD-` **7件**で、本ファイル §6・§7 の一覧と完全一致。レンダリング結果の `.html` は **0件**（`grep -rl --include=*.html` が0）。ただし `_build/html/_sources/*.txt` に9ファイルヒットする |
| 11 | §6-5 で図を落としたページで、図が伝えていた構造が本文・表として残っている | **PASS** | 本ファイル §6「§6-5 本文と食い違う図の削除（4件・ゲート11）」の対比表4行 |

### ゲート10 の「条件付き」の内訳 — user 判断が要る1件

`_build/html/_sources/` に、reST の原文がそのまま `.txt` として複写される（Sphinx の `html_copy_source` の既定が `True` であるため）。`TODO(NTF-MOD-`／`TODO(NTF-FIG-` を含む9ファイルは**すべてこの `_sources/` 配下**であり、レンダリング結果の `.html` には1件も出ない。

読者から到達できるかを実測した。

- `grep -rl 'TODO(NTF-MOD-\|TODO(NTF-FIG-' --include=*.html _build/html` = **0件**
- `grep -rl '_sources/' --include=*.html _build/html` = **0件**（`ja/conf.py:177` が `html_show_sourcelink = False` のため、どのページにも「ソースを表示」のリンクが出ない）

したがってサイト上の導線からは到達できない。一方、`_build/html` をそのまま配信すると `_sources/` のファイル自体は URL で取得できる。これは NTF 解説書に限らず**このリポジトリの全ページに以前から当てはまる**性質であり、`#28` で作り込んだものではない。

**是正の手段は `ja/conf.py` に `html_copy_source = False` を足すことだが、禁止事項 `:754`「`ja/conf.py` を変更しない」に当たるため実施していない。** 扱いの判断を user に仰ぐ（`#last` の申し送り）。

**user 判断（2026-08-18、`/rn:gm`）: 変更しないで進める。`ja/conf.py` は変更しない。** ゲート10 の「条件付き PASS」はこの判断をもって確定とする。

## 調整役が自分で行った是正

1. **`ja/development_tools/testing_framework/implementation/deal_unit_test/batch.rst:15`** — 「バッチアプリケーションでは、1つの取引が複数のバッチ処理に分かれることが多い。」を削除した（コミット `8ecc713`）。出典（`2e501ad:.../03_DealUnitTest/batch.rst:5-6`）に無い頻度の主張であり、FW解説書の `batch/`・`messaging/db/` にも「取引」は0件で裏付けが取れない。§2 の対象32件にも §4 の対象（`ja/` の `.rst` は変更しない）にも入らず、担当のあいだで落ちる位置にあった
2. **`.rn/20260724-ntf-yaml-support/steering.md` の `# Assumptions`** — §4-7 が前提とした「参照リポジトリ表」が存在しなかったため、4リポジトリの参照コミットをピンする表を新設した（コミット `8ecc713`）。詳細は本ファイル §4-7
3. **`reviews/page-master_data_tool.md` の G6 の内訳** — 「`tip` 2件・`important` 3件」が誤りだった。ページ作成時点（`4095bab`）の実測は `tip` 3件・`important` 3件で、`#28` §7 の削除後の現在は `tip` 3件・`important` 2件である。訂正行を足した
4. **本ファイル §7 の見出し「ゲート9」** — ゲート番号の取り違えだったため、`TODO(NTF-MOD-` の実測（ゲート10 の前半）である旨に改めた

## user review（`/rn:gm`、2026-08-18）による S-04 実測値の是正

`e57a0d3` を対象に見出しを再走査したところ、`mapping/style.md` S-04 の実測値3ブロックが古くなっていた。
`#28` §3 の実測（本ファイル §3「実測4件」）は `18fb782` 時点の値で当時は正しく、その後 §6-2 が
`implementation/testdata_examples.rst` に見出しを足したため 384→392 見出しに増えている。**§3 の実測ブロックは
当時の記録としてそのまま残し、ここに再計測値を記す。**

再計測（2026-08-18、`e57a0d3`、`ja/development_tools/testing_framework/**/*.rst` の38ページ。判定式は
「下線長 == max(レベル既定値, タイトルの表示幅)」、表示幅は East Asian Width が W/F を2・他を1）:

```
見出し総数 392（L1 38 / L2 68 / L3 164 / L4 122）
下線長  一致 296 / 不一致 96
  L1 38/38   L2 68/68   L3 128/164   L4 62/122
不一致 96 はすべて「49とすべき箇所を50にしている」型
  implementation/testdata_examples.rst  L3 22件・L4 60件（計82件）
  tools/request_data_tool.rst           L3  8件
  tools/master_data_tool.rst            L3  6件
L3またはL4を持つページ 31 のうち不一致を含むのは上記3ページのみ（残り28ページは不一致0件）
下線の直後  空行でない  L3 164/164・L4 121/122（例外は testdata_notation.rst:1379）
                        L1 空行あり 37/38（例外は index.rst:1）・L2 空行なし30／空行あり38
L4を持つL3 49件（配下 2本が41件・3本が1件・5本が1件・6本が4件・7本が1件・1本が1件）
L4の本数が多いページ  testdata_examples.rst 60本・testdata_notation.rst 27本・request_unit_test/web.rst 15本
```

増えた2件は `implementation/testdata_examples.rst` のL4見出し「Excel形式の場合」（`:20-21`）・
「YAML形式の場合」（`:139-140`）で、いずれも下線50である。同じ §6-2 で新設したL3見出し2件は `7553b81` で
49に直してあるが、このL4 2件は残っている。

**`.rst` は変更しない（user 判断）。** `implementation/testdata_examples.rst` はL3・L4が82件とも下線50で
そろっており、新設2件だけ49にするとファイル内で割れるためである。是正したのは `mapping/style.md` の
実測値のみ（`:252`・`:257`・`:265-268`・`:276`）。

**`#last` への申し送り**: 本ファイル `:229` の表「S-04（下線長）」の**94件は96件に読み替える**
（`implementation/testdata_examples.rst` 82件・`tools/request_data_tool.rst` 8件・
`tools/master_data_tool.rst` 6件）。表そのものは §2 担当へ渡した当時の記録のため書き換えていない。
