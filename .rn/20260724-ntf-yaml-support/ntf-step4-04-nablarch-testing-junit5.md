# Step 4 指示書 — nablarch-testing-junit5

宛先: `nablarch-testing-junit5` モジュール担当CC

---

## 0. 渡すときの文面

**担当CCには次の3つを伝えれば足りる。以下をそのまま貼る。**

```
Step 4 の作業を依頼します。指示書に11件が確定済みで載っています。探索は不要です。

作業場:
  /home/tie303177/work/nablarch/nablarch-testing-junit5/.claude/worktrees/fix-resolveTestRules
  ブランチ worktree-fix-resolveTestRules（2ebea7e）
  リポジトリ本体は main（1afcc5e）をチェックアウトしていますが、そちらでは作業しないでください。

指示書:
  /home/tie303177/work/nablarch/nablarch-document/.rn/20260724-ntf-yaml-support/ntf-step4-04-nablarch-testing-junit5.md
  nablarch-document の origin/ntf-yaml-support に入っています。
  作業ツリーが古い場合は
  git show origin/ntf-yaml-support:.rn/20260724-ntf-yaml-support/ntf-step4-04-nablarch-testing-junit5.md
  で読んでください。

指示書の「1. やること」「2. 作業一覧」「3. 完了条件」「5. 報告」に従ってください。
特に次の2つを落とさないでください。

- 足したテストそれぞれについて、期待値をわざと崩すと落ちることを1度確認し、確認したことを報告に書く
  （「テストが通る」だけでは、そのテストが何かを押さえた証拠になりません）
- #1（resolveTestRules のリスト順序）は、順序を入れ替えた負のテストを必ず書く

後始末: git status --short が空になること。jacoco.exec を残さないこと
（.gitignore に入っていません）。一時ファイル・作業用スクリプト・ログを消すこと。
```

---

## 1. やること

**解説書 `setup/junit5_extension.rst` が書いている挙動のうち、既存テストが押さえていない11件をテストで押さえる。**

探索は不要である。**下の表の11件がすべてで、これ以外を探しに行かない。**
突合はディレクターが済ませている（解説書453行を検証項目95件に分解し、既存テスト28クラス61メソッドと照合した）。

### 参照点（必ずこのピンで読む）

| リポジトリ | ピン | 読み方 |
|---|---|---|
| `nablarch-document` | `c6559eb` | `git show c6559eb:ja/development_tools/testing_framework/setup/junit5_extension.rst` |
| `nablarch-testing-junit5` | `2ebea7e`（`origin/worktree-fix-resolveTestRules`） | 作業ブランチはここから切る |

**作業ツリーの `main`（`1afcc5e`）を読まない。** ピンとは別物である。
本書の `file:line` はすべてこのピンでの行番号であり、実測で確認済みである。

### 守ること

- **`src/main` を変更しない。** 本モジュールはリリース済み（`2.1.0`）で、後方互換の対象になる利用者がいる。
  解説書のほうが正しいと判断した場合も実装を直しに行かない
- **解説書を変更しない。** 解説書が誤っていると判断したら、根拠（`file:line` と実測）を添えて報告して止める
- **書いたテストが落ちたら、直さず `@Ignore` を付けて記録する。** 落ちた事実がこの作業の成果物である。
  何を直すかはディレクターが全モジュール分を集めてから判断する
  - 理由の書式: `@Ignore("NTF-DOC: setup/junit5_extension.rst:439 — 期待 X / 実際 Y")`
- **表にない不一致を見つけても直さない。** 報告に1行書いて止める
- 事実には `file:line` とピンのハッシュを添える。示せないものは「未確認」と書く

---

## 2. 作業一覧（11件）

| # | 解説書 | 何を押さえるか | 種別 |
|---|---|---|---|
| 1 | `:439` | `resolveTestRules()` が返すリストの順序 | テスト追加 |
| 2 | `:121` | スーパクラスで宣言されたフィールドにもインジェクションされる | テスト追加 |
| 3 | `:121` | 対象フィールドが複数のとき、全部に**同じインスタンス**が入る | テスト追加 |
| 4 | `:121` | `Object` 型フィールドもインジェクション対象になる | テスト追加 |
| 5 | `:125` | 初期値を入れた `Object` 型フィールドで `IllegalStateException` になる | テスト追加 |
| 6 | `:172` | `@RegisterExtension` をインスタンスフィールドで宣言すると `beforeAll`/`afterAll` が実行されない | テスト追加 |
| 7 | `:357` | `findAnnotation` はスーパクラスのアノテーションと間接設定のアノテーションを取得できない | テスト追加 |
| 8 | `:393` | オーバーライドで `super` を呼ばないとスーパクラスの事前・事後処理が実行されない | テスト追加 |
| 9 | `:412`-`:420` | 独自拡張クラスの `@Rule` 付きフィールドは JUnit 5 では発火せず、`resolveTestRules()` の実装が要る | テスト追加 |
| 10 | `:275` | `AbstractHttpRequestTestTemplate` を直接継承した独自拡張クラスに `BasicHttpRequestTestExtension` を使える | テスト追加 |
| 11 | — | `TimeoutRuleIntegrationTest.java:80` のテスト名と Javadoc から、解説書に無くなった例への参照を外す | 名前修正 |

---

### #1 `resolveTestRules()` が返すリストの順序

**解説書 `:439`（逐語）**

> 複数の ``TestRule`` を返す場合は、リストの先頭にあるものほど内側、末尾にあるものが最も外側になる（JUnit 4の ``RunRules`` と同じ順序）。

**既存テストが押さえていない根拠**
`StandardTestRuleIntegrationTest.java:186` は `RuleChain.outerRule(recordingRule("outer")).around(recordingRule("inner"))` を1本のルールとして渡しており、確かめているのは `RuleChain` 自身の入れ子順である。
`resolveTestRules()` が返す**リストの並び**が入れ子順を決めることは、どのテストも押さえていない（61メソッド全走査で0件）。

**書くテスト**
`ConfigurableTestRuleExtension.setTestRules(TestRule...)`（`ConfigurableTestRuleExtension.java:39`）に `recordingRule("A")`・`recordingRule("B")` の2本を渡し、`RuleIntegrationTestBase.RecordingTestFixture` を `JupiterEngineRunner` で実行して `executionLog` を見る。

- `setTestRules(recordingRule("A"), recordingRule("B"))` → `["B-before", "A-before", "test", "A-after", "B-after"]`
- **順序を入れ替えた負のテストを必ず書く。** `setTestRules(recordingRule("B"), recordingRule("A"))` → `["A-before", "B-before", "test", "B-after", "A-after"]`

負のテストが無いと、「たまたま両方通る書き方」になっていないことを示せない。

---

### #2 スーパクラスで宣言されたフィールド

**解説書 `:121`（逐語）**

> インジェクションの対象になるのは、生成したインスタンスを代入できる型で宣言されたフィールドすべてである。フィールドの可視性は何でもよく、スーパクラスで宣言されたフィールドも対象になる。

**既存テストが押さえていない根拠**
`TestEventDispatcherExtensionTest.java:58` が押さえているのは**可視性**（`:45`-`:50` の public / public / protected / package-private / private の5フィールド）と、型が非互換なフィールドが `null` のままであること（`:67`）だけである。同クラスにスーパクラスは無い。
`RuleIntegrationTestBase`（`:30`）を継承するテストクラスは5本あるが、この基底クラスはインジェクション対象のフィールドを持たない（`:35` の `executionLog` は `List<String>` の static）。

**書くテスト**
インジェクション対象のフィールドを持つ基底クラスを作り、それを継承したクラスに対して `postProcessTestInstance` を呼んで、基底クラスのフィールドに値が入ることを確かめる。

**実装はこの挙動を満たしているはずである**（`TestEventDispatcherExtension.java:256`-`:258` が
`ReflectionUtils.findFields(..., HierarchyTraversalMode.BOTTOM_UP)` を使っている。`2ebea7e` 実測）。
落ちたら `@Ignore` を付けて報告する。

---

### #3 複数フィールドに同じインスタンスが入る

**解説書 `:121`（逐語）**

> 該当するフィールドが複数ある場合は、そのすべてに同じインスタンスが代入される。

**既存テストが押さえていない根拠**
`TestEventDispatcherExtensionTest.java:61`-`:65` は5フィールドそれぞれに `is(instanceOf(MockTestEventDispatcher.class))` を掛けているだけで、**互いに同一インスタンスかを見ていない**（`sameInstance` が1つも無い）。
フィールドごとに別インスタンスを生成する実装に変わっても、このテストは緑のままになる。

**書くテスト**
複数の対象フィールドが `sameInstance` であることを確かめる。既存テストを書き換えるのではなく、テストメソッドを足す。

**実装はこの挙動を満たしているはずである**（`TestEventDispatcherExtension.java:271` が
ループの外で1回だけ生成した `support` を全フィールドに `field.set` する。`2ebea7e` 実測）。

---

### #4・#5 `Object` 型フィールド

**解説書 `:121`・`:125`（逐語）**

> インジェクションの対象になるのは、生成したインスタンスを代入できる型で宣言されたフィールドすべてである。
>
> インジェクションの対象になるフィールドに、あらかじめ値を設定しておいてはならない。値が設定されている場合、Extensionクラスは ``IllegalStateException`` を送出し、そのテストは失敗する。 ``Object`` 型のフィールドも代入できる型に該当するため、初期値を設定した ``Object`` 型のフィールドを宣言していると、意図せずこの例外が発生する。

**既存テストが押さえていない根拠**
`TestEventDispatcherExtensionTest.java:45`-`:50` の5フィールドはいずれも `TestEventDispatcher` 系の型で、`Object` 型のフィールドは1つも無い。
`:71` の `IllegalStateException` のテストも `MockTestEventDispatcher` 型のフィールドで確かめている。
**解説書がわざわざ注意している経路（`Object` 型）だけが未検証である。**

**書くテスト（2件に分ける）**

- #4: 初期値を入れていない `Object` 型フィールドを宣言したクラスで、インジェクションされること
- #5: 初期値を入れた `Object` 型フィールドを宣言したクラスで `IllegalStateException` になること。メッセージも見る

**実装はこの挙動を満たしているはずである**（`TestEventDispatcherExtension.java:289`-`:291` の
`field.getType().isAssignableFrom(supportClass)` は `Object` に対して true を返す。`2ebea7e` 実測）。

---

### #6 `@RegisterExtension` をインスタンスフィールドで宣言した場合

**解説書 `:172`（逐語）**

> ``RegisterExtension`` を使う場合は、必ず ``static`` フィールドで宣言する。インスタンスフィールドで宣言すると ``beforeAll`` や ``afterAll`` などの処理が実行されず、Extensionクラスが正しく動作しない。

**既存テストが押さえていない根拠**
`@RegisterExtension` を使うテストは `TestEventDispatcherExtensionLifecycleMethodTest.java:18`-`:19` の1箇所だけで、**`static` フィールドの正しい使い方しか確かめていない**。
インスタンスフィールドで宣言したときに `beforeAll`/`afterAll` が実行されないことは、どのテストも押さえていない。

**書くテスト**
`JupiterEngineRunner` で、`@RegisterExtension` をインスタンスフィールドで宣言した実行対象クラスを動かし、`beforeAll`/`afterAll` が呼ばれないことを確かめる。
`MockTestEventDispatcherExtension`（`:35`・`:43` に `isBeforeEachInvoked()`/`isAfterEachInvoked()` がある）と同じ形で、`beforeAll`/`afterAll` の呼び出しを記録できる仮実装を用意してよい。

**この項目は解説書の警告どおりの結果になるとは限らない。** JUnit 5 の版によっては例外になる可能性がある。
その場合も**実装を直さず**、観測した結果を報告する。テストが落ちるなら `@Ignore` を付ける。

---

### #7 `findAnnotation` が取得しないもの

**解説書 `:357`（逐語）**

> ``findAnnotation(Object, Class)`` を使うと、テストクラスに設定されたアノテーションの情報を取得できる。これを使用して、独自拡張クラスに ``baseUri`` の値を渡す。取得できるのはテストクラスに直接設定されたアノテーションだけで、スーパクラスに設定されたアノテーションや、他のアノテーションを介して間接的に設定されたアノテーションは取得できない。

**既存テストが押さえていない根拠**
`TestEventDispatcherExtensionTest.java:231` は「テストクラスに直接付いていれば取れる」、`:241` は「どこにも付いていなければ `null`」を確かめている。
解説書が明示している**2つの取得できない経路**（スーパクラスに設定・他のアノテーションを介して間接的に設定）は、どちらも未検証である。

**書くテスト（負のテスト2件）**

- 基底クラスにだけアノテーションを付け、サブクラスのインスタンスに対して `findAnnotation` が `null` を返すこと
- アノテーション A の定義に `@NablarchTest` を付け、クラスには A だけを付けて、`findAnnotation(..., NablarchTest.class)` が `null` を返すこと

---

### #8 `super` を呼ばないオーバーライド

**解説書 `:393`（逐語）**

> オーバーライドするときは、必ずスーパクラスの同じメソッドを実行する。実行しないと、スーパクラスで定義された事前処理・事後処理が呼ばれなくなる。

**既存テストが押さえていない根拠**
`MockTestEventDispatcherExtension.java:21`・`:27` は `super.beforeEach(context)`/`super.afterEach(context)` を**呼んでいる**版だけで、呼ばない版が無い。
`TestEventDispatcherExtensionLifecycleMethodTest` はこの版を使っており、確かめているのは「`super` を呼んだ場合に動くこと」である。

**書くテスト**
`super` を呼ばずに `beforeEach` をオーバーライドした仮実装を用意し、`TestEventListener` の `beforeTestMethod` が呼ばれない（`beforeTestMethodInvokedCount` が増えない）ことを確かめる。
比較対象として、`super` を呼ぶ版で増えることも同じテストクラスで押さえる。

---

### #9 `@Rule` 付きフィールドは JUnit 5 では発火しない

**解説書 `:397`・`:412`-`:420`（逐語）**

> 独自拡張クラスの中でJUnit 4の ``org.junit.rules.TestRule`` を使用している場合は、本拡張機能でもそれを再現できる。
>
> （コード例）``@Rule public TestRule customRule = new CustomRule();``
>
> この場合、独自拡張用のExtensionクラスで ``resolveTestRules()`` メソッドをオーバーライドし、再現したい ``TestRule`` のリストを返すように実装する。

**既存テストが押さえていない根拠**
`resolveTestRules()` を実装した場合にルールが適用されることは、`TestRuleEmulationIntegrationTest` ほかが押さえている。
押さえていないのは**その前提**、すなわち `@Rule` を付けただけでは JUnit 5 では発火しないことである。
`src/test` 全体で `@Rule` を付けたフィールドは `TimeoutRuleIntegrationTest.java:107`（`CustomTestSupport.timeout`）の1件だけで、
それは同ファイル `:125` の `CustomTestSupportExtension.resolveTestRules()` が返している（`2ebea7e` 実測）。
**`resolveTestRules()` を実装しない場合にルールが発火しないこと**を押さえたテストは無い。

**書くテスト**
`@Rule` を付けた `TestRule` フィールドを持つ独自拡張クラスを用意し、`resolveTestRules()` を**オーバーライドしない** Extension で実行して、ルールの前処理・後処理が実行ログに一切現れないことを確かめる。
続けて、同じルールを `resolveTestRules()` で返す Extension では実行されることを確かめ、差が `resolveTestRules()` の実装だけであることを示す。

---

### #10 `AbstractHttpRequestTestTemplate` の直接継承

**解説書 `:275`（逐語）**

> ``AbstractHttpRequestTestTemplate`` を直接継承した独自拡張クラスでは、対応するExtensionクラスとして ``BasicHttpRequestTestExtension`` を使用できる。

**既存テストが押さえていない根拠**
`BasicHttpRequestTestExtensionTest.java:23` は `BasicHttpRequestTestTemplate` そのものの生成を、`:40` はアノテーション無しのときの例外を確かめている。
`AbstractHttpRequestTestTemplate` を**直接**継承した独自クラスを `BasicHttpRequestTestExtension` でインジェクションする経路は未検証である。

**書くテスト**
`AbstractHttpRequestTestTemplate` を直接継承した仮実装クラスを用意し、`BasicHttpRequestTestExtension` を継承した Extension の `createSupport` でそれを返して、テストクラスのフィールドにインジェクションされ `getBaseUri()` が合成アノテーションの値を返すことを確かめる。

---

### #11 `TimeoutRuleIntegrationTest.java:80` の名前修正

**解説書への参照が3箇所あり、いずれも指す先が無くなっている**（`2ebea7e` 実測）。

| 箇所 | 現在の文言 |
|---|---|
| `:80` | テストメソッド名 `解説書の例と同じ実装でTimeoutを追加するとテストがタイムアウトすることをテスト()` |
| `:104` | Javadoc `解説書の例と同じ形の、 {@link Timeout} をルールとして宣言した独自サポートクラス。` |
| `:112` | Javadoc `解説書の例と同じ形の、 {@link CustomTestSupport} のルールを再現する Extension。` |

解説書の独自拡張クラスの例は `:410`-`:418` で `CustomTestSupport extends TestSupport` が
`@Rule public TestRule customRule = new CustomRule();` を持つ形になっており、`Timeout` を使っていない。
さらに `:401` は `Timeout` を JUnit 5 の `@Timeout` に置き換えるよう勧めている。
テスト側の `CustomTestSupport` は `TestEventDispatcher` を継承し `Timeout` を持つ（`:106`-`:109`）ため、解説書の例とは別物である。

**テストは残す。** 3箇所から解説書への参照を外し、何を確かめているか（`resolveTestRules()` で返した `Timeout` が適用されてテストがタイムアウトすること）が文言だけで分かる形にする。

---

## 3. 完了条件

1. **11件すべてに対応がある。** テストを足したか、`@Ignore` を付けて記録したか、いずれか
2. **#1 の負のテスト（順序を入れ替えた側）がある。** 片方向だけのテストは不可
3. **足したテストが、対象の欠陥を実際に検知することを示す。**
   各テストについて、**期待値をわざと崩すと落ちること**を1度確認し、確認したことを報告に書く。
   「テストが通る」だけでは、そのテストが何かを押さえた証拠にならない
4. **`git diff 2ebea7e HEAD -- src/main` が空である**（`src/main` を変更していない）
5. **`ja/` 配下を変更していない**（解説書を変更していない）
6. `mvn test` が通る（`@Ignore` を付けたものを除く）
7. C0/C1 カバレッジを計測し、追加前後の値を報告に書く。`jacoco.exec` を作業ツリーに残さない
8. **一時ファイルを残さない。** `.claude/` などの未追跡ファイルを含め、`git status --short` が空になること
9. 変更を push する

---

## 4. レビュー

**4観点レビューは回さない。**

理由は、渡す作業が11件に確定していて探索を含まないこと、対象が `src/test` だけで公開 API・公開本文に新しいものが入らないこと、
そして完了条件3が「わざと崩すと落ちる」ことを要求しており、検証手段の妥当性（観点D）をそこで押さえていることによる。

**ディレクターが担当範囲を全量読み直して独立に検証する。**

---

## 5. 報告

次の3つだけを書く。経緯・試行錯誤は書かない。

1. **11件の結果表**（# / 対応 / テストの `file:line` / 崩したら落ちることを確認したか）
2. **`@Ignore` を付けたもの**（あれば）。`@Ignore` の理由文をそのまま貼る
3. **表にない不一致を見つけた場合**、1行ずつ。直していないこと
