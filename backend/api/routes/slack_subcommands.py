#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Slack Subcommands."""
from functools import wraps

SUB_CMD_ROUTES = {}

def slack_subcommand(route_name: str):
    """Decorator for slack subcommands."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        SUB_CMD_ROUTES[route_name] = wrapper
        return wrapper
    return decorator
