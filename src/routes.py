from flask import render_template
from app import app


@app.route('/')
def index():
    return render_template('main.html')
    return 'Hello World!'


@app.route('/room/<room>')
def getRoomDetails(room):
    return 'Details for room: %s' % room