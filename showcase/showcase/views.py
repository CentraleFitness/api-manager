"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, jsonify
from showcase import app

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
        city = request.form['city']
        email = request.form['email']
    except KeyError:
        return jsonify({'status': 'ko', 'reason': 'does not meet requirements'})
    # Add city and email to the cluster
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
