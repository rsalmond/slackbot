FROM alpine:latest

ADD ./slackbot/requirements.txt /slackbot/requirements.txt

RUN apk update && apk add python3 python3-dev gcc libc-dev \
  && pip3 install setuptools --upgrade \
  && pip3 install -r /slackbot/requirements.txt

ADD ./slackbot /slackbot
