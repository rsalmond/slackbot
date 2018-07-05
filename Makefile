# Build/version information
NAME    :=$(shell basename `git rev-parse --show-toplevel`)
RELEASE :=$(shell git rev-parse --verify --short HEAD)
VERSION  = 0.0.6
BUILD    = $(VERSION)-$(RELEASE)
LDFLAGS  = "-X main.buildVersion=$(BUILD)"

build: 
	docker build -t rsalmond/${NAME}:${VERSION} . --build-arg tag=${VERSION} --cache-from rsalmond/${NAME}:latest

push:
	docker push rsalmond/${NAME}:${VERSION}
	docker tag rsalmond/${NAME}:${VERSION} rsalmond/${NAME}:latest
	docker push rsalmond/${NAME}:latest
