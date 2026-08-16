# 作業依頼: `resolveTestRules()` で再現できる `TestRule` の範囲についての仕様判定と対応

宛先: `nablarch-testing-junit5` の担当

## 0. この依頼の位置づけ

NTF解説書（`nablarch/nablarch-document` の `ntf-yaml-support` ブランチ）を全面的に作り直している。その過程で、JUnit 5用拡張機能の `resolveTestRules()` に関する事象を1件確認した。**解説書にどう書くかがこの判定に依存する**ため、判定をいただきたい。

**この依頼は「不具合を直してください」ではない。** まず**NTF仕様として、この挙動が意図されたものかどうかを判定していただきたい**。仕様であれば、そう判定していただければそれでよい（解説書側に制約として書く）。不具合であれば、§4 の方針で対応をお願いしたい。

**急ぎではない。** YAML対応も解説書の刷新もいずれも開発中で、まだリリースしない。利用者はいないため、期限より**判定の正しさを優先していただきたい**。

## 1. 検証環境

| 項目 | 値 |
| --- | --- |
| 読んだもの | `~/.m2/repository/com/nablarch/framework/nablarch-testing-junit5/2.1.0/nablarch-testing-junit5-2.1.0-sources.jar` |
| バージョン | `Implementation-Version: 2.1.0`（同 jar の `META-INF/MANIFEST.MF` で確認） |
| 対象ファイル | `nablarch/test/junit5/extension/event/TestEventDispatcherExtension.java` |

**リポジトリそのものは依頼者の作業環境に無く、sources jar を展開して読んだ。** 行番号はこの sources jar のものである。最新版で状況が変わっている場合はお知らせいただきたい。

---

## 2. 観測した事実

### 2-1. 実装

`TestEventDispatcherExtension.java` の該当箇所を抜き出す。

**`:44-49` — 何も実行しない `Statement`**

```java
    private static final Statement NOOP_STATEMENT = new Statement() {
        @Override
        public void evaluate() {
            // TestRule の再現を行うときのベースとなる Statement になるため処理は何も行わない
        }
    };
```

**`:113-117` — テストメソッドの前処理**

```java
    public void beforeEach(ExtensionContext context) throws Exception {
        emulateTestRules(context);
        support.dispatchEventOfBeforeTestMethod();
    }
```

**`:122-136` — `TestRule` の再現**

```java
    private void emulateTestRules(ExtensionContext context) {
        Description description = convert(context);

        List<TestRule> testRules = resolveTestRules();
        Statement statement = NOOP_STATEMENT;
        for (TestRule testRule : testRules) {
            statement = testRule.apply(statement, description);
        }

        try {
            statement.evaluate();
        } catch (Throwable e) {
            throw new RuntimeException(e);
        }
    }
```

### 2-2. 読み取れること

各 `TestRule` は `NOOP_STATEMENT` を起点にチェーンされ、その結果の `Statement` が `beforeEach` の中で `evaluate()` される。

つまり**テスト本体は、このルールのチェーンの内側では実行されない**。ルールが受け取るのは「何もしない `Statement`」であり、テストメソッドの実行を包み込むことはできない。

このため、`Description` から情報を受け取るだけのルール（`TestName` など）は再現できるが、**テスト本体の実行を制御するルールは機能しない**と読める。

`:169-171` の既定実装も、`TestName` 1件だけを返している。

```java
    protected List<TestRule> resolveTestRules() {
        return Collections.singletonList(support.testName);
    }
```

### 2-3. 解説書側の状況

`resolveTestRules()` の Javadoc（`:149-168`）は、独自の `TestRule` を追加する方法を実装例つきで説明しているが、**再現できるルールの範囲には触れていない**。

そして現行解説書の出典（`JUnit5_Extension.rst:376-390`）は、**`Timeout` を実装例として挙げている**。上の読み取りが正しければ、`Timeout` はテスト本体の実行時間を制限するルールなので機能しない。

作り直し中の解説書は、判定が出るまで出典どおり `Timeout` の例を載せ、制約には触れていない。

---

## 3. 判定していただきたいこと

1. **上の読み取りは正しいか。** `resolveTestRules()` に登録した `Timeout` は、実際には機能しないという理解でよいか
2. **これは仕様か。** JUnit 4 の `TestRule` を完全に再現することは目的外で、`Description` を受け取るルールに限定するのが意図された設計か
3. **仕様である場合、Javadoc（`:149-168`）に制約を明記すべきか**
4. **出典（`JUnit5_Extension.rst:376-390`）が `Timeout` を実装例に挙げているのは誤りか。** 誤りであれば、解説書側は別の例に差し替える

---

## 4. 不具合と判定した場合の対応方針

**テスト駆動で対応をお願いしたい。**

1. **先に、失敗する再現テストを書く。** `resolveTestRules()` をオーバーライドして `Timeout`（または任意の、テスト本体の実行を包むルール）を返すテストクラスを用意し、そのルールが実際に効くことをアサートする。この時点でテストが**失敗すること**を確認して、テストだけをコミットする（コミットメッセージに「再現テストを追加する」旨を書く）
2. **実装を直す。** テスト本体の実行がルールのチェーンの内側に入るようにする。`beforeEach` で `evaluate()` する現在の構造では成立しないため、`InvocationInterceptor` などへの作り替えが要ると思われる（依頼者の推測であり、実装方針は担当の判断による）
3. **既存テストが壊れていないことを確認する**
4. **`resolveTestRules()` の Javadoc を、対応後の実際の範囲に合わせて更新する**

## 5. 仕様と判定した場合にお願いしたいこと

`resolveTestRules()` の Javadoc に、**再現できる `TestRule` の範囲**を明記していただきたい。解説書はその記述を出典として引くことができる。

## 6. 回答していただきたい形式

- **判定**: 仕様 / 不具合 / 判断保留（保留の場合は何が決まれば判定できるか）
- **仕様と判定した場合**: そう言える根拠と、解説書に書くべき制約の文言
- **不具合と判定した場合**: 対応する版と、おおよその見込み時期
- **`Timeout` を実装例に挙げた出典の扱い**: そのままでよいか、差し替えるべきか

解説書側は、**判定が出るまで該当箇所に TODO を残し、不具合が直る前提で本文を書く**方針で進める。仕様と判定された場合は本文を制約つきで書き直すので、その旨をお知らせいただきたい。

## 7. 禁止事項

- 依頼者は不具合と断定していない。**まず仕様かどうかを判定すること**
- 判定より先に実装を直さないこと
- 再現テストを書く前に実装を直さないこと
