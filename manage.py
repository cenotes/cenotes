import json
from datetime import date
from urllib.parse import unquote

import functools
from flask_migrate import MigrateCommand
from flask_script import Manager

from cenotes import create_app
from cenotes.api import craft_response, CENParams
from cenotes.models import Note

manager = Manager(create_app)
manager.add_option("-c", "--config", dest="app_settings", required=False)
manager.add_command('db', MigrateCommand)


def show_json_request_format(indent=False):
    func = functools.partial(json.dumps, indent=4) if indent else json.dumps
    return func(CENParams(plaintext="", key="",
                          expiration_date=date.today().isoformat(),
                          visits_count=0, max_visits=0).__dict__)


def show_json_response_format(indent=False):
    func = functools.partial(json.dumps, indent=4) if indent else json.dumps
    return func(craft_response(
        error="", success=True, plaintext="", key="", dkey="",
        payload="ciphertext",
        enote=Note(payload="ciphertext", expiration_date=date.today())))


def list_url_endpoints():
    output = []
    for rule in manager.app.url_map.iter_rules():
        if rule.endpoint == "static":
            continue
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        line = unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, rule))
        output.append(line)
    return output


@manager.option('--response', dest="response", action="store_true", default=False)
@manager.option('--request', dest="request", action="store_true", default=False)
@manager.option('--both', dest="both", action="store_true", default=False)
def api(response, request, both):
    def response_format():
        print("Response format is always like this:\n"
              "(Some fields may be left empty depending on endpoint call)")
        print(show_json_response_format(indent=True))
        print("")

    def request_format():
        print("Request format is always like this:\n"
              "(Some fields may be left empty depending on endpoint call)")
        print(show_json_request_format(indent=True))
        print("")

    if both:
        response = request = True

    if response:
        response_format()
    if request:
        request_format()


@manager.command
def routes():
    for line in sorted(list_url_endpoints()):
        print(line)


if __name__ == '__main__':
    manager.run()
