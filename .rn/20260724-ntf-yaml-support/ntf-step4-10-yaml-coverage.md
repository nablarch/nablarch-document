# Step 4 指示書 — nablarch-testing-yaml カバレッジ未達2箇所への理由コメント追記

宛先: `nablarch-testing-yaml` 担当CC

**基準（user 確定 2026-08-31）: 本モジュールは全部新規なので未達0が基準。到達不能として user が承認した未達には、未達箇所に理由コメントを入れる。**

本モジュールの未達は2箇所だけで、いずれも `#19` で user が「到達不能」と承認済み（`#45` 完了時の再測定でも同一。C0 1809/1822・C1 174/176、`.rn/ntf-yaml/report-step4-2.md` §7.1）。今回 user が理由コメントの追記を承認した（2026-08-31）。

| 箇所 | 未達 | 状態 |
|---|---|---|
| `YamlFileBuilder.java:246`-`:247`（`if (!(rowObj instanceof List)) { continue; }`） | 命令1・分岐1 | **コメントあり**（`:244`-`:245`「…通常到達不能だが、堅牢性のために残す」）。**変更不要** |
| `YamlLoader.java` static 初期化子（`schemaStream == null` の true 側・`catch (IOException e)`） | 命令12・分岐1 | **コメント無し。追記する** |

## 0. 渡すときの文面

```
カバレッジ未達2箇所のうち YamlLoader へ理由コメントを追記する作業を依頼します。
git show origin/ntf-yaml-support:.rn/20260724-ntf-yaml-support/ntf-step4-10-yaml-coverage.md
（nablarch-document の作業ツリー /home/tie303177/work/nablarch/nablarch-document で fetch してから読む）
を読み、§1〜§3 のとおり実施して報告・停止してください。src/main の変更はこのコメント追記だけです。
```

## 1. やること

1. `feature/ntf-yaml` の先端（`4837713` またはそれ以降）で、`YamlLoader.java` の static 初期化子の直前に、次の趣旨のコメントを入れる（文面は実装に合わせて整えてよい。技術的理由だけを書き、カバレッジ計測や文書への言及はしない）:

   > スキーマは本モジュールの jar に同梱するリソースであり、通常の実行環境ではクラスパスから欠落しない。`schemaStream == null` と `IOException` の分岐は、クラスローダを細工しない限り到達できない防御である。

2. 再測定して、未達が上表の2箇所のまま（コメント追記で数値が動かない）ことを確認する:

   ```bash
   rm -f jacoco.exec
   JAVA_HOME=/usr/lib/jvm/temurin-17-jdk-amd64 mvn -o clean jacoco:instrument test jacoco:restore-instrumented-classes
   JAVA_HOME=/usr/lib/jvm/temurin-17-jdk-amd64 mvn -o jacoco:report -Djacoco.dataFile=$(pwd)/jacoco.exec
   ```

## 2. やらないこと

- 上記コメント以外の `src/` 変更・テスト変更をしない
- コメントに解説書・`.rn/` 文書・タスク番号・カバレッジ計測への参照を書かない
- force push・`--amend` をしない

## 3. 完了条件

1. `YamlLoader.java` にコメントが入り、差分がコメント行のみである（`git diff` で確認）
2. 再測定の全体値と未達2箇所が `#45` 完了時（C0 1809/1822・C1 174/176、`INSTRUCTION_MISSED` 13・`BRANCH_MISSED` 2）と一致する
3. `mvn -o clean test` 全件緑（318件）・`git status --short` 空・1コミットで push 済み

## 4. 報告とレビュー

報告は ①差分（コメントの逐語）②再測定の値、の2点だけでよい。レビューは回さない（コメント追記のみ。ディレクターが実物で確認する）。

## 5. 承認と回答（2026-08-31 user 承認）

**#46 を承認する。** ディレクターの独立再測定（GitHub からの別 clone・JaCoCo agent 方式）で C0 1809/1822・C1 174/176・未達が承認済み2箇所のみ・320件緑、の一致を確認した。

State の「ディレクター判断待ち1件（§3-3 の 318件 vs 実測 320件）」への回答: **指示書の件数は更新しない。** 320件が正で、差は `#45` の T6/L6 追加によるもの。実測の記録は台帳と steering に残っており、本指示書は消費済みのため。

本指示書の作業はこれで完了。次の指示書（`ntf-step4-13` スキーマ description 全件突合）は converter の作業完了後に別途送付するので、State を更新して停止のままでよい。
