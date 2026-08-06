# NTF解説書 トンマナ規約

## 1. 適用範囲と file:line の基準

本書は、`design.md`「7. トンマナ」が定めた8観点について、FW解説書のライブラリ
（`ja/application_framework/application_framework/libraries/`、以下 `FW:`）から
記述の調子を抽出し、ページ作成時にCCが従う基準として定めたものである。

`FW:` の行番号の基準は作業ツリーである（`mapping/glossary.md` §1 と同じ記号体系）。

本書の役割は「ページ作成時にCCが従う基準」であり、網羅性を追求する対象ではない。
観点は次の9つに限定する（S-01〜S-08は`#4`確定時点の8観点、S-09は2026-08-06、
`/rn:gm`フィードバック「FW解説書のようにNTF解説書の各ページの先頭に目次を入れる」を
受けて追加）。文の長さ・改行位置・図の配置・括弧の全角半角・英数字と日本語の間の空白・
送り仮名や漢字/かなの揺れなど、機械判定できない規則性は対象外とし、本書には記載しない。

## 2. 規約一覧

### S-01 文体（だ・である調）

**規約**: 本文はである調（常体）で書く。「〜である。」「〜する。」「〜行う。」で文を終える。
「です・ます」調は使わない。

**根拠**:

- `FW:libraries/exclusive_control.rst:10` 「この機能では、データベースのデータ更新に対する排他制御を行う。」
- `FW:libraries/exclusive_control.rst:18` 「この機能は、以下の理由により **非推奨** である。」
- `FW:libraries/static_data_cache.rst:8` 「データベースやファイルなどに格納した静的データへのアクセスを高速化するためのキャッシュ機能を提供する。」
- `FW:libraries/session_store.rst:169` 「テーブル名およびカラム名は変更可能である。」

「です・ます」調が使われている箇所は、確認した範囲（`exclusive_control.rst`、`date.rst`、
`session_store.rst`）で1件も見つからなかった。

### S-02 ページのセクション構成

**規約**:

- 第2部のページは「機能概要 → 使用方法 → 拡張例」の順に並べる。
- 第3部のページは「機能概要 → 使用方法」の順に並べる（拡張例の見出しは置かない）。
- 第2部・第3部のいずれのページにも「モジュール一覧」の見出しは置かない。依存関係（モジュール一覧）は
  第1部「テスティングフレームワークとは」の「稼動環境」セクション1箇所に集約する。

この構成は `design.md` の第2部ページアウトライン（`design.md:76-88`）、第3部ページアウトライン
（`design.md:132-141`）の決定に基づく。

FW解説書のライブラリ（`ja/application_framework/application_framework/libraries/`）の一般的なページは
「機能概要 → モジュール一覧 → 使用方法 → 拡張例」の4セクション構成である（下記「根拠（セクションの
並び順）」参照）。しかしNTF解説書はこの型をそのまま採用しない。`design.md` の「モジュール一覧の集約」節
（`design.md:48-52`）は、依存関係（`nablarch-testing`、`nablarch-testing-junit5`、JUnit関連等）を
第1部「稼動環境」（`design.md:34`）に集約し、**処理方式ごとのページには置かない**と明示的に決めている
（`design.md:50` 「依存関係（…）は本ページの「稼動環境」に集約する。処理方式ごとのページには置かない。」）。
そのため第2部・第3部のページには「モジュール一覧」の見出し自体を置かない。処理方式固有の依存がある
場合のみ、当該ページの「機能概要」または「使用方法」配下で個別に触れる（`design.md:52`）。

拡張できる内容が無い機能（第2部のみ。第3部には「拡張例」の見出し自体を置かない。
`design.md:143` 「拡張例は第3部に置かない。」）では「拡張例」を次のいずれかの方法で扱う。

- 見出し自体を置かない
- 見出しは置き、本文に「なし。」とだけ書く

**根拠**（design.mdの決定）:

- `design.md:76-88` 第2部ページのアウトライン。機能概要→使用方法→拡張例の3セクションで、モジュール一覧を含まない。
- `design.md:132-141` 第3部ページのアウトライン。機能概要→使用方法の2セクションのみで、モジュール一覧・拡張例のいずれも含まない。
- `design.md:143` 「拡張例は第3部に置かない。拡張はコンポーネント設定とクラス差し替えであり、アーキテクトの領域のため第2部に置く。」
- `design.md:48-52` 「モジュール一覧の集約」節。依存関係は第1部「稼動環境」に集約し、処理方式ごとのページには置かないと明示。
- `design.md:34` 第1部「稼動環境」セクションに「モジュール一覧（依存関係）」を記載する旨の記述。

**根拠**（セクションの並び順。FW解説書ライブラリの一般的な型の実例。NTF解説書はこのうち
「モジュール一覧」を除いた並び順のみを踏襲する）:

- `FW:libraries/exclusive_control.rst:29,71,90,403` 「機能概要」→「モジュール一覧」→「使用方法」→「拡張例」の順。
- `FW:libraries/date.rst:10,23,38,138` 同順。
- `FW:libraries/session_store.rst:43,72,98,371` 同順。
- `FW:libraries/transaction.rst:11,25,39,150` 同順。

**根拠**（拡張例の省略）:

- `FW:libraries/exclusive_control.rst:403-405` 「拡張例」の見出しの直後に「なし。」とだけ書かれている。
- `FW:libraries/service_availability.rst:112-114` 同様に「拡張例」の直後に「なし。」とだけ書かれている。
- `FW:libraries/code.rst`、`FW:libraries/format.rst`、`FW:libraries/static_data_cache.rst`、
  `FW:libraries/db_double_submit.rst`、`FW:libraries/file_path_management.rst` は「拡張例」の見出し自体が無い
  （`grep -n "^拡張例$"` で該当なし）。

### S-03 セクションタイトルの形式（「〜する」形式）

**規約**: 「使用方法」「拡張例」配下の小見出しは、動詞終止形の「〜する」で終える。
読者が見出しから目的の操作に直接辿り着けるようにする。

**根拠**:

- `FW:libraries/exclusive_control.rst:95` 「排他制御を使うために準備する」
- `FW:libraries/exclusive_control.rst:154` 「楽観的ロックを行う」
- `FW:libraries/exclusive_control.rst:381` 「悲観的ロックを行う」
- `FW:libraries/date.rst:143` 「システム日時を切り替える」（拡張例配下）
- `FW:libraries/date.rst:152` 「業務日付を切り替える」（拡張例配下）
- `FW:libraries/service_availability.rst` の「使用方法」配下 「サービス提供可否をチェックする」
  「サービス提供可否に応じて画面表示を制御する」

なお「機能概要」配下の小見出しは「〜できる」（能力を示す形。例: `FW:libraries/exclusive_control.rst:32`
「楽観的ロック/悲観的ロックができる」、`FW:libraries/static_data_cache.rst:20` 「任意のデータをキャッシュできる」）
や体言止めが使われており、必ずしも「〜する」形式ではない。「〜する」形式を適用するのは
「使用方法」「拡張例」配下の小見出しとする。

**追加規約（内容の条件、`#6`確定）**: 「〜する」形式は見出しの形式にすぎず、それだけでは
中身の一意性・可読性を保証しない。上記の形式規約に、以下の内容条件を加える。

- **ページタイトルとセクションタイトルの組で一意であり、かつその組だけで中身が分かること。**
  利用者は見出しを見て目的の情報に辿り着く。加えて Nabledge がセクションタイトルであたりを
  付けるため、タイトルが検索面そのものになる
- セクションタイトル単独での文書全体一意は不要。ページタイトルが処理方式名等を持つため、
  組で一意になる（`vocabulary.md` の確定34ページはすべて一意であることを確認済み）
- 「〜する」形式でも、`概要` / `補足` / `注意事項` / `その他` / `準備する` / `設定する` の
  ように、ページタイトルを足しても情報が増えない語は不可
- 同一ページ内でセクションタイトルを重複させない
- 出典の見出し（`目的別API使用方法` のような作成側の都合による名前）をそのまま使わない

### S-04 見出しのアンダーライン記法とレベル対応

**規約**: 見出しのアンダーライン記号とレベルの対応は次のとおりとする。

| レベル | 記号 | 用途 |
|---|---|---|
| L1（ページタイトル） | `=` | ページ全体のタイトル1つのみ |
| L2（機能概要/モジュール一覧/使用方法/拡張例） | `-` | 4つの大セクション |
| L3（個別項目） | `~` | 大セクション配下の個別の見出し |
| L4（L3のさらに下の細分） | `^` | L3配下をさらに細分する見出し。用例が薄いページでのみ使う |

長さはタイトル文字列と同じ長さ以上にする（アンダーラインがタイトルより短いとRST構文エラーになるため）。

**根拠**:

- `FW:libraries/exclusive_control.rst:3-4` ページタイトル「排他制御」の下に `=` の下線（69文字）。
- `FW:libraries/exclusive_control.rst:29-30,71-72,90-91,403-404` 「機能概要」「モジュール一覧」「使用方法」「拡張例」の
  下にいずれも `-` の下線。
- `FW:libraries/exclusive_control.rst:32-33,95-96,154-155` 「楽観的ロック/悲観的ロックができる」「排他制御を使うために準備する」
  「楽観的ロックを行う」の下にいずれも `~` の下線。
- `FW:libraries/date.rst:2,11,14,24,39,44` も同じ対応（`=`→L1、`-`→L2、`~`→L3）。

**根拠（L4、`^`）**: `FW:libraries/` 配下では確認できなかったが、`ja/` 配下全体では `^` を4階層目として
使う `.rst` が存在する。うち `=`→`-`→`~`→`^` の4階層を本書と同じ順序で使っている例は次の2件。

- `ja/application_framework/adaptors/lettuce_adaptor/redisstore_lettuce_adaptor.rst:4,20,41,48` 「コンポーネント設定ファイルを修正する」（`:47-48`）。
- `ja/biz_samples/12/index.rst:4,8,59,87` 「インタフェース」（`:85-87`、上下線とも `^`）。

### S-05 コードブロックのインデント幅と言語指定

**規約**: `.. code-block::` の内容は、ディレクティブ自身の行より2字下げる（ネストしている場合も、
そのディレクティブの開始位置からの相対で2字下げ）。言語指定は実際の内容に応じて `xml` / `java` /
`sql` / `html` / `properties` / `bash` などを個別に付ける（無指定の `code-block::` のみは使わない）。

**根拠**:

- `FW:libraries/exclusive_control.rst:73-75` `.. code-block:: xml` （0字下げ）の内容が2字下げの
  `  <dependency>` から始まる。
- `FW:libraries/exclusive_control.rst:99-100,102-104` 定義リスト項目内で1字下げの
  `.. code-block:: xml` の内容が3字下げ（相対2字下げ）の `  <!-- ... -->` から始まる。
- `FW:libraries/exclusive_control.rst:115-123` は `code-block:: sql`、`FW:libraries/exclusive_control.rst:252-267` は
  `code-block:: html` を使用。同一ファイル内で内容に応じて言語指定を使い分けている。
- 言語指定はコーパス全体（`FW:libraries/*.rst`）で `xml`（78件）、`java`（78件）、`jsp`（68件）、
  `properties`（24件）、`bash`（19件）、`html`（11件）、`sql`（2件）などが使われている
  （`grep -n "^ *\.\. code-block::"` で集計）。

### S-06 アドミニション（tip / note / important）の使い分け

**規約**: 「important」は、無視すると不具合・非推奨機能の誤用・データ不整合につながる、
読者が必ず守るべき注意事項に使う。「tip」は、読まなくても機能は正しく使えるが、
知っておくと役立つ補足情報（背景・小技・バージョン情報など）に使う。「note」は
FW解説書のライブラリでは使用例が見つからなかったため、本解説書でも積極的には使わない。

**根拠**（important = 必須の注意事項）:

- `FW:libraries/exclusive_control.rst:17-19` 非推奨機能である旨と代替手段を示す警告。
- `FW:libraries/exclusive_control.rst:207-209` 「バージョン番号のチェックを行わなければ、画面間でバージョン番号が引き継がれない。」
- `FW:libraries/static_data_cache.rst:12-15` 「大量のデータをキャッシュした場合、Full GCが頻発しパフォーマンスに悪影響を与える可能性があるので、注意すること。」
- `FW:libraries/session_store.rst:27-32` 「本機能を使用する場合、以下の機能は用途が重複するため非推奨となる。」

**根拠**（tip = 補足情報）:

- `FW:libraries/exclusive_control.rst:54-62` 排他制御用テーブルの単位の決め方についての実務的な補足。
- `FW:libraries/exclusive_control.rst:346-349` カスタムタグを使うともっと簡単に扱えるという補足と `:ref:` 誘導。
- `FW:libraries/session_store.rst:34-35` 「本機能で使用するクッキー(`NABLARCH_SID`)は、HTTPセッションの追跡に使用されるJSESSIONIDとは全く別物である。」
- `FW:libraries/session_store.rst:37-38` 「Nablarch 5u16より、セッションストアの有効期間保存先にHTTPセッション以外も選べるようになった。」（バージョン情報の補足）

**根拠**（noteの不使用）:

- `FW:libraries/*.rst` 全体を `grep -rn "^\s*\.\. note::"` で検索した結果、該当なし（0件）。

### S-07 表の記法

**規約**: 2〜3列程度の短い説明表は simple table（`====` の区切り線）を使う。
セル内に複数行の説明や `:ref:` を含む長文が入る表は `list-table` を使い、`:widths:` で列幅を指定する。
grid table（`+---+` 形式）は使わない。

**根拠**（simple table）:

- `FW:libraries/date.rst:64-67` 業務日付管理テーブルのレイアウトを2列の simple table で記載。
- `FW:libraries/code.rst:14-19` 性別区分の例を3列（値・名称・略称）の simple table で記載。
- `FW:libraries/service_availability.rst:63-66`、`FW:libraries/session_store.rst:287-292` も同形式。

**根拠**（list-table）:

- `FW:libraries/mail.rst:111-114` 「メール送信要求」の表を `.. list-table::` に `:widths: 24,18,58` を付けて記載。
  各セルには `:ref:` を含む長文の説明が入る（`FW:libraries/mail.rst:121` 参照）。
- `FW:libraries/mail.rst:153,171,192,542` 他4箇所も同じ `list-table` + `:widths:` の形式。
- `FW:libraries/log.rst`、`FW:libraries/format.rst`、`FW:libraries/utility.rst` でも `list-table` を使用
  （`grep -c "list-table::"` でそれぞれ7件・1件・1件）。

**根拠**（grid tableの不使用）:

- `FW:libraries/*.rst` 全体を `grep -n '^+-'` で検索した結果、grid table の罫線（`+---+`）は見つからなかった。

### S-08 `:ref:` ラベルの命名規則

**規約**: ページ先頭のラベルはページIDそのもの（英語のスネークケース）を使う
（例: `exclusive_control`）。ページ内の個別セクションのラベルは
`<ページID>-<セクションの内容を表す英語スネークケース>` の形式にする。
バッククォートで囲む書き方（`` `label` ``）と囲まない書き方の両方が見られるが、
ラベル名の構造自体はどちらも同じである。

**根拠**:

- `FW:libraries/exclusive_control.rst:1` ページ先頭ラベル `.. _exclusive_control:`
- `FW:libraries/exclusive_control.rst:15,93,152,237,379` セクションラベル
  `exclusive_control-deprecated`、`exclusive_control-optimistic_setting`、
  `exclusive_control-optimistic_lock`、`exclusive_control-optimistic_lock-bulk`、
  `exclusive_control-pessimistic_lock`。
- `FW:libraries/date.rst:41,57,141,150` セクションラベル `date-system_time_settings`、
  `date-business_date_settings`、`date-system_time_change`、`date-business_date_change`。
- `FW:libraries/session_store.rst:1,61,87,101` ページ先頭ラベルは `` .. _`session_store`: ``
  （バッククォート付き）、セクションラベルは `session_store-serialize`、`session_store-constraint`、
  `session_store-use_config`。

### S-09 各ページ先頭の目次（`.. contents::` ディレクティブ）

**規約**: 複数のL2セクション（「機能概要」「使用方法」等、`-` の下線）を持つページは、
ページタイトルの下線の直後（本文・イントロ段落より前）に次の3行を置く。

```
.. contents:: 目次
  :depth: 3
  :local:
```

ページ先頭にラベル（`.. _xxx:`）がある場合は、ラベル→タイトル→目次の順とする。

**適用しないページ**: `.. toctree::` のみで構成され、L2セクション（`-` の下線）を
1つも持たないランディング/インデックスページ（NTF解説書では
`index.rst`・`setup/index.rst`・`implementation/index.rst`・`tools/index.rst`が該当）。
`:local:` はページ内のセクション見出しにのみリンクするため、セクションを持たない
ページに置いても空の目次になり意味がない。

**根拠**:

- `FW:libraries/exclusive_control.rst:1-8`、`FW:libraries/date.rst:1-6`、
  `FW:libraries/session_store.rst:1-8`、`FW:libraries/mail.rst:1-6` など、
  L2セクションを持つページ143件中138件で、タイトル下線の直後（本文より前）に
  同一の3行（`.. contents:: 目次` / `:depth: 3` / `:local:`）を確認した
  （`grep -rl "contents::" ja/application_framework/application_framework/libraries/`
  と `grep -n "contents::"` の行番号がタイトル下線の直後であることを実測）。
- 例外5件（`data_converter.rst`・`database_management.rst`・`permission_check.rst`・
  `validation.rst`・`index.rst`）はいずれも `.. toctree::` のみで構成され、
  L2セクション（`-` の下線）を1つも持たない（`grep -c "^-\{5,\}$"` で0件を確認）。

**由来**: 2026-08-06、ユーザーから `/rn:gm` で「FW解説書のようにNTF解説書の
各ページの先頭に目次を入れることにしませんか？」とフィードバックを受け追加。

## 3. 検証していない事項

本書は9観点（S-09は2026-08-06追加）に限定して作成した。文の長さ、改行位置、図の配置、
括弧の全角半角、英数字と日本語の間の空白、送り仮名・漢字/かなの揺れなど、他の規則性に
気づいた場合でも本書には記載しない（`design.md`「8. トンマナ」および本タスクの作業指示による）。
