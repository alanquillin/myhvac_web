from flask import Flask

app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
