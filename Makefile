# Build/version information
NAME    :=$(shell basename `git rev-parse --show-toplevel`)
RELEASE :=$(shell git rev-parse --verify --short HEAD)
VERSION  = 0.0.4
BUILD    = $(VERSION)-$(RELEASE)
LDFLAGS  = "-X main.buildVersion=$(BUILD)"

build: 
	docker build -t rsalmond/${NAME}:${VERSION} . --build-arg tag=${VERSION}

push:
	docker push rsalmond/${NAME}:${VERSION}

