# Path Related
MKFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
MKFILE_DIR := $(dir $(MKFILE_PATH))
DIST_DIR := ${MKFILE_DIR}build/dist

# Rules
.PHONY: build
build: build_server

.PHONY: build_server
build_server:
	@ CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -a -ldflags "-s -w" -o server ./cmd/main.go


.PHONY: test
test:
	cd ${MKFILE_DIR}
	go test -v ./...

.PHONY: serve
serve:
	cd ${MKFILE_DIR}
	gow -v -s \
		run -trimpath ${MKFILE_DIR}

.PHONY: mod_update
mod_update:
	cd ${MKFILE_DIR} && go get -u -v ./...

.PHONY: clean
clean:
	rm -rf ${DIST_DIR}/*


dev:
	go run cmd/main.go

server:
	@ CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -a -ldflags "-s -w" -o contains lyric/main.go

.PHONY: contains
contains:
	@CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -a -ldflags "-s -w" -o contains lyric/main.go && scp contains ciroy@10.0.2.73:/home/ciroy/Downloads
