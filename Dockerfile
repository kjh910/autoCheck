FROM --platform=linux/amd64 python:3

ADD requirements.txt /home/
ENV PORT=80

RUN set -x && \
  apt-get update && \
  apt-get install -y vim && \
  pip install -r /home/requirements.txt

WORKDIR /app
COPY ./app/ /app/

RUN wget http://ftp.mozilla.org/pub/firefox/releases/87.0/linux-x86_64/ja/firefox-87.0.tar.bz2
RUN tar xvf firefox-87.0.tar.bz2 
RUN mv firefox /opt/
RUN ln -s /opt/firefox/firefox /usr/bin/firefox
RUN apt-get install -y xvfb
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz
RUN tar xzf geckodriver-v0.30.0-linux64.tar.gz
RUN mv geckodriver /usr/bin/geckodriver
RUN apt-get -y install firefox-esr


RUN chmod 777 /app/runserver.sh
EXPOSE 80
EXPOSE 9224

CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --timeout 500 

