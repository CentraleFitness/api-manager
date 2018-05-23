
import json
from email_api import app, SETTINGS_FILE

def main():
    with open(SETTINGS_FILE, 'r') as fhandler:
        data = json.load(fhandler)
    app.run(data['host'], data['port'])

if __name__ == "__main__":
    main()
