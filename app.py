from flask import Flask, render_template, redirect, url_for, request
from flask_restful import Api, Resource
from flask_httpauth import HTTPTokenAuth

from kiosk import ChromeWebKiosk
from utils import *
from pathlib import Path

""" TODO """
# 1: Gesture control. Go to homepage, go back? Is it done?


"""Initialize flask."""
app = Flask(__name__, static_folder='static')
auth = HTTPTokenAuth(scheme='Bearer')
api = Api(app)

"""Load config from file."""
conf_file = Path(__file__).parent / CONF_FILE
if not conf_file.exists():
    print("\n * First launch - will generate Bearer token stored in conf.json")
    first_launch()

config = load_config_from_file(conf_file)

print("\n * Config file loaded - {file}".format(file=conf_file))

"""If first launch or token have been deleted, generate a new one."""
if TOKEN not in config:
    # Generate a token if first time running this script
    print(" * No token found, generating a new one...")
    new_token = generate_token()
    config.update({TOKEN: new_token})
    with open(conf_file, 'w') as outfile:
        json.dump(config, outfile, indent=INDENT)
    print(" * New token have been generated! - {token}\n".format(token=new_token))


"""Start webkiosk"""
print(" * Starting webkiosk with url: {url}".format(url=config[KIOSK][KIOSK_URL]))
kiosk = ChromeWebKiosk(config[KIOSK])


"""Flask app below"""

COMMANDS = FEDORA_COMMANDS


@app.route(ROOT)
def index():
    return redirect(url_for('homepage'))


@app.route(HOMEPAGE)
def homepage():
    return render_template(
        "index.html",
        url=config[KIOSK][KIOSK_URL],
        current_url=kiosk.get_current_page(),
        token=config[TOKEN],
        config_file=json.dumps(config, sort_keys=True, indent=INDENT, separators=(',', ': '))
    )


@auth.verify_token
def verify_token(token):
    if token == config[TOKEN]:
        return token


class Config(Resource):

    @auth.login_required
    def post(self):
        content = request.get_json()
        if save_config_to_file(conf_file, content['new_config']):
            response = RESPONSE_SUCCESS
            response.update({
                'message': 'Config saved to file.'
            })
            return response, 200, HEADER
        else:
            return ERROR_MISSING_CONFIG, 200, HEADER


class System(Resource):

    @auth.login_required
    def get(self):
        system = COMMANDS[SYSTEM_INFO]
        capacity = COMMANDS[SYSTEM_BATTERY_CAPACITY]
        status = COMMANDS[SYSTEM_BATTERY_STATUS]

        info = subprocess.run(system.split(), stdout=subprocess.PIPE)

        battery_capacity = subprocess.run(capacity.split(), stdout=subprocess.PIPE)

        battery_status = subprocess.run(status.split(), stdout=subprocess.PIPE)

        response = {
            'success': True,
            'system': {
                'info': str(info.stdout.decode('utf-8').rstrip())},
            'battery': {
                'capacity': int(battery_capacity.stdout.decode('utf-8')),
                'status': str(battery_status.stdout.decode('utf-8').rstrip())},
            'kiosk': {
                'homepage': str(config[KIOSK][KIOSK_URL]),
                'state': str(kiosk.state),
                'since': int(kiosk.since),
                'last_url_opened': str(kiosk.last_url_opened)
            }
        }

        return response, 200, HEADER

    @auth.login_required
    def post(self, service):
        if service in config[SERVICES]:
            output = execute_command(COMMANDS[service])
            if output:
                return RESPONSE_SUCCESS, 200, HEADER
            else:
                response = RESPONSE_FAILED
                response.update({
                    'message': output
                })
                return response, 200, HEADER
        else:
            return ERROR_NOT_ENABLED, 200, HEADER


class Kiosk(Resource):

    @auth.login_required
    def get(self):
        response = {
            'success': True,
            'kiosk': {
                'homepage': str(config[KIOSK][KIOSK_URL]),
                'state': str(kiosk.state),
                'since': int(kiosk.since),
                'last_url_opened': str(kiosk.last_url_opened)
            }
        }

        return response, 200, HEADER

    @auth.login_required
    def post(self):
        content = request.get_json()
        print(content)
        response = RESPONSE_SUCCESS
        if 'homepage' in content:
            if kiosk.open_page(homepage=True):
                response.update({
                    'url_opened': config[KIOSK][KIOSK_URL],
                    'homepage': True
                })
                return response, 200, HEADER
            else:
                return RESPONSE_FAILED, 200, HEADER
        else:
            url = content['url']
            if kiosk.open_page(url):
                response.update({
                    'url_opened': url
                })
                return response, 200, HEADER
            else:
                return RESPONSE_FAILED, 200, HEADER

    @auth.login_required
    def delete(self):
        if kiosk.close_page():
            return RESPONSE_SUCCESS, 200, HEADER
        else:
            return RESPONSE_FAILED, 200, HEADER


api.add_resource(Config, REST_ENDPOINT + '/config')
api.add_resource(System, REST_ENDPOINT + '/system', REST_ENDPOINT + '/system/<string:service>')
api.add_resource(Kiosk, REST_ENDPOINT + '/kiosk')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=config[PORT], debug=False)
