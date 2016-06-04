from flask import render_template

from app import app

import logging

LOG = logging.getLogger(__name__)


@app.route('/')
def dashboard():
    return render_template('dashboard.html')

