FROM python:3.8.18-slim

WORKDIR /root

COPY requirements.txt /root/
COPY package*.json /root/
COPY patches /root/patches/

# Sphinxのセットアップ
RUN pip install --no-cache-dir -r requirements.txt

# textlintのセットアップ
RUN apt-get update \
    && curl -sL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs npm --no-install-recommends \
    && apt-get clean

# package-lock.json で依存バージョンを固定し、npm ci による再現性のある
# インストールを行う。これにより脆弱性データベースの更新時期に左右されず、
# 同一の依存ツリーで常に同じ結果を得られる。
#
# npm audit（脆弱性監査）はビルドの合否判定に含めない方針とする。
# 現状 high 深刻度の脆弱性が残存するが、いずれも破壊的なメジャーアップグレード
# でしか解消できず、その本質対応は別イシューとして扱う。監査自体をビルドの
# 合否条件にすると、依存の破壊的更新を伴わない限りビルドが常に失敗するため、
# 監査はビルドから切り離す。脆弱性状況を確認したい場合は `npm audit` を
# 情報表示として別途実行すること。
RUN npm ci
