from json import loads

from flask import Flask


app = Flask(__name__)


@app.route('/')
def hello():
    print 'Rabbit Season'
    return 'Duck Season'
