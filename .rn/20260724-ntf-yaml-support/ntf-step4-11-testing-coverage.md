# Step 4 指示書 — nablarch-testing カバレッジ基準の適用（既存未達以外の増加0の証明と、承認済み未達2行への理由コメント）

宛先: `nablarch-testing` 担当CC

**基準（user 確定 2026-08-31）: 本体はリリース済みモジュールなので、既存の未達以外に未達が増えていてはならない。** 増えた未達は「テスト不足／不要な実装／到達不能」を判断し、到達不能は user 確認のうえ理由コメントを入れる。

既知の事実（pr75 `#27`、2026-08-21 実測・user 承認済み）: PR ブランチが `origin/develop` から変更した `src/main` の行・分岐のうち未達は `TestDataParsingTemplate.java` の2行（`:266` `tryLoadFromCache` の既定実装 `return false;`・`:277` `storeToCache` の既定実装）だけで、規約上到達不能として承認済み。ただし**モジュール全体で「既存未達が増えていない」ことの baseline 比較は未実施**。

**user 承認（2026-08-31）: この2行への理由コメント追記は、`src/main` 変更禁止（2026-08-26）の例外として認められた。** それ以外の `src/main` 変更は引き続き禁止。

## 0. 渡すときの文面

```
カバレッジ基準の適用を依頼します。①origin/develop と PR 先端の全モジュール比較で
「既存未達以外に未達が増えていない」ことを証明し、②承認済みの到達不能2行に理由コメントを入れてください。
git show origin/ntf-yaml-support:.rn/20260724-ntf-yaml-support/ntf-step4-11-testing-coverage.md
（nablarch-document の作業ツリー /home/tie303177/work/nablarch/nablarch-document で fetch してから読む）
を読み、§1〜§3 のとおり実施して報告・停止してください。
src/main の変更は②のコメント2箇所だけが許可されています。
```

## 1. やること

1. **baseline 比較**。`git worktree add --detach <一時パス> origin/develop` で baseline を取り出し、baseline と PR 先端（`convert-testdata-excel-to-text` `44b9cc9`）の両方を同じ手順で測定する:

   ```bash
   rm -f jacoco.exec
   JAVA_HOME=/usr/lib/jvm/temurin-17-jdk-amd64 mvn -o clean jacoco:instrument test jacoco:restore-instrumented-classes
   JAVA_HOME=/usr/lib/jvm/temurin-17-jdk-amd64 mvn -o jacoco:report -Djacoco.dataFile=$(pwd)/jacoco.exec
   ```

   `jacoco.xml` の line 要素（`mi`/`mb`）を機械抽出して両者の未達集合を突き合わせ、**PR 側にだけある未達**を全件列挙する（行番号ずれは差分を挟んで対応づける。クラス単位の件数比較だけで済ませない）。期待は「`TestDataParsingTemplate.java` の2行のみ」。それ以外が出たら、(a) テスト不足→テスト追加（`src/test` は追加可。実装を壊すと落ちることを実測）(b) 不要な実装・(c) 到達不能→**直さずに報告して止まる**（`src/main` に触れるため user 判断）。
   測定後は worktree を `git worktree remove --force` で片づける。

2. **理由コメント追記**（承認済み2行）。`TestDataParsingTemplate.java` の `tryLoadFromCache`・`storeToCache` の既定実装本体に、次の趣旨の1行コメントを入れる（文面は既存コメントの調子に合わせる。カバレッジや文書への言及はしない）:

   > 既定実装。cacheEnabled() が false の既定ではこの実装に到達しない（キャッシュを持つサブクラスは本メソッドを必ず実装する規約のため）。

   `storeToCache` の本体に既にある `// 既定はキャッシュ無し。` と重複しない形に整えてよい（`prepareResult` は別内容のコメントを既に持つ。2026-08-31 実測）。

## 2. やらないこと

- §1-2 のコメント2箇所以外の `src/main` 変更（1文字も）
- コメント・記録に解説書への参照を書かない
- force push・`--amend` をしない

## 3. 完了条件

1. baseline（`origin/develop` の測定 HEAD を明記）と PR 先端の両測定値・突合方法・**PR 側にだけある未達の全件一覧**が報告にある
2. その一覧が `TestDataParsingTemplate.java` の2行のみである。またはそれ以外の全件に (a)(b)(c) の分類・根拠が付き、(a) 以外は未処置のまま報告されている
3. コメント2箇所の差分がコメント行のみである（`git diff` で確認）
4. `mvn -o clean test` 全件緑（856件基準）・`git status --short` 空・worktree 残置なし・push 済み

## 4. 報告とレビュー

報告は ①結論（増えた未達の有無）②突合の方法と一覧 ③コメントの逐語、の順。レビューは回さない（コメント2行と測定報告のみ。ディレクターが独立再測定で検証する）。
