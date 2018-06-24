# Makefile to generate streamline-cli binaries

# Build/version information
NAME    :=$(shell basename `git rev-parse --show-toplevel`)
RELEASE :=$(shell git rev-parse --verify --short HEAD)
VERSION  = 0.0.3
BUILD    = $(VERSION)-$(RELEASE)
LDFLAGS  = "-X main.buildVersion=$(BUILD)"

build: 
	docker build -t rsalmond/${NAME}:latest . --build-arg tag=${VERSION}

push:
	docker push rsalmond/${NAME}:latest

