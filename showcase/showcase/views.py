"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, jsonify

from showcase import app
from showcase.models import MongoCollection


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/list', methods=['GET'])
def list_gyms():
    data = [
        ['Keep Cool Marseille La Joliette', (43.310449, 5.370846)],
        ['NeoNess Marseille-Vieux Port', (43.299801, 5.370921)]
        ]
    return jsonify(data)

@app.route('/notification', methods=['POST'])
def notification_add_recipient():
    try:
        city = request.form['city'].lower()
        email = request.form['email']
    except KeyError:
        return jsonify({'status': 'ko', 'reason': 'does not meet requirements'})
    db = MongoCollection('proximity_notification', 'centralefitness', 'localhost', 27017)
    ret = db.collection.insert_one({'email': email, 'city': city})
    if ret.acknowledged != True:
        return jsonify({'status': 'ko', 'reason': 'insert failed'})
    return jsonify({'status': 'ok'})

@app.route('/newsletter', methods=['POST'])
def newsletter_add_recipient():
    try:
        # Determine the fields to handle
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
    except KeyError:
        return jsonify({'status': 'ko', 'reason': 'does not meet requirements'})
    # Send the data to the cluster
    return jsonify({'status': 'ok'})
