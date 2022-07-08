#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Slack interface."""
import json
import logging
import traceback
from typing import Any, Dict

from aws_lambda_powertools.logging.logger import Logger
from api import config
from api.config import DEBUG, LOG_LEVEL, SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET
from api.lib.slack import MessageBuilder
from api.lib.slack_exception import send_exception
from api.routes.slack_subcommands import SUB_CMD_ROUTES, slack_subcommand
from slack_bolt import App
from slack_bolt import BoltContext
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from slack_bolt.context.ack.ack import Ack
from slack_sdk.models.views import View
from slack_sdk.web.client import WebClient

logging.basicConfig(level=logging.INFO)
LOG = Logger(service_name="slack-bot")
LOG.setLevel(LOG_LEVEL)

# process_before_response must be True when running on FaaS
slack_app = App(
    process_before_response=True,
    logger=LOG,
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET,
)


@slack_app.event("app_mention")
def handle_app_mentions(context: BoltContext):
    context.say("What's up?")


@slack_app.event("app_home_opened")
def handle_home(
    event: dict,
    client: WebClient,
    ack: Ack,
):

    ack()
    msg = MessageBuilder()
    msg.add_header("Welcome to the Slack App Home!")
    msg.add_divider()
    msg.add_fields_section(
        [
            (
                "*Getting Started*\n<https://google.com"
                "|Google>\n"
            ),
        ]
    )
    client.views_publish(
        user_id=event["user"],
        view=View(
            type="home",
            blocks=msg.blocks,
        ),
    )


@slack_app.error
def custom_error_handler(error, body, logger):
    tb = traceback.format_exc()
    logger.error(f"Error: {error}")
    logger.error(f"Body: {body}")
    send_exception("Slack Error", error, tb)


@slack_app.command(config.SLACK_SLASH_COMMAND)
def respond_to_slack_within_3_seconds(context: BoltContext, payload: Dict[str, Any]):
    route = payload.get("text", "help")
    if route not in SUB_CMD_ROUTES:
        route = "help"
    return SUB_CMD_ROUTES[route](context, payload)


@slack_subcommand("test_exception")
def test_exception(*args, **kwargs):
    LOG.info("test_exception args: %s, kwargs: %s", args, kwargs)
    raise RuntimeError("This is a test exception")


@slack_subcommand("help")
def help_command(context: BoltContext, payload: Dict[str, Any]):
    context.ack(
        f"""
    *Slack Slash Command Was Executed!*
    Hello <@{{{context.user_id}}}>!
    """
    )
    print(json.dumps(payload, indent=4, separators=(",", " : ")))


SlackRequestHandler.clear_all_log_handlers()


LOG.inject_lambda_context(log_event=DEBUG)  # type: ignore
