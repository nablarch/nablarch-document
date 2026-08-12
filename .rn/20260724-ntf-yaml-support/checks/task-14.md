# task-14 Completion Check

対象: `ja/development_tools/testing_framework/setup/class_unit_test.rst`（第2部「クラス単体テストの設定」）

初版コミット `8285125`。`sphinx.mo`（Dockerビルドが再生成した差分）は `f6947b2` で元に戻した（`#9` の `73e84dc` と同じ事象）。

## §1 マッピング全件の反映対応表（母集合は `mapping.csv` の `dest_page=クラス単体テストの設定` の全行）

母集合の切り出しは次のコマンドで行った。ホワイトリストは使っていない。

```
python3 -c "import csv;[print(r['mapping_id'],r['src_file'],r['src_body_start'],r['src_body_end']) for r in csv.DictReader(open('.rn/20260724-ntf-yaml-support/mapping/mapping.csv')) if r['dest_page']=='クラス単体テストの設定']"
```

出力は3行（`DROP` 0件）。全3行が下表に現れる。

| mapping_id | 出典（`src_file` の行範囲） | disposition | 反映先セクション | 反映先の行 |
|---|---|---|---|---|
| `current-0010` | `05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.rst` 704–770 | MOVE | 使用方法 > エンティティ単体テストの設定項目を登録する | `:16`〜`:66`（導入文・設定項目一覧の表8項目・メッセージIDの選ばれ方の段落・`important`・Bean Validation の記述例） |
| `current-0021` | `05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/02_entityUnitTestWithNablarchValidation.rst` 688–763 | MOVE | 使用方法 > エンティティ単体テストの設定項目を登録する | `:68`〜`:101`（Nablarch Validation の記述例・バリデータ側の設定と一致させる旨と記述例）。設定項目一覧は `current-0010` と同一クラスのため統合 |
| `current-0191` | `06_TestFWGuide/02_DbAccessTest.rst` 446–495 | MOVE | 使用方法 > 省略したテーブルのカラムのデフォルト値を変更する | `:105`〜`:141`（導入文と `testdata_notation-column_omission` への `:ref:`・設定項目一覧の表3項目・記述例） |

（行番号は是正ラウンド2（`5a55ada`）後の値。ラウンド2でセクションラベル行（`:103`）を追加したため、`current-0191` の反映範囲が2行後ろにずれている。`current-0021` の「（全項目必須）」は `:37` の `characterGenerator` セルに、実装で確認した実効的な必須性として反映した——詳細は §1-3。）

### §1-3 出典にあってページに文言として現れない記述の扱い

| 出典の記述 | 出典の `file:line` | ページでの扱い | 根拠 |
|---|---|---|---|
| 「（全項目必須）」 | `02_entityUnitTestWithNablarchValidation.rst:696` | **一律の必須としては書かない。** 実効的に必須な `characterGenerator` について「指定を省略するとテストの実行時に例外が発生する」を `:37` に記載 | 実装に一律の必須検査は無い（`EntityTestConfiguration` に必須検査なし、`validationTestStrategy` は `EntityTestConfiguration.java:41` で既定値あり）。`characterGenerator` は未設定で `CharsetTestVariation.java:320` が NPE |
| 第3部エンティティ単体テストへの `:ref:` | `01_entityUnitTestWithBeanValidation.rst:705`・`02_entityUnitTestWithNablarchValidation.rst:689` | **保留。** 参照先ページが未作成のため張れない | `reviews/page-class_unit_test.md` の R1-P1・申し送り1 |
| `current-0191` の設定値表（`02_DbAccessTest.rst:469-477`） | 同 `:469-477` | 表としては持ち込まず、同じ値をXML記述例（`:128`〜）に保持 | 表とXMLで値が重複しており、事実の消失がない |

### §1-2 出典どうしの食い違いの処理（`design.md` §8 により実装を優先）

| 事項 | `current-0010`（Bean Validation版） | `current-0021`（Nablarch Validation版） | 実装での確定 | ページでの扱い |
|---|---|---|---|---|
| 設定項目の件数 | 8項目（`minMessageId`・`validationTestStrategy` を含む） | 6項目 | `EntityTestConfiguration` のセッターは両方を持つ | 8項目の表に統合 |
| `maxAndMinMessageId` の意味 | 可変長・超過時 | 可変長（超過/不足の別を書かない） | `getOverLimitMessageId`（`EntityTestConfiguration.java:100-111`）で `max>min` の超過時 | 超過時と明記 |
| `underLimitMessageId` の意味 | 可変長・不足時 | 「文字列長不足時」 | `getUnderLimitMessageId`（同 `:76-91`）で `max>min` の不足時 | 最大・最小の両方を指定した項目の不足時と明記 |
| `fixLengthMessageId` の意味 | 固定長 | 固定長 | 同 `:84-85` / `:104-105` で超過・不足の双方に使われる | 双方に使われると明記 |
| `minMessageId` の有無 | あり（`:725` 表・`:736` 脚注・`:761` 記述例） | なし | `CharsetTestVariation.java:126-129` により Nablarch Validation では最大文字列長の省略が実行時エラーとなり `minMessageId` に到達しない | `current-0021` に無いのは欠落ではなく正しい。表には載せ、`important` で条件を明示 |
| `validationTestStrategy` の有無 | あり（`:731` 表・`:744` 脚注・`:767` 記述例） | なし | 既定は `NablarchValidationTestStrategy`（`EntityTestConfiguration` の初期値） | 表・記述例ともに掲載（下記 §2 の decide） |

## §2 decide の記録（`validationTestStrategy` の掲載可否）

**判定: 載せる**（ユーザー判定、2026-08-12）。

事前調査（`ntf-doc-13-standing-rules.md:79` の付録）は次の2点を挙げていたが、**いずれも指示側の誤りとして取り消された**（ユーザー確認済み）。

1. 「`validationTestStrategy` はどちらの出典にも無い」— **誤り**。`current-0010` の表（`:731`）・脚注（`:744`）・記述例（`:767`）に実在する。無いのは `current-0021` だけである。落とすと「マッピングにある内容を落とさない」に抵触する。
2. 「`minMessageId` は出典どうしが食い違っており実装が正」— **誤り**。実装上 Nablarch Validation では `minMessageId` に到達しない（`CharsetTestVariation.java:126-129`）ため、`current-0021` に無いのは欠落ではなく正しい記載である。

初版（`8285125`）は判定と同じ側で書かれているため、本文の変更は不要。

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| `mapping.csv` の当該 `dest_page` の全行が反映されている（`DROP` を除く） | OK | `python3 -c "import csv;[print(r['mapping_id'],r['disposition']) for r in csv.DictReader(open('.rn/20260724-ntf-yaml-support/mapping/mapping.csv')) if r['dest_page']=='クラス単体テストの設定']"` → `current-0191 MOVE` / `current-0021 MOVE` / `current-0010 MOVE` の3行（`DROP` 0件）。3件とも §1 の表に反映先あり。`current-0021` の未反映分「（全項目必須）」（`02_entityUnitTestWithNablarchValidation.rst:696`）は `class_unit_test.rst:37` の `characterGenerator` セルに反映済み | OK | コーディネータが独立に再抽出（`csv.DictReader`、`dest_page` 一致のみ）して3行・`DROP` 0件を確認。出典3件を `git show origin/develop:<path>` で該当行範囲まで読み、記述例XMLのプロパティが過不足なく反映されていること、`current-0021:696`「（全項目必須）」の扱いが実装（`EntityTestConfiguration` に必須検査なし／`CharsetTestVariation.java:320` の NPE）と整合することを確認した |
| 当該 `dest_page` のマッピング行が全件、ページのどこに反映されたかの対応表がある | OK | §1 の表に3行すべて（`current-0010`・`current-0021`・`current-0191`）が `mapping_id` ごとの反映先セクションつきで記載されている（`checks/task-14.md:19-21`） | OK | 反映先の行番号は是正ラウンド2（`5a55ada`）後の実値に更新済み。`current-0191` はセクションラベル行の追加で2行後ろにずれていたのをコーディネータが是正した |
| 全件表を求める項目が、ゲートの実行順の先頭に置かれている（母集合をホワイトリストで切り出していない） | OK | 全件表は本ファイル冒頭の §1（`checks/task-14.md:7`）にあり、Completion Criteria 表（`:45`）より前に置かれている。母集合は `csv.DictReader` で `dest_page` 一致のみを条件に切り出しており（`checks/task-14.md:12` のコマンド）、`mapping_id` のホワイトリストは使っていない | OK | §1 は本ファイルの先頭節であり、Completion Criteria 表より前にある。抽出条件に `mapping_id` の列挙が無いことを確認（`#10b` の申し送り「母集合をホワイトリストで切り出さない」に適合） |
| 4観点のレビューがすべて実施・記録されている | OK | `reviews/page-class_unit_test.md:47-94`。4観点（A:網羅性 / B:トンマナ / C:用語 / D:整合性）を別サブエージェントで実施し、must 4件・should 8件・note 12件を記録。是正20件（R1-1〜R1-20）・却下6件（R1-X1〜R1-X6）・保留1件（R1-P1） | OK | 4観点を**別々のサブエージェント**で実施し、self-check も他観点の判定も渡していない。プロンプトに Rules の3点を全観点入れたことを確認。ラウンド2は `#10b` の申し送りに従い是正差分限定の2観点に絞った |
| 未対応の指摘が残っていない、または残す判断とその理由が記録されている | OK | ラウンド1の是正20件は本文に反映済み（コミット `ca699c5`）。その差分限定検証で残った7件（G1〜G7）をラウンド2で是正済み — G1: L3見出しを「省略したテーブルのカラムのデフォルト値を変更する」に（`class_unit_test.rst:105`、表示幅48・下線49文字）／G2・G4: 文字列長メッセージIDの選択条件に `max`・`min` のカラム名と超過・不足の軸を明記（`:41`、`CharsetTestVariation.java:124-137`・`EntityTestConfiguration.java:76-91,100-111`）／G3: `messageIdWhenInvalidLength` を名指し（`:45`、`CharsetTestVariation.java:279-281`）／G5: 文字種不適合時のメッセージIDにデフォルト値が無いことを導入文に明記（`:16`、`CharsetTestVariation.java:41-47,153-160,296-320`）／G6: 「メッセージテンプレート」をFW解説書の先例（`bean_validation.rst:114,139`）に寄せた表現に変更（`:47`、`BeanValidationTestStrategy.java:135-150`）／G7: `class_unit_test_setting-column_default_values` ラベルを追加し `testdata_notation.rst:700` の参照を該当セクションに向けた。却下6件は `reviews/page-class_unit_test.md:78-87` に根拠つきで記録。保留1件（第3部エンティティ単体テストへの `:ref:`）は参照先ページ未作成のため `reviews/page-class_unit_test.md:89-93` と申し送り1（`:95-99`）に記録 | OK | ラウンド2で指示範囲外だった変更1件（`underLimitMessageId` の説明）も受け入れ理由つきで記録済み。未対応で理由の無い指摘は0件 |
| `make html` が当該ページについてエラーを出さない | OK | `docker run --rm -v <repo>:/root/document nablarch-document-build /bin/bash -c "cd /root/document; sphinx-build -E -a -d _build/.doctrees/ja -b html ja _build/html"` → ラウンド2の是正後も `build succeeded, 1 warning.`。警告は既知の `db_double_submit.rst:108: undefined label` 1件のみで、当該2ページの警告・エラーは0件（`-E` により全ファイル再パース済み）。G1 で見出しを変更したが `Title underline too short` は0件。G7 の `:ref:` は生成HTMLで `../setup/class_unit_test.html#class-unit-test-setting-column-default-values` を指し、当該セクションの `<div class="section" id="...">` に着地することを確認。`locales/ja/LC_MESSAGES/sphinx.mo` の再生成は `git checkout -- locales/` で復元 | OK | **コーディネータ自身も Docker で `-E -a` のフルビルドを実行**し、`build succeeded, 1 warning.`（既知件数と一致）を確認した。加えて、初版コミット `8285125` に混入していた `locales/ja/LC_MESSAGES/sphinx.mo` を `f6947b2` で元に戻した（`#9` の `73e84dc` と同じ事象） |

## 4観点レビュー（A:網羅性 / B:トンマナ / C:用語 / D:整合性）

`steering.md` Rules に従い、**4観点をそれぞれ別のサブエージェント**で実施した。各観点には成果物・目的・完了条件・チェックリストのみを渡し、本ファイル（self-check）も他観点の判定も渡していない。プロンプトには Rules が要求する3点（実測コマンドで裏付けよ／付属の検証スクリプトを正解として使わず独立に組め／敵対的にレビューせよ）を全観点に入れた。

| ラウンド | 観点 | 判定 | 指摘 | 対応 |
|---|---|---|---|---|
| 1 | A: 網羅性 | fail | must 1・should 2・note 5 | 全件トリアージ。`current-0021:696`「（全項目必須）」の脱落（must）は §1-3 のとおり実装に即して是正 |
| 1 | B: トンマナ | fail | should 3・note 5 | S-01〜S-11 の全件判定は S-07・S-03 の2件を除き準拠。S-07 の指摘は却下（R1-X1） |
| 1 | C: 用語 | fail | must 1・should 4・note 2 | 専門用語45件の全件突合表つき。`テストケース` 等の禁止表記は0件 |
| 1 | D: 整合性 | fail | must 3・should 2・note 5 | ページの主張29件を実装と全件突合。事実誤り3件（must）を検出 |
| 2 | 是正差分限定 | **pass** | must 0・should 3・note 5 | `#10b` の申し送りに従い、ラウンド2は「是正が指示範囲に収まっているか」「新しい欠陥を生んでいないか」の2観点に限定。7件（G1〜G7）を是正 |

ラウンド1の指摘は **是正20件（R1-1〜R1-20、コミット `ca699c5`）／却下6件（R1-X1〜R1-X6）／保留1件（R1-P1）**。ラウンド2の指摘は **是正7件（G1〜G7、コミット `5a55ada`）／記録のみ1件**（`underLimitMessageId` の説明も併せて直したのは指示範囲外だが、`fixLengthMessageId` 行との整合上必要な変更であり実装とも一致するため受け入れた）。各指摘の内容・根拠・判断理由は `reviews/page-class_unit_test.md` を参照。

## Overall Verdict

- Self-check: OK（完了条件6件すべて OK。4観点レビューの是正20件（ラウンド1、`ca699c5`）に加え、差分限定検証で残った7件（G1〜G7）をラウンド2で是正済み。却下6件・保留1件は理由を記録済み。Dockerビルドは `build succeeded, 1 warning.` で既知警告1件のみ、`Title underline too short` は0件）
- QA（コーディネータの独立検証）: OK
- Design expert: N/A（ページ作成タスクでは `steering.md` のA〜D観点を用いる）
- Craft expert: OK（観点B。ラウンド2で pass）
- Verification expert: OK（観点D＋ラウンド2の差分限定検証。ページの主張を実装と全件突合し、Dockerフルビルドで確認）
- Ready to check off: **user review 承認待ち**（`steering.md` Rules「user review の承認を受けるまで次タスクに着手しない」）

---

## 締め — デフォルト値の制約に実装の根拠を書き足す（`ntf-doc-14-close.md`）

公開本文は承認済み。本追記は表の説明セル2件と申し送り1件のみで、4観点のレビューは回していない（作業指示の明示指定）。

### STEP 1・2 — 追記した2セル

| 設定項目 | 追記後の説明セル | 実装（`nablarch/nablarch-testing` `main` = `e21bf67`） |
|---|---|---|
| `charValue` | 文字列型のデフォルト値。**固定長文字列型（`CHAR`・`NCHAR`）では、指定した値をカラム長の数だけ繰り返した文字列が使われる** | `src/main/java/nablarch/test/core/db/BasicDefaultValues.java:158-159`（`getCharValue` → `StringUtil.repeat(charValue, length)`）。可変長文字列型・`CLOB` はそのまま返す（同 `:147` `getVarcharValue`・`:182` `getClobValue`） |
| `numberValue` | 数値型のデフォルト値。**カラム長を超える値を指定した場合は、先頭からカラム長の分だけ切り出した値が使われる** | 同 `:171-172`（`getNumberValue` → `NablarchTestUtils.limit(numberValue, length)`）→ `src/main/java/nablarch/test/NablarchTestUtils.java:290-300`（`string.length() > threshold ? string.substring(0, threshold) : string`） |

「指定できる値」列（`1文字のASCII文字`・`0または正の整数`）は変更していない。`dateValue` の行も変更していない（`setDateValue` は `Timestamp.valueOf` に渡すだけで、繰り返しも切り詰めも起きない。`BasicDefaultValues.java:116-118`）。

**出典の制約に検査の裏付けが無いことも確認済み** — `setCharValue` は1文字でなければ `IllegalArgumentException` を投げるが**ASCII かどうかは検査しない**（`BasicDefaultValues.java:102-108`、実測 `:103` が `charValue.length() != 1`）。`setNumberValue` に検査は**無い**（同 `:125-127`、実測 `:126` が代入のみ）。したがって制約は「実装が弾くから守る」ものではなく、**上表の加工挙動によって守らないと壊れる**ものである。この点を説明セルに書き足したのが本追記であり、ラウンド1の `R1-X4`（実装が検査しないから緩めるか／推奨値として維持するか）が実装の挙動を示さないまま処理されていた不足を埋める。申し送りは `reviews/page-class_unit_test.md` の「`#15` 以降への申し送り」6 に追記した。

**実装の確認方法**: `git clone --depth 50 https://github.com/nablarch/nablarch-testing.git`（`git log --oneline -1` → `e21bf67 Merge remote-tracking branch 'origin/release-6u2'`）。作業指示に記載された5件の `file:line` を、コーディネータが**すべて実ファイルで独立に再確認**した（`grep -n` の実測行番号が指示と一致）。

### ゲート

| # | ゲート | 結果 | 実行内容 |
|---|---|---|---|
| 1 | `git diff 104a6c4 HEAD -- ja/` の変更が説明セル2行だけ・削除行0行 | OK（注記あり） | `1 file changed, 2 insertions(+), 2 deletions(-)`。変更されたのは `class_unit_test.rst:117` と `:120` の説明セル2行のみ。**既存文言は両行とも先頭にそのまま残しており、削除された記述は0件**（追記は末尾への文の追加）。行単位のdiffでは追記でも `-`/`+` の対で表示されるため、`deletions(-)` が2と出る。他ファイル・他行の変更は0 |
| 2 | `1文字のASCII文字`・`0または正の整数` が各1件残存 | OK | `grep -c` → それぞれ `1`・`1` |
| 3 | `verify_mapping.py` が `exit 0`、594行 / 12,986 / 11,983 が不変 | OK | `python3 mapping/tools/verify_mapping.py` → `Loaded 594 rows` / `lines total (all rows): 12986` / `lines total (excluding DROP): 11983` / `OK: no errors`、`exit=0` |
| 4 | `mapping/`・`ja/conf.py`・`design.md`・`style.md` の差分が空 | OK | `git diff 104a6c4 -- <上記>` → 出力0行 |
| 5 | 見出しの文言・並び順が不変、`:ref:` 未定義0件、段落内改行0件 | OK | 見出しを `104a6c4` 版と機械比較 → 4件で完全一致（`クラス単体テストの設定`=／`使用方法`-／`エンティティ単体テストの設定項目を登録する`~／`省略したテーブルのカラムのデフォルト値を変更する`~）。未定義ラベル警告は当該ページ0件（ゲート6）。段落内改行の検出スクリプト（空行を挟まず日本語の本文行が連続する箇所）→ 0件 |
| 6 | Docker フルビルド（`-a`）で `build succeeded`・警告は既知1件のみ | OK | `docker run --rm -v <repo>:/root/document nablarch-document-build /bin/bash -c "cd /root/document; sphinx-build -E -a -d _build/.doctrees/ja -b html ja _build/html"` → `build succeeded, 1 warning.`。警告は `db_double_submit.rst:108: WARNING: undefined label: how_to_set_token_in_request_unit_test` の**既知1件のみで新規0件**（`grep -iE "warning\|error"` で全出力を確認）。生成HTMLで両セルの描画を確認（`固定長文字列型（CHAR・NCHAR）では、指定した値をカラム長の数だけ繰り返した文字列が使われる`／`カラム長を超える値を指定した場合は、先頭からカラム長の分だけ切り出した値が使われる`。`\ ` エスケープによる余分な空白なし）。ビルドが再生成した `locales/ja/LC_MESSAGES/sphinx.mo` は `git checkout -- locales/` で復元 |

### Overall Verdict（締め）

- 追記2件・申し送り1件のみ。禁止事項（「指定できる値」列・`dateValue` 行・表の列構成・見出し・他セクション・`mapping.csv` 他の設定文書・承認済みの他ページ）はいずれも変更していない
- 既存のレビュー記録・チェック記録は書き換えず、追記のみとした
- Ready to check off: **user review 承認待ち**（承認まで `#15` に着手しない）
