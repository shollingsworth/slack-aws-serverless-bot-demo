#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S3 lib."""
import json
import time

from aws_lambda_powertools.logging import Logger
import boto3
from api import config
from mypy_boto3_s3.service_resource import Bucket

LOG = Logger(service="mangum")


def get_bucket() -> Bucket:
    session = boto3.Session()
    return session.resource("s3").Bucket(config.BUCKET)  # type: ignore


def upload_github_event_json_to_s3(
    event: str,
    action: str,
    headers: dict,
    payload: dict,
):
    bucket = get_bucket()
    ts = time.time()
    key = f"payload/{ts}_{event}_{action}.json"
    json_data = {
        "headers": headers,
        "payload": payload,
    }
    bucket.put_object(
        Key=key,
        Body=json.dumps(json_data),
    )
    LOG.info(f"Uploaded {key} to S3")
