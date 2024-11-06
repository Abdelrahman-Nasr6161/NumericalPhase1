from flask import Flask , render_template , request
from flask.json import jsonify
import requests
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify("hello")