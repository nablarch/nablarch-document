# 作業指示: `#13` ページ作成の共通手順を `steering.md` に定着させる

配置先: `.rn/20260724-ntf-yaml-support/ntf-doc-13-standing-rules.md`

対象ブランチ: `lovaizu/nablarch-document` の `work`（`#12` 承認後の HEAD の続き）

**ページを作らないタスクである。** `#11` で個別の作業指示として渡した内容のうち、以降の全ページに効くものを `steering.md` の共通 Steps に一度だけ入れる。**以降の小さいページは個別の作業指示を出さず、`steering.md` だけで進める。**

`ja/` 配下の `.rst` と `style.md`・`design.md`・`mapping.csv` は変更しない。

---

## STEP 1 — 「#9〜: ページの作成」の共通 Steps に4項目を追加する

既存の項目は変更しない。次の4つを追加する。

- [ ] **出典が述べている事実のうち、クラス名・プロパティ名・キー名・既定値・書式・桁数など実装で確かめられるものは、`nablarch/nablarch-testing`（YAML 側は `nablarch/nablarch-testing-yaml` の `feature/ntf-yaml`）を clone して実コードで確認してから書く。** 出典どうしが食い違う場合、および出典と実装が食い違う場合は**実装を優先**する（`design.md` §8）。確認した `file:line` と参照コミットを `reviews/page-*.md` に記録する
- [ ] **第2部と第3部の記載範囲を守る**（`design.md` §3「記載範囲」）。第2部にはコンポーネント設定ファイル・環境設定ファイルの設定項目と記述例、拡張方法を置く。**テストソースコードの実装例とテストデータの記述例は第2部に置かず、第3部へ `:ref:` で導線を張る。** 出典に含まれていても同じ。内容を落とすのではなく、事実は地の文に残してコードブロックを置かない
- [ ] **ページ先頭ラベルは `style.md` S-08 の一覧から引く**（`#12` で確定済み。新たに考案しない）
- [ ] **是正ラウンド2以降は、是正差分に限定した検証観点のみを回す。** ラウンド1で4観点（A:網羅性 / B:トンマナ / C:用語 / D:整合性）を回し、ラウンド2以降は「是正が指示範囲に収まっているか」「是正が新しい欠陥を生んでいないか」だけを見る。**各ラウンドの指摘件数と観点を `reviews/page-*.md` に記録する**（効果測定のため）

## STEP 2 — 完了条件に2項目を追加する

既存の項目は変更しない。

- 当該 `dest_page` のマッピング行が**全件**、ページのどこに反映されたかの対応表が `checks/task-NN.md` にある（`mapping_id` ごとに反映先のセクション）
- **全件表を求める項目は、ゲートの実行順の先頭に置く。母集合をホワイトリストで切り出さない**（`#10b` の申し送り）

## STEP 3 — 個別の作業指示を出す条件を明記する

「#9〜: ページの作成」の冒頭に次の趣旨を1段落で追記する。

> **個別の作業指示は、次のいずれかに当たるページにのみ出す。** それ以外のページは本節の共通 Steps に従って進める。
>
> - 出典が500 lines を超えるページ
> - `design.md` の確定事項どうし、または `design.md` と `mapping.csv` が食い違うページ
> - 出典が0行で、書く内容を設計から決める必要があるページ（導線のみの3ページなど）

---

## ゲート

`checks/task-13.md` に記録すること。

1. `git diff <基準コミット> HEAD -- ja/ .rn/20260724-ntf-yaml-support/mapping/ .rn/20260724-ntf-yaml-support/design.md` が**空**
2. `python3 mapping/tools/verify_mapping.py` が `exit 0`、**594行 / 12,986 / 11,983 が不変**
3. `steering.md` の差分が「#9〜: ページの作成」の節の中だけに収まっていること。既存の Steps・完了条件の行に削除・変更が無いこと（削除行が0行であること）
4. 追加した項目が STEP 1 の4件・STEP 2 の2件・STEP 3 の1段落で、**それ以外の追加が無い**こと

## 禁止事項

- `ja/` 配下の `.rst` を1行も変更しない。ページは作らない
- `mapping.csv` / `_batch/` / `vocabulary.md` / `glossary.md` / `style.md` / `design.md` / `ja/conf.py` を変更しない
- `steering.md` の既存の Steps・完了条件・Rules を書き換えない。**追加のみとする**
- 4観点のレビューは回さない
- user review の承認を受けるまで次タスクに着手しない

---

## 付録 — 次ページ「クラス単体テストの設定」の事前調査（レビュー役が実装で確認済み）

**本タスクの作業対象ではない。** 次のページ（`setup/class_unit_test.rst`、マッピング3行 / 193 lines）を作るときに使う。**同じ調査をやり直さなくてよい。**

確認対象は `nablarch/nablarch-testing` の `main`、コミット `e21bf67`。

### 1. `EntityTestConfiguration` のプロパティは8件。出典2件はどちらも不足している

`src/main/java/nablarch/test/core/entity/EntityTestConfiguration.java`

| プロパティ | setter の行 | 出典 `current-0021`（Nablarch Validation） | 出典 `current-0010`（Bean Validation） |
|---|---|---|---|
| `maxMessageId` | `:127` | あり | あり |
| `maxAndMinMessageId` | `:163` | あり | あり |
| `fixLengthMessageId` | `:154` | あり | あり |
| `underLimitMessageId` | `:136` | あり | あり |
| `emptyInputMessageId` | `:118` | あり | あり |
| `characterGenerator` | `:181` | あり | あり |
| **`minMessageId`** | `:145` | **無し** | あり |
| **`validationTestStrategy`** | `:199` | **無し** | **無し** |

**`minMessageId` は実装に存在する**（フィールド `:32`）。出典どうしが食い違っており、実装が正である。

**`validationTestStrategy` はどちらの出典にも無いが、実装では既定値が `new NablarchValidationTestStrategy()` である**（`:41`）。Bean Validation を使う場合は差し替えが必要になる設定であり、第2部の「コンポーネント設定ファイルの設定項目一覧」に該当する。**扱いを決めること**（記載する／記載しない）。記載しない場合はその理由を `reviews/page-class_unit_test.md` に残す。

### 2. `BasicDefaultValues` は3プロパティのみ設定可能。出典の3項目は正しい

`src/main/java/nablarch/test/core/db/BasicDefaultValues.java`

| プロパティ | setter | 既定値 | 既定値の行 |
|---|---|---|---|
| `numberValue` | `:125` | `"0"` | `:38` |
| `dateValue` | `:116` | `null` | `:41` |
| `charValue` | `:102` | `" "`（半角スペース1文字） | `:44` |

**`binaryValue` というフィールドが `:47` に存在するが setter が無く、コンポーネント設定では変更できない。** 出典が3項目しか挙げていないのは正しい。**「4つ目がある」と書かないこと。**

### 3. ページ先頭ラベル

`class_unit_test_setting`（`style.md` S-08 の一覧。`#12` で確定）。
