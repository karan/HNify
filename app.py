#!/usr/bin/env python

from flask import Flask, jsonify, make_response
from hn import HN
import time

app = Flask(__name__)
temp_cache = {'top' : {'response_json' : None,
                       'time' : time.time()},
              'best' : {'response_json' : None,
                       'time' : time.time()},
              'newest' : {'response_json' : None,
                       'time' : time.time()}}
timeout = 300

@app.route('/')
def index():
    '''
    This page is displayed when index page is requested.
    '''
    return '''<b>Check out <a href="https://github.com/karan/HNify">HNify on Github</a>.</b>'''

@app.route('/get/top', methods = ['GET'])
def get_top():
    '''
    Returns stories from the front page of HN.
    '''
    if temp_cache['top']['response_json'] is not None \
       and temp_cache['top']['time'] + timeout < time.time():
        return temp_cache['top']['response_json']
    else:
        hn = HN()
        temp_cache['top']['response_json'] = jsonify({'stories': hn.get_stories()})
        temp_cache['top']['time'] = time.time()
        return temp_cache['top']['response_json']

@app.route('/get/<story_type>', methods = ['GET'])
def get_stories(story_type):
    '''
    Returns stories from the requested page of HN.
    story_type is one of:
    \tnewest
    \tbest
    '''
    if temp_cache[story_type]['response_json'] is not None \
       and temp_cache[story_type]['time'] + timeout < time.time():
        return temp_cache[story_type]['response_json']
    else:
        hn = HN()
        temp_cache[story_type]['response_json'] = jsonify({'stories': hn.get_stories(story_type=story_type)})
        temp_cache[story_type]['time'] = time.time()
        return temp_cache[story_type]['response_json']

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
