ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
CPL_ENV_FILE?=""
ifneq ($(CPL_ENV_FILE), "")
DOCKER_ENV_PARAM=--env-file "$(CPL_ENV_FILE)"
endif

build:
	docker build -t cpl-manager .
run: build
	docker run -d $(DOCKER_ENV_PARAM) -p 0.0.0.0:8080:80 -v "$(ROOT_DIR)/app/database:/opt/cpl-manager/database" --name cpl-manager cpl-manager
clean:
	docker stop -t 1 cpl-manager
	docker rm cpl-manager
update: clean build run
