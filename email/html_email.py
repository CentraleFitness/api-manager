import os
from base64 import b64encode
import smtplib
import argparse
import json

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.headerregistry import Address

API_KEY_SIZE = 16
TEMPLATE_EMAIL_PATH = "./cerberus-fluid.html"
EMAIL_RENDER_PATH = "./email-render.html"
SETTINGS_FILE_PATH = "./settings.json"

def entropy_pool(size: int) -> bytes:
    return os.urandom(size)

def generate_API_key() -> str:
    return b64encode(entropy_pool(API_KEY_SIZE)).decode('utf-8')

def read_email_template(path: str=TEMPLATE_EMAIL_PATH) -> str:
    with open(path, 'r') as fhandler:
        raw_html = fhandler.read()
    return raw_html

def format_email(body: str, key: str) -> str:
    return body.format(api_key=key)

def save_email_render(body: str, path: str=EMAIL_RENDER_PATH) -> None:
    with open(path, 'w') as fh:
        fh.write(body)

def main():
    with open(SETTINGS_FILE_PATH, 'r') as fhandler:
        settings = json.load(fhandler)
    sender = Address(
        settings['sender']['name'],
        settings['sender']['user'],
        settings['sender']['domain'])
    recipient = Address(
        settings['recipient']['name'],
        settings['recipient']['user'],
        settings['recipient']['domain'])
    subject = "Test email"
    # BODY_PLAIN_TEXT = "This is a test"
    body_html = format_email(read_email_template(), generate_API_key())
    save_email_render(body_html)
    message = MIMEMultipart('alternative')
    message['From'] = str(sender)
    message['To'] = str(recipient)
    message['Subject'] = subject
    # message.attach(MIMEText(BODY_PLAIN_TEXT, 'plain'))
    message.attach(MIMEText(body_html, 'html'))
    with smtplib.SMTP(settings['smtp']['host'], settings['smtp']['port']) as smtp:
        smtp.starttls()
        smtp.login(settings['smtp']['username'], settings['smtp']['password'])
        smtp.send_message(message)
        print("message sended")

if __name__ == "__main__":
    main()
