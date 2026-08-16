# 作業依頼: テストデータ変換ツールの往復変換で起きる事象2件の仕様判定と対応

宛先: `nablarch-testing-converter` の担当

## 0. この依頼の位置づけ

NTF解説書（`nablarch/nablarch-document` の `ntf-yaml-support` ブランチ）を全面的に作り直している。その過程で、テストデータ変換ツールに2つの事象を確認した。**解説書にどう書くかがこの判定に依存する**ため、判定をいただきたい。

**この依頼は「不具合を直してください」ではない。** まず**NTF仕様として、この挙動が意図されたものかどうかを判定していただきたい**。仕様であれば、そう判定していただければそれでよい（解説書側に仕様として書く）。不具合であれば、§4 の方針で対応をお願いしたい。

依頼者はテストデータ変換ツールの設計意図を知らない。以下はすべて**実行して観測した事実**であって、正誤の判断を含まない。

**急ぎではない。** YAML対応も解説書の刷新もいずれも開発中で、まだリリースしない。利用者はいないため、期限より**判定の正しさを優先していただきたい**。

## 1. 検証環境

| 項目 | 値 |
| --- | --- |
| リポジトリ | `nablarch-testing-converter` |
| コミット | `45194f9`（`docs(coverage): レビュー指摘を台帳へ反映し、実測と食い違う数値を直す`） |
| JDK | Temurin 21.0.11+10 |
| 準備 | `mvn -o -DskipTests test-compile dependency:build-classpath -Dmdep.outputFile=cp.txt` |
| 入力データ | 同梱の `src/test/resources/nablarch/test/tool/converter/xls/reference/ProjectActionRequestTest.xlsx` |

再現に使ったドライバは §5 に全文を載せた。`target/classes` と `cp.txt` をクラスパスに置けばそのまま動く。

---

## 2. 事象1: XLS → YAML → XLS → YAML の往復で内容が変わる

### 2-1. 観測した事実

同梱の `ProjectActionRequestTest.xlsx` を起点に

```
XLS(元) → YAML(1回目) → XLS → YAML(2回目)
```

を実行し、**YAML(1回目) と YAML(2回目) を比較した**（どちらも同じ書き出し器が生成した YAML なので、整形の違いは入らない）。

結果は次のとおり。

| 指標 | 値 |
| --- | --- |
| 出力ファイル数 | 26（1回目・2回目とも同数） |
| 内容が異なるファイル | **22 / 26** |
| 総行数 | 1回目 **1,352行** → 2回目 **1,425行** |
| 削除された行 | 19 |
| 追加された行 | 92 |

変化は3種類に分かれた。

**(a) 全カラムの値が空文字の行が、行ごと消える**

`confirmOfCreateAbNormal.yaml` の `requestParams` ブロック。

```yaml
# YAML(1回目)
  - id: "requestParams"
    rows:
      - form.projectName: ""
        form.projectType: ""
        form.projectClass: ""
        form.clientId: ""

# YAML(2回目)
  - id: "requestParams"
    rows: []
```

同種の変化が6ファイルで起きている（`rows:` が `rows: []` になる）。

**(b) 空の行（`- {}`）が増える**

削除された `- {}` が5行、追加された `- {}` が84行。たとえば `updateNormal.yaml` の `requestParams` は `- {}` が1行から2行に増えた。

**(c) 行が0件のテーブルが、直後のテーブルを取り込む**

`setUpDb.yaml` の `setup_tables`。

```yaml
# YAML(1回目)
  - table: "PROJECT"
    rows: []
  - table: "INDUSTRY"
    rows:
      - INDUSTRY_CODE: "01"
        INDUSTRY_NAME: "農業"
  - table: "CLIENT"
    ...

# YAML(2回目)
  - table: "PROJECT"
    rows:
      - SETUP_TABLE=INDUSTRY: "INDUSTRY_CODE"
      - SETUP_TABLE=INDUSTRY: "01"
  - table: "CLIENT"
    ...
```

`INDUSTRY` テーブルの定義そのものが消え、そのヘッダ行とデータ行が `PROJECT` テーブルの行として、`SETUP_TABLE=INDUSTRY` というカラム名で取り込まれている。`INDUSTRY_NAME` の値 `農業` は失われている。

### 2-2. 判定していただきたいこと

1. **(a) は仕様か。** 全カラムが空文字の行を「データ無し」とみなして落とすことが、NTFのテストデータとして正しい扱いか。リクエストパラメータのキーだけを送る（値は空）というテストケースが表現できなくなるが、それが意図した割り切りか
2. **(b) は仕様か。** `- {}` の件数が往復で増えることに、NTF仕様上の意味があるか
3. **(c) は仕様か。** 行0件のテーブルの直後にあるテーブルが取り込まれる挙動が意図されたものか

`RoundTripTest.java` の Javadoc は「可逆性の対象外」として Excel の色・書式・結合セル・コメント、YAML のコメント、および Excel 経路の `null` → 文字列 `"null"` を挙げている。**上の3つはいずれもそこに挙がっていない**が、これが記載漏れなのか、そもそも往復の保証範囲外なのかを含めて判定していただきたい。

### 2-3. 参考: 入力データ側にも1点ある

変換の実行時に次の警告が出た。

```
警告: [ProjectActionRequestTest] シート "updateNormal" のブロック "testShots" に
      重複カラム名 "expectedTable" があります。10 列目の値を採用します。
```

これは同梱のサンプル `.xlsx` 側にカラム名の重複があることを示している。事象1とは別件だが、同梱データを直すべきかどうかもあわせて判定いただきたい。

---

## 3. 事象2: 同名で拡張子違いの Excel ブックが同居すると、片方の変換結果が無言で失われる

### 3-1. 観測した事実

入力ディレクトリに `Foo.xls` と `Foo.xlsx` を置き（中身は別物）、XLS → YAML を実行した。

```
converted files=2
```

2件とも変換対象になり、**2件とも同じ出力ディレクトリ `out/Foo/` に書き出された**。結果として辞書順で後に処理された側が先の側を上書きし、出力に残ったのは片方だけだった（出力の総行数から、後勝ちした側を特定できた）。

**警告もエラーも出ない。** 利用者は片方の変換結果が失われたことに気づけない。

関係すると思われる箇所を挙げる（コードを読んだだけで、意図は確認していない）。

- `ConverterFileFilter.java:29` — `XLS_EXTENSIONS = {".xls", ".xlsx"}` として両方を変換対象にしている
- `XlsFormatHandler.java:34` — `ConverterPathResolver.stripExtension(...)` でブック名から拡張子を落としている
- `XlsFormatHandler.java:46` 付近 — `resolveOutputBase` が拡張子を含まないブック名で出力先を決めている

### 3-2. 判定していただきたいこと

1. **同名で拡張子違いの Excel ブックの同居を、NTFは想定しているか。** 想定外（利用者側の運用ミス）と整理するのか、ツールが検出すべきものか
2. 想定外と整理する場合、**無言で上書きしてよいか。** それとも検出してエラーにすべきか

---

## 4. 不具合と判定した場合の対応方針

**テスト駆動で対応をお願いしたい。** 手順は次のとおり。

1. **先に、失敗する再現テストを書く。** 事象1は §2-1 の3種類それぞれについて、事象2は §3-1 の同居ケースについて、期待する挙動をアサートするテストを追加する。この時点でテストが**失敗すること**を確認し、テストだけをコミットする（コミットメッセージに「再現テストを追加する」旨を書く）
2. **実装を直す。** 直したうえで、1のテストが通ることを確認する
3. **既存テストが壊れていないことを確認する。** `RoundTripTest.java` を含む全テストを実行する
4. **`RoundTripTest.java` の Javadoc の「可逆性の対象外」の記述を、判定結果に合わせて更新する**

事象1の(a)(b)(c)は原因が別々である可能性がある。**同じコミットにまとめず、事象ごとに再現テスト → 修正の単位で進めていただきたい。**

## 5. 再現用ドライバ

`RT.java`（事象1）。`src/test/java` には置かず、任意の場所でコンパイルして実行した。

```java
import java.nio.file.*;
import nablarch.test.tool.converter.*;

public class RT {
    public static void main(String[] a) throws Exception {
        Path src = Paths.get(a[0]);   // 入力の .xlsx
        Path work = Paths.get(a[1]);  // 作業ディレクトリ
        Path in = work.resolve("in"), mid = work.resolve("mid"), out = work.resolve("out");
        Files.createDirectories(in); Files.createDirectories(mid); Files.createDirectories(out);
        Files.copy(src, in.resolve(src.getFileName().toString()), StandardCopyOption.REPLACE_EXISTING);
        TestDataConverter.convert(new ConversionRequest.Builder()
            .sourceFormat(DataFormat.XLS).targetFormat(DataFormat.YAML)
            .inputPath(in).outputPath(mid).overwrite(true).build());
        TestDataConverter.convert(new ConversionRequest.Builder()
            .sourceFormat(DataFormat.YAML).targetFormat(DataFormat.XLS)
            .inputPath(mid).outputPath(out).overwrite(true).build());
        TestDataConverter.convert(new ConversionRequest.Builder()
            .sourceFormat(DataFormat.XLS).targetFormat(DataFormat.YAML)
            .inputPath(out).outputPath(work.resolve("mid2")).overwrite(true).build());
    }
}
```

実行後に `diff -ru <work>/mid <work>/mid2` で比較した。

事象2は、`in` に `Foo.xls` と `Foo.xlsx` を置いて XLS → YAML を1回実行し、出力ディレクトリの中身を数えた。

## 6. 回答していただきたい形式

事象ごとに次を返していただきたい。

- **判定**: 仕様 / 不具合 / 判断保留（保留の場合は何が決まれば判定できるか）
- **仕様と判定した場合**: そう言える根拠（設計文書・コード上の意図・Javadoc など）。解説書にそのまま書けるだけの説明があると助かる
- **不具合と判定した場合**: 対応する版と、おおよその見込み時期

解説書側は、**判定が出るまで該当箇所に TODO を残し、不具合が直る前提で本文を書く**方針で進める。仕様と判定された場合は本文を仕様に合わせて書き直すので、その旨をお知らせいただきたい。

## 7. 禁止事項

- 依頼者は不具合と断定していない。**まず仕様かどうかを判定すること**
- 判定より先に実装を直さないこと
- 再現テストを書く前に実装を直さないこと
