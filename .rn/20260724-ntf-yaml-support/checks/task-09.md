# self-check: `#9` テストデータの書き方（`implementation/testdata_notation.rst`）

## 対象行の反映

`mapping.csv` の `dest_page=テストデータの書き方` 全140行（使用方法139・機能概要1、`DROP`なし）を、
観点Aレビューで140件全件を出典と突合して確認した（内訳: `05_UnitTestGuide`系29件・`06_TestFWGuide`系34件・
`ntf-doc-terms.md`/`ntf-testdata-loading.md`系19件・`ntf-testdata-doc.md`系49件・
`ntf-testdata-doc-examples-testshots.md`系9件）。`REFERENCE`区分（`current-0290`）が本文化されていないことも
`grep -n "batch_request_test"`で確認済み（該当なし）。詳細は`reviews/page-testdata_notation.md`参照。

```
$ python3 -c "
import csv
with open('mapping/mapping.csv') as f:
    rows = [r for r in csv.DictReader(f) if r['dest_page']=='テストデータの書き方']
print(len(rows), sum(1 for r in rows if r['disposition']=='DROP'))
"
140 0
```

## 4観点レビュー

A（網羅性）・B（トンマナ）・C（用語）・D（整合性）を、それぞれ別のサブエージェントで実施した。
プロンプトには「実測コマンドで裏付けよ」「検証スクリプトを正解として使わず独立に組め」「敵対的にレビューせよ」の
3点を含めた。指摘・対応内容は`reviews/page-testdata_notation.md`に全件記録済み。

## 未対応の指摘

- `must`区分は全件（A-1・A-2・B-F02〜F10・T-01・T-02・D-1）解消済み
- `decide`区分3件（A-3・B-F01・D-4）はユーザーレビューで判断を仰ぐ。理由は`reviews/page-testdata_notation.md`参照
- `note`区分2件（D-3・D-5）は実害が小さいため未対応のまま記録のみ

## `make html`（Docker、README「環境構築」＞「Docker」手順）

```
$ docker run --rm -v <repo>:/root/document nablarch-document-build-sandboxed \
    /bin/bash -c "cd /root/document; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"
(...)
/root/document/ja/application_framework/application_framework/libraries/db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test (if the link has no caption the label must precede a section header)
build succeeded, 1 warning.
```

警告1件は`#7`から追跡済みの既知警告（`checks/task-07.md`参照）で、本タスクによる新規警告は0件。

## toctree導線

`implementation/index.rst`の`toctree`に`testdata_notation`・`testdata_examples`（次ページ`#10`用スタブ）を追記済み。

## `verify_mapping.py`

```
$ python3 mapping/tools/verify_mapping.py
(...)
lines total (all rows): 12986
lines total (excluding DROP): 11983
OK: no errors
$ python3 -c "import csv; print(sum(1 for _ in csv.DictReader(open('mapping/mapping.csv'))))"
594
```

594行 / 12,986 / 11,983 いずれも不変（`mapping.csv`は本タスクで変更していない）。

## ラウンド2（差し戻し是正）self-check

2026-08-06のuser reviewで差し戻し。是正指示は `ntf-doc-09-fix.md`（STEP 1〜7）。差し戻し経緯・指摘内容は
`reviews/page-testdata_notation.md`「ラウンド2」参照。本節は同STEP 1〜7の実施結果を記録する。

### Completion Criteria

| Criterion | Self-check | Evidence |
|---|---|---|
| `mapping.csv` の当該 `dest_page` の全行が反映されている（`DROP` を除く） | OK | 本ラウンドは既存反映済み140行の記述訂正・並び替えのみで、行の追加・削除は行っていない。`mapping.csv` 自体を変更していないことは後述ゲート1・2で確認済み |
| 4観点のレビューがすべて実施・記録されている | OK | ラウンド1で4観点実施済み（`reviews/page-testdata_notation.md`）。本ラウンドはユーザー指摘・実物確認による是正であり、4観点の再実施は指示書のスコープ外（指示書冒頭「STEP 1〜7をすべて実施したうえで、再度user reviewに上げる」） |
| 未対応の指摘が残っていない、または残す判断とその理由が記録されている | OK | ラウンド2の`must`4件（A-3確定・B-F01確定・A-4・A-5）全て解消。`decide`のD-4はユーザー判断により対応済み。未対応指摘なし（`reviews/page-testdata_notation.md`「ラウンド2終了時点のまとめ」） |
| `make html` が当該ページについてエラーを出さない | OK | 下記ゲート9のDockerフルビルドで確認 |

### ゲート（ntf-doc-09-fix.md）

| # | 内容 | Self-check | Evidence |
|---|---|---|---|
| 1 | `verify_mapping.py` exit 0、594行/12,986/11,983 不変 | OK | `$ python3 mapping/tools/verify_mapping.py` → `OK: no errors`、`lines total (all rows): 12986`、`lines total (excluding DROP): 11983`。`$ python3 -c "import csv; print(sum(1 for _ in csv.DictReader(open('mapping/mapping.csv'))))"` → `594` |
| 2 | `git diff a0d09aa -- mapping.csv _batch/` が空 | OK | `$ git diff a0d09aa -- .rn/20260724-ntf-yaml-support/mapping/mapping.csv .rn/20260724-ntf-yaml-support/mapping/_batch/ \| wc -l` → `0` |
| 3 | 行頭太字（`^\*\*`）が0件 | OK | `$ grep -c "^\*\*" ja/.../testdata_notation.rst` → `0` |
| 4 | `^` 見出し7件、`~` 見出し10件 | OK | `$ grep -c '^\^\{10,\}$' ...` → `7`。`$ grep -c '^~\{10,\}$' ...` → `10`（STEP 6-2の切り出しで+1、STEP 7の廃止で-1、差し引き現状と同数） |
| 4a | `~` 見出しに `セル` 0件、`理解する`/`保つ` で終わる `~` 見出し0件 | OK | `$ awk '/^~+$/{print prev} {prev=$0}' ... \| grep -E "セル\|理解する$\|保つ$" \| wc -l` → `0`。全10件の`~`見出しタイトルを目視確認（`ファイル構成を確認する`、`データブロックの種別を確認する`、`グループIDでデータブロックを分ける`、`テーブルのデータを記述する`、`LIST_MAPのデータを記述する`、`テストケース一覧（testShots）を記述する`、`ファイルのデータを記述する`、`メッセージングのデータを記述する`、`値を特殊記法で記述する`、`コメント・マーカーカラム・空エントリを扱う`） |
| 4b | `testdata_notation-independence` ラベル0件。`.. _` 直後（空行1行）が見出しでない箇所0件 | OK | `$ grep -rn "testdata_notation-independence" ja/ \| wc -l` → `0`。全ラベルについて「空行→見出しテキスト→アンダーライン」の並びをPythonスクリプトで機械チェックし、違反0件を確認 |
| 4c | `.. note::` が0件 | OK | `$ grep -c "^\\. \\. note::" ja/.../testdata_notation.rst` → `0` |
| 5 | `requestParams`・`responseResult` がカラム表の行として存在しない（地の文には存在可） | OK | `$ grep -cE '\* - ``requestParams``\|\* - ``responseResult``' ...` → `0`。地の文（L617付近）に両語とも存在することを確認済み（gate 6と合わせて目視） |
| 6 | `searchResult` が1箇所以上 | OK | `$ grep -c "searchResult" ja/.../testdata_notation.rst` → `1`（`expectedSearch`行の説明内） |
| 7 | `about/index.rst` の `:ref:` に `testdata_notation` が1件 | OK | `$ grep -c "testdata_notation" ja/.../about/index.rst` → `1`。同じ文に既存の `testdata_converter` 参照も維持されていることを確認 |
| 8 | `style.md` S-04 に L4・`^`の記載、根拠2件以上 | OK | `mapping/style.md` S-04に表の行を追加し、`ja/application_framework/adaptors/lettuce_adaptor/redisstore_lettuce_adaptor.rst:4,20,41,48`（`Read`で見出し行・アンダーライン行を実測し47/48行目を確認）・`ja/biz_samples/12/index.rst:4,8,59,87`（同85-87行目を実測）の2件を根拠として記載 |
| 9 | Dockerフルビルド（`-a`）成功、警告は既知の`db_double_submit.rst` 1件のみ | OK | `docker run --rm -v <repo>:/root/document nablarch-document-build-sandboxed /bin/bash -c "cd /root/document; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"` → 末尾 `build succeeded, 1 warning.`。警告行: `/root/document/ja/application_framework/application_framework/libraries/db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test (if the link has no caption the label must precede a section header)`（`#7`から追跡済みの既知警告。本ラウンドによる新規警告は0件） |
| 10 | 追加・変更した段落に改行がないこと | OK | 本ラウンドで`testdata_notation.rst`に追加・変更した段落（L545の「必須」定義文、L599の`expectedSearch`説明、L617の`requestParams`/`responseResult`地の文、STEP7で`important`/`tip`化した2段落、7件のL4見出し直後の本文、`about/index.rst`L24）はいずれも`Read`で1行のみで構成されていることを確認した |

### Method適用の記録

- `file:line`引用は書く前に実ファイルを`Read`/`grep`で再確認した。具体的には `style.md` S-04の2件（`redisstore_lettuce_adaptor.rst:4,20,41,48,47-48`、`biz_samples/12/index.rst:4,8,59,87,85-87`）、`testdata_notation.rst`内の全編集対象行（L19・L128/126・L400・L447・L508・L553・L628・L665・L677・L722・L1169）、`design.md`L74・§8直後
- `grep -rn "testdata_notation-independence" ja/` は本ラウンドで実際に実行し、0件（本ページを含めどこからも参照なし）であることを確認したうえでラベルを削除した
- `nablarch-testing`実装のfile:line引用（`TestCaseInfo.java`等）は、`ntf-doc-09-fix.md`が「確認した事実」として既に検証済みのものをそのまま引用し、新たな未検証の実装事実は追加していない。参照コミットは`e21bf67`であり、`6u3`との差分は未確認であることを`reviews/page-testdata_notation.md`に明記した

- Self-check: OK

### ラウンド2 fix-round 1（Craft/Design/Verification指摘対応）

ラウンド2の記述訂正（STEP 1〜7）を経てもなお、Craft/Design両エキスパートのレビューで独立に3件の指摘が
残っていた。本節はその是正結果を記録する。ラウンド1・ラウンド2の記録は書き換えず、本節を追記のみとする。

#### Finding A（Design + Craft）— L19見出しと中身の不一致

- 指摘: L3見出し「ファイル構成を確認する」（L19-20）は、STEP 7で移設された`important`（実行順序非依存）・
  `tip`（マスタデータ再利用）の2ブロックをタイトルが示していない
- 対応: (a)見出しタイトルを「ファイル構成を確認する」→「ファイル構成と記述時の注意点を確認する」に拡張、
  (b)図の直後・`important`直前に橋渡し文「ここまでのファイル構成を踏まえたうえで、テストデータを記述する際は
  次の点に留意する。」（L126、1行のみ）を追加
- Self-check: OK
  - Before: `L19-20: ファイル構成を確認する` / `~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`
  - After: `L19-20: ファイル構成と記述時の注意点を確認する` / `~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`（アンダーライン49文字は不変）
  - 橋渡し文: `$ grep -n "ここまでのファイル構成を踏まえたうえで" ja/development_tools/testing_framework/implementation/testdata_notation.rst` →
    `126:ここまでのファイル構成を踏まえたうえで、テストデータを記述する際は次の点に留意する。`（`important`ブロックの直前に1行で挿入。本文の追加・変更のみで`important`/`tip`の本文自体は無変更）
  - `理解する`/`保つ`で終わる見出しは依然0件（新タイトルは「確認する」終わりであり、`role_check.rst:210`に前例のある動詞形を踏襲）。`セル`も含まない

#### Finding B（Craft + Design）— L451の古い道案内文

- 指摘: STEP 6-2の切り出しで新設された「LIST_MAPのデータを記述する」（L449）冒頭文が「ここではまず
  `LIST_MAP`自体の記法を説明し、続けてテストケース一覧（`testShots`）が持つカラムを処理方式ごとに説明する」
  と、testShotsカラムの説明が同じ節内にあるかのように述べていたが、実際は分割先の兄弟節
  「テストケース一覧（testShots）を記述する」（L512）にある
  - Before: `テストケース一覧は、``LIST_MAP``\ というデータタイプの利用例の1つである。ここではまず\ ``LIST_MAP``\ 自体の記法を説明し、続けてテストケース一覧（``testShots``\ ）が持つカラムを処理方式ごとに説明する。`
  - After: `テストケース一覧は、``LIST_MAP``\ というデータタイプの利用例の1つである。ここでは\ ``LIST_MAP``\ 自体の記法を説明する。テストケース一覧（``testShots``\ ）が持つカラムの処理方式ごとの説明は、後続の\ :ref:`テストケース一覧（testShots）を記述する <testdata_notation-test_shots>`\ で行う。`
- Self-check: OK
  - `$ grep -n "テストケース一覧は、\`\`LIST_MAP\`\`" ja/development_tools/testing_framework/implementation/testdata_notation.rst` →
    `451:テストケース一覧は、``LIST_MAP``\ というデータタイプの利用例の1つである。ここでは\ ``LIST_MAP``\ 自体の記法を説明する。テストケース一覧（``testShots``\ ）が持つカラムの処理方式ごとの説明は、後続の\ :ref:`テストケース一覧（testShots）を記述する <testdata_notation-test_shots>`\ で行う。`
  - 参照先ラベル`testdata_notation-test_shots`はL510に既存（新規追加なし）。1物理行のみで構成（改行なし）。内容の追加・削除ではなく、STEP 6-2の分割で生じた「ここでは…続けて…説明する」という局所性の誤りを訂正しただけであり、STEP 6-2の「内容の追加・削除は行わない」制約には抵触しない

#### Finding C（Verification）— `reviews/page-testdata_notation.md`のA-3（確定）行の引用不足

- 指摘: A-3（確定）行が「全処理方式で『必須』とは…のみを検査する」（STEP 1(a)相当）と全処理方式にまたがる
  主張をしているにもかかわらず、引用が`TestCaseInfo.java:443-448`（ウェブアプリケーションのみ）に限られており、
  `ntf-doc-09-fix.md`STEP 1(a)が挙げる`TestShot.java:77-78`（バッチ・メッセージング）・
  `EntityTestSupport.java:269-276`（エンティティバリデーション）が欠けていた
- 対応: A-3（確定）行の該当文に、処理方式ごとの内訳として3つの引用を明記
  - Before: `…（``TestCaseInfo.java:443-448``の``containsKey``判定）も確認した`
  - After: `…（ウェブアプリケーション: ``TestCaseInfo.java:443-448``の``containsKey``判定、バッチ・メッセージング: ``TestShot.java:77-78``の``assertContainsRequiredKeys``、エンティティバリデーション: ``EntityTestSupport.java:269-276``の``containsAll``判定）も確認した`
- Self-check: OK
  - `$ grep -n "TestShot.java:77-78" .rn/20260724-ntf-yaml-support/reviews/page-testdata_notation.md` → A-3（確定）行内に1件ヒット
  - `$ grep -n "EntityTestSupport.java:269-276" .rn/20260724-ntf-yaml-support/reviews/page-testdata_notation.md` → A-3（確定）行内に1件ヒット
  - ラウンド1・ラウンド2の他の行は無変更（`git diff`でA-3行1行のみの差分であることを確認）

#### ゲート再確認（3件の是正は影響しないことの確認）

```
$ F=ja/development_tools/testing_framework/implementation/testdata_notation.rst
$ grep -c '^\*\*' "$F"                              # gate 3
0
$ grep -c '^\^\{5,\}$' "$F"                          # gate 4 (^)
7
$ grep -c '^~\{5,\}$' "$F"                           # gate 4 (~)
10
$ awk '/^~+$/{print prev} {prev=$0}' "$F" | grep -c 'セル'              # gate 4a
0
$ awk '/^~+$/{print prev} {prev=$0}' "$F" | grep -cE '理解する$|保つ$'  # gate 4a
0
$ grep -c '^\.\. note::' "$F"                        # gate 4c
0
```

Dockerフルビルド（`-a`）を再実行し、既知警告1件（`db_double_submit.rst:108`）以外の新規警告が
無いことを再確認した。

```
$ docker run --rm -v <repo>:/root/document nablarch-document-build-sandboxed \
    /bin/bash -c "cd /root/document; sphinx-build -a -d _build/.doctrees/ja -b html ja _build/html"
(...)
/root/document/ja/application_framework/application_framework/libraries/db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test (if the link has no caption the label must precede a section header)
build succeeded, 1 warning.
```

gate 10（段落内改行なし）: 本ラウンドで変更・追加した3行（L19見出し・L126橋渡し文・L451道案内文）は
いずれも`grep -n`の結果が1行で完結しており、物理行内改行は無い。

## コーディネータによるレビュー（ラウンド2、`task-verify-workflow.md` Phase: Verify）

差し戻し是正（`ntf-doc-09-fix.md` STEP 1〜7、実装コミット`02f398a`）に対し、QA・Craft（writing）・
Verification（fact-check）・Design の4専門家を独立したサブエージェントとして実施した（STEP 6/7がページ構造を
改訂するため、通常の3軸に加えDesignを追加）。各プロンプトには steering.md Rules の3点
（実測コマンドで裏付けよ／検証スクリプトを正解として使わず独立に組め／敵対的にレビューせよ）を含めた。

### QA Expert Review

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| 検証アプローチがゲート10件・completion criteria・禁止事項を独立再現して確認しているか | OK | 自前のverify_mapping.py実行・自前のheading/labelパーサ・自前のgrep・自前のDockerビルドで10ゲート全件を再導出し、全てOKと一致確認。「rubber-stamped」な検証は無し |

### Design Expert（本タスクはSTEP 6/7で構造を改訂するため対象）

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Approach/structure fits | OK（fix-round後） | ラウンド1でNG（冒頭L3セクションの見出しとSTEP7統合内容の不一致）。fix-round 1で見出しを`ファイル構成と記述時の注意点を確認する`に広げ橋渡し文を追加し、design.md§11.6観点Dの文言上の基準（見出し+ページタイトルの組で中身が分かる）は満たされたことをラウンド2レビューで確認 |
| System-wide integrity（cross-doc consistency） | OK | STEP 6-2分割（LIST_MAP一般/testShots）の`:ref:`解決、`about/index.rst`からの`:ref:`解決、全14ラベルの非孤立を独立確認 |

ラウンド2Designレビューが残した指摘（「2トピックを1つのL3見出しに広げるのではなく、独立したL3見出しに分割すべき」）は
**Invalid（対象外）として却下した**。根拠: `ntf-doc-09-fix.md` STEP 7が「独立した見出しを持たせず、冒頭セクションの
中に注記として統合する。（2026-08-06 ユーザー判断）」と明記しており、指摘の推奨（独立見出しへの分割）はこの確定済み
ユーザー判断を覆す。レビュー担当自身も「design.md§11.6観点Dの文言上の基準は満たされている」と認めており、これは
達成済みの completion criteria を超えたスタイル上の代案であって、STEP 7の明示的なスコープ境界の外にある。

### Craft Expert（writing）

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Medium-specific best practice | OK（fix-round後） | ラウンド1でNG（L449の道案内文がセクション分割後も「ここで説明する」と誤った局所性を主張）。fix-round 1で`:ref:`による参照に修正し、ラウンド2レビューで解決を確認 |
| Consistency with existing style | OK（付帯意見あり） | L451の新しい参照表現`後続の:ref:`...`で行う。`が、ページ内の既存慣用句`詳細は :ref:`...` を参照。`と表現が異なる（6箇所の先例あり）。指摘は非ブロッキングの任意改善として記録し、対応は見送る（機能上・ゲート上の問題はなく、3ラウンド上限の中で必須修正を優先） |

### Verification Expert（fact-check）

| Aspect | Verdict | Evidence / Improvement |
|---|---|---|
| Artifact actually checked | OK | `style.md` S-04の2件の`file:line`引用を独自に`Read`で実測し、claimed行・階層順序と一致を確認。ラウンド2 `reviews/`の`e21bf67`/`6u3`未確認の開示が保持されていることも確認 |
| Coverage（引用の網羅性） | OK（fix-round後） | ラウンド1でNG（A-3（確定）行が「全処理方式」を主張しながら引用1件のみ）。fix-round 1で`TestShot.java:77-78`・`EntityTestSupport.java:269-276`を追加し、他行は無変更であることをラウンド2レビューで確認 |

### Overall Verdict

- Self-check: OK
- QA: OK
- Design expert: OK（fix-round後。残存指摘1件はInvalidとして却下、理由は上記）
- Craft expert: OK（fix-round後。非ブロッキングの任意改善1件は見送り）
- Verification expert: OK（fix-round後）
- Ready to check off: **No** — 本プロジェクトの`steering.md` Rules「user review の承認を受けるまで次タスクに着手しない」および`#9〜`タスクStepsの最終項目「user review — 承認を受けるまで次ページに進まない」により、上記4専門家レビュー通過後もユーザーによる `/rn:ty`（承認）または `/rn:gm`（修正）を待つ。これは通常タスクのper-taskゲートではなく、本セッション固有のページ単位ユーザーレビューであり、`task-verify-workflow.md`のPhase: Completeで自動チェックオフしない

- Self-check: OK（3件とも是正済み、ゲート3/4/4a/4c/9/10は不変で再確認済み）
