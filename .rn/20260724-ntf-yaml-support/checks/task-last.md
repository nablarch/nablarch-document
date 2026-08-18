# `#last` Evaluation sign-off の検査記録

対象コミット: 掃き出し前 `51bcd12` / 掃き出し後は本タスクのコミット。
実行日: 2026-08-18。実行環境: Docker イメージ `nablarch-document-build-sandboxed`。

`file:line` の基準は作業ツリー（`mapping/glossary.md` §1 と同じ記号体系）。

---

## 1. Acceptance criteria の達成状況

| # | Acceptance criteria | 判定 | 根拠 |
|---|---|---|---|
| 1 | 全量を失わない | **達成** | `mapping.csv` は `csv.DictReader` でレコード数 597。`disposition` は MOVE 237・MERGE 228・DROP 96・SPLIT 22・REFERENCE 14。**DROP 以外の501件で `dest_page` が空の行は0件**。DROP 96件は `#5c` で全件レビュー済み（`checks/task-05c.md`） |
| 2 | 重複がない | **達成** | `verify_mapping.py` が exit 0（`OK: no errors`）。同一 `src_section_id` が複数の `dest_page` に割り当てられていないことを検査する |
| 3 | 用語が統一されている | **達成** | `verify_glossary.py` が exit 0・`RESULT: OK`。9検査すべて不一致0件（refs 290・counts 118・sections 86・terms 201・applies 96・population 331・design_sections 21・scheme_names 7・reasons 0） |
| 4 | トンマナが揃っている | **条件付き達成** | `style.md` S-04（下線長）・S-13（`\ ` エスケープ）は本タスクの掃き出しで**違反0件**。ただし同じ `#28` 申し送り表の**残り5件が未処理**（下記 §5） |
| 5 | `make html` がエラー0で完了する | **達成** | 下記 §2 |

`.rst` は38ページ（`find ja/development_tools/testing_framework -name "*.rst" \| wc -l` = 38）。

## 2. フルビルドと未解決参照（`#last` Steps 2）

`ja/conf.py:103` が `keep_warnings = True` のため未解決参照はビルド失敗にならない。エラー0の確認だけでは
不十分なので、ログに対して3種類の文字列を個別に数えた。

実行コマンド（掃き出し後・クリーンビルド）:

```
docker run --rm -v "$PWD":/root/document nablarch-document-build-sandboxed /bin/bash -c \
  "cd /root/document; rm -rf _build; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"
git -C <repo> checkout -- locales/ja/LC_MESSAGES/sphinx.mo
```

| 検査 | コマンド | 結果 |
|---|---|---|
| ビルド成否 | `sphinx-build` の exit code とログ末尾 | **exit 0**・`build succeeded.` |
| WARNING | `grep -ci warning <log>` | **0件** |
| `undefined label` | `grep -c 'undefined label' <log>` | **0件** |
| `toctree contains reference to nonexisting document` | 同左 | **0件** |
| `unknown document` | `grep -c 'unknown document' <log>` | **0件** |
| ERROR | `grep -niE '\berror\b' <log>` | ヒット1件のみで、`application_framework/.../images/tag/error.png` という**ファイル名**。エラー出力は0件 |

出力は `.html` 486ページ。ビルド直後に `locales/ja/LC_MESSAGES/sphinx.mo` を `git checkout` で戻し、
`git status` がクリーンであることを確認した。

## 3. `checks/task-07.md`「リンク切れになる参照」3件（`#last` Steps 3）

3件とも解消済み。実ファイルで確認した。

| # | 参照元 | 参照の形 | 解消後の参照先 | 実ファイルでの確認 |
|---|---|---|---|---|
| 1 | `ja/development_tools/index.rst:10` | toctree `testing_framework/index` | `ja/development_tools/testing_framework/index.rst` | ファイルが存在する（890バイト）。中身は第1部〜第4部への toctree（`about/index`・`setup/index`・`implementation/index`・`tools/index`） |
| 2 | `ja/index.rst:54` | `:doc:` `` `テスティングフレームワーク <development_tools/testing_framework/index>` `` | 同上 | 同上。`grep -n "testing_framework" ja/index.rst` が `:54` の1件を返し、飛び先が存在する |
| 3 | `ja/application_framework/application_framework/libraries/db_double_submit.rst:106` | `:ref:` `` `テスティングフレームワークのトークン発行<how_to_set_token_in_request_unit_test>` `` | `ja/development_tools/testing_framework/implementation/request_unit_test/web.rst:257` にラベル `.. _how_to_set_token_in_request_unit_test:` を定義。直後の見出しは `:258` 「二重サブミット防止機能のトークンを設定する」 | `grep -rn "how_to_set_token_in_request_unit_test" --include=*.rst ja/` が**定義1件・参照1件**を返す |

ビルドの `undefined label` が0件であること（§2）が、3件とも実際に解決していることの裏付けになる。

## 4. 持ち越し(1) `maven-surefire-plugin` 2.22.0 の一次情報

**対象**: `ja/development_tools/testing_framework/setup/junit5_extension.rst:73`
「JUnit 5を使用するには、\ ``maven-surefire-plugin``\ が2.22.0以上である必要がある。」

### 自分で確認した一次情報

| 出典 | 実測 |
|---|---|
| `~/.m2/repository/com/nablarch/nablarch-parent/6u2/nablarch-parent-6u2.pom:52` | `<surefire.plugin.version>2.22.2</surefire.plugin.version>`（`:91`・`:370` で使用） |
| 同 `6` / `6u1` / `6u3` / `6-NEXT-SNAPSHOT` の各 `:52` | いずれも **2.22.2**。`5u22`〜`5u26` は `:50` が 2.22.2、`5u13`〜`5u21` は `<version>` を持たない |
| `~/.m2/repository/org/apache/maven/plugins/maven-surefire-plugin/` | **2.22.2・3.2.5・3.5.0 の3つのみ。2.22.0 は存在しない**（＝本作業環境では 2.22.0 側の一次情報を取得できない） |
| 現行解説書 `2e501ad:.../06_TestFWGuide/01_Abstract.rst:691-695` | 「前提条件 … * maven-surefire-plugin が 2.22.0 以上であること」 |
| 現行解説書 `2e501ad:.../06_TestFWGuide/JUnit5_Extension.rst:26-33` | 「前提条件 … * maven-surefire-plugin の 2.22.0 以上」 |
| `mapping.csv` の `current-0179`（MOVE）・`current-0266`（MERGE） | どちらも「2.22.0以上」を新ページ「JUnit 5用拡張機能 > 機能概要」へ送る行 |

### 判断（user 判断が要る）

**「2.22.0以上」は本刷新が加筆したものではなく、現行解説書に元からある記述を `mapping.csv` の
2行（`current-0179`・`current-0266`）に従って移設したものである。** したがって本文を変えることは
Rules「マッピングにある内容を落とさない」と Acceptance criteria 1「全量を失わない」に触れる。

一方、**「2.22.0」という下限値の Nablarch 側の一次情報は存在しない**。Nablarch の親POM が固定するのは
2.22.2 であり、これは「Nablarch 自身のビルドが使う版」であって「利用者のプロジェクトが満たすべき下限」
ではない。下限としての 2.22.0 は maven-surefire-plugin 側が JUnit Platform プロバイダを同梱した版という
JUnit/Maven 側の事実だが、**その出典は本作業環境（オフライン）で取得できず未確認である**。

**推奨は現状維持（本文を変更しない）。** 理由は3つ。(a) マッピングにある記述であり、落とすと全量保証に
反する。(b) 2.22.2 に書き換えると「親POMが使う版」と「利用者が満たすべき下限」を取り違えた記述になり、
かえって誤りになる。(c) 下限を書くこと自体をやめる案は、現行解説書が2箇所で述べている前提条件を落とす
ことになる。**未確認なのは「2.22.0 という下限の出典」であって「記述の出所」ではない。**

## 5. 持ち越し(2) 規約確定にともなう機械的な掃き出し

`checks/task-28.md:223-234`「`ja/` 配下の本文是正への申し送り（§2 の担当へ）」の7行のうち、
**user が指名した2行（S-04 下線長・S-13 エスケープ）を掃き出した。** 残り5行は未処理である（§5-3）。

### 5-1. S-04（下線長）96件 — 掃き出し済み

判定式は「下線長 == max(レベル既定値, タイトルの表示幅)」。既定値は L1・L2 が50、L3・L4 が49。
表示幅は East Asian Width が W/F を2・他を1で数える。`style.md` に付属する検証器を使わず独立に組んだ。

| 時点 | 見出し総数 | 一致 | 不一致 |
|---|---|---|---|
| 掃き出し前（`51bcd12`） | 392（L1 38 / L2 68 / L3 164 / L4 122） | 296 | **96**（L3 36・L4 60） |
| 掃き出し後 | 392 | **392** | **0** |

不一致96件は**すべて「49とすべき箇所を50にしている」**型で、`implementation/testdata_examples.rst` 82件・
`tools/request_data_tool.rst` 8件・`tools/master_data_tool.rst` 6件の3ページに集中していた。
`checks/task-28.md:439` が「S-04 が挙げる『49 とすべき箇所を 50 にしている』不一致94件と同じ性質なので、
全面適用の際にまとめて直すこと」と申し送っていたものにあたる。

`#28` の user review で「`.rst` は変更しない」とした判断（`checks/task-28.md` 末尾）は、
`implementation/testdata_examples.rst` の新設L4 2件**だけ**を49にすると同一ファイル内で50と割れるため
だった。今回は同ファイルの82件すべてを49にそろえたので、その理由は解消している。

### 5-2. S-13（`\ ` エスケープ）192件 — 掃き出し済み

インラインマークアップ（`` `` `` 囲みと `:role:` 記法）の直前・直後の1文字が全角のとき `\ ` があるかを数えた。
コードブロック（`code-block` / `literalinclude` / `parsed-literal` / `::` の直後の字下げブロック）は除外した。

| 時点 | インラインマークアップ | 直前が全角の約物で `\ ` 無し | 直後が全角の約物で `\ ` 無し |
|---|---|---|---|
| `084dd28`（`#28` で S-13 を新設した時点） | 2,159 | 185 | 1（`index.rst:13`） |
| `e57a0d3`（`#28` §6-2 が本文を足した後） | 2,244 | 191 | 1 |
| 掃き出し後 | 2,244 | **0** | **0** |

**`style.md` が記録していた186件は、記録した時点では正しかった。** 自分の抽出器を `084dd28` に当てると
インラインマークアップ 2,159件・直前185件・直後1件で、`style.md` の実測値と完全に一致する。
その後 `#28` §6-2 が本文を足したため `e57a0d3` では192件に増えていた。**`#28` の user review が
S-04 で見つけたのと同じ「実測値が後続の加筆で古くなる」型である。**

**表を壊さないことの事前確認**: 192件の位置をすべて機械的に取り、`=` 罫線の簡易table・グリッドtable
に属するものが**0件**であることを確認してから編集した（属するのは地の文と `list-table` のセルのみ）。
`list-table` のセルは表示幅で列位置を揃える必要がないため、Rules の「`=` 罫線の簡易tableは表示幅で
そろえる」制約に触れない。

### 5-3. 掃き出しの検証 — HTML出力が1バイトも変わらないこと

掃き出しの前後で、**同条件のクリーンビルドを2回**行って出力を全件比較した。
（`_build` を消さないビルドは前回の生成物が残るため、比較の前提が崩れる。前後とも
`rm -rf _build` をコンテナ内で行ってから `sphinx-build -a` を実行した。掃き出し前の側は
`git worktree` で `51bcd12` を別ディレクトリに取り出してビルドした。）

```
diff -rq <掃き出し前のhtml> <掃き出し後のhtml>
```

| 比較対象 | 差分 |
|---|---|
| `.html` 486ページ | **0件** |
| `searchindex.js` | **差分なし** |
| `objects.inv` | **差分なし** |
| `_images/` | **差分なし** |
| `_sources/*.txt` | 11件（編集した `.rst` の原文複写。差分はここだけ） |

**差分は編集した11ファイルの原文複写だけで、レンダリング結果は1バイトも変わらない。**

掃き出し前のクリーンビルドも `build succeeded.`・WARNING 0件だった。

### 5-4. 差分が意図した編集だけであることの確認

```
git diff --numstat  → 追加220行 / 削除220行（行数の増減なし）
```

220行の内訳を機械的に分類した結果は、**下線行 96件 / `\ ` 挿入 192箇所（124行）/ それ以外 0件**である。
下線以外の行はすべて「`\ ` を除去すると変更前と完全一致し、かつ `\ ` の数が増えている」ことを確認した。

### 5-5. 未処理のまま残る申し送り5件（user 判断が要る）

`checks/task-28.md:223-234` の表の7行のうち、掃き出したのは2行。**残り5行は未処理**であり、
user が「持ち越し2件」と認識していた範囲より多い。すべて本タスクで実測して現状を確認した。

| # | 規約 | 対象 | 件数 | 現状 | 推奨 |
|---|---|---|---|---|---|
| a | S-04（下線の直後） | `implementation/testdata_notation.rst:1379`「Excel形式の場合」の下線の直後の空行 | 1件 | **未処理**（実測で `:1380` が空行） | 空行を削るだけで、HTML出力は変わらない。掃き出しと同種のため**実施を推奨** |
| b | S-04（L4の条件） | `implementation/request_unit_test/web.rst:305`「テストデータを作成する」配下のL4が1本（`:324`「アップロードファイルを用意する」）だけ | 1件 | **未処理**（実測で確認） | L4を1本消すか2本目を足すかは本文の構成の判断であり、機械的には直せない。**user 判断が要る** |
| c | S-12（UI項目名の併記） | 本文のUI項目名が「日本語(English)」併記でない箇所 | 11件 | **未処理**。`setup/request_unit_test/web.rst` に日本語のみが10語（`:186`「実行」「実行構成」・`:187`「引数」「VM 引数」・`:193`「ウィンドウ」「設定」・`:194`「インストール済みのJRE」「編集」・`:198`「デフォルトの VM 引数」・`:218`「VM 引数」）、`tools/request_data_tool.rst:104` に英語のみが1語（「Open With」） | 英語名の確認にEclipseの実機が要る。**user 判断が要る** |
| d | S-07（表内のクラス名） | `implementation/class_unit_test/entity.rst:35`（`EntityTestSupport`）・`implementation/class_unit_test/component.rst:35`（`DbAccessTestSupport`）の `:java:extdoc:` をコードリテラルへ | 2件 | **未処理**（実測で両方とも `:java:extdoc:` のまま）。どちらの表も1列目に「テストクラス」「テストデータ」「テスト対象クラス」というクラスでない行が並ぶため、S-07 の第2条に該当する | 是正するとリンクが2件消える（**HTML出力が変わる唯一の項目**）。**user 判断が要る** |
| e | `design.md` §5（3-16） | `tools/testdata_converter.rst` の `:89-101`（`<plugin>`）と `:174-183`（`<dependency>`）を、新設する「導入」（L2）へ移す | 1ページ | **未処理**（実測でL2見出しは「機能概要」「使用方法」のみ。「導入」は無い） | 節の新設と本文の移動を伴う。**user 判断が要る** |

a のみ機械的に閉じられる。b〜e は本文・出力に影響する判断を含むため、`#last` では実施していない。

## 6. `#28` ゲート10 の確定（記録のみ）

`_build/html/_sources/*.txt` に `TODO(NTF-*)` が9件残る件は、user 判断（2026-08-18、`/rn:ty`）により
**変更しないで進める**で確定。`ja/conf.py` は変更しない。理由は、`_sources/` にこのリポジトリ全325ページの
reST 原文が入っており、`html_copy_source` を落とすとNTF解説書9件だけでなくサイト全体の出力が変わるため、
NTF解説書刷新のスコープ外であること。TODO はモジュール側の判定が返り次第消える暫定マーカーである。
詳細は `checks/task-28.md` の「ゲート10 の『条件付き』の内訳」。

## 7. その他の検査

| 検査 | コマンド | 結果 |
|---|---|---|
| マッピング検証 | `python3 mapping/tools/verify_mapping.py` | exit 0・`OK: no errors` |
| 用語集検証 | `python3 mapping/tools/verify_glossary.py` | exit 0・`RESULT: OK`（9検査すべて不一致0件） |
| ツールの単体テスト | `python3 -m pytest -q` | `183 passed, 96 subtests passed` |
| 作業ツリー | `git status --short` | クリーン（`locales/ja/LC_MESSAGES/sphinx.mo` はビルド直後に復元済み） |
