from flask import Flask
from flask_cors import CORS

from src import register_bps

app = Flask(__name__)
CORS(app)

register_bps(app)
