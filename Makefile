ifeq ($(OS),Windows_NT)
    PWD = /$(shell pwd)
endif

build:
	docker build -t nginx_log .

dev: build
	docker run --rm -it -v $(PWD):/src/app nginx_log bash

test_build:
	docker build --build-arg TEST_MODE=True -t nginx_log:test .

test: test_build
	docker run --rm -v $(PWD):/src/app nginx_log:test pypy3 -m pytest tests