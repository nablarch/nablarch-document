# 作業指示: `#7` の記録補完 — 外部から参照されている `:ref:` ラベルを記録する

配置先: `.rn/20260724-ntf-yaml-support/ntf-doc-07-followup.md`

対象ブランチ: `lovaizu/nablarch-document` の `work`（`6bf8cfb`）

判定: **`#7` は承認**。削除内容は完全に正しく、Completion criteria も満たしている。本書は差し戻しではなく、`#8〜` に着手する前に必要な記録の補完である。**ファイルの削除・復元は行わない。**

---

## 背景

`#7` は `ja/development_tools/index.rst` の toctree 参照と `ja/index.rst:54` の `:doc:` 参照を記録した。これは Steps の要求を満たしている（要求は toctree 参照1件のみ）。

しかし**リンク切れになる参照はもう1件ある。** `checks/task-07.md` には記録がない（`db_double_submit` / `how_to_set_token` で grep して0件）。

検出できなかった原因は、`:ref:` によるラベル参照が**パス文字列を含まない**ことにある。`testing_framework` で grep しても見つからない。パス参照とラベル参照は別の検査が必要である。

自動では気づけない。リポジトリに CI 設定（workflow）は存在せず、`ja/conf.py:103` は `keep_warnings = True` のため、未解決参照はビルド失敗にならず出力に警告として埋め込まれるだけである。

## 未記録の参照（1件）

| 項目 | 内容 |
|---|---|
| 参照元 | `ja/application_framework/application_framework/libraries/db_double_submit.rst:106` |
| 参照の形 | `` :ref:`テスティングフレームワークのトークン発行<how_to_set_token_in_request_unit_test>` `` |
| 文脈 | `.. important::` ブロック内。「テスティングフレームワークのトークン発行はトークンのDB保存に対応していない」という注意喚起の導線 |
| ラベル定義元（削除済み） | `06_TestFWGuide/02_RequestUnitTest.rst:169`（`.. _how_to_set_token_in_request_unit_test:` / 見出し「トークン発行」） |
| 内容を引き継ぐマッピング行 | `current-0206`（`02_RequestUnitTest.rst` 106-207、`MOVE`） |
| 新しい行き先 | 第3部 リクエスト単体テスト（ウェブアプリケーション）> 使用方法 → `implementation/request_unit_test/web.rst` |

**FW解説書側からNTF解説書への被参照であり、NTF解説書の再構築スコープ外から入ってくるリンクである。** 新ページで同名ラベルを定義しない限り、FW解説書の `.. important::` が黙って壊れる。

## `en/` 側は影響なし（確認済み）

`en/index.rst:52` と `en/development_tools/index.rst:10` も `testing_framework` を参照しているが、これらは影響しない。

- `ja/conf.py` と `en/conf.py` が別に存在し、Sphinx プロジェクトが分かれている
- `en/development_tools/testing_framework/` が独立したツリーとして存在し、削除されていない
- `en/` から削除ラベルへの `:ref:` 参照は123件あるが、すべて `en/` 内のラベルを解決する

`#7` が `ja/` 側のみを記録したのは正しい判断である。

---

## 実施

### STEP 1: `checks/task-07.md` に記録を追加する

「リンク切れになる参照」の節を、次の3件に更新する。

| # | 参照元 | 参照の形 | 対応 |
|---|---|---|---|
| 1 | `ja/development_tools/index.rst:10` | toctree `testing_framework/index` | `#8〜` の新構成確定後に更新 |
| 2 | `ja/index.rst:54` | `:doc:` `development_tools/testing_framework/index` | 同上 |
| 3 | `ja/application_framework/.../db_double_submit.rst:106` | `:ref:` `how_to_set_token_in_request_unit_test` | **`#8〜` で `implementation/request_unit_test/web.rst` に同名ラベルを定義する** |

あわせて次を記録する。

- `en/` 側が影響を受けない理由（上記「`en/` 側は影響なし」の3点）
- 検出に使ったコマンドと出力（下記STEP 2の全数調査）
- CI が無く `keep_warnings = True` のため、未解決参照がビルド失敗として検出されない旨

### STEP 2: ラベルの全数調査を行い結果を記録する

削除した47ファイルが定義していた `:ref:` ラベルを全件洗い出し、`ja/` の削除ツリー外から参照されているものを特定する。**推測せず実行結果で示すこと。**

```bash
# 削除ファイルが定義していたラベルを列挙（削除前のコミットから取得）
for f in $(git diff --name-only --diff-filter=D 2e501ad 6bf8cfb); do
  git show 2e501ad:"$f" | grep -oE '^\.\. _[A-Za-z0-9_-]+:'
done | sed 's/^\.\. _//;s/:$//' | sort -u > /tmp/labels.txt
wc -l < /tmp/labels.txt
```

次に、`ja/` 配下（削除ツリーを除く）の `.rst` から `:ref:` を抽出し、上記ラベル集合との交差を取る。`:ref:` は `` :ref:`表示文字<label>` `` と `` :ref:`label` `` の2形式があるため、両方を扱うこと。

独立検証での実測値は **定義ラベル76件 / `ja` 外部参照1件**。**件数が違う場合は、先に原因を突き止めてから進む。**

### STEP 3: `steering.md` の `#8〜` に Step を追加する

```
- [ ] 当該ページが、削除された現行解説書の外部被参照ラベルを引き継ぐ場合、
      同名の `:ref:` ラベルを新ページに定義する（対象は `checks/task-07.md`
      「リンク切れになる参照」の表を参照。現時点で1件、
      `implementation/request_unit_test/web.rst` の
      `how_to_set_token_in_request_unit_test`）
```

`#last`（Evaluation sign-off）の Completion criteria にも次を追加する。

```
- `checks/task-07.md`「リンク切れになる参照」の3件すべてが解消されている
  （toctree・`:doc:` の更新、外部被参照ラベルの再定義）
```

### STEP 4: commit & push → user review

- `checks/task-07.md` と `steering.md` の更新のみ。**`.rst` の削除・復元は行わない**
- `git diff --stat` が `checks/task-07.md` と `steering.md` の2ファイルだけであることを確認する
- commit SHA と STEP 2 の実行出力を報告して `/rn:dn` で中断し、承認まで `#8〜` に進まない

---

## ゲート

- `checks/task-07.md` の「リンク切れになる参照」が3件で、3件目に参照元 file:line・ラベル名・定義元・引き継ぐマッピング行・新しい行き先ファイルがすべて記載されている
- STEP 2 の全数調査のコマンドと出力が記録され、定義ラベル数と `ja` 外部参照数が明記されている
- `steering.md` の `#8〜` と `#last` に上記の項目が追加されている
- `ja/development_tools/testing_framework/` 配下の `.rst` が0件のまま、アセット125件が保持されたまま
- `python3 mapping/tools/verify_mapping.py` が `exit 0`、594行 / 12,986 / 11,983 が不変（本作業では `mapping.csv` を触らないため）

## 禁止事項

- 削除した `.rst` を復元しない
- `db_double_submit.rst` を今の段階で書き換えない。新ページ側で同名ラベルを定義する方針であり、参照元を変えるのは `#8〜` の結果を見てから判断する
- 件数を推測で書かない。STEP 2 の実行出力で裏付ける
- `design.md` / `mapping.csv` を変更しない
