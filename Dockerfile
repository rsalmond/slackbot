FROM alpine:latest

ARG tag

ADD ./slackbot/requirements.txt /slackbot/requirements.txt

RUN apk update && apk add python3 python3-dev gcc libc-dev tzdata \
  && pip3 install setuptools --upgrade \
  && pip3 install -r /slackbot/requirements.txt \
  && echo "WILL_SLACKBOT_VERSION=${tag}" > /slackbot/version.py

ADD ./slackbot /slackbot
