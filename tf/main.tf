provider "aws" {
  region = "us-east-2"
  default_tags {
    tags = local.config.default_tags
  }
}

# uncomment this for production
# terraform {
#   backend "s3" {
#     bucket = "<YOUR_ORG_TF_BUCKET>-terraform-state"
#     key    = "slackbot-demo"
#   }
# }
