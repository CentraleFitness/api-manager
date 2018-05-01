"""
This script runs the showcase application using a development server.
"""

import json

from showcase import app

def main():
    with open('settings.json', 'r') as fhandler:
        data = json.load(fhandler)
    app.run(
        data.get('host', '127.0.0.1'),
        data.get('port', 5540))

if __name__ == '__main__':
    main()
