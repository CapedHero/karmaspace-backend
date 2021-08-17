#!/usr/bin/env bash

set -x  # Print each command
set -e  # Exit immediately if a command returns a non-zero status

curl -sL https://git.io/tusk | bash -s -- -b .venv/bin latest
python -m pip install --upgrade pip
python -m pip install -r requirements/locked/prod.txt
