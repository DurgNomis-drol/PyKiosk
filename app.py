from flask import Flask, render_template, redirect, url_for, request
from flask_restful import Api, Resource
from flask_httpauth import HTTPTokenAuth

from kiosk import ChromeWebKiosk
from utils import *
from pathlib import Path

""" TODO """
# 1: Gesture control. Go to homepage, go back? Is it done?
# 2: Screen dimming?
# 3: Reset to homepage after sometime
# 4: Better web control page.
# 5: Better security.
# 6: Error handling, custom logger?


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
            return json.dumps(response, indent=INDENT), 200, HEADER
        else:
            return json.dumps(ERROR_MISSING_CONFIG, indent=INDENT), 200, HEADER


class System(Resource):

    @auth.login_required
    def get(self):
        system = 'uname -a'
        capacity = "cat /sys/class/power_supply/BATC/capacity"
        status = "cat /sys/class/power_supply/BATC/status"

        info = subprocess.run(system.split(), stdout=subprocess.PIPE)

        battery_capacity = subprocess.run(capacity.split(), stdout=subprocess.PIPE)

        battery_status = subprocess.run(status.split(), stdout=subprocess.PIPE)

        response = RESPONSE_SUCCESS
        response.update({
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
        })

        return json.dumps(response, indent=INDENT), 200, HEADER

    @auth.login_required
    def post(self, service):
        if service in config[SERVICES]:
            command = 'systemctl ' + service
            output = execute_command(command)
            if output:
                return json.dumps(RESPONSE_SUCCESS, indent=INDENT), 200, HEADER
            else:
                response = RESPONSE_FAILED
                response.update({
                    'message': output
                })
                return json.dumps(response, indent=INDENT), 200, HEADER
        else:
            return json.dumps(ERROR_NOT_ENABLED, indent=INDENT), 200, HEADER


class Kiosk(Resource):

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
                return json.dumps(response, indent=INDENT), 200, HEADER
            else:
                return json.dumps(RESPONSE_FAILED, indent=INDENT), 200, HEADER
        else:
            url = content['url']
            if kiosk.open_page(url):
                response.update({
                    'url_opened': url
                })
                return json.dumps(response, indent=INDENT), 200, HEADER
            else:
                return json.dumps(RESPONSE_FAILED, indent=INDENT), 200, HEADER

    @auth.login_required
    def delete(self):
        if kiosk.close_page():
            return json.dumps(RESPONSE_SUCCESS, indent=INDENT), 200, HEADER
        else:
            return json.dumps(RESPONSE_FAILED, indent=INDENT), 200, HEADER


api.add_resource(Config, REST_ENDPOINT + '/config')
api.add_resource(System, REST_ENDPOINT + '/system', REST_ENDPOINT + '/system/<string:service>')
api.add_resource(Kiosk, REST_ENDPOINT + '/kiosk')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=config[PORT], debug=False)
