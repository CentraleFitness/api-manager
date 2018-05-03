"""
This script runs the showcase application using a development server.
"""

import sys
import argparse
import json

from showcase import app

def main():
    parser = argparse.ArgumentParser(
        prog='runserver.py',
        description='Restful server')
    parser.add_argument(
        '-s', '--settings',
        action='store',
        type=str,
        default='./settings.json',
        help="path to the .json config file")
    args = parser.parse_args(sys.argv[1:])
    with open(args.settings, 'r') as fhandler:
        data = json.load(fhandler)
    app.run(
        data.get('host', '127.0.0.1'),
        data.get('port', 5540))

if __name__ == '__main__':
    main()
