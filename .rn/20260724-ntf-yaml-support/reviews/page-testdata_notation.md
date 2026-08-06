# レビュー記録: `テストデータの書き方`（`implementation/testdata_notation.rst`）

対象 `mapping_id`: `dest_page=テストデータの書き方` の140行（使用方法139・機能概要1、`DROP`なし）。

4観点（A網羅性 / Bトンマナ / C用語 / D整合性）を、それぞれ別のサブエージェントで実施した。プロンプトには
「実測コマンドで裏付けよ」「検証スクリプトを正解として使わず独立に組め」「敵対的にレビューせよ」の3点を
含めた。ラウンド1のみで、`must` は全件解消・`decide` はユーザーレビューに引き継ぐ。

## ラウンド1

| 指摘ID | 観点 | 区分 | 指摘内容 | 対応要否 | 不要の理由 | 対応内容 |
|---|---|---|---|---|---|---|
| A-1 | A | must | `input-0160` 由来。可変長ファイルの有効ディレクティブキーを「8個」と記載していたが、直後の一覧表は9個（`file-type`/`text-encoding`/`record-separator`/`field-separator`/`quoting-delimiter`/`ignore-blank-lines`/`requires-title`/`max-record-length`/`title-record-type-name`）だった | 要 | — | 「8個」→「9個」に修正 |
| A-2 | A | must | `input-0141` 由来。`errorMode:` による障害系テストが機能する範囲（応答電文・モックアップクラス経由に限る）と、`RequestTestingSendSyncSupport`（`GroupMessageParser`）経路では機能しないという制約が欠落していた | 要 | — | `errorMode` 一覧表の直後に `important` を追加し、適用範囲と非対応経路を明記 |
| A-3 | A | must→decide | `input-0101`/`input-0102`（ウェブアプリのtestShots必須カラム）は `isValidToken`/`forwardUri`/`context` を必須、`requestParams` を任意としているが、旧current側出典（`current-0081`、`index.rst` の表）は `isValidToken`/`forwardUri` を必須マーク無し（任意相当）、`requestParams` は同表に無く別表（別途「必須記載」と地の文で案内）としている。成果物は旧current側の区分に従った。2つの出典が「必須」の割当で食い違っており、ドキュメント同士の突合では正誤を決定できない | 要判断 | 出典間の対立でありdesign.md 11.8「機械検証できないもの」に該当しない新種の対立（実装未確認）。決定には`HttpRequestTestSupport`の実装確認が要る | ユーザーレビューに引き継ぐ（後述「decide」参照） |
| B-F01 | B | decide | L3見出し配下の細分に太字文（「〜する。」形式）を7箇所使用。`style.md` S-04はL1/L2/L3の3階層のみ定義、FW解説書コーパスにもこの用法の前例なし | 要判断 | style.mdに規約が無いための設計判断 | ユーザーレビューに引き継ぐ |
| B-F02〜F10 | B | must | 出典9箇所（`input-0126`カラム省略・`06_TestFWGuide/01_Abstract.rst`複数箇所等）の一文がほぼそのまま（語順・接続・修飾関係一致）残っていた。詳細は各指摘参照 | 要 | — | 9箇所すべて常体で言い換え。主キー省略・FK省略・DELETE挙動・EXPECTED_TABLE省略時挙動・セル書式の準備・空行の`""`記法・DATE型タイムゾーン依存・forwardUri・コメント機能導入文 |
| B(他8観点) | B | — | S-01〜S-03, S-05〜S-08は違反なし | 不要 | 確認済み・問題なし | — |
| T-01 | C | must | L658「メッセージ同期送信・HTTPメッセージ同期送信」の語順が`glossary.md`の正表記（「同期応答メッセージ送信」「HTTPメッセージ送信」）と不一致。同じページの他箇所（L604・L607）は正しい語順だった | 要 | — | 正しい語順に修正 |
| T-02 | C | must | 「セクション」が3箇所（旧L319・L701・L704）でデータブロックの意味に誤用。`glossary.md` §8は「テストデータの単位を指す場合は`データブロック`に置換」と規定 | 要 | — | 3箇所とも「データブロック」に置換 |
| T-03 | C | decide | L1068「電文ヘッダ」「電文ボディ」が、同ページ他所（5箇所以上）で使う正表記「フレームワーク制御ヘッダ」「メッセージボディ」と不統一。`glossary.md`未収録語のため機械的な正表記違反ではない | 要 | ページ内一貫性のための編集判断として妥当性が高く、対応するリスクが低いと判断し著者判断で修正 | 「電文ヘッダ」「電文ボディ」の呼称を削除し「フレームワーク制御ヘッダ」「メッセージボディ側」に統一 |
| D-1 | D | must | L435「``SETUP_TABLES``」（複数形）が、ページ内の14種のデータタイプ一覧（``SETUP_TABLE``単数形のみ）と矛盾。出典`current-0122`（`rest.rst:116`）を確認したところ、現行解説書の全域中でも1箇所のみの表記であり、他に同名の別データタイプとしての言及が無いことを`grep`で確認した | 要 | — | `SETUP_TABLES`→`SETUP_TABLE`に統一（現行解説書側の表記揺れと判断） |
| D-2 | D | decide | 見出し「テストデータファイルの構造を理解する」配下に、テスト独立性・マスタデータ再利用という異質な内容（旧L126-132）が混在し、見出しの範囲を超えていた | 要判断 | 内容の追加・削除を伴わない見出し分割の範囲内であり、著者判断で対応可能と判断 | 「テストの独立性を保つ」というL3見出しを新設し、該当2段落をそちらへ分離 |
| D-3 | D | note | ウェブアプリ用カラム表に`expectedStatusCode`が共通カラム表と重複掲載されていた | 不要 | 実害が小さく、他の処理方式の表には同種の重複が無い局所的な冗長のため記録のみに留める | 未対応（記録のみ） |
| D-4 | D | decide | `about/index.rst`（第1部・特徴3点目）の`:ref:`は現状 `テストデータ変換ツール` のみを指しており、design.md 74行目が「本ページ（テストデータの書き方）作成後に参照を見直すことを検討する」としていた宿題が未着手 | 要判断 | 既に承認済みの第1部ページへの変更を伴うため、著者判断でなくユーザー判断が必要 | ユーザーレビューに引き継ぐ |
| D-5 | D | note | 「外部化」の事実が`about/index.rst`（特徴2点目）と本ページ冒頭の両方で異なる理由づけとともに説明されている | 不要 | design.mdが定める役割分担（外部化の事実は第1部、独立性は第3部）の範囲内であり、致命的な重複ではないため記録のみに留める | 未対応（記録のみ） |

## ラウンド1終了時点のまとめ

- `must`: A-1・A-2・B-F02〜F10（9件）・T-01・T-02・D-1、全て解消。Dockerフルビルド（`-a`）で`build succeeded, 1 warning`（既知の`db_double_submit.rst`のみ）を確認
- `decide`（3件、著者判断で解消したT-03・D-2を除く）: A-3（必須/任意区分の出典対立）・B-F01（L4相当の太字疑似見出しパターン）・D-4（`about/index.rst`特徴3点目の参照見直し）。ユーザーレビューで判断を仰ぐ
- `note`（2件）: D-3・D-5。対応不要、記録のみ

## ラウンド2（差し戻し是正）

`#9`はuser reviewで差し戻し。是正指示は `ntf-doc-09-fix.md`。ラウンド1の`decide`3件のうちA-3・B-F01は実物確認で決着し、
D-4はユーザー判断で`#9`是正に同梱した。加えて観点Aが検出できていなかった網羅性の欠落2件（`requestParams`/`responseResult`、
`searchResult`）を新規`must`として記録する。以下は参照したコミット `e21bf67`（`nablarch/nablarch-testing`の`main`、
`nablarch-testing` 2.2.0、`release-6u2`マージ済み）に基づく。**同リポジトリに`6u3`のブランチ・タグは存在せず
（`git ls-remote origin`で確認済み）、`6u3`との差分は未確認である。**

| 指摘ID | ラウンド | 観点 | 区分 | 指摘内容 | 対応要否 | 不要の理由 | 対応内容 |
|---|---|---|---|---|---|---|---|
| A-3（確定） | 2 | A | must | ラウンド1で出典対立のため`decide`に回した`isValidToken`/`forwardUri`の必須区分は、実装確認により決着した。`TestCaseInfo#isValidToken()`（`TestCaseInfo.java:482-484`）は`getValue`経由で読み、呼び出し元`AbstractHttpRequestTestTemplate#executeTestCase:257`は条件分岐の外にあり全テストケースで必ず評価される。`TestCaseInfo#getExpectedForwardUri()`（`TestCaseInfo.java:237-239`）も同じく`getValue`経由で読み、`assertForwardUri`（`AbstractHttpRequestTestTemplate.java:554-557`）は`assertAll:464`から無条件に呼ばれる。全処理方式で「必須」とはカラム自体の存在を指し値は空でよいこと（ウェブアプリケーション: `TestCaseInfo.java:443-448`の`containsKey`判定、バッチ・メッセージング: `TestShot.java:77-78`の`assertContainsRequiredKeys`、エンティティバリデーション: `EntityTestSupport.java:269-276`の`containsAll`判定）も確認した | 要 | — | `isValidToken`・`forwardUri`の必須列を「必須」に修正し、「必須」の意味を1文で定義（STEP 1(a)(b)） |
| B-F01（確定） | 2 | B | must | ラウンド1で規約不在のため`decide`に回したL4相当の太字疑似見出し7箇所は、`ja/`配下全体の実測により決着した。`ja/application_framework/adaptors/lettuce_adaptor/redisstore_lettuce_adaptor.rst:4,20,41,48`・`ja/biz_samples/12/index.rst:4,8,59,87`に、本ページと同じ`=`→`-`→`~`→`^`の4階層の前例がある。一方、行頭太字の疑似見出しは`ja/application_framework/application_framework/libraries/`配下に0件だった | 要 | — | 7箇所を`^`のL4見出しに格上げし、`style.md`S-04にL4（`^`）を追加（根拠2件）（STEP 3） |
| D-4 | 2 | D | decide→対応 | `about/index.rst`（第1部・特徴3点目）の`:ref:`が`テストデータ変換ツール`のみで、`design.md`L74「本ページ作成後に見直すことを検討する」が未着手だった件 | 要 | — | ユーザー判断（2026-08-06）により`#9`是正に同梱。`about/index.rst`に`:ref:`テストデータの書き方\ <testdata_notation>`\`を追加（既存の`テストデータ変換ツール`参照は維持）し、`design.md`L74を実施済みの結論に書き換えた（STEP 4） |
| A-4 | 2 | A | must | `requestParams`・`responseResult`をtestShotsのカラムとして表に掲載していたが誤りだった。`AbstractHttpRequestTestTemplate.java:74,77`で定数として宣言され、`:336-339`で`getCachedListMap(sheetName, REQUEST_PARAMS_LIST_MAP)`のようにリテラルのままLIST_MAPのIDとして使われており、`getValue(testCaseParams, ...)`を経由するtestShotsカラムではない（対照として`context`は`:334-335`で`getValue`経由であり正真正銘のカラム）。誤りの由来は`TestCaseInfo.java:333-338`のJavadocの記載が実コードと一致していないためとみられる。ラウンド1の観点Aは出典間の突合のみを行い実装を確認していなかったため検出できなかった | 要 | — | `requestParams`・`responseResult`の行をカラム表から削除し、両者が読み込み単位内に置く予約IDを持つ`LIST_MAP`である旨を地の文に明記（STEP 1(c)） |
| A-5 | 2 | A | must | `expectedSearch`の説明が、検索結果をリクエストスコープから取得する際の既定キー`searchResult`を欠落していた。出典`current-0081`（削除前の`05_UnitTestGuide/02_RequestUnitTest/index.rst:99-193`）に記載があり、実装`TestCaseInfo.java:72`の`DEFAULT_SEARCH_RESULT_KEY = "searchResult"`、`setSearchResultKey`（`TestCaseInfo.java:123-125`）で変更可能なことも確認した | 要 | — | `expectedSearch`行の説明に既定キー`searchResult`である旨（`setSearchResultKey`で変更可能な旨を含む）を追記（STEP 2） |

### ラウンド2終了時点のまとめ

- `must`: A-3（確定）・B-F01（確定）・A-4・A-5、全て解消
- `decide`: D-4、ユーザー判断（2026-08-06）により`#9`是正に同梱、対応済み
- 本ラウンドで新規に検出した`note`はない。ラウンド1の`note`（D-3・D-5）は本書の対象外であり蒸し返さない
- Dockerフルビルド（`-a`）で`build succeeded, 1 warning`（既知の`db_double_submit.rst`のみ、本タスクによる新規警告は0件）を確認

## ラウンド3（`/rn:gm`による通し読み改善指示への対応）

`/rn:gm`「ここまでのFBを踏まえてページ全体を見直し、意味のある改善をする」を受け、著者自身によるページ全体の通し読みを実施。個別指摘への対症療法ではなく、独立した再読で見つけた欠陥を対象とする。

| 指摘ID | 区分 | 指摘内容 | 対応内容 |
|---|---|---|---|
| R3-1 | must | 「準備データ（SETUP_TABLE）を記述する」「期待値（EXPECTED_TABLE等）を記述する」「カラムを省略する」の3節にまたがり、「主キーカラムは省略できない」「省略カラムはデフォルト値扱い」の同じ事実が3回反復されていた | 「カラムを省略する」節の該当段落を、既出事実の反復から前2節への`前述のとおり`参照＋デフォルト値表への`次の表`参照に書き換え、反復を解消 |
| R3-2 | must | 「カラムを省略する」節冒頭のimportantが「データベースの検索結果の期待値」「登録系テスト」の両方に「カラムを省略できない」という同一の強さの表現を使っていたが、実装（`nablarch-testing`の`Assertion#assertMapEquals`、`actualAsString.equals(expected)`によるMap完全一致）を確認したところ、前者（`expectedSearch`等の`LIST_MAP`比較）のみが機械的な制約であり、後者（登録系テストの全カラム確認）は`EXPECTED_TABLE`が技術的には省略を許すベストプラクティス上の推奨であることが判明。同じ強さの表現では技術的制約と推奨が区別できず、読者が実際には存在しないバリデーションを想定しうる | `LIST_MAP`を名指しし:ref:リンクを追加のうえ機械的制約である理由（Map完全一致）を明記。登録系テストの記述は「推奨する。〜のためである」という本セッションの既定の言い回し（意図ベース）に書き換え、両者の性質の違いを明示 |
| R3-3 | must（ラウンド1 D-3の未対応分） | ラウンド1のD-3で記録のみとされていた「ウェブアプリのカラム表に`expectedStatusCode`が共通カラム表と重複掲載」を、本ラウンドで解消（他の処理方式の表に同種の重複がなく、通し読みで改めて冗長と判断） | ウェブアプリケーション用カラム表から`expectedStatusCode`の行を削除（共通カラム表の記載のみ残す） |

### ラウンド3終了時点のまとめ

- `must`: R3-1・R3-2・R3-3、全て解消
- `decide`・`note`の新規検出なし
- Dockerフルビルド（クリーン、`rm -rf _build`後再実行）で`build succeeded, 1 warning`（既知の`db_double_submit.rst`のみ、新規警告0件）を確認
