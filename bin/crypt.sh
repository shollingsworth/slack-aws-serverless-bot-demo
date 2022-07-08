#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.."
DIR="$(readlink -f "$DIR")"
SEC_JSON=$(readlink -f "$DIR/.secrets.json")
CONF="${DIR}/config.json"
PREFIX="$(jq -r '.application_namespace' "$CONF")"
if [[ "${PREFIX}" == "null" ]]; then
    echo "application_namespace is not set in config.json"
    exit 1
fi

PARAM_NAME="/${PREFIX}/secrets.json"

SEC_TEMPLATE=$(cat <<EOF
{
  "SLACK_BOT_TOKEN": "",
  "SLACK_APP_ID": "",
  "SLACK_CLIENT_SECRET": "",
  "SLACK_CLIENT_ID": "",
  "SLACK_SIGNING_SECRET": "",
  "SLACK_WEBHOOK": "",
  "SLACK_EXCEPTIONS_WEBHOOK": ""
}
EOF
)



get_secret_config() {
    aws \
        ssm \
        get-parameter --name \
        "$PARAM_NAME" \
        --query 'Parameter.Value' \
        --output text \
        --with-decryption | tee "$SEC_JSON"
}

edit_config() {
    tfile=$(mktemp)
    trap 'rm -f $tfile' EXIT
    aws \
        ssm \
        get-parameter --name \
        "${PARAM_NAME}" \
        --query 'Parameter.Value' \
        --output text \
        --with-decryption | tee "${tfile}"


    vim "${tfile}"
    aws \
        ssm \
        put-parameter \
        --name \
        "${PARAM_NAME}" \
        --value "$(cat "${tfile}")" \
        --type SecureString \
        --overwrite | tee
}

put_secret_config() {
    if [[ -f "$SEC_JSON" ]]; then
        echo "Using existing secrets file: $SEC_JSON"
    else
        echo "Creating new blank secrets file: $SEC_JSON"
        echo "$SEC_TEMPLATE" > "$SEC_JSON"
    fi
    aws \
        ssm \
        put-parameter \
        --name \
        "${PARAM_NAME}" \
        --value "$(cat "${SEC_JSON}")" \
        --type SecureString \
        --overwrite | tee
}

action="${1:-}"

usage() {
    echo "Usage: $0 [get|edit|save]"
    echo "  get: get the secrets from SSM"
    echo "  edit: edit the secrets in vim"
    echo "  save: save .secrets.json to SSM"
}


case "$action" in
    get)
        get_secret_config
        ;;
    edit)
        edit_config
        ;;
    save)
        put_secret_config
        ;;
    *)
        usage
        ;;
esac
