import os
import logging
import re
import ollama
import zulip
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Set up logging
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)

# Set up Zulip client
client = zulip.Client(config_file=".zuliprc")

# Environment variables
DEFAULT_MODEL_NAME = os.environ.get('DEFAULT_MODEL_NAME', 'tinyllama')
BOT_NAME = os.environ['BOT_NAME']

def send_reply(reply, message):
    response = {
        'type': message['type'],
        'to': message['sender_email'] if message['type'] == 'private' else message['display_recipient'],
        'content': reply,
    }
    if message['type'] != 'private':
        response['subject'] = message['subject']
    client.send_message(response)

def get_ollama_response(content, model=DEFAULT_MODEL_NAME):
    try:
        response = ollama.chat(model=model, messages=[{'role': 'user', 'content': content}])
        return response['message']['content'].strip()
    except Exception as e:
        logging.error(e)
        return "Ollama API error. Please try again later."

def handle_message(event):
    if event['type'] != 'message':
        return

    msg = event['message']
    content = msg['content'].strip()

    if msg['sender_email'] == client.email:
#        logging.debug("Ignoring message sent by myself")
        return

    # Process and strip bot mention
    content = re.sub("@\*\*{}[^\*]+\*\*".format(BOT_NAME), "", content, flags=re.IGNORECASE).strip()

    # Fetch response from Ollama
    response = get_ollama_response(content)
    send_reply(response, msg)

def main():
    logging.info("Starting the Ollama Zulip bot named: {}".format(BOT_NAME))
    client.call_on_each_event(handle_message, event_types=['message'])

if __name__ == "__main__":
    main()

