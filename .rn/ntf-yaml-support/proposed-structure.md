# NTF 解説書 新構成案

## 設計の背景

現状の解説書は以下の問題を抱えている:

1. **「テストデータの書き方」が10本以上に散在** — `01_Abstract.rst` に全体仕様、各処理方式（batch/real/send_sync 等）にも個別仕様が書かれており、開発者が「どこを読めばわかるか」が不明
2. **アーキテクト向けと開発者向けの混在** — アーキテクトガイド（`06_TestFWGuide/`）に開発者が日常参照する内容（testShots・特殊記法・Tips）が埋まっている
3. **testShots 仕様が10本以上に重複記述** — 処理方式別ファイルにそれぞれ独立して解説されており、横断的な仕様としてまとめた場所がない
4. **YAML 対応後の入口がない** — 「どちらの形式を使うか」「何が変わるか」を利用者が判断する場所がない

本設計はこれらをゼロベースで解消し、Excel/YAML 両対応の構成に組み直す。

---

## 読者ターゲットの定義

| 読者 | 関心事 | 使うタイミング |
|---|---|---|
| **アーキテクト** | FW の仕組み・テストクラス基盤の設定・プロジェクトへの導入方針 | プロジェクト立ち上げ時・テスト基盤設計時 |
| **アプリ開発者** | テストデータの書き方・テストクラスの実装手順・よくある使い方の例 | テスト実装時（日常的に参照） |

---

## 新構成ツリー

タイトルはアプリケーションフレームワーク側（「ウェブアプリケーション編」「Nablarchバッチアプリケーション」等）と同じパターンに揃える。読者の誘導はタイトルではなく index.rst の本文で行う。

```
テスティングフレームワーク（index.rst）
│  ※本文で「FW の概要・設定はXXを、テスト実装はXXを参照」と誘導
│
├── Nablarchテスティングフレームワークとは    ★タイトル確定★
│   │  ※アーキテクト向け。FW の仕組み・設定・導入
│   │  ※アプリケーションFW側の architecture + application_design に相当
│   │
│   ├── A-1. テスティングフレームワーク概要
│   │       FW の特徴・制約・クラス構成・処理フロー
│   │       ※現: 01_Abstract.rst の前半（特徴・FW構成表）
│   │
│   ├── A-2. テストクラスの設定
│   │   ├── A-2-1. データベースを使用するクラスのテスト（DbAccessTestSupport）
│   │   ├── A-2-2. リクエスト単体テスト用クラス（Web/REST/バッチ）
│   │   └── A-2-3. リクエスト単体テスト用クラス（メッセージング各種）
│   │       ※現: 06_TestFWGuide/02_*.rst の「クラス構成・設定」部分
│   │
│   ├── A-3. テストデータの形式                ★新規★
│   │       Excel / YAML の違い・どちらを使うか・プロジェクト統一方針
│   │
│   ├── A-4. JUnit 5用拡張機能
│   │       ※現: JUnit5_Extension.rst そのまま
│   │
│   ├── A-5. マスタデータ復旧機能
│   │       ※現: 04_MasterDataRestore.rst そのまま
│   │
│   └── A-6. テストツール
│           ※現: 08_TestTools/ そのまま
│
└── テストの実装方法                           ★タイトル確定★
    │  ※開発者向け。テストコードの書き方・テストデータの作り方
    │  ※アプリケーションFW側の feature_details に相当
    │  ※現行「単体テスト実施方法」から「テストの実装方法」に変更
    │
    ├── B-1. テストデータの記述方法             ★最大の変更点・1ページ★
    │       テストデータの構造・データブロック種別・testShots・
    │       テーブルデータ・ファイルデータ・メッセージング・値の記述方法
    │       ※現在10本以上に散在 → 1ページに集約。長くてもスクロールで通読できる
    │       ※主素材: input/ntf-testdata-doc.md 全章（§1〜10）
    │
    ├── B-2. テストデータの記述例               ★新規・1ページ★
    │       Excel / YAML 対比例を一覧。仕様を調べるなら B-1、写して使うなら B-2
    │       ※主素材: input/ntf-testdata-doc-examples-*.md 6本をまとめる
    │       　- 全体像・groupId の例
    │       　- testShots（処理方式別カラム仕様）の例
    │       　- テーブルデータの例
    │       　- ファイルデータの例
    │       　- メッセージングデータの例
    │       　- 特殊値・ディレクティブ・ヘッダ/コメント の例
    │
    ├── B-3. クラス単体テストの実装方法
    │       ※現: 05_UnitTestGuide/01_ClassUnitTest/ ほぼそのまま
    │       ※「テストデータの書き方」節 → B-1 参照に置換
    │
    ├── B-4. リクエスト単体テストの実装方法
    │   ├── ウェブアプリケーション
    │   ├── RESTful ウェブサービス
    │   ├── バッチ処理
    │   ├── メッセージング（同期応答受信 / 応答不要受信 / HTTP 同期応答受信）
    │   ├── メッセージング（同期応答送信 / 応答不要送信 / HTTP 同期応答送信）
    │   └── その他（ファイルアップロード / メール / 2重送信防止）
    │       ※現: 05_UnitTestGuide/02_RequestUnitTest/
    │       ※各ページの「テストデータの書き方」節 → B-1 参照に置換
    │
    ├── B-5. 取引単体テストの実装方法
    │       ※現: 05_UnitTestGuide/03_DealUnitTest/ ほぼそのまま
    │       ※「テストデータの書き方」節 → B-1 参照に置換
    │
    └── B-6. 目的別API使用方法
            ※現: 06_TestFWGuide/03_Tips.rst → 開発者向けに移動
            ※Excel 固有表現をテストデータファイル表現に修正
```

### タイトル確定の根拠

| タイトル | 根拠 |
|---|---|
| `Nablarchテスティングフレームワークとは` | 「Nablarchバッチアプリケーション」「ウェブアプリケーション編」と同じく **「何のFWか」を先頭に置く** パターン。「〜とは」でFW概要ページであることを明示 |
| `テスティングフレームワーク概要` | FW側の配下ページは「アーキテクチャ概要」のように **FW名を繰り返さない**。「自動」は「テスティングフレームワーク」から自明なため不要 |
| `テストの実装方法` | 内容が「テストコードを書く・テストデータを作る」という**実装行為**。「実施」はテストを走らせるQAプロセスのニュアンスで内容とズレがある。現行の「単体テスト実施方法」を正す機会 |

---

## 設計の核心：B-1「テストデータの書き方」の独立

### なぜ独立させるか

現状では開発者が「testShots に何を書くか」「SETUP_TABLE の構造は？」を調べるたびに複数ファイルを横断する必要がある。B-1 を独立させることで:

- **一か所に来れば全部わかる** — データブロック種別・特殊記法・値の型・ディレクティブが揃う
- **Excel / YAML を並列で説明できる** — `ntf-testdata-doc.md` の構成がそのまま活きる
- **各処理方式ページがすっきりする** — 「テストケースの追加は B-1-3 を参照」で済む

### B-1 の構成イメージ（ntf-testdata-doc.md を主素材）

| B-1 節 | 内容 | 主素材 |
|---|---|---|
| B-1-1 全体像 | Excel=1ブック/1シート、YAML=1ディレクトリ/1ファイル の対応関係 | ntf-testdata-doc.md §1〜2 |
| B-1-2 データブロック種別 | 14種の一覧・識別方法・Excel vs YAML キー対応表 | ntf-testdata-doc.md §3 |
| B-1-3 testShots | testShots の定義・処理方式別カラム仕様・groupId | ntf-testdata-doc.md §4 + examples-testshots.md |
| B-1-4 テーブルデータ | SETUP_TABLE / EXPECTED_TABLE / LIST_MAP | ntf-testdata-doc.md §5 + examples-table.md |
| B-1-5 ファイルデータ | 固定長・可変長・ディレクティブ | ntf-testdata-doc.md §6・9 + examples-file.md |
| B-1-6 メッセージング | MESSAGE / EXPECTED_REQUEST_* / RESPONSE_* | ntf-testdata-doc.md §7 + examples-messaging.md |
| B-1-7 値の書き方 | null/空文字/日付/${systemTime} 等・Excel vs YAML 対比 | ntf-testdata-doc.md §8・10 + examples-special.md |

### B-1 記述例のイメージ（Excel / YAML 並列）

各節の末尾に「記述例」として Excel 表と YAML コードブロックを並べて掲載する。
現場ですぐ写して使えることを目標とする。

```
テーブルへの準備データ（SETUP_TABLE）の例
==========================================

.. tab:: Excel

   .. list-table::
      :header-rows: 1

      * - SETUP_TABLE=ORDER_HEADER
        - ORDER_ID
        - ITEM_COUNT
      * -
        - 10001
        - 10

.. tab:: YAML

   .. code-block:: yaml

      setup_tables:
        - table: ORDER_HEADER
          rows:
            - ORDER_ID: "10001"
              ITEM_COUNT: "10"
```

※タブ切り替えの対応状況次第では「Excel の場合」「YAML の場合」の見出し分けでも可

---

## 新旧マッピング表（品質担保用）

既存ファイルの内容が新構成のどこに移るかを示す。この表をもとに「漏れなし」を確認する。

| # | 既存ファイル | 内容カテゴリ | 新構成の移動先 | 処理方針 |
|---|---|---|---|---|
| 1 | `06_TestFWGuide/01_Abstract.rst` § 特徴・構成表 | FW の仕組み | **A-1** | 抜粋・移動 |
| 2 | `06_TestFWGuide/01_Abstract.rst` § 命名規約・データタイプ一覧・特殊記法・注意事項 | テストデータ仕様 | **B-1**（Excel+YAML対応に拡充）、記述例は **B-2** | 集約・拡充 |
| 3 | `06_TestFWGuide/02_DbAccessTest.rst` § クラス構成・仕組み説明 | テストクラス基盤 | **A-2-1** | 抜粋・移動 |
| 4 | `06_TestFWGuide/02_DbAccessTest.rst` § API 使い方・記述例 | テスト実装方法 | **B-2** に残置 or 参照化 | 検討 |
| 5 | `06_TestFWGuide/02_RequestUnitTest.rst` | リクエスト単体テスト基盤 | **A-2-2** | 移動 |
| 6 | `06_TestFWGuide/RequestUnitTest_batch.rst` | バッチ用クラス設定 | **A-2-2** | 移動 |
| 7 | `06_TestFWGuide/RequestUnitTest_rest.rst` | REST 用クラス設定 | **A-2-2** | 移動 |
| 8 | `06_TestFWGuide/RequestUnitTest_real.rst` | メッセージング受信用クラス設定 | **A-2-3** | 移動 |
| 9 | `06_TestFWGuide/RequestUnitTest_send_sync.rst` | メッセージング送信用クラス設定 | **A-2-3** | 移動 |
| 10 | `06_TestFWGuide/RequestUnitTest_http_send_sync.rst` | HTTP 送信差分説明 | **A-2-3** | 移動 |
| 11 | `06_TestFWGuide/03_Tips.rst` | 目的別 API / Tips | **B-5** | 開発者向けに移動、Excel→テストデータファイル表現に修正 |
| 12 | `06_TestFWGuide/04_MasterDataRestore.rst` | マスタデータ復旧 | **A-5** | そのまま移動 |
| 13 | `06_TestFWGuide/JUnit5_Extension.rst` | JUnit 5 拡張 | **A-4** | そのまま移動 |
| 14 | `05_UnitTestGuide/01_ClassUnitTest/index.rst` | クラス単体テスト概要 | **B-3** | そのまま |
| 15 | `05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/01_*.rst` | エンティティ単体テスト（Bean Validation） | **B-3** | テストデータの書き方 → B-1 参照に |
| 16 | `05_UnitTestGuide/01_ClassUnitTest/01_entityUnitTest/02_*.rst` | エンティティ単体テスト（Nablarch Validation） | **B-3** | テストデータの書き方 → B-1 参照に |
| 17 | `05_UnitTestGuide/01_ClassUnitTest/02_componentUnitTest.rst` | コンポーネント単体テスト | **B-3** | テストデータの書き方 → B-1 参照に、命名規約 → B-1 参照に |
| 18 | `05_UnitTestGuide/02_RequestUnitTest/index.rst` | リクエスト単体テスト概要 | **B-4** | そのまま |
| 19 | `05_UnitTestGuide/02_RequestUnitTest/batch.rst` | バッチリクエスト単体テスト実装手順 | **B-4** | 「テストデータの書き方」節 → B-1 参照に |
| 20 | `05_UnitTestGuide/02_RequestUnitTest/rest.rst` | REST リクエスト単体テスト実装手順 | **B-4** | 「テストデータの書き方」節 → B-1 参照に |
| 21 | `05_UnitTestGuide/02_RequestUnitTest/real.rst` | 同期応答受信 実装手順 | **B-4** | 「テストデータの書き方」節 → B-1 参照に |
| 22 | `05_UnitTestGuide/02_RequestUnitTest/http_real.rst` | HTTP 同期応答受信 実装手順 | **B-4** | 「テストデータの書き方」節 → B-1 参照に |
| 23 | `05_UnitTestGuide/02_RequestUnitTest/send_sync.rst` | 同期応答送信 実装手順 | **B-4** | 「テストデータの書き方」節 → B-1 参照に |
| 24 | `05_UnitTestGuide/02_RequestUnitTest/delayed_send.rst` | 応答不要送信 実装手順 | **B-4** | 参照先へ委譲のため軽微 |
| 25 | `05_UnitTestGuide/02_RequestUnitTest/delayed_receive.rst` | 応答不要受信 実装手順 | **B-4** | 参照先へ委譲のため軽微 |
| 26 | `05_UnitTestGuide/02_RequestUnitTest/http_send_sync.rst` | HTTP 同期応答送信 実装手順 | **B-4** | 「テストデータの書き方」節 → B-1 参照に |
| 27 | `05_UnitTestGuide/02_RequestUnitTest/mail.rst` | メール送信テスト 実装手順 | **B-4** | 軽微修正 |
| 28 | `05_UnitTestGuide/02_RequestUnitTest/fileupload.rst` | ファイルアップロードテスト 実装手順 | **B-4** | 軽微修正 |
| 29 | `05_UnitTestGuide/02_RequestUnitTest/double_transmission.rst` | 2重送信防止テスト 実装手順 | **B-4** | 変更なし |
| 30 | `05_UnitTestGuide/03_DealUnitTest/batch.rst` | バッチ業務単体テスト 実装手順 | **B-5** | 「テストデータの書き方」節 → B-1 参照に |
| 31 | `05_UnitTestGuide/03_DealUnitTest/send_sync.rst` | 同期応答送信 業務単体テスト | **B-5** | 「テストデータの書き方」節 → B-1 参照に |
| 32 | `05_UnitTestGuide/03_DealUnitTest/http_send_sync.rst` | HTTP 同期応答送信 業務単体テスト | **B-5** | 「テストデータの書き方」節 → B-1 参照に |
| 33 | `05_UnitTestGuide/03_DealUnitTest/real.rst` | 同期応答受信 業務単体テスト | **B-5** | そのまま |
| 34 | `05_UnitTestGuide/03_DealUnitTest/rest.rst` | REST 業務単体テスト | **B-5** | そのまま |
| 35 | `05_UnitTestGuide/03_DealUnitTest/delayed_send.rst` | 応答不要送信 業務単体テスト | **B-5** | そのまま（参照のみ） |
| 36 | `05_UnitTestGuide/03_DealUnitTest/delayed_receive.rst` | 応答不要受信 業務単体テスト | **B-5** | そのまま（参照のみ） |
| 37 | `08_TestTools/01_HttpDumpTool/` | HTTP dump ツール | **A-6** | そのまま |
| 38 | `08_TestTools/02_MasterDataSetup/` | マスタデータセットアップツール | **A-6** | そのまま |
| 39 | `08_TestTools/03_HtmlCheckTool/` | HTML チェックツール | **A-6** | そのまま |
| ★ | *(新規)* | テストデータの形式（Excel / YAML） | **A-3** | 新規作成 |
| ★ | *(新規、ntf-testdata-doc.md 主素材)* | テストデータの記述方法（仕様リファレンス） | **B-1** | ntf-testdata-doc.md を RST 化、1ページ |
| ★ | *(新規、examples 6本 主素材)* | テストデータの記述例（Excel/YAML 対比） | **B-2** | examples 6本をまとめて RST 化、1ページ |

---

## input/ 資料と新構成の対応

| input/ ファイル | 内容 | 使う/使わない | 用途 |
|---|---|---|---|
| `ntf-testdata-doc.md` | テストデータ仕様リファレンス全体（Excel/YAML 両対応） | **使う** | B-1 全体の主素材 |
| `ntf-testdata-doc-examples-overview.md` | 全体像・groupId の記述例 | **使う** | B-1-1 に掲載 |
| `ntf-testdata-doc-examples-testshots.md` | 処理方式別 testShots カラム仕様と記述例 | **使う** | B-1-3 に掲載 |
| `ntf-testdata-doc-examples-table.md` | テーブルデータの Excel/YAML 記述例 | **使う** | B-1-4 に掲載 |
| `ntf-testdata-doc-examples-file.md` | ファイルデータの Excel/YAML 記述例 | **使う** | B-1-5 に掲載 |
| `ntf-testdata-doc-examples-messaging.md` | メッセージングデータの Excel/YAML 記述例 | **使う** | B-1-6 に掲載 |
| `ntf-testdata-doc-examples-special.md` | 特殊値・ディレクティブ・ヘッダ/コメント の Excel/YAML 記述例 | **使う** | B-1-7 に掲載 |
| `ntf-doc-terms.md` | 用語リファレンス（既存解説書からの用語引き表） | **使う（間接）** | ページには掲載しない。執筆時の用語統一チェックに使用 |
| `ntf-testdata-loading.md` | FW 内部の読み込み機構（4段階変換・クラス設計） | **使わない** | 利用者向けコンテンツの素材にならない内部設計書 |
| `testdata-converter-design.md` | Excel/YAML 変換ツール設計書 | **使わない** | 利用者向けコンテンツの素材にならない内部設計書 |

---

## 品質担保チェックリスト

実装時にこのリストを使って漏れなく作業する。

### Phase 1: 新構成への移行確認

- [ ] 新旧マッピング表の全39項目（＋新規2項目）が新構成に存在するか確認
- [ ] 既存 RST の toctree 参照が全て有効か（`make html` でエラーなし）
- [ ] 既存の内部リンク（`:ref:` ラベル）が移動後も有効か
- [ ] `05_UnitTestGuide/` と `06_TestFWGuide/` 間のクロス参照が壊れていないか

### Phase 2: B-1 コンテンツ品質

- [ ] ntf-testdata-doc.md の全章（§1〜10）が B-1 に対応する節を持つか
- [ ] 全 example ファイル（6本）の記述例が B-1 に掲載されているか
- [ ] Excel 記述例と YAML 記述例が全節に揃っているか（片方だけになっていないか）
- [ ] testShots カラム仕様が処理方式ごとに揃っているか（examples-testshots.md の内容をカバー）

### Phase 3: 用語・トンマナ

- [ ] `ntf-doc-terms.md` の用語（データタイプ、グループ ID、testShots 等）が統一されているか
- [ ] 「Excelファイル」→「テストデータファイル」への置換が B-1 を除く全ページで完了しているか
- [ ] Excel 固有の用語（シート・セル・罫線）が単独で使われていないか（常に「Excel の場合」として限定されているか）

### Phase 4: ビルド確認

- [ ] `make html` がエラーなし
- [ ] 生成された HTML で A 章・B 章が index から正しくリンクされているか
- [ ] B-1 の各節間のリンクが有効か

---

## 設計上の判断（全て提案）

### 判断1: ディレクトリ構造 — 既存パスを活かす

**提案**: 既存の `05_UnitTestGuide/` と `06_TestFWGuide/` のディレクトリ構造は維持し、toctree の構成だけ組み替える。

**理由**: 公開 URL が変わると外部からのリンクが全て切れる。コンテンツの整理が目的であり、ファイルパスの変更はリスクの割にメリットがない。ディレクトリ名の意味（`05_` `06_`）が薄れるが、利用者が見るのは HTML のタイトルであり、ファイルパスは開発者だけが気にする。

**具体的な進め方**:
- B-1（テストデータの書き方）の新規ファイルは `06_TestFWGuide/` 直下に追加
- A-5（マスタデータ復旧）などは現在地のまま、toctree の親だけ A 章側に付け替える
- 削除・移動は行わず「toctree の並べ替えと新規ファイル追加」だけで完結させる

---

### 判断2: B-1 のファイル分割 — 節単位で7ファイルに分割する

**提案**: B-1-1〜B-1-7 を独立した RST ファイルとして7本作成し、B-1 の index.rst がそれらを toctree でまとめる構成にする。

**理由**: `ntf-testdata-doc.md`（約380行）に example ファイル6本を加えると RST 化で 1,500行以上になる見込み。1ファイルにすると読み込みが重い・節内リンクが複雑になる・レビューしにくい。節単位で分割すれば「SETUP_TABLE の書き方だけ見たい」というユースケースに直接 URL が当たる。

**ファイル構成案**:

```
06_TestFWGuide/
  testdata/
    index.rst          ← B-1 の入口、全節の toctree
    overview.rst       ← B-1-1 全体像とファイル構造
    data-blocks.rst    ← B-1-2 データブロック種別一覧
    testshots.rst      ← B-1-3 testShots・処理方式別カラム仕様
    table-data.rst     ← B-1-4 テーブルデータ
    file-data.rst      ← B-1-5 ファイルデータ（固定長・可変長）
    messaging.rst      ← B-1-6 メッセージングデータ
    values.rst         ← B-1-7 値の書き方・特殊記法
```

---

### 判断3: Excel/YAML の並列表示 — タブ切り替えは使わない、見出し分けを採用する

**結論: タブ切り替えは現在のこのリポジトリでは使えない。**

調査結果:
- `sphinx-tabs` 拡張は `requirements.txt` に含まれておらず、インストールされていない
- `conf.py` の `extensions` リストにも未登録
- 既存ページで `.. tabs::` や `.. tab::` を使っているページは1つもない

`sphinx-tabs` を新たに導入することは可能だが、Sphinx 1.8.6（現在使用中）との互換性確認・requirements.txt への追加・既存テーマ（sphinx-rtd-theme 0.2.4）との表示確認が必要になり、リスクが工数に見合わない。

**採用する代替案: 「Excelの場合」「YAMLの場合」の小見出し分け**

各記述例を以下の形式で掲載する。縦に並べるため視覚的な切り替えはないが、コピーして使う用途では十分実用的であり、既存の RST 記法だけで実現できる。

```rst
SETUP_TABLE の記述例
--------------------

**Excelの場合**

.. list-table::
   :header-rows: 1
   :widths: 30 20 20

   * - SETUP_TABLE=ORDER_HEADER
     - ORDER_ID
     - ITEM_COUNT
   * -
     - 10001
     - 10

**YAMLの場合**

.. code-block:: yaml

   setup_tables:
     - table: ORDER_HEADER
       rows:
         - ORDER_ID: "10001"
           ITEM_COUNT: "10"
```

この形式はすでに `.. tip::` や `.. note::` を使っているページと同じスタイルで書けるため、トンマナが壊れない。

---

### 判断4: `02_DbAccessTest.rst` の扱い — ファイル分割は行わず、参照リンクで対応

**提案**: `02_DbAccessTest.rst` はファイル分割せず現在地に置いたままとする。アーキテクト向けセクション（クラス構成・仕組み）と開発者向けセクション（API の使い方）が混在している状態は、当該ファイルの冒頭に「テストデータの書き方は :ref:`testdata_reference` を参照」という誘導を追加することで解消する。

**理由**: ファイルを分割すると `make html` を通す・既存の相互参照を全部張り直す・URL が変わるという3つのコストが発生する。一方、利用者の実害（アーキテクト向けページに開発者向け内容がある）は誘導リンク1本で解消できる。完全な整理は将来の大規模リファクタリング時の課題として先送りする。
