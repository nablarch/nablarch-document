FROM python:3.8.18-slim

WORKDIR /root

COPY requirements.txt /root/
COPY package*.json /root/

# Sphinxのセットアップ
RUN pip install --no-cache-dir -r requirements.txt

# textlintのセットアップ
RUN apt-get update \
    && curl -sL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs npm --no-install-recommends \
    && apt-get clean

RUN npm install && npm audit fix
