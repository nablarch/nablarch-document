# `#56` 作業指示 — 台帳の締め（`#52`〜`#54` の完了記録、`#33` (e-1)・`#34` の打ち切り）

**user 判断（2026-09-02）**:

- `#52`・`#53`・`#54` はモジュール側で完了し、承認の記録もモジュール側と本リポジトリの指示書にある。本 `steering.md` の台帳見出しだけが「送付待ち」のまま古い。**完了として閉じる。**
- `#33` の残り (e-1)（`.rn/` 内の相互参照の節見出し化）と `#34`（Docker イメージの再作成）は**捨てる（処置しない）。** (e-1) は `.rn/` 内の記録文書の書式統一で解説書本文に影響しない。`#34` は環境固有の CA の問題で、`Dockerfile` に入れない方針が既決（`steering.md` §「#34」の「方針（2026-08-21）」）。既存イメージ `nablarch-document-build` でのフルビルドは Rules「ビルド確認は自分でDockerを使って行う」のとおり動いている。

**このタスクで変えるのは `.rn/20260724-ntf-yaml-support/steering.md` と `checks/task-56.md` だけ。** `ja/` には触れない。

**レビューは回さない。** 台帳の記録更新のみで公開本文に変更が無く、差分はディレクターが実物で確認する（`nablarch/CLAUDE.md` 3-1）。

---

## 0. 着手前検証（台帳を変更しない）

§2 の表の各行を、**実物で1件ずつ確認する。** 確認の手段は次のどちらか。

- GitHub から一時ディレクトリ（リポジトリ外）へ `git clone --depth 60 --branch <ブランチ>` して `git show <ハッシュ>:<パス>`・`git log -1 <ハッシュ>` で読む
- `~/work/nablarch/<リポジトリ>` は他の CC の作業ツリーなので、**読み取り専用**（`git -C <dir> show`・`git -C <dir> log`）でのみ使う。`checkout`・`pull`・`fetch` を実行しない

反例（ハッシュが存在しない・件名が違う・引用した数値や節が無い）が1件でもあれば、§1 に進まず全件を報告して停止する。結果は `checks/task-56.md` §0 に「行・確認したコマンド・一致/不一致」で記録する。

## 1. やること

1-1. **`#52`・`#53`・`#54` を閉じる。** 見出し末尾を「— 完了（2026-09-02 user 判断で閉じる）」に改める。Rules「タスクが完全に閉じたら……エントリを圧縮する」に従い、各エントリを **Purpose 1行＋根拠（§2 の該当行をそのまま）＋指示書へのポインタ** に圧縮する。`#54` の「発端」「是正」の段落は SSoT 内部矛盾の記録なので、**圧縮せず残す**（上書きした `#41` の決定を指す記述を含むため）。

1-2. **`#33` を閉じる。** 見出し末尾に「— Closed（2026-09-02。(e-1) は user 判断で打ち切り）」を付け、「処置状況」の末尾の行「残るのは (e-1) ……のみ。別に `#34` が残る」を「(e-1) は打ち切り（user 判断 2026-09-02。処置しない。理由は `ntf-doc-56-ledger-close.md` 冒頭）」に差し替える。**それ以外の本文（処置状況・背景と未決点）は圧縮しない。** 何を処置しなかったかの記録として残す。

1-3. **`#34` を閉じる。** 見出し末尾に「— Closed（2026-09-02 user 判断・処置しない）」を付け、末尾の「**Steps**: 着手時に詳細化する。」を「打ち切り（user 判断 2026-09-02）。イメージの再作成は行わず、既存イメージ `nablarch-document-build` でのフルビルドを続ける。理由は `ntf-doc-56-ledger-close.md` 冒頭」に差し替える。本文は圧縮しない。

1-4. **`#56` のエントリ**（本指示書と同時にディレクターが追加済み）に完了の判定を書き、見出しを「— 完了」にする。

1-5. **State** を次の内容で更新する（文言は整えてよい）。Status `paused`／Last completed `#56`／Next「user の刷新版38本全量読みレビュー（質問が来たら実物で答える）。`#29` の残り（『マージ直前にまとめて処置する』の台帳）は user のマージ判断まで着手しない」。**「`#52`〜`#54` は指示書送付待ち」の文言を State から消す。**

1-6. `checks/task-56.md` に §0 の検証結果と §3 の完了条件の実測を記録する。

1-7. コミットは意図ごとに分ける（例: `#52`〜`#54` の締め／`#33`・`#34` の打ち切り／`#56` 判定と State）。push して停止する。

## 2. 根拠 — モジュール側の一次記録（§0 で全件を実物確認する）

`.rn/` 内の参照は節見出しで、他リポジトリの実物はコミットハッシュとパスで指す（Rules）。

| 台帳 | 指示書（本リポジトリ） | モジュール側の一次記録（2026-08-31。すべて `origin` の PR ブランチ上） |
|---|---|---|
| `#52` integration 再検証 | `ntf-step4-08-nablarch-testing-integration.md` §5「再実行（#54 追随後。2026-08-31 追記）」 | `nablarch-testing-integration` `feature/migrate-integration-test`: `2a0518e`「docs: complete task #25 — #54 追随後 converter での結合テスト再実行の結果を記録」。`.rn/step4-08-retest/report.md` §「R-3. Surefire summary（逐語）」に `Tests run: 546, Failures: 0, Errors: 0, Skipped: 18`。State（`d2353b7`）: Last completed `#25`・Next なし・「2026-06-25 基準（`69125c3`）へ完全に回帰」 |
| `#53` converter カバレッジ | `ntf-step4-09-converter-coverage.md` §5「判断結果と第2ラウンド（2026-08-31 user 判断）」 | `nablarch-testing-converter` `ntf-test-data-converter`: `21da937`「docs: #49 の承認を steering に記録する（(c) 第2ラウンド 完了）」。`.rn/ntf-test-data-converter/steering.md` §「#49 の承認（2026-08-31）」 |
| `#53` yaml カバレッジ | `ntf-step4-10-yaml-coverage.md` §5「承認と回答（2026-08-31 user 承認）」（**#46 を承認する**） | （承認は本リポジトリ側の §5 に記録。モジュール側の追加確認は不要） |
| `#53` 本体カバレッジ | `ntf-step4-11-testing-coverage.md` §5「承認（2026-08-31 user）」（**#29・#30 を承認する**） | `nablarch-testing` `convert-testdata-excel-to-text`: `f4f59ed`「chore: Step 4-11（#29・#30）の user 承認を記録し State をクローズ状態にする」。`docs/pr75/steering.md` State（`dcaed44`）: 「Step 4-11（カバレッジ基準）は #29・#30 とも user 承認済み」 |
| `#54` converter 追随 | `ntf-step4-12-converter-marker-rows.md` | `nablarch-testing-converter`: `8c0fcad`「docs: complete task #54 — 変異確認・カバレッジ・完了報告を記録する」。`.rn/ntf-test-data-converter/checks/step4-54-report.md` §「⑤ ゲート」に `Tests run: 731, Failures: 0, Errors: 0, Skipped: 0`。State（`9ab6648`）: 「#54（締め）まで完了」「未達 30 行／8 分岐は #49 で承認済みの到達不能箇所と完全一致」 |
| `#54` スキーマ description 全件突合 | `ntf-step4-13-yaml-schema-consistency.md` §5「第1ラウンド是正指示」・§6「Q1〜Q6 への回答」 | `nablarch-testing-yaml` `feature/ntf-yaml`: `a69084e`「docs: complete task #49 — 指示書 ntf-step4-13 §6 の Q1〜Q6 を実施する」、`b67e106`「docs: #48・#49 のユーザー承認を記録しセッションを締める」。State（`d50ee2b`）: 「#48・#49 とも 2026-08-31 にユーザー承認（`/rn:ty`）済み」「`Tests run: 324, Failures: 0, Errors: 0, Skipped: 0`」「C0 1809/1822・C1 174/176」。報告書 `.rn/ntf-yaml/report-step4-3.md` |

`#52` の再実行で緑になったのは、`#54` の追随（converter `9ab6648`・yaml `4837713`）を install した上での結果である（同 report.md §「R-2. 使った jar の証拠」）。台帳 `#52` の締めにはこの因果を1行残す。

## 3. やらないこと

- `ja/` 配下を変更しない
- 指示書 `ntf-step4-*.md`・`ntf-doc-*.md` を編集しない
- モジュール側リポジトリ（`~/work/nablarch/` 配下・clone した一時ディレクトリ）に変更を加えない。push もしない
- `#29` のエントリに触れない
- `#33`・`#34` の本文を圧縮・削除しない（1-2・1-3 の差し替え箇所のみ）

## 4. 完了条件

1. `git diff --stat 35144abc..HEAD -- ja/` が空
2. `steering.md` の `#33`・`#34`・`#52`・`#53`・`#54`・`#56` の見出しに終了語（完了／Closed）と日付があり、`#52`〜`#54` の各エントリに §2 の該当行（リポジトリ・ブランチ・コミット・パス・節）が入っている
3. `grep -n '送付待ち' .rn/20260724-ntf-yaml-support/steering.md` の結果に、`#52`〜`#54` の見出しと State が含まれない（`#54` の本文「送付は `#53` の完了後」のような経緯の記述は残ってよい）
4. `checks/task-56.md` に §0 の検証結果（全行一致）と本節 1〜3 の実測がある
5. `git status --short` が空・`origin/ntf-yaml-support` へ push 済み

## 5. 報告

①§0 の結果（一致/不一致の件数） ②コミット一覧（ハッシュと件名） ③完了条件1〜5 の実測、の順で報告して停止する。
