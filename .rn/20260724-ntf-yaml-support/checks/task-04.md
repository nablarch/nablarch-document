# task-04 Completion Check

## Completion Criteria

| Criterion | Self-check | Evidence | QA | QA Evidence |
|---|---|---|---|---|
| 上記8観点（文体／セクション構成／セクションタイトル形式／見出し記法／コードブロック／アドミニション／表の記法／`:ref:`ラベル）すべてに規約と根拠（FW解説書ライブラリのfile:line、各2件以上）がある | OK | `mapping/style.md` に `S-01`〜`S-08` の8節を作成。各節に「規約」と「根拠」を記載し、根拠は `grep -c "^### S-"` で8件、各節の `FW:libraries/*.rst:NN` 形式の引用数は S-01=4件、S-02=8件、S-03=8件、S-04=4件、S-05=4件、S-06=9件、S-07=8件、S-08=4件（すべて2件以上）。引用したfile:lineはすべて実ファイルを`Read`/`sed -n`で開いて内容が一致することを確認済み（`exclusive_control.rst`・`date.rst`・`session_store.rst`・`static_data_cache.rst`・`code.rst`・`service_availability.rst`・`transaction.rst`・`message.rst`・`mail.rst`・`log.rst`・`format.rst`・`utility.rst`・`tag.rst`を横断） |  |  |
| `.rn/20260724-ntf-yaml-support/design.md` の第2部・第3部のページアウトラインと矛盾がない | OK（コーディネーター修正後） | 実装エキスパートの当初提出時、S-02が「機能概要→モジュール一覧→使用方法→拡張例」をNTF解説書の規約本文としており、`design.md`の「モジュール一覧の集約」節（`design.md:48-52`。依存関係は第1部「稼動環境」に集約し処理方式ごとのページには置かない）および第2部・第3部のページアウトライン（`design.md:76-88`・`design.md:132-141`。いずれもモジュール一覧を含まない）と矛盾していることをコーディネーターが独立検証（`grep -n "モジュール一覧" design.md`と該当行の直接読み込み）で発見した（コミット`01933e6`時点）。実装エキスパートに修正を発注し、S-02を「第2部: 機能概要→使用方法→拡張例／第3部: 機能概要→使用方法。いずれもモジュール一覧なし」に書き直させた（コミット`c3f8afa`）。修正後の`design.md:34,48-52,76-88,132-141,143`の引用をコーディネーターが`sed -n`で再照合し、一致を確認済み |  |  |
| 観点が8つ以外に増えていない | OK | `mapping/style.md` の `## 2. 規約一覧` 配下に `### S-` 見出しは8個のみ（`grep -c "^### S-"` → 8）。文の長さ・改行位置・図の配置・括弧の全角半角・英数字と日本語の間の空白・送り仮名の揺れ等、抽出中に気づいた他の規則性は`## 3. 検証していない事項`に「本書には記載しない」旨のみを明記し、規約としては追加していない |  |  |

## Overall Verdict

- Self-check: OK（S-02のdesign.md不整合をコーディネーターが発見・修正発注し解消。上記参照）
- コーディネーターの独立検証: `style.md`の全8節から根拠file:lineを抽出し、S-01(2件)・S-02(design.md 5件)・S-03(1件)・S-04(2件)・S-06(1件)・S-07(1件)・S-08(1件)を`sed -n`で実ファイルと直接照合し、引用文・行番号とも一致を確認。`grep -rn "^\s*\.\. note::"` `grep -rn '^+-'` で「noteの不使用」「grid tableの不使用」の否定命題も再実行し確認。`git diff --stat`でスコープ外ファイル（`glossary.md`・`term-candidates.csv`・`design.md`）への変更がないことを確認
- 4観点（QA/設計/クラフト/検証）のサブエージェントレビューは実施していない（ユーザー指示）。QA / QA Evidence列は空欄のまま残す
- 未決事項: `glossary.md` §6・§11.2が「#4で決めること」としていた3項目（括弧の全角半角、英数字と日本語間の空白、送り仮名・漢字/かなの揺れ）は、ユーザー指示によりstyle.mdの8観点に含めず、#8以降のページ作成時に都度FW解説書ライブラリの多数派表記に合わせる方針とした（`steering.md` #4「未決事項」参照）
- Ready to check off: user review待ち
