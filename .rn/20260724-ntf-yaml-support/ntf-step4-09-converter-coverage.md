# Step 4 指示書 — nablarch-testing-converter カバレッジ基準の適用（未達0）

宛先: `nablarch-testing-converter` 担当CC

**基準（user 確定 2026-08-31）: 本モジュールは全部新規なので、C0（行）・C1（分岐）の未達は0でなければならない。**
未達1件ごとに、まず「テストケースが足りない」のか「不要な実装」なのかを判断する。テストで到達を実現できないものだけを、理由を付けて user 判断に上げる（OK が出たら次ラウンドで未達箇所に理由コメントを入れる）。

現状の実測（`#47` 完了時 `26701b7` の記録、`checks/step4-2-report.md` §6）: 行 1632/1704 ＝ 95.77%／分岐 763/810 ＝ 94.20%。未到達分岐は `XlsFormatReader` に15件集中し、第1回から持ち越しの `XlsFormatWriter#isQuotationWrapped` 全角クォート側3分岐・`TestCoreReaderAdapter#markerGroupId` 角括弧が閉じていない側2分岐も残っている（a5f006c に両実装が実在することは 2026-08-31 にディレクターが確認済み）。

---

## 0. 渡すときの文面

```
カバレッジ基準の適用を依頼します。基準は「未達0」です。指示書を読み、
測定 → 未達全件の分類 → テスト追加・不要実装の削除 → 到達不能候補の報告、まで行って停止してください。

作業場: /home/tie303177/work/nablarch/nablarch-testing-converter（ブランチ ntf-test-data-converter、先端 a5f006c）
指示書: git show origin/ntf-yaml-support:.rn/20260724-ntf-yaml-support/ntf-step4-09-converter-coverage.md
（nablarch-document の作業ツリー /home/tie303177/work/nablarch/nablarch-document で fetch してから読む）

- 過去の分類（coverage/coverage-report.md §3 の「テスト不要15件」等）をそのまま採用しない。
  基準が変わったので全件を判断し直す。当時の分析は手がかりとしてのみ使う
- 追加した各テストは、実装をわざと壊すと落ちることを1件ずつ確認して報告に書く
- 到達不能と判断したものは、テストで実現できない理由を付けて報告し、コメントはまだ入れない
- ソース・記録に解説書（nablarch-document）への参照を書かない
```

## 1. やること

1. **測定**（HEAD ＝ `a5f006c`。src は `46457d3` とバイト同一）:

   ```bash
   rm -f jacoco.exec
   JAVA_HOME=/usr/lib/jvm/temurin-17-jdk-amd64 mvn -o clean jacoco:instrument test jacoco:restore-instrumented-classes
   JAVA_HOME=/usr/lib/jvm/temurin-17-jdk-amd64 mvn -o jacoco:report -Djacoco.dataFile=$(pwd)/jacoco.exec
   ```

   `target/site/jacoco/jacoco.xml` の line 要素から `mi>0` または `mb>0` の行を**機械抽出**し、`src/main` 全クラスの未達行・未達分岐の全件一覧（`file:line`・どちら側が未到達か）を作る。抽出コマンドを報告に載せる。

2. **分類**（未達1件ごと。根拠つき）:

   | 分類 | 判断基準 | 処置 |
   |---|---|---|
   | (a) テスト不足 | 仕様上その経路に到達する入力を組める | テストを追加する。担保内容を javadoc に1文。**実装をわざと壊すと落ちることを実測**して報告に書く |
   | (b) 不要な実装 | 呼び出しが無い、または仕様上その経路に入る入力が存在しない実装都合のコード | 削除する（本モジュールは未リリースで `src/main` 変更可）。**削除前に `git grep -n '<名前>('` で呼び出し側を全走査し、結果を報告に貼る**（定義だけの grep で「死んでいる」と判断しない） |
   | (c) 到達不能（残す） | 防御的ガード等で、テストで到達を実現できないが残すべきもの | **報告して止まる。** テストで実現できない理由・残すべき理由を書く。コメント追記は user 判断後 |

3. **再測定**: (a)(b) の処置後に同じ手順で測り直し、残る未達が (c) の一覧と完全一致することを確認する。

## 2. やらないこと

- 解説書・他モジュールを変更しない。解説書に無い「あるべき姿」を追うテストを足さない（過去に `@Ignore` 2件を削除した経緯と同じ基準）
- ソース・記録に解説書への参照（`file:line`・節見出し・逐語引用）を書かない
- (c) に分類したものへ先回りでコメントを入れない
- force push・`--amend` をしない。jacoco.exec・target/ を残さない（.gitignore 済み）

## 3. 完了条件

1. HEAD での測定結果（全体値と未達全件の `file:line` 一覧・抽出コマンド）が報告にある
2. 未達全件に (a)(b)(c) の分類と根拠がある
3. (a) は全件テスト追加済みで、再測定で当該未達が消え、**実装を壊すと落ちることの実測**が1件ずつ記録されている
4. (b) は全件削除済みで、呼び出し側全走査の grep 結果が報告にある
5. 再測定で残る未達が (c) の一覧と完全一致し、(c) 全件に「テストで実現できない理由」がある
6. `mvn -o clean test` 全件緑・`@Ignore` 0件・`git status --short` 空・修正意図ごとに1コミットで push 済み
7. `grep -rn "nablarch-document\|\.rst" src/` が0件（解説書参照なし）

## 4. 報告とレビュー

報告は ①結論（未達の内訳: 解消件数と (c) 残件数）②(c) の一覧（user 判断待ち）③追加テストと変異確認の表 ④削除一覧と grep 証明 ⑤測定ログ、の順。

レビュー（4観点）は回さない。検証はディレクターが同手順で独立に再測定し、全体値・未達一覧の一致と変異確認の抜き取り再実行で行う。

## 5. 判断結果と第2ラウンド（2026-08-31 user 判断）

**(c) 8件すべて決着した。** C1〜C5・C7・C8 は到達不能として承認（残す）。C6 のみ下記 5-1 の是正を行う。ディレクターの独立再測定は完了しており（測定値・未達29行/8分岐・変異抜き取り3件すべて一致）、本節は残作業の指示である。

### 5-1. C6 の是正 — `XlsFormatReader` の分岐末尾に安全網を追加する

`XlsFormatReader#read` の if-チェーン末尾（`else if (XlsDataTypeUtil.isSendSyncType(type)) { ... }` の後）に `else` 節を追加する（user 判断: 選択肢 (C)。同じ13種を捌く `YamlFormatWriter#sectionKey` の default throw と同型に揃える）:

```java
} else {
    // ここまでの5分岐で DataType の全13種（DEFAULT は readHeaders が除外する）を尽くしており、到達しない。
    // DataType 追加時にブロックが黙って変換結果から欠落するのを防ぎ、その場で検出するための安全網として残す。
    throw new IllegalStateException("unhandled DataType: " + type);
}
```

文面・例外メッセージは周辺の調子に合わせて整えてよい。実行文の変更はこの else 節の追加だけ。追加した throw は到達不能（承認済み扱い）で、テストは足さない。

### 5-2. 理由コメント — (c) 全箇所（新設 throw 含む）

**基準: 各コメント単体で「なぜ到達不能か」「なぜ残しているか」の両方が、そこを読んだ第三者に分かること**（user 指示 2026-08-31）。

- コメントが無い箇所には新規に入れる
- 既存コメントが片方しか言っていない箇所（例: `Styles.java:91` は unreachable としか言っていない）は同水準まで追記する。両方を既に満たす箇所（例: `DataFormat.java:47`・`YamlFormatWriter.java:503`-`:504`）は変更不要
- あわせて `XlsFormatWriter.java:273` の「isMarkerColumn の null 判定は防御として残してある」を、null 判定を削除済みの実装と整合する記述に直す
- 引き続き、カバレッジ計測・解説書・タスク番号への言及は書かない

### 5-3. 完了条件

1. 差分が「C6 の else 節（throw 1文）＋コメント行」のみ（`git diff` で確認）
2. (c) 全箇所のコメント一覧（`file:line` と逐語）が報告にあり、全件が 5-2 の基準を満たす
3. 再測定で、未達が (c) の箇所（＋新設 throw。コメント挿入分の行番号ずれは吸収して示す）と完全一致する
4. `mvn -o clean test` 全件緑（710件基準）・`git status --short` 空・push 済み

### 5-4. 報告とレビュー

報告は ①差分の逐語 ②コメント全件一覧 ③再測定値、の順。レビューは回さない（実行文の変更は到達不能な throw 1文のみで、ディレクターが実物確認と独立再測定で検証する）。
