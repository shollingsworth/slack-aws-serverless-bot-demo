#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Configuration
"""
import json
import os

from aws_lambda_powertools.logging import Logger
import boto3
from botocore.exceptions import UnauthorizedSSOTokenError

NAMESPACE = os.environ["NAMESPACE"]
logger = Logger(service=NAMESPACE)

SSM_NAME=f"/{NAMESPACE}/secrets.json"
ENV_SLASH_COMMAND = os.environ["SLACK_COMMAND"]
SLACK_SLASH_COMMAND = f"/{ENV_SLASH_COMMAND}"

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
DEBUG = os.environ["DEBUG"] == "true"
BUCKET = os.environ["BUCKET"]
MOCK = os.environ.get("MOCK") == "true"


def _get_jdata():
    return (
        boto3.Session()
        .client("ssm")
        .get_parameter(
            Name=SSM_NAME, WithDecryption=True
        )["Parameter"]["Value"]
    )

try:
    _SECRET_DATA = json.loads(_get_jdata())
except UnauthorizedSSOTokenError as err:
    raise SystemExit("Unauthorized SSO token, please re-authenticate") from err


SLACK_APP_ID = _SECRET_DATA["SLACK_APP_ID"]
SLACK_CLIENT_SECRET = _SECRET_DATA["SLACK_CLIENT_SECRET"]
SLACK_CLIENT_ID = _SECRET_DATA["SLACK_CLIENT_ID"]
SLACK_SIGNING_SECRET = _SECRET_DATA["SLACK_SIGNING_SECRET"]
SLACK_EXCEPTIONS_WEBHOOK = _SECRET_DATA["SLACK_EXCEPTIONS_WEBHOOK"]
SLACK_BOT_TOKEN = _SECRET_DATA["SLACK_BOT_TOKEN"]
SLACK_WEBHOOK = _SECRET_DATA["SLACK_WEBHOOK"]
