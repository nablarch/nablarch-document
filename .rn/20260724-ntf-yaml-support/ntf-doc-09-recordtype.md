# 作業指示: `#9` レコード種別の形式差の明記

配置先: `.rn/20260724-ntf-yaml-support/ntf-doc-09-recordtype.md`

対象ブランチ: `lovaizu/nablarch-document` の `work`（`b7e97b3` の続き）

`#9` は user review で**差し戻し**とする。指摘は `must` 1件のみである。本書を適用したうえで、再度 user review に上げること。

判断を求められた3件（`design.md` §4 の上書き、内容追加2件の例外、`style.md` S-07 の裁定）は**いずれも承認**である。取り消しや再検討は不要。

---

## 指摘（`must`）

`メッセージングのデータを記述する` の中で、`Excel形式の場合` と `YAML形式の場合` が、レコード種別について異なる挙動を述べている。**どちらの記述も事実として正しい。** しかし両者が異なるという事実がどこにも書かれていないため、片方だけ読む読者は差に気づかず、両方読む読者は矛盾と受け取る。

| 箇所 | 現在の記述 |
|---|---|
| 現状 L1220（`Excel形式の場合`） | `MESSAGE`（`setUpMessages`・`expectedMessages`）では記載した値が破棄され `"default"` に置き換えられる。同期応答メッセージ送信で使う4つのデータタイプと取引単体テストのモックアップクラスの電文では、**記載した値がそのままレコード種別になる** |
| 現状 L1247（`YAML形式の場合`） | `record_type` の値は、`messages` と同期応答メッセージ送信で使う4つのキーの**いずれにおいても**、常に `"default"` に置き換えられる |

**両形式の相互変換がこのページの前提である以上、この差は明記が必要である。** Excel で記述した同期応答送信の電文を YAML に変換すると、レコード種別の扱いが変わる。

### 確認済みの根拠

**Excel 経路**（`nablarch/nablarch-testing`、`main`、`e21bf67`、`nablarch-testing` 2.2.0）

- `DataFileParser.java:152` の `onReadingNames` が `createNewFragment(line)` を呼び、先頭要素がレコード種別になる
- `MessageParser.java:60-66` はこれを上書きし、`temp.remove(0)` → `temp.add(0, "default")` で先頭要素を `"default"` に差し替える。`BasicTestDataParser.java:83` により `DataType.MESSAGE` がこの経路を通る
- `SendSyncMessageParser.java:110-142` は `createFixedLengthFileParser` を上書きしているが、その無名クラスは `onReadingValues` と `createNewFile` のみを上書きしており、**`onReadingNames` は上書きしていない**。したがって基底の挙動が働き、記載した値がそのままレコード種別になる。`BasicTestDataParser.java:100` および `GroupMessageParser.java:43` がこの経路を通る

**YAML 経路**（`nablarch/nablarch-testing-yaml`、`feature/ntf-yaml`、`a966ab9`）

- `YamlFileBuilder.java:120-122` の `buildFragmentsForFile`（通常ファイル）は `buildFragmentsInternal(file, records, false, false, interps)` を呼び、`record_type` をそのまま使う
- `YamlFileBuilder.java:135-137` の `buildFragmentsForMessage` と `:150` 前後の `buildFragmentsForSendSync` は、いずれも第3引数 `skipFwHeader` に `true` を渡す。`:176-184` の `buildFragmentsInternal` は `skipFwHeader` が `true` のとき `record_type` を `DEFAULT_RECORD_TYPE`（`YamlSection.java:84` = `"default"`）に固定する
- **したがって YAML 経路では、`messages` と同期応答メッセージ送信の4キーの双方で `record_type` が `"default"` に固定される**

---

## 実施すること

### 1. 形式差を共通部に明記する

`style.md` S-10 規約1 は「両形式を比較することに意味がある内容は共通部に置く」と定めており、本件はその典型である。**`メッセージングのデータを記述する` の共通部（現状 L1105〜1211 の範囲、最初の `^` 見出しである `Excel形式の場合` より前）に、`important` として追記する。**

含める内容は次の3点に限る。

- Excel 形式では、同期応答メッセージ送信で使う4つのデータタイプと取引単体テストのモックアップクラスの電文について、記載した値がそのままレコード種別になる
- YAML 形式では、`messages` と同期応答メッセージ送信の4キーのいずれにおいても、`record_type` は常に `"default"` に固定される
- したがって、レコード種別に意味のある値を記載した Excel 形式のテストデータを YAML 形式へ変換すると、レコード種別の扱いが変わる

**「どちらが正しい」「どちらが仕様である」とは書かない。** 現在の挙動を両形式について並べて示すにとどめる。仕様意図の確定は解説書の範囲外である（下記4を参照）。

配置は、現状 L1111 の「フレームワーク制御ヘッダ以降のメッセージボディは…」の段落と、現状 L1113 の `important`（フィールド名称の重複は許容されない）の近傍が自然である。既存の `important` と統合せず、独立した `important` として置くこと。

### 2. 各形式別 L4 の既存記述は変更しない

L1220 と L1247 はいずれも正しい。**書き換えない。** 共通部の `important` から重複する内容を削らないこと（形式別 L4 だけを読む読者にも各形式の挙動が残る必要がある）。

### 3. 他の形式差の有無を確認する

同種の「両形式で挙動が異なるが、その差が共通部に書かれていない」箇所が他にないかを確認する。**確認は `メッセージングのデータを記述する` に限らず、形式別 L4 対を持つ8つの L3 すべてを対象とする。**

確認の観点は、片方の L4 が述べている挙動と、もう片方の L4 が述べている挙動が、同じ事象について異なる結果を示していないか、である。該当があれば同じ形で共通部に `important` を追加し、無ければ「確認した、該当なし」と記録すること。

**新たな事実調査を行う必要はない。** ページ内の既存記述どうしの突合で足りる。ページ内に書かれていない挙動差の探索は本書の対象外とする。

### 4. `#10` 以降への申し送りに1件追加する

`reviews/page-testdata_notation.md` の申し送りに、次を追加する。

- **レコード種別の形式差が、仕様として意図されたものか、YAML 経路の挙動乖離かは未確定である。** YAML 経路は `YamlFileBuilder` が本体パイプラインとは別に `record_type` を解決しており、`nablarch/nablarch-testing` PR #75 で扱っている「converter/YAML 経路が本体パイプラインを再実装しているための挙動乖離」と同じ型に該当する可能性がある
- 解説書側では現在の挙動を並記するにとどめ、仕様確定は PR #75 側の判断に委ねる
- 仕様が確定した場合、本ページの当該 `important` と両形式別 L4 の記述を見直す

---

## ゲート

すべて実行結果で確認し、`checks/task-09-recordtype.md`（新規）に記録すること。

1. `python3 mapping/tools/verify_mapping.py` が `exit 0`、**594行 / 12,986 / 11,983 が不変**
2. `git diff b7e97b3 HEAD -- .rn/20260724-ntf-yaml-support/mapping/` が**空**
3. `-` 見出し3件、`~` 見出し10件、`^` 見出し26件が不変
4. 追加した `important` が、`メッセージングのデータを記述する` の**最初の `^` 見出しより前**にあること
5. 現状 L1220・L1247 の2文が**変更されていない**こと（`git diff` で当該行に差分が無いこと）
6. 段落内改行0件、`:ref:` 未定義0件
7. Docker でフルビルド（`-a`）し、`build succeeded` かつ警告が**既知の `db_double_submit.rst` 1件のみ**
8. 手順3の確認結果（対象8セクション、該当の有無）を記録すること

---

## 禁止事項

- **`mapping.csv` / `_batch/` / `vocabulary.md` / `glossary.md` / `design.md` / `style.md` を変更しない。** 本件は本文への追記1件のみである
- L1220・L1247 の記述を書き換えない。どちらも正しい
- 「どちらが正しい挙動か」「どちらが仕様か」を書かない。断定できない
- 実装の内部構造（クラス名・メソッド名）を本文に書かない。読者向けの記述は挙動の説明にとどめる。根拠の `file:line` は `checks/` と `reviews/` に記録する
- 承認済みの3件（`design.md` §4 の上書き、内容追加2件、`style.md` S-07 の例外）を再検討・取り消ししない
- 手順3で、ページ内に書かれていない挙動差を新規に調査しない。既存記述どうしの突合にとどめる
- ラウンド1〜6のレビュー記録を書き換えない。追記のみとする
- user review の承認を受けるまで `#10` に着手しない
