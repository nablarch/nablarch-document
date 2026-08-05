FROM python:3.10.20-slim

WORKDIR /root

COPY requirements.txt /root/
COPY package*.json /root/
COPY patches /root/patches/

# Sphinxのセットアップ
#
# docutils-ast-writer==0.1.2 の setup.py は use_2to3 を使用しており、
# setuptools 58 以降では拒否されるため、setuptools を 57.5.0 に固定し、
# ビルド分離(build isolation)を無効化してこの setuptools でインストール
# する。use_2to3 は lib2to3 を用いるため Python 3.11 まで、かつ旧
# setuptools は distutils を用いるため Python 3.11 までしか動作しない。
# さらに Sphinx==1.3.6 は Python 3.11 の正規表現仕様変更(全域フラグの
# 先頭以外への記述がエラー化)により起動できない。以上より、本イメージの
# Python はツールチェーンを更新しない限り 3.10 系が上限である。
RUN pip install --no-cache-dir setuptools==57.5.0 wheel \
    && pip install --no-cache-dir --no-build-isolation -r requirements.txt

# Python 3.10 で削除された標準ライブラリ parser モジュールの互換シム。
#
# Sphinx 1.3.6 (sphinx/highlighting.py) は、言語指定のないコードブロックを
# ハイライトする前に parser.suite() で「有効な Python コードか」を判定し、
# 無効なら着色なし(none)へフォールバックする。parser モジュールが存在
# しないと全ブロックが Python と見なされ、非 Python のブロックが誤って
# トークン着色される(ビルド成果物が変わる)。compile() で同等の構文判定を
# 提供し、Python 3.8/3.9 時代と同じハイライト判定を維持する。
RUN SITE_DIR=$(python -c "import site; print(site.getsitepackages()[0])") \
    && printf '%s\n' \
       '"""Py3.10+ compat shim for the removed stdlib parser module."""' \
       '' \
       '' \
       'def suite(source):' \
       '    try:' \
       '        return compile(source, "<string>", "exec")' \
       '    except SyntaxError:' \
       '        raise' \
       '    except ValueError as exc:' \
       '        raise SyntaxError(str(exc))' \
       > "$SITE_DIR/parser.py"

# textlintのセットアップ
#
# ベースの slim イメージには curl が含まれないため明示的にインストール
# する(curl が無いまま `curl ... | bash` を実行するとパイプ全体が成功扱い
# となり、NodeSource リポジトリ未登録のまま Debian 標準の古い nodejs が
# 入ってしまう)。セットアップスクリプトは一旦ファイルへ保存してから
# 実行し、ダウンロード失敗を確実にビルド失敗として検知する。
# NodeSource の nodejs パッケージには npm が同梱されるため、npm を別途
# インストールする必要はない。
RUN apt-get update \
    && apt-get install -y curl ca-certificates --no-install-recommends \
    && curl -fsSL https://deb.nodesource.com/setup_22.x -o /tmp/nodesource_setup.sh \
    && bash /tmp/nodesource_setup.sh \
    && apt-get install -y nodejs --no-install-recommends \
    && rm /tmp/nodesource_setup.sh \
    && apt-get clean

# package-lock.json で依存バージョンを固定し、npm ci による再現性のある
# インストールを行う。これにより脆弱性データベースの更新時期に左右されず、
# 同一の依存ツリーで常に同じ結果を得られる。
#
# npm audit（脆弱性監査）はビルドの合否判定に含めない方針とする。
# 脆弱性状況を確認したい場合は `npm audit` を情報表示として別途実行する
# こと。
RUN npm ci
