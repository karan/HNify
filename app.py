#!/bin/env python

from flask import Flask, jsonify, make_response
from hn import HN

app = Flask(__name__)

@app.route('/')
def index():
    return "<b>Check out <a href=\"https://github.com/thekarangoel/HNify\">HNify on Github</a>.</b>"

@app.route('/get/top', methods = ['GET'])
def get_top():
    hn = HN()
    return jsonify({'stories': hn.get_stories()})

@app.route('/get/<story_type>', methods = ['GET'])
def get_stories(story_type):
    hn = HN()
    return jsonify({'stories': hn.get_stories(story_type=story_type)})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

if __name__ == '__main__':
    app.run(debug=True)