# 本Dockerfileは2つの独立したステージで構成される。
#
#   lint ステージ : textlint実行環境 (Python 3.10 + Node.js 22)
#   docs ステージ : HTML生成・linkcheck環境 (Python 3.12 + Sphinx 9)
#
# HTML生成に使う docutils と、textlint-plugin-rst が依存する
# docutils-ast-writer(rst2ast) の要求する docutils のバージョンが両立
# しないため、環境を分離している。docs ステージが最終ステージのため、
# `docker build` はデフォルトで docs 環境のイメージを生成する。
# lint 環境は `docker build --target lint` で生成する(README参照)。

# ---------------------------------------------------------------------------
# lint ステージ: textlint実行環境
# ---------------------------------------------------------------------------
# docutils-ast-writer==0.1.2 の setup.py は use_2to3 を使用しており、
# setuptools 58 以降では拒否されるため、setuptools を 57.5.0 に固定し、
# ビルド分離(build isolation)を無効化してこの setuptools でインストール
# する。use_2to3 は lib2to3 を用いるため Python 3.11 まで、かつ旧
# setuptools は distutils を用いるため Python 3.11 までしか動作しない。
# 以上より、本ステージの Python は 3.10 系が上限である。
FROM python:3.10.20-slim AS lint

WORKDIR /root

COPY requirements-lint.txt /root/
COPY package*.json /root/
COPY patches /root/patches/

RUN pip install --no-cache-dir setuptools==57.5.0 wheel \
    && pip install --no-cache-dir --no-build-isolation -r requirements-lint.txt

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

# ---------------------------------------------------------------------------
# docs ステージ: HTML生成・linkcheck環境 (デフォルトターゲット)
# ---------------------------------------------------------------------------
# Sphinx 9.1 は Python 3.12 以上を要求する。requirements.txt は
# requirements.in から pip-compile で生成した lock ファイルであり、
# 全依存を固定してビルドの再現性を担保する。
FROM python:3.12-slim AS docs

WORKDIR /root

COPY requirements.txt /root/

RUN pip install --no-cache-dir -r requirements.txt
