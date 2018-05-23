import smtplib
import argparse
import json
import bson
import logging

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.headerregistry import Address

from flask import request, jsonify
from email_api import app, SETTINGS_FILE
from email_api.models import MongoCollection


TEMPLATE_EMAIL_PATH = "./cerberus-fluid.html"

logger = logging.getLogger(__name__)

## Utiliy functions

def read_email_template(path: str=TEMPLATE_EMAIL_PATH) -> str:
    with open(path, 'r') as fhandler:
        raw_html = fhandler.read()
    return raw_html

def format_email(body: str, key: str) -> str:
    return body.format(api_key=key)


## App routes

@app.route('/send_email', methods=["POST"])
def send_email():
    if not request.form.get('cf') == '42':
        logger.warning("Unauthorized access in send_email")
        return jsonify({'status': 'ko', 'reason': 'unauthorized access'})
    id = request.form.get('id', None)
    if not id:
        logger.debug("Missing parameters in call to send_email")
        return jsonify({'status': 'ko', 'reason': 'missing parameters'})
    oid = bson.ObjectId(id)
    db = MongoCollection('fitness_centers', 'centralefitness', 'localhost', 27017)
    res = db.collection.find_one({'_id': oid})
    with open(SETTINGS_FILE, 'r') as fhandler:
        data = json.load(fhandler).get('smtp', dict())
    sender = Address(data['name'], data['username'], data['domain'])
    recipient = "{} <{}>".format(res['name'], res['email'])
    body_html = format_email(read_email_template(), res['apiKey'])
    message = MIMEMultipart('alternative')
    message['From'] = str(sender)
    message['To'] = recipient
    message['Subject'] = "Votre clé d'API Centrale Fitness"
    message.attach(MIMEText(body_html, 'html'))
    with smtplib.SMTP(data['host'], data['port']) as smtp:
        smtp.starttls()
        smtp.login("{}@{}".format(data['username'], data['domain']), data['pass'])
        smtp.send_message(message)
        logger.info("API key email sent to {}".format(res['email']))
    return jsonify({'status': 'ok'})
