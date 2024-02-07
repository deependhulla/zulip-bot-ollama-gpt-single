#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR" || exit

source env/bin/activate

python zulip-ollama-direct-bot.py >/var/log/zulip-ollama-direct-bot.log 2>&1 &
echo "Started zulip-ollama-direct-bot.py"

echo "For Log check : /var/log/zulip-ollama-direct-bot.log"
