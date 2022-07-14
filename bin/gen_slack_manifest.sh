#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.."
DIR="$(readlink -f "$DIR")"
CONF="${DIR}/config.json"
SCONF="${DIR}/serverless.json"

APP_NAME="$(jq -r '.slack_app_name' "$CONF")"
APP_DESCRIPTION="$(jq -r '.slack_app_description' "$CONF")"
APP_SLACK_COMMAND="$(jq -r '.slack_slash_command' "$CONF")"
URL="$(jq -r '.HttpApiUrl' "$SCONF")"


TEMPLATE=$(cat <<EOF
display_information:
  name: "${APP_NAME}"
  description: "${APP_DESCRIPTION}"
  background_color: "#383038"
features:
  app_home:
    home_tab_enabled: true
    messages_tab_enabled: true
    messages_tab_read_only_enabled: false
  bot_user:
    display_name: "${APP_NAME} Bot"
    always_online: true
  slash_commands:
    - command: /${APP_SLACK_COMMAND}
      url: ${URL}/slack/events
      description: Placeholder
      usage_hint: new | help
      should_escape: false
oauth_config:
  scopes:
    bot:
      - app_mentions:read
      - chat:write
      - commands
      - groups:read
      - groups:write
      - pins:write
      - pins:read
      - incoming-webhook
      - team:read
      - users:read
      - users:read.email
settings:
  event_subscriptions:
    request_url: ${URL}/slack/events
    bot_events:
      - app_home_opened
      - app_mention
  interactivity:
    is_enabled: true
    request_url: ${URL}/slack/events
    message_menu_options_url: ${URL}/slack/events
  org_deploy_enabled: false
  socket_mode_enabled: false
  token_rotation_enabled: false
EOF
)

echo "${TEMPLATE}"
