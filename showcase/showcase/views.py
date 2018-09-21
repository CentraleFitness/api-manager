"""
Routes and views for the flask application.
"""

import json

from datetime import datetime
from flask import request

from showcase import app
from showcase.models import MongoCollection
from showcase.content import render_json_resp


@app.route('/list', methods=['GET'])
def list_gyms():
    data = [
        ['Keep Cool Marseille La Joliette', (43.310449, 5.370846)],
        ['NeoNess Marseille-Vieux Port', (43.299801, 5.370921)]
        ]
    return render_json_resp(data=data)

@app.route('/notification', methods=['POST'])
def notification_add_recipient():
    try:
        raw_data = request.data.decode('utf-8')
        json_data = json.loads(raw_data).get('user')
        city = json_data['city'].lower()
        email = json_data['email']
    except KeyError:
        return render_json_resp(status_code=400)
    db = MongoCollection(
        'proximity_notification',
        'centralefitness',
        'localhost', 27017)
    ret = db.collection.insert_one({'email': email, 'city': city})
    if ret.acknowledged != True:
        return render_json_resp(status_code=500, reason='insert failed')
    return render_json_resp()

@app.route('/newsletter', methods=['POST'])
def newsletter_add_recipient():
    try:
        raw_data = request.data.decode('utf-8')
        json_data = json.loads(raw_data).get('user')
        firstname = json_data['firstname']
        lastname = json_data['lastname']
        email = json_data['email']
    except KeyError:
        return render_json_resp(status_code=400)
    # Send the data to the cluster
    return render_json_resp()
