# NTF 解説書 刷新版 レビューガイド

チームメンバー・TL が刷新版をレビューするための申し送りです。読むのは刷新版の HTML で、本書は「このページはどこから来たか」「利用者のどんな困りごとを、どう考えて変えたか」「どこを開いて何を判断してほしいか」だけを伝えます。

## レビューの進め方

| | |
|---|---|
| 読むもの | 刷新版の HTML（`ja/development_tools/testing_framework/` 配下 38 ページ。配布方法は別途連絡） |
| 比較する相手 | v6 の公開解説書 https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/index.html （各ページの申し送りに、元になった v6 ページの URL を書いてあります） |
| 順序 | 1. 「全ページ共通の申し送り」を読み、「全体で判断してほしいこと」に答える → 2. 担当ページの申し送りを読み、「レビューポイント」の箇所を刷新版で開いて判断する |
| 分担 | TL: 全ページ共通の申し送り（構成・削除・方針）と第1部。メンバー: 担当領域のページ（第2部の設定と第3部の実装は処理方式ごとに対になっています） |
| コメント先 | PR #728 https://github.com/nablarch/nablarch-document/pull/728 のレビューコメント（該当行に付けてください。ページ全体への意見は「Files changed」のファイル先頭行へ） |
| 気にしなくてよいこと | 用語の統一、`:ref:` 化、JUnit 5 形式へのコード例の書き換え、図の差し替え、表の折り返しなどの機械的・横断的な変更は「全ページ共通の申し送り」で1回だけ判断してください。ページ別には書いていません |

## 全ページ共通の申し送り

**刷新の全体像**: v6 の 47 ページ（入口の index 1 ページと `guide/development_guide` 配下 46 ページ。https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/index.html ）を、38 ページ・4 部構成に組み直した。第1部「テスティングフレームワークとは」（1 ページ）は、テストの種類とアーキテクチャなど、アーキテクトとアプリケーションプログラマに共通する前提。第2部「テスティングフレームワークの導入と設定」（16 ページ）は、アーキテクトが行う導入と設定。第3部「テスティングフレームワークによるテスト実装」（16 ページ）は、アプリケーションプログラマが行うテストデータの記述とテストコードの実装。第4部「テスティングフレームワークの提供ツール」（4 ページ）は、ツールごとに導入と使い方を1箇所で完結させる。v6 は「単体テスト実施方法」（テスト実装者向け）・「自動テストフレームワークの使用方法」（アーキテクト向け）・「プログラミング工程で使用するツール」の3本立てで、設定の説明と実装手順が同じページに混在し、横断の設定は「目的別API使用方法」に散らばっていた。

**全ページに共通する変更と、その考え方**
- JUnit 5 を標準にした: v6 は JUnit 4 ベースを前提に書かれ、JUnit 5 は「JUnit 5用拡張機能」という追加機能の扱いだった。新しくテストを書く利用者はブランクプロジェクトも JUnit 5 と Extension の構成であるため、解説書全体を JUnit 5 前提に反転し、第3部 9 ページの Java コード例（63 ブロック）を、サポートクラスを継承する書き方から合成アノテーション（`@BasicHttpRequestTest`・`@DbAccessTest` など）でサポートクラスをインジェクションする書き方に書き換えた。JUnit 4 で書き続ける方法（継承方式・junit-vintage-engine）は第2部「JUnit 4での使用」1 ページに集約した。
- 導入と設定を横断ページに集めた: v6 では、テスト用トランザクション・テストデータの読み込み先・システム日時の固定・採番の置き換えなど、テストの種類によらず要る設定が「目的別API使用方法」や方式別のページに散らばり、アーキテクトは何をどの順で設定すればよいか一望できなかった。読者の目的で「テスティングフレームワークの導入」「テストデータの設定」「システム日時と採番の固定」の 3 ページに分け、方式別の設定ページには方式に固有の設定だけを残した。`testTran` の登録は、デフォルト設定 `nablarch/test/test-transaction.xml` を import する手順に改めた（ブランクプロジェクトと同じ）。
- 解説書に書く基準を決めて当てた: v6 には実装と食い違う記述・古い製品名・「間違えたときにどうなるか」の注意が混ざり、利用者が読むべき記述を埋もれさせていた。(a) 実装と食い違う記述は実装を優先する（例: `\n` を LF に変換するという記述は、実装 `LineSeparatorInterpreter` が `\r` しか変換しないため落とした。`htmlCheckerConfig` は「`htmlChecker` を設定しなかった場合のみ有効」ではなく `HttpTestConfiguration#setHtmlCheckerConfig` が `htmlChecker` を作り直すため逆向きに直した）。(b) 陳腐化した例示は落とす（Pentium4、`-Xverify:none`、「Nablarch5u18以降の」）。(c) 無いと手順が動かない設定は足す（`httpServerFactory`。未登録だと `SimpleRestTestSupport` が内蔵サーバを生成できず例外になる）。(d) 書くのは「利用者が正しく書こうとしても踏むもの」だけとし、「間違えたときにどうなるか」は書かない。
- 用語を統一した: v6 は同じものを複数の語で呼んでいた。`自動テストフレームワーク`→`テスティングフレームワーク`（v6 で 70 行）、`テストケース`→`テストショット`（v6 で 189 行。1 回の実行に対応する 1 組の入力と期待値を指す語で、プロジェクトのテスト仕様書上のテストケースとは層が違うため語を分けた）、`スーパークラス`→`スーパクラス`（`インタフェース` など他のカタカナ語と同じく長音を省く側に揃えた）。
- 図を描き直した: v6 の画像 107 件は、内部構造のクラス図・Excel のスクリーンショット・Eclipse の画面が中心で、利用者がテストを書くために要る図と、図でなくてよいものが混ざっていた。「文章より図で見せたほうが利用者が理解しやすいか」を基準に 21 枚（構成図・シーケンス図・テストデータのレイアウト図）を PlantUML で新しく描き、原本 `.puml` をリポジトリに置いた。Excel のスクリーンショットは表に書き直し、ツール操作の画面キャプチャ 10 枚は残した。
- 各ページ先頭の「機能概要」を読者価値の型に揃えた: v6 のページ冒頭は見出しの言い換えや存在告知になっていて、読んでも何が嬉しいか分からなかった。「その設定・機能は何のためにあるか」「読者はいつ要るか（必須か、特定の場合だけか）」「代表例 1〜2 件」の 3 点で書く型に統一した（導線だけの 3 ページと記載例ページを除く 32 ページ）。
- テストデータの YAML 形式を併記した: テストデータを AI エージェントが生成・解析できるよう、Excel 形式に加えてテキストの YAML 形式を導入した（`nablarch-testing-yaml` の `YamlTestDataParser`。既存の `BasicTestDataParser` を継承し、YAML ファイルを直接読む）。第3部「テストデータの書き方」は記法ごとに「Excel形式の場合」「YAML形式の場合」を対で示し（8 対）、「テストデータの記載例」は用途ごとに両形式の実例を並べた（34 対）。YAML への切り替え設定は「テストデータの設定」、形式の相互変換は第4部「テストデータ変換ツール」（新規ページ）にある。
- 表の見た目を直した: テーマが表のセルを折り返さないため、NTF の表は横スクロールが出ていた。146 表すべてに折り返しを指定した。Excel シートを再現した 10 表は、識別子やパスが語の途中で切れて見える害の方が大きいため横スクロールのまま残した。

**削除したもの（v6 にあって刷新版に無いもの）**
- 実体の無い行（41 行）: RST の内部アンカーラベルだけの節 30 行と、toctree・目次だけの節 11 行 → 新構成でラベルと toctree を組み直したため、移すものが無い。
- 重複（26 行）: v6 の RESTful ウェブサービスのリクエスト単体テストにあった「前提条件」「テストクラスの書き方」配下の 6 節（別ページに詳しい版がある）、取引単体テストの「テスト結果エビデンスの収集」の二重掲載、YAML 対応の設計資料にあった用語表・カラム一覧 → より詳しい側だけを残した。
- 設計資料の内部設計・開発プロセス（29 行）: テストデータ変換ツール設計書のクラス図・アダプタ設計・品質担保工程・リポジトリ分割手順、テストデータ読み込み機構の 4 段階・状態機械・キャッシュ → 利用者がテストを書くために知る必要が無い。
- 陳腐化・実装と食い違う記述: ウェブの「テストの実行速度を上げる ＞ JVMオプションの指定」小節（`-Xverify:none` は JDK 13 で非推奨。テスティングフレームワークが読む設定でもない）、`nablarch-testing` の `<exclusions>`（jetty・findbugs は現在の依存に無い）、バッチ・MOM の「常駐化機能を無効化する」（`MainForRequestTesting` にそのコードが無い）→ 残すと今日の読者が誤る。
- 図・画像・サンプルファイル: 内部構造のクラス図 9 件（利用者がテストコード・テストデータ・設定に名前を書かないクラスの関係）、Excel のスクリーンショット（表に書き直した）、`:download:` のサンプル Java・xlsx 10 本（エンティティ単体テスト 6 本・コンポーネント単体テスト 4 本。旧ツリーの撤去で参照が壊れ、実ファイルも失われた）。
- 個別に判断してほしい削除: (1) `:download:` のサンプルファイル 10 本 — 復元できないため、記載例ページの Excel/YAML の例で代替できているか。(2) ウェブの JVM オプション小節 — 落とす判断は済んでいるが、実行速度で困る利用者への案内が無くなってよいか。(3) 落とした記録が見つからない削除（ウェブのリクエストスコープの Form 取得・`SqlRow` のコード例、ファイルアップロードの具体例、テストデータの書き方の `forwardUri` の例示・`description` の脚注など）— 各ページの申し送りに挙げてある。

**全体で判断してほしいこと**
1. JUnit 5 を標準にし、JUnit 4 を「JUnit 4での使用」1 ページに寄せた位置づけでよいか。JUnit 4 で書き続けるプロジェクトが、第3部の合成アノテーション方式のコード例を継承方式に読み替えられるか。
2. 横断の設定を「導入」「テストデータの設定」「システム日時と採番の固定」に集め、方式別ページには方式固有の設定だけを残した構成で、アーキテクトが設定漏れなく辿れるか。`testTran` を `nablarch/test/test-transaction.xml` の import で登録する手順が、ブランクプロジェクトの `unit-test.xml` と合っているか。
3. 実装を優先して v6 の記述を変えた方針でよいか。特に、実装の挙動が意図どおりか（`\n` を LF に変換しない `LineSeparatorInterpreter`、`htmlCheckerConfig` が `htmlChecker` を上書きする `HttpTestConfiguration`）。実装側の不具合であれば解説書ではなく実装を直す判断になる。
4. 「間違えたときにどうなるか」を書かない基準で、利用者が実際に困る注意まで落としていないか（例: 同期応答メッセージ送信で `expectedMessage`・`responseMessage` を空欄にすると失敗する旨）。
5. YAML 形式を Excel 形式と対等に併記したことで、Excel だけを使う読者にとって「テストデータの書き方」「テストデータの記載例」が読みにくくなっていないか。
6. 内部構造のクラス図を落とし、利用者向けの構成図・シーケンス図 21 枚に置き換えた判断でよいか。実装を知るレビュアーから見て、図が示す関係（インジェクション、ハンドラキュー経由の呼び出し、モックアップクラスの位置）が実装と合っているか。

# ページ別の申し送り

## 入口

### テスティングフレームワーク（`index.rst`）

**由来**: 既存。v6「テスティングフレームワーク」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/index.html ）から。見出し 1（L1 のみ。L2〜L4 は無い）のうち内容変更 1・文面調整のみ 0・新設 0。

**利用者観点の課題と変更の考え方**
- v6 の入口ページは toctree 3本（単体テストガイド／テスティングフレームワークガイド／テストツール）の下に「実装者は unitTestGuide、アーキテクトは testFWGuide」の1文があるだけで、各ガイドに何が書いてあるか・どの順に読むかが分からなかった。刷新版は「とは／導入と設定／テスト実装／ツール」の4部構成にし、各部の役割と対象読者を1段落ずつ書き、「役割を問わず、まず〈とは〉を読む」と読む順序を示した。
- v6 の important 2件（Jakarta Batch・マルチスレッド非対応）は入口ページから外し、〈テスティングフレームワークとは〉の「テストの種類」節末に移した。何に対応するかを説明する節の裏返しとして、同じ場所で読める方が理解が続くという考え方である。
- 冒頭に「JUnit をベースに Nablarch アプリケーションのテストを補助する機能を提供するフレームワーク」の1文を置き、入口だけで何のツールか分かるようにした。

**レビューポイント**
1. 4部の役割説明: 「アーキテクトが導入と設定」「アプリケーションプログラマがテストデータの記述とテストコードの実装」という分担が、実際のプロジェクトでの役割分担と合っているか。
2. 読む順序: 「役割を問わず、まず〈テスティングフレームワークとは〉を読むこと」の指示が、目次（toctree）より上の文章だけで伝わるか。
3. important 2件の移設: 対応しない基盤（Jakarta Batch・マルチスレッド）の注意が入口ページに無くてよいか。

## 第1部 テスティングフレームワークとは

### テスティングフレームワークとは（`about/index.rst`）

**由来**: 混在。v6「自動テストフレームワーク」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/01_Abstract.html の「特徴」「自動テストフレームワークの構成」「テストメソッド記述方法」「テストデータは全てExcelシートに記述する」）と、v6「テスティングフレームワーク」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/index.html の important 2件）から。見出し 8 のうち内容変更 4・文面調整のみ 1・新設 3。

**利用者観点の課題と変更の考え方**
- v6 の「特徴」は「JUnit4ベース／Excel に外部化できる／Nablarch 特化 API」と機能を並べるだけで、利用者に何が嬉しいのかも、3種類のテストが何かも書いていなかった。刷新版は冒頭で3種類（クラス単体＝クラス単位、リクエスト単体＝1リクエスト単位、取引単体＝複数リクエストにまたがる業務単位）を定義し、特徴を「本番同等の経路でテストできる」「テストコードは定型かつ少量で済む」「テストデータ形式を選べる」「JUnit の書き方を活かせる」という利用者の利益で書き直した。
- v6 は「どのテストを書けばよいか」を判断する材料が無く、対応しない基盤（Jakarta Batch・マルチスレッド）の注意だけが入口ページにあった。「テストの種類」節を新設し、3種類の対比表（実行方法・テスト範囲）と、リクエスト単体テストの6処理方式の内訳表を置いた。取引単体テストの手動／自動は、v6 が明言している3処理方式（ウェブ＝手動、REST・バッチ＝自動）だけを名指しし、残る3処理方式は述べていない。
- v6 は「JUnit4ベース。JUnit 5 で動かすなら Vintage 参照」で、JUnit 5 でテストを書く人が自分向けの説明を見つけにくかった。「対応するJUnitのバージョン」を「JUnit 5 で使用する。JUnit 4 の既存資産があれば〈JUnit 4での使用〉」に反転した。
- v6 の構成図と構成物表（構成物・説明・作成者）は「図を見れば分かる」内容の再掲だった。表を落とし、図を「サポートクラスをインジェクションして使う／準備データ投入と期待値照合はサポートクラス／クラス単体は直接呼び出し、リクエスト単体はハンドラキュー経由／NAF はテスト用のコンポーネント設定ファイルを読む」の4点に絞って描き直し、サポートクラスの継承関係の図を加えた。

**レビューポイント**
1. 全体像: 3種類のテストの粒度の定義（クラス単位／1リクエスト単位／複数リクエストにまたがる業務単位）が、現場での使い分けと合っているか。
2. テストの種類（対比表と直後の段落）: 取引単体テストの実行方法を「ウェブ＝手動操作、REST・バッチ＝JUnit で自動実行」とだけ書き、MOM・HTTPメッセージング・テーブルをキューとして使ったメッセージングには触れていない。利用経験から、名指ししないままでよいか、あるいは誤りが無いか。
3. テストの種類（6処理方式の内訳表）: 各行の説明（例: ウェブアプリケーションの行「Ajax等のリッチクライアントは未対応」）が現状の実装・利用実態と合っているか。
4. 対応するJUnitのバージョン: 「テスティングフレームワークは、JUnit 5 で使用する」と言い切り、JUnit 4 を既存資産向けの位置づけにしてよいか。
5. アーキテクチャ: 図2枚が実装と合っているか。構成図の4つの関係と、継承関係の図（`TestEventDispatcher` を頂点に `TestSupport`・`DbAccessTestSupport`・`EntityTestSupport`・`HttpRequestTestSupport`→`AbstractHttpRequestTestTemplate`→`BasicHttpRequestTestTemplate`・`StandaloneTestSupportTemplate`→`BatchRequestTestSupport`／`MessagingRequestTestSupport`→`MessagingReceiveTestSupport`・`IntegrationTestSupport`・`SimpleRestTestSupport`→`RestTestSupport`）の各注記（どのテストで使うか）が正しいか。

## 第2部 導入と設定

### テスティングフレームワークの導入（`setup/introduction.rst`）

**由来**: 混在。v6 に対応するのは「取引単体テスト（MOM）＞必要な単体テストライブラリのpom.xmlへの追加」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/send_sync.html ）の依存関係だけで、残りは刷新で書き起こした。見出し 5 のうち内容変更 1・文面調整のみ 1・新設 3。

**利用者観点の課題と変更の考え方**
- v6 では `nablarch-testing` を pom に足す手順が MOM の取引単体テストのページにしか無く、他の処理方式の読者は見つけられなかった。テストの種類によらず最初に行う3つ（依存関係・テスト用のコンポーネント設定ファイル・テストデータ投入用トランザクション）をこのページに集めた。依存関係は `test` スコープにし、v6 の `<exclusions>`（jetty・findbugs）は現在の `nablarch-testing` に当該依存が無いため落とした。
- 第2部のどのページも「テスト用のコンポーネント設定ファイル」が何か・どこに置くか・本番用とどう切り替えるかを書いておらず、リンクをたどっても設定方法にたどり着けなかった。クラスパス直下の `unit-test.xml` に本番用を import して上書きすること、テスト用の環境設定ファイルは import の後に `config-file` で読むことを、ブランクプロジェクトの複製で動かして確かめたうえで書いた。
- `testTran` は v6 のどこにも無いが、登録していないと準備データの投入時点で例外になる。デフォルト設定 `nablarch/test/test-transaction.xml` の import を主手順にし、ファクトリ名が異なる場合だけ手書きするようにした。

**レビューポイント**
1. テスティングフレームワークを依存関係に追加する: `<exclusions>` を落としてよいか（プロジェクトで jetty・findbugs の衝突を経験していないか）。tip「専用のモジュールが `nablarch-testing` に依存する場合は個別に追加しなくてよい」は、ブランクプロジェクトが `nablarch-testing-rest` 経由で `nablarch-testing` を得ている構成と合っているか。
2. テスト用のコンポーネント設定ファイルを用意する: 記述例（本番用 import → デフォルト設定 import → 上書き → `config-file`）が、ブランクプロジェクトの `src/test/resources/unit-test.xml` の書き方と合っているか。環境設定値の優先順位（後から読み込んだ値が優先）の説明が正しいか。
3. テストデータの投入に使用するトランザクションを登録する: `nablarch/test/test-transaction.xml` の import を主手順にしてよいか。手書き例が `transactionFactory` に `jdbcTransactionFactory` を参照している点が、「別名で登録している場合」の例として自然か。
4. 機能概要: 「テストの種類によらず次の3つを行う」で、導入時に必要なものが漏れていないか（例: `nablarch-testing-default-configuration` の依存など、実プロジェクトで併せて入れているもの）。

### JUnit 5での使用（`setup/standard_usage.rst`）

**由来**: 既存。v6「JUnit 5用拡張機能」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/JUnit5_Extension.html ）から。前提事項の surefire 条件だけは v6「自動テストフレームワーク」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/01_Abstract.html の「JUnit 5で自動テストフレームワークを動かす＞前提条件」）から。見出し 15 のうち内容変更 8・文面調整のみ 7・新設 0。

**利用者観点の課題と変更の考え方**
- v6 は「拡張機能」としてガイドの末尾にあり、新しくテストを書く人が JUnit 4 と 5 のどちらで書くべきか分からなかった。刷新版は「JUnit 5での使用」を第2部の導入ページ直後に置き、機能概要を「テスティングフレームワークは JUnit 4 前提の継承設計 → サポートクラスの前処理・後処理は JUnit 4 のアノテーションで動くため JUnit 5 から継承しても動かない → だから Extension を提供 → 新規は JUnit 5 で書く。ブランクプロジェクトも JUnit 5 構成」の順に書き直した。
- v6 の依存関係は `nablarch-testing-junit5` 1件だけで、JUnit 5 本体をどう入れるかは読者任せだった。`junit-bom` 5.11.0 の `dependencyManagement` と `junit-jupiter` を加え、`nablarch-testing-rest` が optional で推移的に解決されない旨の tip を足した。
- v6 の注意書きは実装と食い違う箇所があった。「対象フィールドが null でないとエラー終了」を、インジェクション対象の決まり方と `IllegalStateException` で失敗すること、`Object` 型のような幅広い型のフィールドを宣言しないことに書き換えた。「RegisterExtension でも利用できる」には `BasicHttpRequestTestExtension` だけは適用できない例外を足した。v6 の tip 2件（`SimpleRestTestSupport` は Class 不要、`AbstractHttpRequestTestTemplate` には `BasicHttpRequestTestExtension`）は実装と合わず削除した。
- v6 の「TestRule を再現する」は `Timeout` を例にし「スーパクラスの `resolveTestRules()` をベースにせよ」と書いていたが、`Timeout` は `DbAccessTestExtension` と併用すると DB 接続を取れないままテストが成功する。例をプロジェクト独自の `TestRule` に差し替え、「JUnit 5 に同等機能があれば移植しない」の対応表と、テストが失敗せずに壊れる5件の warning を追加した。

**レビューポイント**
1. 機能概要: 「新規は JUnit 5 で書く」と迷わず読めるか。「サポートクラスの前処理・後処理は JUnit 4 のアノテーションで動くため、JUnit 5 のテストクラスから継承しても動かない」が実装 `TestEventDispatcher`（`@BeforeClass`・`@Before`・`@After`）と合っているか。
2. 依存関係を追加する: `junit-bom` 5.11.0 と `junit-jupiter` の書き方がブランクプロジェクトと一致しているか。
3. テストクラスに合成アノテーションを設定する: インジェクション対象の条件（代入できる型すべて・可視性不問・スーパクラスのフィールドも・複数なら全部・0件なら何もしない・値が入っていれば `IllegalStateException`）が `TestEventDispatcherExtension#postProcessTestInstance` と合っているか。「`Object` 型のフィールドはテストクラスで宣言しない」という注意が実務上の困りごとに当たるか。
4. RegisterExtensionでExtensionクラスを適用する: `BasicHttpRequestTestExtension` だけ適用できないという例外が `BasicHttpRequestTestExtension#createSupport` と合っているか。
5. JUnit 4のTestRuleを再現する: 本文は `nablarch-testing-junit5` の修正版（`resolveTestRules()` の基底実装が空リストを返し、内部ルールは `resolveInternalTestRules()` が返す）を前提にしている。リリース済みの 2.1.0 では基底の `resolveTestRules()` が内部ルール（`TestName`）を返すため、2.1.0 の読者が本文どおりに書くと内部ルールが落ちる。解説書の公開とモジュールのリリースの前後関係をどう扱うか判断してほしい。あわせて warning 5件（`@BeforeEach` との順序、`@BeforeEach` 失敗時、`Timeout` と `DbAccessTestExtension`、`@TestFactory`、`@Nested`）の内容が修正版の Javadoc と合っているか。
6. 独自拡張クラスを作成する／独自拡張用のExtensionクラスを作成する: v6 の tip 2件を削除してよいか。特に `AbstractHttpRequestTestTemplate` を直接継承した独自拡張クラスに対し、どの Extension を継承すればよいかが「baseUriを渡す合成アノテーションを作成する」の例だけで読み取れるか。
7. 前提事項: `maven-surefire-plugin` 2.22.0 以上という条件が現在も妥当か（surefire 側の根拠を知っていれば確認してほしい）。

### JUnit 4での使用（`setup/junit4.rst`）

**由来**: 混在。依存関係は v6「自動テストフレームワーク」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/01_Abstract.html の「JUnit 5で自動テストフレームワークを動かす」）、共通処理と継承せずに使う方法は v6「Tips集」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.html の「テスト実行前後に共通処理を行いたい。」「本フレームワークのクラスを継承せずに使用したい」）から。機能概要とテストクラスの例は刷新で書き起こした。見出し 6 のうち内容変更 2・文面調整のみ 2・新設 2。

**利用者観点の課題と変更の考え方**
- 解説書を JUnit 5 標準にした結果、第3部の実装例はすべて合成アノテーション＋インジェクション方式になった。JUnit 4 の既存資産を持つプロジェクトが継承方式で書き続けられるよう、継承の最小例と第3部の例の読み替え規則（合成アノテーション＋フィールド宣言 → サポートクラスの継承、`support.` 経由 → 直接呼び出し）を置いた。JUnit 4 固有の話（`@BeforeClass` の同名メソッド、単一継承の制約で継承できない場合の委譲）も、コンポーネント単体テストのページからここへ集めた。
- v6 は「JUnit 5 で動かすには `junit-jupiter` と `junit-vintage-engine` を足す」だったが、ブランクプロジェクトは既に JUnit 5 構成であり、そのまま JUnit 4 のテストを置くと1件も実行されないままビルドが成功する。「JUnit 4 本体は `nablarch-testing` が持つので不要。`junit-jupiter` を持つプロジェクトでは `junit-vintage-engine` を `test` で追加」に書き換え、無いときの症状を important にした（ブランクプロジェクトの複製で実測）。
- v6 の委譲の例 `assertSqlResultSetEquals("test", "id", actual)`（3引数）は実装に無くコンパイルできないため、4引数に直した。「前処理・後処理を明示的に呼び出す」は、トランザクションの開始・終了が自動では行われないため、と理由を具体化した。

**レビューポイント**
1. 依存関係: 「JUnit 4 本体の追加は不要（`nablarch-testing` が `junit:junit` 4.13.1 を `compile` で持つ）」でよいか。プロジェクト側で `junit` を exclude する運用や、`nablarch-testing` の推移的依存に頼らず明示する運用が無いか。important「`junit-vintage-engine` が無いと1件も実行されないままビルドが成功する」が経験と合うか。
2. テストクラスを作成する: 読み替え規則だけで、第3部の JUnit 5 の例を JUnit 4 に読み替えられるか。読み替えが効かない例（`baseUri` の指定など）が第3部に無いか。
3. テスティングフレームワークのクラスを継承せずに使用する: `dbSupport.assertSqlResultSetEquals("従業員検索", "test", "expected", actual)` の4引数が `DbAccessTestSupport` と合っているか。`@Before`/`@After` から `beginTransactions()`/`endTransactions()` を呼ぶ説明で、委譲時に必要な呼び出しが漏れていないか。
4. 機能概要: JUnit 4 を「既存資産があるプロジェクト向け」に位置づけ、新規は JUnit 5 へ誘導する書き方で、JUnit 4 で書き続けたい読者が迷わないか。

### テストデータの設定（`setup/testdata.rst`）

**由来**: 混在。v6 の5ページに散らばっていた、テストの種類によらず効くテストデータの設定を1ページに集めた。集めた元は、Tips「テストデータ読み込みディレクトリを変更したい」「メッセージング処理でテストデータに対し定型的な変換処理を追加したい」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.html ）、データベースアクセステスト「デフォルト値の変更方法」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/02_DbAccessTest.html ）、リクエスト単体テスト（Nablarchバッチ）「ディレクティブのデフォルト値」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_batch.html ）、同ページ第3部側の tip「符号無数値・符号付数値」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/batch.html ）、メッセージング（RequestUnitTest_real／RequestUnitTest_send_sync）の「TestDataConvertor」。見出し 9 のうち内容変更 5・文面調整のみ 2（本文を持たない L2「使用方法」「拡張例」）・新設 2（機能概要、YAML）。

**利用者観点の課題と変更の考え方**
- v6 には YAML 形式を使い始めるための設定がどこにも無く、記法を読めても動かせなかった。依存関係の追加、`testDataParser` の `YamlTestDataParser` への差し替え、Interpreter の選び方を1節にまとめた。Interpreter はデフォルト設定 `nablarch/test/test-data.xml` の5つのうち、null・ダブルクォート・改行を Excel のセル値から読み取る3つを外し、日時と文字種の2つだけを指定する形にした。
- 読み込み先の設定は、v6 が「コンポーネント設定ファイル」に書くとしデフォルトを `test/java` としていたが、実際は properties 形式（環境設定ファイル）で、デフォルト設定を読み込むと `src/test/java` になる。読者が書く先とデフォルトの認識を実物に合わせた。
- ディレクティブ・テスト用データ型・変換処理は v6 ではバッチや MOM のページにあり、ウェブや HTTP メッセージングの読者は辿り着けなかった。実装がテストの種類によらず同じ設定を読むため、横断の設定としてこのページに置いた。
- v6 の記述例には固定長のディレクティブを `variableLengthDirectives` に書く誤りがあり、そのままでは固定長のデフォルトが効かない。実装のキー名 `fixedLengthDirectives` に直し、共通→種別→個々のブロックの適用順序と、共通には両種別で有効なキーだけを書く制約を足した。

**レビューポイント**
1. テストデータの形式をYAMLに変更する: `interpreters` に `dateTimeInterpreter`・`compositeInterpreter` の2つだけを指定し、`nullInterpreter`・`quotationTrimmer`・`lineSeparatorInterpreter` を外す判断が正しいか。実装 `YamlTestDataParser` と、YAML 形式のテストデータで `${systemTime}`・`${文字種,文字数}` が実際に変換されることを確かめてほしい。
2. テストデータの読み込み先を変更する: 環境設定ファイル（properties）に `nablarch.test.resource-root` を書く案内と、デフォルト `src/test/java` が、ブランクプロジェクトの構成と合っているか。VM 引数 `-D` での一時上書きの案内を落としたことでよいか。
3. 省略したテーブルのカラムのデフォルト値を変更する: 適用範囲を「準備データと `EXPECTED_COMPLETE_TABLE`」に限定した点、`charValue` が固定長文字列型でカラム長分繰り返される・`numberValue` がカラム長で切り出される、という v6 に無い説明が実装 `BasicDefaultValues` と合っているか。記述例に v6 に無い `dbInfo` プロパティを足しているが、この形でよいか。
4. ディレクティブのデフォルト値を設定する: v6 記述例の是正2件（固定長の map 名を `fixedLengthDirectives` に、可変長の `quoting-delimiter` を空文字から `&quot;` に）が実装と合っているか。適用順序と「共通には両種別で有効なキーだけ」の制約が、実装 `DataFile`・`FixedLengthFile` の読み方と合っているか。
5. 符号無数値・符号付数値のテスト用のデータ型を登録する: 対応表を v6 の15件から `replacement` を含む16件にした。6u3 の `FixedLengthConvertorFactory` のデフォルト対応表と一致しているか。「型記号の前に `TEST_` を付ける」規則の説明で読者が他の型にも応用できるか。
6. テストデータの変換処理を実装する: 適用対象を v6 の「Excel に記述されたデータ」から形式非依存の「電文のテストデータ」に広げた。YAML 形式でも `TestDataConverter_<file-type>` が効くか。tip「`file-type` の値は応答電文のアサート方式にも影響する」が実装 `MessagePool` の挙動と合っているか。

### システム日時と採番の固定（`setup/fixed_time_and_id.rst`）

**由来**: 混在。v6 の Tips ページに並んでいた2つの節「システム日時を任意の値に固定したい」「シーケンスオブジェクトを使った採番のテストをしたい」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.html ）を、テストの種類によらず効く横断の設定として1ページにまとめた。見出し 4 のうち内容変更 2・文面調整のみ 1（本文を持たない L2「使用方法」）・新設 1（機能概要）。

**利用者観点の課題と変更の考え方**
- v6 は`fixedDate`の桁数を「yyyyMMddHHmmss (12桁)」「yyyyMMddHHmmssSSS (15桁)」と書いていたが、実装が受け付けるのは 14桁と 17桁だけで、v6 のとおり12桁で書くと例外になる。読者が最初に書く1行なので実装の挙動に合わせた。
- v6 は本番側のシーケンス採番クラスを`nablarch.common.idgenerator.OracleSequenceIdGenerator`と書いていたが、このクラスは Nablarch に存在しない（javadoc も404）。読者が自分のプロジェクトのクラスだと分かるよう`com.example`配下の FQCN に改めた。
- v6 の tip は「テーブル採番用の設定値の詳細は`IdGenerator`を参照」としていたが、`IdGenerator`の javadoc には`tableName`等の説明が無く、読者は設定値の意味に辿り着けない。説明がある`FastTableIdGenerator`に参照先を変えた。
- v6 はシステム日時を取り出す Java コード例と property の表を持っていたが、第2部は設定を書くページで、テストコードの実装例は置かない。事実を落とさずに地の文へ移し、Excel の記述例は第3部への参照にした。

**レビューポイント**
1. システム日時を固定する: `fixedDate`を「14桁／17桁」と書いた。実装の挙動とは合っているが、`FixedSystemTimeProvider`の javadoc は現在も「12桁／15桁」と書いており、解説書と javadoc が食い違う状態になる。解説書側を実挙動に合わせたままでよいか（javadoc の是正を別に起こすか）を判断してほしい。
2. システム日時を固定する: v6 にあった`SystemRepository`から`SystemTimeProvider`を取得する Java コード例を落とし、「テスト対象のアプリケーションが`SystemTimeProvider`を通じて取得するシステム日時は、指定した日時に固定される」の1文に置き換えた。読者がこの1文で足りるか。
3. シーケンス採番をテーブル採番に置き換える: 本番側の設定例のクラス名を`com.example.common.idgenerator.OracleSequenceIdGenerator`にした。ブランクプロジェクトやプロジェクト標準の命名と合っているか。
4. シーケンス採番をテーブル採番に置き換える: 参照先を`FastTableIdGenerator`にした。記述例の4プロパティ（`tableName`・`idColumnName`・`noColumnName`・`dbTransactionManager`）の意味を、読者がその javadoc から引けるか。
5. 機能概要: この2つの設定を「どちらもテストの種類によらず使える」と位置づけた。ウェブ・バッチ・メッセージングのどの単体テストでも同じ設定で効くという理解でよいか。

### クラス単体テストの設定（`setup/class_unit_test.rst`）

**由来**: 混在。v6 の3ページに分かれていた設定を1ページに集めた。エンティティ単体テスト「自動テストフレームワーク設定値」の Bean Validation 版（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.html ）と Nablarch Validation 版（同 .../02_entityUnitTestWithNablarchValidation.html ）、および Tips「デフォルト以外のトランザクションを使用したい」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.html ）。見出し 4 のうち内容変更 2・文面調整のみ 1（本文を持たない L2「使用方法」）・新設 1（機能概要）。

**利用者観点の課題と変更の考え方**
- v6 は同じ`EntityTestConfiguration`の設定項目表を Bean Validation 版と Nablarch Validation 版の2ページに分けて持ち、項目数も説明も揃っていなかった（Nablarch Validation 版は`minMessageId`と`validationTestStrategy`を欠き、`underLimitMessageId`の説明も両者で違う）。読者はどちらのページを見たかで理解が変わる。実装の分岐で各IDの意味を確定し、8項目の表1つに統合した。
- v6 は各メッセージIDがどの条件で使われるかを、設定の節ではなくテストデータのカラム説明の脚注（max欄・min欄の組み合わせの表）に置いていた。設定を書く読者が設定の節だけで使い分けを読めるよう、条件を各項目の説明そのものに書き入れた。
- v6 の Nablarch Validation 版は「（全項目必須）」と書いていたが、実装に一律の必須検査は無く、未設定で確実に破綻するのは`characterGenerator`だけである。`minMessageId`が必須になるのも、Bean Validation で最大文字列長を省略し、かつ最小文字列長が2以上で、かつテストデータ側でメッセージIDを指定していないときに限られる。「全項目必須」を落とし、その条件を important に切り出した。
- v6 は「プロパティファイルにトランザクション名を記載しておけば」としか書かず、キー名も値の形も示していないため、読者はこの設定を書けなかった。実装のキー名`dbAccessTest.dbTransactionName`、値がコンポーネント名であること、カンマ区切り、未登録なら例外、デフォルトのトランザクションは記述の有無によらず開始されること、を足した。

**レビューポイント**
1. エンティティ単体テストの設定項目を登録する: 5つの文字列長系メッセージIDの使い分け（最大だけ→`maxMessageId`、最大＝最小→`fixLengthMessageId`が超過・不足の両方、最大＞最小→超過は`maxAndMinMessageId`・不足は`underLimitMessageId`、最大を省略→`minMessageId`）が`EntityTestConfiguration`の分岐と合っているか。特に`fixLengthMessageId`を「超過・不足のいずれの場合も使われる」と書いた点。
2. 同: important の条件（Bean Validation で最大文字列長を省略し、最小文字列長に2以上を指定し、テストデータの`messageIdWhenInvalidLength`を指定していないときに`minMessageId`が必須）が、読者がテストデータを書くときの判断として辿れるか。
3. 同: v6 の「（全項目必須）」を落とし、`characterGenerator`を「指定を省略するとテストの実行時に例外が発生する」に置き換えた。実際に発生する例外がこの表現で読者に伝わるか（例外の型とメッセージを確かめてほしい）。
4. 同: Bean Validation の記述例で、メッセージIDを`{`・`}`で囲む理由を「テスティングフレームワークが`MessageInterpolator`で変換して期待するメッセージを組み立てるため」と説明した。この説明で読者が自分のアノテーションのメッセージIDを書けるか。
5. デフォルト以外のトランザクションを使用する: `dbAccessTest.dbTransactionName`を環境設定ファイル（properties）に書く案内と、値に`SimpleDbTransactionManager`のコンポーネント名を並べる形が、ブランクプロジェクトの構成・プロジェクトの実運用と合っているか。

### リクエスト単体テストの設定（ウェブアプリケーション）（`setup/request_unit_test/web.rst`）

**由来**: 既存。v6 のリクエスト単体テスト（ウェブ）のページ（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/02_RequestUnitTest.html ）から、「各種設定値」「その他の設定」、および構造の説明のうち`AbstractHttpRequestTestTemplate`・`TestCaseInfo`の項を取った。見出し 7 のうち内容変更 2・文面調整のみ 3（本文を持たない L2「使用方法」「拡張例」と L3「テストデータの書き方を拡張する」）・新設 2（機能概要、必要なモジュールとコンポーネント設定を追加する）。

**利用者観点の課題と変更の考え方**
- v6 の`dumpVariableItem`の説明は実装と逆だった。v6 は「可変項目を出力するか否か」「毎回同じ結果にしたい場合は OFF(false)」と書いているが、実装は`true`のときに JSESSIONID と二重サブミット防止用トークンを空文字に置換して除去する。読者が書く値が反対になるため説明を反転し、プロパティ名から受ける印象と逆である旨の注意を添えた。
- v6 の「デフォルト値」欄は実装のフィールド初期値で書かれており、デフォルト設定`nablarch/test/http-request-test.xml`を読み込んだ実際の値とは違っていた（`webBaseDir`が`../main/web`、`jsTestResourceDir`が`../test/web`、拡張子リストが3件、`tempDirectory`が「jettyのデフォルト動作に依存」など）。読者は通常デフォルト設定を読み込むので、欄を読み込み後の実効値に統一し、その前提を導入文に書いた。上書きが要るかどうかの判断が変わる項目である。
- v6 の説明が実装と食い違う項目が他にもあった。`jsTestResourceDir`は「コピー先ディレクトリ名」だが実装ではコピー元、`htmlResourcesCharset`は「CSSファイルの文字コード」だが実装では`css`・`js`・`template`が対象、`htmlCheckerConfig`は「`htmlChecker`を設定しなかった場合のみ有効」だが実装では設定すると`htmlChecker`側に`Html4HtmlChecker`が入る。いずれも実装に合わせた。
- v6 は「実行速度を上げる」枠組みの下に JVM オプション（`-Xms256m -Xmx256m`、`-Xverify:none`）と Eclipse の手順・画像を置いていたが、これはテスティングフレームワークが読む設定ではなく、`-Xverify:none`は JDK 13 で非推奨になっている。枠組みごと落とし、HTMLリソースのコピー抑止だけを独立した節にした。

**レビューポイント**
1. コンポーネント設定ファイルに設定項目を登録する: `dumpVariableItem`の説明を v6 と逆向きにした（「除去するかどうか。同じ内容にしたい場合は`true`」）。実装の挙動と合っているか、また「プロパティ名から受ける印象とは逆」という注意の書き方でよいか。
2. 同: デフォルト値の欄をデフォルト設定読み込み後の実効値に統一した。表の値が現行のデフォルト設定と合っているか。特に`htmlChecker`の欄を「`htmlCheckerConfig`の設定に伴って設定される`Html4HtmlChecker`」と書いた点。
3. 同: important（`checkHtml`を`true`のままにするなら`htmlChecker`か`htmlCheckerConfig`のどちらかが必要で、どちらも無いとステータスコード500未満のHTMLレスポンスのチェック時に例外）を追加した。デフォルト設定を読み込まない読者への注意として、この位置と粒度でよいか。
4. 同: 表に載せる項目の取捨。`htmlResourcesRoot`はデフォルト設定が値を与えており、「HTMLリソースのコピーを抑止する」の tip でそのデフォルト値に触れているが、表には無い。表に載せなくてよいか。
5. HTMLリソースのコピーを抑止する: v6 の JVM オプションの小節（`-Xms`／`-Xmx`、`-Xverify:none`、Eclipse の実行構成と JRE 編集の手順、画像3枚）と、その親にあった「実行速度を上げる」という枠組みを丸ごと落とした。落としてよいか。
6. 必要なモジュールとコンポーネント設定を追加する（新設）: `nablarch-testing-jetty12` の依存関係、`nablarch/test/http-request-test.xml` の import、`httpServerFactory` の登録を、RESTful ウェブサービスのページと同じ形で足した。important「デフォルト設定は `httpServerFactory` を登録しない」が `nablarch-testing-default-configuration` の実物と合っているか。ウェブプロジェクトのアーキタイプに既にある旨の tip が現行のアーキタイプと合っているか。

### リクエスト単体テストの設定（RESTfulウェブサービス）（`setup/request_unit_test/rest.rst`）

**由来**: 既存。v6 のリクエスト単体テスト（RESTfulウェブサービス）のページ（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_rest.html ）の「モジュール一覧」「設定」「各種設定値」から取った。見出し 4 のうち内容変更 2・文面調整のみ 1（本文を持たない L2「使用方法」）・新設 1（機能概要）。

**利用者観点の課題と変更の考え方**
- v6 は依存関係3件と`<import>`1行しか書いておらず、内蔵サーバを生成する`httpServerFactory`の登録に触れていなかった。`nablarch-testing-jetty12`が提供するのはクラスだけでコンポーネントの登録は行わないため、アーキタイプ以外から作った読者はこのページのとおりに書いても内蔵サーバの生成で例外に当たる。登録の記述と、なぜ必要かの important を足した。
- v6 は「アーキタイプからブランクプロジェクトを作成した場合、`src/test/resources/unit-test.xml`にテスティングフレームワークの設定がされている」と具体パスを書いていたが、実装が読むのはクラスパス直下の`unit-test.xml`で、プロジェクト構成に依らない。読者が自分の構成と照合して迷わないよう、パスの記述を落とした。
- v6 の tip は「Nablarch5u18以降のアーキタイプから」という条件付きで、対象も設定ファイルの読み込みだけ、他のプロジェクトについては「追加が必要となる」としか書いていなかった。現行のアーキタイプでは無条件に成り立つため条件を落とし、tip の対象を依存関係3件にも広げて「不足している記述を追加する」に改めた。
- v6 は`webFrontControllerKey`を指定する条件を「ひとつのWarで実行する場合など」と構成の話で説明し、脚注にハンドラキュー定義の XML を2件丸ごと載せていた。実装が見ているのはコンポーネント名だけなので、条件を「`webFrontController`以外のコンポーネント名で登録している場合」に一般化し、併用構成は例示に落とした。XML 2件は同じ内容が FW解説書側にあるため、そちらへの参照に置き換えた。

**レビューポイント**
1. 必要なモジュールとコンポーネント設定を追加する: `httpServerFactory`の登録と important を v6 に無い形で足した。`SimpleRestTestSupport`の挙動、および`nablarch-testing-jetty12`が提供するものの実態（内蔵サーバとリクエスト単体データ作成ツールのクラスだけ）と合っているか。
2. 同: v6 の「ブランクプロジェクトでは`src/test/resources/unit-test.xml`に設定されている」を落とした。設定を書く先が分からなくなる読者がいないか。
3. 同: `RestTestSupport`を使うテストでデータベースを扱う場合に`testDataParser`も登録する、という1文を足し、記述例はテストデータの設定ページへの参照にした。この案内の位置と粒度でよいか。
4. コンポーネント設定ファイルで設定値を変更する: `webFrontControllerKey`を指定する条件を「`webFrontController`以外のコンポーネント名で登録している場合」に一般化し、v6 が脚注に載せていたハンドラキュー定義の XML 2件を FW解説書「委譲するWebフロントコントローラの名前を変更する」への参照に置き換えた。読者がこのページだけで指定の要否を判断できるか。
5. 同: `webBaseDir`に複数のディレクトリを指定したときの「指定された順にディレクトリを探索し、最初に見つかったリソースを使用する」が、内蔵サーバ（Jetty 12）の実挙動と合っているか。
6. 機能概要: 「専用のモジュールと内蔵サーバの設定を追加しないと実行できない」で、読者が「使用方法」の最初の節へ進めるか。

### リクエスト単体テストの設定（HTTPメッセージング）（`setup/request_unit_test/http_messaging.rst`）

**由来**: 混在。v6「リクエスト単体テストの実施方法(HTTP同期応答メッセージ送信処理)」の節「フレームワークで使用するクラスの設定」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/http_send_sync.html ）と、「リクエスト単体テストの実施方法（HTTP同期応答メッセージ受信処理）」の節「テストデータの書き方」の important（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/http_real.html ）。見出し 4 のうち 内容変更 3・文面調整のみ 0・新設 1。

**利用者観点の課題と変更の考え方**
- v6 の記述例はコンポーネント名が `defaultMessageSenderClient` という固定名で、自分のプロジェクトで何という名前にすべきかが分からない。名前は環境設定ファイルの `messageSender.<リクエストID>.messageSenderClient` に書いた値で決まり、その名前で参照されないコンポーネントはモックアップとして使われない、と書いた。
- v6 の `charset` の説明は「ログに出力する文字コード」で、どのログのことか読み取れない。メッセージングログに出力する電文の文字コード名だと特定し、メッセージングログのページへリンクした。
- v6 は「フレームワーク制御ヘッダの項目をPJで変更している場合」としか書いておらず、指定した名前がデフォルトを置き換えることも、空白がトリムされないことも読み取れない。名前を変えていないフィールドも含めて全列挙が要ること、カンマの前後に空白を入れないことを足した。
- v6 は同じ important を HTTP 受信のページと MOM 受信のページに二重に持っていた。設定を読む経路は1つなので本ページに本文を集約し、MOM のページからは参照だけにした。

**レビューポイント**
1. モックアップクラスを登録する: コンポーネント名の決まり方（`messageSender.<リクエストID>.messageSenderClient`。この項目にリクエストIDごとの設定しかなく `DEFAULT` へのフォールバックが無いこと）が実装 `MessageSenderSettings` と合っているか。記述例のコンポーネント名 `defaultMessageSenderClient` と本文の説明を並べて読んで、読者が名前を決められるか。
2. フレームワーク制御ヘッダのフィールド名を指定する（important）: 「この設定は Excel 形式・YAML 形式のどちらでも使用される。YAML 形式では `fw_header:` に記載できるキーがこの設定の名前（省略時は `requestId`・`userId`・`resendFlag`・`resultCode`）に限られ、それ以外はエラー」が、実装 `YamlMessageBuilder` と合っているか。第3部「テストデータの書き方」の YAML 形式の節と同じことを言えているか。
3. フレームワーク制御ヘッダのフィールド名を指定する: 「メッセージ送信のテストでも、この設定は使用されない」が `SendSyncMessageParser` の実態と合っているか。また受信テストに限る条件付けが、ウェブ・Nablarchバッチから HTTP メッセージ送信を行う場合の読者に誤解を与えないか。
4. 使用方法: v6 にあった「通常、これらの設定はアーキテクトが行うものでありアプリケーションプログラマが設定する必要はない」を落とし、L2 直下は見出しだけになっている。第2部全体がアーキテクト向けである前提で、ページ単位のこの断りが無くてよいか。

### リクエスト単体テストの設定（Nablarchバッチアプリケーション）（`setup/request_unit_test/batch.rst`）

**由来**: 混在。v6「リクエスト単体テスト（バッチ処理）」の節「各種設定値」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_batch.html ）。見出し 4 のうち 内容変更 2・文面調整のみ 1・新設 1。

**利用者観点の課題と変更の考え方**
- v6 は「常駐バッチのテストを実施する際には」と適用条件をアプリケーションの種類で書いているが、置き換えが要るかどうかはリクエストスレッド内ループ制御ハンドラを構成に含むかで決まる。テーブルをキューとして使ったメッセージングのように常駐バッチでない構成でも該当するため、条件をハンドラの有無に改めた。
- v6 は「変更が必要なハンドラ」の表で変更対象・変更後・理由を示していたが、対象が1件しかない表で、なぜ終わらないのかを読むのに表のセルを横に読む必要があった。表をやめ、終わらない理由と置き換え後の挙動を地の文にした。
- v6 は同名で上書きする方法だけを書いており、本番用の設定に書いたプロパティの値がそのまま効くと読めてしまう。上書き前後でクラスが異なるため値は引き継がれないことを tip に足した。
- v6 は応答不要メッセージ送信のプロバイダ差し替えを書いていない。差し替えないと要求電文が実際のキューへ送られ、テストショット一覧の `expectedMessage` との照合が送信件数の不一致で落ちる。設定が無いとテストが成立しないため、節を新設した。

**レビューポイント**
1. リクエストスレッド内ループ制御ハンドラを置き換える: 「このハンドラはテーブルをキューとして使ったメッセージングのハンドラ構成に含まれる」と1つだけ挙げているが、FW解説書のハンドラ構成では MOM によるメッセージングにも同じハンドラが入っている。DBキューだけを挙げてよいか、MOM も挙げるべきか。
2. 応答不要メッセージ送信用のメッセージングプロバイダに差し替える（新設）: コンポーネント名の説明を「本番用のコンポーネント設定ファイルでメッセージングプロバイダに付けた名前」としている。同じ `RequestTestingMessagingProvider` の登録を、MOM のページでは「`messageSender.<リクエストID>.messagingProviderName` に指定した名前」と説明している。応答不要送信はハンドラのプロパティ経由、同期応答送信は `messageSender` 設定経由という違いによる書き分けだが、読者に不揃いと映らないか。
3. 応答不要メッセージ送信用のメッセージングプロバイダに差し替える: この節を Nablarchバッチアプリケーションのページに置いたのが妥当か。ウェブや RESTful ウェブサービスのリクエスト単体テストで応答不要送信を行う場合の読者が、このページに辿り着くか。
4. リクエストスレッド内ループ制御ハンドラを置き換える: 「上書きの記述は、本番用のコンポーネント設定ファイルの読み込みより後に置く」が、ブランクプロジェクトのテスト用コンポーネント設定ファイルの構成と合っているか。
5. ページ全体: v6 がこのページに持っていた「ディレクティブのデフォルト値」と符号無数値・符号付数値のテスト用データ型（`TEST_X9`・`TEST_SX9`）の登録は、「テストデータの設定」ページへ移した。本ページからの導線は置いていない。目次で先に出るページに移したことで足りるか。

### リクエスト単体テストの設定（MOMによるメッセージング）（`setup/request_unit_test/mom.rst`）

**由来**: 混在。v6 に対応するのは「リクエスト単体テストの実施方法(同期応答メッセージ受信処理)」の節「テストデータの書き方」の important 1件だけである（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/real.html ）。見出し 5 のうち 内容変更 1・文面調整のみ 1・新設 3。

**利用者観点の課題と変更の考え方**
- v6 は MOM のリクエスト単体テストに必要なメッセージングプロバイダの設定を1行も書いていない。受信のテストはコンポーネント名 `messagingProvider` で `EmbeddedMessagingProvider` を登録しないと実行時に例外で落ち、キュー名も `TEST.REQUEST`・`TEST.RESPONSE` に固定されている。設定が無いとテストが動かないため、節を新設した。
- 同期応答メッセージ送信のプロバイダ差し替えも v6 に無い。差し替えないと要求電文が実際のキューへ送られ、テストショット一覧の `expectedMessage` に書いた期待値との照合が成立しない。これも節を新設した。
- v6 は外部の MOM を用意する必要があるのかどうかを書いていない。受信のテストで使うキューはテストの実行中だけ JVM 内で動く内蔵サーバであり、外部の MOM は不要である旨を機能概要と使用方法に明記した。
- フレームワーク制御ヘッダのフィールド名の設定は、v6 が HTTP のページと本ページに同文の important を二重に持っていた。設定内容は同じなので HTTP のページに本文を集約し、本ページは同名の見出しを残して参照だけを置いた。

**レビューポイント**
1. メッセージ受信用のメッセージングプロバイダを登録する（新設）: 「コンポーネント名は `messagingProvider` 固定」「キュー名は `TEST.REQUEST`・`TEST.RESPONSE` で固定されており変更できない」が実装 `MessagingRequestTestSupport`・`EmbeddedMessagingProvider` と合っているか。
2. 受信の節と送信の節の関係: 受信はコンポーネント名 `messagingProvider` 固定、送信は `messageSender.<リクエストID>.messagingProviderName` に指定した名前、と別々の規則を書いている。送信側に別名を使っているプロジェクトで、この2つのプロバイダをどう共存させるか（別の設定ファイルに分けるのか）を本文は示していない。読者が迷わないか。
3. 同期応答メッセージ送信用のメッセージングプロバイダに差し替える: 記述例のコンポーネント名を `messagingProvider` としているが、本文は「`messagingProviderName` に指定した名前」と説明している。FW解説書の記述例では `messageSender.DEFAULT.messagingProviderName=defaultMessagingProvider` のように別名を使っている。例と説明の組み合わせでよいか。
4. フレームワーク制御ヘッダのフィールド名を指定する: 本文を持たず HTTP メッセージングのページへのリンクだけを置く形にした。MOM だけを読む読者が「自分には関係ない」と読み飛ばさないか。見出しを同名にしたことで足りるか。
5. 機能概要: 「テストの実行中だけ JVM 内で動く内蔵のメッセージングサーバ」という説明が実態と合っているか（`EmbeddedMessagingProvider` は JVM 内でメッセージブローカを起動し、テストショットの終了時に停止する）。
6. ページ全体: リクエストスレッド内ループ制御ハンドラの置き換えは本ページに書いていない。FW解説書の MOM によるメッセージングのハンドラ構成にはこのハンドラが含まれるため、応答不要メッセージ受信の常駐型を読む読者に、Nablarchバッチアプリケーションのページへの導線が要らないかを判断してほしい。

### リクエスト単体テストの設定（テーブルをキューとして使ったメッセージング）（`setup/request_unit_test/db_queue.rst`）

**由来**: 新規。v6 の NTF 解説書に対応する記述は無い。本文は「リクエスト単体テストの設定（Nablarchバッチアプリケーション）」への導線 1 文だけで、L2 以下の見出しは 0（内容変更 0・文面調整のみ 0・新設 1＝ページ自体）。

**利用者観点の課題と変更の考え方**
- v6 はテーブルをキューとして使ったメッセージングのリクエスト単体テストの設定をどこにも書いておらず、章見出しからも辿れない。読者は「自分の方式のページが無い」状態で他方式のページを当たることになる。他の方式と並ぶ位置に章を立て、中身は設定が書いてあるページへの導線だけとした。
- 設定の実体は Nablarchバッチアプリケーションのページと同じであるため、本文を複製せず、リンク 1 文で済ませた。目次・機能概要・使用方法は置いていない。

**レビューポイント**
1. ページ全体（飛び先の妥当性）: 飛び先の「リクエスト単体テストの設定（Nablarchバッチアプリケーション）」は、(a) リクエストスレッド内ループ制御ハンドラの置き換えと、(b) 応答不要メッセージ送信用のメッセージングプロバイダの差し替えの 2 節を持つ。(a) はテーブルをキューとして使ったメッセージングのハンドラ構成に該当するが、(b) が該当するかは本文からは読み取れない（FW解説書のテーブルをキューとして使ったメッセージングの章には送信側の記述が無い）。「設定は…と同じである」でよいか、該当する設定を名指しすべきか。
2. ページ全体（形）: 導線 1 文だけで、目次ディレクティブも機能概要・使用方法の見出しも置いていない。設定章の他のページと形が揃っていないが、導線ページとしてこの形でよいか。

### 取引単体テストの設定（RESTfulウェブサービス）（`setup/deal_unit_test/rest.rst`）

**由来**: 既存。v6「取引単体テスト（RESTfulウェブサービス）」の節「Cookieなど前のレスポンスの情報を引き継ぐ方法」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/rest.html ）。見出し 6 のうち 内容変更 2・文面調整のみ 4・新設 0。

**利用者観点の課題と変更の考え方**
- v6 の XML 記述例2つは開始タグを `/>` で閉じたまま子要素を持つ構文不正で、写すとコンポーネント設定の読み込みで止まる。読者がそのまま写して動く形に直した。
- `RequestResponseCookieManager` は `cookieName` を指定しないとレスポンス処理時に例外になるが、v6 は必須と書いていない。important で必須と明記し、`NablarchSIDManager` は初期値 `NABLARCH_SID` を持つため指定不要と書き分けた。
- v6 は提供済み実装2クラスの説明を「実装クラスを作成する」の節に置いており、登録するだけで済む読者が拡張の話を読まされる。提供実装は「使用方法」、独自実装の手順だけを「拡張例」に分けた。
- 複数の実装を `ComplexRequestResponseProcessor` に列挙したときの実行順が v6 に無く、順序に依存する組み合わせを安全に組めない。記述順に実行されると追記した。

**レビューポイント**
1. 前のレスポンスの値を次のリクエストに引き継ぐ: `cookieName` 必須の important（未指定なら「レスポンスの処理時に例外」）が実装 `RequestResponseCookieManager#processResponse` と合っているか。`NablarchSIDManager` を「`cookieName` を指定しなくてよい」と案内してよいか。
2. 同節・複数の値をまとめて引き継ぐ: 是正した XML 記述例2つが、テスト用のコンポーネント設定ファイルにそのまま置いて読み込める形になっているか。
3. 複数の値をまとめて引き継ぐ: 「リクエストの操作・レスポンスの操作のいずれも記述順に実行される」が実装 `ComplexRequestResponseProcessor` と合っているか。順序に依存する組み合わせを前提に書いてよいか。
4. リクエストとレスポンスの操作を実装する: `reset()` が「各テストメソッドの開始時」に呼ばれるという説明が実装 `SimpleRestTestSupport#setUp` と合っているか。`defaultProcessor` 未登録時に何もしない実装が使われることは書いていないが、書かなくてよいか。
5. 機能概要: 「引き継ぎをテストコードに毎回書かずに済むよう」という動機づけは v6 に無い言い回しである。実際の利用場面と合っているか。

### 取引単体テストの設定（HTTPメッセージング）（`setup/deal_unit_test/http_messaging.rst`）

**由来**: 混在。v6「取引単体テスト（HTTPメッセージング）」の節「フレームワークで使用するクラスの設定」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/http_send_sync.html ）と、v6「取引単体テスト（MOMによるメッセージング）」の節「Excelファイルの配置場所の設定」「テストデータ解析クラスの設定」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/send_sync.html ）。見出し 6 のうち 内容変更 3・文面調整のみ 1・新設 2。

**利用者観点の課題と変更の考え方**
- v6 の HTTP メッセージングのページはモックアップクラスの登録しか書いておらず、応答電文の読み込み設定（`sendSyncTestData`・`messagingTestDataParser`）は MOM のページにしか無い。HTTP の読者が自分のページどおりに設定すると実行時に例外で止まる。読み込み設定は HTTP と MOM で共通のため本ページに本文を置き（目次で先に出る）、MOM のページからはリンクした。デフォルト設定に含まれないこと、未設定なら例外になること、同じコンポーネントに `format` も要ることを明記した。
- v6 の記述例のコンポーネント名 `defaultMessageSenderClient` は、リクエスト単体テストの設定ページと同じ名前で別クラスを登録する例になっており、両方を行うプロジェクトでは書かれたとおりに動かない。`defaultRealTimeMessagingClient` に変え、名前の決まり方はリクエスト単体テストの設定ページへ導線を張った。
- `charset` は v6 で「ログに出力する文字コード」とだけあり、応答電文の解釈にも効くと読める。実装ではメッセージングログの出力にだけ使われるため、適用範囲を限定した。
- Interpreter を v6 はインライン定義で書いていたが、import 済みの `nablarch/test/test-data.xml` が同じものを定義している。定義ではなく `component-ref` で参照する形に揃え、YAML 形式では `compositeInterpreter` だけを指定する（null・空文字・ダブルクォートは YAML の構文が担う）。

**レビューポイント**
1. モックアップクラスを登録する: 記述例の名前を `defaultRealTimeMessagingClient` に変え、名前の決まり方（`messageSender.<リクエストID>.messageSenderClient`）はリクエスト単体テストの設定ページに委ねた。この分担でよいか。`charset` を「メッセージングログに出力する電文の文字コード」に限定したことが実装 `MockMessagingClient` と合っているか。
2. 同期応答メッセージ送信・HTTPメッセージ送信のテストデータの読み込みを設定する: 「デフォルト設定には含まれない」「設定していないと実行時に例外」「`format` も同じコンポーネントに設定する」が、実際のプロジェクトの `unit-test.xml` の書き方と合っているか。本文を HTTP 側に置き MOM 側をリンクにした置き方でよいか。
3. Excel形式の場合: Interpreter を `nullInterpreter`・`quotationTrimmer`・`compositeInterpreter` の `component-ref` で書く形は、`nablarch/test/test-data.xml` を import している前提である。この前提を本文で十分に示せているか。`fileExtensions` は `xlsx` または `xls` で一致しないファイルは読まれない、リクエストIDごとに1ファイル、の2点。
4. YAML形式の場合: `fileExtensions` に `sendSyncTestData` を設定すると例外になる important（実行して確認済み）、`testDataReader` を指定しない、`compositeInterpreter` だけでよい、の3点が `YamlTestDataParser` の使い方として妥当か。
5. 機能概要（新設）: 「通信先を用意せずに実施する」「電文を実際に送る代わりに」という言い切りで、HTTP メッセージングの取引単体テストの実態と合っているか。

### 取引単体テストの設定（MOMによるメッセージング）（`setup/deal_unit_test/mom.rst`）

**由来**: 混在。v6「取引単体テスト（MOMによるメッセージング）」の節「フレームワークで使用するクラスの設定」のうち「モックアップクラスの設定」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/send_sync.html ）。見出し 4 のうち 内容変更 2・文面調整のみ 1・新設 1。

**利用者観点の課題と変更の考え方**
- v6 の記述例は `messagingProvider` という固定名で、自分のプロジェクトで何という名前にすべきかが分からない。名前は環境設定ファイルの `messageSender.<リクエストID>.messagingProviderName`、無ければ `messageSender.DEFAULT.messagingProviderName` で決まり、本番用と同じ名前で登録すると置き換わる、と書いた。
- v6 は同じページに応答電文の読み込み設定（`sendSyncTestData`・`messagingTestDataParser`）を持っていたが、この設定は HTTP メッセージングと共通で、目次で先に出る HTTP メッセージングのページに本文を置いた。本ページには同じ見出しを残し、リンクだけを置いて確実にたどり着けるようにした。
- モックアップクラスを使うとキューへのアクセスは行われず、テストデータから応答電文が生成されて返ることを機能概要と使用方法に明記した。v6 は「モックアップクラスを設定する」としか書いていない。

**レビューポイント**
1. モックアップクラスを登録する: コンポーネント名の決まり方（リクエストIDごとの `messagingProviderName` → `DEFAULT` へのフォールバック）が実装 `MessageSenderSettings` と合っているか。「本番用と同じ名前で登録することで置き換わる」という案内で、実際のプロジェクト構成（テスト用の設定ファイルで上書き）に沿うか。
2. 同期応答メッセージ送信・HTTPメッセージ送信のテストデータの読み込みを設定する: 本文を持たず HTTP メッセージングのページへのリンクだけを置く形で、MOM の読者が「自分には関係ない」と読み飛ばさないか。見出しを同名にしたことで足りるか。
3. 機能概要（新設）: 「キューを用意せずに実施する」「キューへ接続する処理を置き換える」という説明が、`MockMessagingProvider`・`MockMessagingContext` の実態と合っているか。
4. モックアップクラスを登録する: 「キューへのアクセスは行われず」（本ページ）と「電文の送信は行われず」（HTTP メッセージングのページ）で言い分けている。差し替わる層が違うため意図的に揃えていないが、読者に不揃いと映らないか。

### マスタデータ復旧機能（`setup/master_data_restore.rst`）

**由来**: 既存。v6「マスタデータ復旧機能」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/04_MasterDataRestore.html ）。見出し 8 のうち 内容変更 6・文面調整のみ 2・新設 0。

**利用者観点の課題と変更の考え方**
- v6 の設定例には `testEventListeners` の記述が無く、写しても復旧が動かない。`testEventListeners` は `MasterDataRestorer` のプロパティではなくテストイベントの通知先一覧なので、設定項目の表から外して地の文と important に移し、記述例に `RepositoryInitializer` を含む一覧を足した。
- v6 は環境構築の4節を並列に置き、依存関係の解析の抑止まで必須に読める。必須3件（バックアップ用スキーマ・監視対象テーブル・SQLログ）と任意1件を分け、抑止は使用方法の末尾に移した。
- 抑止設定の副作用が v6 に無い。列挙順に挿入・逆順に削除するので親テーブルを先に列挙すること、この設定はマスタデータの復旧だけでなく準備データの投入やマスタデータ投入ツールの投入順にも効くことを important にした。
- v6 の「テーブルを復旧する際、いったん全件削除し、その後全件挿入」はテーブルごとの繰り返しとも読めるが、実装は変更があった全テーブルをまとめて削除してから挿入する。記述と図（1枚に統合）を実装に合わせた。バックアップ用スキーマの tip には、マスタデータ投入ツールでバックアップ用スキーマにも投入する場合は記述した全テーブルが必要という但し書きを足した。

**レビューポイント**
1. 監視対象テーブルを登録する: 記述例の `<list name="testEventListeners">`（`RepositoryInitializer` を含む）と important「登録を省略すると復旧は行われない」が、実装 `TestEventDispatcher`・`MasterDataRestorer` および実際のプロジェクトの `unit-test.xml` と合っているか。デフォルト値を「該当なし」としているが、デフォルト設定には `nablarch/test/master-data-restorer.xml`（`backupSchema` が `nablarch_test_master`、Nablarch のサンプル向けの監視テーブル一覧）が同梱されている。本文で触れなくてよいか。
2. テーブルの依存関係の解析を抑止する: important「列挙順に挿入・逆順に削除。外部キーがあるときは親を先に列挙する」は、実装 `TableDataSorter` の Javadoc「DBにFKが設定されていない場合にのみ使用すること」と食い違う。v6 の節「外部キーが設定されたテーブルを使用する場合について」に忠実に、外部キーがある場合も列挙順で運用できると案内してよいか。
3. 同節: 「この設定はテーブルの依存関係の解析すべてに適用され、準備データの投入・マスタデータ投入ツールの投入順にも効く」という適用範囲の追記が、`DbAccessTestSupport`・`MasterDataSetUpper` の実態と合っているか。
4. マスタデータを復旧する流れ: 「変更があったテーブルのレコードをすべて削除したうえで…すべて挿入」と図 `restore_flow.png` が `MasterDataRestorer` の復旧処理と合っているか。
5. バックアップ用スキーマを作成する: tip の但し書き（投入ツールでバックアップ用スキーマにも投入する場合は記述した全テーブルが必要）が `MasterDataSetUpper` と合っているか。記述例のスキーマ名を配布物の綴り `NABLARCH_TEST_MASTER`（大文字）にしたが、読者の環境の綴りと合うか。
6. SQLログを出力する: `NopLogWriter` を「何も出力しないログライター」（v6 は「何もしないロガー」）に改めた点と、important「`INFO` 以上を指定するとSQLログが出力されず検出できない」でよいか。

## 第3部 テストの実装

### テストデータの書き方（`implementation/testdata_notation.rst`）

**由来**: 混在。v6 では記法の説明が「テスティングフレームワークの概要」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/01_Abstract.html ）・「データベースアクセスのテスト」（…/06_TestFWGuide/02_DbAccessTest.html）・「Tips」（…/06_TestFWGuide/03_Tips.html）と、リクエスト単体テストの各処理方式のページ（…/05_UnitTestGuide/02_RequestUnitTest/index.html・batch.html・real.html・http_real.html・send_sync.html・http_send_sync.html）に分散していた。見出し 41 のうち 内容変更 19・文面調整のみ 9・新設 13（新設は主に YAML 形式の節と、テストデータの構造・0件のデータ・エンティティバリデーションのカラム）。

**利用者観点の課題と変更の考え方**
- v6 は同じ記法の説明が複数ページに分かれ、互いに食い違っていた（例: グループID `default` の脚注はバッチとメッセージングにあるが、Tips のグループID節はテーブルだけをサポート対象と書く）。1ページに集め、食い違いは実装で確かめて一本化した。
- v6 の記述どおりに書くと動かない箇所を実装に合わせた。Excel の `\n` は LF に変換されない（変換されるのは `\r` だけ）、可変長ファイルの `""` 行は空行ではなく全フィールドが空文字のレコードになる、電文の対応付けは `no` の値ではなく記述順、マーカーカラムが使えるのはカラム名の行を持つデータタイプだけ。
- テーブルを0件で書く方法（準備データを空にする・期待値で空を検証する）が v6 のどこにも無い。節を新設し、Excel はカラム名の行が必須（カラム名を持たない場合はマーカーカラムを1つ置く）、YAML は `rows: []` と書き分けた。
- Excel と YAML で結果が分かれる箇所を important で明示した。行内で値を書かなかったカラムは Excel＝空文字・YAML＝null、外側のダブルクォート1層の除去は Excel だけ、YAML は値を必ずダブルクォートで囲む（クォートなし `null` だけが Java の null）。省略カラムのデフォルト値表も実装に合わせ、日付型は JVM のタイムゾーンに依存する値（JST では `1970-01-01 09:00:00.0`）とした。

**レビューポイント**
1. グループIDによる使い分け: 「`"default"` をグループIDなしと同等に扱うのは Nablarch バッチ・メッセージングのテストで、ウェブアプリケーションのテストには適用されない」（実装 `TestShot`・`BatchRequestTestSupport`。ウェブ側に同じ処理は無い）。ウェブのテストで `default` と書いている現場が無いか。収集方式の表（データタイプは前方一致、ID は完全一致）。
2. 0件のデータを記述する／Excel形式の場合／YAML形式の場合: Excel でカラム名を持たない0件はマーカーカラムを1つ置く、という手順が実際に使えるか。YAML の `expected_tables` に `rows: []` を書いた場合の「レコードが1件もないことの検証」は本体が追随する前提で書いている。現在の `nablarch-testing-yaml` で動くか。
3. テーブルのデータを記述する／コメント・マーカーカラム・空エントリを扱う: important「行内で値を書かなかったカラムは Excel＝空文字・YAML＝null」と、空エントリの判定（Excel は全セル空、YAML は `{}` のみ。`""` は値。判定はマーカーカラム除外の前）を仕様として案内してよいか。
4. カラムを省略する: デフォルト値表（CHAR は半角スペース×カラム長、VARCHAR は `" "`、日付は epoch 起点で JVM タイムゾーン依存、バイナリは10バイトのゼロ、Boolean は `"false"`）が実装 `BasicDefaultValues` と合っているか。v6 の「検索結果の期待値は全カラム必須／登録系テストも省略不可」を「`LIST_MAP` は Map 完全一致の制約／登録系は推奨」に分けた判断でよいか。
5. null・空文字・改行など特殊な値を記述する（Excel形式・YAML形式）: 改行は `\r` だけが CR に変換され `\n` は2文字のまま（v6 の逆。デフォルト設定の `LineSeparatorInterpreter`）。YAML は全データ値をダブルクォート必須、`"\\r"` を含む値はエラー、外側クォート1層の除去は行われない。`${文字種,文字数}` の文字種を 14 種にした（中国語・サロゲートペア・改行を追加）。
6. ファイルのデータを記述する: `""` 行は空行にならず全フィールド `""` のレコードになる（v6 Tips「空行を表せる」を否定）、末尾の `null` は `""` になる、`TEST_{型記号}` は「元の型に代えて使用される」、ディレクティブ表（`record-separator` はシンボル以外ならその文字列自身、`field-separator` は `\t` 以外は1文字）。
7. メッセージングのデータを記述する（障害系・Excel形式・YAML形式を含む）: 電文の対応付けは記述順で `no` は使われない、レコードレイアウトは1つ、レコード種別は `MESSAGE` では `"default"` 固定・同期応答送信の4データタイプでは記載値、`errorMode:timeout` は MOM の取引単体テストのモックアップだけ例外を出さず `null` を返す、YAML の `fw_header:` に書けるキーは `reader.fwHeaderfields` の名前だけ。実装・利用経験と合っているか。
8. testShots本体を記述する／ウェブアプリケーションのカラム／メッセージングのカラム: 「必須」＝カラムを定義する必要があり値は空でもよい、`isValidToken`・`forwardUri` を必須に、`requestPath`・`userId` はカラムが無ければ `test` が使われる（v6 は必須）。実装 `TestCaseInfo`・`MessagingRequestTestSupport` と合っているか。

### テストデータの記載例（`implementation/testdata_examples.rst`）

**由来**: 混在。v6 に対応するページは無い。採番処理の例だけが v6「Tips集」の「Excelファイル記述例」（採番）から来ている（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.html ）。見出し 111 のうち 内容変更 0・文面調整のみ 2・新設 109。

**利用者観点の課題と変更の考え方**
- v6 では記述例が Tips集・DBアクセステスト・各テスト種別のページに散らばり、多くが Excel のスクリーンショットで、写して使えなかった。用途別（データブロック／グループID／testShots／LIST_MAP／テーブル／ファイル／メッセージング／特殊値／コメント）に1ページへ集め、すべての例を Excel（セル格子の表）と YAML（同じ内容のコードブロック）の対で示した。
- 例の由来: v6 本文から起こしたのは採番の例だけ。残りは記法の下書き資料から書き起こし、題材の一部（バッチのサンプル名 `DBtoDBBatchSample`・`BatchSample.xml`、電文のリクエストID `RM11AD0102`・`RM21AA0104` など）はテスティングフレームワーク本体のテストリソースに合わせた。下書きの例のうち実装と食い違っていたもの（複数レコードレイアウトのレコード長不一致、`sendSyncTestData` を識別子と誤っていた点、`EXPECTED_COMPLETE_TABLE` の補完条件、`quoting-delimiter` の YAML 例）は実装に合わせて直した。
- 例の確かめ方: YAML の例は全ブロックをスキーマで検証した（違反0）。JSON・XML の電文の例は Excel・YAML の両方を実際にパーサ（`YamlTestDataParser` 等）に通し、読み込み結果が一致することを確かめた。それ以外の Excel の例は読み込ませて確かめていないため、レビューで実物と突き合わせてほしい。
- 引かれる場面: 「テストデータの書き方」（記法の仕様）の各節・各形式から「実際の記述例は…」でここへ送る。エンティティ単体テスト・コンポーネント単体テストなど第3部の他 11 ページからも「記述例は…を参照」で送っており（41 箇所）、読者は自分のテストデータを書くときに該当する用途の節を開いて写す。

**レビューポイント**
1. テーブルのデータを記述する: `MEMBER`・`ORDER_HEADER` の例（`Null`、`${binaryFile:}`、`EXPECTED_COMPLETE_TABLE` で `UPDATE_DATE` をカラム名の行から外す形、`rows: []` の0件）が、実際に読み込めてテストが成立する形か。0件の期待値は YAML 実装で検証されない現状を注記せず仕様どおりに書いている。これでよいか。
2. ファイルのデータを記述する: 複数レコードレイアウトでヘッダに `FILLER`（34）を足して40バイトに揃えた例、タブ区切り（Excel は `\t` 2文字、YAML は `"\\t"`）、`quoting-delimiter`（YAML では値の囲みを外す）、「全フィールドが空文字のレコード」（書き出しは `,,` になり空行にならない）が、実際の読み込み・書き出しの挙動と合うか。
3. メッセージングのデータを記述する: 識別子 `setUpMessages`／`expectedMessages`、`sendSyncTestData` 配下の `REQ001.xls` の `message` シート（YAML は `REQ001/message.yaml`）への配置、応答不要送信の `messageRequestId` と `EXPECTED_REQUEST_HEADER_MESSAGES[case1]=RM11AC0301`、JSON・XML のフィールド長 `-` が、実際のリクエスト単体テストで動く形か。
4. null・空文字・改行など特殊な値を記述する: `${systemTime}`・`${updateTime}`・`${setUpTime}` の使い分け、YAML の `null`（クォートなし＝Java の null、`"null"`＝文字列）、`${半角数字,3}-${半角数字,4}` のような部分増幅、`${attach:}` のパスの基準（カレントディレクトリ）が、利用経験・実装と合うか。
5. テストショット一覧（testShots）を記述する: 処理方式ごとの例（ウェブの `context` 参照、バッチの `setUpFile` のグループID、メッセージングの `expectedMessage`／`responseMessage`、エンティティバリデーションの `title`・`expectedMessageId1`・`propertyName1`）が、各テスト種別ページが求めるカラムと合うか。エンティティバリデーションの例に足した入力パラメータ `params`（`userName` を空欄にして必須エラーを起こす 1 行）が、`EntityTestSupport` が読む形（`testShots` と同じ行数・順序）として正しいか。

### エンティティ単体テスト（`implementation/class_unit_test/entity.rst`）

**由来**: 既存。v6 の2ページ「Bean Validationに対応したForm/Entityのクラス単体テスト」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_entityUnitTestWithBeanValidation.html ）と「Nablarch Validationに対応したForm/Entityのクラス単体テスト」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/02_entityUnitTestWithNablarchValidation.html ）を1ページに統合した。見出し 13 のうち 内容変更 7・文面調整のみ 4・新設 2。

**利用者観点の課題と変更の考え方**
- v6 はバリデーション方式ごとに2ページに分かれ、同じ説明が二重にあり、自分のクラスでどのメソッドを呼べるかを2ページ突き合わせて読む必要があった。1ページに統合し、「確認する対象 × 使用するメソッド × 対象となる方式」の表と、カラム表の「使用できる方式」列で方式差だけを示した。方式と合わないメソッドを呼んだときの挙動（`UnsupportedOperationException`、コンストラクタのテストはデフォルトコンストラクタにフォールバック）を機能概要に足した。
- v6 はテストデータのカラムを Excel のスクリーンショット14枚で示していて、検索もコピーもできず、必須カラムや空欄セルの扱いが読み取れなかった。画像をすべてカラム表に書き起こし、実装から「値が空欄でもカラム自体を用意する5カラム」「`set`／`get` が空欄の行の扱い」「文字列長不足のテストは `min` が1以下なら実行されない」「指定できる文字種は14種」を足した。
- v6 のテストクラス・テストデータ・テスト対象クラスのダウンロードリンク6本は落とした（撤去する旧ページ配下にあるため）。読者はサンプルを入手できなくなるので、記載例ページへの導線で代替した。
- テストが失敗したときに何が出力されるかが v6 に無かった。「テスト結果を確認する」を新設し、確認する対象ごとの出力情報と、その他の単項目バリデーションでは `case` が出力されない旨を書いた。

**レビューポイント**
1. 機能概要: 「設定した方式に対応しない `testBeanValidation`／`testValidateAndConvert` は `UnsupportedOperationException`、`testConstructorAndGetter` は `Map` コンストラクタが無ければデフォルトコンストラクタを使う」が `EntityTestSupport` と合っているか。
2. 文字種と文字列長をテストする: 必須5カラム（`propertyName`・`allowEmpty`・`min`・`max`・`messageIdWhenNotApplicable`）、文字種14種、「`min` が1以下なら文字列長不足のテストは実行されない」（v6 は「`min` 欄を省略した場合」）が `CharsetTestVariation`・`BasicJapaneseCharacterGenerator` と合っているか。`min` に `1` を書いた利用者が不足テストが走らないことに気づけるか。
3. その他の単項目バリデーションをテストする: v6 に無い「`propertyName`・`input1`・`messageId` は必須のカラム」が `EntityTestSupport` と合っているか。
4. コンストラクタをテストする: v6 にあった「型の制限に該当しないプロパティを個別にテストするコード例（`getParamMap` → `new Entity(params)`）」を落とし、「型の制限は setter と getter のテストと同じ」の1文にした。setter と getter の節の例から読者がコンストラクタ版に読み替えられるか。
5. テスト結果を確認する: 失敗時の出力情報の表（文字種と文字列長は観点＋プロパティ名＋入力値、相関バリデーション・バリデーションメソッドは `title`、setter と getter・コンストラクタは `name`）が実際の失敗メッセージと合っているか。
6. 相関バリデーションをテストする／バリデーションメソッドをテストする: 記述例として送っている記載例ページの「エンティティバリデーション」の例（`testShots` と `params` の対）で、相関バリデーション・バリデーションメソッドの読者が自分のテストデータを組み立てられるか。

### コンポーネント単体テスト（`implementation/class_unit_test/component.rst`）

**由来**: 既存。v6「Action/Componentのクラス単体テスト」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.html ）を軸に、「データベースを使用するクラスのテスト」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/02_DbAccessTest.html ）と「Tips集」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/03_Tips.html ）の DB テスト関連の節を統合した。見出し 15 のうち 内容変更 8・文面調整のみ 6・新設 1。

**利用者観点の課題と変更の考え方**
- v6 はサンプルアプリ `UserComponent#registerUser` 固有の長いコードと Excel 画像で説明していて、汎用の手順（準備データ投入 → 実行 → コミット → 確認）が読み取りにくく、参照系の書き方や `getListMap`・ループ・グループIDの使い方は別の2ページに散らばっていた。参照系・更新系の手順を先に示し、共通する書き方（`ThreadContext`・引数と期待値の取得・データを変えた繰り返し・テストショットごとの使い分け）を1ページに集めた。サンプル固有の記述・画像・ダウンロードリンク4本は落とした。
- v6 のコード例は実装と合っておらず、そのまま書くとコンパイルまたは実行できなかった（`assertSqlResultSetEquals` が3引数、`assertTableEquals(シート名, 実測値)`、`getListMap("/foo/bar/Baz.xlsx", "sheet001", …)`）。`DbAccessTestSupport`・`TestDataParser`・`PoiXlsReader` に合わせて直し、別ディレクトリのテストデータは Excel／YAML それぞれの解決先を書いた。
- v6 はテストデータの記述例（Excel）を本ページ内に持っていた。記述例は記載例ページに集約し、本ページはテストコード側の書き方に絞った。

**レビューポイント**
1. 参照系のテストを作成する／更新系のテストを作成する／データを変えて同じテストメソッドを実行する: 直したコード例（`support.assertSqlResultSetEquals("全件検索", "testSelectAll", "expected", actual)` の4引数、`support.assertTableEquals("testDeleteExpired")`、`deleteExpired()` を戻り値なしに）が `DbAccessTestSupport` と合っているか。
2. テストクラスを作成する: 「`@DbAccessTest` を付けて `DbAccessTestSupport` 型のフィールドを宣言すると、テストメソッドの前後でトランザクションが開始・終了される」が `DbAccessTestExtension` と合っているか。ブランクプロジェクトのテストクラスの書き方と合っているか。
3. テストコードと別のディレクトリのテストデータを読み込む: 第2引数が `<ファイル名>/<読み込み単位の名前>` であること、Excel は `<ディレクトリ>/<ファイル名>.xls`（または `.xlsx`）のシート、YAML は `<ディレクトリ>/<ファイル名>/<読み込み単位の名前>.yaml` に解決されることが `PoiXlsReader`・`YamlLoader` と合っているか。
4. テストデータを作成する: 期待値に自動設定項目も書く、テーブル採番の準備データを用意する、静的マスタは投入済み前提、外部キーはマスタデータ復旧機能を参照 — 実際にコンポーネント単体テストを書くときの注意として過不足がないか。
5. テスト結果を確認する: 「確認する対象 → 使用するメソッド」の表は刷新で組んだもの（`assertSqlRowEquals` を含む）。使い分けとして抜け・誤りがないか。`assertSqlResultSetEquals` の性質（全カラム比較・順序厳密）は v6 どおり。

### リクエスト単体テスト（ウェブアプリケーション）（`implementation/request_unit_test/web.rst`）

**由来**: 混在。v6 の「リクエスト単体テスト（ウェブアプリケーション）」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/02_RequestUnitTest.html ）と「リクエスト単体テストの実施方法」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/index.html ）を1ページに統合し、「リクエスト単体テストの実施方法(ファイルアップロード)」（同 `05_UnitTestGuide/02_RequestUnitTest/fileupload.html`）・「二重サブミット防止機能のテスト実施方法」（同 `double_transmission.html`）・「リクエスト単体テストの実施方法(メール送信)」（同 `mail.html`）・「目的別API使用方法」（同 `06_TestFWGuide/03_Tips.html` の「クラスのプロパティを検証したい」）を取り込んだ。見出し 23 のうち内容変更 14・文面調整のみ 8・新設 1。

**利用者観点の課題と変更の考え方**
- v6 は「実施方法」と「テスティングフレームワークの構造」が別ページで、テストクラスを1つ書くのに両方を往復する必要があった。作成→実行→確認の順に1ページへ統合し、内部構造（継承階層の図、`HttpServer`・`HttpRequestTestSupport`・`DbAccessTestSupport` の表の行）は落として、利用者が名前を書くクラスだけを表に残した。
- v6 のコード例には、写してもコンパイルできない箇所があった（`getParam` の戻り値は `String[]`、`assertObjectPropertyEquals` の例が `HttpRequestTestSupport` を継承しつつ同クラスに無い `execute(String, Advice)` を呼ぶ、`getListMap` の読み込み単位名がテストメソッドと別名）。実装のシグネチャに合わせて直した。
- インジェクション方式では呼べないメソッド（`protected` の `execute(String, HttpRequest, ExecutionContext)`、`protected abstract` の `getBaseUri()`）を v6 のまま案内すると読者が詰まる。`Class<?>` 付きの `execute` と合成アノテーションの `baseUri` 属性に置き換えた。
- 出力されたファイルを探せるように、HTML ダンプとダウンロードファイルの名前を v6 の「テストケース説明と同名」から実装どおりの `読み込み単位の名前_Shot番号_説明` 形式に改め、固定パス `tmp/html_dump` は設定ページに委ねた。サポートクラスが自動確認する項目も v6 の4項目から実装どおりの8項目に広げた。

**レビューポイント**
1. 機能概要: 「主なクラスとリソース」を5行（テストクラス・テストデータ・Action・`BasicHttpRequestTestTemplate`・`TestCaseInfo`）に絞り、`HttpServer`・`DbAccessTestSupport`・`HttpRequestTestSupport` を落とした。利用者が名前を書くクラスだけという基準で過不足がないか。図8（同一 JVM 上の構成物）で構造の説明として足りるか。
2. サポートクラスをインジェクションする: 実行手順を「トークン設定 → `beforeExecute`」の順にし（v6 は逆）、`setUpDb` は繰り返しに入る前に1回だけとした。実装 `AbstractHttpRequestTestTemplate` の `executeTestCase`・`execute(String, Advice, boolean)` と合っているか。
3. テストを実行するメソッドを呼び出す: `execute` の4オーバーロード（引数なし／`sheetName`／`shouldSetUpDb`／両方）と「`shouldSetUpDb=false` で `setUpDb` を省略できる」を足した。JUnit 5 のインジェクションで引数なし `execute()` がテストメソッド名を解決できることを含め、実装と合っているか。
4. リクエストと実行コンテキストを組み立てる: 送信メソッドを `execute(Class<?>, String, HttpRequest, ExecutionContext)` に差し替えた。第1引数の説明「クラスの名前が HTML ダンプの出力先ディレクトリの決定に使われる」で読者が正しく使えるか。
5. テスト結果を確認する: 自動確認8項目とカラム名の対応が `AbstractHttpRequestTestTemplate#assertAll` と合っているか。特に「同期送信したメッセージの確認（`expectedMessage`・`responseMessage`）」を自動確認の項目に含めてよいか。
6. リクエストスコープの値を確認する: v6 にあった Form 取得と `SqlRow` のコード例を落とし、型ごとの使用メソッド表と tip に置き換えた。利用経験から、コード例なしで `SqlRow`・入れ子 Form の確認が書けるか。
7. アップロードファイルを用意する: v6 の具体例2組（`picture.png` を指定する `requestParams`、`member_list.csv` を生成する `SETUP_FIXED`）を落とし、2方法の説明と記法ページへの参照だけにした。具体例なしで書き始められるか（記載例ページに画像ファイルの例はある）。
8. ダウンロードファイルを確認する／HTMLダンプを目視で確認する: ファイル名 `読み込み単位の名前_Shot番号_説明.html`・`…_ダウンロードされたファイル名` が実装 `TestCaseInfo#getTestCaseName`・`HttpServer#getFileByContentDisposition` と合っているか。

### リクエスト単体テスト（RESTfulウェブサービス）（`implementation/request_unit_test/rest.rst`）

**由来**: 既存。v6 の「リクエスト単体テスト（RESTfulウェブサービス）」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_rest.html ）と「リクエスト単体テストの実施方法」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/rest.html ）を1ページに統合した。見出し 9 のうち内容変更 6・文面調整のみ 3・新設 0。

**利用者観点の課題と変更の考え方**
- v6 の「実施方法」は5ステップの参照リストで、各ステップの中身は別ページの「構造」節へ飛ばないと読めなかった。各ステップを本ページの節にし、テストクラスの全体像のコードを先頭に置いて、往復せずに1本のテストが書ける並びにした。
- v6 のコード例 `readTextResource("…json")` は継承前提で、インジェクション方式では1引数版が `protected` のため呼べない。`readTextResource(getClass(), fileName)` に差し替え、期待値ファイルの配置パスも Maven 標準の `src/test/resources/...` に補った。
- v6 の「`sendRequest` を呼ぶと内蔵サーバが起動される」は実装と違い、起動はテストメソッドの実行前に行われる。「起動済みの内蔵サーバに送信する」に改め、読者がサーバ起動のタイミングを誤解しないようにした。
- リクエストボディの設定方法（`setBody`、Content-Type 未設定時は `application/json`）が v6 に無く、POST・PUT・PATCH のテストが書けなかった。実装で挙動を確かめて1段落足した。

**レビューポイント**
1. 機能概要: 表から `HttpServer`・`DbAccessTestSupport` を落とし、`RestTestSupport`・`SimpleRestTestSupport` を1行に併記した。「必要なモジュールは他の処理方式より多い。モジュールの追加とコンポーネント設定は設定ページに従う」で、設定ページとの分担が読者に伝わるか。
2. テストクラスを作成する: tip「`testDataParser` のコンポーネントを準備する（`dbInfo` はそのプロパティ）」（v6 は「`dbInfo` または `testDataParser`」）が、実装 `RestTestSupport`（リポジトリキー `testDataParser`）・`BasicTestDataParser#setDbInfo` と、ブランクプロジェクトの `unit-test.xml` の設定と合っているか。
3. テストメソッドを作成する: `setBody` の段落「文字列はそのまま、それ以外のオブジェクトは Content-Type が `application/json` の場合に JSON へ変換。Content-Type 未設定なら `application/json` が設定される」が `RestMockHttpRequest#setBody`・`RestMockHttpRequestBuilder` の既定値と合っているか。JSON 以外の Content-Type でオブジェクトを渡した場合の扱いをこの書き方で読者が誤らないか。
4. テストを実行する: 「内蔵サーバは、サポートクラスがテストメソッドの実行前に起動する」が、JUnit 5 のインジェクション経由でも `SimpleRestTestSupport#setUp` と同じタイミングになるか。
5. レスポンスボディを検証する: `readTextResource(Class<?>, String)` への差し替えと、配置表の `<PROJECT_ROOT>/src/test/resources/com/example/SampleTest/` が実装（`testClass.getSimpleName() + "/" + fileName` をクラスパスから解決）と合っているか。
6. v6 にあった「`SimpleRestTestSupport` を継承する場合は以下のテストデータの書き方は読み飛ばしてよい」に相当する一言が無い。`SimpleRestTestSupport` を選んだ読者が「テストデータを作成する」を読み飛ばせると分かるか。

### リクエスト単体テスト（HTTPメッセージング）（`implementation/request_unit_test/http_messaging.rst`）

**由来**: 既存。v6 の「リクエスト単体テストの実施方法（HTTP同期応答メッセージ受信処理）」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/http_real.html ）と「リクエスト単体テストの実施方法(HTTP同期応答メッセージ送信処理)」（同 `05_UnitTestGuide/02_RequestUnitTest/http_send_sync.html`）の導入部、および「リクエスト単体テスト（HTTP同期応答メッセージ送信処理）」（同 `06_TestFWGuide/RequestUnitTest_http_send_sync.html`）の読み替え表から来た。見出し 3 のうち内容変更 1・文面調整のみ 2・新設 0。

**利用者観点の課題と変更の考え方**
- v6 は受信・送信の2ページがそれぞれ「MOM のページを参照せよ」と書くだけで、何が同じで何が違うかを読者が自分で突き合わせる必要があった。「MOM と同じ枠組み。違うのはテストデータとコンポーネント設定」と1ページで宣言し、固有の手順が無いことと用語の読み替え表だけを置いた。
- v6 の読み替え表にある `MockMessagingContext → MockMessagingClient` は、リクエスト単体テストの経路では呼ばれない取引単体テスト向けのクラスで、読み替え先の MOM ページにも登場しない。読者が探しても見つからない読み替えになるため、行を落とした。
- v6 の「送信キュー・受信キューを通信先と読み替える」は限定が無かったが、受信側のテストは実際にキューを使う。読み替えの適用範囲を「同期応答メッセージ送信の説明」に限定し、受信側の「キュー」はそのまま読ませる。
- MOM ページの「処理は内部クラスに委譲される」を機械的に読み替えると実装に無い記述になるため、`RequestTestingMessagingClient` は内部クラスを持たず自身がアサートと返却を行う旨を足した。

**レビューポイント**
1. 機能概要: 「HTTP メッセージ受信は同期応答メッセージ受信と、HTTP メッセージ送信は同期応答メッセージ送信と同じ方法で行う」という言い換えが、利用経験上そのとおりか。差分が本当にテストデータとコンポーネント設定だけか。
2. 用語を読み替える: `MockMessagingContext → MockMessagingClient` の行を落としてよいか。取引単体テストでこの読み替えを必要とする読者が本ページに来る可能性はないか。
3. 用語を読み替える: 適用範囲を「同期応答メッセージ送信の説明」に限定したことと、末尾の「`RequestTestingMessagingClient` は内部クラスを持たず、要求電文のアサートと応答電文の返却は同クラス自身が行う」が、実装 `RequestTestingMessagingClient#sendSync` と合っているか。
4. 使用方法: 「HTTP メッセージングに固有の手順はない」と言い切ってよいか。HTTP メッセージングで追加で必要な準備があれば指摘してほしい。

### リクエスト単体テスト（Nablarchバッチアプリケーション）（`implementation/request_unit_test/batch.rst`）

**由来**: 混在。v6 の「リクエスト単体テスト（バッチ処理）」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_batch.html ）と「リクエスト単体テストの実施方法(バッチ)」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/batch.html ）を1ページに統合し、「リクエスト単体テストの実施方法（応答不要メッセージ送信処理）」（同 `05_UnitTestGuide/02_RequestUnitTest/delayed_send.html`）を取り込んだ。見出し 7 のうち内容変更 6・文面調整のみ 0・新設 1。

**利用者観点の課題と変更の考え方**
- v6 は「バッチ」と「応答不要メッセージ送信」が別ページで、後者の実体が Nablarch バッチアプリケーションのテストであることが見えにくかった。1ページに統合し、応答不要メッセージ送信は「異なる箇所だけ」を各節に差し込む形にした。
- v6 が「通常はこちらを使う」と勧める引数なし `execute()` は、インジェクション方式では呼べない（`protected final`）。読み込み単位の名前をリテラルで渡す1方式に統一し、v6 のコード例で `testRegister` メソッド内の `execute()` を「`execute("testRegisterUser")` と等価」と書いていた誤りも正した。
- v6 の `MainForRequestTesting` の差異「常駐化機能を無効化する」は実装に無く、実際に行うのは「実行後にリポジトリを元に戻す」である。実装どおりに改め、ループ制御ハンドラの置き換え条件を「常駐バッチの場合」から「ハンドラ構成にリクエストスレッド内ループ制御ハンドラが含まれる場合」に変えた。
- 応答不要メッセージ送信で読者がはまる点（`expectedMessage` にグループ ID を書かないと要求電文が照合されない、Action を差し替えないと `errorCase` が無視される、`expectedStatusCode` は空欄にできない）を実装で確かめて明記した。

**レビューポイント**
1. 機能概要: 表を3行（テストクラス・テストデータ・`BatchRequestTestSupport`）にし、`MainForRequestTesting`・`TestShot`・`FileSupport`・`DbAccessTestSupport` は地の文と図13 で説明した。落とし過ぎていないか。特に `FileSupport` は、ダウンロードのテストで利用者が `new FileSupport(getClass())` と名前を書くクラスである。
2. テストメソッドを作成する: `support.execute("testRegisterUser")` のリテラル方式に統一した。`execute(String, boolean setUpPerTestShot)`（テストショットごとに準備データを投入する版）に触れていないが、利用者に必要か。
3. テストデータを作成する: important「切り替えないまま `errorCase` を記述しても、正常系として実行される」「`expectedStatusCode` には、異常終了したときの終了コードを記述する」が、`AsyncMessageSendActionForUt` と本番の `AsyncMessageSendAction` の実挙動と合っているか（本番 Action が `errorCase` を無視することは本番側で確認してほしい）。
4. テストを実行する: 「`MainForRequestTesting` はテスト対象の実行後に元のリポジトリへ戻す」「ハンドラ構成にリクエストスレッド内ループ制御ハンドラが含まれる場合は置き換える」が `MainForRequestTesting#handle` と設定ページの記述、および利用経験と合っているか。
5. テスト結果を確認する: 「`expectedStatusCode` は必須カラム。値を空にすると終了コードと一致せず失敗する」が `TestShot.REQUIRED_COLUMNS`・`BatchRequestTestSupport#compareStatus` と合っているか。v6 の「データベースの結果検証」に「実際のファイル出力結果を確認できる」とあったのを誤記と見て「テーブルの状態を照合する」に読み替えた。
6. テスト結果を確認する: ファイル期待値の記法表（`EXPECTED_FIXED[グループID]=` 等）とログ検証のカラム表・AND 条件の注意を本ページから落とし「テストデータの書き方」への参照にした。バッチの読者が本ページだけで期待値を書けなくて困らないか。

### リクエスト単体テスト（MOMによるメッセージング）（`implementation/request_unit_test/mom.rst`）

**由来**: 既存。v6 の5ページを1ページに統合した。「リクエスト単体テスト（メッセージ受信処理）」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/06_TestFWGuide/RequestUnitTest_real.html ）、「リクエスト単体テスト（同期応答メッセージ送信処理）」（同 `06_TestFWGuide/RequestUnitTest_send_sync.html`）、「リクエスト単体テストの実施方法(同期応答メッセージ受信処理)」（同 `05_UnitTestGuide/02_RequestUnitTest/real.html`）、「リクエスト単体テストの実施方法(同期応答メッセージ送信処理)」（同 `05_UnitTestGuide/02_RequestUnitTest/send_sync.html`）、「リクエスト単体テストの実施方法（応答不要メッセージ受信処理）」（同 `05_UnitTestGuide/02_RequestUnitTest/delayed_receive.html`）。見出し 7 のうち内容変更 5・文面調整のみ 2・新設 0。

**利用者観点の課題と変更の考え方**
- v6 は同期応答受信・応答不要受信・同期応答送信が5ページに分かれ、送信のページは「テストクラスの書き方はウェブ・バッチのページを見よ」だけだった。3つのテストを1ページに置き、送信は「テスト対象の処理方式のテストを踏襲し、MOM に固有の点だけ書く」構成にして、どのページを読めばよいかを冒頭で示した。
- v6 が同期応答メッセージ送信で継承させる「`StandaloneTestSupportTemplate` または `AbstractHttpRequestTestTemplate`」は利用者が直接使わない中間クラスで、要求電文をアサートする主体も取引単体テスト用の `MockMessagingContext` と書かれていた。実際にインジェクションする `BatchRequestTestSupport`・`BasicHttpRequestTestTemplate` と、実際に動く `RequestTestingMessagingProvider` に改めた。
- v6 のパッケージ名 `nablarch.test.core.http.MessagingRequestTestSupport` は誤りで、写すと import が通らない。実在の `nablarch.test.core.messaging` に直し、引数なし `execute()`（インジェクション方式では呼べない）を `support.execute("…")` に統一した。
- 実装で確かめて足した事実が3つある。構造化データ以外のフレームワーク制御ヘッダでは `expectedStatusCode` も照合される、応答不要受信では応答電文の確認が行われない、`MainForRequestTesting` は「常駐化を無効化する」のではなく実行後にリポジトリを戻す。

**レビューポイント**
1. 機能概要: 表を `MessagingRequestTestSupport`・`MessagingReceiveTestSupport`・`RequestTestingMessagingProvider`・`TestDataConverter` の4クラス＋テストクラス・テストデータに絞り、`MQSupport`・`MessageSender`・`MainForRequestTesting`・`TestShot` は地の文と図15・図17 で触れるだけにした。構造の説明として足りるか。
2. 機能概要: 同期応答メッセージ送信の流れ「`MessageSender` が生成した要求電文を `RequestTestingMessagingProvider` が受け取り、期待値とアサートし、テストデータの応答電文を生成して返す。`MessageSender` がそれをパースして Action へ渡す」が、実装と Nablarch Application Framework 側の実際の流れに合っているか。
3. テストクラスを作成する: 同期応答メッセージ送信で `BatchRequestTestSupport`／`BasicHttpRequestTestTemplate` をインジェクションする、という案内だけで送信テストを書き始められるか。v6 の `StandaloneTestSupportTemplate`／`AbstractHttpRequestTestTemplate` の名前を本ページから消してよいか。
4. テストデータを作成する: 「同期応答メッセージ送信のテストデータも、テストクラスに対応する読み込み単位に記述する」「`expectedMessage`・`responseMessage` にグループ ID を記述してテストショットと対応付ける」が、利用経験と `RequestTestingMessagingContext#initializeForRequestUnitTesting` の引数と合っているか。
5. テスト結果を確認する: 「構造化データ以外のフレームワーク制御ヘッダを使用する場合、`expectedStatusCode` とステータスコードの照合も行われる」が `MessagingRequestTestSupport`（`fwHeadFormatter` が設定されている場合の分岐）と合っているか。応答不要受信で「応答電文の内容の確認は行われない」と明文化してよいか。
6. 使用方法: 受信テストのコンポーネント設定（`EmbeddedMessagingProvider`、送信テストでの `RequestTestingMessagingProvider` への差し替え）は設定ページ側に置いた。本ページからの導線（使用方法の末尾）で足りるか。

### リクエスト単体テスト（テーブルをキューとして使ったメッセージング）（`implementation/request_unit_test/db_queue.rst`）

**由来**: 新規。v6 に対応するページは無い（v6 のテスティングフレームワーク解説書に「テーブルをキューとして使ったメッセージング」の記述は 0 件）。見出し（L2〜L4）は 0。本文は「Nablarch バッチアプリケーションと同じ方法で行う」の1文と、そのページへの参照だけである。

**利用者観点の課題と変更の考え方**
- v6 では「テーブルをキューとして使ったメッセージング」のテスト方法がどこにも書かれておらず、この処理方式のテストを書こうとした読者は、バッチのテストと同じでよいのかを自分で判断するしかなかった。読者が章見出しから辿り着けるよう独立したページを立て、中身は導線だけにした（コード例・テストデータの例は置かない）。

**レビューポイント**
1. 「Nablarch バッチアプリケーションと同じ方法で行う」の1文で足りるか。飛び先のバッチのページはテーブルをキューとして使ったメッセージングに一言も触れていない。飛び先側に受けの一言（この処理方式もこの方法で行う旨）が要るか。
2. 利用経験から、テーブルをキューとして使ったメッセージングのリクエスト単体テストで、バッチと異なる準備が本当に無いか。ハンドラ構成（リクエストスレッド内ループ制御ハンドラ）の置き換えは設定ページ側に書かれているが、それ以外に本ページで触れるべき差分が無いか。

### 取引単体テスト（ウェブアプリケーション）（`implementation/deal_unit_test/web.rst`）

**由来**: 既存。v6「取引単体テストの実施方法」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/index.html ）と、「二重サブミット防止機能のテスト実施方法」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/02_RequestUnitTest/double_transmission.html ）の取引単体テスト側を1ページにした。見出し 6 のうち内容変更 1（テスト結果のエビデンスを取得する）・文面調整のみ 5・新設 0。

**利用者観点の課題と変更の考え方**
- v6 には「画面ハードコピー取得ツール、DBダンプ取得ツール等は現在検討中」という tip が 2020 年から残り、読者が補助ツールの提供を待つ形になっていた。取得するエビデンス（画面ハードコピー・DBダンプ）は変わらないので、tip だけを落とした。
- v6 では二重サブミット防止機能の確認手順がリクエスト単体テストのページ配下にあり、取引単体テストの読者が辿り着きにくかった。本ページの見出しに畳み、クライアントサイドとサーバサイドで確認が分かれる理由はリクエスト単体テスト（ウェブアプリケーション）へ参照で送った。
- 準備手順の「アプリケーションサーバを起動する」と、二重サブミット確認の「デバッグモードで起動する」が同じページに並ぶことになったため、後者を「テストの実施とは別に」行う手順として書き分けた。
- 機能概要に、HTTP メッセージ送信を伴う場合の導線を足した（v6 は MOM 版への参照のみ）。

**レビューポイント**
1. 機能概要: ウェブアプリケーションの取引単体テストでテスティングフレームワークが関わるのはモックアップクラスだけ、という書き方で足りているか。MOM 版・HTTP メッセージング版への2本の導線で読者が迷わないか。
2. テスト結果のエビデンスを取得する: 補助ツールの tip を落とした。現時点で提供予定・提供済みの補助ツールがあれば、この節に書き戻す必要があるか。
3. 二重サブミット防止機能を確認する: 4 手順（デバッグモードで起動→ブレークポイント→ボタン選択→止めた状態で再選択し送信されないことを確認）が、現行のブランクプロジェクトの二重サブミット防止の実装で今も成立するか。

### 取引単体テスト（RESTfulウェブサービス）（`implementation/deal_unit_test/rest.rst`）

**由来**: 混在。v6「取引単体テストの実施方法」（RESTfulウェブサービス。https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/rest.html ）。見出し 3 のうち内容変更 1（機能概要）・文面調整のみ 1（テストメソッドを作成する）・新設 1（使用方法）。v6 後半の「Cookie など前のレスポンスの情報を引き継ぐ方法」は設定の話なので「取引単体テストの設定（RESTfulウェブサービス）」へ移し、本ページは tip で導線だけを置いた。

**利用者観点の課題と変更の考え方**
- v6 は「リクエスト毎のテストを連続実行することにより取引単体テストが実施可能」と書いており、テストメソッドを複数並べれば取引になると読めた。しかし v6 自身のコード例は1つのテストメソッド内で3リクエストを送っており、実装もテストメソッドごとに `RequestResponseProcessor#reset` を呼ぶため、メソッドをまたいだ引き継ぎは効かない。「複数のリクエストを1つのテストメソッドの中で順に送信する」に改めた。
- v6 はテストクラスの作り方・実行方法・テストデータの書き方を書いておらず、読者がどこを見ればよいか分からなかった。使用方法の1文で、リクエスト単体テスト（RESTfulウェブサービス）とテストデータの書き方へ委譲した。
- v6 のコード例は `parseProject`・`assertProjectEquals` が何かを説明しておらず、フレームワークの API と誤解する余地があった。テストクラスに用意した補助メソッドである旨を注記した。

**レビューポイント**
1. 機能概要: 「1つのテストメソッドの中で順に送信する」が実装 `SimpleRestTestSupport`（`setUp` で `defaultProcessor.reset()` を呼ぶ）と合っているか。テストメソッドを分けて取引を構成している現場の運用があれば、この記述で困らないか。
2. テストメソッドを作成する: `parseProject`・`assertProjectEquals` を「テストクラスに用意した補助メソッド」と注記した。読者がこの2つを自分で書くものだと読み取れるか。
3. 使用方法: 「テストクラスの作成方法とテストの実行方法はリクエスト単体テスト（RESTfulウェブサービス）と同じ」の1文だけで足りるか。取引単体テストで追加で必要なもの（例の取引がセッションや CSRF トークンの引き継ぎ設定なしで動く前提など）が抜けていないか。

### 取引単体テスト（HTTPメッセージング）（`implementation/deal_unit_test/http_messaging.rst`）

**由来**: 既存。v6「HTTP同期応答メッセージ送信処理を伴う取引単体テストの実施方法」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/http_send_sync.html ）の実施方法部分。同ページ後半の「フレームワークで使用するクラスの設定」は「取引単体テストの設定（HTTPメッセージング）」へ移した。見出し 3 のうち内容変更 2（使用方法、テストデータを作成する）・文面調整のみ 1（機能概要）・新設 0。

**利用者観点の課題と変更の考え方**
- v6 は「MOM 版を参照し、送信キュー・受信キューを通信先と読み替える」とだけ書き、ログの出方まで MOM 版と同じだと読めた。実装 `MockMessagingClient` は `MESSAGING` ロガーへ INFO で出すだけで、MOM 版の Map 形式・CSV 形式のログは出ない。MOM 版の `log.properties` 設定をそのまま真似ても何も出ないため、使用方法でこの違いを明示した。
- v6 は「HTTP 通信は要求・応答電文ともにヘッダが存在しないため本文のみ定義する」と書いていたが、実装は `RESPONSE_HEADER_MESSAGES` を読んで応答電文のヘッダに渡す。前提を書かず「本文だけを定義すればよい。ヘッダを指定する場合は併せて定義する」に改めた。
- v6 は「要求電文のフォーマットはログ出力に使われる」と書き、記載例の画像に要求電文のデータブロックがあったが、実装はフォーマット定義ファイル `<リクエストID>_SEND` を使い、テストデータの要求電文ブロックを読まない。読者に実装が無視する記述を書かせないよう「要求電文のデータブロックは定義しない」に改め、画像は落として「テストデータの記載例」へ送った。

**レビューポイント**
1. 使用方法: 「`MESSAGING` ロガーに INFO で出力され、Map 形式・CSV 形式は出ない」が `MockMessagingClient` の現行実装と合っているか。HTTP メッセージング用のログ出力設定の例が本ページにも設定ページにも無い状態で、エビデンス取得の手順として読者が困らないか。
2. テストデータを作成する: 「要求電文のデータブロックは定義しない」は、v6 の画像どおりに要求電文ブロックを書いてある既存のテストデータと衝突する。書いてあっても無視されるだけである旨を補足するべきか。
3. テストデータを作成する: `RESPONSE_HEADER_MESSAGES` でステータスコードを返せることに触れていない（カラム名を名指ししていない）。4xx/5xx 応答を試す読者にとって必要な情報か。

### 取引単体テスト（Nablarchバッチアプリケーション）（`implementation/deal_unit_test/batch.rst`）

**由来**: 混在。v6「取引単体テストの実施方法（バッチ）」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/batch.html ）。見出し 7 のうち内容変更 3（テストメソッドを作成する、テストデータを作成する、Excel形式の場合）・文面調整のみ 3（機能概要、使用方法、テストクラスを作成する）・新設 1（YAML形式の場合）。

**利用者観点の課題と変更の考え方**
- v6 の表とコードを写すとテストが動かない。必須カラム `diConfig`・`userId` が表に無く、`case`・`outFile` は実装に無いカラム名で、import のパッケージも実在しない（`messaging.BatchRequestTestSupport`）。実装の必須カラム（`TestShot.REQUIRED_COLUMNS`）とカラム名（`description`・`expectedFile`）に合わせて全表と import を直した。
- v6 は正常系の例に `expectedStatusCode: 100` を書いていたが、FW 解説書では 100〜199 はエラー処理用の範囲である。正常終了の例として `0` に直した。あわせて、対応するデータブロックが無い `expectedTable: fileInputBatch` を空欄にした。
- v6 は準備データの投入と期待値の検証がテストショットごとに行われることを書いておらず、3つの書き方で期待値カラムの有無が違う理由を読者が読み取れなかった。実装どおり「投入はショットごと」「`expectedTable`・`expectedFile` が空欄なら検証しない」を地の文に足した。
- v6 の見出し 6 本（分割方針・基本的な記述方法・複数シート・複数ケース…）は「テストデータを作成する」の導入と 3 つの太字ラベルに再構成し、Excel 形式・YAML 形式の対で示した。

**レビューポイント**
1. テストメソッドを作成する: 引数なし `execute()`（テストメソッド名と同じシートを読む）が注入方式では呼べないため `support.execute("testSuccess")` に置き換え、「読み込み単位の名前はテストメソッド名と同じにする」を規約として書いた。この置き換えと規約が `nablarch-testing-junit5` の `BatchRequestTest` の実装と合っているか。
2. Excel形式の場合: `expectedStatusCode` を `100` から `0` に変えた。バッチの正常終了コードとして `0` が現場の例と合うか。
3. Excel形式の場合: 「複数の読み込み単位に分割する」の各シートに必須 6 カラムをすべて書かせている。実装（`TestShot.REQUIRED_COLUMNS`）どおりだが、既存のテストデータで一部を省いて動いている例が無いか。
4. テストデータを作成する: 「投入はテストショットごと」「期待値カラムが空欄なら検証しない」の 2 文が `TestShot` の実装と合っているか。分割例のユーザ削除シートが `setUpTable: default` と `expectedTable: default` を同時に持つ（前ショットで投入したデータを再投入する）が、例として意図どおりか。
5. YAML形式の場合: Excel の空セルに対応するキーを `""` で書き下している。キーを省略した場合と同じ動作になるか、記法ページの説明と揃っているか。
6. 機能概要: 「1つの取引を構成する複数のバッチ処理」という前提が、本ページへ導線だけで送られてくるテーブルをキューとして使ったメッセージングにも当てはまるか。

### 取引単体テスト（MOMによるメッセージング）（`implementation/deal_unit_test/mom.rst`）

**由来**: 混在。v6 の 3 ページを 1 ページにした。「同期応答メッセージ送信処理を伴う取引単体テストの実施方法」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/send_sync.html ）、「取引単体テストの実施方法（同期応答メッセージ受信処理）」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/real.html ）、「取引単体テストの実施方法（応答不要メッセージ受信処理）」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/05_UnitTestGuide/03_DealUnitTest/delayed_receive.html ）。send_sync.html 後半の設定・障害系・電文記法は設定ページ・記法ページへ移した。見出し 6 のうち内容変更 6・文面調整のみ 0・新設 0。

**利用者観点の課題と変更の考え方**
- v6 は送信側（ウェブアプリケーション）と受信側（バッチ相当）が別ページに散り、応答不要メッセージ送信のページは本文と参照先が食い違っていた。1 ページに畳み、機能概要で「受信側」「同期応答送信を伴うウェブ側」の 2 通りに分け、進め方はそれぞれバッチ版・ウェブ版の取引単体テストへ委ねた。
- v6 はモックアップクラスが何をしないかを書いておらず、応答不要送信や受信のテストにも使えると読めた。実装（`receiveMessage` は `UnsupportedOperationException`、`send`・`sendMessage` はログ出力と固定 ID の返却だけ）を important で明示した。
- v6 の再読み込みの説明は Excel の `no` 列がインクリメントされると書いていたが、実装はデータの並び順で応答を選ぶ。YAML 形式には `no` が無いため「記述した順に 1 件ずつ返す」に改め、画像 2 枚は落として記載例ページへ送った。
- v6 のログ出力例は日時・ロガー名 `MESSAGING_SEND_MAP`・`header:` ラベルを含み、実装のロガー名（`MESSAGING_MAP`/`MESSAGING_CSV`）・ラベル（`message header =`）と一致していなかった。実装どおりの例に直し、DEBUG レベルであることを足した。
- 出典に無い前提として「要求電文のフレームワーク制御ヘッダに `requestId` という名前のフィールドがあること」を足した。無いとモックアップクラスが動かない。

**レビューポイント**
1. 機能概要（important）: モックアップクラスの限定が `MockMessagingContext` の現行実装と合っているか。応答不要メッセージ送信の取引単体テストをどう進めるかが本ページに無いが、それでよいか。
2. 使用方法・テストクラスを作成する: 送信側（ウェブ）の進め方をウェブアプリケーションの取引単体テスト（手動操作）に委ね、「モックアップクラスはコンポーネント設定ファイルで登録するため、テストクラスに記述することはない」とした。送信側ではテストクラスを書かないと読者が読み取れるか。
3. テストデータを作成する: 「`requestId` フィールドがあることを前提」の追記。制御ヘッダのフィールド名を変えているプロジェクトが実際にあるか、注記の重さが適切か。あわせて、テストデータを置くディレクトリの設定を HTTP メッセージングの設定ページへ送っている導線で MOM の読者が迷わないか。
4. テストを実行する: 「テストデータのタイムスタンプが更新されると読み込み直す」を YAML 形式にも当てはまる書き方にした。YAML 形式ではディレクトリ配下の最終更新日時の比較で、1 ファイルを編集すれば効くという理解でよいか（実装 `SendSyncSupport`）。
5. テスト結果を確認する: ロガー名・DEBUG レベル・ログ例の書式が現行の `SendSyncSupport` の出力と一致するか。`log.properties` の設定例がブランクプロジェクトの `log.properties` と併存できるか。

### 取引単体テスト（テーブルをキューとして使ったメッセージング）（`implementation/deal_unit_test/db_queue.rst`）

**由来**: 新規。v6 にこの処理方式の取引単体テストを扱うページは無い（v6 の取引単体テスト配下 8 ページのいずれにも該当しない）。見出し 0（ページ題のみ。本文は 1 文）。

**利用者観点の課題と変更の考え方**
- v6 では、テーブルをキューとして使ったメッセージングの取引単体テストをどう行うかがどこにも書かれておらず、読者はバッチ版のページが当てはまることを自力で見つける必要があった。他の処理方式と同じく章として立て、本文は「Nablarchバッチアプリケーションと同じ方法で行う」という 1 文と参照だけにした（コード例・テストデータ例は置かない）。

**レビューポイント**
1. 本文: 「取引単体テスト（Nablarchバッチアプリケーション）と同じ方法で行う」が実際にそうか。飛び先の前提（1 つの取引が複数のバッチ処理で構成される）と記述例（ファイル入力→ユーザ削除→ファイル出力）が、テーブルをキューとして使ったメッセージングにも当てはまるか。
2. 本文: 1 文だけのページで読者が困らないか。飛び先で読み替えが必要な点（リクエストの単位がテーブルのレコードであることなど）があれば、本ページに 1 文足すべきか。

## 第4部 ツール

### リクエスト単体データ作成ツール（`tools/request_data_tool.rst`）

**由来**: 既存。v6「リクエスト単体データ作成ツール」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/08_TestTools/01_HttpDumpTool/01_HttpDumpTool.html ）と「リクエスト単体データ作成ツール インストールガイド」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/08_TestTools/01_HttpDumpTool/02_SetUpHttpDumpTool.html ）を 1 ページにした。見出し 11 のうち内容変更 5（前提事項、依存関係を確認して起動用スクリプトを配置する、Eclipseから起動できるように設定する、使用方法、入力となるHTMLダンプを生成する）・文面調整のみ 6・新設 0。

**利用者観点の課題と変更の考え方**
- v6 の前提に `JAVA_HOME` が無いが、起動用スクリプトは `%JAVA_HOME%\bin\java` を参照しており、未設定だと起動しない。前提に加えた。同様に、スクリプトを pom.xml と同じ場所に置く理由（自身のディレクトリへ移動して `./lib/*` をクラスパスにする）が無く、別の場所に置いて動かない読者が出るため tip で説明した。
- v6 は「Linux の場合は httpDump.sh」と書くが、配布物に `.sh` は無く読者が入手できない。`httpDump.bat` だけを案内した。前提の「開発環境構築ガイドに従って構築済み」は参照先のページが存在しないので落とした。
- v6 は初期画面表示のテストデータを「空のリクエストパラメータを作成すればよい」と書くが、実装はテストショット番号分の行が無いと例外を投げる。「テストショット番号の列だけを記載した列を用意する」に改め、HTML ダンプの出力先（`htmlDumpDir` の下のテストクラス名ディレクトリ）も足した。
- Eclipse の操作は、画面キャプチャの実物に合わせて押す項目名を「日本語(English)」で特定した。

**レビューポイント**
1. 前提事項・依存関係を確認して起動用スクリプトを配置する: 配布物が `httpDump.bat` だけになり、Linux/Mac で開発するメンバーへの案内が無い。それでよいか、または `.sh` を用意すべきか。
2. Eclipseから起動できるように設定する: 「関連付けられたエディター(Associated editors)」の「追加(Add...)」、「外部プログラム(External programs)」、「参照(Browse...)」が現行 Eclipse の日本語表示と合っているか。
3. 入力となるHTMLダンプを生成する: 「`requestParams` にはテストショット番号の列だけを記載した列を用意する」で、読者が初期画面表示のテストデータを実際に書けるか（テストデータの書き方ページと表現が揃っているか）。
4. 使用方法（図 20）: 新しい全体図が実際の流れ（リクエスト単体テスト→HTML ダンプ→ブラウザで操作→Excel→テストデータへコピー）と一致するか。
5. HTMLダンプからツールを起動する: 「`httpDump` で開く」の操作と、tip の内蔵サーバの挙動（2 回目以降はスキップ、誤って閉じても次回自動起動）が現行の `nablarch-testing-jetty12` 版でも同じか。

### マスタデータ投入ツール（`tools/master_data_tool.rst`）

**由来**: 既存。v6「マスタデータ投入ツール」（目次 https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/08_TestTools/02_MasterDataSetup/index.html 、本文 https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/08_TestTools/02_MasterDataSetup/01_MasterDataSetupTool.html ）と「マスタデータ投入ツール インストールガイド」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/08_TestTools/02_MasterDataSetup/02_ConfigMasterDataSetupTool.html ）を 1 ページにした。見出し 9 のうち内容変更 7・文面調整のみ 2（導入、使用方法）・新設 0。

**利用者観点の課題と変更の考え方**
- v6 の配布物の説明（`tool/db/data/` 配下・`MASTER_DATA.xlsx`）が zip の実物（ディレクトリ無しの 6 ファイル・`.xls` 2 つ）と違い、展開した読者が説明どおりのファイルを見つけられなかった。実物どおりに改め、サンプルアプリケーションのデータが入っていてそのまま実行すると全テーブルが置き換わることを警告した。
- v6 は前提を「アーキタイプから生成されたプロジェクト」とし、同じページの tip で gsp-dba-maven-plugin を推奨しており、本ツールを使う条件が読めなかった。前提を「Maven の標準ディレクトリ構成」に広げ blank_project はその一例とし、バックアップ用スキーマに必要なテーブルの範囲も実装（記述した全テーブルをコピー）に合わせて具体化した。
- YAML 形式への対応で、マスタデータファイルを YAML でも書けること、`masterdata.file` のパターン変更、読み込み単位の違い（Excel はシート、YAML は 1 ファイル）を足した。Excel 形式のファイルに YAML 用パーサを設定すると例外も警告も出ずに投入 0 件になる罠を important にした。
- v6 のターゲット表は動作（main が test へフォールバック、test がバックアップへコピーする範囲、失敗しても `BUILD SUCCESSFUL`、削除→挿入の順序）を書いておらず、投入できたかどうかを読者が判断できなかった。実装と配布物のビルドファイルから書き足した。

**レビューポイント**
1. 機能概要: gsp-dba-maven-plugin の推奨（v6 と同じ）と本ツールの説明が同居して読者が迷わないか。important「Excel 形式に YAML 用パーサを設定すると無言で 0 件」が `MasterDataSetUpper` の現行実装と合っているか。
2. 前提事項: 「Maven の標準ディレクトリ構成なら使える」に広げたが、ビルドファイルが前提とする `src/main/resources`・`src/test/resources`・`classpath:unit-test.xml` 以外に blank_project 固有の前提が残っていないか。
3. マスタデータを記述する: YAML 形式の置き方（`masterdata.dir` 直下、テストクラスに対応するディレクトリを作らない、`MASTER_DATA*.yaml`）が実装と合っているか。important の「`tablesTobeWatched` と同じ集合に保つ」で、片方にだけ足したときの挙動の説明が正しいか（マスタデータ復旧機能の実装 `MasterDataRestorer`）。
4. Antビューからターゲットを実行する: 表の説明（main→test のフォールバック、test は記述した全テーブルをバックアップへコピー、既定ターゲットの実行順）と「失敗しても `BUILD SUCCESSFUL`」が配布物の `master_data-build.xml` と合っているか。
5. AntビューにAntビルドファイルを登録する: 「ビューの表示(Show View)」「ビルド・ファイルの追加(Add Buildfiles)」が現行 Eclipse の表示と合っているか（v6 は「設定(Show View)」「＋印のアイコン」）。

### HTMLチェックツール（`tools/html_check_tool.rst`）

**由来**: 既存。v6「HTMLチェックツール」（https://nablarch.github.io/docs/LATEST/doc/development_tools/testing_framework/guide/development_guide/08_TestTools/03_HtmlCheckTool/index.html ）。見出し 9 のうち内容変更 6・文面調整のみ 3（HTML4.01との相違点、前提事項、使用方法）・新設 0。

**利用者観点の課題と変更の考え方**
- v6 の仕様記述がパーサの実装と食い違い、読者が指摘の理由を理解できなかった。「省略可能なタグも省略を許可しない」は実装では `head`・`body`・`tbody` を要素ごと省略できる。文書型宣言は `PUBLIC` 形式のみで `<!DOCTYPE html>` は指摘される。クォートの例 `<table align="center">` はデフォルト設定で禁止されている属性だった。パーサ定義と実測に合わせて書き直した。
- v6 は HTML5 で書いたプロジェクトで使えないことに触れておらず、サンプルアプリケーション自身が `checkHtml=false` にしている。important で明示し、無効化・差し替えの節へ誘導した。
- v6 の tip「JavaScript に `-` が 2 つ以上連続すると失敗」は、文字列リテラルの `--` では失敗しない（実測）。HTML コメント `<!-- -->` の中に `--` がある場合に限定し、回避策を「コメントで囲まない／外部ファイル化」にした。
- 設定ファイルの書き損じで黙って壊れる事象（BOM で先頭行だけ無効、タグ禁止と属性禁止を併記するとタグ禁止が無効、禁止タグの配下は検出されない、形式不正は例外）と、`htmlCheckerConfig` を設定すると `htmlChecker` が上書きされる副作用を実装から追記した。指摘メッセージの形式を表にし、構文エラーがあると禁止タグの指摘が出ないことを tip にした。

**レビューポイント**
1. 構文チェックの仕様: 省略可否・文書型宣言・クォートの各項目が現行のパーサ定義（`Html4.jj`）と合っているか。特に「`head`・`body`・`tbody` は要素ごと省略できる」。
2. 機能概要: important「HTML5 で記述しているプロジェクトでは使用できない」が強すぎないか（HTML5 で本ツールを使っている現場があるか）。チェック対象の限定（ステータスコード 500 未満、`Content-Type` のサブタイプが `htm` で始まる）が `HttpRequestTestSupport` と合っているか。
3. 使用を禁止するタグ・属性を変更する: 4 つの important が `HtmlForbiddenNodeConf`・`HtmlForbiddenChecker` の実装と合っているか。設定例のパス `src/test/resources/project/html-check-config.csv` がブランクプロジェクトの配置と合っているか。
4. 使用方法: 「デフォルト設定を読み込んでいる場合は W3C 非推奨タグ・属性を禁止する設定ファイルが適用される」が、デフォルト設定（`nablarch-testing-default-configuration`）の `htmlCheckerConfig` の実効値と合っているか。
5. チェックの内容を差し替える: Java の例を `Files.readAllBytes` 版に書き換え、`throws InvalidHtmlException` と `FileUtil.closeQuietly` を外した。`HtmlChecker#checkHtml` のシグネチャと整合し、そのままコンパイルできるか。
6. 指摘の内容を確認する: メッセージ形式の表（最上位・原因例外の 2 表）が現行の出力と一致するか。行番号・桁番号が HTML ダンプ上の位置であることが読者に伝わるか。

### テストデータ変換ツール（`tools/testdata_converter.rst`）

**由来**: 新規。v6 に対応するページは無い。Excel 形式と YAML 形式を相互変換する `nablarch-testing-converter` が YAML 対応に伴って新設されたツールであり、本ページはその実装と設計資料から書き起こした。見出し 10 のうち新設 10。

**利用者観点の課題と変更の考え方**
- Excel 形式で書いてきた既存のテストデータを YAML 形式へ移したい利用者には、「変換で何が保たれ、何が変わるか」が先に要る。両形式の間に仕様上の意味だけを持つ中間モデルを置くこと、往復で意味が変わらないこと、再現されないのはテスティングフレームワークが読まない情報（セルの色・書式、マーカーカラムの値、行末の空セル）だけであることを機能概要に置いた。
- 変換しただけでは「本当に同じか」を確かめられない。同じ形式への往復（Excel→Excel）が中間モデルで表現できるかの確認に使えること、手書きの YAML の記述ミスを実行前に見つける `YamlTestDataValidator` があることを示した。検証は変換の経路に組み込まれておらず、明示的に呼ぶ必要がある点も書いた。
- 設計資料には Maven プラグイン・pom.xml への追加内容が無く、そのままでは使い始められない。実装から、Maven プラグイン（`convert` ゴール）で一括変換する方法と Java のコードから呼ぶ方法の 2 通りを導入・使用方法として書き起こし、出力の構造（ブック ⇔ ディレクトリ＋`<シート名>.yaml`）を表にした。
- Excel 形式へ書き出すときの整形（色・罫線・列幅）は設定で変えられるので、項目とデフォルト値を実装の既定値から表にした。

**レビューポイント**
1. 機能概要（tip）: 「値なしを除いてすべてダブルクォートで囲む。値なしは `null`」が `YamlFormatWriter` と合っているか。読者が YAML を手で書くときも同じ規則に従う必要があるのかが読み取れるか。
2. 意味を変えずに往復できる／往復で再現されないもの: 表と箇条書きの区分（マーカーカラムの値、行末の空セル、`[EMPTY]`、交互記述は警告して変換）が現行の変換実装と一致するか。特に「カラム名の行をマーカーカラムだけで構成したブロックは値ごと保つ」例外。
3. 使用方法: 出力構造（`foo/bar.xlsx` ⇔ `foo/bar/` と `<シート名>.yaml`）が `ConverterPathResolver` と合っているか。`overwrite=false` で同名ファイルがあると「変換を中断する」という書き方で、部分的に出力が残るのかどうかが読者に伝わるか。
4. Mavenプラグインで一括変換する: パラメータ名・必須・デフォルトが `ConverterMojo` と合っているか。導入例の `<plugin>` に `<version>` が無いが、親 POM の管理を前提にしてよいか。
5. Javaのコードから変換を呼び出す: `nablarch.test.tool.converter.TestDataConverter` と既存の `nablarch.test.core.file.TestDataConverter` が同名である。注記で足りるか、実装側でクラス名を変えるべきか（変えるなら本ページも追随する）。
6. YAML形式のテストデータを検査する: 「直下の `.yaml` だけを検査し、上位ディレクトリを指定すると 1 件も検査せず空のリストが返る」を、そのまま仕様として案内してよいか。実装側で警告を出すべき挙動ではないか。
7. Excel形式の出力を整形する: 表のデフォルト値と Java のメソッド名が `ExcelFormatConfig` と合っているか。
