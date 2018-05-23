
import json
import logging.config

from email_api import app, SETTINGS_FILE

def main():
    with open(SETTINGS_FILE, 'r') as fhandler:
        data = json.load(fhandler)
    logging.config.dictConfig(data['logging_dict'])
    app.run(data['host'], data['port'])

if __name__ == "__main__":
    main()
