.DEFAULT_GOAL := help
Stackname := example-apigateway-websocket
Id := `id -F`
S3Bucket := $(Stackname)-$(Id)
OutputTemplateFile := sam-output.yaml

## Create bucket
bucket:
	aws s3 mb s3://$(S3Bucket)

## Build
build:
	sam build

## Package
package:
	aws cloudformation package \
		--template-file .aws-sam/build/template.yaml \
		--s3-bucket $(S3Bucket) \
		--output-template-file $(OutputTemplateFile)

## Deploy
deploy:
	aws cloudformation deploy \
		--template-file $(OutputTemplateFile) \
		--stack-name $(Stackname) \
		--capabilities CAPABILITY_IAM \
		--no-fail-on-empty-changeset

## Create changesets
changesets:
	aws cloudformation deploy \
		--template-file $(OutputTemplateFile) \
		--stack-name $(Stackname) \
		--capabilities CAPABILITY_IAM \
		--no-fail-on-empty-changeset \
		--no-execute-changeset

## Show help
help:
	@make2help $(MAKEFILE_LIST)

.PHONY: help
.SILENT:
