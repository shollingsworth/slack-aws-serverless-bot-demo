#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""."""
from aws_lambda_powertools.logging import Logger
from api import config
from api.lib.slack import MessageBuilder
import requests

LOG = Logger(service="mangum")


def send_exception(title: str, _err: Exception, tb: str) -> None:
    """Send exception to slack."""
    message = MessageBuilder()

    subtitle = f"{_err.__class__.__name__}: {_err}"
    message.add_header(title)
    # last 1000 characters of the traceback
    tb = tb[-1000:]
    tb_txt = f"```{tb}```"
    message.add_divider()
    message.add_markdown(f'*{subtitle}*')
    message.add_divider()
    message.add_markdown(tb_txt)
    url = config.SLACK_EXCEPTIONS_WEBHOOK
    headers = {"Content-Type": "application/json"}
    data = {"blocks": message.blocks_json()}
    LOG.debug("Sending exception to slack: %s", data)
    try:
        LOG.debug("Data: %s", data)
        res = requests.post(url, json=data, headers=headers)
        LOG.debug("Response from slack: %s", res.text)
    except Exception as _err:
        LOG.error("Failed to send exception to slack: %s", _err)

async def async_send_exception(title: str, _err: Exception, tb: str) -> None:
    """Send exception to slack."""
    send_exception(title, _err, tb)
