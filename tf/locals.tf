locals {
  config = jsondecode("${file("../config.json")}")
  prefix = local.config.application_namespace
  region = data.aws_region.current.name
}

data "aws_region" "current" {}
data "aws_caller_identity" "current" {}
