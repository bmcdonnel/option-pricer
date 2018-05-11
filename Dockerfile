FROM python:3.6.5-stretch

RUN apt-get update -qq && \
    apt-get install -y postgresql-client-9.6

COPY requirements.txt /tmp/
WORKDIR /tmp
RUN pip install -r requirements.txt

ENV APP_HOME=/home/option_pricer
WORKDIR $APP_HOME
ADD . $APP_HOME

COPY entrypoint_web.sh /usr/local/bin/
COPY entrypoint_worker.sh /usr/local/bin/
