# slackbot

A bot to do dumb things in the slack(s) I idle in.


## Developing

Local dev env is built on docker compose. To get hacking clone the repo and run `docker-compose up`, you can then exec into the running container to run the bot `python3 /slackbot/run_will.py` and iterate on code in the `/slackbot` directory using your favourite editor outside the container.

See [this blog post](https://rob.salmond.ca/developing-in-docker/) for a walkthrough of this pattern.

## Deploying

To upgrade slackbot @message him: `@<slackbot> upgrade`. He will pull the latest [container from dockerhub](https://hub.docker.com/r/rsalmond/slackbot/).
