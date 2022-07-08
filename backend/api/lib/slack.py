#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Slack Lib."""
from dataclasses import dataclass
from typing import Any, Dict, List

from aws_lambda_powertools.logging import Logger
from api import config
from slack_sdk.models.blocks import Block
from slack_sdk.models.blocks.basic_components import MarkdownTextObject, PlainTextObject
from slack_sdk.models.blocks.block_elements import ButtonElement, ImageElement
from slack_sdk.models.blocks.blocks import (
    DividerBlock,
    HeaderBlock,
    ImageBlock,
    SectionBlock,
)
from slack_sdk.web.client import WebClient

def get_client():
    """Get a client."""
    return WebClient(token=config.SLACK_BOT_TOKEN)


@dataclass
class Icons:
    """Icons."""

    star: str = ":star:"


class MessageBuilder:
    """Message Builder."""
    def __init__(self) -> None:
        self._blocks = []  # type: List[Block]
        self._log = Logger(service="slack", child=True)

    def add_divider(self) -> None:
        self._blocks.append(DividerBlock())

    def add_fields_section(self, markdown_fields: List[str]) -> None:
        self._blocks.append(
            SectionBlock(
                fields=[
                    MarkdownTextObject(
                        text=field,
                    )
                    for field in markdown_fields
                ],
            )
        )

    def add_image(self, title: str, image_url: str) -> None:
        self._blocks.append(
            ImageBlock(
                title=PlainTextObject(
                    text=title,
                ),
                alt_text=title,
                image_url=image_url,
            )
        )

    def add_header(self, text: str) -> None:
        self._blocks.append(
            HeaderBlock(
                text=PlainTextObject(
                    text=text,
                ),
            ),
        )

    def add_markdown(self, text: str, image_url: str = "") -> None:
        if image_url:
            self._blocks.append(
                SectionBlock(
                    text=MarkdownTextObject(
                        text=text,
                    ),
                    accessory=ImageElement(
                        image_url=image_url,
                        alt_text="image",
                    ),
                )
            )
        else:
            self._blocks.append(
                SectionBlock(
                    text=MarkdownTextObject(
                        text=text,
                    ),
                )
            )

    def add_link_section(self, text: str, link: str) -> None:
        self._blocks.append(
            SectionBlock(
                text=MarkdownTextObject(
                    text=text,
                ),
                accessory=ButtonElement(
                    text=PlainTextObject(
                        text="View",
                    ),
                    url=link,
                ),
            )
        )

    @property
    def blocks(self) -> List[Block]:
        for blk in self._blocks:
            blk.validate_json()
        return self._blocks

    def blocks_json(self) -> List[Dict[str, Any]]:
        return [i.to_dict() for i in self.blocks]

    def send(self, slack_id: str, title: str):
        if config.MOCK:
            self._log.info("MOCK: Sending message to %s", slack_id)
            return
        cli = get_client()
        cli.chat_postMessage(
            text=title,
            channel=slack_id,
            blocks=self.blocks,
        )

def all_users():
    members = []
    cli = get_client()
    res = cli.users_list()
    members += res.data['members'] # type: ignore
    while res.get("response_metadata", {}).get("next_cursor"):
        cursor = res.get("response_metadata", {}).get("next_cursor")
        res = cli.users_list(cursor=cursor)
        print(f'fetching {len(res.data["members"])} users') # type: ignore
        members += res.data.get('members', []) # type: ignore
    return members
