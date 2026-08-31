# Step 4 指示書 — nablarch-testing-integration 再検証（修正後モジュールでの結合テスト）

宛先: `nablarch-testing-integration` 担当CC

**2026-06-25 の全緑確認（`69125c3`「Java 17 mvn install 全緑確認」、`Tests run: 546, Failures: 0, Errors: 0, Skipped: 18`）のあと、依存する2モジュールの `src/` が大きく動いた。** 修正後のモジュールで結合テストを再実行し、結果を観測して報告するのが本タスクである。

- `nablarch-testing-yaml`（`feature/ntf-yaml`）: 是正2ラウンド（`#34`・`#45`）。`src/` の最終コミットは `3fecc4e`（2026-08-29）。remote 先端 `4837713` と `src/` はバイト同一（`git diff --stat 3fecc4e 4837713 -- src/` が空。2026-08-31 実測）
- `nablarch-testing-converter`（`ntf-test-data-converter`）: 是正2ラウンド（`#33`〜`#39`・`#40`〜`#47`）。第2回だけで `src/` 61ファイル・+2962/−716（`git diff --stat d611bec a5f006c -- src/`。2026-08-31 実測）。`src/` の最終コミットは `46457d3`、remote 先端 `a5f006c` と `src/` はバイト同一
- **`~/.m2` の converter jar は 2026-08-26 22:14 install であり、第2回の是正（`46457d3`、2026-08-28 以降）を含まない。必ず入れ直す**

---

## 0. 渡すときの文面

**担当CCには次をそのまま貼る。**

```
nablarch-testing-integration の再検証を依頼します。修正後の nablarch-testing-yaml と
nablarch-testing-converter で結合テストを一括実行し、結果を報告して停止してください。
テストが赤くなることは想定内です。目的は「どこが割れるか」の観測であり、緑にすることではありません。

作業場:
  /home/tie303177/work/nablarch/nablarch-testing-integration
  ブランチ feature/migrate-integration-test（8d92f7c）

指示書:
  /home/tie303177/work/nablarch/nablarch-document/.rn/20260724-ntf-yaml-support/ntf-step4-08-nablarch-testing-integration.md
  nablarch-document の origin/ntf-yaml-support に入っています。作業ツリーが古い場合は
  git show origin/ntf-yaml-support:.rn/20260724-ntf-yaml-support/ntf-step4-08-nablarch-testing-integration.md
  で読んでください。

指示書の「1. やること」「2. やらないこと」「3. 完了条件」「4. 報告」に従ってください。
特に次の4つを落とさないでください。

- yaml・converter は GitHub から新しく clone して install する（~/work/nablarch/ にある
  既存の作業ツリーは他の担当のものなので触らない）
- JAVA_HOME は temurin-17 を絶対パスで使う（/usr/lib/jvm/temurin-17-jdk-amd64）。
  `V=x $V/bin/java` の形は代入前に展開されるので使わない
- どのモジュールも直さない。integration 側もロジック・期待値・アサーションを変えない。
  落ちたテストは1件ずつ原因の見立てを付けて報告し、停止する
- 「どの jar で動かしたか」の証拠（install ログ・MANIFEST・javap）を報告に含める。
  Surefire の結果だけでは完了になりません
```

---

## 1. やること

### 1-1. 参照点（ピン）

| 対象 | ブランチ | ピン | 備考 |
|---|---|---|---|
| nablarch-testing-integration | `feature/migrate-integration-test` | `8d92f7c` | ローカル作業ツリーの HEAD と remote 先端が一致していることを確認してから始める |
| nablarch-testing | `convert-testdata-excel-to-text` | `44b9cc9` | `~/.m2` の jar（2026-08-21 18:28 install・`Build-Jdk: 17.0.19`）が PR ブランチ由来なら取り直し不要（確認方法は 1-2） |
| nablarch-testing-yaml | `feature/ntf-yaml` | `4837713` | **clone して install し直す** |
| nablarch-testing-converter | `ntf-test-data-converter` | `a5f006c` | **clone して install し直す**（`~/.m2` の版は古い） |

clone した HEAD がピンと一致しない場合（remote が進んでいた場合）は、**進んだ分の `src/` 差分を `git diff --stat <ピン> HEAD -- src/` で確認し、空でなければ手を止めて報告する**。docs のみなら続行してよい。

### 1-2. 事前確認（本体 jar）

```bash
javap -p -classpath ~/.m2/repository/com/nablarch/framework/nablarch-testing/6-NEXT-SNAPSHOT/nablarch-testing-6-NEXT-SNAPSHOT.jar \
  nablarch.test.core.reader.TestDataParsingTemplate | grep -c "cachedParse\|tryLoadFromCache\|storeToCache"
unzip -p ~/.m2/repository/com/nablarch/framework/nablarch-testing/6-NEXT-SNAPSHOT/nablarch-testing-6-NEXT-SNAPSHOT.jar META-INF/MANIFEST.MF | grep Build-Jdk
```

`cachedParse` 等が出れば PR ブランチ由来なので取り直し不要（この3メソッドはブランチだけが持つ）。出なければ `44b9cc9` を clone して install してから進む。

### 1-3. yaml・converter の install

新しい作業用ディレクトリ（例: `~/work/nablarch/tmp-step4-08/`）に GitHub から clone する。

```bash
git clone --branch feature/ntf-yaml https://github.com/nablarch/nablarch-testing-yaml.git
git clone --branch ntf-test-data-converter https://github.com/nablarch/nablarch-testing-converter.git
```

それぞれ HEAD がピン（`4837713`・`a5f006c`）であることを `git rev-parse HEAD` で確認したうえで、**この順に**（converter は yaml に依存する）:

```bash
JAVA_HOME=/usr/lib/jvm/temurin-17-jdk-amd64 mvn clean install
```

- **`clean` を必ず付ける**（jacoco 計装済みクラスが `target/classes` に残っていると `Cannot process instrumented class` で落ちる。実測済みの既知事象）
- 両モジュールのテストは承認済みの全緑状態なので、ここで落ちたら環境要因を疑い、ログを添えて報告して止まる
- install 後、`~/.m2` の両 jar のタイムスタンプと `Build-Jdk`（17 であること）を記録する

### 1-4. 結合テストの一括実行

```bash
cd /home/tie303177/work/nablarch/nablarch-testing-integration
JAVA_HOME=/usr/lib/jvm/temurin-17-jdk-amd64 mvn clean test
```

pom の surefire 設定（`reuseForks=false` / `forkCount=1`）はそのまま使う。2026-06-25 の基準は `Tests run: 546, Failures: 0, Errors: 0, Skipped: 18`。

### 1-5. 落ちたテストの原因特定

落ちた1件ごとに、次のどれに当たるかを見立てる。**見立てには根拠の `file:line` とコミットを添える。**

| 分類 | 意味 |
|---|---|
| (a) モジュールの是正起因 | yaml / converter の是正後の挙動と、integration のフィクスチャ・期待値（是正前の挙動前提）が食い違う |
| (b) スキーマ起因 | yaml のスキーマ検証が厳しくなり、変換生成物・固定 YAML が弾かれる（`YamlSchemaValidationTest` 含む） |
| (c) 環境・ビルド起因 | 依存解決・JDK・リソース配置など |

是正の内容は各リポジトリの `git log <June時点>..<ピン>` とコミットメッセージ・`.rn/` の steering から自分で読む。

## 2. やらないこと

- **モジュール（nablarch-testing・-yaml・-converter）を変更しない。** 見つけた問題は報告に書いて止める
- **integration のロジック・期待値・アサーションを変更しない**（本リポジトリの既存ルールどおり）。pom の依存調整を含め、変更が要ると判断したら案と根拠を報告して止まる
- **`~/work/nablarch/nablarch-testing-yaml`・`~/work/nablarch/nablarch-testing-converter` の作業ツリーに触らない**（他の担当CCのもの）
- **ソース・記録に解説書（nablarch-document）への参照を書かない**（`file:line`・節見出し・逐語引用のいずれも不可）
- force push・`--amend` をしない

## 3. 完了条件

1. 使った jar の証拠が報告にある — 本体の javap／MANIFEST 確認結果、yaml・converter の clone HEAD（ピンと一致）、install 後の `~/.m2` の jar タイムスタンプと `Build-Jdk: 17`。**これが無いと「修正後モジュールで確認した」ことにならない**
2. `mvn clean test` の Surefire summary（`Tests run: N, Failures: F, Errors: E, Skipped: S`）が**逐語で**報告にある（要約しない）
3. Skipped の全件が列挙され、由来（`@Ignore` か `Assume` か）が書いてある。2026-06-25 基準（546 / 18）との件数差が説明されている
4. Failures / Errors の全件に 1-5 の分類・根拠 `file:line`・コミットが付いている（全緑なら「0件」と明記）
5. `git status --short` が空（生成物・一時ファイルを残さない）
6. 記録を `.rn/step4-08-retest/report.md` に置き、`.rn/migrate-integration-test/steering.md` の State を更新してコミット・push し、停止する

## 4. 報告

報告は次の順で書く: ①結論（緑/赤と件数）②使った jar の証拠 ③Surefire summary 逐語 ④落ちた全件の分類表 ⑤Skipped 全件 ⑥判断を仰ぐ事項（あれば1件ずつ）。

レビュー（4観点）は回さない。新しい公開物・コード変更が無く、結果はディレクターが同じ手順を独立に再実行して検証するため。
