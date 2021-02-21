import subprocess
import secrets
import json

from const import *


def generate_token():
    token = secrets.token_urlsafe(32)
    return token


def execute_command(command):
    output = subprocess.run(command.split(), stdout=subprocess.PIPE)
    return output


def first_launch():
    with open(CONF_FILE, 'w') as outfile:
        json.dump(DEFAULT_CONFIG, outfile, indent=INDENT)
    return True


def load_config_from_file(file):
    with open(file) as json_file:
        config = json.load(json_file)
    return config


def save_config_to_file(file, new_config):
    if SERVICES in new_config and PORT in new_config and KIOSK in new_config and KIOSK_URL in new_config[KIOSK]:
        # Write config to file
        with open(file, 'w') as outfile:
            json.dump(new_config, outfile, indent=INDENT)
        success = True
        return success
    else:
        success = False
        return success
