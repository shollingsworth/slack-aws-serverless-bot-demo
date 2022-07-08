#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Root Handler."""
from aws_lambda_powertools.logging import Logger
from api.routes.slack import slack_app
from slack_bolt.adapter.aws_lambda import SlackRequestHandler


LOG = Logger(service="mangum")


def handler(event, context):
    # Warmer
    if event.get("source") == "serverless-plugin-warmup":
        LOG.info("WarmUp - Lambda is warm!")
        return {}

    # Slack Request Handler
    if event.get("rawPath", "") == "/slack/events":
        slack_handler = SlackRequestHandler(app=slack_app)
        return slack_handler.handle(event, context)

    return {"statusCode": 200, "body": "ack"}
