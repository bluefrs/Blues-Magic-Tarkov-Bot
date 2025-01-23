import json
import os

CONFIG_FILE = os.path.join(os.path.expanduser("~"), "Documents", "Blues_Magic_Tarkov_Bot", "config.json")

# Function to ensure the bot's directory exists
def ensure_bot_directory():
    bot_dir = os.path.dirname(CONFIG_FILE)
    if not os.path.exists(bot_dir):
        os.makedirs(bot_dir)
        print(f"Created directory: {bot_dir}")
        with open(CONFIG_FILE, 'w') as config_file:
            json.dump({}, config_file)  # Create empty config file

def save_config(bot_token, channel_name):
    config_data = {'bot_token': bot_token, 'channel_name': channel_name}
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(config_data, config_file)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as config_file:
            config_data = json.load(config_file)
            return config_data.get('bot_token'), config_data.get('channel_name')
    return None, None