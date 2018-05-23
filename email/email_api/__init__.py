""" email_api package """

from flask import Flask

app = Flask(__name__)

SETTINGS_FILE = "./settings.json"

import email_api.views
