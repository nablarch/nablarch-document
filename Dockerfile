FROM python:3.8.18-slim

RUN apt-get update

# Sphinxのセットアップ
RUN pip install --upgrade pip && pip install  \
    setuptools==57.5.0 \
    jinja2==3.0.3 \
    Sphinx==1.6.3 \
    javasphinx==0.9.15 \
    sphinx-rtd-theme==0.2.4 \
    docutils-ast-writer==0.1.2

# textlintのセットアップ
RUN curl -sL https://deb.nodesource.com/setup_20.x | bash -
RUN apt-get install -y nodejs npm
COPY package*.json /root/
WORKDIR /root
RUN npm install && npm audit fix
