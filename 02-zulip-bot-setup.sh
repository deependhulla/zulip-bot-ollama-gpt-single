#!/bin/bash

/bin/cp -pRv zulip-bot-connect-ollama /opt/

cd /opt/zulip-bot-connect-ollama
python3 -m venv env
source env/bin/activate
pip install -q -r requirements.txt -U
/bin/cp -p dot-env-sample .env
/bin/cp -p dot-zuliprc-example .zuliprc

echo " Update the zulip config info in /opt/zulip-bot-connect-ollama/.zuliprc";

echo "To Start Bot run : /opt/zulip-bot-connect-ollama/start-bot.sh";
