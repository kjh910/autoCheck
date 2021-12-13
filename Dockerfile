FROM python:3

ADD requirements.txt /home/

# vimとseleniumをインストール
RUN set -x && \
  apt-get update && \
  apt-get install -y vim && \
  pip install -r /home/requirements.txt

EXPOSE 9223
