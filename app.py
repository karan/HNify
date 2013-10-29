#!/bin/env python

from flask import Flask, jsonify, make_response
from hn import HN

app = Flask(__name__)

@app.route('/')
def index():
    '''
    This page is displayed when index page is requested.
    '''
    return '''<b>Check out <a href="https://github.com/thekarangoel/HNify">HNify on Github</a>.</b>'''

@app.route('/get/top', methods = ['GET'])
def get_top():
    '''
    Returns stories from the front page of HN.
    '''
    hn = HN()
    return jsonify({'stories': hn.get_stories()})

@app.route('/get/<story_type>', methods = ['GET'])
def get_stories(story_type):
    '''
    Returns stories from the requested page of HN.
    story_type is one of:
    \tnewest
    \tbest
    '''
    hn = HN()
    return jsonify({'stories': hn.get_stories(story_type=story_type)})

@app.errorhandler(404)
def not_found(error):
    '''
    Returns a jsonified 404 error message instead of a HTTP 404 error.
    '''
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.errorhandler(503)
def not_found(error):
    '''
    Returns a jsonified 503 error message instead of a HTTP 404 error.
    '''
    return make_response(jsonify( { 'error': 'Request times out' } ), 503)

if __name__ == '__main__':
    app.run(debug=True)