#!/bin/bash

function log() {
	printf "$(date): $1\n"
}

DEPLOY=$(kubectl get deploy --selector=app=slackbot -o json | jq '.items[].metadata.name' -r)

log "Updating deploy: ${DEPLOY}"

MSG=$(kubectl patch deployment ${DEPLOY} -p  "{\"spec\":{\"template\":{\"metadata\":{\"labels\":{\"date\":\"$(date +'%s')\"}}}}}")

log "${MSG}"
