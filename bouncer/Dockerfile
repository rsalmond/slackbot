FROM alpine:latest

RUN apk update && apk add jq curl bash && \
    curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl && \
    mv kubectl /usr/local/bin/ && \
    chmod +x /usr/local/bin/kubectl

ADD ./bouncer.sh /bouncer.sh

CMD ["bash", "/bouncer.sh"]
