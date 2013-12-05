#!/usr/bin/env python

import time

from hn import HN
from flask import Flask, jsonify, make_response, render_template, redirect

app = Flask(__name__)
temp_cache = {
    'top': {
        'response_json' : None,
        'time' : time.time()
        },
    'best': {
        'response_json' : None,
        'time' : time.time()
        },
    'newest': {
        'response_json' : None,
        'time' : time.time()
        }
    }

# cache time to live in seconds
timeout = 300

@app.route('/')
def index():
    '''
    This page is displayed when index page is requested.
    '''
    return render_template('main.html')

@app.route('/get/top', methods = ['GET'])
def get_top():
    '''
    Returns stories from the front page of HN.
    '''
    if temp_cache['top']['response_json'] is not None \
       and temp_cache['top']['time'] + timeout < time.time():
        return jsonify(temp_cache['top']['response_json'])
    else:
        hn = HN()
        temp_cache['top']['response_json'] = {'stories': hn.get_stories()}
        temp_cache['top']['time'] = time.time()
        return jsonify(temp_cache['top']['response_json'])

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
        temp_cache[story_type]['response_json'] = {'stories': hn.get_stories(story_type=story_type)}
        temp_cache[story_type]['time'] = time.time()
        return jsonify(temp_cache[story_type]['response_json'])

@app.errorhandler(404)
def not_found(error):
    '''
    Returns a jsonified 404 error message instead of a HTTP 404 error.
    '''
    return make_response(jsonify({ 'steve_martin': 'A day without sunshine is like, you know, night.' }), 404)

@app.errorhandler(503)
def not_found(error):
    '''
    Returns a jsonified 503 error message instead of a HTTP 404 error.
    '''
    return make_response(jsonify({ 'einstein': 'If the facts don\'t fit the theory, change the facts.' }), 503)

if __name__ == '__main__':
    app.run(debug=True)
