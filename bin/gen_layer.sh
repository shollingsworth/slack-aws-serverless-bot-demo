#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

cd ~/app
poetry export \
    --without-hashes \
    -o /tmp/requirements.txt

cd backend
test -d layer && rm -rfv layer/
mkdir -p layer/python
pip3 install -r /tmp/requirements.txt -t layer/python
