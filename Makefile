.DEFAULT_GOAL := help
.EXPORT_ALL_VARIABLES:
UID = $(shell id -u)
REGION = us-east-2
PROJECT_NAME = $(shell basename $(PWD))
PREFIX = $(shell jq -r '.application_namespace' < config.json)

help:
	@echo "Available commands:"
	@echo
	@cat Makefile | grep '^\w.*:$$' | cut -d ':' -f 1 | grep -v '^help$$'

list:
	cd backend/ && serverless deploy list functions --stage production --region ${REGION}

serverless_output:
	aws cloudformation describe-stacks --stack-name ${PREFIX}-backend --query Stacks[0].Outputs | \
 	jq '. |  map({(.OutputKey) : (.OutputValue)}) | add' | tee serverless.json

logs:
	cd backend/ && serverless logs --stage production --region ${REGION} \
		--function web -t --startTime 20m

destroy:
	cd backend/ && serverless remove \
		--stage production --region ${REGION}

diff:
	cd backend/ && serverless diff \
	--stage production --region ${REGION}

print:
	cd backend/ && serverless print --stage production --region ${REGION} --verbose

deploy_only_serverless:
	cd backend/  && \
	serverless deploy --stage production --region ${REGION} --verbose

deploy_all: backend_layer deploy_only_serverless

gen_slack_manifest: serverless_output
	./bin/gen_slack_manifest.sh > slack/manifest.yaml

build_image:
		docker-compose \
		-p ${PROJECT_NAME} \
		--profile build \
		--file ./localdev/docker-compose.yaml up \
		--build

backend_layer: build_image
	docker-compose \
		-p ${PROJECT_NAME} \
		--profile layer \
		--file ./localdev/docker-compose.yaml up \
		--force-recreate \
		layer

local: build_image
	docker-compose \
		-p ${PROJECT_NAME} \
		--profile local \
		--file ./localdev/docker-compose.yaml up \
		--remove-orphans
