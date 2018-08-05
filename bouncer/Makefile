# Build/version information
NAME     = "bouncer"
RELEASE :=$(shell git rev-parse --verify --short HEAD)
VERSION  = 0.0.1
BUILD    = $(VERSION)-$(RELEASE)

build: 
	docker pull rsalmond/${NAME}:latest
	docker build -t rsalmond/${NAME}:${VERSION} . --cache-from rsalmond/${NAME}:latest

push:
	docker push rsalmond/${NAME}:${VERSION}
	docker tag rsalmond/${NAME}:${VERSION} rsalmond/${NAME}:latest
	docker push rsalmond/${NAME}:latest
