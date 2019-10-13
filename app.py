from flask import Flask
from src import register_bps

app = Flask(__name__)
register_bps(app)
