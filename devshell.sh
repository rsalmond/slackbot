#!/bin/bash

docker exec -it $( docker ps | grep slackbot | cut -d ' ' -f1) sh
